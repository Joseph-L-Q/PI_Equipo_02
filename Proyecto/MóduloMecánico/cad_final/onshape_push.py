"""Uploads one STEP to the LanternGuard Onshape document as NEW tabs (never deletes or replaces a tab).

    python cad_final/onshape_push.py <ruta.step> [--nombre X] [--plano]

The name is --nombre or the file name; if a tab with that name already exists, the next free _vN is used
(X, X_v2, X_v3...). The STEP is uploaded as a new blob element with translation (Part Studio, plus an Assembly when
the STEP has more than one part, unless --plano flattens it), the translation is polled every 5 s and the links of the
new tabs are printed. Keys and the call log are the ones of onshape_sync.py (cad_final/.env, onshape_calls.log).
Endpoints (official OpenAPI spec, also valid under v6):
    GET  /documents/d/{did}/w/{wid}/elements          tabs of the workspace (names)
    POST /blobelements/d/{did}/w/{wid}                uploadFileCreateElement, multipart, translate=true
    GET  /translations/{tid}                          requestState ACTIVE / DONE / FAILED, resultElementIds
"""
import argparse
import re
import sys
from pathlib import Path

import onshape_sync as OS

API_V6 = "https://cad.onshape.com/api/v6"


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


def push(path, nombre=None, flatten=False):
    path = Path(path)
    if not path.exists():
        raise OS.OnshapeError(f"no existe {path}")
    cfg = OS.read_json(OS.CONFIG, {})
    if not cfg:
        raise OS.OnshapeError("falta onshape_config.json (python cad_final/onshape_sync.py --init)")
    did, wid = cfg["documentId"], cfg["workspaceId"]
    OS.API = API_V6
    client = OS.Client()
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
    ap = argparse.ArgumentParser(description="Sube un STEP a Onshape como pestanas nuevas")
    ap.add_argument("step")
    ap.add_argument("--nombre")
    ap.add_argument("--plano", action="store_true", help="aplana el ensamble en un solo Part Studio")
    a = ap.parse_args()
    try:
        n0 = OS.year_total()
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
