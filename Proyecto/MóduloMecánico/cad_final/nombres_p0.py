"""Names the solids of the P0 assembly STEPs (simple V1 and modular), which were exported as a bare compound and reach
Onshape as "Open CASCADE STEP translator ..." parts. Geometry is not touched: the same solids, in the same place, are
written again as a cq.Assembly whose children carry the names.

    python cad_final/nombres_p0.py            # writes <ensamble>_v2_nombres.step next to each P0 assembly
    python cad_final/onshape_push.py --ensamble-v2 LG_P0_original --ensamble <..._v2_nombres.step> [--pestana X]

Printed pieces are recognised by volume against the per-piece STEPs of the same folder (step/*.step, 0.2 %), with
_+X/_-X (or _+Y/_-Y) from the centroid when a piece appears twice. What is left is classified by its bounding box with
the rules below, and what is not printed gets REF_ (correction 4 of Yoichi, 30/10). The lastre plates keep "lastre_"
without REF_, as Yoichi named the new lastre bodies (lastre_izq / lastre_der).
"""
import json
import sys
from pathlib import Path

import cadquery as cq

MOD = Path(__file__).resolve().parent.parent
P0 = MOD / "salida" / "prototipos" / "P0_original"
TOL = 0.002


def rules(bb, c):
    """Name for a solid that matches no printed piece, from its bounding box (mm) and centroid."""
    dims = sorted((bb.xlen, bb.ylen, bb.zlen))
    if dims == sorted((100.0, 25.0, 5.0)):
        return f"lastre_{'+Y' if c.y > 0 else '-Y'}_pletina"
    if abs(bb.xlen - 208) < 1 and abs(bb.ylen - 208) < 1 and bb.zlen < 10:
        return "REF_aro_superior"
    if abs(bb.xlen - 200) < 1 and abs(bb.zlen - 200) < 1:
        return "REF_linterna_malla"
    if abs(bb.xlen - 196) < 1 and bb.zlen < 2:
        return "REF_linterna_piso"
    if abs(bb.xlen - 212) < 1 and abs(bb.ylen - 212) < 1 and bb.zlen < 7:
        return "LR1_separador"
    if dims[0] < 5 and dims[1] < 5 and abs(c.x) < 1 and abs(c.y) < 1:
        return "REF_cabo"
    if bb.zlen > 150 and c.z > 150 and dims[0] > 40:          # V1: cords from the separator up to the apex
        return "REF_cuerda_apice"
    if dims[:2] == [4.0, 4.0] or (bb.zlen > 150 and dims[0] < 70 and bb.xlen < 100):
        return "REF_cuerda"
    if abs(bb.xlen - 300) < 1 and abs(bb.ylen - 20) < 1:
        return "REF_long_line"
    if abs(bb.xlen - 210) < 1 and abs(bb.ylen - 140) < 1:
        return "REF_boya"
    if bb.xlen > 400 and dims[0] < 10:
        return "REF_varilla_M8"
    if abs(bb.xlen - 2) < 0.5 and abs(bb.ylen - 24) < 0.5:
        return f"REF_arandela_M8_{'+X' if c.x > 0 else '-X'}"
    if abs(bb.xlen - 6.5) < 0.5 and abs(bb.ylen - 15) < 0.5:
        return f"REF_tuerca_M8_{'+X' if c.x > 0 else '-X'}"
    if dims[0] < 11 and dims[1] < 22:
        return "REF_umbilical"
    return None


def side(c):
    return (f"_{'+X' if c.x > 0 else '-X'}" if abs(c.x) >= abs(c.y) else f"_{'+Y' if c.y > 0 else '-Y'}")


def name_assembly(asm_path, piece_dir):
    pieces = {f.stem: cq.importers.importStep(str(f)).val().Volume() for f in sorted(Path(piece_dir).glob("*.step"))}
    solids = cq.importers.importStep(str(asm_path)).solids().vals()
    hits = [[k for k, v in pieces.items() if abs(v - s.Volume()) <= TOL * v] for s in solids]
    count = {}
    for h in hits:
        if len(h) == 1:
            count[h[0]] = count.get(h[0], 0) + 1
    names, unknown = [], []
    for i, (s, h) in enumerate(zip(solids, hits)):
        c, bb = s.Center(), s.BoundingBox()
        if len(h) == 1:
            n = h[0] + (side(c) if count[h[0]] > 1 else "")
        else:
            n = rules(bb, c)
            if n is None:
                unknown.append(i)
                n = f"REF_sin_clasificar_{i}"
        names.append(n)
    # numbered families (cuerdas 1..4, pisos, pletinas, umbilical segments) in file order
    for base in ("REF_cuerda", "REF_cuerda_apice", "REF_linterna_piso", "REF_umbilical", "lastre_+Y_pletina", "lastre_-Y_pletina"):
        idx = [i for i, n in enumerate(names) if n == base]
        for k, i in enumerate(idx):
            names[i] = f"{base}_{k + 1}"
    dup = {n for n in names if names.count(n) > 1}
    if dup or unknown:
        raise SystemExit(f"{asm_path.name}: nombres repetidos {sorted(dup)}, sin clasificar {unknown}")
    asm = cq.Assembly(name=asm_path.stem)
    for s, n in zip(solids, names):
        asm.add(s, name=n)
    out = asm_path.with_name(asm_path.stem + "_v2_nombres.step")
    asm.save(str(out), exportType="STEP")
    table = [{"n": i, "nombre": n, "volumen_mm3": round(s.Volume(), 1)} for i, (s, n) in enumerate(zip(solids, names))]
    out.with_suffix(".json").write_text(json.dumps({"origen": asm_path.name, "solidos": len(solids), "partes": table},
                                                   ensure_ascii=False, indent=1), encoding="utf-8")
    return out, names


def main():
    for sub, asm in (("simple_V1", "ensamble_simple_V1.step"), ("modular", "ensamble_modular_D200.step")):
        out, names = name_assembly(P0 / sub / asm, P0 / sub / "step")
        print(f"{out.relative_to(MOD)}: {len(names)} solidos")
        print("   " + ", ".join(names))
    return 0


if __name__ == "__main__":
    sys.exit(main())
