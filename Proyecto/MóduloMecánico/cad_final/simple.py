"""Simple version of the node for the real prototype (ring Ø200), behind params.VERSION = "simple".

One-piece rail of SIMPLE_RAIL_L split in two equal halves M3s with a flat joint at x = 0 under the box (4 M3 through
ears), no M8 rod, no extensions or tips; fixed C hooks M9s with a strap slot; capsules at a fixed tilt held by the lid
M5s, whose foot is a saddle bolted across the rail (no toothed hinge). Box M1, lid M2, tray M11, capsule M4, bezel M6
and window M7 are the modular ones. Test lantern: ring, net, separator LR1 above the node, 4 cords going straight up
to the separator and on to the apex, central line to the fixed point, slack umbilical.

    python simple.py        (from cad_final/; build.py runs it when version = "simple")
Outputs: salida/simple/ (stl/, step/, simscale/, ensamble_simple_D200.step, renders), salida/linterna_prueba/
(LR1_separador) and cad_final/reporte_simple.md.
Frame: the box frame (outer bottom z = 0), X along the rail; the -X half is the +X one turned 180 deg about Z.
"""
import math
import time
from itertools import combinations
from pathlib import Path

import cadquery as cq
import numpy as np

import params as P
import camara
camara.RAIL_ROD_M8 = False      # no M8 rod here; set before importing riel, which reads camara.lanes() on import
import riel  # noqa: E402
riel.RAIL_ROD_M8 = False
import capsula as CP  # noqa: E402
import ensambles as E  # noqa: E402
import fase_a as FA  # noqa: E402
import layout  # noqa: E402
from checks import brep_check, export_part, fix_step_stamp, mesh_checks, min_thickness, sanitize  # noqa: E402

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
OUT = MOD / "salida" / "simple"
LR_OUT = MOD / "salida" / "linterna_prueba"
Z0, YAX, ZAX = cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), cq.Vector(0, 0, 1)

S, W = P.RAIL_SECTION, P.RAIL_WALL
XT = P.SIMPLE_RAIL_L / 2
R_RING = P.SIMPLE_RING_D / 2
SLOT_MARGIN = 2.0          # x gap between the saddle and the cable exit slot (constant listed in the report)
NET_STEEL = FA.NET_STEEL
RHO_W = P.SEAWATER_DENSITY
_box = riel._box


def _cyl(p, d, r, h):
    return cq.Workplane().add(cq.Solid.makeCylinder(r, h, cq.Vector(*p), cq.Vector(*d)))


def solid(s):
    return s.val() if hasattr(s, "val") else s


def put(shape, side):
    """+X part -> the -X one is the same part turned 180 deg about Z."""
    s = solid(shape)
    return s.rotate(Z0, ZAX, 180) if side < 0 else s


# ------------------------------------------------------------------ rail half M3s
def joint_ears(c, layers):
    """z range of the joint ears (on the ballast pocket roof, under the flange) and the (y, z) of the 4 M3."""
    z_lo = camara.pocket_z(c, layers)[2]
    z_hi = -P.CHAMBER_FLANGE_W[1]
    m = (z_hi - z_lo) / 4
    ew = P.SIMPLE_JOINT_EAR[0]
    return z_lo, z_hi, [(sy * (S / 2 + ew / 2), z) for sy in (1, -1) for z in (z_lo + m, z_hi - m)]


def foot_frame(c):
    """Capsule saddle along the rail: x range (clear of the cable exit slot), x of the 2 bolts, z of the bolts."""
    h, ln, dist = P.RAIL_EXIT_SLOT
    x1 = XT - dist - ln - SLOT_MARGIN
    x0 = x1 - P.SIMPLE_FOOT[0]
    sp, zb = P.SIMPLE_FOOT_BOLTS
    xc = (x0 + x1) / 2
    return x0, x1, (xc - sp / 2, xc + sp / 2), c.z_rail + zb


def rail_half(lay, c, layers):
    """+X half: half of the cable chamber (pocket, T-slot, M4 to the box) + plain conduit to the tip, end wall with the
    nut channel open, cable exit on +Y, holes of the saddle bolts and the joint ears at x = 0."""
    body = camara.chamber_solid(lay, layers)["M3_riel_central"]
    L2, z0 = P.RAIL_CENTRAL_L / 2, c.z_rail
    end = P.RAIL_TIP_END_T
    tube = _box(L2 - 0.01, XT, -S / 2, S / 2, z0, z0 + S).cut(
        _box(L2 - 1, XT - end, -S / 2 + W, S / 2 - W, z0 + W, z0 + S - W))
    tube = riel._tslot(tube, z0, L2, XT)
    tube = tube.cut(_box(XT - end - 1, XT + 1, -riel.TS_W / 2, riel.TS_W / 2, z0 + W - 1, z0 + W + riel.TS_H))
    body = riel._exit_slot(body.union(tube), z0, XT)
    _, _, bx, bz = foot_frame(c)
    for x in bx:
        body = body.cut(_cyl((x, -S, bz), (0, 1, 0), P.M4_CLEAR / 2, 2 * S))
    z_lo, z_hi, pts = joint_ears(c, layers)
    ew, et = P.SIMPLE_JOINT_EAR
    for sy in (1, -1):
        ya, yb = sorted((sy * (S / 2 - 0.01), sy * (S / 2 + ew)))
        body = body.union(_box(0, et, ya, yb, z_lo - 0.01, z_hi + 0.01))
    for y, z in pts:
        body = body.cut(_cyl((-1, y, z), (1, 0, 0), P.M3_CLEAR / 2, et + 2))
    return body.intersect(_box(0, XT + 1, -200, 200, -500, 500))


# ------------------------------------------------------------------ hook M9s
def hook(strap=None):
    """M9s in its own frame: ring rod centre at the origin, rod along Y, rail bottom at z = HOOK_DROP. Open C seat
    (drops onto the rod), web with the strap slot along X, flange with 2 M4 to nuts in the T-slot. strap = False
    (gancho.correa): no slot and a flared mouth, so the node lifts off the ring without undoing anything."""
    strap = P.SIMPLE_HOOK_STRAP if strap is None else strap
    clr, wall, seat = P.SIMPLE_HOOK_C
    ri = P.RING_SECTION / 2 + clr
    ro = ri + wall
    fl_l, fl_t = P.HOOK_FLANGE
    zt = P.HOOK_DROP
    wy = P.STRAP_W / 2 + P.JAW_WALL
    wx = P.HOOK_CONTACT_W / 2
    fy = max(S / 2, wy)
    h = _box(-fl_l / 2, fl_l / 2, -fy, fy, zt - fl_t, zt)
    h = h.union(_box(-wx, wx, -wy, wy, ro - wall / 2, zt - fl_t + 0.01))
    h = h.union(_cyl((0, -seat / 2, 0), (0, 1, 0), ro, seat))
    h = h.cut(_cyl((0, -wy - 1, 0), (0, 1, 0), ri, 2 * wy + 2))
    h = h.cut(_box(-ri, ri, -wy - 1, wy + 1, -ro - 1, 0))
    if strap:
        zs = strap_z()
        h = h.cut(_box(-wx - 1, wx + 1, -P.STRAP_W / 2, P.STRAP_W / 2, zs - P.STRAP_SLOT_T / 2, zs + P.STRAP_SLOT_T / 2))
    else:
        flare = ri + 0.6 * wall                 # mouth opens from ri at the rod centre to this at the tips
        h = h.cut(cq.Workplane("XZ").workplane(offset=-wy - 1).polyline(
            [(-ri, 0.01), (ri, 0.01), (flare, -ro - 1), (-flare, -ro - 1)]).close().extrude(2 * wy + 2))
    for x in (-P.SIMPLE_HOOK_BOLT_X, P.SIMPLE_HOOK_BOLT_X):
        h = h.cut(_cyl((x, 0, zt - fl_t - 1), (0, 0, 1), P.M4_CLEAR / 2, fl_t + 2))
    return h


def strap_z():
    clr, wall, _ = P.SIMPLE_HOOK_C
    return (P.RING_SECTION / 2 + clr + wall + P.HOOK_DROP - P.HOOK_FLANGE[1]) / 2


def strap_band(t=1.5):
    """Strap loop in the hook frame (render only): through the web slot, down both sides of the C, under the rod."""
    clr, wall, _ = P.SIMPLE_HOOK_C
    ro = P.RING_SECTION / 2 + clr + wall
    zs, w = strap_z(), P.STRAP_W / 2
    xo, zb = ro + 1.0 + t, -ro - 1.0 - t
    return _box(-xo, xo, -w, w, zb, zs + t / 2).cut(_box(-xo + t, xo - t, -w - 1, w + 1, zb + t, zs - t / 2))


def assemble(an, ch, half, hk, m5s, cover, cp, ax, az, z_rod, plates, strap=False):
    """name -> (shape, group) of the whole node in the box frame; strap=True adds the strap loops (render only)."""
    cap_w = {kk: place_cap(cp[kk], ax, az) for kk in ("M4", "M6", "M7")}
    node = {"M1 caja": (an["m1"], "caja"), "M2 tapa": (an["m2"], "caja")}
    node.update({f"M11 {kk}": (t, "caja") for kk, t in an["trays"].items()})
    node.update({"M3t tapa bolsillo n": (cover, "riel"), "M3t tapa bolsillo s": (solid(ch["tapa_bolsillo_s"]), "riel")})
    node.update({f"pletina {i + 1}": (p, "lastre") for i, p in enumerate(plates)})
    for side, sg in ((1, "+X"), (-1, "-X")):
        node[f"M3s riel {sg}"] = (put(half, side), "riel")
        node[f"M9s gancho {sg}"] = (put(hk.translate(cq.Vector(R_RING, 0, z_rod)), side), "gancho" + sg)
        if strap:
            node[f"correa {sg}"] = (put(solid(strap_band()).translate(cq.Vector(R_RING, 0, z_rod)), side), "correa")
        node[f"M5s tapa con pie {sg}"] = (put(m5s, side), "capsula" + sg)
        for kk, nm in (("M4", "M4 capsula"), ("M6", "M6 bisel"), ("M7", "M7 ventana")):
            node[f"{nm} {sg}"] = (put(cap_w[kk], side), "capsula" + sg)
    return node


# ------------------------------------------------------------------ capsule with the fixed foot (M5s)
def capsule_pose(c, parts):
    """(ax, az) of the capsule frame origin for the fixed tilt: top of the tilted capsule SIMPLE_FOOT_GAP under the
    saddle plate; the lid face centre on the back normal through the saddle centre (clamped)."""
    th = math.radians(P.SIMPLE_CAP_TILT)
    zmax = max(solid(parts[k]).rotate(Z0, YAX, P.SIMPLE_CAP_TILT).BoundingBox().zmax for k in ("M4", "lid", "M6"))
    x0, x1, _, _ = foot_frame(c)
    z_pb = c.z_rail - P.SIMPLE_FOOT[1]
    az = z_pb - P.SIMPLE_FOOT_GAP - zmax
    xl = CP.cap_dims()[4]
    cf_z = az - xl * math.sin(th)
    off = (z_pb - cf_z) / math.tan(th) if th > 1e-6 else 80.0
    off = min(max(off, P.SIMPLE_FOOT[0] / 2), 80.0)
    ax = (x0 + x1) / 2 + off - xl * math.cos(th)
    return ax, az


def place_cap(shape, ax, az):
    return solid(shape).rotate(Z0, YAX, P.SIMPLE_CAP_TILT).translate(cq.Vector(ax, 0, az))


def lid_with_foot(c, lid, ax, az):
    """M5s in the box frame (+X side): lid plate + web + saddle (plate under the rail, two cheeks, 2 M4 across)."""
    th = math.radians(P.SIMPLE_CAP_TILT)
    fl, ft, fc = P.SIMPLE_FOOT
    x0, x1, bx, bz = foot_frame(c)
    z_pb = c.z_rail - ft
    yo = S / 2 + P.FIT_CLEAR + fc
    saddle = _box(x0, x1, -yo, yo, z_pb, c.z_rail)
    for sy in (1, -1):
        ya, yb = sorted((sy * (S / 2 + P.FIT_CLEAR), sy * yo))
        saddle = saddle.union(_box(x0, x1, ya, yb, c.z_rail - 0.01, c.z_rail + S))
    xl = CP.cap_dims()[4]
    hw = CP.cap_dims()[3] / 2 - 4.0

    def lid_pt(z, inset):
        """Point of the lid face (capsule frame x = xl + inset, height z) in the box frame; inset > 0 goes into the lid."""
        x, zz = xl + inset, z
        return (ax + x * math.cos(th) + zz * math.sin(th), az - x * math.sin(th) + zz * math.cos(th))
    pts = [(x0, z_pb), (x1, z_pb), lid_pt(hw, 1.0), lid_pt(-hw, 1.0)]
    from scipy.spatial import ConvexHull
    hull = ConvexHull(np.array(pts))
    poly = [tuple(map(float, pts[i])) for i in hull.vertices]
    yw = P.SIMPLE_FOOT_WEB / 2
    web = cq.Workplane("XZ").workplane(offset=-yw).polyline(poly).close().extrude(2 * yw)
    foot = saddle.union(web).union(cq.Workplane().add(place_cap(lid, ax, az)))
    for x in bx:
        foot = foot.cut(_cyl((x, -yo - 1, bz), (0, 1, 0), P.M4_CLEAR / 2, 2 * yo + 2))
    return foot


# ------------------------------------------------------------------ test lantern and separator LR1
def sep_points(z):
    return [(R_RING * math.cos(math.radians(a)), R_RING * math.sin(math.radians(a)), z) for a in P.SIMPLE_CORD_AZ]


def separator(z_mid):
    """LR1 in the box frame, mid plane at z_mid: ring of the ring diameter or spokes to the centre, a hole per cord."""
    w, t = P.SEP_SECTION
    z0 = z_mid - t / 2
    if P.SEP_TYPE == "aro":
        s = cq.Workplane("XY").workplane(offset=z0).circle(R_RING + w / 2).circle(R_RING - w / 2).extrude(t)
    else:
        s = cq.Workplane("XY").workplane(offset=z0).circle(1.5 * w).extrude(t)
        for a in P.SIMPLE_CORD_AZ:
            spoke = _box(0, R_RING, -w / 2, w / 2, z0, z0 + t).union(_cyl((R_RING, 0, z0), (0, 0, 1), w / 2, t))
            s = s.union(spoke.rotate((0, 0, 0), (0, 0, 1), a))
    for x, y, _ in sep_points(z0):
        s = s.cut(_cyl((x, y, z0 - 1), (0, 0, 1), P.SEP_HOLE / 2, t + 2))
    return s


def segment(p, q, d):
    v = cq.Vector(*q) - cq.Vector(*p)
    return cq.Solid.makeCylinder(d / 2, v.Length, cq.Vector(*p), v)


def lantern(z_rod, z_sep, z_apex):
    """Ring, net with floors, vertical cords, upper cords, central line, fixed point and slack umbilical (box frame)."""
    rd = P.RING_SECTION
    out = {"aro": cq.Solid.makeTorus(R_RING, rd / 2, cq.Vector(0, 0, z_rod), ZAX)}
    axes = {}
    h = P.LANTERN_NET_H
    z_net = z_rod - rd / 2
    out["red"] = cq.Solid.makeCylinder(R_RING, h, cq.Vector(0, 0, z_net - h), ZAX).cut(
        cq.Solid.makeCylinder(R_RING - P.LANTERN_NET_T, h + 2, cq.Vector(0, 0, z_net - h - 1), ZAX))
    for k in range(P.LANTERN_FLOORS):
        z = z_net - h * (k + 1) / (P.LANTERN_FLOORS + 1)
        out[f"piso {k + 1}"] = cq.Solid.makeCylinder(R_RING - P.LANTERN_NET_T - 1, 1.0, cq.Vector(0, 0, z), ZAX)
    z_top = z_apex + P.LANTERN_LINE_L
    for (x, y, _), a in zip(sep_points(0), P.SIMPLE_CORD_AZ):
        axes[f"cuerda vertical {int(a)}"] = ((x, y, z_rod), (x, y, z_sep))
        axes[f"cuerda al apice {int(a)}"] = ((x, y, z_sep), (0, 0, z_apex))
    if P.LANTERN_CENTRAL_LINE:
        axes["cabo central"] = ((0, 0, z_apex), (0, 0, z_top))
    for name, (p, q) in axes.items():
        out[name] = segment(p, q, P.LANTERN_CORD_D)
    if P.LANTERN_FIXED_POINT == "boya":
        out["boya (punto fijo)"] = solid(_box(-105, 105, -70, 70, z_top, z_top + 76))
        buoy_end = (60.0, 0.0, z_top)
    else:
        out["estructura (punto fijo)"] = solid(_box(-150, 150, -10, 10, z_top, z_top + 20))
        out["boya"] = solid(_box(-105, 105, 180, 320, z_top, z_top + 76))
        buoy_end = (0.0, 200.0, z_top)
    return out, axes, buoy_end


def umbilical(gland, buoy_end):
    """Slack umbilical: up from the gland, then a sagging curve to the buoy (render and STEP only)."""
    p0 = np.array(gland, float)
    p1 = p0 + np.array([0, 0, 40.0])
    p2 = np.array(buoy_end, float)
    pts = [p0]
    for t in np.linspace(0, 1, 13):
        pts.append(p1 + (p2 - p1) * t - np.array([0, 0, P.UMB_SAG * 4 * t * (1 - t)]))
    d = P.UMBILICAL[0]
    return [segment(tuple(a), tuple(b), d) for a, b in zip(pts, pts[1:]) if np.linalg.norm(b - a) > 1e-6]


# ------------------------------------------------------------------ checks
def process(name, shape, stem, stl_dir, step_dir, thick=True, orient_name=None):
    """Sanitize, B-rep check, export, print orientation (the given one, or the fewest overhangs that fits), wall
    thickness."""
    shp = sanitize(cq.Workplane().add(solid(shape)))
    chk = brep_check(shp)
    export_part(shp, stem, stl_dir, step_dir)
    path = str(stl_dir / f"{stem}.stl")
    best = None
    for on, orient in CP.ORIENTS.items():
        if orient_name and on != orient_name:
            continue
        mc = mesh_checks(path, P.PRINT_BED, orient)
        if mc["fits_bed"] and (best is None or mc["overhang_mm2"] < best[1]["overhang_mm2"]):
            best = (on, mc)
    if best is None:
        best = ("no cabe", mesh_checks(path, P.PRINT_BED, None))
    p1, pmin = min_thickness(path) if thick else (float("nan"), float("nan"))
    return dict(name=name, stem=stem, shape=shp, chk=chk, orient=best[0], mc=best[1], p1=p1, pmin=pmin)


def section_props(shape, x):
    """Area, I about the horizontal axis through the centroid and c of the rail section at x (0.05 mm slice)."""
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps
    t = 0.05
    sl = solid(shape).intersect(solid(_box(x, x + t, -100, 100, -300, 300)))
    pr = GProp_GProps()
    BRepGProp.VolumeProperties_s(sl.wrapped, pr)
    A = pr.Mass() / t
    zc = pr.CentreOfMass().Z()
    mi = pr.MatrixOfInertia()                        # about the centroid: (y2+z2), (x2+z2), (x2+y2) on the diagonal
    i_zz = (mi.Value(1, 1) + mi.Value(2, 2) - mi.Value(3, 3)) / 2 / t     # integral of z^2 per unit length
    bb = sl.BoundingBox()
    return A, i_zz, max(bb.zmax - zc, zc - bb.zmin)


def min_air(node_shapes, cords, solids):
    """Minimum distance (mm) to the node surfaces: cords = name -> (p, q, radius), axis sampled every mm and the radius
    subtracted; solids = name -> shape, surface sampled."""
    from scipy.spatial import cKDTree
    tree = cKDTree(E.surface_points(node_shapes, 0.7))
    out = {}
    for name, (p, q, r) in cords.items():
        p, q = np.array(p, float), np.array(q, float)
        n = int(max(20, np.linalg.norm(q - p)))
        out[name] = float(tree.query(p + (q - p) * np.linspace(0, 1, n)[:, None])[0].min() - r)
    for name, sh in solids.items():
        out[name] = float(tree.query(E.surface_points([sh], 0.7))[0].min())
    return out


def min_separator_h(node_pts, z_rod):
    """Lowest mid plane of the separator over the ring rod that keeps CORD_CLEAR to the node below it."""
    w, t = P.SEP_SECTION
    xy = node_pts[:, :2]
    if P.SEP_TYPE == "aro":
        rr = np.linalg.norm(xy, axis=1)
        near = np.abs(rr - R_RING) <= w / 2 + P.CORD_CLEAR
    else:
        near = np.zeros(len(xy), bool)
        for a in P.SIMPLE_CORD_AZ:
            u = np.array([math.cos(math.radians(a)), math.sin(math.radians(a))])
            s = np.clip(xy @ u, 0, R_RING)
            near |= np.linalg.norm(xy - s[:, None] * u, axis=1) <= w / 2 + P.CORD_CLEAR
        near |= np.linalg.norm(xy, axis=1) <= 1.5 * w + P.CORD_CLEAR
    if not near.any():
        return 0.0
    return float(node_pts[near, 2].max() + P.CORD_CLEAR + t / 2 - z_rod)


# ------------------------------------------------------------------ hand calculations
def hand_calcs(c, rail_shape, x_load, x_front, layers):
    F, D = P.HANDLING_LOAD_N, P.SIMPLE_RING_D
    out = {}
    # rail on the hooks (water), 150 N on one capsule: cantilever past the hook
    xs = (R_RING + P.HOOK_FLANGE[0] / 2 + foot_frame(c)[0]) / 2       # plain tube between the hook and the saddle
    A, I, cz = section_props(rail_shape, xs)
    Mb = F * (x_load - R_RING)
    sb = Mb / (I / cz)
    out["riel"] = dict(x_sec=xs, A=A, I=I, c=cz, M=Mb, sigma=sb, fs=P.PETG_YIELD / sb, fs_z=P.PETG_YIELD_Z / sb,
                       flecha=F * (x_load - R_RING) ** 3 / (3 * P.PETG_E * I))
    # flat joint at x = 0 without counting the box: hogging moment from the far hook, tension in the upper M3
    r_far = F * (x_load - R_RING) / D
    M0 = r_far * R_RING
    z_lo, z_hi, pts = joint_ears(c, layers)
    zb = sum(z for _, z in pts) / len(pts)
    lever = zb - c.z_rail
    T = M0 / lever
    tb = T / 4
    out["union"] = dict(M=M0, lever=lever, T=T, por_m3=tb, sigma_m3=tb / 5.03,
                        aplast=tb / (P.M3_NUT[0] ** 2 * math.sqrt(3) / 2 - math.pi * P.M3_CLEAR ** 2 / 4))
    # lifting by the handle (out of the water), 150 N on one capsule: inserts of the box (modular §4)
    out["insertos"] = F * (x_load + 40.0) / 80.0 / 2
    # hook: 75 N on the C seat (curved beam, M = F r / 2), 2 M4 to the T-slot
    clr, wall, seat = P.SIMPLE_HOOK_C
    rm = P.RING_SECTION / 2 + clr + wall / 2
    Mh = P.HOOK_LOAD_N * rm / 2
    sh = 6 * Mh / (seat * wall ** 2)
    out["gancho"] = dict(M=Mh, sigma=sh, fs=P.PETG_YIELD / sh, labios=P.HOOK_LOAD_N / 2 / (2 * 1.2 * P.M4_NUT[0]))
    # capsule foot: 150 N at the capsule front, saddle with 2 horizontal M4 bearing on both rail walls
    x0, x1, bx, bz = foot_frame(c)
    sp = P.SIMPLE_FOOT_BOLTS[0]
    Mf = F * (x_front - (x0 + x1) / 2)
    fb = F / 2 + Mf / sp
    bear = fb / (2 * P.M4_CLEAR * W)
    out["pie"] = dict(M=Mf, por_m4=fb, aplast=bear, fs=P.PETG_YIELD / bear, fs_z=P.PETG_YIELD_Z / bear)
    return out


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    for d in (OUT / "stl", OUT / "step", OUT / "simscale", LR_OUT):
        d.mkdir(parents=True, exist_ok=True)
    fails = []
    lay = layout.build(floors=1)
    c = camara.dims(lay)
    layers = P.PLATE_POCKET_LAYERS
    k = P.SIMPLE_PLATES
    if k > layers:
        fails.append(f"lastre.pletinas = {k} no entra en el bolsillo (capacidad {layers})")
    an = FA.analyse_box(lay)
    ch = camara.chamber_solid(lay, layers)
    z_rod = c.z_rail - P.HOOK_DROP
    print("caja y camara", f"{time.time() - t0:.0f}s", "z_rail", round(c.z_rail, 2), flush=True)

    # pieces
    half = solid(rail_half(lay, c, layers))
    hk = solid(hook())
    cp = {"M4": CP.capsule_body(), "M6": CP.bezel(), "M7": CP.window_disc(), "lid": CP.lid_plate()}
    ax, az = capsule_pose(c, cp)
    m5s = solid(lid_with_foot(c, cp["lid"], ax, az))
    cover = solid(ch["tapa_bolsillo_n"])
    stl, step = OUT / "stl", OUT / "step"
    # flange down like the modular central: bending along the layers (standing up has fewer overhangs but the layers
    # would cross the rail, and the hand calculation assumes this orientation)
    rows = [process("M3s riel, mitad", half, "M3s_riel_mitad", stl, step, orient_name="X180"),
            process("M9s gancho en C", hk, "M9s_gancho", stl, step),
            process("M5s tapa con pie", m5s, "M5s_capsula_tapa_pie", stl, step),
            process("M3t tapa del bolsillo", cover, "M3t_tapa_bolsillo", stl, step, thick=False),
            process("M1 caja, cuerpo", an["m1"], "M1_caja_cuerpo", stl, step, thick=False),
            process("M2 caja, tapa con asa", an["m2"], "M2_caja_tapa", stl, step, thick=False)]
    for kk, t in an["trays"].items():
        rows.append(process(f"M11 bandeja ({kk})", t, kk if kk.startswith("M11") else f"M11_{kk}", stl, step, thick=False))
    rows += [process("M4 capsula, cuerpo", cp["M4"], "M4_capsula_cuerpo", stl, step, thick=False),
             process("M6 bisel", cp["M6"], "M6_capsula_bisel", stl, step, thick=False),
             process("M7 ventana (acrilico)", cp["M7"], "M7_capsula_ventana", stl, step, thick=False)]
    for r in rows:
        ok = r["chk"]["ok"] and r["mc"]["watertight"] and r["mc"]["bodies"] == 1 and r["mc"]["fits_bed"]
        if not ok:
            fails.append(f"{r['stem']}: brep={r['chk']} estanco={r['mc']['watertight']} cuerpos={r['mc']['bodies']} cama={r['mc']['fits_bed']}")
        if r["p1"] == r["p1"] and r["p1"] < P.MIN_WALL:
            fails.append(f"{r['stem']}: espesor p1 {r['p1']:.2f} < {P.MIN_WALL}")
        print(f"{r['stem']:24s} ok={ok} or={r['orient']} bbox={tuple(round(v, 1) for v in r['mc']['bbox'])} "
              f"ov={r['mc']['overhang_mm2']:.0f} p1={r['p1']:.2f}", flush=True)
    R = {r["stem"]: r["shape"] for r in rows}
    half, hk, m5s = R["M3s_riel_mitad"], R["M9s_gancho"], R["M5s_capsula_tapa_pie"]
    print("piezas", f"{time.time() - t0:.0f}s", flush=True)

    # node in the box frame
    plates = [solid(p) for p in camara.plates_solid(lay, k)]
    node = assemble(an, ch, half, hk, m5s, cover, cp, ax, az, z_rod, plates)

    # interferences inside the node (touching faces give ~0)
    bbs = {kk: E.bbox(v[0]) for kk, v in node.items()}
    pairs, slivers = [], []
    for a, b in combinations(node, 2):
        if node[a][1] == node[b][1] and node[a][1] in ("caja", "lastre"):
            continue
        if E.bb_hit(bbs[a], bbs[b]):
            inter = node[a][0].intersect(node[b][0])
            v = inter.Volume()
            if not (v <= P.INTERF_TOL):
                bb = inter.BoundingBox()
                # camara.py overlaps the pocket covers 0.01 mm into the chamber wall so they fuse (modular too)
                (slivers if min(bb.xlen, bb.ylen, bb.zlen) <= 0.011 else pairs).append((a, b, v))
    for a, b, v in pairs:
        fails.append(f"interferencia {a} / {b}: {v:.2f} mm3")
    print("interferencias", len(pairs), f"{time.time() - t0:.0f}s", flush=True)

    # cable lane against the saddle bolts and the joint
    cable_top = c.z_rail + riel.EXIT_SLOT_ZC + P.CAT5E_D / 2
    bolt_gap = foot_frame(c)[3] - P.M4_CLEAR / 2 - cable_top
    if bolt_gap < 0.5:
        fails.append(f"los M4 del pie pasan a {bolt_gap:.1f} mm del Cat5e")

    # fused rail for SimScale (one solid)
    fused = half.fuse(put(half, -1)).clean()
    n_sol = len(fused.Solids())
    sim_path = OUT / "simscale" / "M3s_riel_fusionado.step"
    cq.exporters.export(cq.Workplane().add(fused), str(sim_path))
    fix_step_stamp(sim_path)
    if n_sol != 1:
        fails.append(f"riel fusionado: {n_sol} solidos")

    # masses and buoyancy (trays 40 % and 100 %)
    th = math.radians(P.SIMPLE_CAP_TILT)
    cav = CP.capsule_cavity().val()
    air = cav.Volume() - cav.intersect(cp["M4"].val()).Volume()
    plate_g = camara.plate_mass_g()
    lo, hi = (t * 1000 for t in P.BALLAST_TARGET_KGF)
    bal = {}
    for f in P.INFILL_CASES:
        parts_g = {"caja (M1 + M2 + bandeja + electronica)": FA.solid_g(an["m1"]) + FA.solid_g(an["m2"])
                   + sum(FA.mass_g(t, f) for t in an["trays"].values()) + an["fixed_g"],
                   "riel (2 M3s al 100 %)": 2 * FA.solid_g(half),
                   "tapas del bolsillo (2 M3t)": 2 * FA.solid_g(cover),
                   "ganchos (2 M9s al 40 %)": 2 * FA.mass_g(hk, 0.4),
                   "capsulas (M4 + M5s al 100 %, M6 al 40 %, M7, contenido)": 2 * (
                       FA.solid_g(cp["M4"].val()) + FA.solid_g(m5s) + FA.mass_g(cp["M6"].val(), 0.4)
                       + P.ACRYLIC_DENSITY * cp["M7"].val().Volume() / 1000 + P.CAPSULE_CONTENT_G),
                   "tornilleria y correas": P.SIMPLE_HARDWARE_G}
        disp = (an["v_disp"] + 2 * half.Volume() / 1000 + 2 * cover.Volume() / 1000 + 2 * hk.Volume() / 1000
                + 2 * (cp["M4"].val().Volume() + m5s.Volume() + cp["M6"].val().Volume() + cp["M7"].val().Volume() + air) / 1000
                + P.SIMPLE_HARDWARE_G / P.STEEL_DENSITY)
        node_g = sum(parts_g.values())
        app0 = node_g - RHO_W * disp
        k_need = next((n for n in range(0, 20) if app0 + n * 2 * plate_g * NET_STEEL >= lo), None)
        app = app0 + k * 2 * plate_g * NET_STEEL
        bal[f] = dict(parts=parts_g, node_g=node_g, disp=disp, app0=app0, k_need=k_need,
                      k_max=max((n for n in range(0, 20) if app0 + n * 2 * plate_g * NET_STEEL <= hi), default=None),
                      app=app, total=node_g + k * 2 * plate_g, in_window=lo <= app <= hi)
        if not bal[f]["in_window"]:
            fails.append(f"peso aparente {app:+.0f} g con {k} pletinas por bolsillo y bandeja al {f * 100:.0f} %: "
                         f"hacen falta {k_need}")
        if bal[f]["total"] > P.AIR_MASS_MAX_KG * 1000:
            fails.append(f"peso en aire {bal[f]['total']:.0f} g > {P.AIR_MASS_MAX_KG:g} kg")

    # stability: centres of mass and buoyancy of the whole node (trays 40 %)
    f = P.INFILL_CASES[0]
    m_pts = [(an["m1"].Center().z, FA.solid_g(an["m1"])), (an["m2"].Center().z, FA.solid_g(an["m2"]))]
    m_pts += [(t.Center().z, FA.mass_g(t, f)) for t in an["trays"].values()]
    m_pts.append((P.BOX_FLOOR + lay.cav[2] / 2, an["fixed_g"]))
    m_pts += [(half.Center().z, 2 * FA.solid_g(half)), (cover.Center().z, 2 * FA.solid_g(cover)),
              (node["M9s gancho +X"][0].Center().z, 2 * FA.mass_g(hk, 0.4)),
              (node["M4 capsula +X"][0].Center().z, 2 * (FA.solid_g(cp["M4"].val()) + P.CAPSULE_CONTENT_G)),
              (m5s.Center().z, 2 * FA.solid_g(m5s)), (c.z_rail + S / 2, P.SIMPLE_HARDWARE_G)]
    m_pts += [(p.Center().z, plate_g) for p in plates]
    air_w = place_cap(cav.cut(cp["M4"].val()), ax, az)
    b_pts = [(an["filled"].Center().z, an["filled"].Volume()), (an["m2"].Center().z, an["m2"].Volume()),
             (half.Center().z, 2 * half.Volume()), (cover.Center().z, 2 * cover.Volume()),
             (node["M9s gancho +X"][0].Center().z, 2 * hk.Volume()),
             (node["M4 capsula +X"][0].Center().z, 2 * cp["M4"].val().Volume()), (m5s.Center().z, 2 * m5s.Volume()),
             (air_w.Center().z, 2 * air_w.Volume())] + [(p.Center().z, p.Volume()) for p in plates]
    zg = sum(z * m for z, m in m_pts) / sum(m for _, m in m_pts)
    zb = sum(z * v for z, v in b_pts) / sum(v for _, v in b_pts)
    if zg >= zb:
        fails.append(f"centro de masa sobre el de empuje (G {zg:.1f}, B {zb:.1f})")

    # test lantern, separator LR1 and clearances
    node_solids = [v[0] for v in node.values()]
    node_pts = E.surface_points(node_solids, 0.7)
    z_top_node = float(node_pts[:, 2].max())
    h_sep_min = min_separator_h(node_pts, z_rod)
    z_sep = z_rod + P.SEP_H
    z_apex = z_sep + P.APEX_H
    sep = solid(separator(z_sep))
    lant, axes, buoy_end = lantern(z_rod, z_sep, z_apex)
    gland = (lay.lid_gland[0], lay.lid_gland[1], lay.box_outer()[2] + P.BOX_LID_T) if lay.lid_gland else lay.wall_gland
    umb = umbilical(gland, buoy_end)
    airs = min_air(node_solids, {kk: (p, q, P.LANTERN_CORD_D / 2) for kk, (p, q) in axes.items()},
                   {"LR1 separador": sep})
    worst = min(airs.values())
    if worst < P.CORD_CLEAR:
        fails.append(f"aire minimo entre la suspension y el nodo {worst:.1f} mm < {P.CORD_CLEAR:g}")
    if P.SEP_H < h_sep_min:
        fails.append(f"separador.altura {P.SEP_H:g} < minimo {h_sep_min:.0f}")
    ring_hits = {kk: E.common(v[0], lant["aro"]) for kk, v in node.items() if E.bb_hit(bbs[kk], E.bbox(lant["aro"]))}
    ring_hits = {kk: v for kk, v in ring_hits.items() if not (v <= P.INTERF_TOL)}
    net_hits = {kk: E.common(v[0], lant["red"]) for kk, v in node.items() if E.bb_hit(bbs[kk], E.bbox(lant["red"]))}
    net_hits = {kk: v for kk, v in net_hits.items() if not (v <= P.INTERF_TOL)}
    for kk, v in {**ring_hits, **{f"red/{a}": b for a, b in net_hits.items()}}.items():
        fails.append(f"linterna contra el nodo: {kk} {v:.2f} mm3")
    print("linterna", airs, "sep min", round(h_sep_min, 1), f"{time.time() - t0:.0f}s", flush=True)

    # LR1 as a printable reference piece (flat on the bed)
    lr = process("LR1 separador", solid(separator(P.SEP_SECTION[1] / 2)), "LR1_separador", LR_OUT, LR_OUT, thick=False)
    if not (lr["chk"]["ok"] and lr["mc"]["fits_bed"]):
        fails.append(f"LR1_separador: brep={lr['chk']['ok']} cama={lr['mc']['fits_bed']}")

    # assembly STEP and renders
    asm = [v[0] for v in node.values()] + list(lant.values()) + [sep] + umb
    asm_path = OUT / f"ensamble_simple_D{P.SIMPLE_RING_D:g}.step"
    E.comp(asm).exportStep(str(asm_path))
    fix_step_stamp(asm_path)
    from render import render
    col = {"caja": ("#5b8fb9", 0.55), "riel": ("#3a9d7a", 1.0), "lastre": ("#777777", 1.0)}
    node_items = []
    for kk, (sh, g) in node.items():
        cc, op = col.get(g, ("#c9a227", 1.0) if g.startswith("gancho") else ("#3a7ca5", 1.0))
        node_items.append((sh, cc, op, True, None))
    items = list(node_items)
    for kk, sh in lant.items():
        cc = "#c0504d" if kk.startswith(("cuerda", "cabo")) else "#8a8a8a" if kk in ("aro",) else "#b9d6e8"
        items.append((sh, cc, 0.25 if kk.startswith(("red", "piso")) else 0.9, False, None))
    items += [(sep, "#e07b39", 1.0, True, None)] + [(u, "#222222", 1.0, False, None) for u in umb]
    title = (f"Version simple Ø{P.SIMPLE_RING_D:g}: riel {P.SIMPLE_RAIL_L:g}, capsulas a {P.SIMPLE_CAP_TILT:g} grados, "
             f"separador {P.SEP_TYPE} a {P.SEP_H:g}, apice +{P.APEX_H:g}")
    render(items, OUT / "ensamble_simple_iso.png", "iso", title)
    render(items, OUT / "ensamble_simple_lado.png", "frontal", title)
    render(node_items, OUT / "nodo_simple_iso.png", "iso", "Nodo simple (sin la linterna)")

    # hand calculations and cable
    x_load = node["M4 capsula +X"][0].Center().x
    x_front = node["M4 capsula +X"][0].BoundingBox().xmax
    calc = hand_calcs(c, half, x_load, x_front, layers)
    cab = cable_run(c, lay, ax, az)
    secs = time.time() - t0
    write_report(rows, lr, bal, k, plate_g, zg, zb, airs, h_sep_min, z_rod, z_sep, z_apex, z_top_node, pairs,
                 slivers, ring_hits, net_hits, calc, cab, n_sol, bolt_gap, fails, c, layers, secs)
    print(f"peso aparente {bal[0.4]['app']:+.0f} g, total {bal[0.4]['total']:.0f} g, apice {z_apex - z_rod:.0f} mm sobre el aro, "
          f"aire min {worst:.1f} mm, {secs:.0f}s")
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


def cable_run(c, lay, ax, az):
    """Cat5e per camera: box slack + gland + chamber bend + conduit to the exit slot + loop to the capsule PG7 + rest."""
    _, out_h, _, _, _, x0, _ = CP.cap_dims()
    gx, gz = x0 + P.CAP_GLAND_X, -out_h / 2
    th = math.radians(P.SIMPLE_CAP_TILT)
    g = (ax + gx * math.cos(th) + gz * math.sin(th), 0.0, az - gx * math.sin(th) + gz * math.cos(th))
    h, ln, dist = P.RAIL_EXIT_SLOT
    ex = (XT - dist - ln / 2, S / 2, c.z_rail + riel.EXIT_SLOT_ZC)
    glx = max(abs(x) for x, _ in lay.floor_glands)
    rail = math.pi / 2 * c.bend_r + (ex[0] - glx - c.bend_r)
    a = P.CABLE_ALLOW
    loop = max(a["bucle"], math.dist(ex, g))
    total = a["caja"] + a["prensaestopas"] + rail + loop + a["capsula"] + a["holgura"]
    return dict(rail=rail, loop=loop, total=total, spi=total > P.SPI_TEST_LIMIT)


def write_report(rows, lr, bal, k, plate_g, zg, zb, airs, h_sep_min, z_rod, z_sep, z_apex, z_top_node, pairs,
                 slivers, ring_hits, net_hits, calc, cab, n_sol, bolt_gap, fails, c, layers, secs):
    qty = {"M3s_riel_mitad": 2, "M9s_gancho": 2, "M5s_capsula_tapa_pie": 2, "M3t_tapa_bolsillo": 2, "M1_caja_cuerpo": 1,
           "M2_caja_tapa": 1, "M4_capsula_cuerpo": 2, "M6_capsula_bisel": 2, "M7_capsula_ventana": 2}
    b4, b1 = bal[0.4], bal[1.0]
    L = ["# Version simple del nodo, aro Ø{:g} (generado por `simple.py`)".format(P.SIMPLE_RING_D), "",
         "No editar a mano: se regenera con `python cad_final/build.py --rapido` cuando `version = \"simple\"` en "
         "`params.py`. La version modular (`version = \"modular\"`) no cambia. mm, g, N, MPa.", "",
         f"Riel de una pieza de {P.SIMPLE_RAIL_L:g} en 2 mitades iguales M3s (union plana en x = 0 bajo la caja, 4 M3 en "
         f"orejas), sin varilla M8, extensiones ni puntas. Ganchos en C fijos M9s a x = ±{R_RING:g} con ranura para correa "
         f"de {P.STRAP_W:g}, sin casquillo, pestillo ni perilla. Capsulas fijas a {P.SIMPLE_CAP_TILT:g} grados: la tapa M5s "
         "trae un pie en silla que se atornilla con 2 M4 horizontales que cruzan el riel (sin bisagra dentada). Caja, tapa, "
         "bandeja, capsula, bisel y ventana iguales a la modular. Los cables van por dentro del riel y salen por la "
         "ranura lateral junto a la capsula.", "",
         "## 1. Piezas", "",
         "| Pieza | Archivo (`salida/simple/stl`, `step`) | Cant. | BRep/BOP | Estanco | Cuerpos | Bbox en la orientacion (mm) | Voladizo mm² | Espesor p1 | Masa al 100 % g |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        mc = r["mc"]
        q = qty.get(r["stem"], 1)
        m = (P.ACRYLIC_DENSITY if r["stem"].startswith("M7") else P.PETG_DENSITY) * r["shape"].Volume() / 1000
        p1 = "" if r["p1"] != r["p1"] else f"{r['p1']:.2f}"
        L.append(f"| {r['name']} | {r['stem']} | {q} | {'ok' if r['chk']['ok'] else 'FALLA'} | {'si' if mc['watertight'] else 'NO'} | "
                 f"{mc['bodies']} | {' x '.join(f'{v:.1f}' for v in mc['bbox'])} ({r['orient']}) | {mc['overhang_mm2']:.0f} | {p1} | {m:.0f} |")
    L += ["", f"Tipos impresos: 9 (M1, M2, M11, M3s, M3t, M9s, M4, M5s, M6) mas la ventana M7 de acrilico. Piezas impresas "
          "por nodo: 15. El espesor p1 se mide en las piezas nuevas; las demas son las de la modular, ya medidas.",
          f"STEP del riel como un solo solido para SimScale: `salida/simple/simscale/M3s_riel_fusionado.step` ({n_sol} solido).", "",
          "## 2. Peso y peso aparente", "",
          f"Pletinas de inox {P.PLATE_BAR[0]:g} × {P.PLATE_BAR[1]:g} × {P.PLATE_L:g} ({plate_g:.0f} g, hunde {plate_g * NET_STEEL:.0f} g cada una), "
          f"{k} por bolsillo (`lastre.pletinas`), 2 bolsillos. Ventana: {P.BALLAST_TARGET_KGF[0] * 1000:.0f} a "
          f"{P.BALLAST_TARGET_KGF[1] * 1000:.0f} g hacia abajo; en aire ≤ {P.AIR_MASS_MAX_KG:g} kg. Desplazamiento con los "
          "volumenes reales de los solidos (las piezas con relleno parcial cuentan su volumen entero: la piel cierra el aire) "
          "y el aire sellado de la caja y de las capsulas.", "",
          "| Concepto | Bandeja 40 % | Bandeja 100 % |", "|---|---|---|"]
    for kk in b4["parts"]:
        L.append(f"| {kk} | {b4['parts'][kk]:.0f} | {b1['parts'][kk]:.0f} |")
    L += [f"| Nodo sin pletinas g | {b4['node_g']:.0f} | {b1['node_g']:.0f} |",
          f"| Desplaza cm³ | {b4['disp']:.0f} | {b1['disp']:.0f} |",
          f"| Peso aparente sin pletinas g | {b4['app0']:+.0f} | {b1['app0']:+.0f} |",
          f"| Pletinas por bolsillo para entrar en la ventana | {b4['k_need']} a {b4['k_max']} | {b1['k_need']} a {b1['k_max']} |",
          f"| **Peso aparente con {k} por bolsillo g** | **{b4['app']:+.0f}** | **{b1['app']:+.0f}** |",
          f"| **Peso en aire g** | **{b4['total']:.0f}** | **{b1['total']:.0f}** |", "",
          f"Estabilidad (bandeja al 40 %, capsulas a {P.SIMPLE_CAP_TILT:g} grados): centro de masa z = {zg:.1f}, centro de empuje "
          f"z = {zb:.1f}, BG = **{zb - zg:.1f} mm** ({'no se voltea' if zg < zb else 'SE VOLTEA'}).", "",
          "## 3. Linterna de prueba y suspension", "",
          f"La linterna cuelga de su propia brida: 4 cuerdas a {', '.join(f'{a:g}' for a in P.SIMPLE_CORD_AZ)} grados suben "
          f"verticales del aro al separador LR1 ({P.SEP_TYPE}, {P.SEP_SECTION[0]:g} × {P.SEP_SECTION[1]:g}) y de ahi al apice; del "
          f"apice sube el cabo central al punto fijo (`linterna.punto_fijo` = {P.LANTERN_FIXED_POINT}). El nodo no carga la "
          "linterna: va enganchado al aro con los ganchos y la correa; el ojal del asa queda solo para izarlo. El umbilical "
          f"baja de la boya al PG7 de la tapa con {P.UMB_SAG:g} mm de comba (sin tension).", "",
          "| Concepto | Valor |", "|---|---|",
          f"| Techo del nodo sobre el centro de la varilla del aro | {z_top_node - z_rod:.0f} mm |",
          f"| Separador (plano medio) sobre el aro, `separador.altura` | {P.SEP_H:g} mm (minimo calculado con 10 mm de aire: **{h_sep_min:.0f} mm**) |",
          f"| Apice sobre el separador, `apice.altura` | {P.APEX_H:g} mm |",
          f"| **Apice sobre el aro** | **{z_apex - z_rod:.0f} mm** |",
          f"| Aire minimo suspension-nodo (exigido {P.CORD_CLEAR:g}) | **{min(airs.values()):.1f} mm** |"]
    for kk, v in sorted(airs.items(), key=lambda x: x[1]):
        L.append(f"| aire {kk} | {v:.1f} mm |")
    L += [f"| Aro contra el nodo (ganchos con holgura {P.SIMPLE_HOOK_C[0]:g}) | {'sin contacto' if not ring_hits else ring_hits} |",
          f"| Red contra el nodo | {'sin contacto' if not net_hits else net_hits} |", "",
          f"LR1 (`salida/linterna_prueba/LR1_separador.stl` y `.step`): pieza de referencia de la linterna, no del nodo; "
          f"se imprime plana en PETG si hace falta. Bbox {' x '.join(f'{v:.1f}' for v in lr['mc']['bbox'])} "
          f"({lr['orient']}), cabe en la cama: {'si' if lr['mc']['fits_bed'] else 'NO'}. Con `separador.tipo` = cruceta "
          "son rayos al centro y la altura minima sube (pasa sobre el asa).", "",
          "## 4. Interferencias del nodo", "",
          ("Ninguna (umbral {:g} mm³; las caras en contacto dan 0).".format(P.INTERF_TOL) if not pairs else
           "\n".join(f"- {a} / {b}: {v:.2f} mm³" for a, b, v in pairs)),
          ("Solapes de modelado de 0.01 mm, no son choques (las tapas del bolsillo entran 0.01 en la pared para unirse, "
           "igual que en la modular): " + "; ".join(f"{a} / {b} {v:.1f} mm³" for a, b, v in slivers) + ".") if slivers else "",
          f"Los M4 del pie cruzan el conducto {bolt_gap:.1f} mm por encima del Cat5e.", "",
          "## 5. Verificacion a mano (150 N de manipulacion en una capsula)", ""]
    rr, un, gh, pie = calc["riel"], calc["union"], calc["gancho"], calc["pie"]
    L += [f"- **Riel apoyado en los ganchos (en el agua, caso normal):** voladizo desde el gancho, M = F·(x_capsula − {R_RING:g}) = "
          f"{rr['M']:.0f} N·mm. Seccion del tubo en x = {rr['x_sec']:.0f} (corte del CAD): A = {rr['A']:.0f} mm², I = {rr['I']:.0f} mm⁴, "
          f"c = {rr['c']:.1f}. σ = {rr['sigma']:.1f} MPa → FS {rr['fs']:.1f} (45, flexion a lo largo de las capas) / {rr['fs_z']:.1f} (22). "
          f"Flecha de la capsula ≈ {rr['flecha']:.1f} mm.",
          f"- **Union plana sin contar la caja:** el gancho del otro lado tira hacia abajo (correa) y en x = 0 queda "
          f"M = {un['M']:.0f} N·mm con traccion arriba. Brazo de los M3 al fondo del riel {un['lever']:.1f}: T = {un['T']:.0f} N, "
          f"{un['por_m3']:.0f} N por M3 → {un['sigma_m3']:.0f} MPa en el acero (A2-70 del orden de 450) y {un['aplast']:.1f} MPa bajo la "
          "tuerca en el PETG. La caja, atornillada a las dos mitades con 4 M4, hace de puente: en la realidad la union carga menos.",
          f"- **Izado por el asa fuera del agua (150 N en una capsula):** traccion por inserto M4 del fondo de la caja "
          f"**{calc['insertos']:.0f} N** (la modular pedia 251 en Ø200): se prueba con PB8.",
          f"- **Gancho M9s con {P.HOOK_LOAD_N:g} N:** C como viga curva, M = F·r/2 = {gh['M']:.0f} N·mm sobre {P.SIMPLE_HOOK_C[2]:g} × "
          f"{P.SIMPLE_HOOK_C[1]:g}: σ = {gh['sigma']:.1f} MPa → FS {gh['fs']:.1f} (se imprime de costado, carga en el plano de las capas). "
          f"Tuerca M4 contra los labios de la ranura T: {gh['labios']:.1f} MPa. La correa solo toma el levantamiento.",
          f"- **Pie de la capsula:** M = {pie['M']:.0f} N·mm desde el frente de la capsula al centro de la silla; con 2 M4 a "
          f"{P.SIMPLE_FOOT_BOLTS[0]:g} la mayor fuerza por perno es {pie['por_m4']:.0f} N y aplasta las 2 paredes del riel "
          f"(Ø{P.M4_CLEAR:g} × {W:g}) a {pie['aplast']:.1f} MPa → FS {pie['fs']:.1f} (45) / **{pie['fs_z']:.1f}** (22: el riel se imprime "
          "con la brida abajo y la carga del perno va a traves de las capas). El alma del pie no se calculo: conviene "
          "llevar M5s a SimScale o probarla con la mano antes del agua.", "",
          "## 6. Cable", "",
          f"Por camara: {P.CABLE_ALLOW['caja']:g} + {P.CABLE_ALLOW['prensaestopas']:g} + riel {cab['rail']:.0f} + bucle {cab['loop']:.0f} + "
          f"{P.CABLE_ALLOW['capsula']:g} + {P.CABLE_ALLOW['holgura']:g} = **{cab['total']:.0f} mm** "
          f"({'requiere prueba SPI a 8 y 4 MHz' if cab['spi'] else 'no pasa de ' + format(P.SPI_TEST_LIMIT, 'g') + ': alcanza el cable de fabrica'}).", "",
          "## 7. Chequeos que fallaron", ""] + ([f"- {x}" for x in fails] if fails else ["- ninguno"])
    L += ["", "## 8. Constantes de modulo", "",
          f"- `SLOT_MARGIN` = {SLOT_MARGIN:g}: aire en x entre la silla del pie y la ranura de salida del cable.",
          f"- Tiempo de `simple.py`: {secs:.0f} s."]
    (HERE / "reporte_simple.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
