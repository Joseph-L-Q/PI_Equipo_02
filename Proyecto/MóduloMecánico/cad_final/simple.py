"""Simple version of the node for the real prototype (ring Ø200), behind params.VERSION = "simple".

Version V2 (29/10, team decisions): low box. The ESP32-S3 sits on KIT A (simple.esp32_base, 2 floors); the PG7 of each
camera goes through an END wall of M1 at the height of the rail conduit and its dome enters the conduit, so there is no
cable chamber under the box. Each rail half M3s bolts with a flange to a pad on the end wall (4 M4 inserts) and carries
its C hook (fused, gancho.correa) and the saddle of the capsule foot. The ballast pockets are moulded under the floor of
M1, outside the seal, closed by M3t. The capsules look inward and down to the net (capsula.acimut, capsula.angulo).
Box M2, tray M11, capsule M4, bezel M6 and window M7 are the modular ones (the tray gets two notches for the PG7 nuts).
Test lantern (tanda 3, 30/10 night): ring, net, 4 cords that go straight up from the ring (45 deg to the rail) past the lid and
on to ONE tie point, a line (cabo) from there to the long line, slack umbilical. No separator LR1 and no apex (params
separador.usar = False; the LR1 code is kept). The ballast is bulk (M8 nuts and washers or shot), ONE pocket per side.
The assembly STEP is a named assembly: printed parts by code and stem, the rest REF_*, ballast "lastre_izq"/"lastre_der".

    python simple.py        (from cad_final/; build.py runs it when version = "simple")
Outputs: salida/simple/ (stl/, step/, simscale/, ensamble_simple_D200.step, renders, resultados.json),
salida/linterna_prueba/ (LR1_separador) and cad_final/reporte_simple.md.
Prototypes (bloque B): params.version = P1_minimo | P2_robusto | P3_monocasco | P4_estetico (or env LG_VERSION) switch
flags (params.PROTO_CFG) in this same code: truss rail, snap/clamp hooks, monocoque box + rail, fillets and logo; outputs go
to salida/prototipos/<version>/ and reporte goes there too.
Frame: the box frame (outer bottom of the box body z = 0), X along the rail; the -X half is the +X one turned 180 deg
about Z.
"""
import json
import math
import time
from itertools import combinations
from pathlib import Path

import cadquery as cq
import numpy as np
from OCP.BRepCheck import BRepCheck_Analyzer

import params as P
import camara
camara.RAIL_ROD_M8 = False      # no M8 rod here; set before importing riel, which reads camara.lanes() on import
import riel  # noqa: E402
riel.RAIL_ROD_M8 = False
import caja_central as CC  # noqa: E402
import capsula as CP  # noqa: E402
import ensambles as E  # noqa: E402
import fase_a as FA  # noqa: E402
import layout  # noqa: E402
from checks import brep_check, export_part, fix_step_stamp, mesh_checks, min_thickness, sanitize  # noqa: E402

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
OUT = MOD / "salida" / P.SALIDA_REL
LR_OUT = MOD / "salida" / "linterna_prueba" if P.VERSION == "simple" else OUT / "lr1"
CFG = P.CFG                                     # per-version flags (params.PROTO_CFG): the prototypes P1..P4 are the same code
MONO, TRUSS_ON, ESTET = CFG["monocasco"], CFG["riel"] == "celosia", CFG["estetico"]
HOOK_STYLE = CFG["gancho"]
X_CUT = P.MONO_CUT
Z0, YAX, ZAX = cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), cq.Vector(0, 0, 1)

S, W = P.RAIL_SECTION, CFG["pared"]
XT = P.SIMPLE_RAIL_L / 2
LAY_OUTER = (0.0, 0.0, 0.0)  # box outer size, set by set_pad
X_PAD = 0.0                   # x of the rail flange / pad face; set by set_pad(lay) from the layout
R_RING = P.SIMPLE_RING_D / 2
Z_G = P.BOX_FLOOR + P.nut_corner_r() + 1.0      # PG7 axis in the end walls: the inner nut clears the floor by 1 mm
Z_RAIL = Z_G - S / 2                             # rail bottom: the conduit is centred on the PG7
CABLE_Z = Z_RAIL + W + P.CAT5E_D / 2             # the Cat5e lies on the conduit floor
PAD_BORE = 30.0           # socket access to the PG7 body through the pad (constants listed in the report)
POCKET_END = 8.0          # end walls of the ballast pockets, they hold the vertical M3 inserts of M3t
TIP_HOLE = 8.0            # cable hole in the end wall at the tip of the rail
HOOK_CLR = 10.0           # x gap between the hook web and the innermost point of the capsule
NET_STEEL = FA.NET_STEEL
RHO_W = P.SEAWATER_DENSITY
SUPPORT_MM2 = 300.0       # overhang area above which the piece is printed with supports (bitacora)
INFILL = {"M1": 1.0, "M2": 1.0, "M4": 1.0, "M5s": 1.0, "M3t": 1.0, "M11": 0.4, "M6": 0.4, "riel": 0.4, "gancho": 1.0,
          "LR1": 0.4}   # bitacora J: sealed boxes, sealed lids and hooks 100 %, rail, saddle/foot zones and tray 40 %
EXTRA = {}
QTY = {}
SEALS = dict(tapa_caja=1, tapa_capsula=2, ventana=2, pg7_caja=2, pg7_capsula=2)   # gasketed or glanded watertight joints
K_M1 = "M1m_caja_riel" if MONO else "M1s_caja_cuerpo"
K_RAIL = "M3s_riel_gancho"
K_M5 = "M5m_extremo_pie" if MONO else "M5s_capsula_tapa_pie"
REPORT = HERE / "reporte_simple.md" if P.VERSION == "simple" else OUT / "REPORTE.md"
_box = riel._box


def _cyl(p, d, r, h):
    return cq.Workplane().add(cq.Solid.makeCylinder(r, h, cq.Vector(*p), cq.Vector(*d)))


def solid(s):
    return s.val() if hasattr(s, "val") else s


def put(shape, side):
    """+X part -> the -X one is the same part turned 180 deg about Z."""
    s = solid(shape)
    return s.rotate(Z0, ZAX, 180) if side < 0 else s


FILLET_LOG = {}      # name -> radius applied (mm) or 0 when every attempt failed (P4); goes to resultados.json


def soften(name, shape, picker, r):
    """Fillet the edges chosen by picker(edge) with radius r, then 0.75 r and 0.5 r; the shape unchanged (FILLET_LOG 0) when
    a fillet fails on a boolean result (CadQuery/OCC often does)."""
    s = solid(shape)
    es = [e for e in s.Edges() if picker(e)]
    for rr in (r, 0.75 * r, 0.5 * r):
        try:
            out = s.fillet(rr, es)
            if es and out.isValid() and out.Volume() > 0.9 * s.Volume():
                FILLET_LOG[name] = rr
                return cq.Workplane().add(out)
        except Exception:                                  # noqa: BLE001 - OCC raises bare StdFail
            pass
    FILLET_LOG[name] = 0
    return cq.Workplane().add(s)


def axis_edges(axis, halfs, tol=0.6):
    """Picker: edges parallel to axis ('X'|'Z') whose two transverse coordinates are both +-h for some h in halfs."""
    def pick(e):
        a, b = e.startPoint(), e.endPoint()
        d = b - a
        if axis == "Z":
            return abs(d.x) < 1e-6 and abs(d.y) < 1e-6 and any(abs(abs(a.x) - h[0]) < tol and abs(abs(a.y) - h[1]) < tol for h in halfs)
        ok = abs(d.y) < 1e-6 and abs(d.z) < 1e-6
        return ok and any(abs(abs(a.y) - h[0]) < tol and abs(abs(a.z) - h[1]) < tol for h in halfs)
    return pick


def perimeter(ci, val, ext):
    """Picker: straight edges lying in the plane (coordinate ci = val) on the outline of a part, i.e. both ends at the same
    extreme |coordinate| (ext: coordinate index -> extreme). The rounded corners are tangent to them: OCC fillets the whole chain."""
    def pick(e):
        a, b = e.startPoint().toTuple(), e.endPoint().toTuple()
        if e.geomType() != "LINE" or abs(a[ci] - val) > 0.05 or abs(b[ci] - val) > 0.05:
            return False
        return any(abs(abs(a[i]) - v) < 0.1 and abs(abs(b[i]) - v) < 0.1 for i, v in ext.items())
    return pick


def pad_bolts():
    """(y, z) of the 4 M4 between the rail flange and the end-wall pad."""
    return [(sy * 20.0, Z_G + sz * 10.0) for sy in (1, -1) for sz in (1, -1)]


# ------------------------------------------------------------------ box M1 (low, pockets under the floor)
def pocket_dims(depth):
    lin, win = P.PLATE_L + 2 * P.PLATE_CLR, P.BALLAST_POCKET_W + 2 * P.PLATE_CLR
    w = P.PLATE_POCKET_WALL
    y_in0 = 1.0 + w                                   # 1 mm centre wall half + wall
    return dict(lin=lin, win=win, w=w, depth=depth, y0=y_in0, y1=y_in0 + win,
                x_out=lin / 2 + POCKET_END, x_ins=lin / 2 + POCKET_END / 2, yc=y_in0 + win / 2)


def box_body_low(lay, depth, bolts=True):
    import copy
    lay_b = copy.copy(lay)
    lay_b.floor_glands = []                            # the cables now leave through the end walls
    keep = CC.BASE_M4_PTS
    CC.BASE_M4_PTS = ()                                # no rail under the box: no blind M4 inserts in the floor
    try:
        m1 = CC.box_body(lay_b)
    finally:
        CC.BASE_M4_PTS = keep
    ol, ow, oh = lay.box_outer()
    pad_t, fl_t, hw = P.SIMPLE_GLAND_PAD
    for sg in (1, -1):
        xa, xb = sorted((sg * (ol / 2 - 1.0), sg * (ol / 2 + pad_t)))
        m1 = m1.union(_box(xa, xb, -hw, hw, 0.0, Z_G + PAD_BORE / 2 + 4.0))   # the bore must not touch the top face
        xo = sg * (ol / 2 + pad_t)
        m1 = m1.cut(_cyl((sg * ol / 2, 0, Z_G), (sg, 0, 0), PAD_BORE / 2, pad_t + 1))
        m1 = m1.cut(_cyl((sg * (ol / 2 - P.BOX_WALL - 1), 0, Z_G), (sg, 0, 0), P.PG7_HOLE / 2, P.BOX_WALL + 2))
        for y, z in (pad_bolts() if bolts else []):
            m1 = m1.cut(_cyl((xo + sg * 0.01, y, z), (-sg, 0, 0), P.M4_INSERT_HOLE / 2, P.M4_INSERT_DEPTH))
    d = pocket_dims(depth)
    for sy in (1, -1):
        ya, yb = sorted((sy * 1.0, sy * (d["y1"] + d["w"])))
        outer = _box(-d["x_out"], d["x_out"], ya, yb, -d["depth"], 0.01)
        ia, ib = sorted((sy * d["y0"], sy * d["y1"]))
        m1 = m1.union(outer.cut(_box(-d["lin"] / 2, d["lin"] / 2, ia, ib, -d["depth"] - 1, 0.0)))
        for x in (-d["x_ins"], d["x_ins"]):
            m1 = m1.cut(_cyl((x, sy * d["yc"], -d["depth"] - 0.01), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.01))
    if ESTET:                                          # P4: round the vertical corners of the body and of the lid flange
        fl = P.BOX_FLANGE                              # the corners of the box are already rounded (R6): round the flange underside
        m1 = soften("M1 brida", m1, perimeter(2, oh - P.BOX_FLANGE_T, {0: ol / 2 + fl, 1: ow / 2 + fl}), P.FILLETS["caja"])
    return m1


def pocket_cover(depth):
    """M3t (+Y pocket; the -Y one is the same part turned 180 deg about Z): plate with 2 countersunk M3."""
    d = pocket_dims(depth)
    w = d["w"]
    zc = -d["depth"] - w
    c = _box(-d["x_out"], d["x_out"], 1.0, d["y1"] + w, zc, -d["depth"])
    dk = P.M3_CSK_HEAD[0]
    for x in (-d["x_ins"], d["x_ins"]):
        cone = cq.Solid.makeCone(dk / 2 + 0.01, P.M3_CLEAR / 2, (dk - P.M3_CLEAR) / 2 + 0.01, cq.Vector(x, d["yc"], zc - 0.01), ZAX)
        c = c.cut(cq.Workplane().add(cone)).cut(_cyl((x, d["yc"], zc - 1), (0, 0, 1), P.M3_CLEAR / 2, w + 2))
    return c


def plates(depth, k):
    d = pocket_dims(depth)
    w, th = P.PLATE_BAR
    out = []
    for sy in (1, -1):
        for i in range(k):
            ya, yb = sorted((sy * (d["y0"] + P.PLATE_CLR), sy * (d["y0"] + P.PLATE_CLR + w)))
            z0 = -d["depth"] + i * th                     # stacked up from the cover
            out.append(solid(_box(-P.PLATE_L / 2, P.PLATE_L / 2, ya, yb, z0, z0 + th)))
    return out


def ballast_solids(depth, g_side, rho):
    """The bulk ballast as ONE solid per pocket (names lastre_izq = +Y pocket, lastre_der = -Y pocket): a block of the pocket
    plan (PLATE_CLR clear of the walls) piled on the cover up to the height g_side grams of apparent density rho fill."""
    d = pocket_dims(depth)
    c = P.PLATE_CLR
    wy = d["win"] - 2 * c
    h = min(g_side / rho * 1000.0 / (P.PLATE_L * wy), depth)
    out = {}
    for name, sy in (("lastre_izq", 1), ("lastre_der", -1)):
        ya, yb = sorted((sy * (d["y0"] + c), sy * (d["y0"] + c + wy)))
        out[name] = solid(_box(-P.PLATE_L / 2, P.PLATE_L / 2, ya, yb, -depth, -depth + h))
    return out


def gland_nuts(lay):
    """PG7 locknuts inside the end walls (hex along X), to check them against the trays and the modules."""
    ol = lay.box_outer()[0]
    af = P.PG7_NUT_AF
    out = []
    for sg in (1, -1):
        x0 = sg * (ol / 2 - P.BOX_WALL)
        nut = cq.Workplane("YZ").workplane(offset=min(x0, x0 - sg * P.PG7_INNER_H)).center(0, Z_G).polygon(
            6, af / math.cos(math.pi / 6)).extrude(P.PG7_INNER_H)
        out.append(solid(nut))
    return out


def trays_low(lay):
    """Trays of the layout with a notch at each end over the PG7 locknut (+2 mm around its corners)."""
    L = lay.cav[0]
    r = P.nut_corner_r() + 2.0
    out = {}
    for k, t in CC.trays(lay).items():
        for sg in (1, -1):
            xa, xb = sorted((sg * (L / 2 - P.PG7_INNER_H - 2.0), sg * (L / 2 + 1)))
            t = t.cut(_box(xa, xb, -r, r, -10, 200))
        out[k] = t
    return out


# ------------------------------------------------------------------ rail half M3s with its C hook
def hook(strap=None, holes=True, style=None):
    """C hook in its own frame: ring rod centre at the origin, rod along Y, rail bottom at z = HOOK_DROP. Open C seat
    (drops onto the rod), web with the strap slot along X. holes = M4 of the old bolted M9s (False when fused).
    strap = False (gancho.correa): no slot and a flared mouth, it lifts off the ring without undoing anything."""
    style = style or HOOK_STYLE
    strap = (P.SIMPLE_HOOK_STRAP and style == "c") if strap is None else strap
    clr, wall, seat = P.SIMPLE_HOOK_C
    ri = P.RING_SECTION / 2 + clr
    ro = ri + wall
    fl_l, fl_t = P.HOOK_FLANGE
    zt = P.HOOK_DROP
    wy = P.STRAP_W / 2 + P.JAW_WALL
    wx = P.SIMPLE_HOOK_WEB / 2
    fy = max(S / 2, wy)
    h = _box(-fl_l / 2, fl_l / 2, -fy, fy, zt - fl_t, zt)
    h = h.union(_box(-wx, wx, -wy, wy, ro - wall / 2, zt - fl_t + 0.01))
    h = h.union(_cyl((0, -seat / 2, 0), (0, 1, 0), ro, seat))
    h = h.cut(_cyl((0, -wy - 1, 0), (0, 1, 0), ri, 2 * wy + 2))
    h = h.cut(_box(-ri, ri, -wy - 1, wy + 1, -ro - 1, 0))
    if style == "snap":
        # flexure arms (ENGANCHES.md, 2): below z = raiz_z the wall beyond the arm is removed, so the two horns of the C
        # become cantilever arcs of thickness `brazo` rooted in the crown, each with an inward barb that narrows the mouth
        sn = P.SNAP
        arm_o = ri + sn["brazo"]
        ann = _cyl((0, -wy - 1, 0), (0, 1, 0), ro + 2, 2 * wy + 2).cut(_cyl((0, -wy - 2, 0), (0, 1, 0), arm_o, 2 * wy + 4))
        h = h.cut(ann.intersect(_box(-ro - 3, ro + 3, -wy - 2, wy + 2, -ro - 3, sn["raiz_z"])))
        bh = ri - sn["apertura"] / 2
        for sg in (1, -1):
            pts = [(sg * (ri + 0.3), -1.4), (sg * (ri - bh), -2.9), (sg * (ri - bh), -3.9), (sg * (ri + 0.3), -4.5)]
            h = h.union(cq.Workplane("XZ").workplane(offset=-seat / 2).polyline(pts).close().extrude(seat))
    elif style == "abrazadera":
        # half-moon clamp (ENGANCHES.md, 1): an ear on each side of the C at the split plane z = 0; the lower half M9c bolts to it
        eo, et = P.CLAMP["oreja"], P.CLAMP["oreja_t"]
        h = h.cut(_box(-ro - 3, ro + 3, -wy - 2, wy + 2, -ro - 3, 0))      # the lower half belongs to M9c
        for sg in (1, -1):
            xa, xb = sorted((sg * (ro - 2), sg * (ro + eo)))
            h = h.union(_box(xa, xb, -seat / 2, seat / 2, 0, et))
            xc = sg * (ro + eo / 2)
            h = h.cut(_cyl((xc, 0, -1), (0, 0, 1), P.M4_CLEAR / 2, et + 2))
            h = h.cut(cq.Workplane("XY").workplane(offset=et - P.M4_NUT[1] - 0.2).center(xc, 0).polygon(
                6, (P.M4_NUT[0] + 0.4) / math.cos(math.pi / 6)).extrude(P.M4_NUT[1] + 1))
    elif strap:
        zs = strap_z()
        h = h.cut(_box(-wx - 1, wx + 1, -P.STRAP_W / 2, P.STRAP_W / 2, zs - P.STRAP_SLOT_T / 2, zs + P.STRAP_SLOT_T / 2))
    else:
        flare = ri + 0.6 * wall
        h = h.cut(cq.Workplane("XZ").workplane(offset=-wy - 1).polyline(
            [(-ri, 0.01), (ri, 0.01), (flare, -ro - 1), (-flare, -ro - 1)]).close().extrude(2 * wy + 2))
    if holes:
        for x in (-P.SIMPLE_HOOK_BOLT_X, P.SIMPLE_HOOK_BOLT_X):
            h = h.cut(_cyl((x, 0, zt - fl_t - 1), (0, 0, 1), P.M4_CLEAR / 2, fl_t + 2))
    return h


def clamp_piece():
    """M9c in the hook frame (rod centre at the origin): lower half-moon of the C with an ear on each side that bolts to the
    ears of the hook (1 M4 each, nut in the hook ear). Printed with the ears flat."""
    clr, wall, seat = P.SIMPLE_HOOK_C
    ri = P.RING_SECTION / 2 + clr
    ro = ri + wall
    eo, et = P.CLAMP["oreja"], P.CLAMP["oreja_t"]
    c = _cyl((0, -seat / 2, 0), (0, 1, 0), ro, seat).intersect(_box(-ro - 1, ro + 1, -seat, seat, -ro - 1, 0))
    for sg in (1, -1):
        xa, xb = sorted((sg * (ro - 2), sg * (ro + eo)))
        c = c.union(_box(xa, xb, -seat / 2, seat / 2, -et, 0))
    c = c.cut(_cyl((0, -seat, 0), (0, 1, 0), ri, 2 * seat))
    for sg in (1, -1):
        c = c.cut(_cyl((sg * (ro + eo / 2), 0, -et - 1), (0, 0, 1), P.M4_CLEAR / 2, et + 2))
    return c


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


def x_flange(lay):
    return lay.box_outer()[0] / 2 + P.SIMPLE_GLAND_PAD[0]


def set_pad(lay):
    global X_PAD, LAY_OUTER
    X_PAD = x_flange(lay)
    LAY_OUTER = lay.box_outer()


TRUSS_N = {}


def truss_spans(kind, foot):
    """x ranges of the conduit side walls that may take the truss windows: clear of the flange, the saddle and the tip."""
    t = P.TRUSS
    fl_t = P.SIMPLE_GLAND_PAD[1]
    end = P.RAIL_TIP_END_T
    if kind == "half":
        out = [(X_PAD + fl_t + t["margen_brida"], foot["x0"] - t["margen_silla"]),
               (foot["x1"] + t["margen_silla"], XT - end - t["margen_punta"])]
    elif kind == "stub":
        out = [(X_PAD + t["margen_brida"], X_CUT - fl_t - t["margen_brida"])]
    else:
        out = [(X_CUT + fl_t + t["margen_brida"], foot["x0"] - t["margen_silla"]),
               (foot["x1"] + t["margen_silla"], XT - end - t["margen_punta"])]
    return [(a, b) for a, b in out if b - a > 20.0]


def truss_cut(shape, kind, foot):
    """Warren truss: equilateral triangular windows through both side walls of the conduit, between the floor and the top
    (which are left whole). Bars of TRUSS.barra between windows and to the chords."""
    bar = P.TRUSS["barra"]
    zb, zt = Z_RAIL + W, Z_RAIL + S - W
    h = zt - zb
    b = 2 * h / math.tan(math.radians(P.TRUSS["angulo"]))
    cut = None
    n = 0
    for xa, xb in truss_spans(kind, foot):
        j = 0
        while xa + b * j + b <= xb:
            x0 = xa + b * j
            tris = [[(x0, zb), (x0 + b, zb), (x0 + b / 2, zt)]]
            if x0 + 1.5 * b <= xb:
                tris.append([(x0 + b / 2, zt), (x0 + 1.5 * b, zt), (x0 + b, zb)])
            for t in tris:
                a, bb, c = (math.dist(t[1], t[2]), math.dist(t[0], t[2]), math.dist(t[0], t[1]))
                inc = [(a * t[0][k] + bb * t[1][k] + c * t[2][k]) / (a + bb + c) for k in (0, 1)]
                area = abs((t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) - (t[2][0] - t[0][0]) * (t[1][1] - t[0][1])) / 2
                r_in = 2 * area / (a + bb + c)
                if r_in <= bar / 2 + 1.0:
                    continue
                f = (r_in - bar / 2) / r_in
                pts = [(inc[0] + (p[0] - inc[0]) * f, inc[1] + (p[1] - inc[1]) * f) for p in t]
                w = cq.Workplane("XZ").workplane(offset=-S / 2 - 1).polyline(pts).close().extrude(S + 2)
                cut = w if cut is None else cut.union(w)
                n += 1
            j += 1
    TRUSS_N[kind] = n
    return shape.cut(cut) if cut is not None else shape


def hex_pocket(x0, y, z, depth):
    """M4 nut pocket opening on the plane x = x0 and going +X by depth (the YZ workplane normal is +X)."""
    return cq.Workplane("YZ").workplane(offset=x0).center(y, z).polygon(
        6, (P.M4_NUT[0] + 0.4) / math.cos(math.pi / 6)).extrude(depth)


def rail_piece(lay, foot, kind="half", strap=None, hook_on=True):
    """Rail piece of the +X side. kind 'half' (V2/P1/P2): flange to the end-wall pad (4 M4, bore for the PG7 dome), conduit to
    the tip, end wall with the cable hole, the 2 M4 of the saddle and the C hook fused at x = R_RING. 'stub' (P3): from the pad
    of the box to X_CUT (fused to M1m, no flange there) with the joint flange at X_CUT (nut pockets). 'end' (P3): the flange at
    X_CUT (through holes) and the conduit to the tip (the saddle is fused by end_piece). Truss windows and hook style per the
    version flags."""
    set_pad(lay)
    x_f = X_PAD
    fl_t, hw = P.SIMPLE_GLAND_PAD[1], P.SIMPLE_GLAND_PAD[2]
    z0, end = Z_RAIL, P.RAIL_TIP_END_T
    xa, xb = {"half": (x_f, XT), "stub": (x_f, X_CUT), "end": (X_CUT, XT)}[kind]
    fl = {"half": (x_f, x_f + fl_t), "stub": (X_CUT - fl_t, X_CUT), "end": (X_CUT, X_CUT + fl_t)}[kind]
    tube = _box(xa, xb, -S / 2, S / 2, z0, z0 + S)
    if ESTET:
        tube = soften("riel tubo", tube, lambda e: abs(e.endPoint().y - e.startPoint().y) < 1e-6
                      and abs(e.endPoint().z - e.startPoint().z) < 1e-6 and abs(e.endPoint().x - e.startPoint().x) > 1.0,
                      P.FILLETS["riel"])
    r = tube.union(_box(fl[0], fl[1], -hw, hw, z0, z0 + S))
    x_in = xb if kind == "stub" else xb - end
    r = r.cut(_box(xa - 1, x_in + (1 if kind == "stub" else 0), -S / 2 + W, S / 2 - W, z0 + W, z0 + S - W))
    if kind == "half":
        r = r.cut(_cyl((x_f - 1, 0, Z_G), (1, 0, 0), (P.PG7_DOME[0] + 2) / 2, fl_t + 2))
        for y, z in pad_bolts():
            r = r.cut(_cyl((x_f - 1, y, z), (1, 0, 0), P.M4_CLEAR / 2, fl_t + 2))
    elif kind == "stub":
        for y, z in pad_bolts():
            r = r.cut(_cyl((X_CUT - fl_t - 1, y, z), (1, 0, 0), P.M4_CLEAR / 2, fl_t + 2))
            r = r.cut(hex_pocket(X_CUT - P.M4_NUT[1] - 0.2, y, z, P.M4_NUT[1] + 1))
    else:
        for y, z in pad_bolts():
            r = r.cut(_cyl((X_CUT - 1, y, z), (1, 0, 0), P.M4_CLEAR / 2, fl_t + 2))
    if kind != "stub":
        r = r.cut(_cyl((XT - end - 1, 0, z0 + W + TIP_HOLE / 2), (1, 0, 0), TIP_HOLE / 2, end + 2))
    if kind == "half":
        for x in foot["bx"]:
            r = r.cut(_cyl((x, -S, foot["bz"]), (0, 1, 0), P.M4_CLEAR / 2, 2 * S))
    if TRUSS_ON:
        r = truss_cut(r, kind, foot)
    if hook_on and kind != "end":
        hk = hook(strap, holes=False).translate((R_RING, 0, Z_RAIL - P.HOOK_DROP))
        r = r.union(hk.intersect(_box(x_f, xb, -50, 50, -200, 200)))
    return r


def rail_half(lay, foot, strap=None, hook_on=True):
    return rail_piece(lay, foot, "half", strap, hook_on)


# ------------------------------------------------------------------ capsule with the fixed foot (M5s)
def cap_rot(shape):
    """Capsule frame -> tilted down by capsula.angulo and turned to capsula.acimut (adentro: front toward -X)."""
    s = solid(shape).rotate(Z0, YAX, P.SIMPLE_CAP_TILT)
    return s.rotate(Z0, ZAX, 180) if P.SIMPLE_CAP_AZ == "adentro" else s


def cap_pt(x, z):
    """A point of the capsule frame (x, 0, z) after cap_rot, as (x, z)."""
    th = math.radians(P.SIMPLE_CAP_TILT)
    xr, zr = x * math.cos(th) + z * math.sin(th), -x * math.sin(th) + z * math.cos(th)
    return (-xr, zr) if P.SIMPLE_CAP_AZ == "adentro" else (xr, zr)


def capsule_pose(lay, parts):
    """Capsule origin (ax, az) and the saddle {x0, x1, bx, bz}. adentro: the innermost point of the capsule HOOK_CLR
    past the hook web, its top SIMPLE_FOOT_GAP under the saddle; the saddle on the back normal of the lid, clamped to
    the rail between the hook flange and the tip. afuera (V1): the saddle before the old side exit, capsule outboard."""
    fl, ft, _ = P.SIMPLE_FOOT
    th = math.radians(P.SIMPLE_CAP_TILT)
    z_pb = Z_RAIL - ft
    bbs = [cap_rot(parts[k]).BoundingBox() for k in ("M4", "lid", "M6")]
    zmax, xmin, xmax = max(b.zmax for b in bbs), min(b.xmin for b in bbs), max(b.xmax for b in bbs)
    az = z_pb - P.SIMPLE_FOOT_GAP - zmax
    xl = CP.cap_dims()[4]
    lo = R_RING + P.HOOK_FLANGE[0] / 2 + 2.0 + fl / 2           # saddle centre range on the rail
    hi = XT - P.RAIL_TIP_END_T - fl / 2
    if P.SIMPLE_CAP_AZ == "adentro":
        ax = R_RING + P.SIMPLE_HOOK_WEB / 2 + HOOK_CLR - xmin
        cfx, cfz = ax + cap_pt(xl, 0)[0], az + cap_pt(xl, 0)[1]
        nx, nz = math.cos(th), math.sin(th)                     # back normal of the lid: outward and up
        xs = cfx + nx * (z_pb - cfz) / nz if nz > 1e-6 else hi
    else:
        xs = hi
        cfz = az + cap_pt(xl, 0)[1]
        off = (z_pb - cfz) / math.tan(th) if th > 1e-6 else 80.0
        ax = xs + min(max(off, fl / 2), 80.0) - cap_pt(xl, 0)[0]
    xs = min(max(xs, lo), hi)
    sp, zb = P.SIMPLE_FOOT_BOLTS
    return ax, az, dict(x0=xs - fl / 2, x1=xs + fl / 2, xs=xs, bx=(xs - sp / 2, xs + sp / 2), bz=Z_RAIL + zb, z_pb=z_pb)


def place_cap(shape, ax, az):
    return cap_rot(shape).translate(cq.Vector(ax, 0, az))


def lid_with_foot(lid, ax, az, foot):
    """M5s in the box frame (+X side): lid plate + web + saddle (plate under the rail, two cheeks, 2 M4 across)."""
    fl, ft, fc = P.SIMPLE_FOOT
    x0, x1, z_pb = foot["x0"], foot["x1"], foot["z_pb"]
    yo = S / 2 + P.FIT_CLEAR + fc
    saddle = _box(x0, x1, -yo, yo, z_pb, Z_RAIL)
    for sy in ([] if MONO else (1, -1)):
        ya, yb = sorted((sy * (S / 2 + P.FIT_CLEAR), sy * yo))
        saddle = saddle.union(_box(x0, x1, ya, yb, Z_RAIL - 0.01, Z_RAIL + S))
    xl = CP.cap_dims()[4]
    hw = CP.cap_dims()[3] / 2 - 4.0
    pts = [(x0, z_pb), (x1, z_pb)] + [(ax + cap_pt(xl + 1.0, z)[0], az + cap_pt(xl + 1.0, z)[1]) for z in (hw, -hw)]
    from scipy.spatial import ConvexHull
    hull = ConvexHull(np.array(pts))
    poly = [tuple(map(float, pts[i])) for i in hull.vertices]
    yw = P.SIMPLE_FOOT_WEB / 2
    web = cq.Workplane("XZ").workplane(offset=-yw).polyline(poly).close().extrude(2 * yw)
    m5 = saddle.union(web).union(cq.Workplane().add(place_cap(lid, ax, az)))
    for x in ([] if MONO else foot["bx"]):
        m5 = m5.cut(_cyl((x, -yo - 1, foot["bz"]), (0, 1, 0), P.M4_CLEAR / 2, 2 * yo + 2))
    return m5


def end_piece(lay, foot, lid, ax, az):
    """P3/P4 extension M5m: rail end from X_CUT to the tip + the saddle plate and web + the capsule lid, in one piece."""
    return rail_piece(lay, foot, "end").union(lid_with_foot(lid, ax, az, foot))


def central_mono(lay, depth, foot):
    """P3/P4 M1m: the low box (no insert holes in the pads) with both rail stubs (hooks fused) up to X_CUT, in one piece."""
    m = box_body_low(lay, depth, bolts=False)
    stub = rail_piece(lay, foot, "stub")
    return m.union(stub).union(put(stub, -1))


def capsule_parts():
    """Capsule modules in the capsule frame."""
    cp = {"M4": CP.capsule_body(), "M6": CP.bezel(), "M7": CP.window_disc(), "lid": CP.lid_plate()}
    # P4: the long outer corners of the capsule are already rounded in the base design (plane-cylinder-plane); a front or lid
    # perimeter fillet of 3 mm split the body into pieces at the bezel seat (tried 30/10), so the profile is left as is
    return cp


def lid_logo(m2):
    """P4: LOGO text raised on the top plate of the lid, beside the handle (y = -35)."""
    lg = P.LOGO
    try:
        zt = solid(m2).BoundingBox().zmin + P.BOX_LID_T
        txt = cq.Workplane("XY").workplane(offset=zt - 0.01).center(0, -35.0).text(
            lg["texto"], lg["alto"], lg["relieve"] + 0.01, combine=False, halign="center", valign="center")
        out = cq.Workplane().add(solid(m2)).union(txt)
        FILLET_LOG["logo"] = lg["relieve"]
        return out
    except Exception as e:                                   # noqa: BLE001 - font missing on the machine
        FILLET_LOG["logo"] = 0
        print("logo omitido:", e, flush=True)
        return m2


def lid_edges(m2):
    """P4: the lid outline takes the same corner radius as the flange of the box (continuous line)."""
    ol, ow, _ = LAY_OUTER
    fl = P.BOX_FLANGE
    zt = solid(m2).BoundingBox().zmin + P.BOX_LID_T
    return soften("M2 borde superior", m2, perimeter(2, zt, {0: ol / 2 + fl, 1: ow / 2 + fl}), P.FILLETS["caja"])


SIDE = {1: "der", -1: "izq"}      # rail halves, capsules, hooks: der = +X, izq = -X (top view, X to the right)


def assemble(an, half, m5s, cover, cp, ax, az, ballast, m1, trays, strap=False):
    """name -> (shape, group) of the whole node in the box frame. The names are the ones of the assembly STEP: printed parts by
    code and stem (pocket parts izq = +Y, der = -Y), bought bodies REF_*, ballast lastre_izq / lastre_der. strap=True adds the
    strap loops (render only)."""
    cap_w = {kk: place_cap(cp[kk], ax, az) for kk in ("M4", "M6", "M7")}
    node = {K_M1: (solid(m1), "caja"), "M2_caja_tapa": (solid(an["m2"]), "caja")}
    node.update({kk: (solid(t), "caja") for kk, t in trays.items()})
    node.update({"M3t_tapa_bolsillo_izq": (solid(cover), "lastre_t"), "M3t_tapa_bolsillo_der": (put(cover, -1), "lastre_t")})
    node.update({kk: (b, "lastre") for kk, b in ballast.items()})
    z_rod = Z_RAIL - P.HOOK_DROP
    for side in (1, -1):
        sg = SIDE[side]
        if not MONO:
            node[f"{K_RAIL}_{sg}"] = (put(half, side), "riel")
        if HOOK_STYLE == "abrazadera":
            node[f"M9c_abrazadera_{sg}"] = (put(solid(clamp_piece()).translate(cq.Vector(R_RING, 0, z_rod)), side), "abrazadera")
        if strap:
            node[f"REF_correa_{sg}"] = (put(solid(strap_band()).translate(cq.Vector(R_RING, 0, z_rod)), side), "correa")
        node[f"{K_M5}_{sg}"] = (put(m5s, side), "capsula" + ("+X" if side > 0 else "-X"))
        for kk, nm in (("M4", "M4_capsula_cuerpo"), ("M6", "M6_capsula_bisel"), ("M7", "REF_M7_capsula_ventana")):
            node[f"{nm}_{sg}"] = (put(cap_w[kk], side), "capsula" + ("+X" if side > 0 else "-X"))
    return node


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


def lantern(z_rod, z_sep, z_apex, fixed=None):
    """Ring, net with floors, vertical cords, upper cords, central line, fixed point (box frame).
    Returns (name -> shape, name -> axis (p, q), end of the umbilical at the buoy)."""
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
    fixed = fixed or P.LANTERN_FIXED_POINT
    if P.LANTERN_CENTRAL_LINE and fixed != "ninguno":
        axes["cabo central"] = ((0, 0, z_apex), (0, 0, z_top))
    for name, (p, q) in axes.items():
        out[name] = segment(p, q, P.LANTERN_CORD_D)
    if fixed == "boya":
        out["boya (punto fijo)"] = solid(_box(-105, 105, -70, 70, z_top, z_top + 76))
        buoy_end = (60.0, 0.0, z_top)
    elif fixed == "estructura":
        out["estructura (punto fijo)"] = solid(_box(-150, 150, -10, 10, z_top, z_top + 20))
        out["boya"] = solid(_box(-105, 105, 180, 320, z_top, z_top + 76))
        buoy_end = (0.0, 200.0, z_top)
    else:
        buoy_end = None
    return out, axes, buoy_end


def lantern_tie(z_rod, z_bend, z_tie, fixed=None):
    """Test lantern without separator (box frame): ring, net with floors, 4 cords straight up from the ring (tied round the rod, so
    the axis lies outside it) to z_bend and from there straight to ONE tie point, the cabo from the tie point to the long line.
    Names are the REF_* ones of the assembly STEP. Returns (name -> shape, name -> [(p, q), ...] axes, end of the umbilical)."""
    rd = P.RING_SECTION
    out = {"REF_aro_superior": cq.Solid.makeTorus(R_RING, rd / 2, cq.Vector(0, 0, z_rod), ZAX)}
    h = P.LANTERN_NET_H
    z_net = z_rod - rd / 2
    out["REF_linterna_malla"] = cq.Solid.makeCylinder(R_RING, h, cq.Vector(0, 0, z_net - h), ZAX).cut(
        cq.Solid.makeCylinder(R_RING - P.LANTERN_NET_T, h + 2, cq.Vector(0, 0, z_net - h - 1), ZAX))
    for k in range(P.LANTERN_FLOORS):
        z = z_net - h * (k + 1) / (P.LANTERN_FLOORS + 1)
        out[f"REF_linterna_piso_{k + 1}"] = cq.Solid.makeCylinder(R_RING - P.LANTERN_NET_T - 1, 1.0, cq.Vector(0, 0, z), ZAX)
    d = P.LANTERN_CORD_D
    r_c = R_RING + rd / 2 + d / 2
    axes = {}
    tie = (0.0, 0.0, z_tie)
    for i, a in enumerate(P.SIMPLE_CORD_AZ):
        x, y = r_c * math.cos(math.radians(a)), r_c * math.sin(math.radians(a))
        p0, p1 = (x, y, z_rod), (x, y, z_bend)
        axes[f"REF_cuerda_{i + 1}"] = [(p0, p1), (p1, tie)]
        c = cq.Workplane().add(segment(p0, p1, d)).union(cq.Workplane().add(
            cq.Solid.makeSphere(d / 2, cq.Vector(*p1), angleDegrees1=-90, angleDegrees2=90))).union(
            cq.Workplane().add(segment(p1, tie, d))).clean()
        out[f"REF_cuerda_{i + 1}"] = solid(c)
    z_top = z_tie + P.LANTERN_LINE_L
    fixed = fixed or P.LANTERN_FIXED_POINT
    if P.LANTERN_CENTRAL_LINE and fixed != "ninguno":
        axes["REF_cabo"] = [(tie, (0.0, 0.0, z_top))]
        out["REF_cabo"] = segment(tie, (0.0, 0.0, z_top), d)
    if fixed == "boya":
        out["REF_boya"] = solid(_box(-105, 105, -70, 70, z_top, z_top + 76))
        buoy_end = (60.0, 0.0, z_top)
    elif fixed == "estructura":
        out["REF_estructura_punto_fijo"] = solid(_box(-150, 150, -10, 10, z_top, z_top + 20))
        out["REF_boya"] = solid(_box(-105, 105, 180, 320, z_top, z_top + 76))
        buoy_end = (0.0, 200.0, z_top)
    else:
        buoy_end = None
    return out, axes, buoy_end


def umbilical(gland, buoy_end):
    """Slack umbilical: up from the gland, then a sagging curve to the buoy (render and STEP only). Returns [ONE solid]: the
    segments and the joint spheres fused, so the assembly has a single body REF_umbilical."""
    p0 = np.array(gland, float)
    p1 = p0 + np.array([0, 0, 40.0])
    p2 = np.array(buoy_end, float)
    pts = [p0]
    for t in np.linspace(0, 1, 13):
        pts.append(p1 + (p2 - p1) * t - np.array([0, 0, P.UMB_SAG * 4 * t * (1 - t)]))
    d = P.UMBILICAL[0]
    segs = [segment(tuple(a), tuple(b), d) for a, b in zip(pts, pts[1:]) if np.linalg.norm(b - a) > 1e-6]
    u = cq.Workplane().add(segs[0])
    for sg_, pt in zip(segs[1:], pts[1:]):
        u = u.union(cq.Workplane().add(sg_)).union(cq.Workplane().add(
            cq.Solid.makeSphere(d / 2, cq.Vector(*pt), angleDegrees1=-90, angleDegrees2=90)))
    return [solid(u.clean())]


def lid_gland_point(lay):
    if lay.lid_gland:
        return (lay.lid_gland[0], lay.lid_gland[1], lay.box_outer()[2] + P.BOX_LID_T)
    return lay.wall_gland


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
        near = np.abs(np.linalg.norm(xy, axis=1) - R_RING) <= w / 2 + P.CORD_CLEAR
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


def camera_view(ax, az, z_rod, ring_r):
    """Lens (front centre) and optical axis of the +X camera; distance along the axis to the net (cylinder of radius
    ring_r from the ring down LANTERN_NET_H) and the diagonal of the field there."""
    xf = CP.cap_dims()[6]
    lx, lz = ax + cap_pt(xf, 0)[0], az + cap_pt(xf, 0)[1]
    th = math.radians(P.SIMPLE_CAP_TILT)
    dx = -math.cos(th) if P.SIMPLE_CAP_AZ == "adentro" else math.cos(th)
    dz = -math.sin(th)
    z_top, z_bot = z_rod - P.RING_SECTION / 2, z_rod - P.RING_SECTION / 2 - P.LANTERN_NET_H
    hit = None
    for t in np.arange(0.5, 3000.0, 0.5):
        x, z = lx + dx * t, lz + dz * t
        if z < z_bot - 50:
            break
        crossed = (abs(lx) > ring_r) != (abs(x) > ring_r) if t > 0.5 else False
        if crossed or (abs(lx) <= ring_r and abs(x) >= ring_r):
            if z_bot <= z <= z_top:
                hit = t
                break
    diag = 2 * hit * math.tan(math.radians(P.CAM_FOV_DIAG / 2)) if hit else None
    lo, hi = P.CAM_FOCUS
    return dict(lens=(lx, lz), dist=hit, campo_diag=diag, en_foco=bool(hit and lo <= hit <= hi), D=2 * ring_r)


# ------------------------------------------------------------------ hand calculations
def hand_calcs(lay, rail, x_load, x_front, foot):
    F, D = P.HANDLING_LOAD_N, P.SIMPLE_RING_D
    out = {}
    x_f = X_CUT if MONO else x_flange(lay)             # the 4 M4 of the joint carry the moment: pad flange or the mid joint
    lever = abs(x_load - R_RING)
    xs = (R_RING + P.HOOK_FLANGE[0] / 2 + foot["x0"]) / 2 if foot["x0"] > R_RING + P.HOOK_FLANGE[0] / 2 + 2 else x_f + P.SIMPLE_GLAND_PAD[1] + 2
    A, I, cz = section_props(rail, xs)
    Mb = F * lever
    sb = Mb / (I / cz)
    out["riel"] = dict(x_sec=xs, A=A, I=I, c=cz, M=Mb, sigma=sb, fs=P.PETG_YIELD / sb, fs_z=P.PETG_YIELD_Z / sb,
                       flecha=F * lever ** 3 / (3 * P.PETG_E * I))
    # rail flange to the box pad: 4 M4 inserts at z = Z_G +-10; lifting by the handle with 150 N on one capsule
    zs = sorted({z for _, z in pad_bolts()})
    arm = zs[-1] - zs[0]
    Mi = F * abs(x_load - x_f)
    out["insertos"] = dict(M=Mi, por_inserto=Mi / arm / 2 + F / 4, arm=arm)
    # in the water on the hooks, the far hook pulls down: moment at the pad of the near side
    r_far = F * abs(x_load - R_RING) / D
    out["insertos_agua"] = r_far * (R_RING - x_f) / arm / 2 if R_RING > x_f else 0.0
    clr, wall, seat = P.SIMPLE_HOOK_C
    rm = P.RING_SECTION / 2 + clr + wall / 2
    Mh = F * rm / 2                       # the capsule hangs next to its hook: one hook takes the 150 N (FEM)
    sh = 6 * Mh / (seat * wall ** 2)
    out["gancho"] = dict(M=Mh, sigma=sh, fs=P.PETG_YIELD / sh, fs_z=P.PETG_YIELD_Z / sh)
    sp = P.SIMPLE_FOOT_BOLTS[0]
    Mf = F * abs(x_front - foot["xs"])
    fb = F / 2 + Mf / sp
    bear = fb / (2 * P.M4_CLEAR * W)
    out["pie"] = dict(M=Mf, por_m4=fb, aplast=bear, fs=P.PETG_YIELD / bear, fs_z=P.PETG_YIELD_Z / bear)
    return out


def cable_run(lay, ax, az):
    """Cat5e per camera: box slack + gland + straight conduit from the end wall to the tip hole + loop to the capsule
    PG7 + inside the capsule + spare (no bend chamber any more)."""
    _, out_h, _, _, _, x0, _ = CP.cap_dims()
    g = (ax + cap_pt(x0 + P.CAP_GLAND_X, -out_h / 2)[0], 0.0, az + cap_pt(x0 + P.CAP_GLAND_X, -out_h / 2)[1])
    ex = (XT, 0.0, Z_RAIL + W + TIP_HOLE / 2)
    rail = XT - lay.box_outer()[0] / 2 + P.PG7_DOME[1] * 0
    a = P.CABLE_ALLOW
    loop = max(a["bucle"], math.dist(ex, g))
    total = a["caja"] + a["prensaestopas"] + rail + loop + a["capsula"] + a["holgura"]
    return dict(rail=rail, loop=loop, total=total, spi=total > P.SPI_TEST_LIMIT)


def piece_mass(shape, infill):
    return FA.mass_g(shape, infill)


# ------------------------------------------------------------------ main
# ------------------------------------------------------------------ bodies of the assembly STEP
def one_solid(name, shape, rec):
    """The body of the assembly as ONE valid Solid (ShapeFix when it is not), so Onshape imports it as a single part.
    rec gets the entry written to ensamble_solidos.json."""
    s = solid(shape)
    fixed = False
    if not (BRepCheck_Analyzer(s.wrapped, True).IsValid() and len(s.Solids()) == 1):
        s = solid(sanitize(cq.Workplane().add(s)))
        fixed = True
    sols = s.Solids()
    out = sols[0] if len(sols) == 1 else s
    valid = bool(BRepCheck_Analyzer(out.wrapped, True).IsValid() and len(sols) == 1 and out.Volume() > 0)
    rec.append(dict(nombre=name, solidos=len(sols), valido=valid, corregido=fixed, volumen_mm3=round(out.Volume(), 1)))
    return out


def cord_air(axes, groups):
    """Minimum free distance (mm) from each cord/line (axes: name -> [(p, q), ...], radius LANTERN_CORD_D / 2) to each group of
    node bodies (groups: name -> [shapes]); returns {group: {cord: mm}}."""
    from scipy.spatial import cKDTree
    r = P.LANTERN_CORD_D / 2
    samples = {}
    for name, segs in axes.items():
        pts = []
        for p, q in segs:
            p, q = np.array(p, float), np.array(q, float)
            pts.append(p + (q - p) * np.linspace(0, 1, int(max(20, np.linalg.norm(q - p))))[:, None])
        samples[name] = np.vstack(pts)
    out = {}
    for g, shapes in groups.items():
        tree = cKDTree(E.surface_points(shapes, 0.7))
        out[g] = {name: float(tree.query(pp)[0].min() - r) for name, pp in samples.items()}
    return out


def ballast_h(depth, g_side, rho):
    """Height (mm) that g_side grams of bulk ballast of apparent density rho (g/cm3) fill in the pocket."""
    d = pocket_dims(depth)
    return g_side / rho * 1000.0 / (P.PLATE_L * (d["win"] - 2 * P.PLATE_CLR))


# ------------------------------------------------------------------ main
def main():
    t0 = time.time()
    for d in [OUT / "stl", OUT / "step", OUT / "simscale"] + ([LR_OUT] if P.SEP_USE else []):
        d.mkdir(parents=True, exist_ok=True)
    for old in list((OUT / "stl").glob("*")) + list((OUT / "step").glob("*")):
        old.unlink()                                    # piece names changed in V2: no stale files
    fails, warns = [], []
    lay = layout.build(P.SIMPLE_ESP32_BASE, floors=P.SIMPLE_FLOORS)
    set_pad(lay)
    s = layout.summary(lay)
    if s["conflictos"] or s["fuera_de_cavidad"]:
        fails.append(f"layout {P.SIMPLE_ESP32_BASE} {P.SIMPLE_FLOORS} pisos: {s['conflictos']} {s['fuera_de_cavidad']}")
    depth = CFG.get("bolsillo", P.SIMPLE_POCKET_DEPTH)
    an = FA.analyse_box(lay)
    if ESTET:
        an["m2"] = solid(lid_logo(lid_edges(an["m2"])))
    cp = capsule_parts()
    ax, az, foot = capsule_pose(lay, cp)
    m1 = solid(sanitize(central_mono(lay, depth, foot) if MONO else box_body_low(lay, depth)))
    trays = {kk: solid(sanitize(t)) for kk, t in trays_low(lay).items()}
    cover = solid(pocket_cover(depth))
    print("caja", f"{time.time() - t0:.0f}s", "exterior", [round(v, 1) for v in lay.box_outer()], flush=True)

    # pieces
    stl, step = OUT / "stl", OUT / "step"
    clamp = solid(clamp_piece()) if HOOK_STYLE == "abrazadera" else None
    if MONO:
        end_p = solid(end_piece(lay, foot, cp["lid"], ax, az))
        rail_calc = solid(rail_piece(lay, foot, "stub")).fuse(end_p).clean()
        rows = [process("M1m caja con tramos de riel", m1, K_M1, stl, step, thick=False),
                process("M2 caja, tapa con asa", an["m2"], "M2_caja_tapa", stl, step, thick=False),
                process("M3t tapa del bolsillo", cover, "M3t_tapa_bolsillo", stl, step, thick=False),
                process("M5m extremo de riel con pie y tapa", end_p, K_M5, stl, step)]
    else:
        half = solid(rail_half(lay, foot))
        m5s = solid(lid_with_foot(cp["lid"], ax, az, foot))
        rows = [process("M1 caja baja con bolsillos", m1, K_M1, stl, step, thick=False),
                process("M2 caja, tapa con asa", an["m2"], "M2_caja_tapa", stl, step, thick=False),
                process("M3s riel con gancho, mitad", half, K_RAIL, stl, step, orient_name="X+90"),
                process("M3t tapa del bolsillo", cover, "M3t_tapa_bolsillo", stl, step, thick=False),
                process("M5s tapa con pie", m5s, K_M5, stl, step)]
    if clamp is not None:
        rows.append(process("M9c abrazadera (media luna del gancho)", clamp, "M9c_abrazadera", stl, step, thick=False))
    for kk, t in trays.items():
        rows.append(process(f"M11 bandeja ({kk})", t, kk, stl, step, thick=False))
    rows += [process("M4 capsula, cuerpo", cp["M4"], "M4_capsula_cuerpo", stl, step, thick=False),
             process("M6 bisel", cp["M6"], "M6_capsula_bisel", stl, step, thick=False),
             process("M7 ventana (acrilico)", cp["M7"], "M7_capsula_ventana", stl, step, thick=False)]
    for r in rows:
        chk_ok = r["chk"]["ok"] or (ESTET and r["stem"] == "M2_caja_tapa" and FILLET_LOG.get("logo") and r["chk"]["brep"]
                                    and not r["chk"]["bop"] and r["chk"]["solids"] == 1)    # OCCT flags the B-spline text; B-rep valid
        ok = chk_ok and r["mc"]["watertight"] and r["mc"]["bodies"] == 1 and r["mc"]["fits_bed"]
        if not ok:
            fails.append(f"{r['stem']}: brep={r['chk']} estanco={r['mc']['watertight']} cuerpos={r['mc']['bodies']} cama={r['mc']['fits_bed']}")
        if r["p1"] == r["p1"] and r["p1"] < P.MIN_WALL:
            fails.append(f"{r['stem']}: espesor p1 {r['p1']:.2f} < {P.MIN_WALL}")
        print(f"{r['stem']:24s} ok={ok} or={r['orient']} bbox={tuple(round(v, 1) for v in r['mc']['bbox'])} "
              f"ov={r['mc']['overhang_mm2']:.0f} p1={r['p1']:.2f}", flush=True)
    R = {r["stem"]: r["shape"] for r in rows}
    m5s = R[K_M5]
    if MONO:
        half = rail_calc
    else:
        half = R[K_RAIL]
    print("piezas", f"{time.time() - t0:.0f}s", flush=True)

    # fused rail for SimScale and the local FEM (both halves + the box pad region is not included)
    fem_path = OUT / "simscale" / "riel_fem.step"      # one side of the rail as the local FEM sees it (fem.py)
    cq.exporters.export(cq.Workplane().add(half), str(fem_path))
    fix_step_stamp(fem_path)
    if MONO:
        n_sol, sim_note = 1, "P3/P4: riel fundido (tramo central + extremo) de un lado, con las bridas de union como cuerpo continuo"
    else:
        fused = half.fuse(put(half, -1)).clean()
        sim_path = OUT / "simscale" / "M3s_riel_fusionado.step"
        cq.exporters.export(cq.Workplane().add(fused), str(sim_path))
        fix_step_stamp(sim_path)
        n_sol = len(fused.Solids())
        sim_note = "dos mitades separadas por la caja: el STEP tiene las 2 mitades con sus ganchos" if n_sol == 2 else ""

    # masses (the same per piece for the buoyancy and the bitacora), buoyancy and the bulk ballast (one pocket per side)
    cav = CP.capsule_cavity().val()
    air = cav.Volume() - cav.intersect(cp["M4"].val()).Volume()
    masses = {K_M1: piece_mass(m1, INFILL["M1"]), "M2_caja_tapa": piece_mass(an["m2"], INFILL["M2"]),
              "M3t_tapa_bolsillo": piece_mass(cover, INFILL["M3t"]),
              K_M5: piece_mass(m5s, INFILL["M5s"]), "M4_capsula_cuerpo": piece_mass(cp["M4"].val(), INFILL["M4"]),
              "M6_capsula_bisel": piece_mass(cp["M6"].val(), INFILL["M6"]),
              "M7_capsula_ventana": P.ACRYLIC_DENSITY * cp["M7"].val().Volume() / 1000}
    if not MONO:
        rail_only = solid(rail_half(lay, foot, hook_on=False))
        hook_part = half.cut(rail_only)
        masses[K_RAIL] = piece_mass(rail_only, INFILL["riel"]) + piece_mass(hook_part, INFILL["gancho"])
    if clamp is not None:
        masses["M9c_abrazadera"] = piece_mass(clamp, INFILL["gancho"])
    rail_vol = 0.0 if MONO else 2 * half.Volume()
    clamp_vol = 0.0 if clamp is None else 2 * clamp.Volume()
    bulk = P.BALLAST_BULK["opciones"][P.BALLAST_BULK["material"]]
    net = 1 - RHO_W / bulk["solido"]                    # net sinking per gram of the ballast metal
    lo, hi = (t * 1000 for t in P.BALLAST_TARGET_KGF)
    mid = P.BALLAST_MID_KGF * 1000
    elec = an["fixed_g"]
    bal = {}
    for f in P.INFILL_CASES:
        tray_g = sum(piece_mass(t, f) for t in trays.values())
        parts_g = {"caja (M1 con bolsillos + M2 + bandejas + electronica)" if not MONO else "caja con tramos de riel (M1m + M2 + bandejas + electronica)":
                   masses[K_M1] + masses["M2_caja_tapa"] + tray_g + elec}
        if not MONO:
            parts_g["riel con ganchos (2 M3s)"] = 2 * masses[K_RAIL]
        if clamp is not None:
            parts_g["abrazaderas (2 M9c)"] = 2 * masses["M9c_abrazadera"]
        parts_g.update({"tapas del bolsillo (2 M3t)": 2 * masses["M3t_tapa_bolsillo"],
                        "capsulas (M4, M5, M6, M7, contenido)": 2 * (masses["M4_capsula_cuerpo"] + masses[K_M5]
                                                                   + masses["M6_capsula_bisel"] + masses["M7_capsula_ventana"] + P.CAPSULE_CONTENT_G),
                        "tornilleria y correas": P.SIMPLE_HARDWARE_G})
        env = m1.fuse(CC.cavity_tool(lay).val())
        disp = (env.Volume() + an["m2"].Volume() + rail_vol + clamp_vol + 2 * cover.Volume()
                + 2 * (cp["M4"].val().Volume() + m5s.Volume() + cp["M6"].val().Volume() + cp["M7"].val().Volume() + air)) / 1000 \
            + P.SIMPLE_HARDWARE_G / P.STEEL_DENSITY
        node_g = sum(parts_g.values())
        app0 = node_g - RHO_W * disp
        bal[f] = dict(parts=parts_g, node_g=node_g, disp=disp, app0=app0,
                      g_lo=(lo - app0) / net, g_mid=(mid - app0) / net, g_hi=(hi - app0) / net)
    f0 = P.INFILL_CASES[0]
    g_tot = max(0.0, round(bal[f0]["g_mid"] / 10.0) * 10.0)      # grams of ballast in the node, 10 g steps (both pockets)
    g_side = g_tot / 2
    g_rng = (max(max(0.0, b["g_lo"]) for b in bal.values()), min(b["g_hi"] for b in bal.values()))
    for f, b in bal.items():
        b.update(g=g_tot, app=b["app0"] + g_tot * net, total=b["node_g"] + g_tot)
        b["in_window"] = lo <= b["app"] <= hi
        if not b["in_window"]:
            fails.append(f"peso aparente {b['app']:+.0f} g con {g_tot:.0f} g de lastre y bandeja al {f * 100:.0f} %: la ventana pide {lo:.0f} a {hi:.0f}")
        if b["total"] > P.AIR_MASS_MAX_KG * 1000:
            fails.append(f"peso en aire {b['total']:.0f} g > {P.AIR_MASS_MAX_KG:g} kg")
    ballast = ballast_solids(depth, g_side, bulk["aparente"])
    h_b, h_hi = ballast_h(depth, g_side, bulk["aparente"]), ballast_h(depth, g_rng[1] / 2, bulk["aparente"])
    dp = pocket_dims(depth)
    pocket_cm3 = P.PLATE_L * (dp["win"] - 2 * P.PLATE_CLR) * depth / 1000
    if h_b > depth - 0.2:
        fails.append(f"el lastre ({g_tot:.0f} g de {bulk['nombre']}) llena {h_b:.1f} mm y el bolsillo mide {depth:g}")
    bsum = dict(material=P.BALLAST_BULK["material"], nombre=bulk["nombre"], aparente=bulk["aparente"], solido=bulk["solido"],
                total_g=g_tot, por_bolsillo_g=g_side, rango_total_g=list(g_rng), altura_mm=h_b, altura_en_el_maximo_mm=h_hi,
                bolsillo_mm=depth, bolsillo_cm3=pocket_cm3, ocupacion=h_b / depth, cabe_en_el_maximo=bool(h_hi <= depth),
                volumen_lastre_cm3=g_side / bulk["aparente"], medida_bolsillo=[P.PLATE_L, dp["win"] - 2 * P.PLATE_CLR, depth])
    alt = {}                                            # the other bulk material, same window, for the report
    for key, o in P.BALLAST_BULK["opciones"].items():
        n2 = 1 - RHO_W / o["solido"]
        g2 = max(0.0, (mid - bal[f0]["app0"]) / n2)
        alt[key] = dict(nombre=o["nombre"], total_g=g2, altura_mm=ballast_h(depth, g2 / 2, o["aparente"]))
    bsum["alternativas"] = alt
    print("lastre", f"{g_tot:.0f} g en 2 bolsillos de {depth:g} mm ({h_b:.1f} mm llenos), rango {g_rng[0]:.0f} a {g_rng[1]:.0f} g, "
          f"peso aparente {bal[f0]['app']:+.0f} g, {time.time() - t0:.0f}s", flush=True)

    node = assemble(an, half, m5s, cover, cp, ax, az, ballast, m1, trays)
    z_rod = Z_RAIL - P.HOOK_DROP

    # interferences inside the node (touching faces give ~0), PG7 nuts inside the box
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
                (slivers if min(bb.xlen, bb.ylen, bb.zlen) <= 0.011 else pairs).append((a, b, v))
    for a, b, v in pairs:
        fails.append(f"interferencia {a} / {b}: {v:.2f} mm3")
    nuts = gland_nuts(lay)
    dummies = [solid(d) for _, d in CC.module_dummies(lay)]
    nut_hits = sum(E.common(n, o) for n in nuts for o in list(trays.values()) + dummies + [m1])
    if nut_hits > P.INTERF_TOL:
        fails.append(f"contratuercas de los PG7 de las paredes chocan {nut_hits:.2f} mm3 (bandeja, modulos o caja)")
    cable_gap = foot["bz"] - P.M4_CLEAR / 2 - (CABLE_Z + P.CAT5E_D / 2)
    if cable_gap < 0.5:
        fails.append(f"los M4 del pie pasan a {cable_gap:.1f} mm del Cat5e")
    print("interferencias", len(pairs), "tuercas", round(nut_hits, 3), f"{time.time() - t0:.0f}s", flush=True)

    # stability (trays 40 %)
    f = P.INFILL_CASES[0]
    xr = node[f"{K_M5}_der"][0]
    m_pts = [(m1.Center().z, masses[K_M1]), (an["m2"].Center().z, masses["M2_caja_tapa"])]
    m_pts += [(t.Center().z, piece_mass(t, f)) for t in trays.values()]
    m_pts += [((b.z[0] + b.z[1]) / 2, P.COMPONENTS[key][3]) for _, key, b in lay.modules]
    m_pts.append((P.BOX_FLOOR + lay.cav[2] / 2, elec - sum(P.COMPONENTS[key][3] for _, key, _ in lay.modules)))
    m_pts += [(cover.Center().z, 2 * masses["M3t_tapa_bolsillo"]),
              (node["M4_capsula_cuerpo_der"][0].Center().z, 2 * (masses["M4_capsula_cuerpo"] + P.CAPSULE_CONTENT_G)),
              (xr.Center().z, 2 * masses[K_M5]), (Z_RAIL + S / 2, P.SIMPLE_HARDWARE_G)]
    if not MONO:
        m_pts.append((half.Center().z, 2 * masses[K_RAIL]))
    if clamp is not None:
        m_pts.append((Z_RAIL - P.HOOK_DROP, 2 * masses["M9c_abrazadera"]))
    m_pts += [(b.Center().z, g_side) for b in ballast.values()]
    air_w = place_cap(cav.cut(cp["M4"].val()), ax, az)
    env_box = m1.fuse(CC.cavity_tool(lay).val())
    b_pts = [(env_box.Center().z, env_box.Volume()), (an["m2"].Center().z, an["m2"].Volume()),
             (cover.Center().z, 2 * cover.Volume()),
             (node["M4_capsula_cuerpo_der"][0].Center().z, 2 * cp["M4"].val().Volume()), (xr.Center().z, 2 * m5s.Volume()),
             (air_w.Center().z, 2 * air_w.Volume())] + [(b.Center().z, g_side / bulk["solido"] * 1000) for b in ballast.values()]
    if not MONO:
        b_pts.append((half.Center().z, 2 * half.Volume()))
    zg = sum(z * m for z, m in m_pts) / sum(m for _, m in m_pts)
    zb = sum(z * v for z, v in b_pts) / sum(v for _, v in b_pts)
    if zg >= zb:
        fails.append(f"centro de masa sobre el de empuje (G {zg:.1f}, B {zb:.1f})")

    # test lantern: ring, 4 cords to ONE tie point, cabo to the long line (no separator since tanda 3) and clearances
    node_solids = [v[0] for v in node.values()]
    node_pts = E.surface_points(node_solids, 0.7)
    z_top_node = float(node_pts[:, 2].max())
    h_sep_min = min_separator_h(node_pts, z_rod) if P.SEP_USE else None
    sep, z_sep = None, None
    if P.SEP_USE:                                       # legacy path (LR1 + apex), kept: separador.usar = True
        z_sep = z_rod + P.SEP_H
        z_apex = z_sep + P.APEX_H
        sep = solid(separator(z_sep))
        lant0, axes0, buoy_end = lantern(z_rod, z_sep, z_apex)
        lant = {"REF_" + kk.replace(" ", "_").replace("(", "").replace(")", ""): v for kk, v in lant0.items()}
        axes = {"REF_" + kk.replace(" ", "_"): [pq] for kk, pq in axes0.items()}
        z_bend = z_tie = z_apex
        if P.SEP_H < h_sep_min:
            fails.append(f"separador.altura {P.SEP_H:g} < minimo {h_sep_min:.0f}")
    else:
        z_bend = z_top_node + P.CORD_CLEAR + P.LANTERN_CORD_D          # cords go straight up past the lid, then to the tie point
        z_tie = z_rod + P.LANTERN_TIE_H
        z_apex = z_tie
        if z_tie < z_bend + 50.0:
            fails.append(f"linterna.nudo_h {P.LANTERN_TIE_H:g} deja el punto de amarre a menos de 50 mm sobre el codo de las cuerdas ({z_bend - z_rod:.0f})")
        lant, axes, buoy_end = lantern_tie(z_rod, z_bend, z_tie)
    umb = umbilical(lid_gland_point(lay), buoy_end)
    arm_sh = [half, put(half, -1)]
    cap_keys = [kk for kk in node if "capsula" in kk or kk.startswith(K_M5)]
    cap_sh = [node[kk][0] for kk in cap_keys]
    rail_keys = [kk for kk in node if kk.startswith(K_RAIL)]
    box_sh = [v[0] for kk, v in node.items() if kk not in cap_keys and kk not in rail_keys]
    air_g = cord_air(axes, {"brazo": arm_sh, "capsula": cap_sh, "caja": box_sh})
    clr = {g: min(v.values()) for g, v in air_g.items()}
    airs = {f"{g}/{c}": v for g, d in air_g.items() for c, v in d.items()}
    worst = min(clr["brazo"], clr["capsula"])
    if worst < P.CORD_CLEAR:
        fails.append(f"aire minimo cuerda-brazo {clr['brazo']:.1f} / cuerda-capsula {clr['capsula']:.1f} mm < {P.CORD_CLEAR:g}")
    if clr["caja"] < 0:
        warns.append(f"cuerda contra la caja: {clr['caja']:.1f} mm (interpenetra)")
    elif clr["caja"] < P.CORD_CLEAR:
        warns.append(f"cuerda-caja (brida de la tapa) a {clr['caja']:.1f} mm, menos que los {P.CORD_CLEAR:g} que se piden a brazos y capsulas")
    ring_hits = {kk: E.common(v[0], lant["REF_aro_superior"]) for kk, v in node.items() if E.bb_hit(bbs[kk], E.bbox(lant["REF_aro_superior"]))}
    ring_hits = {kk: v for kk, v in ring_hits.items() if not (v <= P.INTERF_TOL)}
    net_hits = {kk: E.common(v[0], lant["REF_linterna_malla"]) for kk, v in node.items() if E.bb_hit(bbs[kk], E.bbox(lant["REF_linterna_malla"]))}
    net_hits = {kk: v for kk, v in net_hits.items() if not (v <= P.INTERF_TOL) and not kk.startswith("M9c")}   # the net is lashed through the clamp
    for kk, v in {**ring_hits, **{f"red/{a}": b for a, b in net_hits.items()}}.items():
        fails.append(f"linterna contra el nodo: {kk} {v:.2f} mm3")
    views = [camera_view(ax, az, z_rod, R_RING), camera_view(ax, az, z_rod, 250.0)]
    print("linterna", {g: round(v, 1) for g, v in clr.items()}, "nudo +", round(z_tie - z_rod), "camara", views, f"{time.time() - t0:.0f}s", flush=True)
    for w in warns:
        print("AVISO:", w, flush=True)

    lr = None
    if P.SEP_USE:
        lr = process("LR1 separador", solid(separator(P.SEP_SECTION[1] / 2)), "LR1_separador", LR_OUT, LR_OUT, thick=False)
        if not (lr["chk"]["ok"] and lr["mc"]["fits_bed"]):
            fails.append(f"LR1_separador: brep={lr['chk']['ok']} cama={lr['mc']['fits_bed']}")

    # assembly STEP: one named body per part (printed ones by code and stem, the rest REF_*), each ONE valid solid
    rec = []
    asm = cq.Assembly(name=f"nodo_{P.VERSION}")
    named = {}
    for kk, (sh, g) in node.items():
        named[kk] = one_solid(kk, sh, rec)
    for kk, sh in lant.items():
        named[kk] = one_solid(kk, sh, rec)
    if sep is not None:
        named["LR1_separador"] = one_solid("LR1_separador", sep, rec)
    for i, u in enumerate(umb):
        named["REF_umbilical" if len(umb) == 1 else f"REF_umbilical_{i + 1}"] = one_solid("REF_umbilical", u, rec)
    for kk, sh in named.items():
        asm.add(sh, name=kk)
    asm_path = OUT / f"ensamble_simple_D{P.SIMPLE_RING_D:g}.step"
    asm.export(str(asm_path))
    fix_step_stamp(asm_path)
    bad = [r_ for r_ in rec if not r_["valido"]]
    for r_ in bad:
        fails.append(f"ensamble: {r_['nombre']} no es un solido unico valido ({r_['solidos']} solidos)")
    import re
    step_names = re.findall(r"PRODUCT\('([^']*)'", asm_path.read_text(encoding="utf-8", errors="replace"))
    back = cq.importers.importStep(str(asm_path))
    n_back = sum(len(v.Solids()) for v in back.vals())
    miss = [kk for kk in named if kk not in step_names]
    if miss or n_back != len(named):
        fails.append(f"el STEP del ensamble: {n_back} solidos leidos de {len(named)}, nombres que faltan {miss}")
    (OUT / "ensamble_solidos.json").write_text(json.dumps(dict(
        ensamble=asm_path.name, version=P.VERSION, cuerpos=len(rec), solidos_total=sum(r_["solidos"] for r_ in rec),
        solidos_leidos_del_step=n_back, nombres_en_step=len(step_names) - 1, cuerpos_no_validos=[r_["nombre"] for r_ in bad],
        solidos=rec), indent=1, ensure_ascii=False), encoding="utf-8")
    print("ensamble", len(rec), "cuerpos,", n_back, "solidos leidos del STEP", f"{time.time() - t0:.0f}s", flush=True)

    from render import render
    col = {"caja": ("#5b8fb9", 0.55), "riel": ("#3a9d7a", 1.0), "lastre": ("#777777", 1.0), "lastre_t": ("#3a9d7a", 1.0)}
    node_items = [(sh, *col.get(g, ("#3a7ca5", 1.0)), True, None) for sh, g in node.values()]
    items = list(node_items)
    for kk, sh in lant.items():
        cc = "#c0504d" if kk.startswith(("REF_cuerda", "REF_cabo")) else "#8a8a8a" if kk == "REF_aro_superior" else "#b9d6e8"
        items.append((sh, cc, 0.25 if kk.startswith(("REF_linterna_malla", "REF_linterna_piso")) else 0.9, False, None))
    items += ([(sep, "#e07b39", 1.0, True, None)] if sep is not None else []) + [(u, "#222222", 1.0, False, None) for u in umb]
    title = (f"Nodo {P.VERSION} Ø{P.SIMPLE_RING_D:g}: caja baja, capsulas {P.SIMPLE_CAP_AZ} a {P.SIMPLE_CAP_TILT:g} grados, "
             + (f"separador a {P.SEP_H:g}, apice +{P.APEX_H:g}" if P.SEP_USE else f"4 cuerdas al nudo a {z_tie - z_rod:.0f} mm sobre el aro, sin separador"))
    render(items, OUT / "ensamble_simple_iso.png", "iso", title)
    render(items, OUT / "ensamble_simple_lado.png", "frontal", title)
    render(node_items, OUT / "nodo_simple_iso.png", "iso", f"Nodo {P.VERSION} (sin la linterna)")
    half_cut = _box(-400, 400, -200, 0, -300, 300).val()
    render([(sh.cut(half_cut), c, 1.0 if c != "#5b8fb9" else 0.9, True, None) for sh, c, *_ in node_items
            if sh.BoundingBox().ymin < 0 and sh.cut(half_cut).Volume() > 1e-3],
           OUT / "nodo_simple_corte.png", "frontal", "Corte en y = 0: PG7 por la pared extrema al conducto del riel, bolsillos de lastre bajo la caja")

    x_load = node["M4_capsula_cuerpo_der"][0].Center().x
    x_front = (ax + cap_pt(CP.cap_dims()[6], 0)[0])
    calc = hand_calcs(lay, half, x_load, x_front, foot)
    cab = cable_run(lay, ax, az)
    QTY.update({K_M1: 1, "M2_caja_tapa": 1, "M3t_tapa_bolsillo": 2, K_M5: 2, "M4_capsula_cuerpo": 2, "M6_capsula_bisel": 2,
                "M7_capsula_ventana": 2})
    QTY.update({kk: 1 for kk in trays})
    if not MONO:
        QTY[K_RAIL] = 2
    if clamp is not None:
        QTY["M9c_abrazadera"] = 2
    printed = {kk: q for kk, q in QTY.items() if not kk.startswith("M7")}
    juntas = dict(riel_caja=0 if MONO else 2, union_extremo=2 if MONO else 0, pie_m4=0 if MONO else 2,
                  abrazadera_m4=2 if clamp is not None else 0)
    EXTRA.update(zmax_sobre_aro=z_top_node - z_rod, zmin_sobre_aro=float(node_pts[:, 2].min()) - z_rod,
                 cg_sobre_aro=zg - z_rod, cb_sobre_aro=zb - z_rod, piezas_impresas=sum(printed.values()),
                 tipos_impresos=len(printed), camaras=views, caja_exterior=list(lay.box_outer()),
                 version=P.VERSION, cfg=CFG, cantidades=dict(QTY), sellos=SEALS, juntas_atornilladas=juntas,
                 celosia_ventanas=dict(TRUSS_N), redondeos=dict(FILLET_LOG),
                 aire_cuerdas=dict(brazo=clr["brazo"], capsula=clr["capsula"], caja=clr["caja"]),
                 cuerdas=dict(azimut_en_el_marco_del_nodo=list(P.SIMPLE_CORD_AZ), codo_sobre_aro=z_bend - z_rod,
                              nudo_sobre_aro=z_tie - z_rod, por_cuerda=airs),
                 ensamble=dict(cuerpos=len(rec), solidos=n_back, no_validos=[r_["nombre"] for r_ in bad]), avisos=warns)
    secs = time.time() - t0
    save_results(rows + ([lr] if lr else []), masses, bal, bsum, zg, zb, clr, h_sep_min, z_rod, z_apex, calc, cab, lay, trays)
    write_report(rows, lr, bal, bsum, zg, zb, clr, h_sep_min, z_rod, z_sep, z_apex, z_top_node, pairs, slivers,
                 ring_hits, net_hits, calc, cab, n_sol, sim_note, cable_gap, nut_hits, views, fails, warns, lay, foot, secs, z_bend)
    print(f"peso aparente {bal[0.4]['app']:+.0f} g, lastre {g_tot:.0f} g, total {bal[0.4]['total']:.0f} g, nudo {z_tie - z_rod:.0f} mm sobre el aro, "
          f"aire cuerda-brazo {clr['brazo']:.1f} / capsula {clr['capsula']:.1f} / caja {clr['caja']:.1f} mm, "
          f"alto {z_top_node - float(node_pts[:, 2].min()):.0f} mm, {secs:.0f}s")
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if fails else 0


def save_results(rows, masses, bal, bsum, zg, zb, clr, h_sep_min, z_rod, z_apex, calc, cab, lay, trays):
    """salida/simple/resultados.json: what the bitacora reads (same mass per piece as the buoyancy)."""
    ol, ow, oh = lay.box_outer()
    out_w, out_h, *_ = CP.cap_dims()
    _, _, _, _, _, x0, x_front = CP.cap_dims()
    infill_of = {"M1s_caja_cuerpo": "M1", "M1m_caja_riel": "M1", "M2_caja_tapa": "M2", "M3s_riel_gancho": "riel",
                 "M3t_tapa_bolsillo": "M3t", "M5s_capsula_tapa_pie": "M5s", "M5m_extremo_pie": "M5s", "M4_capsula_cuerpo": "M4",
                 "M6_capsula_bisel": "M6", "LR1_separador": "LR1", "M9c_abrazadera": "gancho"}
    piezas = {}
    for r in rows:
        st = r["stem"]
        inf = INFILL.get(infill_of.get(st, "M11" if st.startswith("M11") else "M6"), 0.4)
        m = masses.get(st) or (piece_mass(r["shape"], inf) if not st.startswith("M7") else None)
        piezas[st] = dict(nombre=r["name"], orient=r["orient"], bbox=list(r["mc"]["bbox"]), voladizo_mm2=r["mc"]["overhang_mm2"],
                          soportes=r["mc"]["overhang_mm2"] > SUPPORT_MM2, volumen_cm3=r["shape"].Volume() / 1000,
                          relleno=("riel 40 %, gancho 100 %" if st == "M3s_riel_gancho" else (None if st.startswith("M7") else inf)),
                          masa_g=m)
    data = {
        "piezas": piezas, "soporte_umbral_mm2": SUPPORT_MM2,
        "riel": dict(largo=P.SIMPLE_RAIL_L, seccion=S, pared=W, fondo_z=Z_RAIL),
        "caja": dict(exterior=[ol, ow, oh], interior=list(lay.cav), con_brida=[ol + 2 * P.BOX_FLANGE, ow + 2 * P.BOX_FLANGE],
                     pared=P.BOX_WALL, fondo=P.BOX_FLOOR, esp32=P.SIMPLE_ESP32_BASE, pisos=P.SIMPLE_FLOORS),
        "capsula": dict(exterior=[x_front - x0, out_w, out_h], cavidad=[CP.CAP_CAV_L, CP.CAP_CAV_W, CP.CAP_CAV_H],
                        angulo=P.SIMPLE_CAP_TILT, acimut=P.SIMPLE_CAP_AZ),
        "ventana": dict(diametro=P.WIN_DIA, espesor=P.WIN_T),
        "gancho": dict(c_interior=P.RING_SECTION + 2 * P.SIMPLE_HOOK_C[0], pared=P.SIMPLE_HOOK_C[1],
                       asiento=P.SIMPLE_HOOK_C[2], caida=P.HOOK_DROP, correa=P.SIMPLE_HOOK_STRAP, fusionado=True),
        "separador": dict(usar=P.SEP_USE, tipo=P.SEP_TYPE, seccion=list(P.SEP_SECTION), altura=P.SEP_H, altura_min=h_sep_min),
        "lastre": bsum,
        "peso": {f"{int(f * 100)}": dict(aire_g=b["total"], aparente_g=b["app"], sin_lastre_g=b["app0"], lastre_g=b["g"],
                                          lastre_min_g=max(0.0, b["g_lo"]), lastre_max_g=b["g_hi"]) for f, b in bal.items()},
        "bg_mm": zb - zg, "apice_sobre_aro": z_apex - z_rod, "aire_min": min(clr["brazo"], clr["capsula"]),
        "fs": dict(riel=calc["riel"]["fs"], riel_capas=calc["riel"]["fs_z"], pie=calc["pie"]["fs"],
                   pie_capas=calc["pie"]["fs_z"], gancho=calc["gancho"]["fs"], gancho_capas=calc["gancho"]["fs_z"]),
        "insertos_N": calc["insertos"]["por_inserto"], "cable_mm": cab["total"], **EXTRA,
    }
    (OUT / "resultados.json").write_text(json.dumps(data, indent=1, ensure_ascii=False, default=float), encoding="utf-8")


def write_report(rows, lr, bal, bsum, zg, zb, clr, h_sep_min, z_rod, z_sep, z_apex, z_top_node, pairs, slivers,
                 ring_hits, net_hits, calc, cab, n_sol, sim_note, cable_gap, nut_hits, views, fails, warns, lay, foot, secs, z_bend):
    qty = QTY
    b4, b1 = bal[0.4], bal[1.0]
    ol, ow, oh = lay.box_outer()
    L = ["# Version {} del nodo, aro Ø{:g} (generado por `simple.py`)".format(P.VERSION, P.SIMPLE_RING_D), "",
         "No editar a mano: se regenera con `python cad_final/build.py --rapido` cuando `version = \"simple\"` en "
         "`params.py`. La version modular no cambia. mm, g, N, MPa.", "",
         f"**V2 (29/10, decisiones del equipo) y tanda 3 (30/10 noche):** ESP32-S3 sobre {P.SIMPLE_ESP32_BASE.upper()} en {P.SIMPLE_FLOORS} pisos "
         f"(caja {ol:.1f} × {ow:.1f} × {oh:.1f}). **Caja baja:** el PG7 de cada camara atraviesa la pared extrema de M1 a "
         f"z = {Z_G:.1f}, el eje del conducto del riel, y el domo entra en el conducto: no hay camara de cables. Cada mitad "
         f"del riel (M3s, con el gancho en C fusionado) se atornilla con una brida a un cojin de la pared extrema (4 M4 a "
         f"insertos). **Lastre a granel:** un bolsillo por lado moldeado bajo el piso de M1, fuera del sello, cerrado por M3t. Capsulas "
         f"fijas a {P.SIMPLE_CAP_TILT:g} grados mirando **{P.SIMPLE_CAP_AZ}** (a la malla); la tapa M5s trae el pie en silla "
         "con 2 M4 que cruzan el riel.", "",
         "## 1. Piezas", "",
         "| Pieza | Archivo (`salida/simple/stl`, `step`) | Cant. | BRep/BOP | Estanco | Cuerpos | Bbox en la orientacion (mm) | Voladizo mm² | Espesor p1 | Masa al 100 % g |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        mc = r["mc"]
        m = (P.ACRYLIC_DENSITY if r["stem"].startswith("M7") else P.PETG_DENSITY) * r["shape"].Volume() / 1000
        p1 = "" if r["p1"] != r["p1"] else f"{r['p1']:.2f}"
        L.append(f"| {r['name']} | {r['stem']} | {qty.get(r['stem'], 1)} | {'ok' if r['chk']['ok'] else 'FALLA'} | "
                 f"{'si' if mc['watertight'] else 'NO'} | {mc['bodies']} | {' x '.join(f'{v:.1f}' for v in mc['bbox'])} "
                 f"({r['orient']}) | {mc['overhang_mm2']:.0f} | {p1} | {m:.0f} |")
    L += ["", f"Piezas impresas por nodo: {EXTRA['piezas_impresas']} de {EXTRA['tipos_impresos']} tipos, mas las 2 ventanas M7 de "
          "acrilico. Fusionado respecto de V1: el gancho M9s dentro de cada mitad del riel (se imprimen de costado, la C y el "
          "riel en el plano de las capas) y la camara de cables dentro de la caja; los bolsillos del lastre dentro de M1. "
          "Quedan aparte, para desmontar: tapas (M2, M3t, M5s), capsulas y bandeja.",
          f"STEP del riel para SimScale y el FEM local: `salida/simple/simscale/M3s_riel_fusionado.step` ({n_sol} solido(s)"
          + (f"; {sim_note}" if sim_note else "") + ").", "",
          "## 2. Peso, lastre y peso aparente", "",
          f"Masa por pieza con su relleno (100 % cajas estancas, tapas con junta y ganchos; 40 % riel y bandeja; piel de "
          f"{P.SHELL_T:g}): la misma que usa la bitacora. **Lastre:** {bsum['nombre']} (densidad aparente {bsum['aparente']:g} g/cm³ del granel, "
          f"metal de {bsum['solido']:g}; ESTIMADO, pesar un cubo lleno), UN bolsillo por lado de {bsum['medida_bolsillo'][0]:g} × "
          f"{bsum['medida_bolsillo'][1]:g} × {bsum['medida_bolsillo'][2]:g} mm ({bsum['bolsillo_cm3']:.0f} cm³) cerrado por M3t con 2 M3. "
          f"En el ensamble es un solido por bolsillo (`lastre_izq` = +Y, `lastre_der` = -Y).", "",
          "| Concepto | Bandeja 40 % | Bandeja 100 % |", "|---|---|---|"]
    for kk in b4["parts"]:
        L.append(f"| {kk} | {b4['parts'][kk]:.0f} | {b1['parts'][kk]:.0f} |")
    L += [f"| Nodo sin lastre g | {b4['node_g']:.0f} | {b1['node_g']:.0f} |",
          f"| Desplaza cm³ | {b4['disp']:.0f} | {b1['disp']:.0f} |",
          f"| Peso aparente sin lastre g | {b4['app0']:+.0f} | {b1['app0']:+.0f} |",
          f"| Lastre que deja el peso aparente en la ventana ({P.BALLAST_TARGET_KGF[0] * 1000:.0f} a {P.BALLAST_TARGET_KGF[1] * 1000:.0f} g), total g | "
          f"{max(0, b4['g_lo']):.0f} a {b4['g_hi']:.0f} | {max(0, b1['g_lo']):.0f} a {b1['g_hi']:.0f} |",
          f"| **Lastre puesto g (total, mitad por bolsillo)** | **{b4['g']:.0f}** ({b4['g'] / 2:.0f}) | **{b1['g']:.0f}** ({b1['g'] / 2:.0f}) |",
          f"| **Peso aparente con ese lastre g** | **{b4['app']:+.0f}** | **{b1['app']:+.0f}** |",
          f"| **Peso en aire g** | **{b4['total']:.0f}** | **{b1['total']:.0f}** |", "",
          f"Rango de lastre que mantiene ambos casos en la ventana: **{bsum['rango_total_g'][0]:.0f} a {bsum['rango_total_g'][1]:.0f} g** en total. "
          f"El granel llena {bsum['altura_mm']:.1f} de {bsum['bolsillo_mm']:g} mm del bolsillo ({bsum['ocupacion'] * 100:.0f} %); en el maximo del rango llenaria "
          f"{bsum['altura_en_el_maximo_mm']:.1f} mm ({'cabe' if bsum['cabe_en_el_maximo'] else 'NO cabe'}). "
          + " ".join(f"Con {a['nombre']}: {a['total_g']:.0f} g en total, {a['altura_mm']:.1f} mm llenos." for a in bsum["alternativas"].values()),
          "", f"Estabilidad: centro de masa a {zg - z_rod:.1f} y de empuje a {zb - z_rod:.1f} sobre el aro, BG = **{zb - zg:.1f} mm**.", "",
          "## 3. Linterna de prueba, cuerdas y camaras", "",
          "Aro Ø200, malla de referencia, **4 cuerdas** que suben rectas del aro (atadas por fuera de la varilla) a 45 grados del riel, por encima de la tapa, y de ahi "
          "van rectas a **un solo punto de amarre**; del nudo sale un cabo a la linea larga. Sin separador LR1, sin anillo guia y sin apice. "
          "El nodo cuelga del aro con el riel (los brazos) entre cuerdas.", "",
          "| Concepto | Valor |", "|---|---|",
          f"| Nodo sobre el centro de la varilla del aro | de {EXTRA['zmin_sobre_aro']:.0f} a {z_top_node - z_rod:.0f} mm |",
          f"| Azimut de las cuerdas en el marco del nodo (riel en X) | {', '.join(f'{a:g}' for a in P.SIMPLE_CORD_AZ)} grados |",
          f"| Codo de las cuerdas / punto de amarre sobre el aro | {z_bend - z_rod:.0f} / **{z_apex - z_rod:.0f} mm** (`linterna.nudo_h`) |",
          f"| **Aire cuerda-brazo** (exigido {P.CORD_CLEAR:g}) | **{clr['brazo']:.1f} mm** |",
          f"| **Aire cuerda-capsula** (exigido {P.CORD_CLEAR:g}) | **{clr['capsula']:.1f} mm** |",
          f"| Aire cuerda-caja (brida de la tapa; informativo) | {clr['caja']:.1f} mm |",
          f"| Aro y red contra el nodo | {'sin contacto' if not (ring_hits or net_hits) else {**ring_hits, **net_hits}} |"]
    if lr is not None:
        L.append(f"| Separador `separador.altura` (separador.usar = True) | {P.SEP_H:g} mm (minimo calculado: **{h_sep_min:.0f}**) |")
    for v in views:
        if v["dist"]:
            L.append(f"| Camara en Ø{v['D']:g}: lente a la red | {v['dist']:.0f} mm, campo diagonal {v['campo_diag']:.0f} mm, "
                     f"{'dentro' if v['en_foco'] else 'FUERA'} del enfoque ({P.CAM_FOCUS[0]:g} mm a infinito, estimado) |")
        else:
            L.append(f"| Camara en Ø{v['D']:g} | el eje optico no corta la red |")
    L += ["", f"FOV {P.CAM_FOV_DIAG:g} grados diagonal (estimado, sin ficha). El aro LED rodea el lente: ilumina el encuadre si "
          "su haz es al menos tan ancho como el FOV (dato del LED por confirmar).", "",
          "## 4. Interferencias y recorridos", "",
          ("Ninguna (umbral {:g} mm³).".format(P.INTERF_TOL) if not pairs else "\n".join(f"- {a} / {b}: {v:.2f} mm³" for a, b, v in pairs)),
          ("Solapes de modelado de 0.01 mm (no son choques): " + "; ".join(f"{a} / {b} {v:.1f}" for a, b, v in slivers) + ".") if slivers else "",
          f"Contratuercas de los PG7 de las paredes contra bandeja, modulos y caja: {nut_hits:.2f} mm³ (la bandeja tiene una "
          "muesca en cada extremo). Los M4 del pie pasan "
          f"{cable_gap:.1f} mm sobre el Cat5e.", "",
          "## 5. Verificacion a mano (150 N de manipulacion en una capsula)", ""]
    rr, ins, gh, pie = calc["riel"], calc["insertos"], calc["gancho"], calc["pie"]
    L += [f"- **Riel en los ganchos (en el agua):** M = F·|x_capsula − {R_RING:g}| = {rr['M']:.0f} N·mm; seccion en x = {rr['x_sec']:.0f}: "
          f"I = {rr['I']:.0f} mm⁴, c = {rr['c']:.1f}; σ = {rr['sigma']:.1f} MPa → FS {rr['fs']:.1f} / {rr['fs_z']:.1f} entre capas.",
          f"- **Brida del riel a la caja, izado por el asa:** M = {ins['M']:.0f} N·mm sobre 4 insertos M4 con {ins['arm']:.0f} de "
          f"brazo: **{ins['por_inserto']:.0f} N por inserto** (PB8). En el agua, sobre los ganchos: {calc['insertos_agua']:.0f} N.",
          f"- **Gancho en C (fusionado) con {P.HANDLING_LOAD_N:g} N** (la capsula cuelga junto a su gancho: uno solo lleva la carga):** σ = {gh['sigma']:.1f} MPa → FS {gh['fs']:.1f} / {gh['fs_z']:.1f} entre capas.",
          f"- **Pie de la capsula:** M = {pie['M']:.0f} N·mm, {pie['por_m4']:.0f} N por M4 sobre las paredes de {W:g} del riel: "
          f"{pie['aplast']:.1f} MPa → FS {pie['fs']:.1f} / **{pie['fs_z']:.1f}** entre capas "
          + ("(cumple FS ≥ 2 sin inserto ni pared de 6: la capsula mirando adentro queda bajo la silla y la palanca es corta)."
             if pie["fs_z"] >= 2 else "(NO llega a FS 2 entre capas)."), "",
          "## 6. Cable", "",
          f"Por camara: {P.CABLE_ALLOW['caja']:g} + {P.CABLE_ALLOW['prensaestopas']:g} + conducto {cab['rail']:.0f} (recto, sin curva) + "
          f"bucle {cab['loop']:.0f} + {P.CABLE_ALLOW['capsula']:g} + {P.CABLE_ALLOW['holgura']:g} = **{cab['total']:.0f} mm** "
          f"({'requiere prueba SPI a 8 y 4 MHz' if cab['spi'] else 'alcanza el cable de fabrica de 300'}).", "",
          "## 7. Chequeos que fallaron", ""] + ([f"- {x}" for x in fails] if fails else ["- ninguno"])
    L += ["", "## 7b. Avisos (no hacen fallar el build)", ""] + ([f"- {x}" for x in warns] if warns else ["- ninguno"])
    L += ["", "## 8. Constantes de modulo", "",
          f"- `PAD_BORE` = {PAD_BORE:g}: agujero del cojin para la llave de vaso del PG7. `POCKET_END` = {POCKET_END:g}: "
          f"paredes extremas de los bolsillos con los insertos M3 de M3t. `TIP_HOLE` = {TIP_HOLE:g}: salida del cable en la punta. "
          f"`HOOK_CLR` = {HOOK_CLR:g}: aire entre el gancho y la capsula.",
          f"- Tiempo de `simple.py`: {secs:.0f} s."]
    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
