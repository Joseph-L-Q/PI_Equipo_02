"""Whole system of the simple version: node + test lantern (ring, net, 4 cords to ONE tie point, no separator since tanda 3) at
linterna.profundidad + cabo C1 + umbilical U1 + the PET-bottle buoy (boya_pet.py, read-only use) at the surface, as a named
assembly: printed parts by code and stem (M*, B*), the rest REF_* so Onshape keeps them apart.

    python sistema.py        (from cad_final/; run simple.py (version simple) and boya_pet.py first)
U1 is a reference flexible hose (umbilical.diametro_manguera) swept along a smooth path from the PG7 of the lid of M1 to
the PG7 in the -X wall of the buoy box (B3): it leaves the cord cone through the gap at 180 deg, its minimum bend radius
and its slack (umbilical.longitud - path) are checked. REF_cabo (C1) goes straight up from the tie point to the mooring pad
of the buoy hull (B1, keel centre): the line carries the lantern, the cable carries nothing.
Outputs: salida/simple/ENSAMBLE_sistema_simple.step, ensamble_solidos_sistema.json, sistema_simple_iso.png, sistema.json.
"""
import json
import math
import re
from pathlib import Path

import cadquery as cq
import numpy as np

import params as P
import simple as SM
import boya_pet as BP
import capsula as CP
import fase_a as FA
import layout
from checks import fix_step_stamp

OUT = SM.OUT
BUOY_OUT = Path(__file__).resolve().parent.parent / "salida" / "boya_pet"


def node_parts():
    lay = layout.build(P.SIMPLE_ESP32_BASE, floors=P.SIMPLE_FLOORS)
    SM.set_pad(lay)
    an = FA.analyse_box(lay)
    depth = P.SIMPLE_POCKET_DEPTH
    cp = {"M4": CP.capsule_body(), "M6": CP.bezel(), "M7": CP.window_disc(), "lid": CP.lid_plate()}
    ax, az, foot = SM.capsule_pose(lay, cp)
    half = SM.solid(SM.rail_half(lay, foot))
    m5s = SM.solid(SM.lid_with_foot(cp["lid"], ax, az, foot))
    lastre = json.loads((OUT / "resultados.json").read_text(encoding="utf-8"))["lastre"]      # grams the V2 run found
    ballast = SM.ballast_solids(depth, lastre["por_bolsillo_g"], lastre["aparente"])
    node = SM.assemble(an, half, m5s, SM.pocket_cover(depth), cp, ax, az, ballast, SM.box_body_low(lay, depth), SM.trays_low(lay))
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
    """Tube of diameter d swept along a smooth curve through the waypoints (straight up out of the gland);
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


def route(g0, g1, radius=100.0, tail=35.0):
    """Waypoints of U1: up out of the lid gland, an S through the 180 deg gap between the cords, a vertical run outside the hull end
    (x of the arc start), and a quarter circle of `radius` that ends horizontal, with `tail` mm straight, into the -X wall PG7 of B3."""
    x0, y0, z0 = g0
    cx, zc = g1[0] - tail, g1[2] - radius
    arc = [(cx - radius * math.cos(math.radians(t)), 0.0, zc + radius * math.sin(math.radians(t))) for t in (0, 15, 30, 45, 60, 75, 90)]
    xo = arc[0][0]
    return [g0, (x0, y0, z0 + 70), (-60.0, 20.0, z0 + 190), (-100.0, 10.0, z0 + 350), (-145.0, 3.0, z0 + 450),
            (xo + 14, 0.0, z0 + 570), (xo, 0.0, z0 + 700), (xo, 0.0, zc - 100)] + arc + [g1]


def main():
    lay, node = node_parts()
    z_rod = SM.Z_RAIL - P.HOOK_DROP
    z_top_node = max(sh.BoundingBox().zmax for sh, _ in node.values())
    z_bend = z_top_node + P.CORD_CLEAR + P.LANTERN_CORD_D
    z_tie = z_rod + P.LANTERN_TIE_H
    z_ws = z_rod + P.LANTERN_DEPTH                       # water surface
    d = BP.dims(P.FLOT_BOTTLE, P.FLOT_COUNT)
    res_b = json.loads((BUOY_OUT / "resultados.json").read_text(encoding="utf-8"))
    calado = res_b["hidro"]["calado"]
    zb0 = z_ws - calado                                  # keel of the buoy hull
    dxb = 0.0                                            # the mooring pad (keel centre) right over the tie point
    lant, axes, _ = SM.lantern_tie(z_rod, z_bend, z_tie, fixed="ninguno")
    # buoy printed parts (the 4 of boya_pet.py) and its reference bodies, moved to the surface
    buoy = {}
    for stem in ("B1_casco", "B2_cubierta", "B3_caja", "B4_tapa"):
        buoy[stem] = cq.importers.importStep(str(BUOY_OUT / "step" / f"{stem}.step")).val().translate(cq.Vector(dxb, 0, zb0))
    dm = BP.dummies(d)
    buoy["REF_panel_solar"] = dm["panel"].val().translate(cq.Vector(dxb, 0, zb0))
    for i in (1, 2):
        buoy[f"REF_botella_{i}"] = dm[f"botella{i}"].val().translate(cq.Vector(dxb, 0, zb0))
    # REF_cabo (C1): straight up from the tie point to the mooring pad of the hull
    pad_pt = (dxb, 0.0, zb0)
    tie = (0.0, 0.0, z_tie)
    c1 = SM.segment(tie, pad_pt, P.LANTERN_CORD_D)
    axes["REF_cabo"] = [(tie, pad_pt)]
    # U1: lid gland -> up inside the cords -> out through the 180 deg gap -> up outside the cone -> into the PG7 of the -X wall of B3
    g0 = SM.lid_gland_point(lay)
    gl = BP.layout(d)
    g1 = (dxb + d["X0"] - d["Lx"] / 2, 0.0, zb0 + gl["umb_z"])
    pts = route(g0, g1)
    u1, length, rmin = hose(pts, P.UMB_HOSE_D)
    slack = P.UMB_LEN - length
    # clearances of U1 to the cords, the cabo and the node (sampled)
    from scipy.spatial import cKDTree
    import ensambles as E
    u_tree = cKDTree(E.surface_points([u1], 1.0))
    near = {}
    for k, segs in axes.items():
        s = np.vstack([np.array(p) + (np.array(q) - np.array(p)) * np.linspace(0, 1, 400)[:, None] for p, q in segs])
        near[k] = float(u_tree.query(s)[0].min() - P.LANTERN_CORD_D / 2)
    near["boya"] = float(u_tree.query(E.surface_points([buoy["B3_caja"]], 2.0))[0].min())
    fails = []
    if rmin < P.UMB_BEND_R:
        fails.append(f"radio minimo de U1 {rmin:.0f} < {P.UMB_BEND_R:g}")
    if slack < 0:
        fails.append(f"U1 necesita {length:.0f} mm y el umbilical mide {P.UMB_LEN:g}")
    if min(v for k, v in near.items() if k != "boya") < 5.0:
        fails.append(f"U1 roza la suspension: {min(v for k, v in near.items() if k != 'boya'):.1f} mm")
    # assembly with names (each body ONE valid solid)
    rec = []
    named = {}
    for k, (sh, g) in node.items():
        named[k] = SM.one_solid(k, sh, rec)
    for k, sh in lant.items():
        named[k] = SM.one_solid(k, sh, rec)
    for k, sh in buoy.items():
        named[k] = SM.one_solid(k, sh, rec)
    named["REF_umbilical"] = SM.one_solid("REF_umbilical", u1, rec)
    named["REF_cabo"] = SM.one_solid("REF_cabo", c1, rec)
    asm = cq.Assembly(name="sistema_simple")
    for k, sh in named.items():
        asm.add(sh, name=k)
    path = OUT / "ENSAMBLE_sistema_simple.step"
    asm.export(str(path))
    fix_step_stamp(path)
    bad = [r for r in rec if not r["valido"]]
    for r in bad:
        fails.append(f"ensamble: {r['nombre']} no es un solido unico valido ({r['solidos']} solidos)")
    step_names = re.findall(r"PRODUCT\('([^']*)'", path.read_text(encoding="utf-8", errors="replace"))
    n_back = sum(len(v.Solids()) for v in cq.importers.importStep(str(path)).vals())
    miss = [k for k in named if k not in step_names]
    if miss or n_back != len(named):
        fails.append(f"el STEP del sistema: {n_back} solidos leidos de {len(named)}, nombres que faltan {miss}")
    (OUT / "ensamble_solidos_sistema.json").write_text(json.dumps(dict(
        ensamble=path.name, cuerpos=len(rec), solidos_total=sum(r["solidos"] for r in rec), solidos_leidos_del_step=n_back,
        nombres_en_step=len(step_names) - 1, cuerpos_no_validos=[r["nombre"] for r in bad], solidos=rec),
        indent=1, ensure_ascii=False), encoding="utf-8")
    from render import render
    items = [(sh, "#5b8fb9" if g == "caja" else "#3a9d7a" if g == "riel" else "#3a7ca5", 1.0, True, None) for sh, g in node.values()]
    items += [(sh, "#c0504d" if k.startswith(("REF_cuerda", "REF_cabo")) else "#8a8a8a" if k == "REF_aro_superior" else "#b9d6e8",
               0.25 if k.startswith(("REF_linterna_malla", "REF_linterna_piso")) else 0.9, False, None) for k, sh in lant.items()]
    items += [(u1, "#222222", 1.0, False, None), (c1, "#c0504d", 1.0, False, None)]
    items += [(sh, "#1d1d3a" if "panel" in k else "#5dade2" if "botella" in k else "#e07b39" if k.startswith("B2") else "#3a7ca5",
               0.5 if "botella" in k else 1.0, True, None) for k, sh in buoy.items()]
    water = cq.Workplane("XY").box(900, 700, 1).translate((dxb, 0, z_ws - 0.5)).val()
    items.append((water, "#7fb3d5", 0.2, False, None))
    render(items, OUT / "sistema_simple_iso.png", "iso",
           f"Sistema simple: linterna a {P.LANTERN_DEPTH / 1000:g} m, U1 de {length:.0f} mm (holgura {slack:.0f}), cabo del nudo a la boya")
    res = dict(u1_largo=length, u1_holgura=slack, u1_radio_min=rmin, u1_aire=near, cabo_largo=float(np.linalg.norm(np.array(pad_pt) - np.array(tie))),
               z_superficie=z_ws, z_fondo_boya=zb0, calado_boya=calado, cuerpos=len(rec), solidos=n_back, fallas=fails)
    (OUT / "sistema.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"U1 {length:.0f} mm (holgura {slack:.0f}, radio min {rmin:.0f}), aire U1-suspension {min(v for k, v in near.items() if k != 'boya'):.1f} mm, "
          f"U1-boya {near['boya']:.1f}, cabo {res['cabo_largo']:.0f} mm, {len(rec)} cuerpos / {n_back} solidos")
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
