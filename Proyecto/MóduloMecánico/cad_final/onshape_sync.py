"""Uploads the cad_final STEP files to Onshape through the REST API (no browser).

    python cad_final/onshape_sync.py --init "LanternGuard CAD final"      crea el documento (1 llamada)
    python cad_final/onshape_sync.py --subir salida/preliminar/step salida/boya/step
    python cad_final/onshape_sync.py --actualizar M9                     solo esa pieza (M3 = las 4 del riel)
    python cad_final/onshape_sync.py --ensamble 200                      salida/ensambles/ensamble_D200.step, aplanado
    python cad_final/onshape_sync.py --subir ... --dry-run               qué haría y cuántas llamadas, sin llamar
    python cad_final/onshape_sync.py --cuenta                            llamadas gastadas este año

Keys come from ../.env (ONSHAPE_ACCESS_KEY, ONSHAPE_SECRET_KEY), never from this file. Endpoints checked against the
official OpenAPI spec (cad.onshape.com/api/openapi) and onshape-public.github.io/docs:
    POST /documents                                  createDocument -> id, defaultWorkspace.id
    POST /blobelements/d/{did}/w/{wid}               uploadFileCreateElement (multipart) -> id, translationId
    POST /blobelements/d/{did}/w/{wid}/e/{eid}       uploadFileUpdateElement (multipart) -> id, translationId
    GET  /translations/{tid}                         getTranslation -> requestState ACTIVE/DONE/FAILED, resultElementIds
Every request is appended to onshape_calls.log; Onshape only bills 2xx/3xx responses (EDU Student: 2500 per year).
A file whose content (line endings ignored) has not changed since its last upload is skipped; --forzar uploads it anyway.
"""
import argparse
import base64
import datetime as dt
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ENV_FILE = ROOT / ".env"
CONFIG = HERE / "onshape_config.json"
MAP = HERE / "onshape_map.json"
CALLS_LOG = HERE / "onshape_calls.log"
STEP_DIRS = ("salida/preliminar/step", "salida/boya/step")
ENSAMBLE = "salida/ensambles/ensamble_D{}.step"

API = "https://cad.onshape.com/api/v10"
YEAR_LIMIT = 2500
POLL_S = 5            # seconds between translation status checks (user rule)
POLL_MAX = 60         # 5 min per file, then give up and report
POLLS_ESTIMATE = 4    # for --dry-run: a small STEP usually translates in 10 to 20 s


class OnshapeError(RuntimeError):
    pass


def load_keys():
    if not ENV_FILE.exists():
        raise OnshapeError(f"falta {ENV_FILE} con ONSHAPE_ACCESS_KEY y ONSHAPE_SECRET_KEY")
    env = {}
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    try:
        return env["ONSHAPE_ACCESS_KEY"], env["ONSHAPE_SECRET_KEY"]
    except KeyError as e:
        raise OnshapeError(f"falta {e.args[0]} en {ENV_FILE}") from None


def year_total():
    year = str(dt.date.today().year)
    if not CALLS_LOG.exists():
        return 0
    return sum(1 for line in CALLS_LOG.read_text(encoding="utf-8").splitlines()
               if line.startswith(year) and line.endswith("\tsi"))


def log_call(method, path, status):
    billed = "si" if 200 <= status < 400 else "no"
    with open(CALLS_LOG, "a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now().isoformat(timespec='seconds')}\t{method}\t{path}\t{status}\t{billed}\n")


def multipart(fields, file_path):
    boundary = uuid.uuid4().hex
    out = bytearray()
    for k, v in fields.items():
        out += f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    out += (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{file_path.name}"\r\n'
            f'Content-Type: application/octet-stream\r\n\r\n').encode()
    out += file_path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    return bytes(out), f"multipart/form-data; boundary={boundary}"


class Client:
    def __init__(self):
        access, secret = load_keys()
        self.auth = "Basic " + base64.b64encode(f"{access}:{secret}".encode()).decode()

    def call(self, method, path, body=None, content_type="application/json"):
        if isinstance(body, dict):
            body = json.dumps(body).encode()
        req = urllib.request.Request(API + path, data=body, method=method, headers={
            "Authorization": self.auth, "Accept": "application/json;charset=UTF-8; qs=0.09",
            **({"Content-Type": content_type} if body is not None else {})})
        for attempt in range(2):
            try:
                with urllib.request.urlopen(req, timeout=120) as r:
                    log_call(method, path, r.status)
                    return json.loads(r.read() or b"{}")
            except urllib.error.HTTPError as e:
                log_call(method, path, e.code)
                detail = e.read().decode(errors="replace")[:300]
                if e.code == 429 and attempt == 0:
                    wait = int(e.headers.get("Retry-After") or 30)
                    print(f"  429 (demasiadas llamadas), espero {wait} s")
                    time.sleep(wait)
                    continue
                if e.code == 402:
                    raise OnshapeError("402: se acabó el cupo anual de llamadas de la API") from None
                raise OnshapeError(f"{method} {path} -> {e.code}: {detail}") from None

    def wait_translation(self, tid):
        for _ in range(POLL_MAX):
            time.sleep(POLL_S)
            t = self.call("GET", f"/translations/{tid}")
            if t.get("requestState") != "ACTIVE":
                return t
        raise OnshapeError(f"la traducción {tid} sigue ACTIVE después de {POLL_S * POLL_MAX} s")


def read_json(p, default):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def write_json(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def content_hash(p):
    # Windows checkouts turn LF into CRLF: the geometry is the same, so it must not trigger an upload
    return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def rel(p):
    return p.resolve().relative_to(ROOT).as_posix()


def doc_url(cfg):
    return f"https://cad.onshape.com/documents/{cfg['documentId']}/w/{cfg['workspaceId']}"


def cmd_init(name, dry, force):
    if CONFIG.exists() and not force:
        cfg = read_json(CONFIG, {})
        print(f"Ya hay documento en {CONFIG.name}: {doc_url(cfg)}\n(--forzar crea otro y reemplaza la config)")
        return 0
    if dry:
        print(f'[dry-run] POST /documents "{name}": 1 llamada')
        return 0
    d = Client().call("POST", "/documents", {"name": name, "isPublic": False})
    cfg = {"name": name, "documentId": d["id"], "workspaceId": d["defaultWorkspace"]["id"]}
    cfg["url"] = doc_url(cfg)
    write_json(CONFIG, cfg)
    write_json(MAP, {})
    print(f"Documento creado: {cfg['url']}")
    return 0


def plan_files(files, mapping, force):
    plan = []
    for f in files:
        entry = mapping.get(f.stem)
        if entry and entry.get("sha256") == content_hash(f) and not force:
            plan.append((f, "igual"))
        else:
            plan.append((f, "actualizar" if entry else "crear"))
    return plan


def upload(client, cfg, mapping, f, action, flatten):
    """crear: new STEP tab + its translated Part Studio. actualizar: only replaces the file in the existing STEP tab.

    Tested on 29/10 with M7: re-uploading with translate=true makes a second Part Studio (assemblies keep pointing at the
    old one), and with translate=false the old Part Studio does not refresh. The API has no equivalent of the
    "Update..." menu, so after "actualizar" that step is done by hand in Onshape (ONSHAPE.md).
    """
    did, wid = cfg["documentId"], cfg["workspaceId"]
    new = action == "crear"
    fields = {"encodedFilename": f.name, "translate": str(new).lower(), "storeInDocument": "true"}
    if new:
        fields |= {"importWithinDocument": "true", "yAxisIsUp": "false", "flattenAssemblies": str(flatten).lower()}
    body, ctype = multipart(fields, f)
    old = mapping.get(f.stem, {})
    path = f"/blobelements/d/{did}/w/{wid}" + ("" if new else f"/e/{old['blobElementId']}")
    r = client.call("POST", path, body, ctype)
    t = client.wait_translation(r["translationId"]) if new else {"requestState": "FALTA_UPDATE_EN_ONSHAPE"}
    state = t.get("requestState")
    results = t.get("resultElementIds") or old.get("partStudioIds", [])
    mapping[f.stem] = {"file": rel(f), "sha256": content_hash(f), "blobElementId": r["id"], "partStudioIds": results,
                       "translationId": r.get("translationId") if new else old.get("translationId"),
                       "estado": state, "fecha": dt.datetime.now().isoformat(timespec="seconds")}
    write_json(MAP, mapping)  # after every file, so an interrupted run keeps what it already uploaded
    if new and state != "DONE":
        raise OnshapeError(f"{f.name}: traducción {state}: {t.get('failureReason')}")
    return results


def cmd_upload(files, dry, force, flatten=False):
    if not CONFIG.exists() and not dry:
        print("Primero: --init \"<nombre>\"")
        return 1
    cfg, mapping = read_json(CONFIG, {}), read_json(MAP, {})
    plan = plan_files(files, mapping, force)
    todo = [(f, a) for f, a in plan if a != "igual"]
    est = sum(2 + POLLS_ESTIMATE if a == "crear" else 1 for _, a in todo)  # crear: POST + polls; actualizar: POST
    used = year_total()
    for f, a in plan:
        print(f"  {a:10s} {rel(f)}")
    print(f"{len(todo)} de {len(plan)} archivos para subir, ≈ {est} llamadas. Gastadas este año: {used} de {YEAR_LIMIT}.")
    if used + est > YEAR_LIMIT:
        print("No alcanza el cupo anual: no subo nada.")
        return 1
    if dry or not todo:
        return 0
    client, t0, n0, ok = Client(), time.time(), used, True
    for f, a in todo:
        try:
            ps = upload(client, cfg, mapping, f, a, flatten)
            print(f"OK    {f.stem:24s} {a:10s} Part Studio {', '.join(ps) or '-'}")
        except OnshapeError as e:
            ok = False
            print(f"FALLA {f.stem:24s} {e}")
            if "402" in str(e):
                break
    print(f"{'TODO BIEN' if ok else 'HUBO FALLAS'} en {time.time() - t0:.0f} s, {year_total() - n0} llamadas "
          f"(año: {year_total()} de {YEAR_LIMIT}). Documento: {cfg['url']}")
    pending = [f.stem for f, a in todo if a == "actualizar" and mapping.get(f.stem, {}).get("sha256") == content_hash(f)]
    if pending:
        print("FALTA EN ONSHAPE (a mano, ONSHAPE.md): clic derecho en la pestaña del Part Studio → Update... y elegir "
              "el STEP nuevo, para: " + ", ".join(pending))
    return 0 if ok else 1


def find_piece(code):
    found = [f for d in STEP_DIRS for f in sorted((ROOT / d).glob("*.step"))
             if f.stem.lower() == code.lower() or f.stem.lower().startswith(code.lower() + "_")]
    if not found:
        raise OnshapeError(f"no hay STEP de {code} en {', '.join(STEP_DIRS)}")
    return found


def main():
    ap = argparse.ArgumentParser(description="Sube los STEP de cad_final a Onshape por la API")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--init", metavar="NOMBRE", help="crea el documento y guarda onshape_config.json")
    g.add_argument("--subir", nargs="+", metavar="CARPETA", help="sube o actualiza cada .step de esas carpetas")
    g.add_argument("--actualizar", metavar="PIEZA", help="solo esa pieza, por ejemplo M9 o B5b")
    g.add_argument("--ensamble", metavar="ARO", choices=("100", "200", "300", "500"), help="ensamble_D<ARO>.step aplanado")
    g.add_argument("--cuenta", action="store_true", help="llamadas gastadas este año")
    ap.add_argument("--dry-run", action="store_true", help="muestra el plan y las llamadas, sin llamar")
    ap.add_argument("--forzar", action="store_true", help="sube aunque el archivo no haya cambiado")
    a = ap.parse_args()
    try:
        if a.cuenta:
            print(f"{year_total()} de {YEAR_LIMIT} llamadas este año ({CALLS_LOG.name})")
            return 0
        if a.init:
            return cmd_init(a.init, a.dry_run, a.forzar)
        if a.subir:
            dirs = [ROOT / d for d in a.subir]
            missing = [d for d in dirs if not d.is_dir()]
            if missing:
                raise OnshapeError(f"no existe: {', '.join(map(str, missing))}")
            return cmd_upload([f for d in dirs for f in sorted(d.glob("*.step"))], a.dry_run, a.forzar)
        if a.actualizar:
            return cmd_upload(find_piece(a.actualizar), a.dry_run, a.forzar)
        f = ROOT / ENSAMBLE.format(a.ensamble)
        if not f.exists():
            raise OnshapeError(f"no existe {rel(f.parent)}/{f.name}: se genera con python cad_final/build.py --todo")
        return cmd_upload([f], a.dry_run, a.forzar, flatten=True)
    except OnshapeError as e:
        print(f"ERROR: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
