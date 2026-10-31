"""Fase G: boya de superficie B1..B6. Casco seco central dimensionado desde el layout (PCB, Waveshare, portabaterias,
RTC, codo del umbilical), tapa con junta, soporte del panel elevado, mastil de antena, flotadores modulares con espuma
y ojal de amarre independiente del umbilical. Calcula hidrostatica (calado, francobordo, GM) y escribe
cad_final/reporte_boya.md y salida/boya/.

    python boya.py            (desde cad_final/)
Marco: X a lo largo del casco, centrado en x = y = 0, fondo exterior del casco en z = 0.
"""
import math
import sys
from pathlib import Path
from types import SimpleNamespace

import cadquery as cq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import caja_central as C  # noqa: E402
import params as P  # noqa: E402
from checks import brep_check, export_part, mesh_checks, min_thickness, sanitize  # noqa: E402
from fase_a import mass_g  # noqa: E402
from render import render  # noqa: E402

OUT = HERE.parent / "salida" / "boya"
STL, STEP = OUT / "stl", OUT / "step"
RHO = P.SEAWATER_DENSITY * 1e-3            # g/mm3
ORIENTS = {"sin girar": None, "X180": ("X", 180), "X+90": ("X", 90), "Y+90": ("Y", 90)}


def box(x0, x1, y0, y1, z0, z1):
    return C._box(x0, x1, y0, y1, z0, z1)


def cyl(x, y, z0, h, d):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d / 2).extrude(h)


# ------------------------------------------------------------------ layout derivado
def make_layout():
    g = SimpleNamespace()
    pcb_x, pcb_y, pcb_t = P.BUOY_PCB
    ws_x, ws_y, ws_t = P.BUOY_WAVESHARE
    bat_x, bat_y, bat_h = P.BUOY_BATT_HOLDER
    rtc_x, rtc_y, rtc_h = P.BUOY_RTC
    g.cd = P.UMBILICAL[0]
    g.r_bend = max(P.CABLE_BEND_R_MIN, P.CABLE_BEND_K * g.cd)
    edge, gap = P.BUOY_TRAY_EDGE, P.BUOY_COMP_GAP
    gland_rel = P.GAP_WALL + P.nut_corner_r() + P.BUOY_UMB_MARGIN
    zone = gland_rel + g.r_bend + g.cd / 2 + P.BUOY_CABLE_CLEAR
    col_w = max(ws_x, rtc_x)
    tray_len = 2 * edge + pcb_x + gap + col_w
    g.L = float(math.ceil(zone + tray_len + P.GAP_WALL))
    g.W = float(math.ceil(max(pcb_y + 2 * edge + 2 * P.GAP_WALL,
                              bat_y + 2 * (P.BUOY_POST_D + P.BUOY_POST_WALL_GAP + 0.5))))
    g.zf = P.BOX_FLOOR
    g.z_bat0 = g.zf + P.BUOY_BATT_STANDOFF
    g.z_bat1 = g.z_bat0 + bat_h
    g.tray_bot = g.z_bat1 + P.BUOY_TRAY_GAP
    g.tray_top = g.tray_bot + P.TRAY_T
    g.top_h = max(P.BUOY_TOP_COMP_H, rtc_h, ws_t)
    g.out_h = g.tray_top + g.top_h + P.BOX_LID_GAP
    g.H = g.out_h - g.zf
    g.out_l, g.out_w = g.L + 2 * P.BOX_WALL, g.W + 2 * P.BOX_WALL
    g.lid_top = g.out_h + P.BOX_LID_T
    x_lo = -g.L / 2
    g.gx = x_lo + gland_rel
    g.tray_x0 = x_lo + zone
    g.tray_x1 = g.tray_x0 + tray_len
    g.tray_hy = g.W / 2 - P.GAP_WALL
    g.pcb_x0 = g.tray_x0 + edge
    g.col_x0 = g.pcb_x0 + pcb_x + gap
    g.col_w = col_w
    tot = ws_y + gap + rtc_y
    assert tot <= 2 * g.tray_hy, "columna WS + RTC no cabe en la bandeja"
    g.ws = (g.col_x0 + (col_w - ws_x) / 2, -tot / 2)
    g.rtc = (g.col_x0 + (col_w - rtc_x) / 2, -tot / 2 + ws_y + gap)
    g.post_y = g.W / 2 - P.BUOY_POST_WALL_GAP - P.BUOY_POST_D / 2
    g.post_pts = [(sx, sy * g.post_y) for sx in (g.tray_x0 + 5.0, g.tray_x1 - 5.0) for sy in (1, -1)]
    g.holder_pts = [(sx * P.BUOY_HOLDER_HOLES[0] / 2, sy * P.BUOY_HOLDER_HOLES[1] / 2) for sx in (1, -1) for sy in (1, -1)]
    g.z_cable_end = g.tray_top + g.cd / 2 + P.BUOY_CABLE_CLEAR
    g.z_nut = g.zf + P.PG7_INNER_H
    g.arc_cz = g.z_cable_end - g.r_bend
    assert g.arc_cz >= g.z_nut, "el codo del umbilical no cabe bajo la bandeja"

    class Stub:
        def box_outer(s):
            return g.out_l, g.out_w, g.out_h
    g.screws = C.screw_pts(Stub())
    xs = sorted({x for x, y in g.screws if abs(y) > 1e-6})
    g.rail_x, g.edge_x = xs[-2], xs[-1]
    g.leg_y = max(y for x, y in g.screws)
    g.lid_hx = g.out_l / 2 + P.BOX_FLANGE
    g.lid_hy = g.out_w / 2 + P.BOX_FLANGE
    g.y_in = g.out_w / 2 + P.BUOY_FLOAT_GAP
    g.ear_hole_y = g.out_w / 2 + P.BUOY_EAR[0] - P.BUOY_EAR_HOLE_TIP
    g.eye_hole_x = g.out_l / 2 + P.BUOY_EAR[0] - P.BUOY_EAR_HOLE_TIP
    g.panel_z0 = g.lid_top + P.BUOY_PANEL_LIFT_USED + P.BUOY_RAIL[2]
    return g


# ------------------------------------------------------------------ B1 casco, B1b bandeja, B2 tapa
def body_solid(g, ears=True):
    ol, ow, oh = g.out_l, g.out_w, g.out_h
    body = cq.Workplane("XY").rect(ol, ow).extrude(oh).edges("|Z").fillet(5)
    flange = (cq.Workplane("XY").workplane(offset=oh - P.BOX_FLANGE_T)
              .rect(ol + 2 * P.BOX_FLANGE, ow + 2 * P.BOX_FLANGE).extrude(P.BOX_FLANGE_T).edges("|Z").fillet(6))
    z_sk = oh - P.BOX_FLANGE_T
    s0 = cq.Sketch().rect(ol, ow).vertices().fillet(5)
    s1 = cq.Sketch().rect(ol + 2 * P.BOX_FLANGE, ow + 2 * P.BOX_FLANGE).vertices().fillet(6)
    skirt = (cq.Workplane("XY").workplane(offset=z_sk - P.BOX_FLANGE)
             .placeSketch(s0, s1.moved(cq.Location(cq.Vector(0, 0, P.BOX_FLANGE)))).loft())
    out = body.union(flange).union(skirt)
    if ears:
        el, ew, et = P.BUOY_EAR
        for sx in (1, -1):
            for sy in (1, -1):
                y0, y1 = sorted((sy * (ow / 2 - 1), sy * (ow / 2 + el)))
                out = out.union(box(sx * P.BUOY_EAR_X - ew / 2, sx * P.BUOY_EAR_X + ew / 2, y0, y1, 0, et)
                                .edges("|Z").fillet(2))
        out = out.union(box(ol / 2 - 1, ol / 2 + el, -P.BUOY_EYE_EAR_W / 2, P.BUOY_EYE_EAR_W / 2, 0, et)
                        .edges("|Z").fillet(2))
    return out


def lid_plate(g):
    return (cq.Workplane("XY").workplane(offset=g.out_h)
            .rect(g.out_l + 2 * P.BOX_FLANGE, g.out_w + 2 * P.BOX_FLANGE).extrude(P.BOX_LID_T).edges("|Z").fillet(6))


def m5_hole_with_nut(wp, x, y, et):
    wp = wp.cut(cyl(x, y, 0, et, P.BUOY_M5[0]))
    return wp.cut(C._hex(x, y, P.BUOY_M5[1], 0, P.BUOY_M5[2]))


def b1_casco(g):
    body = body_solid(g)
    cav = (cq.Workplane("XY").workplane(offset=g.zf).rect(g.L, g.W).extrude(g.H).edges("|Z").fillet(3))
    body = body.cut(cav)
    for (x, y) in g.screws:
        body = body.cut(cyl(x, y, g.out_h - P.M3_INSERT_DEPTH, P.M3_INSERT_DEPTH, P.M3_INSERT_HOLE))
    body = body.cut(cyl(g.gx, 0, 0, P.BOX_FLOOR, P.PG7_HOLE))
    yw, zw = P.BUOY_SOLAR_GLAND
    body = body.cut(cq.Workplane("YZ").workplane(offset=-g.out_l / 2 - 1).center(yw, zw)
                    .circle(P.PG7_HOLE / 2).extrude(P.BOX_WALL + 2))
    for (x, y) in g.holder_pts:
        body = body.union(cyl(x, y, g.zf, P.BUOY_BATT_STANDOFF, P.BUOY_POST_D))
        body = body.cut(cyl(x, y, g.z_bat0 - P.M3_INSERT_DEPTH, P.M3_INSERT_DEPTH, P.M3_INSERT_HOLE))
    for (x, y) in g.post_pts:
        body = body.union(cyl(x, y, g.zf, g.tray_bot - g.zf, P.BUOY_POST_D))
        body = body.cut(cyl(x, y, g.tray_bot - P.M3_INSERT_DEPTH, P.M3_INSERT_DEPTH, P.M3_INSERT_HOLE))
    et = P.BUOY_EAR[2]
    for sx in (1, -1):
        for sy in (1, -1):
            body = m5_hole_with_nut(body, sx * P.BUOY_EAR_X, sy * g.ear_hole_y, et)
    body = m5_hole_with_nut(body, g.eye_hole_x, 0, et)
    return body


def b1b_bandeja(g):
    t = box(g.tray_x0, g.tray_x1, -g.tray_hy, g.tray_hy, g.tray_bot, g.tray_top).edges("|Z").fillet(2)
    for (x, y) in g.post_pts:
        t = t.cut(cyl(x, y, g.tray_bot, P.TRAY_T, P.M3_CLEAR))
    return t


def b2_tapa(g):
    L, W = g.L, g.W
    z0 = g.out_h
    lid = lid_plate(g)
    for (x, y) in g.screws:
        lid = lid.cut(cyl(x, y, z0, P.BOX_LID_T, P.M3_CLEAR))
    cl_l = (L + g.out_l + P.BOX_FLANGE) / 2
    cl_w = (W + g.out_w + P.BOX_FLANGE) / 2
    outer = (cq.Workplane("XY").workplane(offset=z0).rect(cl_l + P.GROOVE_WIDTH, cl_w + P.GROOVE_WIDTH)
             .extrude(P.GROOVE_DEPTH).edges("|Z").fillet(6))
    inner = (cq.Workplane("XY").workplane(offset=z0).rect(cl_l - P.GROOVE_WIDTH, cl_w - P.GROOVE_WIDTH)
             .extrude(P.GROOVE_DEPTH).edges("|Z").fillet(3.5))
    return lid.cut(outer.cut(inner))


# ------------------------------------------------------------------ B3 larguero del panel (x2)
def b3_larguero(g):
    rw, rl, rt = P.BUOY_RAIL
    lift = P.BUOY_PANEL_LIFT_USED
    r = box(-rw / 2, rw / 2, -rl / 2, rl / 2, lift, lift + rt).edges("|Z").fillet(3)
    for sy in (1, -1):
        r = r.union(cyl(0, sy * g.leg_y, 0, lift + 1, P.BUOY_LEG_D))
    for sy in (1, -1):
        r = r.cut(cyl(0, sy * g.leg_y, 0, lift + rt, P.M3_CLEAR))
        r = r.cut(cyl(0, sy * g.leg_y, lift + rt - P.BUOY_CBORE[1], P.BUOY_CBORE[1], P.BUOY_CBORE[0]))
        r = r.cut(cyl(0, sy * P.BUOY_PANEL_HOLE_Y, lift + rt - P.M3_INSERT_DEPTH, P.M3_INSERT_DEPTH, P.M3_INSERT_HOLE))
    return r


# ------------------------------------------------------------------ B4 mastil de antena
def b4_mastil(g):
    pw, pt = P.BUOY_MAST_PLATE
    od, idd, h = P.BUOY_MAST
    ys = g.leg_y + 8.0
    plate = box(g.edge_x - 8.0, g.edge_x - 8.0 + pw, -ys, ys, 0, pt).edges("|Z").fillet(3)
    mx = g.edge_x + P.BUOY_MAST_OFFSET
    mast = cyl(mx, 0, 0, pt + h, od)
    m = plate.union(mast)
    if P.BUOY_SMA_BULKHEAD:
        m = m.cut(cyl(mx, 0, pt, h - 3.0, idd))
        m = m.cut(cyl(mx, 0, pt + h - 3.0, 3.0, P.BUOY_SMA_HOLE))
    else:
        m = m.cut(cyl(mx, 0, pt, h, idd))
    for (x, y) in g.screws:
        if abs(x - g.edge_x) < 1e-6:
            m = m.cut(cyl(x, y, 0, pt, P.M3_CLEAR))
    return m


# ------------------------------------------------------------------ B5 flotador (x4)
def float_outer():
    Lf, Wf, Hf = P.BUOY_FLOAT
    return box(0, Lf, 0, Wf, 0, Hf).edges("|Z").fillet(P.BUOY_FLOAT_R)


def b5_flotador():
    Lf, Wf, Hf = P.BUOY_FLOAT
    s, iw = P.BUOY_FLOAT_SHELL, P.BUOY_FLOAT_INNER_WALL
    hb = Hf - s
    tl, tw, tt = P.BUOY_TAB
    et = P.BUOY_EAR[2]
    o = box(0, Lf, 0, Wf, 0, hb).edges("|Z").fillet(P.BUOY_FLOAT_R)
    o = o.union(box(Lf / 2 - tw / 2, Lf / 2 + tw / 2, -tl, 1.0, et, et + tt))
    o = o.cut(box(s, Lf - s, iw, Wf - s, s, hb + 1).edges("|Z").fillet(P.BUOY_FLOAT_R - s))
    for hx in P.BUOY_TAB_HOLES:
        o = o.cut(cyl(hx, -tl + P.BUOY_EAR_HOLE_TIP, et, tt, P.BUOY_M5[0]))
    return o


def b5_tapa():
    Lf, Wf, Hf = P.BUOY_FLOAT
    s, iw = P.BUOY_FLOAT_SHELL, P.BUOY_FLOAT_INNER_WALL
    t = box(0, Lf, 0, Wf, 0, s).edges("|Z").fillet(P.BUOY_FLOAT_R)
    return t.cut(cyl(Lf / 2, (iw + Wf - s) / 2, 0, s, P.BUOY_FLOAT_PORT))


def float_cavity_cm3():
    Lf, Wf, Hf = P.BUOY_FLOAT
    s, iw = P.BUOY_FLOAT_SHELL, P.BUOY_FLOAT_INNER_WALL
    return (Lf - 2 * s) * (Wf - s - iw) * (Hf - 2 * s) / 1000.0


# ------------------------------------------------------------------ B6 ojal de amarre
def b6_ojal():
    od, idd, t, d = P.BUOY_EYE
    w = P.BUOY_EYE_EAR_W
    pad = cq.Workplane("XY").center(d / 4, 0).rect(d / 2 + w / 2, w).extrude(t).edges("|Z").fillet(3)
    neck = cq.Workplane("XY").center(d * 0.6, 0).rect(d * 0.6, od * 0.6).extrude(t)
    ring = cq.Workplane("XY").center(d, 0).circle(od / 2).extrude(t)
    e = pad.union(neck).union(ring)
    e = e.cut(cyl(d, 0, 0, t, idd))
    return e.cut(cyl(0, 0, 0, t, P.BUOY_M5[0]))


# ------------------------------------------------------------------ dummies
def dummies(g):
    bx, by, bh = P.BUOY_BATT_HOLDER
    px, py, pt = P.BUOY_PCB
    wx, wy, wt = P.BUOY_WAVESHARE
    rx, ry, rh = P.BUOY_RTC
    d = {"bateria": box(-bx / 2, bx / 2, -by / 2, by / 2, g.z_bat0, g.z_bat1),
         "pcb": box(g.pcb_x0, g.pcb_x0 + px, -py / 2, py / 2, g.tray_top, g.tray_top + pt),
         "pcb_zona": box(g.pcb_x0, g.pcb_x0 + px, -py / 2, py / 2, g.tray_top, g.tray_top + g.top_h),
         "waveshare": box(g.ws[0], g.ws[0] + wx, g.ws[1], g.ws[1] + wy, g.tray_top, g.tray_top + wt),
         "rtc": box(g.rtc[0], g.rtc[0] + rx, g.rtc[1], g.rtc[1] + ry, g.tray_top, g.tray_top + rh)}
    return d


def cable_solid(g):
    r, cx = g.r_bend, g.gx + g.r_bend
    x_end = g.pcb_x0 - 0.5
    a = math.radians(45)
    path = (cq.Workplane("XZ").moveTo(g.gx, g.z_nut).lineTo(g.gx, g.arc_cz)
            .threePointArc((cx - r * math.cos(a), g.arc_cz + r * math.sin(a)), (cx, g.z_cable_end))
            .lineTo(x_end, g.z_cable_end))
    return cq.Workplane("XY", origin=(g.gx, 0, g.z_nut)).circle(g.cd / 2).sweep(path)


# ------------------------------------------------------------------ piece processing
def process(name, stem, wp, qty=1):
    shape = sanitize(wp)
    chk = brep_check(shape)
    export_part(shape, stem, STL, STEP)
    path = STL / f"{stem}.stl"
    best = None
    for on, ori in ORIENTS.items():
        mc = mesh_checks(str(path), P.PRINT_BED, ori)
        if mc["fits_bed"] and (best is None or mc["overhang_mm2"] < best[1]["overhang_mm2"]):
            best = (on, mc)
    if best is None:
        on, mc = "no cabe", mesh_checks(str(path), P.PRINT_BED, None)
    else:
        on, mc = best
    p1, pmin = min_thickness(str(path))
    return dict(name=name, stem=stem, shape=shape, chk=chk, orient=on, mc=mc, p1=p1, pmin=pmin, qty=qty,
                vol=shape.Volume() / 1000.0)


def vol(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception:
        return float("nan")


# ------------------------------------------------------------------ hidrostatica
def immersed(envs, T):
    cutter = cq.Solid.makeBox(4000, 4000, T + 100, pnt=cq.Vector(-2000, -2000, -100))
    V, mz = 0.0, 0.0
    for e in envs:
        i = e.intersect(cutter)
        v = i.Volume()
        if v > 1e-6:
            V += v
            mz += v * i.Center().z
    return V, (mz / V if V else 0.0)


def solve_draft(envs, mass_g_total, T_max):
    lo, hi = 0.0, T_max
    for _ in range(40):
        mid = (lo + hi) / 2
        if immersed(envs, mid)[0] * RHO < mass_g_total:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def waterplane(rects):
    """rects = [(cx, cy, dx, dy)] -> area, Ix (sobre el eje X: integral y2 dA), Iy, ambos por el centroide."""
    A = sum(dx * dy for _, _, dx, dy in rects)
    xc = sum(cx * dx * dy for cx, _, dx, dy in rects) / A
    yc = sum(cy * dx * dy for _, cy, dx, dy in rects) / A
    Ix = sum(dx * dy ** 3 / 12 + dx * dy * (cy - yc) ** 2 for _, cy, dx, dy in rects)
    Iy = sum(dy * dx ** 3 / 12 + dx * dy * (cx - xc) ** 2 for cx, _, dx, dy in rects)
    return A, Ix, Iy


def main():
    STL.mkdir(parents=True, exist_ok=True)
    STEP.mkdir(parents=True, exist_ok=True)
    g = make_layout()
    print(f"cavidad {g.L:g} x {g.W:g} x {g.H:g}; casco {g.out_l:g} x {g.out_w:g} x {g.out_h:g}; tapa sup z={g.lid_top:g}")

    rows = []
    for name, stem, fn, q in (("B1 casco central", "B1_casco_central", lambda: b1_casco(g), 1),
                              ("B1b bandeja", "B1b_bandeja", lambda: b1b_bandeja(g), 1),
                              ("B2 tapa", "B2_tapa", lambda: b2_tapa(g), 1),
                              ("B3 larguero del panel", "B3_larguero_panel", lambda: b3_larguero(g), 2),
                              ("B4 mastil de antena", "B4_mastil_antena", lambda: b4_mastil(g), 1),
                              ("B5 flotador (cuerpo)", "B5_flotador", b5_flotador, 4),
                              ("B5b tapa del flotador", "B5b_tapa_flotador", b5_tapa, 4),
                              ("B6 ojal de amarre", "B6_ojal_amarre", b6_ojal, 1)):
        print("construyendo", name, flush=True)
        r = process(name, stem, fn(), q)
        rows.append(r)
        print(f"  ok={r['chk']['ok']} {r['chk']} wt={r['mc']['watertight']} bodies={r['mc']['bodies']} or={r['orient']} "
              f"bbox={tuple(round(v, 1) for v in r['mc']['bbox'])} fits={r['mc']['fits_bed']} "
              f"ov={r['mc']['overhang_mm2']:.0f} p1={r['p1']:.2f} min={r['pmin']:.2f}", flush=True)
    R = {r["stem"]: r for r in rows}
    hull, tray, lid, rail, mast, flt, eye, flid = (R[s]["shape"] for s in (
        "B1_casco_central", "B1b_bandeja", "B2_tapa", "B3_larguero_panel", "B4_mastil_antena", "B5_flotador",
        "B6_ojal_amarre", "B5b_tapa_flotador"))

    # ---- colocacion en el ensamble
    def put(s, x=0.0, y=0.0, z=0.0, rot=0.0):
        if rot:
            s = s.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), rot)
        return s.moved(cq.Location(cq.Vector(x, y, z)))

    Lf = P.BUOY_FLOAT[0]
    floats, f_env, f_lids = [], [], []
    zl = P.BUOY_FLOAT[2] - P.BUOY_FLOAT_SHELL
    fo = sanitize(float_outer())
    for sx in (1, -1):
        x0 = 0.0 if sx > 0 else -Lf
        floats.append(put(flt, x0, g.y_in, 0))
        f_lids.append(put(flid, x0, g.y_in, zl))
        f_env.append(put(fo, x0, g.y_in, 0))
        floats.append(put(flt, x0 + Lf, -g.y_in, 0, 180))
        f_lids.append(put(flid, x0 + Lf, -g.y_in, zl, 180))
        f_env.append(put(fo, x0 + Lf, -g.y_in, 0, 180))
    rails = [put(rail, sx * g.rail_x, 0, g.lid_top) for sx in (1, -1)]
    mast_p = put(mast, 0, 0, g.lid_top)
    eye_p = put(eye, g.eye_hole_x, 0, P.BUOY_EAR[2])
    panel = box(-P.BUOY_PANEL[0] / 2, P.BUOY_PANEL[0] / 2, -P.BUOY_PANEL[1] / 2, P.BUOY_PANEL[1] / 2,
                g.panel_z0, g.panel_z0 + P.BUOY_PANEL[2]).val()
    dm = {k: v.val() for k, v in dummies(g).items()}
    try:
        cable = sanitize(cable_solid(g))
    except Exception as ex:
        print("cable: fallo", ex)
        cable = None

    # ---- interferencias
    pairs = [("casco-flotadores", hull, floats + f_lids), ("casco-bandeja", hull, [tray]), ("casco-tapa", hull, [lid]),
             ("casco-bateria", hull, [dm["bateria"]]), ("casco-pcb zona", hull, [dm["pcb_zona"]]),
             ("casco-waveshare", hull, [dm["waveshare"]]), ("casco-rtc", hull, [dm["rtc"]]),
             ("bandeja-bateria", tray, [dm["bateria"]]), ("tapa-pcb zona", lid, [dm["pcb_zona"]]),
             ("pcb zona-waveshare", dm["pcb_zona"], [dm["waveshare"], dm["rtc"]]),
             ("waveshare-rtc", dm["waveshare"], [dm["rtc"]]),
             ("tapa-largueros", lid, rails), ("tapa-mastil", lid, [mast_p]), ("panel-mastil", panel, [mast_p]),
             ("panel-largueros", panel, rails), ("panel-flotadores", panel, floats), ("panel-casco", panel, [hull, lid]),
             ("flotadores-largueros", floats[0], rails), ("ojal-casco", eye_p, [hull]),
             ("ojal-flotadores", eye_p, floats + f_lids), ("flotador-flotador", floats[0], floats[1:]),
             ("flotador-tapa de otro", floats[0], f_lids[1:]), ("tapa flotador-panel", panel, f_lids)]
    if cable is not None:
        pairs += [("cable-casco", cable, [hull]), ("cable-bandeja", cable, [tray]), ("cable-bateria", cable, [dm["bateria"]]),
                  ("cable-pcb", cable, [dm["pcb"]]), ("cable-tapa", cable, [lid])]
    interf = {}
    for nm, a, bs in pairs:
        interf[nm] = sum(vol(a, b) for b in bs)
    bad = {k: v for k, v in interf.items() if not (v <= P.INTERF_TOL)}
    print("interferencias > tol:", bad or "ninguna", flush=True)

    # ---- masas
    dens = P.PETG_DENSITY
    def pm(s, infill=1.0):
        return mass_g(s, infill)
    printed = [("B1 casco (100 %)", pm(hull), 1, hull), ("B1b bandeja", pm(tray), 1, tray), ("B2 tapa (100 %)", pm(lid), 1, lid),
               ("B3 larguero", pm(rail), 2, rail), ("B4 mastil+placa", pm(mast), 1, mast),
               ("B5 flotador (cuerpo)", dens * flt.Volume() / 1000.0, 4, flt),
               ("B5b tapa del flotador", dens * flid.Volume() / 1000.0, 4, flid), ("B6 ojal", pm(eye), 1, eye)]
    printed_40 = {"B1b bandeja": pm(tray, P.INFILL_CASES[0]), "B3 larguero": pm(rail, P.INFILL_CASES[0]),
                  "B4 mastil+placa": pm(mast, P.INFILL_CASES[0]), "B6 ojal": pm(eye, P.INFILL_CASES[0])}
    foam_g = P.BUOY_FOAM_DENSITY * float_cavity_cm3() * 4
    M = P.BUOY_MASS
    comp = [("3 x celdas 18650", P.BUOY_CELLS * M["celda_18650"], "estimado", (0, 0, (g.z_bat0 + g.z_bat1) / 2)),
            ("portabaterias", M["portabaterias"], "estimado", (0, 0, (g.z_bat0 + g.z_bat1) / 2)),
            ("PCB + Heltec", M["pcb_heltec"], "estimado", (g.pcb_x0 + P.BUOY_PCB[0] / 2, 0, g.tray_top + g.top_h / 3)),
            ("Waveshare D", M["waveshare"], "estimado", (g.ws[0] + 22, g.ws[1] + 20, g.tray_top + 5)),
            ("RTC DS3231", M["rtc"], "estimado", (g.rtc[0] + 20, g.rtc[1] + 12, g.tray_top + 7)),
            ("panel solar 5 W", M["panel"], "estimado", (0, 0, g.panel_z0 + P.BUOY_PANEL[2] / 2)),
            ("antena LoRa", M["antena"], "estimado", (g.edge_x + P.BUOY_MAST_OFFSET, 0,
                                                       g.lid_top + P.BUOY_MAST_PLATE[1] + P.BUOY_MAST[2] + P.BUOY_ANTENNA_L / 2)),
            ("cables, fusible, conectores", M["cables_fusible"], "estimado", (g.tray_x0 + 40, 0, g.tray_top + 8)),
            ("2 x PG7", M["prensaestopas"], "estimado", (-g.L / 2 + 10, 0, 30.0)),
            ("tornilleria e insertos", M["tornilleria"], "estimado", (0, 0, g.out_h / 2)),
            ("espuma de celda cerrada (4 flotadores)", foam_g, "estimado", None)]
    opt = [("pasamuros SMA (desactivado)", P.BUOY_SMA_G if P.BUOY_SMA_BULKHEAD else 0.0, "opcional",
            (g.edge_x + P.BUOY_MAST_OFFSET, 0, g.lid_top + P.BUOY_MAST[2]))]
    items = []
    for nm, m, q, sh in printed:
        c = sh.Center()
        items.append((nm, m * q, "calculado de la geometria (densidad PETG por verificar)", c.z))
    # cg de las piezas impresas en el ensamble
    printed_cg = {"B1 casco (100 %)": hull.Center().z, "B1b bandeja": tray.Center().z, "B2 tapa (100 %)": lid.Center().z,
                  "B3 larguero": sum(r.Center().z for r in rails) / 2, "B4 mastil+placa": mast_p.Center().z,
                  "B5 flotador (cuerpo)": sum(f.Center().z for f in floats) / 4,
                  "B5b tapa del flotador": sum(f.Center().z for f in f_lids) / 4, "B6 ojal": eye_p.Center().z}
    items = [(nm, m, k, printed_cg[nm]) for nm, m, k, _ in items]
    foam_z = sum(f.Center().z for f in floats) / 4
    for nm, m, q, pos in comp + opt:
        items.append((nm, m, q, foam_z if pos is None else pos[2]))
    M_tot = sum(m for _, m, _, _ in items)
    KG = sum(m * z for _, m, _, z in items) / M_tot
    save40 = sum(printed[i][1] * printed[i][2] - printed_40[printed[i][0]] * printed[i][2]
                 for i in range(len(printed)) if printed[i][0] in printed_40)
    print(f"masa total {M_tot:.0f} g, KG {KG:.1f} mm", flush=True)

    # ---- hidrostatica
    hull_env = sanitize(body_solid(g).union(lid_plate(g)))
    envs = [hull_env] + f_env
    T = solve_draft(envs, M_tot, g.lid_top)
    V, KB = immersed(envs, T)
    free = g.lid_top - T
    T_free = g.lid_top - P.BUOY_FREEBOARD_MIN
    cap_g = RHO * immersed(envs, T_free)[0] - M_tot
    V_all = sum(e.Volume() for e in envs)
    reserve = (V_all - V) / V
    Lh, Wh = g.out_l, g.out_w
    Lf_, Wf_ = P.BUOY_FLOAT[0], P.BUOY_FLOAT[1]
    rects = [(0, 0, Lh, Wh)] + [(sx * Lf_ / 2, sy * (g.y_in + Wf_ / 2), Lf_, Wf_) for sx in (1, -1) for sy in (1, -1)]
    A_wp, Ixx, Iyy = waterplane(rects)
    dV = (immersed(envs, T + 1.0)[0] - immersed(envs, T - 1.0)[0]) / 2.0
    BM_roll, BM_pitch = Ixx / V, Iyy / V
    GM_roll, GM_pitch = KB + BM_roll - KG, KB + BM_pitch - KG
    T_light = solve_draft(envs, M_tot - save40, g.lid_top)
    # Escenario sin un flotador (perdido por completo, sin espuma): calado con 3 modulos, solo masa menos 1 modulo
    envs3 = [hull_env] + f_env[1:]
    m3 = M_tot - (dens * (flt.Volume() + flid.Volume()) / 1000.0 + foam_g / 4)
    T3 = solve_draft(envs3, m3, g.lid_top)
    print(f"calado {T:.1f}, francobordo {free:.1f}, KB {KB:.1f}, KG {KG:.1f}, GM roll {GM_roll:.0f}, pitch {GM_pitch:.0f}", flush=True)

    # ---- renders
    colors = {"hull": "#C9CCD1", "lid": "#5B8DB8", "tray": "#8FBC8F", "float": "#F2A33A", "rail": "#9B59B6",
              "mast": "#2E86C1", "eye": "#C0392B", "panel": "#1F3A5F"}
    items_iso = [(hull, colors["hull"], 1.0, True, None), (lid, colors["lid"], 1.0, True, None)]
    items_iso += [(f, colors["float"], 1.0, True, None) for f in floats + f_lids]
    items_iso += [(r, colors["rail"], 1.0, True, None) for r in rails]
    items_iso += [(mast_p, colors["mast"], 1.0, True, None), (eye_p, colors["eye"], 1.0, True, None),
                  (panel, colors["panel"], 0.75, True, None)]
    render(items_iso, OUT / "boya_iso.png", "iso_alto", "Boya de superficie: B1..B6 (panel de 170 x 170 elevado)")

    def half(s):
        cutter = cq.Workplane("XY").box(3000, 1500, 3000, centered=(True, False, True)).translate((0, -1500, 0))
        return cq.Workplane().add(s).cut(cutter).val()

    def keep(lst):
        return [t for t in lst if t[0].Volume() > 1e-6]

    cut_items = [(half(hull), colors["hull"], 1.0, True, None), (half(lid), colors["lid"], 0.5, True, None),
                 (half(tray), colors["tray"], 1.0, True, None),
                 (half(dm["bateria"]), "#F4D03F", 1.0, True, "3 x 18650"),
                 (half(dm["pcb_zona"]), "#16A085", 0.25, False, None), (half(dm["pcb"]), "#16A085", 1.0, True, "PCB"),
                 (half(dm["waveshare"]), "#E67E22", 1.0, True, "Waveshare D"), (half(dm["rtc"]), "#8E44AD", 1.0, True, "RTC")]
    if cable is not None:
        cut_items.append((half(cable), "#222222", 1.0, True, "umbilical R25"))
    cut_items += [(half(f), colors["float"], 1.0, True, None) for f in floats + f_lids]
    cut_items += [(half(r), colors["rail"], 1.0, True, None) for r in rails]
    cut_items += [(half(mast_p), colors["mast"], 1.0, True, None), (half(panel), colors["panel"], 0.75, True, "panel")]
    cut_items = keep(cut_items)
    render(cut_items, OUT / "boya_corte.png", "frontal", "Corte en y = 0: distribucion de modulos, codo del umbilical y flotadores")
    plan = [(hull, colors["hull"], 1.0, True, None), (tray, colors["tray"], 0.45, True, None),
            (dm["bateria"], "#F4D03F", 0.9, True, "3 x 18650 (bajo la bandeja)"), (dm["pcb"], "#16A085", 1.0, True, "PCB"),
            (dm["waveshare"], "#E67E22", 1.0, True, "Waveshare D"), (dm["rtc"], "#8E44AD", 1.0, True, "RTC")]
    if cable is not None:
        plan.append((cable, "#222222", 1.0, True, "umbilical"))
    plan += [(f, colors["float"], 1.0, True, None) for f in floats + f_lids] + [(eye_p, colors["eye"], 1.0, True, "ojal de amarre")]
    render(plan, OUT / "boya_planta.png", "superior", "Planta sin tapa ni panel")

    write_report(g, rows, items, M_tot, KG, T, V, KB, free, cap_g, reserve, A_wp, dV, Ixx, Iyy, BM_roll, BM_pitch,
                 GM_roll, GM_pitch, T_light, save40, T3, m3, interf, bad, foam_g, V_all)


def fm(v, n=1):
    return f"{v:.{n}f}"


def write_report(g, rows, items, M_tot, KG, T, V, KB, free, cap_g, reserve, A_wp, dV, Ixx, Iyy, BM_r, BM_p,
                 GM_r, GM_p, T_light, save40, T3, m3, interf, bad, foam_g, V_all):
    ok_free = free >= P.BUOY_FREEBOARD_MIN
    L = []
    a = L.append
    a("# Fase G: boya de superficie (B1..B6)\n")
    a("Generado por `cad_final/boya.py`. Todo numero sale de `params.py` o del modelo; lo que no esta medido va marcado "
      "como estimado. Esto es una estimacion de geometria, no una certificacion de flotacion ni de estabilidad en mar.\n")
    a("## Geometria derivada del layout\n")
    a(f"- Cavidad {g.L:g} x {g.W:g} x {g.H:g} mm (referencia del handoff: 220 x 200 x 120 exterior). Casco exterior "
      f"{g.out_l:g} x {g.out_w:g} x {g.out_h:g}; con brida {g.out_l + 2 * P.BOX_FLANGE:g} x {g.out_w + 2 * P.BOX_FLANGE:g}.")
    a(f"- Portabaterias {P.BUOY_BATT_HOLDER[0]:g} x {P.BUOY_BATT_HOLDER[1]:g} x {P.BUOY_BATT_HOLDER[2]:g} centrado en x = y = 0, "
      f"sobre 4 refuerzos M3 de {P.BUOY_BATT_STANDOFF:g} mm (z = {g.z_bat0:g}..{g.z_bat1:g}); bateria baja y asegurada.")
    a(f"- Bandeja B1b (z = {g.tray_bot:g}..{g.tray_top:g}) sobre 4 postes M3, con PCB {P.BUOY_PCB[0]:g} x {P.BUOY_PCB[1]:g} y, "
      f"en columna, Waveshare D y RTC. Altura libre sobre la bandeja {g.top_h:g} mm (estimada) + {P.BOX_LID_GAP:g} de aire.")
    a(f"- Umbilical: PG7 en el fondo en x = {g.gx:.1f}; codo de R{g.r_bend:g} (mayor entre el minimo del equipo y "
      f"{P.CABLE_BEND_K:g} x Ø{g.cd:g}) que sube a z = {g.z_cable_end:.1f}, apenas sobre la bandeja. Cable solar por PG7 en la pared -X "
      f"(y = {P.BUOY_SOLAR_GLAND[0]:g}, z = {P.BUOY_SOLAR_GLAND[1]:g}).")
    a(f"- Panel {P.BUOY_PANEL[0]:g} x {P.BUOY_PANEL[1]:g} x {P.BUOY_PANEL[2]:g} a {P.BUOY_PANEL_LIFT_USED:g} mm sobre la tapa "
      f"(rango del equipo {P.BUOY_PANEL_LIFT[0]:g}..{P.BUOY_PANEL_LIFT[1]:g}); sobresale del casco en Y. Los largueros B3 se apoyan en "
      f"4 de los tornillos M3 de la tapa, que se reemplazan por M3 largos: no perfora la tapa. Drenaje: sin bolsillos, patas "
      f"separadas, el agua de la tapa escurre libre.")
    a(f"- Plataforma: flotadores B5 en dos pontones de 2 modulos ({P.BUOY_FLOAT[0] * 2:g} mm) a cada lado, plataforma "
      f"{P.BUOY_FLOAT[0] * 2:g} x {2 * (g.y_in + P.BUOY_FLOAT[1]):g} mm (referencia inicial 320 x 300). Union casco-flotador: orejas "
      f"del casco + lenguetas del flotador + tornillo M5 inox con tuerca en bolsillo (4 uniones).")
    a(f"- Amarre: ojal B6 atornillado a la oreja del extremo +X del casco con un M5 propio; el umbilical sale por el fondo "
      f"en el extremo -X y no recibe tension.\n")
    a("## Piezas\n")
    a("| Pieza | Cant. | bbox en impresion (mm) | Cabe en cama | Orientacion | p1 (mm) | min (mm) | Voladizo > 45 (mm²) | Volumen (cm³) | BRep | STL cerrado, cuerpos |")
    a("|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        mc = r["mc"]
        a(f"| {r['name']} | {r['qty']} | {' x '.join(fm(v) for v in mc['bbox'])} | {'si' if mc['fits_bed'] else 'NO'} | "
          f"{r['orient']} | {fm(r['p1'], 2)} | {fm(r['pmin'], 2)} | {mc['overhang_mm2']:.0f} | {fm(r['vol'])} | "
          f"{'ok' if r['chk']['ok'] else 'FALLA'} | {'si' if mc['watertight'] else 'NO'}, {mc['bodies']} |")
    bad_p1 = [r["name"] for r in rows if r["p1"] < P.MIN_WALL]
    a(f"\nCriterio p1 >= {P.MIN_WALL:g}: " + ("todas cumplen." if not bad_p1 else "NO cumplen: " + ", ".join(bad_p1) + "."))
    big = [r["name"] for r in rows if max(r["mc"]["bbox"]) > P.PIECE_MAX_L]
    a(f"Piezas con una dimension > {P.PIECE_MAX_L:g} (limite de pieza del equipo): {', '.join(big) or 'ninguna'}. "
      f"B1 y B2 son el casco/tapa (excepcion admitida); cabida en la cama real {P.PRINT_BED[0]:g} x {P.PRINT_BED[1]:g} x {P.PRINT_BED[2]:g} "
      f"(por verificar) se evalua arriba.")
    a("Notas de impresion: B1 y B2 y todas las piezas macizas al 100 % de relleno y 5 perimetros; B5 son cuerpo abierto + tapa B5b de 1.6 mm "
      "(4 perimetros): se llena de espuma y se cierra pegando la tapa (o con la boca de Ø10 de la tapa, que se sella); la lengüeta de B5 sale en voladizo de 19 mm "
      "(puente o soporte local, ver columna de voladizo). B3 se imprime con las patas hacia arriba (girada 180° sobre X).\n")
    a("## Interferencias en el ensamble (volumen comun, mm³)\n")
    a("| Par | Volumen |")
    a("|---|---|")
    for k, v in interf.items():
        a(f"| {k} | {v:.3f} |")
    a(f"\nTolerancia {P.INTERF_TOL:g} mm³: " + ("sin interferencias." if not bad else
      "INTERFIEREN: " + ", ".join(f"{k} ({v:.2f})" for k, v in bad.items())) + "\n")
    a("## Masa total\n")
    a("| Elemento | Masa (g) | Origen | CG z (mm) |")
    a("|---|---|---|---|")
    for nm, m, k, z in items:
        a(f"| {nm} | {m:.1f} | {k} | {z:.1f} |")
    a(f"| **Total** | **{M_tot:.0f}** | | KG = {KG:.1f} |")
    a(f"\nNada de esto esta confirmado por pesaje: las piezas impresas salen del volumen del modelo por la densidad del PETG "
      f"({P.PETG_DENSITY:g} g/cm³, por verificar) con 100 % de relleno (conservador); los componentes son masas tipicas "
      f"(`boya.masas`, estimadas) y el panel es la mayor incertidumbre ({P.BUOY_MASS['panel']:g} g). Con B1b, B3, B4 y B6 al "
      f"{P.INFILL_CASES[0] * 100:.0f} % la masa baja {save40:.0f} g.\n")
    a("## Hidrostatica (agua de mar 1025 kg/m³)\n")
    a("Metodo: el calado T se resuelve por biseccion sobre el volumen sumergido real (interseccion BRep de los solidos "
      "envolventes casco+tapa y 4 flotadores con el semiespacio z <= T) hasta que ρ·V(T) = masa total. "
      "Formulas: `KB` = z del centroide del volumen sumergido; `BM = I_wp / V`; `GM = KB + BM − KG`; "
      "I_wp del plano de flotacion como suma de rectangulos (casco y 4 flotadores, esquinas redondeadas ignoradas, "
      "sobreestima poco); `KG` = suma(m·z)/suma(m) con las posiciones de la tabla.\n")
    a("| Magnitud | Valor |")
    a("|---|---|")
    a(f"| Masa total M | {M_tot:.0f} g |")
    a(f"| Desplazamiento necesario V = M / ρ | {M_tot / (RHO * 1000):.1f} cm³ |")
    a(f"| Calado T (desde el fondo del casco) | {T:.1f} mm |")
    a(f"| Francobordo (tapa, T hasta z = {g.lid_top:g}) | {free:.1f} mm (minimo {P.BUOY_FREEBOARD_MIN:g}): **{'CUMPLE' if ok_free else 'NO CUMPLE'}** |")
    a(f"| Francobordo de los flotadores (alto {P.BUOY_FLOAT[2]:g}) | {P.BUOY_FLOAT[2] - T:.1f} mm |")
    a(f"| Area del plano de flotacion (rectangulos) | {A_wp:.0f} mm² (dV/dT numerico: {dV:.0f} mm²) |")
    a(f"| Carga util extra con francobordo >= {P.BUOY_FREEBOARD_MIN:g} | {cap_g:.0f} g |")
    a(f"| Reserva de flotacion (V sellado total − V sumergido) / V sumergido | {reserve * 100:.0f} % |")
    a(f"| KB | {KB:.1f} mm |")
    a(f"| KG | {KG:.1f} mm |")
    a(f"| I_wp alrededor del eje X (balanceo) / Y (cabeceo) | {Ixx:.3e} / {Iyy:.3e} mm⁴ |")
    a(f"| BM balanceo / cabeceo | {BM_r:.0f} / {BM_p:.0f} mm |")
    a(f"| **GM balanceo / cabeceo** | **{GM_r:.0f} / {GM_p:.0f} mm** |")
    a(f"| Calado con rellenos al {P.INFILL_CASES[0] * 100:.0f} % en piezas no selladas | {T_light:.1f} mm |")
    a(f"| Calado perdiendo un flotador completo (3 modulos, masa {m3:.0f} g, sin escora) | {T3:.1f} mm |")
    a("")
    a("**Lectura.** " + (f"El francobordo cumple con {free - P.BUOY_FREEBOARD_MIN:.1f} mm de margen. " if ok_free else
      f"El francobordo NO cumple: faltan {P.BUOY_FREEBOARD_MIN - free:.1f} mm. ") +
      f"GM positivo y grande en los dos ejes indica estabilidad inicial alta para esta geometria de plataforma ancha; "
      f"no dice nada del comportamiento con oleaje.")
    a("\n**Supuestos y limites.**")
    a("- Si un flotador filtra, la espuma de celda cerrada mantiene la flotabilidad; se supone cero absorcion de agua de la espuma. "
      "La espuma no se modela como solido: su masa se suma como estimada y su cavidad es la de la cascara.")
    a("- Incertidumbres que solo una prueba real resuelve: oleaje y rolido dinamico, torsion que introduce el amarre en la oreja "
      "del extremo, tension y peso del umbilical (3 m, Ø6) sobre el fondo del casco, viento sobre el panel y el mastil, masa real "
      "del panel y de las celdas, y estanqueidad de las juntas de la tapa y de los PG7 (el del umbilical queda sumergido).")
    a("- Retencion de los largueros B3 y del mastil B4: dependen de tornillos M3 largos en los insertos de la brida (5.7 de "
      "rosca, sin perforar la tapa); la carga de viento no se calculo.")
    a("- La lengüeta del flotador y la oreja del casco trabajan a cortante de un M5 y a aplastamiento del PETG; no se calculo "
      "resistencia. El ojal de amarre transmite la tension al casco por la oreja del extremo.\n")
    a("## Cadena de potencia (solo texto)\n")
    a("Panel solar -> Waveshare Solar Power Manager D (carga las celdas 18650 y entrega 5 V regulados) -> 5 V al sistema "
      "(PCB / Heltec / RTC). Sin segunda regulacion: la PCB de la boya debe tomar los 5 V de la salida del Waveshare directamente, "
      "sin otro conversor intermedio ni regulador en serie sobre el mismo bus. Comprobarlo contra el esquematico fisico (los "
      "agujeros y el conexionado de la PCB fabricada estan por verificar); el panel de 5 W nominales no garantiza potencia para "
      "todas las cargas, sobre todo con la radio transmitiendo.\n")
    a("## Parametros agregados a params.py (bloque `# boya (Fase G)`)\n")
    orig = {"boya.pcb", "boya.waveshare_D", "boya.portabaterias", "boya.rtc_reserva", "boya.panel", "boya.panel_elevacion",
            "boya.francobordo_min"}
    a("| Clave | Valor | Origen | Estado |")
    a("|---|---|---|---|")
    for k, pr in P.REGISTRO.items():
        if k.startswith("boya.") and k not in orig:
            a(f"| {k} | {pr.value} | {pr.origen} | {pr.estado} |")
    a("\n## Renders\n")
    a("- `salida/boya/boya_iso.png`: ensamble.\n- `salida/boya/boya_corte.png`: corte en y = 0.\n- `salida/boya/boya_planta.png`: planta sin tapa.")
    a("\nSTL y STEP por pieza en `salida/boya/stl` y `salida/boya/step`.")
    (HERE / "reporte_boya.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("reporte escrito", flush=True)


if __name__ == "__main__":
    main()
