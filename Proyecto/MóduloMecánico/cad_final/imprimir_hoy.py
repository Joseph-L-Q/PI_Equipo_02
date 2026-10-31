"""Print list of the recommended node (P2_robusto) and the PET buoy: oriented STL with clean names in
salida/imprimir_hoy/ and the plate plan for placas.py (3MF per plate + slicer previews in salida/capturas_slicer/).

    python imprimir_hoy.py            (from cad_final/; then: python placas.py ../salida/imprimir_hoy/plan_placas.json)

Groups: 1 probetas (calibration, seal, hook on the real rod, bottle bay with a real bottle), 2 pieces that do not
depend on pending measurements, 3 pieces that wait for aro.seccion, 4 the PET buoy. Two new test pieces are cut from
the STEP with CadQuery: PB10 = 50 mm of the rail around the C hook (x = R_RING +- 25, same orientation as M3s) and
PB9 = the end of the hull with the neck seat and the first body rib of one bottle (80 mm, one side).
STL are turned and laid on the bed with slicer.oriented_stl, the orientation of each piece from its resultados.json.
"""
import json
import shutil
from pathlib import Path

import cadquery as cq

import slicer as SL

MOD = SL.MOD
OUT = MOD / "salida" / "imprimir_hoy"
PROTO = MOD / "salida" / "prototipos" / "P2_robusto"
BOYA = MOD / "salida" / "boya_pet"
OLD = MOD / "salida" / "imprimir_hoy_V2"          # the V2 list of the afternoon, kept for reference

# (file name, source STL or cut, orientation, quantity, infill %, supports, walls, group)
PROBES_OLD = [("01_PB7_peine_holguras", "01_PB7_peine_holguras_x1.stl", 1, 40, False, None),
              ("02_PB7_pines", "02_PB7_pines_x1.stl", 1, 40, False, None),
              ("03_PB8_inserto_M4", "03_PB8_inserto_M4_x3.stl", 3, 100, False, 5),
              ("04_PB6_junta_base", "04_PB6_junta_base_x1.stl", 1, 100, False, None),
              ("05_PB6_junta_tapa", "05_PB6_junta_tapa_x1.stl", 1, 100, False, None)]
NODE = [("08_M6_bisel", "M6_capsula_bisel", 2), ("09_M11_bandeja", "M11_bandeja", 1),
        ("10_M11_bandeja_sup", "M11_bandeja_sup", 1), ("11_M3t_tapa_bolsillo", "M3t_tapa_bolsillo", 2),
        ("12_M4_capsula_cuerpo", "M4_capsula_cuerpo", 2), ("13_M2_caja_tapa", "M2_caja_tapa", 1),
        ("14_M1s_caja_cuerpo", "M1s_caja_cuerpo", 1), ("15_M5s_capsula_tapa_pie", "M5s_capsula_tapa_pie", 2)]
WAIT = [("16_M3s_riel_gancho", "M3s_riel_gancho", 2), ("17_LR1_separador", "LR1_separador", 1)]
BUOY = [("18_B1_casco", "B1_casco", 1), ("19_B2_cubierta", "B2_cubierta", 1), ("20_B3_caja", "B3_caja", 1),
        ("21_B4_tapa", "B4_tapa", 1)]


def cut(step, box, dst):
    """Intersection of the STEP solid with an axis box ((x0, x1), (y0, y1), (z0, z1)), saved as STL."""
    s = cq.importers.importStep(str(step))
    (x0, x1), (y0, y1), (z0, z1) = box
    b = cq.Workplane().box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
    cq.exporters.export(s.intersect(b), str(dst), tolerance=0.02, angularTolerance=0.1)


def infill(r):
    return SL.infill_pct(r) if r is not None else None


def main():
    import params as P
    OUT.mkdir(parents=True, exist_ok=True)
    if not OLD.exists() and (OUT / "01_PB7_peine_holguras_x1.stl").exists():
        shutil.copytree(OUT, OLD)               # the caller moves it with git mv; here only when run standalone
    res = json.loads((PROTO / "resultados.json").read_text(encoding="utf-8"))["piezas"]
    sl = json.loads((PROTO / "slicer.json").read_text(encoding="utf-8"))
    bres = json.loads((BOYA / "slicer.json").read_text(encoding="utf-8"))
    rows = []

    def add(name, src, orient, qty, inf, sup, walls, group, g=None, h=None):
        dst = OUT / f"{name}_x{qty}.stl"
        if orient is None:
            shutil.copy2(src, dst)
        else:
            SL.oriented_stl(src, orient, dst)
        rows.append(dict(archivo=dst.name, cant=qty, orient=orient or "ya orientada", relleno=inf, soportes=sup,
                         paredes=walls or 3, grupo=group, g=g, h=h))

    for name, f, q, inf, sup, walls in PROBES_OLD:
        add(name, OLD / f, None, q, inf, sup, walls, 1)
    r = P.SIMPLE_RING_D / 2
    tmp = OUT / "_corte.stl"
    cut(PROTO / "step" / "M3s_riel_gancho.step", ((r - 25, r + 25), (-60, 60), (-200, 200)), tmp)
    add("06_PB10_gancho_tramo", tmp, res["M3s_riel_gancho"]["orient"], 1, 100, True, None, 1)
    x0 = -P.PET_HULL_MAX / 2
    cut(BOYA / "step" / "B1_casco.step", ((x0 - 1, x0 + 80), (-200, 0), (-1, 300)), tmp)
    add("07_PB9_bahia_botella", tmp, "sin girar", 1, 40, False, None, 1)
    tmp.unlink()
    for name, stem, q in NODE + WAIT:
        info = res[stem]
        src = (PROTO / "lr1" if stem == "LR1_separador" else PROTO / "stl") / f"{stem}.stl"
        s = sl.get(stem, {})
        add(name, src, info["orient"], q, infill(info.get("relleno")), info["soportes"], None,
            3 if (name, stem, q) in WAIT else 2, s.get("g"), s.get("h"))
    for name, stem, q in BUOY:
        b = bres[stem]
        add(name, BOYA / "stl" / f"{stem}.stl", b.get("orientacion", "sin girar"), q, b["relleno_pct"], b["soportes"],
            None, 4, b["g"], b["h"])
    (OUT / "lista.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    plan = {"salida": "salida/imprimir_hoy/3mf", "capturas": "salida/capturas_slicer", "placas": plates(rows)}
    (OUT / "plan_placas.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(rows)} STL en {OUT}, {len(plan['placas'])} placas en plan_placas.json")


PLATES = [  # (plate name, files by number prefix): one infill, one support setting, one wall count per plate
    ("P01_probetas_calibracion", ["01", "02"]), ("P02_probeta_inserto_M4", ["03"]), ("P03_probeta_junta", ["04", "05"]),
    ("P04_probeta_gancho", ["06"]), ("P05_probeta_bahia_botella", ["07"]),
    ("P06_bisel_y_bandejas", ["08", "09", "10"]), ("P07_tapas_bolsillo", ["11"]), ("P08_capsulas", ["12"]),
    ("P09_tapa_caja", ["13"]), ("P10_caja", ["14"]), ("P11_tapas_capsula_con_pie", ["15"]),
    ("P12_rieles_con_gancho", ["16"]), ("P13_separador_LR1", ["17"]),
    ("P14_boya_casco", ["18"]), ("P15_boya_cubierta", ["19"]), ("P16_boya_caja_y_tapa", ["20", "21"])]


def plates(rows):
    out = []
    for name, pre in PLATES:
        rs = [r for r in rows if r["archivo"][:2] in pre]
        keys = {(r["relleno"], r["soportes"], r["paredes"]) for r in rs}
        assert len(keys) == 1, f"{name}: mezcla rellenos/soportes {keys}"
        inf, sup, walls = keys.pop()
        out.append(dict(nombre=name, relleno=inf, soportes=sup, paredes=walls, grupo=rs[0]["grupo"],
                        piezas=[[f"salida/imprimir_hoy/{r['archivo']}", r["cant"]] for r in rs]))
    return out


if __name__ == "__main__":
    main()
