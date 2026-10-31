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
    POST /documents/{did}                             updateDocumentAttributes {parentId, description}
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


FOLDER = "bf32e5647856cd2677198b89"     # carpeta "LanternGuard" que Yoichi creo a mano (30/10)


def organize(client, name, description, folder=FOLDER):
    """Moves the document into the LanternGuard folder and sets its one-line description (updateDocumentAttributes,
    POST /documents/{did} with parentId / description). The public API has no call to reorder tabs."""
    doc = OS.read_json(DOCS, {})[name]
    client.call("POST", f"/documents/{doc['did']}", {"parentId": folder, "description": description})
    return doc


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
    if assembly and "ENSAMBLE" not in have:      # first, so it is the first tab (tabs cannot be reordered by API)
        done += push(assembly, "ENSAMBLE", did=doc["did"], wid=doc["wid"], client=client)[1]
    for stem, f in files.items():
        if stem not in have:
            done += push(f, stem, did=doc["did"], wid=doc["wid"], client=client)[1]
    return doc, done


# Correction 4 (Yoichi, 30/10): what is not printed carries REF_; printed parts keep their code.
REF_NAMES = [(r"^LR_red$", "REF_linterna_malla"), (r"^LR_aro$", "REF_aro_superior"), (r"^LR_aro_superior$", "REF_aro_superior"),
             (r"^LR_cabo(_central)?$", "REF_cabo"), (r"^(LR_|U1_?)umbilical.*$", "REF_umbilical"),
             (r"^LR_boya$", "REF_boya"), (r"^M11_M11_", "M11_"), (r"^LR_", "REF_"),
             (r"^ref_botella(\d+)$", r"REF_botella_\1"), (r"^ref_batt$", "REF_portabaterias_18650"),
             (r"^ref_pcb$", "REF_pcb_heltec"), (r"^ref_ws$", "REF_waveshare"), (r"^ref_panel$", "REF_panel_solar"),
             (r"^ref_", "REF_")]


def step_parts(path):
    """Leaf product names of a STEP and its number of solids (MANIFOLD_SOLID_BREP + BREP_WITH_VOIDS entities)."""
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    solids = len(re.findall(r"=\s*(MANIFOLD_SOLID_BREP|BREP_WITH_VOIDS)\(", text))
    names = re.findall(r"=\s*PRODUCT\('([^']*)'", text)
    return names, solids


def ref_name(name):
    """REF_ name for a reference body; cuerdas are numbered 1..4 by the caller (ref_rename_step)."""
    for pat, new in REF_NAMES:
        if re.search(pat, name):
            return re.sub(pat, new, name)
    return name


def ref_rename_step(src, dst):
    """Copy of src with the PRODUCT names changed by REF_NAMES and the cuerdas renamed REF_cuerda_1..N in file
    order. Geometry is untouched (only the name strings of PRODUCT entities change), so P0 keeps its shapes."""
    text = Path(src).read_text(encoding="utf-8", errors="replace")
    cuerdas = []

    def sub(m):
        old = m.group(2)
        if old.startswith("REF_"):
            new = old
        elif re.search(r"cuerda", old, re.I):
            if old not in cuerdas:
                cuerdas.append(old)
            new = f"REF_cuerda_{cuerdas.index(old) + 1}"
        else:
            new = ref_name(old)
        return f"{m.group(1)}'{new}','{new}'"
    out = re.sub(r"(=\s*PRODUCT\()'([^']*)','[^']*'", sub, text)
    Path(dst).write_text(out, encoding="utf-8")
    return step_parts(dst)


def verify(doc_name, tab_prefix="ENSAMBLE", local=None, client=None):
    """Parts that Onshape reports in each Part Studio whose tab name starts with tab_prefix
    (GET /parts/d/{did}/w/{wid}?elementId=...) against the solids of the local STEP. Returns a list of dicts."""
    OS.API = API_V6
    client = client or OS.Client()
    doc = OS.read_json(DOCS, {})[doc_name]
    out = []
    local_names, local_solids = step_parts(local) if local else ([], None)
    for e in tabs(client, doc["did"], doc["wid"]):
        if e.get("elementType") != "PARTSTUDIO" or not e["name"].startswith(tab_prefix):
            continue
        parts = client.call("GET", f"/parts/d/{doc['did']}/w/{doc['wid']}?elementId={e['id']}")
        names = [p.get("name", "?") for p in parts]
        out.append({"documento": doc_name, "pestana": e["name"], "partes_onshape": len(parts), "solidos_step": local_solids,
                    "coincide": local_solids is None or len(parts) == local_solids,
                    "sin_nombre": sum(1 for n in names if n.lower().startswith(("open cascade", "part "))),
                    "nombres": names, "url": f"https://cad.onshape.com/documents/{doc['did']}/w/{doc['wid']}/e/{e['id']}"})
    return out


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
    ap.add_argument("--verificar", metavar="DOCUMENTO", help="compara las partes de las pestanas ENSAMBLE* con --ensamble")
    ap.add_argument("--ensamble-v2", metavar="DOCUMENTO",
                    help="sube --ensamble como pestana nueva ENSAMBLE_v2 (nombres REF_ en el STEP) y la verifica")
    ap.add_argument("--pestana", default="ENSAMBLE_v2", help="nombre de la pestana para --ensamble-v2")
    a = ap.parse_args()
    try:
        n0 = OS.year_total()
        if a.verificar:
            for r in verify(a.verificar, local=a.ensamble):
                print(f"{r['pestana']}: Onshape {r['partes_onshape']} partes, STEP {r['solidos_step']} solidos, "
                      f"{'coincide' if r['coincide'] else 'NO COINCIDE'}, sin nombre {r['sin_nombre']}")
            return 0
        if a.ensamble_v2:
            src = Path(a.ensamble)      # a *_v2_nombres.step (nombres_p0.py) is uploaded as it is
            dst = src if src.stem.endswith("_v2_nombres") else src.with_name(src.stem + "_v2_nombres.step")
            names, solids = step_parts(dst) if dst == src else ref_rename_step(src, dst)
            doc = OS.read_json(DOCS, {})[a.ensamble_v2]
            OS.API = API_V6
            client = OS.Client()
            name, links = push(dst, a.pestana, flatten=True, did=doc["did"], wid=doc["wid"], client=client)
            print(f"STEP local: {solids} solidos, {len(names)} productos")
            for r in verify(a.ensamble_v2, name, dst, client):
                print(f"  {r['pestana']}: Onshape {r['partes_onshape']} partes, "
                      f"{'coincide' if r['coincide'] else 'NO COINCIDE'}, sin nombre {r['sin_nombre']}")
        elif a.carpeta:
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
