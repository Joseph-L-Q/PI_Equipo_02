"""Fase C, central box: exports M1, M2 and M11 of the chosen layout to salida/preliminar/ (STL + STEP) and runs
the per-piece checks of cad/build.py plus the minimum wall thickness. The rail, hook and capsule pieces have
their own scripts (riel.py, gancho.py, capsula.py).

    python fase_c_caja.py       (from cad_final/)   -> cad_final/reporte_caja.md
"""
from pathlib import Path

import caja_central as C
import fase_a as FA
import layout as LY
import params as P
from checks import brep_check, export_part, mesh_checks, min_thickness

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "preliminar"
STL, STEP = OUT / "stl", OUT / "step"
for d in (STL, STEP):
    d.mkdir(parents=True, exist_ok=True)

# print orientation: (rotation before measuring, what the slicer sees, supports)
ORIENT = {"M1_caja_cuerpo": (None, "boca arriba, fondo en la cama", "sin soportes; la falda de la brida es a 45°"),
          "M2_caja_tapa": (None, "cara interior (ranura) en la cama, asa arriba", "sin soportes; techo de la ventana del asa a 45°"),
          "M11_bandeja": (None, "plana", "sin soportes")}


def chosen_layout():
    cands = LY.candidates()
    if len(cands) == 1:
        return next(iter(cands.values()))
    ok = {f: l for f, l in cands.items() if not LY.conflicts(l) and not LY.inside_cavity(l)}
    return min(ok.values(), key=lambda l: FA.analyse_box(l)["v_air"])


def main():
    lay = chosen_layout()
    an = FA.analyse_box(lay)
    pieces = {"M1_caja_cuerpo": an["m1"], "M2_caja_tapa": an["m2"]}
    pieces.update({k: v for k, v in an["trays"].items()})
    rows = []
    for stem, shape in pieces.items():
        chk = brep_check(shape)
        export_part(shape, stem, STL, STEP)
        o = ORIENT.get(stem, ORIENT["M11_bandeja"] if stem.startswith("M11") else (None, "", ""))
        mc = mesh_checks(STL / f"{stem}.stl", P.PRINT_BED, o[0])
        p1, tmin = min_thickness(STL / f"{stem}.stl")
        sealed = stem.split("_")[0] in P.SEALED_PIECES
        infill = P.INFILL_SEALED if sealed else P.INFILL_CASES[0]
        rows.append(dict(stem=stem, chk=chk, mc=mc, p1=p1, tmin=tmin, g=FA.mass_g(shape, infill), infill=infill,
                         orient=o[1], sup=o[2]))
        print(stem, chk["ok"], mc["watertight"], mc["bodies"], [round(x, 1) for x in mc["bbox"]], round(p1, 2))
    r = ["# Fase C, caja central (generado por `fase_c_caja.py`)", "",
         f"Layout de {lay.floors} piso{'s' if lay.floors > 1 else ''}. STL y STEP en `salida/preliminar/`: "
         "NO LISTO PARA IMPRIMIR hasta medir la electrónica y los prensaestopas (Fase H).", "",
         "| Pieza | BRep/BOP | Sólidos | STL estanco | Cuerpos | bbox mm | Cabe | Voladizo mm² | Espesor mín p1 / mín mm | "
         "Relleno | Masa g | Orientación | Soportes |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for x in rows:
        c, m = x["chk"], x["mc"]
        flag = "" if x["p1"] >= P.MIN_WALL else " **(bajo 1.2)**"
        r.append(f"| {x['stem']} | {'ok' if c['brep'] and c['bop'] else 'FALLA'} | {c['solids']} | "
                 f"{'sí' if m['watertight'] else 'NO'} | {m['bodies']} | {' × '.join(f'{v:.1f}' for v in m['bbox'])} | "
                 f"{'sí' if m['fits_bed'] else 'NO'} | {m['overhang_mm2']:.0f} | {x['p1']:.2f} / {x['tmin']:.2f}{flag} | "
                 f"{x['infill'] * 100:.0f} % | {x['g']:.0f} | {x['orient']} | {x['sup']} |")
    r += ["", "El espesor mínimo se mide con rayos hacia adentro desde 1500 caras al azar; el percentil 1 es el criterio "
          f"(≥ {P.MIN_WALL:g}). El mínimo absoluto suele caer en aristas y redondeos.", ""]
    (HERE / "reporte_caja.md").write_text("\n".join(r), encoding="utf-8")
    print("written reporte_caja.md")


if __name__ == "__main__":
    main()
