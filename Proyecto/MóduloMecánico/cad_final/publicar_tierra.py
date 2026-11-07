"""05/11: T1_caja with the SMA 1 mm lower, its drawing, the ground station assembly and the LR2_aro drawing again.

    python publicar_tierra.py --t1 --ensamble     one upload per piece, no retry loops
    python publicar_tierra.py --lr2 "note text"   new PLANO_A4_LR2_aro: ring diameters, no zero dimensions

Replaced tabs and drawings are renamed OLD, never deleted. A drawing batch with a failed annotation creates nothing, so it
is sent again once without the failed ones. Counter in salida/nuevas/_llamadas_tierra.txt, hard stop at 80.
"""
import argparse
import json
import os
import sys
import time
import urllib.request

os.environ.setdefault("LG_VERSION", "P2_robusto")

import publicar_nuevas as N  # noqa: E402

OS, OP, P = N.OS, N.OP, N.P
DID, WID, FECHA = N.DID, N.WID, N.FECHA
COUNT = N.OUT / "_llamadas_tierra.txt"
MAX = 80
ENS = N.MOD / "salida" / "tierra" / "step" / "00_ENSAMBLE_tierra.step"
_orig = N._orig


def used():
    return int(COUNT.read_text()) if COUNT.exists() else 0


def call(self, method, path, body=None, content_type="application/json"):
    if used() >= MAX:
        raise SystemExit(f"tope de {MAX} llamadas")
    COUNT.write_text(str(used() + 1))
    return _orig(self, method, path, body, content_type)


def clean(q):
    """Dimensions from an edge to itself read 0: the ring has no straight edge to measure."""
    keep = []
    for a in q["annotations"]:
        d = a.get("lineToLineDimension")
        if d and d.get("edge1", {}).get("uniqueId") == d.get("edge2", {}).get("uniqueId"):
            continue
        keep.append(a)
    q["annotations"][:] = keep


def wm(c, did, wid, eid, reqs, desc):
    for q in reqs:
        if "annotations" in q:
            clean(q)
    res = N.wait_modify(c, did, wid, eid, reqs, desc)
    q = reqs[0]
    results = res.get("results", [])
    bad = [i for i, r in enumerate(results) if r.get("status") != "OK"]
    if bad and "annotations" in q:
        print(desc, "fallaron", [results[i].get("errorDescription") for i in bad], "reenvio sin ellas", flush=True)
        q["annotations"][:] = [a for i, a in enumerate(q["annotations"]) if i not in bad]
        res = N.wait_modify(c, did, wid, eid, reqs, desc + " (2)")
    return res


def pdf(c, did, wid, eid, dst):
    t = c.call("POST", f"/drawings/d/{did}/w/{wid}/e/{eid}/translations", {"formatName": "PDF", "storeInDocument": False, "showOverriddenDimensions": True})
    time.sleep(35)
    t = c.call("GET", f"/translations/{t['id']}")
    if t.get("requestState") != "DONE":
        raise SystemExit(f"PDF {t.get('requestState')}")
    req = urllib.request.Request(OS.API + f"/documents/d/{did}/externaldata/{t['resultExternalDataIds'][0]}", headers={"Authorization": c.auth})
    with urllib.request.urlopen(req, timeout=120) as r:
        dst.write_bytes(r.read())


def drawing(c, code, stp, qty, notes, studio, extra=()):
    base = P.title_notes
    P.title_notes = lambda cd: base(cd) + [{"type": "Onshape::Note", "note": {"position": {"type": "Onshape::Reference::Point", "coordinate": [N.NOTE_XY[0], N.NOTE_XY[1], 0]},
                                                                              "contents": N.wrapped(notes), "textHeight": 2.6}}] + list(extra)
    R = P.reg()
    R.setdefault("antes_tierra", {})[code] = R["piezas"].get(code)
    R["piezas"][code] = {"partstudio": studio, "pestana": code}
    P.save(R)
    try:
        return P.piece_a4(code, stp, qty, c, {"elements": {}, "name_pid": None}, chamfer=())
    finally:
        P.title_notes = base


def setup():
    OS.Client.call = call
    OS.API = OP.API_V6
    OS.POLL_S, OS.POLL_MAX = 30, 6
    P.wait_modify = wm
    P.export_pdf = pdf
    P.use_format("equipo")
    P.LIMIT = P.LIMIT_A4 = 2500
    return P.client()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--t1", action="store_true")
    ap.add_argument("--ensamble", action="store_true")
    ap.add_argument("--lr2")
    a = ap.parse_args()
    c = setup()
    S = OS.read_json(N.STATE, {})
    tabs = {e["name"]: e for e in OP.tabs(c, DID, WID)}
    meta = c.call("GET", f"/metadata/d/{DID}/w/{WID}/e/{tabs['T2_tapa']['id']}")
    pid = next(p["propertyId"] for p in meta["properties"] if p["name"] == "Name")

    def rename(eid, name):
        c.call("POST", f"/metadata/d/{DID}/w/{WID}/e/{eid}", {"properties": [{"propertyId": pid, "value": name}]})

    def put(name, path, flatten=False):
        if name in tabs:
            raise SystemExit(f"ya existe la pestana {name}")
        blob, res = N.upload(c, name, path, flatten)
        now = {e["id"]: e for e in OP.tabs(c, DID, WID)}
        sid = next(e for e in res if now[e]["elementType"] == "PARTSTUDIO")
        if now[sid]["name"] != name:
            rename(sid, name)
        parts = c.call("GET", f"/parts/d/{DID}/w/{WID}/e/{sid}")
        solids = OP.step_parts(path)[1]
        rec = dict(blob=blob, estudio=sid, partes=len(parts), solidos=solids, verificado=len(parts) == solids, part0=parts[0]["partId"],
                   url=f"https://cad.onshape.com/documents/{DID}/w/{WID}/e/{sid}", nombres_ref=sum(p.get("name", "").startswith(("REF_", "EXP_")) for p in parts))
        print(name, "partes", len(parts), "solidos", solids, flush=True)
        return rec

    if a.t1 and not S.get("T1_caja", {}).get("sma_z_7"):
        for old in ("T1_caja", "T1_caja.step", "PLANO_A4_T1_caja"):
            rename(tabs[old]["id"], f"OLD {FECHA} {old.replace('.step', '')} (SMA 1 mm mas alta)" + (".step" if old.endswith(".step") else ""))
            tabs.pop(old)
        rec = put("T1_caja", N.STEPS["T1_caja"])
        if not rec["verificado"]:
            raise SystemExit("T1_caja: partes y solidos no coinciden")
        rec["sma_z_7"] = True
        S["T1_caja"] = rec
        OS.write_json(N.STATE, S)
        a4 = drawing(c, "T1_caja", N.STEPS["T1_caja"], 1, N.NOTAS["T1_caja"], rec["estudio"])
        rec["plano"] = dict(id=a4["drawing"], url=a4["url"], cotas=a4["cotas"], escala=a4["escala"], pdf=a4["pdf"])
        OS.write_json(N.STATE, S)
        print("T1 plano", a4["url"], a4["cotas"].get("creadas"), a4["cotas"].get("fallidas"), used(), flush=True)
    if a.ensamble and not S.get("00_ENSAMBLE_tierra"):
        rec = put("00_ENSAMBLE_tierra", ENS, flatten=True)
        S["00_ENSAMBLE_tierra"] = rec
        OS.write_json(N.STATE, S)
        if not rec["verificado"]:
            print("AVISO: partes y solidos no coinciden; no se reintenta", flush=True)
    if a.lr2 is not None:
        rename(tabs["PLANO_A4_LR2_aro"]["id"], f"OLD {FECHA} PLANO_A4_LR2_aro (cotas 0)")
        rec = S["LR2_aro"]
        # views are placed by piece_a4; the two diameters need the view id, so they go in a second batch
        a4 = drawing(c, "LR2_aro", N.STEPS["LR2_aro"], 4, N.NOTAS["LR2_aro"] + [N.LR2_EXTRA, a.lr2], rec["estudio"])
        vid = a4["vistas"]["top"]
        dims = []
        for uid, rm, xyz0, xyz1, tp in (("f4242", 0.10825, (0.10825, 0, 0), (-0.10825, 0, 0), (100.0, 50.0, 0.0)), ("f4241", 0.09175, (0, 0.09175, 0), (0, -0.09175, 0), (58.0, 82.0, 0.0))):
            dims.append({"type": "Onshape::Dimension::Diametric", "diametricDimension": {
                "chordPoint": P.ref_pt(vid, uid, list(xyz0), "ModeNear"), "farChordPoint": P.ref_pt(vid, uid, list(xyz1), "ModeNear"),
                "formatting": P.fmt(), "textOverride": "", "textPosition": P.pt(tp)}})
        r = wm(c, DID, WID, a4["drawing"], [{"messageName": "onshapeCreateAnnotations", "formatVersion": "2021-01-01", "annotations": dims}], "diametros LR2")
        print("LR2 diametros", json.dumps(r, ensure_ascii=False)[:300], flush=True)
        pdf(c, DID, WID, a4["drawing"], P.OUT_A4 / "PLANO_A4_LR2_aro.pdf")
        rec["plano"] = dict(id=a4["drawing"], url=a4["url"], cotas=a4["cotas"], escala=a4["escala"], pdf=a4["pdf"])
        OS.write_json(N.STATE, S)
        print("LR2 plano", a4["url"], used(), flush=True)
    print("llamadas", used())


if __name__ == "__main__":
    sys.exit(main())
