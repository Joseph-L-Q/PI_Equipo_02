"""FEM of the full rail M3s with fem_tet10 (for PCs without CalculiX), same cases and faces as fem.py.

    python fem_riel.py [--step other.step] [--seccion 8] [--holgura 0.4] [--malla 2.5] [--json out.json]

riel_agua: C seat fixed. riel_izado: flange face fixed. 150 N at the front of the capsule. fem.py carries the load with a
rigid body to the saddle holes; here it is a distributing coupling (same force and moment, shared over the hole nodes),
softer locally. Use --step with the previous M3s to calibrate against its CalculiX result in fem/fem.json.
"""
import argparse
import json
import math
import os
from pathlib import Path

os.environ.setdefault("LG_VERSION", "P2_robusto")

import numpy as np  # noqa: E402

import fem  # noqa: E402
import fem_tet10 as F  # noqa: E402
import params as P  # noqa: E402


def coupling(xyz, ids, ref, load):
    """Nodal forces equivalent to the force `load` applied at `ref`, shared over the nodes `ids`."""
    pts = xyz[ids]
    c = pts.mean(axis=0)
    r = pts - c
    moment = np.cross(np.array(ref) - c, load)
    A = np.zeros((3, 3))
    for v in r:
        A += np.dot(v, v) * np.eye(3) - np.outer(v, v)
    w = np.linalg.solve(A, moment)
    return {int(n): tuple(np.array(load) / len(ids) + np.cross(w, v)) for n, v in zip(ids, r)}


def case(name, step, g, size, fixed_test, load_test):
    nodes, tets, surf = fem.mesh(step, size)
    tags = np.array(list(nodes.keys()))
    idx = {int(t): i for i, t in enumerate(tags)}
    xyz = np.array([nodes[t] for t in tags])
    T = np.vectorize(idx.get)(tets)
    fixed_n = fem.pick(surf, fixed_test)
    load_n = fem.pick(surf, load_test) - fixed_n
    if not fixed_n or not load_n:
        raise SystemExit(f"{name}: no encontre las caras (fijas {len(fixed_n)}, carga {len(load_n)})")
    fixed = {idx[int(n)]: (0, 1, 2) for n in fixed_n}
    load = (0.0, 0.0, -P.HANDLING_LOAD_N)
    r = F.solve(xyz, T, fixed, coupling(xyz, np.array([idx[int(n)] for n in load_n]), g["front"], load), P.PETG_E, P.PETG_NU)
    rep = F.report(r, P.PETG_YIELD, P.PETG_YIELD_Z)
    rep.update(nodos=len(xyz), elementos=len(T), nodos_fijos=len(fixed), nodos_carga=len(load_n), reaccion_z=round(float(r["reac"][list(fixed), 2].sum()), 2))
    print(name, {k: round(v, 2) if isinstance(v, float) else v for k, v in rep.items()}, flush=True)
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step")
    ap.add_argument("--seccion", type=float)
    ap.add_argument("--holgura", type=float)
    ap.add_argument("--malla", type=float, default=P.FEM_MESH)
    ap.add_argument("--json")
    a = ap.parse_args()
    if a.seccion:
        P.RING_SECTION = a.seccion
    if a.holgura:
        P.SIMPLE_HOOK_C = (a.holgura, P.SIMPLE_HOOK_C[1], P.SIMPLE_HOOK_C[2])
    step = Path(a.step) if a.step else fem.STEP / "M3s_riel_gancho.step"
    g = fem.geometry()
    rx, rz = g["ring"]
    ri = P.RING_SECTION / 2 + P.SIMPLE_HOOK_C[0]
    seat = lambda bb: fem.near(bb, x=rx, z=rz, tol=ri + 1.0) and (bb[5] - bb[2]) <= 2 * ri + 1.0 and (bb[3] - bb[0]) <= 2 * ri + 1.0  # noqa: E731
    flange = lambda bb: abs(bb[0] - g["x_flange"]) < 0.05 and abs(bb[3] - g["x_flange"]) < 0.05  # noqa: E731

    def saddle(bb):
        c = ((bb[0] + bb[3]) / 2, (bb[1] + bb[4]) / 2)
        return (any(math.dist(c, p) < 1.0 for p in g["pts"]) and bb[3] - bb[0] <= P.M3_INSERT_HOLE + 0.5
                and bb[4] - bb[1] <= P.M3_INSERT_HOLE + 0.5 and bb[5] - bb[2] > 0.5)
    res = dict(step=step.name, seccion=P.RING_SECTION, holgura=P.SIMPLE_HOOK_C[0], malla=a.malla, solver="fem_tet10",
               riel_agua=case("riel_agua", step, g, a.malla, seat, saddle), riel_izado=case("riel_izado", step, g, a.malla, flange, saddle))
    if a.json:
        Path(a.json).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
