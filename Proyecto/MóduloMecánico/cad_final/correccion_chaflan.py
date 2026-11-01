"""Chamfer correction of 01/11/2026 (lab instructor): 45 deg feet at the base of the supports of B2_cubierta, B3_caja,
B5_cuna and M1s_caja_cuerpo (params chaflan.base_soportes, chaflan.base_soportes_max; chaflan.py).

Run AFTER boya_pet.py and build.py --prototipo P2_robusto (they write the v2 STL/STEP and slicer.json):
    python correccion_chaflan.py --antes <folder with boya_pet/ and P2_robusto/ slicer.json of v1> [--sin-3mf]
1. rebuilds the 4 pieces in memory with chaflan.base_soportes = 0 and with the current value: logs every foot (joint, size)
   -> salida/correccion_chaflan/chaflanes.json (read by planos_onshape.py --v2 for the callout);
2. clearances: interference volume of each piece with the components, bottles, gland nuts, ballast and the neighbour pieces,
   v1 against v2 (the chamfer must add none);
3. one 3MF per piece (placas.py: OrcaSlicer, G-code inside) -> salida/correccion_chaflan/3mf/;
4. table v1 -> v2 (grams, hours, cost at S/ 60 per kg, overhang, supports) -> salida/correccion_chaflan/resultado.json.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import cadquery as cq

import params as P
import chaflan as CH

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
OUT = MOD / "salida" / "correccion_chaflan"
BOYA = MOD / "salida" / "boya_pet"
P2 = MOD / "salida" / "prototipos" / "P2_robusto"
PRICE = 60.0     # S/ per kg asked for this correction (params costo.filamento_soles_kg is still 90, by the bitacora)
PIECES = {"B2_cubierta": (BOYA, 1, 40), "B3_caja": (BOYA, 1, 40), "B5_cuna": (BOYA, 2, 40), "M1s_caja_cuerpo": (P2, 1, 100)}


def vol(a, b):
    a = a if isinstance(a, cq.Workplane) else cq.Workplane().add(a)
    b = b if isinstance(b, cq.Workplane) else cq.Workplane().add(b)
    try:
        return sum(s.Volume() for s in a.intersect(b).solids().vals())
    except Exception:
        return float("nan")


def buoy(c):
    import boya_pet as B
    P.CHAMFER_BASE = c
    CH.LOG.clear()
    d = B.dims(P.FLOT_BOTTLE, P.FLOT_COUNT)
    S = {"B1_casco": B.b1_cruz(d), "B2_cubierta": B.b2_cubierta(d), "B3_caja": B.b3_caja(d), "B4_tapa": B.b4_tapa(d)}
    b5 = B.b5_cuna(d)
    S["B5_cuna_+x"], S["B5_cuna_-x"] = B.to_world(b5, 1, d), B.to_world(b5, -1, d)
    dm = B.dummies(d)
    pairs = {"B2_cubierta": ["B1_casco", "B3_caja"], "B3_caja": ["B2_cubierta", "B4_tapa"],
             "B5_cuna_+x": ["B1_casco"], "B5_cuna_-x": ["B1_casco"]}
    inter = {}
    for k, others in pairs.items():
        for o in others:
            inter[f"{k} / {o}"] = vol(S[k], S[o])
        for n, s in dm.items():
            inter[f"{k} / {n}"] = vol(S[k], s)
    return {k: v for k, v in inter.items()}, {k: list(v) for k, v in CH.LOG.items()}


def node(c):
    import layout
    import simple as SM
    import caja_central as CC
    P.CHAMFER_BASE = c
    CH.LOG.clear()
    lay = layout.build(P.SIMPLE_ESP32_BASE, floors=P.SIMPLE_FLOORS)
    SM.set_pad(lay)
    depth = SM.CFG.get("bolsillo", P.SIMPLE_POCKET_DEPTH)
    m1 = SM.box_body_low(lay, depth)
    lr = json.loads((P2 / "resultados.json").read_text(encoding="utf-8"))["lastre"]
    ko = {f"contratuerca PG7 {i + 1}": n for i, n in enumerate(SM.gland_nuts(lay))}
    ko.update({f"módulo {n}": s for n, s in CC.module_dummies(lay)})
    ko.update({f"bandeja {k}": t for k, t in SM.trays_low(lay).items()})
    ko.update({f"{k} (máximo {lr['rango_total_g'][1] / 2:.0f} g)": s
               for k, s in SM.ballast_solids(depth, lr["rango_total_g"][1] / 2, lr["aparente"]).items()})
    ko["M3t tapa del bolsillo"] = SM.pocket_cover(depth)
    inter = {f"M1s_caja_cuerpo / {n}": vol(m1, s) for n, s in ko.items()}
    return inter, {k: list(v) for k, v in CH.LOG.items()}


def plates():
    import slicer as SL
    OUT.mkdir(parents=True, exist_ok=True)
    stl_dir = OUT / "stl"
    stl_dir.mkdir(exist_ok=True)
    plan = {"salida": str((OUT / "3mf").relative_to(MOD)).replace("\\", "/"),
            "capturas": str((OUT / "3mf").relative_to(MOD)).replace("\\", "/"), "placas": []}
    for code, (src, q, inf) in PIECES.items():
        js = json.loads((src / ("resultados.json" if src == P2 else "slicer.json")).read_text(encoding="utf-8"))
        orient = js["piezas"][code]["orient"] if src == P2 else js[code]["orientacion"]
        sup = js["piezas"][code]["soportes"] if src == P2 else js[code]["soportes"]
        dst = stl_dir / f"{code}_v2.stl"
        SL.oriented_stl(src / "stl" / f"{code}.stl", orient, dst)
        plan["placas"].append({"nombre": f"{code}_v2", "relleno": inf, "soportes": bool(sup), "paredes": 3, "fijo": True,
                               "piezas": [[str(dst.relative_to(MOD)).replace("\\", "/"), q]]})
    pj = OUT / "plan_chaflan.json"
    pj.write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    subprocess.run([sys.executable, "placas.py", str(pj)], cwd=HERE, check=False)


def slicer_rows(before):
    rows = {}
    for code, (src, q, _) in PIECES.items():
        old = json.loads((before / src.name / "slicer.json").read_text(encoding="utf-8"))[code]
        new = json.loads((src / "slicer.json").read_text(encoding="utf-8"))[code]
        res = json.loads((src / "resultados.json").read_text(encoding="utf-8"))
        ov = (json.loads((before / src.name / "resultados.json").read_text(encoding="utf-8"))["piezas"][code]["voladizo_mm2"],
              res["piezas"][code]["voladizo_mm2"]) if src == P2 else (old["voladizo_mm2"], new["voladizo_mm2"])
        rows[code] = {"cantidad": q, "g": [old["g"], new["g"]], "h": [round(old["h"], 2), round(new["h"], 2)],
                      "soles": [round(old["g"] * PRICE / 1000, 2), round(new["g"] * PRICE / 1000, 2)],
                      "soportes": [old["soportes"], new["soportes"]], "voladizo_mm2": [round(ov[0], 1), round(ov[1], 1)]}
    return rows


LINES = {   # note on the drawing: short lines (Onshape wraps a note at ~20 x its text height)
    "B2_cubierta": ["Chaflanes a 45°:", "pilares Ø10: 2", "columnas Ø12: 2 (1 lat.)", "mástil Ø14: 2 (en la barra)"],
    "B3_caja": ["Chaflanes a 45°:", "piso-paredes int.: 2", "standoffs Ø9: 2", "postes bandeja Ø8: 2", "orejas-pared ext.: 2"],
    "B5_cuna": ["Chaflanes a 45°:", "costillas-patín: 1", "(botella a 1,5 del patín)", "pared-lengüetas: 2", "postes-lengüetas: 2"],
    "M1s_caja_cuerpo": ["Chaflanes a 45°:", "piso-paredes int.: 2", "(no junto a las PG7)", "bosses bandeja Ø8: 2", "techo bolsillos: 1"]}


def callout(code, log):
    """Main size for the drawing callout and the note that lists every joint (Spanish, comma decimals)."""
    groups = {}
    for j, c in log:
        k = j.split("#")[0].strip()
        groups.setdefault(k, []).append(c)
    sizes = [c for v in groups.values() for c in v if c > 0]
    main = max(set(sizes), key=sizes.count) if sizes else 0.0
    n = lambda v: f"{v:g}".replace(".", ",")
    parts = [k if max(v) == 0 else f"{k}: {n(min(v))}" + (f" a {n(max(v))}" if max(v) != min(v) else "") for k, v in groups.items()]
    return {"c": main, "texto": "Chaflanes 45° en la base de los soportes (mm). " + "; ".join(parts), "grupos": groups,
            "lineas": LINES[code]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--antes", required=True, help="folder with boya_pet/ and P2_robusto/ (slicer.json, resultados.json) of v1")
    ap.add_argument("--sin-3mf", action="store_true")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    c0 = P.CHAMFER_BASE
    i1b, _ = buoy(0.0)
    i2b, logb = buoy(c0)
    i1n, _ = node(0.0)
    i2n, logn = node(c0)
    P.CHAMFER_BASE = c0
    logs = {**logb, **logn}
    ch = {code: callout(code, logs.get(code, [])) for code in PIECES}
    (OUT / "chaflanes.json").write_text(json.dumps(ch, indent=1, ensure_ascii=False), encoding="utf-8")
    inter = {k: {"v1_mm3": round(i1.get(k, 0.0), 2), "v2_mm3": round(v, 2)} for i1, i2 in ((i1b, i2b), (i1n, i2n)) for k, v in i2.items()}
    worse = {k: v for k, v in inter.items() if v["v2_mm3"] > v["v1_mm3"] + 0.01}
    if not a.sin_3mf:
        plates()
    pl = OUT / "3mf" / "placas.json"
    res = {"parametro": {"chaflan.base_soportes": c0, "chaflan.base_soportes_max": P.CHAMFER_BASE_MAX},
           "chaflanes": ch, "registro": logs, "interferencias": inter, "interferencias_nuevas": worse,
           "slicer": slicer_rows(Path(a.antes)), "placas_3mf": json.loads(pl.read_text(encoding="utf-8")) if pl.exists() else None}
    (OUT / "resultado.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"interferencias_nuevas": worse, "slicer": res["slicer"]}, indent=1, ensure_ascii=False))
    return 1 if worse else 0


if __name__ == "__main__":
    sys.exit(main())
