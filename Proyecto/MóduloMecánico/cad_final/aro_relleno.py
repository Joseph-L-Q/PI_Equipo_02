"""LR2_aro as printed: solid wall (perimeters) + gyroid core of reduced stiffness. Same load as aro.fem_ring: 2 kg + 150 N.

    python aro_relleno.py                 prueba de la malla (macizo) and the sweep; writes salida/aro/relleno.json
    python aro_relleno.py 10:15 8:15      only these perimeters:infill %

Core modulus E_core = E * (rho ** EXP) (Gibson-Ashby with C = 1; a gyroid is not measured here), --lineal uses E * rho, the
upper bound. The top and bottom layers are taken as thick as the wall (uniform shell): set them so in the slicer.
FS between layers = 22 MPa / peak von Mises of the WALL away from supports and load patch, as agreed for the ring.
The core stress is reported apart against rho ** 1.5 * 22 MPa. No part of this is a test of the printed infill.
"""
import json
import math
import sys
from pathlib import Path

import cadquery as cq
import gmsh
import numpy as np

import aro
import fem_tet10 as F
import params as P

LINE = 0.4
EXP = 2.0
SWEEP = [(n, i) for n in (4, 5, 6) for i in (15, 20, 25)]
MIN = [(8, 15), (9, 15), (10, 15), (11, 15), (6, 50), (6, 80)]
OUTF = aro.OUT / "relleno.json"
TMP = aro.OUT / "_fem"
FINE, COARSE = 1.6, 3.5


def core_solid(t):
    """Section offset inward by t: circle of radius r - t, cut by the flat base raised by t."""
    d = P.RING_SECTION
    return aro.ring(d - 2 * t, flat=aro.FLAT)


def volumes(t):
    solid = aro.ring().val().Volume()
    core = core_solid(t).val().Volume()
    return solid - core, core


def mesh(t):
    rc = P.RING_SECTION / 2 - t
    p = TMP / f"nucleo_{t:g}.step"
    TMP.mkdir(parents=True, exist_ok=True)
    q = TMP / f"aro_{t:g}.step"
    cq.exporters.export(aro.ring(), str(q))
    cq.exporters.export(core_solid(t), str(p))
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 0)
    try:
        a = gmsh.model.occ.importShapes(str(q))
        b = gmsh.model.occ.importShapes(str(p))
        gmsh.model.occ.fragment(a, b)
        gmsh.model.occ.synchronize()
        f = gmsh.model.mesh.field.add("MathEval")
        rr = f"Sqrt((Sqrt(x*x+y*y)-{aro.R:g})^2+z*z)"
        gmsh.model.mesh.field.setString(f, "F", f"{FINE:g}+({COARSE - FINE:g})*Step({rc - FINE:g}-{rr})")
        gmsh.model.mesh.field.setAsBackgroundMesh(f)
        for k in ("MeshSizeFromPoints", "MeshSizeFromCurvature", "MeshSizeExtendFromBoundary"):
            gmsh.option.setNumber(f"Mesh.{k}", 0)
        gmsh.option.setNumber("Mesh.ElementOrder", 2)
        gmsh.option.setNumber("Mesh.HighOrderOptimize", 1)
        gmsh.model.mesh.generate(3)
        tags, xyz, _ = gmsh.model.mesh.getNodes()
        _, nodes = gmsh.model.mesh.getElementsByType(11)
    finally:
        gmsh.finalize()
    idx = np.zeros(int(tags.max()) + 1, dtype=np.int64)
    idx[tags.astype(np.int64)] = np.arange(len(tags))
    return xyz.reshape(-1, 3), idx[nodes.astype(np.int64)].reshape(-1, 10)


def solve_case(xyz, tets, t, rho, lineal=False):
    rc, flat_z = P.RING_SECTION / 2 - t, -(P.RING_SECTION / 2 - aro.FLAT) + t
    c = xyz[tets[:, :4]].mean(axis=1)
    rad_c = np.hypot(c[:, 0], c[:, 1])
    in_core = (np.hypot(rad_c - aro.R, c[:, 2]) < rc) & (c[:, 2] > flat_z)
    ec = rho if lineal else rho ** EXP
    efac = np.where(in_core, ec, 1.0)
    # same supports and loads as aro.fem_ring
    ang = np.degrees(np.arctan2(xyz[:, 1], xyz[:, 0])) % 360
    top = xyz[:, 2] > 0
    dist = lambda a: np.abs((ang - a + 180) % 360 - 180) * np.pi / 180 * aro.R  # noqa: E731
    fixed = {}
    for k, a in enumerate((45, 135, 225, 315)):
        sel = np.flatnonzero((dist(a) < 4) & top & (np.hypot(np.hypot(xyz[:, 0], xyz[:, 1]) - aro.R, xyz[:, 2]) > rc))
        for n in sel:
            fixed[int(n)] = (0, 1, 2) if k in (0, 2) else (2,)
    weight = P.ARO_FEM["masa_piso_kg"] * 9.81
    load = P.ARO_FEM["manipulacion_N"]
    outer = np.flatnonzero(np.hypot(np.hypot(xyz[:, 0], xyz[:, 1]) - aro.R, xyz[:, 2]) > rc)      # on the wall: the core carries nothing applied
    loads = {int(n): (0.0, 0.0, -weight / len(outer)) for n in outer}
    patch = np.flatnonzero((dist(0) < 10) & top & (np.hypot(np.hypot(xyz[:, 0], xyz[:, 1]) - aro.R, xyz[:, 2]) > rc))
    for n in patch:
        f = loads.get(int(n), (0.0, 0.0, 0.0))
        loads[int(n)] = (f[0], f[1], f[2] - load / len(patch))
    r = F.solve(xyz, tets, fixed, loads, P.PETG_E, P.PETG_NU, efac=efac)
    ac = np.degrees(np.arctan2(c[:, 1], c[:, 0])) % 360
    dc = lambda a: np.abs((ac - a + 180) % 360 - 180) * np.pi / 180 * aro.R  # noqa: E731
    clean = (dc(0) > 15) & np.all([dc(a) > 10 for a in (45, 135, 225, 315)], axis=0)
    wall = clean & ~in_core
    s_wall = float(r["vm"][wall].max())
    s_local = float(np.percentile(r["vm"][~in_core], 99.5))
    s_core = float(r["vm"][clean & in_core].max()) if (clean & in_core).any() else 0.0
    lim_core = rho ** 1.5 * P.PETG_YIELD_Z
    return dict(s_pared=s_wall, fs_capas=P.PETG_YIELD_Z / s_wall, s995_pared=s_local, s_nucleo=s_core, fs_nucleo=lim_core / s_core if s_core else None,
                umax=float(np.linalg.norm(r["u"], axis=1).max()), reaccion_z_N=float(r["reac"][list(fixed), 2].sum()), carga_N=weight + load,
                elementos=len(tets), nodos=len(xyz), elementos_nucleo=int(in_core.sum()))


def grams(t, rho):
    vw, vc = volumes(t)
    return P.PETG_DENSITY * (vw + rho * vc) / 1000.0


def main():
    args = [a for a in sys.argv[1:] if ":" in a]
    lineal = "--lineal" in sys.argv
    cases = [tuple(int(x) for x in a.split(":")) for a in args] or SWEEP + MIN
    res = json.loads(OUTF.read_text(encoding="utf-8")) if OUTF.exists() else {}
    res.setdefault("supuestos", dict(ancho_linea=LINE, E_nucleo="E * rho^2 (C = 1)", malla_pared=FINE, malla_nucleo=COARSE, tapas="iguales a la pared"))
    meshes = {}
    for n, inf in cases:
        key = f"{n}p_{inf}%" + ("_lineal" if lineal else "")
        if key in res:
            continue
        t = n * LINE
        if t not in meshes:
            meshes = {t: mesh(t)}     # one mesh in memory
        xyz, tets = meshes[t]
        rep = solve_case(xyz, tets, t, inf / 100.0, lineal)
        rep.update(perimetros=n, relleno_pct=inf, pared_mm=t, gramos=grams(t, inf / 100.0))
        res[key] = rep
        OUTF.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        print(key, {k: round(v, 2) if isinstance(v, float) else v for k, v in rep.items() if k in ("gramos", "s_pared", "fs_capas", "s_nucleo", "fs_nucleo", "umax", "reaccion_z_N", "elementos")}, flush=True)


if __name__ == "__main__":
    main()
