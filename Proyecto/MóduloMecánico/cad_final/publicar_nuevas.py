"""05/11: publishes LR2_aro, PB_aro, T1_caja, T2_tapa and the M3s with the 16.8 seat. Run with LG_VERSION=P2_robusto.

    python publicar_nuevas.py --local      PB_aro.step, 00_ENSAMBLE.step (32 + 4 rings) and local A4 sheets, no API
    python publicar_nuevas.py --onshape    tabs, 00_ENSAMBLE replaced, 4 PLANO_A4 drawings (salida/nuevas/onshape.json)

Rings in the assembly: centred on the node axis, flat down, one at the level of the hook seat and the floors of
linterna.pisos below it (the spacing of the reference net in simple.py). Hard stop at 160 API calls across runs: 40 spent
on the discarded 8.5 ring plus 120 for this pass. Resumable: what is done is kept in onshape.json. The assembly without
rings stays as "OLD 2026-11-05 00_ENSAMBLE (sin aros)". The tabs of the 8.5 ring are deleted; the M3s with the 8.8 seat is renamed, never deleted.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path

os.environ.setdefault("LG_VERSION", "P2_robusto")

import cadquery as cq  # noqa: E402

import aro  # noqa: E402
import onshape_push as OP  # noqa: E402
import onshape_sync as OS  # noqa: E402
import params as PR  # noqa: E402
import planos_0511 as Q  # noqa: E402
import planos_onshape as P  # noqa: E402

MOD = P.MOD
OUT = MOD / "salida" / "nuevas"
PLANOS = OUT / "planos_A4"
ENS = P.OUT / "00_ENSAMBLE.step"
STATE = OUT / "onshape.json"
COUNT = OUT / "_llamadas.txt"
MAX_CALLS = 160
DOC = "LG_IMPRIMIR_P2"
DID, WID = "b2a875b87e1322c259f4cd3b", "3bda440db9eda84724dc5cff"
PARTIAL = "c235e7c0838e3bedbedf6780"      # drawing of the 8.5 ring, left unfinished
FECHA = "2026-11-05"
STEPS = {"LR2_aro": aro.STEP / "LR2_aro.step", "PB_aro": aro.STEP / "PB_aro.step",
         "T1_caja": MOD / "salida" / "tierra" / "step" / "T1_caja.step", "T2_tapa": MOD / "salida" / "tierra" / "step" / "T2_tapa.step",
         "M3s_riel_gancho": MOD / "salida" / "prototipos" / "P2_robusto" / "step" / "M3s_riel_gancho.step"}
QTY = {"LR2_aro": 4, "PB_aro": 1, "T1_caja": 1, "T2_tapa": 1, "M3s_riel_gancho": 2}
SERVICIO = "Diseñado para 2 kg por piso + 150 N de manipulación; FS entre capas ≥ 3."
IMPRESION = "Imprimir con 13 perímetros de 0,4 y 15 % de gyroid; capas superiores e inferiores de 5,2 mm."


def es(x):
    return f"{x:g}".replace(".", ",")


AJUSTE = (f"Sección Ø{es(PR.RING_SECTION)} con base plana de {es(PR.AROS['plano_base'])}. Asiento del gancho M3s Ø{es(PR.RING_SECTION + 2 * PR.SIMPLE_HOOK_C[0])}: "
          f"juego {es(PR.AROS['juego'])} en diámetro.")
NOTAS = {"LR2_aro": [AJUSTE, SERVICIO, IMPRESION], "PB_aro": [AJUSTE, "Probar el calce antes de imprimir los 4 aros: tramo de 50 mm y asiento real de M3s."],
         "M3s_riel_gancho": [f"Asiento Ø{es(PR.RING_SECTION + 2 * PR.SIMPLE_HOOK_C[0])} para el aro Ø{es(PR.RING_SECTION)}: juego {es(PR.AROS['juego'])} en diámetro.", SERVICIO],
         "T1_caja": ["Cordón NBR Ø2 en ranura 2,6 x 1,5. Insertos M3 y M2,5. Montar con el USB-C hacia abajo.", "Medidas del Heltec y la batería estimadas: confirmar antes de imprimir."],
         "T2_tapa": ["4 M3 inox A4. Ventana OLED: acrílico de 31 x 20 x 2 pegado con sellador en el rebaje.", "Medidas del Heltec estimadas: confirmar la ventana antes de imprimir."]}


def pb_aro():
    tramo = aro.ring(angle=__import__("math").degrees(50.0 / aro.R))
    asiento = cq.importers.importStep(str(aro.STEP / "PB_aro_asiento.step"))
    bb = asiento.val().BoundingBox()
    tb = tramo.val().BoundingBox()
    moved = tramo.val().moved(cq.Location(cq.Vector(bb.xmax + 10 - tb.xmin, 0, bb.zmin - tb.zmin)))
    comp = cq.Compound.makeCompound([asiento.val(), moved])
    cq.exporters.export(cq.Workplane().add(comp), str(STEPS["PB_aro"]))
    return len(cq.importers.importStep(str(STEPS["PB_aro"])).solids().vals())


def ring_levels():
    """z of the 4 ring centres: the hook seat of the node and the floors below it."""
    import simple as SM
    z_rod = SM.Z_RAIL - PR.HOOK_DROP if hasattr(SM, "Z_RAIL") else None
    step = PR.LANTERN_NET_H / (PR.LANTERN_FLOORS + 1)
    return z_rod, [z_rod - k * step for k in range(PR.AROS["cantidad"])]


def ensamble():
    items = Q.build_assembly(None)
    z_rod, levels = ring_levels()
    # the seat of the placed hooks must be where the code says: lowest solid of M3s gives the check
    hooks = [(n, s) for n, s in items if n.startswith("M3s")]
    ring0 = aro.ring().val().moved(cq.Location(cq.Vector(0, 0, levels[0])))
    choque = {n: round(cq.Workplane().add(ring0).intersect(cq.Workplane().add(s)).val().Volume(), 3) if True else 0 for n, s in hooks}
    near = {n: [round(s.BoundingBox().zmin, 1), round(s.BoundingBox().zmax, 1)] for n, s in hooks}
    asm = cq.Assembly(name="LG_ensamble")
    for n, s in items:
        asm.add(s, name=n)
    for k, z in enumerate(levels, 1):
        asm.add(aro.ring().val().moved(cq.Location(cq.Vector(0, 0, z))), name=f"LR2_aro_{k}")
    asm.export(str(ENS))
    Q_names, solids = OP.step_parts(ENS)
    base_vol = sum(s.Volume() for _, s in items)
    ref = sum(s.Volume() for s in cq.importers.importStep(str(MOD / "salida" / "onshape_importar" / FECHA / "00_ENSAMBLE.step")).solids().vals())
    return dict(solidos_step=solids, piezas_base=len(items), volumen_base_cm3=round(base_vol / 1000, 1), volumen_importado_0511_cm3=round(ref / 1000, 1),
                z_rod=z_rod, niveles=levels, choque_aro_gancho_mm3=choque, z_ganchos=near)


def local():
    import planos_piezas as PP
    OUT.mkdir(parents=True, exist_ok=True)
    PLANOS.mkdir(parents=True, exist_ok=True)
    res = dict(PB_aro_solidos=pb_aro(), ensamble=ensamble(), planos={})
    for code, stp in STEPS.items():
        pdf, sc, notes = PP.sheet_equipo(code, stp, QTY[code], PLANOS, FECHA, None, notas=NOTAS[code])
        res["planos"][code] = dict(pdf=str(pdf.relative_to(MOD)), escala=sc, notas=notes)
    (OUT / "local.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))


# ------------------------------------------------------------------- Onshape
_orig = OS.Client.call


def used():
    return int(COUNT.read_text()) if COUNT.exists() else 0


def _call(self, method, path, body=None, content_type="application/json"):
    if used() >= MAX_CALLS:
        raise SystemExit(f"tope de {MAX_CALLS} llamadas")
    COUNT.write_text(str(used() + 1))
    return _orig(self, method, path, body, content_type)


def wait_modify(c, did, wid, eid, reqs, desc):
    r = c.call("POST", f"/drawings/d/{did}/w/{wid}/e/{eid}/modify", {"description": desc, "jsonRequests": reqs})
    time.sleep(25)
    for _ in range(6):
        s = c.call("GET", f"/drawings/modify/status/{r['id']}")
        if s.get("requestState") != "ACTIVE":
            return json.loads(s["output"]) if s.get("output") else s
        time.sleep(20)
    raise OS.OnshapeError(f"modify {desc} sigue ACTIVE")


def upload(c, name, path, flatten=False):
    body, ctype = OS.multipart({"encodedFilename": f"{name}.step", "translate": "true", "storeInDocument": "true", "importWithinDocument": "true",
                                "yAxisIsUp": "false", "flattenAssemblies": str(flatten).lower()}, path)
    r = c.call("POST", f"/blobelements/d/{DID}/w/{WID}", body, ctype)
    t = c.wait_translation(r["translationId"])
    if t.get("requestState") != "DONE":
        raise OS.OnshapeError(f"{name}: traduccion {t.get('requestState')}: {t.get('failureReason')}")
    return r["id"], t["resultElementIds"]


def onshape():
    OS.Client.call = _call
    OS.POLL_S, OS.POLL_MAX = 12, 40
    P.wait_modify = wait_modify
    P.use_format("equipo")
    P.LIMIT = P.LIMIT_A4 = 2500
    OS.API = OP.API_V6
    S = OS.read_json(STATE, {})
    c = P.client()
    if not c.call("GET", "/users/sessioninfo").get("id"):
        raise SystemExit("la clave no autentica")
    els = {e["name"]: e for e in OP.tabs(c, DID, WID)}
    meta = c.call("GET", f"/metadata/d/{DID}/w/{WID}/e/{els['T1_caja']['id']}")
    pid = next(p["propertyId"] for p in meta["properties"] if p["name"] == "Name")

    def rename(eid, name):
        c.call("POST", f"/metadata/d/{DID}/w/{WID}/e/{eid}", {"properties": [{"propertyId": pid, "value": name}]})

    def named(eids, name):
        now = {e["id"]: e for e in OP.tabs(c, DID, WID)}
        for eid in eids:
            if now[eid]["elementType"] == "PARTSTUDIO" and now[eid]["name"] != name:
                rename(eid, name)
        return now

    # 0. out with the 8.5 ring and the 8.8 seat
    if not S.get("reemplazo_165"):
        by_name = {e["name"]: e["id"] for e in els.values()}
        partial = next((e["id"] for e in els.values() if e["elementType"] == "APPLICATION" and e["id"] == PARTIAL), None)
        doomed = [by_name[n] for n in ("LR2_aro", "LR2_aro.step", "PB_aro", "PB_aro.step", "00_ENSAMBLE", "00_ENSAMBLE.step") if n in by_name]
        refs = c.call("GET", f"/appelements/d/{DID}/w/{WID}/resolvereferences")
        users = [eid for eid, r in refs.items() if eid != partial and eid not in doomed and any(x.get("targetElementId") in doomed for x in r.get("resolvedReferences", []))]
        if users:
            raise SystemExit(f"otras pestanas usan lo que iba a borrar: {users}")
        for eid in ([partial] if partial else []) + doomed:
            c.call("DELETE", f"/elements/d/{DID}/w/{WID}/e/{eid}")
        for old, new in (("M3s_riel_gancho", f"OLD {FECHA} M3s_riel_gancho (asiento 8,8)"), ("M3s_riel_gancho.step", f"OLD {FECHA} M3s_riel_gancho (asiento 8,8).step"),
                         ("PLANO_A4_M3s_riel_gancho", f"OLD {FECHA} PLANO_A4_M3s_riel_gancho (asiento 8,8)")):
            if old in by_name:
                rename(by_name[old], new)
        for k in ("LR2_aro", "PB_aro"):
            S.pop(k, None)
        S["00_ENSAMBLE"] = {"retirado": True}
        R = P.reg()
        R["piezas"].pop("LR2_aro", None)
        R["antes_165"] = {"M3s_riel_gancho": R["piezas"].pop("M3s_riel_gancho", None)}
        P.save(R)
        S["reemplazo_165"] = True
        OS.write_json(STATE, S)
    els = {e["name"]: e for e in OP.tabs(c, DID, WID)}

    # 1. pieces
    for code, stp in STEPS.items():
        rec = S.setdefault(code, {})
        if rec.get("verificado"):
            continue
        if code in els:
            raise SystemExit(f"ya existe una pestana {code}: revisar antes de subir")
        blob, res = upload(c, code, stp)
        named(res, code)
        sid = next(iter(res))
        parts = c.call("GET", f"/parts/d/{DID}/w/{WID}/e/{sid}")
        solids = OP.step_parts(stp)[1]
        rec.update(blob=blob, estudio=sid, partes=len(parts), solidos=solids, verificado=len(parts) == solids, part0=parts[0]["partId"],
                   url=f"https://cad.onshape.com/documents/{DID}/w/{WID}/e/{sid}")
        OS.write_json(STATE, S)
        print(code, "partes", len(parts), "solidos", solids, flush=True)
        if not rec["verificado"]:
            raise SystemExit(f"{code}: no coinciden los solidos")
    # 2. assembly
    rec = S.setdefault("00_ENSAMBLE", {})
    if not rec.get("verificado"):
        solids = OP.step_parts(ENS)[1]
        if solids != 36:
            raise SystemExit(f"00_ENSAMBLE.step tiene {solids} solidos, se esperaban 36")
        if not rec.get("retirado"):
            rename(els["00_ENSAMBLE"]["id"], f"OLD {FECHA} 00_ENSAMBLE (sin aros)")
            rename(els["00_ENSAMBLE.step"]["id"], f"OLD {FECHA} 00_ENSAMBLE (sin aros).step")
            rec["retirado"] = True
            OS.write_json(STATE, S)
        blob, res = upload(c, "00_ENSAMBLE", ENS, flatten=True)
        named(res, "00_ENSAMBLE")
        sid = next(iter(res))
        parts = c.call("GET", f"/parts/d/{DID}/w/{WID}/e/{sid}")
        rec.update(blob=blob, estudio=sid, partes=len(parts), solidos=solids, verificado=len(parts) == solids,
                   url=f"https://cad.onshape.com/documents/{DID}/w/{WID}/e/{sid}", aros=sum(p.get("name", "").startswith("LR2_aro") for p in parts))
        OS.write_json(STATE, S)
        print("00_ENSAMBLE partes", len(parts), "solidos", solids, "aros", rec["aros"], flush=True)
    # 3. drawings
    base_notes = P.title_notes
    for code in ("LR2_aro", "T1_caja", "T2_tapa", "M3s_riel_gancho"):
        rec = S[code]
        if rec.get("plano"):
            continue
        y = P.TITLE[3] + 9

        def notes(cd, cur=code, y0=y):
            out = base_notes(cd)
            for i, txt in enumerate(reversed(NOTAS[cur])):
                out.append({"type": "Onshape::Note", "note": {"position": {"type": "Onshape::Reference::Point", "coordinate": [14, 14 + i * 4.2, 0]},
                                                              "contents": txt, "textHeight": 2.6}})
            return out
        P.title_notes = notes
        R = P.reg()
        R.setdefault("piezas", {})[code] = R["piezas"].get(code) or {"partstudio": rec["estudio"], "pestana": code}
        P.save(R)
        ctx = {"elements": {}, "name_pid": pid}
        a4 = P.piece_a4(code, STEPS[code], QTY[code], c, ctx, chamfer=None if code == "M3s_riel_gancho" else ())
        pdf = P.OUT_A4 / f"PLANO_A4_{code}.pdf"
        rec["plano"] = dict(id=a4["drawing"], url=a4["url"], cotas=a4["cotas"], escala=a4["escala"], pdf=str(pdf.relative_to(MOD)))
        OS.write_json(STATE, S)
        print(code, "plano", a4["url"], a4["cotas"].get("creadas"), flush=True)
    P.title_notes = base_notes
    # 4. final check
    tabs = OP.tabs(c, DID, WID)
    refs = c.call("GET", f"/appelements/d/{DID}/w/{WID}/resolvereferences")
    ids = {e["id"] for e in tabs}
    broken = [e["name"] for e in tabs if e["id"] in refs and (refs[e["id"]].get("unresolvedReferenceIds") or any(
        r.get("errorCode") or r.get("targetElementId") not in ids for r in refs[e["id"]]["resolvedReferences"]))]
    names = [e["name"] for e in tabs]
    S["final"] = dict(pestanas=len(tabs), rotas=broken, duplicados=sorted({n for n in names if names.count(n) > 1}), llamadas=used())
    OS.write_json(STATE, S)
    print(S["final"])


# Notes first went to the bottom-left corner, over the title block and past the frame: moved to the free area.
NOTE_XY = (165.0, 82.0)
LR2_EXTRA = "Ø exterior 216,5; Ø medio 200; Ø interior 183,5; alto 16."


def wrapped(texts, width=62):
    lines = []
    for txt in texts:
        cur = ""
        for w in txt.split():
            if cur and len(cur) + len(w) + 1 > width:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
    return chr(10).join(lines)


def fix_drawing(code, pdf=True):
    """Moves the notes, drops failed or zero dimensions, adds the ring diameters. 2 calls per step, on the same counter."""
    OS.Client.call = _call
    OS.API = OP.API_V6
    c = P.client()
    S = OS.read_json(STATE, {})
    eid = S[code]["plano"]["id"]
    base = f"/drawings/d/{DID}/w/{WID}/e/{eid}"

    def export(fmt, dst):
        t = c.call("POST", base + "/translations", {"formatName": fmt, "storeInDocument": False, "showOverriddenDimensions": True})
        time.sleep(30)
        t = c.call("GET", f"/translations/{t['id']}")
        if t.get("requestState") != "DONE":
            raise SystemExit(f"{code} {fmt}: {t.get('requestState')} {t.get('failureReason')}")
        req = urllib.request.Request(OS.API + f"/documents/d/{DID}/externaldata/{t['resultExternalDataIds'][0]}", headers={"Authorization": c.auth})
        with urllib.request.urlopen(req, timeout=120) as r:
            dst.write_bytes(r.read())

    js = OUT / f"_{code}.json"
    if not js.exists():
        export("DRAWING_JSON", js)
    anns = json.loads(js.read_text(encoding="utf-8"))["sheets"][0]["annotations"]
    views = json.loads(js.read_text(encoding="utf-8"))["sheets"][0]["views"]
    drop = [a["note"]["logicalId"] for a in anns if a["type"] == "Onshape::Note" and a["note"].get("contents") in NOTAS[code]]
    for a in anns:
        for v in a.values():
            if isinstance(v, dict) and v.get("displayedValue") in ("0.00", "0,00"):
                drop.append(v["logicalId"])
    texts = NOTAS[code] + ([LR2_EXTRA] if code == "LR2_aro" else [])
    new = [{"type": "Onshape::Note", "note": {"position": {"type": "Onshape::Reference::Point", "coordinate": [NOTE_XY[0], NOTE_XY[1], 0]},
                                              "contents": wrapped(texts), "textHeight": 2.6}}]
    if code == "LR2_aro":
        vid = next(v["viewId"] for v in views if v["orientation"] == "top")
        for uid, rm, y in (("f4242", 0.10825, 66.0), ("f4241", 0.09175, 56.0)):
            new.append({"type": "Onshape::Dimension::Diametric", "diametricDimension": {
                "chordPoint": P.ref_pt(vid, uid, [rm, 0.0, 0.0], "ModeNear"), "farChordPoint": P.ref_pt(vid, uid, [-rm, 0.0, 0.0], "ModeNear"),
                "formatting": P.fmt(), "textOverride": "", "textPosition": P.pt((102.0, y, 0.0))}})
    r = P.wait_modify(c, DID, WID, eid, [{"messageName": "onshapeDeleteAnnotations", "formatVersion": "2021-01-01", "annotationIds": drop},
                                         {"messageName": "onshapeCreateAnnotations", "formatVersion": "2021-01-01", "annotations": new}], f"notas {code}")
    print(code, "borradas", len(drop), json.dumps(r, ensure_ascii=False)[:500], flush=True)
    if pdf:
        export("PDF", MOD / Path(S[code]["plano"]["pdf"].replace(chr(92), "/")))
    print("llamadas", used(), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true")
    ap.add_argument("--onshape", action="store_true")
    ap.add_argument("--corregir", nargs="+", help="planos a corregir")
    ap.add_argument("--sin-pdf", action="store_true")
    a = ap.parse_args()
    if a.local:
        local()
    if a.onshape:
        onshape()
    if a.corregir:
        P.wait_modify = wait_modify
        for code in a.corregir:
            fix_drawing(code, not a.sin_pdf)
    return 0


if __name__ == "__main__":
    sys.exit(main())
