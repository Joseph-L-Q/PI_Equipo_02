"""Uploads one STEP to the LanternGuard Onshape document as NEW tabs (never deletes or replaces a tab).

    python cad_final/onshape_push.py <ruta.step> [--nombre X] [--plano]
    python cad_final/onshape_push.py --carpeta salida/prototipos/P1_minimo/step --documento LG_P1_minimo
                                     [--ensamble ensamble.step] [--dry-run]

--carpeta creates (once) a document of its own and puts one tab per STEP/STL of the folder in it, plus ENSAMBLE; the
document ids and links are kept in cad_final/onshape_docs.json.

The name is --nombre or the file name; if a tab with that name already exists, the next free _vN is used
(X, X_v2, X_v3...). The STEP is uploaded as a new blob element with translation (Part Studio, plus an Assembly when
the STEP has more than one part, unless --plano flattens it), the translation is polled every 5 s and the links of the
new tabs are printed. Keys and the call log are the ones of onshape_sync.py (cad_final/.env, onshape_calls.log).
Endpoints (official OpenAPI spec, also valid under v6):
    GET  /documents/d/{did}/w/{wid}/elements          tabs of the workspace (names)
    POST /blobelements/d/{did}/w/{wid}                uploadFileCreateElement, multipart, translate=true
    GET  /translations/{tid}                          requestState ACTIVE / DONE / FAILED, resultElementIds
    POST /documents                                   createDocument {name, isPublic} -> id, defaultWorkspace.id
"""
import argparse
import re
import sys
from pathlib import Path

import onshape_sync as OS

API_V6 = "https://cad.onshape.com/api/v6"
DOCS = OS.HERE / "onshape_docs.json"


def tabs(client, did, wid):
    return client.call("GET", f"/documents/d/{did}/w/{wid}/elements")


def free_name(name, existing):
    """name if no tab is called like that, else name_vN with the next N."""
    taken = {e["name"].rsplit(".", 1)[0] if e["name"].lower().endswith((".step", ".stp")) else e["name"] for e in existing}
    if name not in taken:
        return name
    pat = re.compile(re.escape(name) + r"_v(\d+)$")
    n = max([1] + [int(m.group(1)) for t in taken if (m := pat.match(t))])
    return f"{name}_v{n + 1}"


def ensure_document(client, name):
    """{did, wid, url} of the document called name, created on the first call and remembered in onshape_docs.json
    (never replaced: a second run reuses it). The public API has no create-folder endpoint (only folder ACL and
    share), so documents land in the root of the account and are moved into a folder by hand."""
    reg = OS.read_json(DOCS, {})
    if name not in reg:
        d = client.call("POST", "/documents", {"name": name, "isPublic": False})
        did, wid = d["id"], d["defaultWorkspace"]["id"]
        reg[name] = {"did": did, "wid": wid, "url": f"https://cad.onshape.com/documents/{did}/w/{wid}"}
        OS.write_json(DOCS, reg)
    return reg[name]


def push_folder(folder, doc_name, assembly=None, dry=False):
    """One tab per STEP (or STL, when a piece has no STEP) of folder, named after the file, plus an ENSAMBLE tab from
    the assembly STEP. Files whose tab already exists are skipped, so the call can be repeated after a failure."""
    folder = Path(folder)
    files = {f.stem: f for f in sorted(folder.glob("*.stl"))}
    files.update({f.stem: f for f in sorted(folder.glob("*.step"))})
    if dry:
        return None, [(stem, "pendiente", str(f)) for stem, f in files.items()]
    OS.API = API_V6
    client = OS.Client()
    doc = ensure_document(client, doc_name)
    have = {e["name"].rsplit(".", 1)[0] for e in tabs(client, doc["did"], doc["wid"])}
    done = []
    for stem, f in files.items():
        if stem not in have:
            done += push(f, stem, did=doc["did"], wid=doc["wid"], client=client)[1]
    if assembly and "ENSAMBLE" not in have:
        done += push(assembly, "ENSAMBLE", did=doc["did"], wid=doc["wid"], client=client)[1]
    return doc, done


def push(path, nombre=None, flatten=False, did=None, wid=None, client=None):
    path = Path(path)
    if not path.exists():
        raise OS.OnshapeError(f"no existe {path}")
    if did is None:
        cfg = OS.read_json(OS.CONFIG, {})
        if not cfg:
            raise OS.OnshapeError("falta onshape_config.json (python cad_final/onshape_sync.py --init)")
        did, wid = cfg["documentId"], cfg["workspaceId"]
    OS.API = API_V6
    client = client or OS.Client()
    name = free_name(nombre or path.stem, tabs(client, did, wid))
    fields = {"encodedFilename": f"{name}{path.suffix}", "translate": "true", "storeInDocument": "true",
              "importWithinDocument": "true", "yAxisIsUp": "false", "flattenAssemblies": str(flatten).lower()}
    body, ctype = OS.multipart(fields, path)
    r = client.call("POST", f"/blobelements/d/{did}/w/{wid}", body, ctype)
    t = client.wait_translation(r["translationId"])
    if t.get("requestState") != "DONE":
        raise OS.OnshapeError(f"traduccion {t.get('requestState')}: {t.get('failureReason')}")
    new = {e["id"]: e for e in tabs(client, did, wid)}
    out = [(r["id"], new.get(r["id"], {}).get("name", name), "STEP")]
    for eid in t.get("resultElementIds") or []:
        e = new.get(eid, {})
        out.append((eid, e.get("name", "?"), e.get("elementType", "?")))
    base = f"https://cad.onshape.com/documents/{did}/w/{wid}/e/"
    return name, [(n, typ, base + eid) for eid, n, typ in out]


def main():
    ap = argparse.ArgumentParser(description="Sube STEP a Onshape como pestanas nuevas")
    ap.add_argument("step", nargs="?")
    ap.add_argument("--nombre")
    ap.add_argument("--plano", action="store_true", help="aplana el ensamble en un solo Part Studio")
    ap.add_argument("--carpeta", help="sube cada STEP/STL de la carpeta a un documento propio")
    ap.add_argument("--documento", help="nombre del documento para --carpeta")
    ap.add_argument("--ensamble", help="STEP del ensamble para la pestana ENSAMBLE (--carpeta)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    try:
        n0 = OS.year_total()
        if a.carpeta:
            doc, links = push_folder(a.carpeta, a.documento or Path(a.carpeta).name, a.ensamble, a.dry_run)
            name = doc["url"] if doc else "(dry-run)"
        else:
            name, links = push(a.step, a.nombre, a.plano)
    except OS.OnshapeError as e:
        print(f"ERROR: {e}")
        return 1
    print(f"Subido como '{name}' ({OS.year_total() - n0} llamadas; ano: {OS.year_total()} de {OS.YEAR_LIMIT})")
    for n, typ, url in links:
        print(f"  {typ:14s} {n}: {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
