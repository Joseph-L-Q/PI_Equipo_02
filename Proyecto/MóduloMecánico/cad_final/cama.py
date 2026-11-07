"""Usable-bed check (impresora.cama_util, 230 x 230): no printed piece may exceed it in X or Y in its print orientation.

    python cama.py            (from cad_final/) exit 1 if any piece is over; writes salida/cama/cama.json

Checks, with the orientation each pipeline chose: the pieces of every prototype (salida/prototipos/<P>/resultados.json),
the PET buoy (salida/boya_pet/slicer.json) and the print list (salida/imprimir_hoy/*.stl, already oriented).
Only what exists on disk is checked; a missing folder is reported, not failed. build.py runs it at the end of every plan.
"""
import json
import sys
from pathlib import Path

import params as P
from checks import mesh_checks

HERE = Path(__file__).resolve().parent
SAL = HERE.parent / "salida"
ORIENT = {"sin girar": None, "X180": ("X", 180), "X+90": ("X", 90), "Y+90": ("Y", 90), "ya orientada": None}


def rows():
    out = []
    for proto in sorted((SAL / "prototipos").glob("P*/resultados.json")):
        for stem, info in json.loads(proto.read_text(encoding="utf-8")).get("piezas", {}).items():
            stl = proto.parent / "stl" / f"{stem}.stl"
            if stl.exists():
                out.append((f"{proto.parent.name}/{stem}", stl, ORIENT.get(info.get("orient"))))
    sl = SAL / "boya_pet" / "slicer.json"
    if sl.exists():
        for stem, info in json.loads(sl.read_text(encoding="utf-8")).items():
            stl = SAL / "boya_pet" / "stl" / f"{stem}.stl"
            if stl.exists():
                out.append((f"boya_pet/{stem}", stl, ORIENT.get(info.get("orientacion"))))
    for stl in sorted((SAL / "imprimir_hoy").glob("*.stl")):
        if not stl.name.startswith("_"):
            out.append((f"imprimir_hoy/{stl.stem}", stl, None))
    return out


def main():
    bx, by = P.BED_USE
    res, bad = [], []
    for name, stl, o in rows():
        mc = mesh_checks(str(stl), (bx, by, P.PRINT_BED[2]), o)
        x, y, z = mc["bbox"]
        ok = x <= bx and y <= by
        res.append(dict(pieza=name, bbox=[round(x, 1), round(y, 1), round(z, 1)], cabe=ok))
        if not ok:
            bad.append(f"{name}: {x:.1f} x {y:.1f} > {bx:g} x {by:g}")
    (SAL / "cama").mkdir(parents=True, exist_ok=True)
    (SAL / "cama" / "cama.json").write_text(json.dumps(dict(cama_util=[bx, by], piezas=res, fuera=bad), indent=1,
                                                       ensure_ascii=False), encoding="utf-8")
    print(f"cama util {bx:g} x {by:g}: {len(res)} piezas revisadas, {len(bad)} fuera")
    for b in bad:
        print("  FUERA", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
