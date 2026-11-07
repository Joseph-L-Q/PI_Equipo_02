"""LR2_aro (lantern ring, printed flat) and its fit coupon PB_aro. Run with LG_VERSION=P2_robusto (hook of the printed node).

    python aro.py            geometry, fit against the real M3s hook, FEM, salida/aro/aro.json
    python aro.py --sin-fem  geometry and fit only

FEM assumptions in params.py (aro.fem). Solver: fem_tet10.py, checked against beam theory. Cords are modelled as vertical
supports on a short patch at the top of the section (the ring may twist there); the 150 N act over 20 mm of the top of
the ring, midway between two cords. Hook case: flange top fixed, 150 N down on the crown of the seat.
"""
import json
import math
import os
import sys
from pathlib import Path

os.environ.setdefault("LG_VERSION", "P2_robusto")

import cadquery as cq  # noqa: E402
import numpy as np  # noqa: E402

import fem_tet10 as F  # noqa: E402
import params as P  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "aro"
STEP, STL = OUT / "step", OUT / "stl"
R = P.AROS["D"] / 2
FLAT = P.AROS["plano_base"]
FS_OBJ = P.FS_TARGET_Z


def section_area(d, flat=FLAT):
    r = d / 2
    h = flat
    return math.pi * r ** 2 - (r ** 2 * math.acos((r - h) / r) - (r - h) * math.sqrt(2 * r * h - h ** 2))


def ring(d=None, angle=360.0, flat=FLAT):
    """Ring in the plane XY, section centre at z = 0, flat base at z = -(d/2 - flat). angle < 360: arc centred on +X."""
    d = d or P.RING_SECTION
    r = d / 2
    prof = cq.Workplane("XZ").center(R, 0).circle(r)
    if angle >= 360:
        s = prof.revolve(360, (-R, 0, 0), (-R, 1, 0))
    else:
        s = prof.revolve(angle, (-R, 0, 0), (-R, 1, 0)).rotate((0, 0, 0), (0, 0, 1), -angle / 2)
    w = 2 * R + 2 * d
    return s.cut(cq.Workplane("XY").box(w, w, d, centered=(True, True, False)).translate((0, 0, -d - (r - flat))))


def seat_coupon():
    """The seat of the real hook of M3s, cut from simple.hook(): the same bore, jaws and strap slot."""
    import simple as SM
    clr, wall, _ = P.SIMPLE_HOOK_C
    ro = P.RING_SECTION / 2 + clr + wall
    h = SM.hook(holes=False)
    return h.intersect(cq.Workplane("XY").box(2 * ro + 8, 80, ro + 6 + ro + 2, centered=(True, True, False)).translate((0, 0, -ro - 2)))


def fit(seat):
    """Arc of ring in the seat. The bore touches the rod only along the seat length of gancho.c (the web above starts over
    the rod), where the curve of the ring deviates by the sagitta; simple.seat_shift() puts the bore half of it inward, so
    the ring on its nominal circle has that half to each side and clears with holgura - sagitta / 2."""
    seat_l = P.SIMPLE_HOOK_C[2]
    sag = seat_l ** 2 / (8 * R)

    def vol(dx):
        arc = ring(angle=math.degrees(50.0 / R)).translate((-R + dx, 0, 0))
        try:
            return arc.intersect(seat).val().Volume()
        except ValueError:
            return 0.0
    return dict(asiento_efectivo_mm=seat_l, flecha_aro_mm=round(sag, 3), holgura_radial_mm=round(P.SIMPLE_HOOK_C[0], 3),
                margen_radial_mm=round(P.SIMPLE_HOOK_C[0] - sag / 2, 3), interferencia_mm3=round(vol(0.0), 3))


def printed_fraction(d=None):
    """Printed mass / solid mass: wall of aro.impreso (perimeters) plus its infill in the core."""
    d = d or P.RING_SECTION
    t = P.AROS["perimetros"] * P.AROS["ancho_linea"]
    solid, core = ring(d).val().Volume(), ring(d - 2 * t).val().Volume()
    return (solid - core + P.AROS["relleno"] * core) / solid


def export(shape, stem):
    STEP.mkdir(parents=True, exist_ok=True)
    STL.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(shape, str(STEP / f"{stem}.step"))
    cq.exporters.export(shape, str(STL / f"{stem}.stl"), tolerance=0.05, angularTolerance=0.1)
    v = shape.val()
    bb = v.BoundingBox()
    return dict(volumen_cm3=round(v.Volume() / 1000, 2), gramos=round(v.Volume() / 1000 * P.PETG_DENSITY, 1),
                caja_mm=[round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)], valido=bool(v.isValid()), solidos=len(shape.solids().vals()))


def fem_ring(d, size, inplane=False):
    tmp = OUT / "_fem"
    tmp.mkdir(parents=True, exist_ok=True)
    p = tmp / f"aro_{d:g}.step"
    cq.exporters.export(ring(d), str(p))
    xyz, tets = F.mesh(p, size)
    ang = np.degrees(np.arctan2(xyz[:, 1], xyz[:, 0])) % 360
    rad = np.hypot(xyz[:, 0], xyz[:, 1])
    top = xyz[:, 2] > 0
    dist = lambda a: np.abs((ang - a + 180) % 360 - 180) * np.pi / 180 * R
    fixed = {}
    for k, a in enumerate((45, 135, 225, 315)):
        sel = np.flatnonzero((dist(a) < 4) & top)
        for n in sel:
            fixed[int(n)] = (2,) if k else (0, 1, 2)     # one cord also holds the ring in its plane
        if k == 2:                                        # the opposite cord stops the rotation about Z
            for n in sel:
                fixed[int(n)] = (0, 1, 2)
    weight = P.ARO_FEM["masa_piso_kg"] * 9.81
    load = P.ARO_FEM["manipulacion_N"]
    w_each = weight / len(xyz)
    loads = {int(n): (0.0, 0.0, -w_each) for n in range(len(xyz))}
    patch = np.flatnonzero((dist(0) < 10) & top)
    for n in patch:
        n = int(n)
        fx = load / len(patch) * (-1 if inplane else 0)
        fz = 0.0 if inplane else -load / len(patch)
        loads[n] = (loads[n][0] + fx, 0.0, loads[n][2] + fz)
    r = F.solve(xyz, tets, fixed, loads, P.PETG_E, P.PETG_NU)
    # away from the supports and the load patch the stress is the plain bending of the ring: the peak there has no artefact
    c = xyz[tets[:, :4]].mean(axis=1)
    ac = np.degrees(np.arctan2(c[:, 1], c[:, 0])) % 360
    dc = lambda a: np.abs((ac - a + 180) % 360 - 180) * np.pi / 180 * R
    clean = (dc(0) > 15) & np.all([dc(a) > 10 for a in (45, 135, 225, 315)], axis=0)
    rep = F.report(r, P.PETG_YIELD, P.PETG_YIELD_Z)
    rep["s_flexion_limpia"] = float(r["vm"][clean].max())
    rep.update(nodos=len(xyz), elementos=len(tets), malla_mm=size, reaccion_z_N=round(float(r["reac"][list(fixed), 2].sum()), 2),
               carga_N=round(weight + (0 if inplane else load), 2), d=d)
    return rep


def fem_hook(d, size=2.5):
    """Hook alone with ring section d, seat = d + clearance rule. Compares the current hook with the proposed one."""
    import simple as SM
    keep = P.RING_SECTION, P.SIMPLE_HOOK_C
    P.RING_SECTION, P.SIMPLE_HOOK_C = d, (P.AROS["juego"] / 2, keep[1][1], keep[1][2])
    try:
        h = SM.hook(holes=False)
        ri = d / 2 + P.SIMPLE_HOOK_C[0]
        tmp = OUT / "_fem"
        tmp.mkdir(parents=True, exist_ok=True)
        p = tmp / f"gancho_{d:g}.step"
        cq.exporters.export(h, str(p))
    finally:
        P.RING_SECTION, P.SIMPLE_HOOK_C = keep
    xyz, tets = F.mesh(p, size)
    zt = xyz[:, 2].max()
    fixed = {int(n): (0, 1, 2) for n in np.flatnonzero(xyz[:, 2] > zt - 1e-3)}
    bore = np.hypot(xyz[:, 0] - SM.seat_shift(), xyz[:, 2])
    crown = np.flatnonzero((np.abs(bore - ri) < 0.05) & (xyz[:, 2] > 0.5 * ri))
    F_n = P.ARO_FEM["manipulacion_N"]
    r = F.solve(xyz, tets, fixed, {int(n): (0.0, 0.0, -F_n / len(crown)) for n in crown}, P.PETG_E, P.PETG_NU)
    rep = F.report(r, P.PETG_YIELD, P.PETG_YIELD_Z)
    rep.update(d=d, asiento=2 * ri, pared=keep[1][1], nodos=len(xyz), elementos=len(tets), nodos_carga=len(crown), nodos_fijos=len(fixed))
    return rep


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    d = P.RING_SECTION
    res = {"seccion_mm": d, "asiento_mm": d + 2 * P.SIMPLE_HOOK_C[0], "area_mm2": round(section_area(d), 2),
           "ancho_plano_base_mm": round(2 * math.sqrt(d * FLAT - FLAT ** 2), 2)}
    res["LR2_aro"] = export(ring(d), "LR2_aro")
    res["PB_aro_tramo"] = export(ring(d, angle=math.degrees(50.0 / R)), "PB_aro_tramo")
    frac = printed_fraction(d)
    res["impresion"] = dict(perimetros=P.AROS["perimetros"], ancho_linea_mm=P.AROS["ancho_linea"], relleno=P.AROS["relleno"], fraccion_de_macizo=round(frac, 4))
    for k in ("LR2_aro", "PB_aro_tramo"):
        res[k]["gramos_macizo"] = res[k]["gramos"]
        res[k]["gramos"] = round(res[k]["gramos"] * frac, 1)
    seat = seat_coupon()
    res["PB_aro_asiento"] = export(seat, "PB_aro_asiento")
    res["calce"] = fit(seat)
    res["gramos_juego_4"] = round(res["LR2_aro"]["gramos"] * P.AROS["cantidad"], 1)
    print(json.dumps(res, ensure_ascii=False, indent=1))
    if "--sin-fem" not in sys.argv:
        fem = {f"aro_{d:g}_malla_2.5": fem_ring(d, 2.5), f"aro_{d:g}_en_plano": fem_ring(d, 2.5, inplane=True), f"gancho_{d:g}": fem_hook(d)}
        res["fem"] = fem
        for k, v in fem.items():
            print(k, {x: round(v[x], 2) if isinstance(v[x], float) else v[x] for x in ("s995", "s_flexion_limpia", "fs_capas", "fs", "umax", "szz995", "elementos", "reaccion_z_N", "carga_N", "nodos_carga", "nodos_fijos") if x in v}, flush=True)
    elif (OUT / "aro.json").exists():
        res["fem"] = json.loads((OUT / "aro.json").read_text(encoding="utf-8")).get("fem", {})
    (OUT / "aro.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
