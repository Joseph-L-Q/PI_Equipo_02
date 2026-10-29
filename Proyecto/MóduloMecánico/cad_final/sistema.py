"""Whole system of the simple version: node + LR1 + cords + lantern at linterna.profundidad + umbilical U1 + mooring
line C1 + buoy at the surface, with named parts (M*, B*, LR*, U1, C1) so Onshape keeps them apart.

    python sistema.py        (from cad_final/; run simple.py and boya_simple.py first)
U1 is a reference flexible hose (umbilical.diametro_manguera) swept along a smooth path from the PG7 of the lid of M1 to
the PG7 in the floor of B1s: it leaves the cord pyramid through the gap at 180 deg, its minimum bend radius and its
slack (umbilical.longitud - path) are checked. C1 goes from the apex up to the mooring eye B6s: the line carries the
lantern, the cable carries nothing.
Outputs: salida/simple/ENSAMBLE_sistema_simple.step, sistema_simple_iso.png, sistema.json.
"""
import json
import math
from pathlib import Path

import cadquery as cq
import numpy as np

import params as P
import simple as SM
import boya_simple as BS
import capsula as CP
import fase_a as FA
import layout
from checks import fix_step_stamp

OUT = SM.OUT


def node_parts():
    lay = layout.build(P.SIMPLE_ESP32_BASE, floors=P.SIMPLE_FLOORS)
    an = FA.analyse_box(lay)
    layers = P.SIMPLE_POCKET_LAYERS
    cp = {"M4": CP.capsule_body(), "M6": CP.bezel(), "M7": CP.window_disc(), "lid": CP.lid_plate()}
    ax, az, foot = SM.capsule_pose(lay, cp)
    half = SM.solid(SM.rail_half(lay, foot))
    m5s = SM.solid(SM.lid_with_foot(cp["lid"], ax, az, foot))
    node = SM.assemble(an, half, m5s, SM.pocket_cover(layers), cp, ax, az, SM.plates(layers, P.SIMPLE_PLATES),
                       SM.box_body_low(lay, layers), SM.trays_low(lay))
    return lay, node


def catmull_rom(W, n=30):
    """Centripetal Catmull-Rom through the waypoints W, n samples per span (OCC spline tangents made loops)."""
    W = np.asarray(W, float)
    Q = np.vstack([2 * W[0] - W[1], W, 2 * W[-1] - W[-2]])
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1:i + 3]
        t0 = 0.0
        t1 = t0 + np.linalg.norm(p1 - p0) ** 0.5
        t2 = t1 + np.linalg.norm(p2 - p1) ** 0.5
        t3 = t2 + np.linalg.norm(p3 - p2) ** 0.5
        for t in np.linspace(t1, t2, n, endpoint=False):
            a1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
            a2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
            a3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3
            b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
            b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3
            out.append((t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2)
    out.append(W[-1])
    return out


def hose(points, d):
    """Tube of diameter d swept along a smooth curve through the waypoints (straight up out of and into the glands);
    returns (solid, path length, minimum bend radius)."""
    vs = [cq.Vector(*p) for p in catmull_rom(points, 8)]
    path = cq.Edge.makeSpline(vs)
    try:
        prof = cq.Wire.makeCircle(d / 2, vs[0], path.tangentAt(0))
        tube = cq.Solid.sweep(prof, [], cq.Wire.assembleEdges([path]), True, True)
    except Exception:  # noqa: BLE001  OCC pipe shell can fail on long 3D splines: chain of short cylinders instead
        q = [path.positionAt(t) for t in np.linspace(0, 1, 160)]
        segs = [cq.Solid.makeCylinder(d / 2, (b - a).Length, a, b - a) for a, b in zip(q, q[1:])]
        segs += [cq.Solid.makeSphere(d / 2, p, angleDegrees1=-90, angleDegrees2=90) for p in q[1:-1]]
        tube = cq.Compound.makeCompound(segs)
    pts = np.array([path.positionAt(t).toTuple() for t in np.linspace(0, 1, 600)])
    rmin = math.inf
    for i in range(1, len(pts) - 1):
        a, b, c = pts[i - 1], pts[i], pts[i + 1]
        ab, bc, ca = np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c)
        area = np.linalg.norm(np.cross(b - a, c - a)) / 2
        if area > 1e-9:
            rmin = min(rmin, ab * bc * ca / (4 * area))
    return tube, path.Length(), rmin


def main():
    lay, node = node_parts()
    res_b = json.loads((BS.OUT / "resultados_boya.json").read_text(encoding="utf-8"))
    z_rod = SM.Z_RAIL - P.HOOK_DROP
    z_sep = z_rod + P.SEP_H
    z_apex = z_sep + P.APEX_H
    z_ws = z_rod + P.LANTERN_DEPTH                       # water surface
    zb0 = z_ws - res_b["calado"]                         # bottom of the buoy box
    dxb = -(BS.L / 2 - 30.0)                             # the mooring eye of the buoy right over the apex
    lant, axes, _ = SM.lantern(z_rod, z_sep, z_apex, fixed="ninguno")
    sep = SM.solid(SM.separator(z_sep))
    # buoy parts, moved to the surface
    buoy = {}
    for stem, qty in (("B1s_casco", 1), ("B2s_tapa", 1), ("B1bs_bandeja", 1), ("B6s_ojal", 1)):
        buoy[stem] = cq.importers.importStep(str(BS.OUT / "step" / f"{stem}.step")).val()
    for i, x in enumerate(BS.rail_x()):
        buoy[f"B3s_larguero_{i + 1}"] = BS.b3_larguero(x).val()
    for i, c in enumerate(BS.float_centres()):
        buoy[f"B5s_flotador_{i + 1}"] = BS.b5_flotador(*c).val()
    buoy = {k: v.translate(cq.Vector(dxb, 0, zb0)) for k, v in buoy.items()}
    pl, pw, pt = P.BUOY_PANEL
    buoy["B_panel_solar_ref"] = BS.dummies()["panel"].val().translate(cq.Vector(dxb, 0, zb0))
    eye = (dxb + BS.L / 2 - 30.0, 0.0, zb0 - 24.0 - 6.0)
    c1 = SM.segment((0, 0, z_apex), eye, P.LANTERN_CORD_D)
    # U1: lid gland -> up inside the cords -> over the LR1 ring through the 180 deg gap -> up to the buoy floor gland
    # (under the ring there are only ~13 mm between the lid and LR1)
    g0 = SM.lid_gland_point(lay)
    ux, uy = BS.layout()["umb"]
    g1 = (dxb + ux, uy, zb0)
    # waypoints tuned for a minimum bend radius over umbilical.radio_min (straight up 53 before turning)
    x0, y0, z0 = g0
    pts = [g0, (x0, y0, z0 + 53), (x0 - 6, y0 - 14, z0 + 93), (x0 - 30, y0 - 32, z0 + 133), (x0 - 80, y0 - 40, z0 + 163),
           (-180.0, 2.0, z0 + 203), (-230.0, 0.0, z0 + 338), (-225.0, 0.0, (z0 + zb0) / 2 + 80),
           (g1[0] - 25.0, 0.0, zb0 - 127), (g1[0] - 2.0, 0.0, zb0 - 47), g1]
    u1, length, rmin = hose(pts, P.UMB_HOSE_D)
    slack = P.UMB_LEN - length
    # clearances of U1 to the cords, LR1 and the node (sampled)
    from scipy.spatial import cKDTree
    import ensambles as E
    u_pts = E.surface_points([u1], 1.0)
    u_tree = cKDTree(u_pts)
    near = {}
    for k, (p, q) in axes.items():
        p, q = np.array(p), np.array(q)
        s = p + (q - p) * np.linspace(0, 1, 400)[:, None]
        near[k] = float(u_tree.query(s)[0].min() - P.LANTERN_CORD_D / 2)
    near["LR1"] = float(u_tree.query(E.surface_points([sep], 1.0))[0].min())
    fails = []
    if rmin < P.UMB_BEND_R:
        fails.append(f"radio minimo de U1 {rmin:.0f} < {P.UMB_BEND_R:g}")
    if slack < 0:
        fails.append(f"U1 necesita {length:.0f} mm y el umbilical mide {P.UMB_LEN:g}")
    if min(near.values()) < 5.0:
        fails.append(f"U1 roza la suspension: {min(near.values()):.1f} mm")
    # assembly with names
    asm = cq.Assembly(name="sistema_simple")
    for k, (sh, g) in node.items():
        asm.add(sh, name=k.replace(" ", "_"))
    for k, sh in lant.items():
        asm.add(sh, name="LR_" + k.replace(" ", "_"))
    asm.add(sep, name="LR1_separador")
    for k, sh in buoy.items():
        asm.add(sh, name=k)
    asm.add(u1, name="U1_umbilical")
    asm.add(c1, name="C1_cabo_amarre")
    path = OUT / "ENSAMBLE_sistema_simple.step"
    asm.export(str(path))
    fix_step_stamp(path)
    from render import render
    items = [(sh, "#5b8fb9" if g == "caja" else "#3a9d7a" if g == "riel" else "#3a7ca5", 1.0, True, None) for sh, g in node.values()]
    items += [(sh, "#c0504d" if k.startswith(("cuerda", "cabo")) else "#8a8a8a" if k == "aro" else "#b9d6e8",
               0.25 if k.startswith(("red", "piso")) else 0.9, False, None) for k, sh in lant.items()]
    items += [(sep, "#e07b39", 1.0, True, None), (u1, "#222222", 1.0, False, None), (c1, "#7a3e9d", 1.0, False, None)]
    items += [(sh, "#e07b39" if k.startswith("B5s") else "#1d1d3a" if "panel" in k else "#3a7ca5", 1.0, True, None) for k, sh in buoy.items()]
    water = cq.Workplane("XY").box(900, 700, 1).translate((dxb, 0, z_ws - 0.5)).val()
    items.append((water, "#7fb3d5", 0.2, False, None))
    render(items, OUT / "sistema_simple_iso.png", "iso",
           f"Sistema simple: linterna a {P.LANTERN_DEPTH / 1000:g} m, U1 de {length:.0f} mm (holgura {slack:.0f}), C1 del apice a la boya")
    res = dict(u1_largo=length, u1_holgura=slack, u1_radio_min=rmin, u1_aire=near, c1_largo=(np.array(eye) - np.array((0, 0, z_apex))).tolist(),
               z_superficie=z_ws, z_fondo_boya=zb0, fallas=fails)
    res["c1_largo"] = float(np.linalg.norm(np.array(eye) - np.array((0, 0, z_apex))))
    (OUT / "sistema.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"U1 {length:.0f} mm (holgura {slack:.0f}, radio min {rmin:.0f}), aire U1-suspension {min(near.values()):.1f} mm, C1 {res['c1_largo']:.0f} mm")
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
