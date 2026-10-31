"""Buoy with sealed PET bottles + PU spray foam (block C of the CAD job); replaces the platform buoy of boya_simple.py.

    python boya_pet.py                       (from cad_final/) CAD + checks + OrcaSlicer + flotation + report
    python boya_pet.py --sin-slicer          reuse salida/boya_pet/slicer.json (or estimate masses if missing)
    python boya_pet.py --botella 500ml|1L|2L --cantidad 2     override flotacion.botella / flotacion.cantidad

Pieces (4 printed, all fit the 256 bed; the hull is NOT watertight, the bottles float it):
  B1_casco     open hull: end ribs + 3 mid ribs with U slots for the bottles (base end solid, neck end holds the neck),
               side walls with windows, floor skids, mooring pad at the keel centre (independent from the umbilical),
               M3 insert bosses for the cover.
  B2_cubierta  ladder of bars screwed on the hull (bottles cannot fall out; windows = foam injection), 4 pillars under
               the ears of the dry box, 4 panel columns (panel 25 mm over the lid), antenna mast with a pigtail port.
  B3_caja      dry box sized to PCB / Waveshare / 3 x 18650 holder / RTC + 5 mm, 3 PG7, ears on the pillars, gasket
               flange, tray posts, battery standoffs.
  B4_tapa      lid with the O-ring cord groove (printed groove up).
Frame: hull centre x = y = 0, hull bottom z = 0, X along the bottles. Seawater from agua.densidad.
Outputs: salida/boya_pet/ (step/, stl/, ENSAMBLE, iso + section png, resultados.json, slicer.json),
cad_final/reporte_boya_pet.md.
"""
import argparse
import json
import math
import shutil
import tempfile
from pathlib import Path

import cadquery as cq

import fase_a as FA
import params as P
from checks import brep_check, export_part, fix_step_stamp, mesh_checks, sanitize

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "boya_pet"
RHO = P.SEAWATER_DENSITY * 1e-3          # g/mm3
ORIENT = {"sin girar": None, "X180": ("X", 180), "X+90": ("X", 90), "Y+90": ("Y", 90)}
INFILL = {"B1": 0.4, "B2": 0.4, "B3": 0.4, "B4": 0.4}
SCREW_OFF = 7.2                           # M3 line of the flange from the outer wall
GROOVE_OFF = 2.8                          # O-ring groove centre line from the outer wall (on the flange)


def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def cyl(p, d, r, h):
    return cq.Workplane().add(cq.Solid.makeCylinder(r, h, cq.Vector(*p), cq.Vector(*d)))


def rbox(lx, ly, z0, h, r, x=0.0, y=0.0):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).rect(lx, ly).extrude(h).edges("|Z").fillet(r)


def diamond_x(x, y, z, r, t):
    """Diamond (45 degree faces: prints without a round bridge), prism along X through a rib."""
    a = r * 1.1
    pts = [(y + a, z), (y, z + a), (y - a, z), (y, z - a)]
    return cq.Workplane("YZ").workplane(offset=x - t).polyline(pts).close().extrude(2 * t)


def poly_prism_y(pts_xz, y0, y1):
    """Prism along Y with the polygon given in (x, z)."""
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts_xz).close().extrude(y1 - y0)


# ---------------------------------------------------------------- geometry
def dims(bottle, n):
    """Every derived dimension of the buoy for a bottle type and count (frame in the module docstring)."""
    b = P.FLOT_BOTTLES[bottle]
    D, Lb = b["D"], b["L"]
    r = D / 2
    wall, rib, clr, wc = P.PET_WALL, P.PET_RIB, P.FLOT_CLEAR, P.FLOT_CHANNEL
    d = dict(bottle=bottle, n=n, D=D, r=r, Lb=Lb, V=b["V"], neck_D=b["neck_D"], neck_len=b["neck_len"], m_bottle=b["m_g"], wall=wall, rib=rib, clr=clr, wc=wc)
    d["slot_w"] = D + 2 * clr
    d["yb"] = wc / 2 + wall + d["slot_w"] / 2
    d["WH"] = wc + 2 * (wall + d["slot_w"]) + 2 * wall
    d["LH"] = min(Lb - P.FLOT_NECK_OUT + 2 * rib, P.PET_HULL_MAX)
    d["zc"] = wall + clr + r
    d["z_top"] = d["zc"] + r + clr
    d["L1"] = d["LH"] / 4
    d["x_bot0"] = -d["LH"] / 2 + rib                    # base end of the bottles (touches the base rib)
    d["xc_bot"] = d["x_bot0"] + Lb / 2
    d["X0"] = d["xc_bot"]                                            # superstructure centred on the bottles: no trim
    tip = d["x_bot0"] + Lb
    xn = d["LH"] / 2 - rib / 2                                      # centre of the neck rib
    ns, sh = tip - b["neck_len"], 30.0
    if xn >= ns:
        rn = b["neck_D"] / 2
    elif xn >= ns - sh:
        rn = b["neck_D"] / 2 + (r - b["neck_D"] / 2) * (ns - xn) / sh        # on the conical shoulder
    else:
        rn = r
    d["neck_slot_r"] = min(r + clr, rn + 1.0)
    # dry box
    bl, bw, bh = P.BUOY_BATT_HOLDER
    pl, pw, _ = P.BUOY_PCB
    wl, ww, wh = P.BUOY_WAVESHARE
    rl, rw, rh = P.BUOY_RTC
    m, bwall = P.PET_BOX_MARGIN, P.PET_BOX_WALL
    d["Li"] = P.PET_GLAND_RES + bl + m + rl + 3.0                   # lower deck: gland | battery | RTC
    d["Wi"] = math.ceil(max(pw, bw) + 2 * m)
    d["Hi"] = P.BUOY_BATT_STANDOFF + bh + P.BUOY_TRAY_GAP + 3.0 + P.BUOY_TOP_COMP_H + m
    d["Lx"], d["Wy"] = d["Li"] + 2 * bwall, d["Wi"] + 2 * bwall
    d["HB"] = bwall + d["Hi"]
    d["pillar_h"] = P.PET_PILLAR[1]
    d["z_cover"] = d["z_top"]
    d["z_cover_top"] = d["z_top"] + P.PET_COVER_T
    d["z0"] = d["z_cover_top"] + d["pillar_h"]                      # box floor bottom
    d["z_lid"] = d["z0"] + d["HB"]
    d["z_lid_top"] = d["z_lid"] + P.PET_LID_T
    d["z_panel0"] = d["z_lid_top"] + P.PET_PANEL_LIFT
    d["z_panel1"] = d["z_panel0"] + P.BUOY_PANEL[2]
    d["z_mast"] = d["z_panel1"] + P.PET_MAST[2]
    d["x_mast"] = d["LH"] / 2 - P.PET_BAR_W / 2
    return d


def boss_y(d):
    """|y| of the cover bolts: just inside the channel fin so the boss is fused to it."""
    return d["wc"] / 2 - P.PET_BOSS


def boss_x(d, x):
    """x of the cover bolts: the end ribs sit at the edge, so the boss is pulled inside the hull length."""
    lim = d["LH"] / 2 - 4.0
    return max(-lim, min(lim, x))


def rib_x(d):
    """(x, kind) of the 5 ribs; the 4 with a cover bar carry the M3 bosses."""
    t = d["rib"]
    x0 = d["X0"]
    return [(-d["LH"] / 2 + t / 2, "base"), (x0 - d["L1"], "mid"), (x0, "mid0"), (x0 + d["L1"], "mid"), (d["LH"] / 2 - t / 2, "neck")]


def b1_casco(d):
    t, wall, r, clr, wc = d["rib"], d["wall"], d["r"], d["clr"], d["wc"]
    LH, WH, zt, zc, yb = d["LH"], d["WH"], d["z_top"], d["zc"], d["yb"]
    h = None
    for x, kind in rib_x(d):
        rb = box(x - t / 2, x + t / 2, -WH / 2, WH / 2, 0, zt)
        if kind == "base":
            for s in (1, -1):                                          # lightening ring behind each bottle base
                rb = rb.cut(diamond_x(x, s * yb, zc, 0.42 * d["D"], t))
            rb = rb.cut(box(x - t, x + t, -wc / 2, wc / 2, wall, zt + 1))     # umbilical leaves by the open channel
        else:
            for s in (1, -1):
                if kind == "neck":
                    rs, ws = d["neck_slot_r"], 2 * d["neck_slot_r"]
                else:
                    rs, ws = r + clr, d["slot_w"]
                rb = rb.cut(cyl((x - t, s * yb, zc), (1, 0, 0), rs, 2 * t)).cut(box(x - t, x + t, s * yb - ws / 2, s * yb + ws / 2, zc, zt + 1))
            rb = rb.cut(box(x - t, x + t, -wc / 2, wc / 2, wall, zt + 1))     # open channel (umbilical)
        h = rb if h is None else h.union(rb)
    for s in (1, -1):
        w = box(-LH / 2, LH / 2, s * (WH / 2 - wall) if s > 0 else -WH / 2, WH / 2 if s > 0 else -WH / 2 + wall, 0, zt)
        xs = [x for x, _ in rib_x(d)]
        for xa, xb in zip(xs[:-1], xs[1:]):                          # hexagon window (45 degree ends: prints without bridges)
            xa += t / 2 + 5
            xb -= t / 2 + 5
            z0, z1 = 9.0, zt - 9.0
            hh = (z1 - z0) / 2
            if xb - xa > 2 * hh + 10:
                win = poly_prism_y([(xa + hh, z0), (xb - hh, z0), (xb, (z0 + z1) / 2), (xb - hh, z1), (xa + hh, z1), (xa, (z0 + z1) / 2)],
                                   s * (WH / 2 - wall - 1) if s > 0 else -WH / 2 - 1, WH / 2 + 1 if s > 0 else -WH / 2 + wall + 1)
                w = w.cut(win)
        h = h.union(w)
        h = h.union(box(-LH / 2, LH / 2, s * yb - 12, s * yb + 12, 0, wall))          # skid under each bottle
    # mooring pad at the keel centre (independent from the umbilical, which leaves by the base rib)
    ew, et, eh = P.PET_EYE
    pad = box(-ew / 2, ew / 2, -(wc / 2 + wall), wc / 2 + wall, 0, et).cut(cyl((0, 0, -1), (0, 0, 1), eh / 2, et + 2))
    h = h.union(pad)
    # M3 insert bosses for the cover: 2 per bar, on the channel fins
    for x, kind in rib_x(d):
        if kind == "mid0":
            continue
        for s in (1, -1):
            x = boss_x(d, x)
            h = h.union(cyl((x, s * boss_y(d), 0), (0, 0, 1), 4.0, zt))      # post from the floor: no overhang
            h = h.cut(cyl((x, s * boss_y(d), zt - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    return h


def box_ear_pts(d):
    return [(d["X0"] + sx * d["L1"], sy * (d["Wy"] / 2 + P.PET_EAR[1] / 2)) for sx in (1, -1) for sy in (1, -1)]


def col_pts(d):
    return [(d["X0"] + sx * d["L1"], sy * d["yb"]) for sx in (1, -1) for sy in (1, -1)]


def b2_cubierta(d):
    LH, WH, zt, ct, bw = d["LH"], d["WH"], d["z_cover"], P.PET_COVER_T, P.PET_BAR_W
    zb = d["z_cover_top"]
    c = None
    bars = [box(x - bw / 2, x + bw / 2, -WH / 2, WH / 2, zt, zb) for x in (d["X0"] - d["L1"], d["X0"] + d["L1"])]
    bars += [box(LH / 2 - bw, LH / 2, -WH / 2, WH / 2, zt, zb), box(-LH / 2, -LH / 2 + bw, -WH / 2, WH / 2, zt, zb)]
    bars += [box(-LH / 2, LH / 2, s * d["yb"] - bw / 2, s * d["yb"] + bw / 2, zt, zb) for s in (1, -1)]
    for b in bars:
        c = b if c is None else c.union(b)
    for x, kind in rib_x(d):                                         # clearance holes for the M3 into the hull bosses
        if kind != "mid0":
            for s in (1, -1):
                c = c.cut(cyl((boss_x(d, x), s * boss_y(d), zt - 1), (0, 0, 1), P.M3_CLEAR / 2, ct + 2))
    pd, ph = P.PET_PILLAR
    for x, y in box_ear_pts(d):                                      # pillars under the ears of the box
        c = c.union(cyl((x, y, zb - 0.1), (0, 0, 1), pd / 2, ph + 0.1))
        c = c.cut(cyl((x, y, zb + ph - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    for x, y in col_pts(d):                                          # panel columns
        c = c.union(cyl((x, y, zb - 0.1), (0, 0, 1), P.PET_COLUMN_D / 2, d["z_panel0"] - zb + 0.1))
        c = c.cut(cyl((x, y, d["z_panel0"] - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    mo, mi, _ = P.PET_MAST
    xm = d["x_mast"]
    c = c.union(cyl((xm, 0, zb - 0.1), (0, 0, 1), mo / 2, d["z_mast"] - zb + 0.1))
    c = c.cut(cyl((xm, 0, zb + 6.0), (0, 0, 1), mi / 2, d["z_mast"] - zb))
    c = c.cut(cyl((xm + 1, 0, zb + 12.0), (-1, 0, 0), 3.5, mo))      # pigtail port towards the box
    return c


def screw_pts(d):
    a, b = d["Lx"] / 2 + SCREW_OFF, d["Wy"] / 2 + SCREW_OFF
    nx, ny = math.ceil(2 * a / P.BOX_SCREW_PITCH), math.ceil(2 * b / P.BOX_SCREW_PITCH)
    pts = {(round(-a + 2 * a * i / nx, 3), sy * b) for i in range(nx + 1) for sy in (1, -1)}
    pts |= {(sx * a, round(-b + 2 * b * j / ny, 3)) for j in range(ny + 1) for sx in (1, -1)}
    return sorted(pts)


def layout(d, local=False):
    """Internal parts (global frame): battery holder, tray, PCB, Waveshare, RTC, glands."""
    z0, bw_ = d["z0"], P.PET_BOX_WALL
    zf = z0 + bw_
    Li, Wi = d["Li"], d["Wi"]
    bl, bw, bh = P.BUOY_BATT_HOLDER
    pl, pw, _ = P.BUOY_PCB
    wl, ww, wh = P.BUOY_WAVESHARE
    rl, rw, rh = P.BUOY_RTC
    xb0 = -Li / 2 + P.PET_GLAND_RES
    zb0 = zf + P.BUOY_BATT_STANDOFF
    zt0 = zb0 + bh + P.BUOY_TRAY_GAP
    g = dict(zf=zf, batt=(xb0, xb0 + bl, -bw / 2, bw / 2, zb0, zb0 + bh), tray_z=(zt0, zt0 + 3.0),
             pcb=(-Li / 2 + 19, -Li / 2 + 19 + pl, -pw / 2, pw / 2, zt0 + 3, zt0 + 3 + P.BUOY_TOP_COMP_H),
             ws=(Li / 2 - 3 - wl - 2, Li / 2 - 5, -ww / 2, ww / 2, zt0 + 3, zt0 + 3 + wh),
             rtc=(Li / 2 - 3 - rl, Li / 2 - 3, -rw / 2, rw / 2, zf, zf + rh),
             umb_z=zf + 15.0, solar=(-25.0, zf + 62.0), pig=(25.0, zf + 62.0))
    if not local:
        for k in ("batt", "pcb", "ws", "rtc"):
            a = g[k]
            g[k] = (a[0] + d["X0"], a[1] + d["X0"]) + a[2:]
    return g


def b3_caja(d):
    Lx, Wy, HB, Li, Wi, z0 = d["Lx"], d["Wy"], d["HB"], d["Li"], d["Wi"], d["z0"]
    wall = P.PET_BOX_WALL
    fw, ft = P.PET_FLANGE
    c = rbox(Lx, Wy, z0, HB, 6).cut(rbox(Li, Wi, z0 + wall, HB, 3))
    # flange with a 45 degree underside (prints without supports): frustum wall -> flange, then a straight rim
    ch = fw
    frus = (cq.Workplane("XY").workplane(offset=z0 + HB - ft - ch).rect(Lx, Wy)
            .workplane(offset=ch).rect(Lx + 2 * fw, Wy + 2 * fw).loft(combine=True))
    rim = cq.Workplane("XY").workplane(offset=z0 + HB - ft).rect(Lx + 2 * fw, Wy + 2 * fw).extrude(ft)
    fl = frus.union(rim).cut(rbox(Li, Wi, z0 + HB - ft - ch - 1, ch + ft + 2, 3))
    c = c.union(fl)
    for x, y in screw_pts(d):
        c = c.cut(cyl((x, y, z0 + HB - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    g = layout(d, local=True)
    hx, hy = P.BUOY_HOLDER_HOLES
    bcx = (g["batt"][0] + g["batt"][1]) / 2
    pd = P.BUOY_POST_D
    for sx in (1, -1):
        for sy in (1, -1):
            c = c.union(cyl((bcx + sx * hx / 2, sy * hy / 2, z0 + wall - 0.1), (0, 0, 1), 4.5, P.BUOY_BATT_STANDOFF + 0.1))
            c = c.cut(cyl((bcx + sx * hx / 2, sy * hy / 2, z0 + wall + P.BUOY_BATT_STANDOFF - P.M3_INSERT_DEPTH), (0, 0, 1),
                          P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
            px, py = sx * (Li / 2 - pd / 2 - P.BUOY_POST_WALL_GAP - 1), sy * (Wi / 2 - pd / 2 - P.BUOY_POST_WALL_GAP - 3.0)
            c = c.union(cyl((px, py, z0 + wall - 0.1), (0, 0, 1), pd / 2, g["tray_z"][0] - (z0 + wall) + 0.1))
            c = c.cut(cyl((px, py, g["tray_z"][0] - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    ew, eo, et = P.PET_EAR
    for x, y in [(x - d["X0"], y) for x, y in box_ear_pts(d)]:        # ears on the pillars (flat on the bed)
        s = 1 if y > 0 else -1
        c = c.union(box(x - ew / 2, x + ew / 2, min(s * (Wy / 2 - 1), s * (Wy / 2 + eo)), max(s * (Wy / 2 - 1), s * (Wy / 2 + eo)), z0, z0 + et))
        c = c.cut(cyl((x, y, z0 - 1), (0, 0, 1), P.M3_CLEAR / 2, et + 2))
    # 3 PG7: umbilical (-X wall, low), panel cable and antenna pigtail (+X wall)
    c = c.cut(cyl((-Lx / 2 - 1, 0, g["umb_z"]), (1, 0, 0), P.PG7_HOLE / 2, wall + 2))
    for y, z in (g["solar"], g["pig"]):
        c = c.cut(cyl((Lx / 2 - wall - 1, y, z), (1, 0, 0), P.PG7_HOLE / 2, wall + 2))
    return c.translate((d["X0"], 0, 0))


def b4_tapa(d):
    Lx, Wy, z = d["Lx"], d["Wy"], d["z_lid"]
    fw = P.PET_FLANGE[0]
    t = rbox(Lx + 2 * fw, Wy + 2 * fw, z, P.PET_LID_T, 12)
    for x, y in screw_pts(d):
        t = t.cut(cyl((x, y, z - 1), (0, 0, 1), P.M3_CLEAR / 2, P.PET_LID_T + 2))
    cl_l, cl_w = Lx + 2 * GROOVE_OFF, Wy + 2 * GROOVE_OFF
    gw = P.GROOVE_WIDTH
    groove = rbox(cl_l + gw, cl_w + gw, z, P.GROOVE_DEPTH, 8).cut(rbox(cl_l - gw, cl_w - gw, z - 0.1, P.GROOVE_DEPTH + 0.2, 5))
    return t.cut(groove).translate((d["X0"], 0, 0))


def bottle_dummy(d, yc):
    """Body cylinder + conical shoulder + neck, base against the base rib."""
    nl, sh = d["neck_len"], 30.0
    xs = d["x_bot0"]
    body = d["Lb"] - nl - sh
    b = cyl((xs, yc, d["zc"]), (1, 0, 0), d["r"], body)
    cone = cq.Workplane().add(cq.Solid.makeCone(d["r"], d["neck_D"] / 2, sh, cq.Vector(xs + body, yc, d["zc"]), cq.Vector(1, 0, 0)))
    neck = cyl((xs + body + sh, yc, d["zc"]), (1, 0, 0), d["neck_D"] / 2, nl)
    return b.union(cone).union(neck)


def dummies(d):
    g = layout(d)
    pl, pw, pt = P.BUOY_PANEL
    out = {k: box(*g[k]) for k in ("batt", "pcb", "ws", "rtc")}
    out["panel"] = box(d["X0"] - pl / 2, d["X0"] + pl / 2, -pw / 2, pw / 2, d["z_panel0"], d["z_panel1"])
    xs = d["x_bot0"]
    for i, s in enumerate((-1, 1)):
        out[f"botella{i + 1}"] = bottle_dummy(d, s * d["yb"])
    return out


# ---------------------------------------------------------------- flotation
def foam_volume_mm3(d):
    """Void between the U slots and the round bottles inside the bay (estimated fill factor applies later)."""
    bay = d["LH"] - 2 * d["rib"]
    per = d["slot_w"] * (d["z_top"] - d["wall"]) * bay - math.pi * d["r"] ** 2 * min(d["Lb"], bay)
    return max(0.0, d["n"] * per)


def hydro(d, M, KG, lcg, lost=0, foam_mm3=0.0):
    """Equilibrium of the sealed volumes (bottles as cylinders of the nominal volume + the dry box) by slicing in z.
    Returns draft, immersed volume, KB, GM roll / pitch, centre of buoyancy y and x."""
    zc, yb = d["zc"], d["yb"]
    leff = d["Lb"] - d["neck_len"] - 15.0                              # waterplane length: body + half the shoulder
    r = math.sqrt(d["V"] * 1000.0 / (math.pi * leff))                   # radius that keeps the NOMINAL volume (conservative)
    bots = [(s * yb, d["xc_bot"]) for s in (-1, 1)][lost:] if d["n"] == 2 else []
    zb0, zb1 = d["z0"], d["z0"] + d["HB"] + P.PET_LID_T
    z_foam0, z_foam1 = d["wall"], d["z_top"]

    def chord(z):
        dz = abs(z - zc)
        return 0.0 if dz >= r else 2 * math.sqrt(r * r - dz * dz)

    def area(z):
        a = sum(leff * chord(z) for _ in bots)
        if zb0 <= z <= zb1:
            a += d["Lx"] * d["Wy"]
        if foam_mm3 and z_foam0 <= z <= z_foam1:
            a += foam_mm3 * (1 - P.FLOT_FOAM_DENSITY / 1025.0) / (z_foam1 - z_foam0)
        return a

    dz_ = 0.25
    V = mz = 0.0
    z = 0.0
    T = None
    while z < zb1 + 50:
        a = area(z + dz_ / 2)
        if RHO * (V + a * dz_) >= M and T is None:
            frac = (M / RHO - V) / (a * dz_) if a > 0 else 0
            T = z + frac * dz_
            V += a * dz_ * frac
            mz += a * dz_ * frac * (z + frac * dz_ / 2)
            break
        V += a * dz_
        mz += a * dz_ * (z + dz_ / 2)
        z += dz_
    if T is None:
        return dict(flota=False, calado=None)
    KB = mz / V
    ixx = iyy = 0.0
    yb_num = xb_num = 0.0
    for yc, xc in bots:
        c = chord(T)
        ixx += leff * c ** 3 / 12 + leff * c * yc ** 2
        iyy += c * leff ** 3 / 12 + c * leff * (xc - 0) ** 2
    if zb0 <= T <= zb1:
        ixx += d["Lx"] * d["Wy"] ** 3 / 12
        iyy += d["Wy"] * d["Lx"] ** 3 / 12
    # centre of buoyancy in plan (bottles weighted by their immersed volume, box by its own)
    wsum = ysum = xsum = 0.0
    for yc, xc in bots:
        zs = [i * 0.25 for i in range(int(T / 0.25) + 1)]
        vb = sum(leff * chord(zz + 0.125) * 0.25 for zz in zs if zz < T)
        wsum += vb
        ysum += vb * yc
        xsum += vb * xc
    cby = ysum / wsum if wsum else 0.0
    cbx = xsum / wsum if wsum else 0.0
    return dict(flota=True, calado=T, V=V, KB=KB, GM_roll=KB + ixx / V - KG, GM_pitch=KB + iyy / V - KG, BMr=ixx / V, BMp=iyy / V,
                cb_y=cby, cb_x=cbx, trim_arm=cbx - lcg)


def bottles_total_g(d):
    return d["n"] * d["V"]            # nominal cm3 x 1.025 would be seawater grams; see caller


# ---------------------------------------------------------------- pipeline
def process(name, stem, wp, qty, out, check_bed=True):
    shp = sanitize(wp)
    chk = brep_check(shp)
    stl = out / "stl"
    export_part(shp, stem, stl, out / "step")
    best = None
    for on, o in ORIENT.items():
        mc = mesh_checks(str(stl / f"{stem}.stl"), P.PRINT_BED, o)
        if mc["fits_bed"] and (best is None or mc["overhang_mm2"] < best[1]["overhang_mm2"]):
            best = (on, mc)
    if best is None:
        best = ("no cabe", mesh_checks(str(stl / f"{stem}.stl"), P.PRINT_BED, None))
    return dict(name=name, stem=stem, shape=shp, chk=chk, orient=best[0], mc=best[1], qty=qty)


def keep_out_corner(stl):
    """The P1P excludes a 18 x 28 corner (machine profile bed_exclude_area): slide a big part off it."""
    import trimesh
    m = trimesh.load(stl)
    (x0, y0, _), (x1, y1, _) = m.bounds
    ex, ey = P.PET_EXCLUDE
    if x0 < ex + 1 and y0 < ey + 1:
        if y1 + (ey + 1 - y0) <= P.PRINT_BED[1] - 1:
            m.apply_translation([0, ey + 1 - y0, 0])
        else:
            m.apply_translation([ex + 1 - x0, 0, 0])
        m.export(stl)


def slice_pieces(rows, out):
    import slicer as S
    prof = S.profiles()
    work = Path(tempfile.mkdtemp(prefix="orca_boya_pet_"))
    import os
    cwd = os.getcwd()
    os.chdir(work)                           # Orca drops 00000.log in the cwd
    res, fails = {}, []
    try:
        for r in rows:
            stl = work / f"{r['stem']}.stl"
            S.oriented_stl(out / "stl" / f"{r['stem']}.stl", r["orient"], stl)
            keep_out_corner(stl)
            sup = r["mc"]["overhang_mm2"] > P.PET_SUPPORT_MM2
            proc = work / f"proceso_{r['stem']}.json"
            S.process_for(prof["process"], sup, proc, 40)
            rc, gc, log = S.slice_one(prof, stl, proc, work / r["stem"])
            got = S.read_gcode(gc) if gc else None
            if not got:
                fails.append(f"{r['stem']}: rc={rc} {log.strip()[-200:]}")
                continue
            g, h = got
            res[r["stem"]] = dict(nombre=r["name"], qty=r["qty"], orientacion=r["orient"], soportes=bool(sup), relleno_pct=40,
                                  g=round(g, 1), h=round(h, 2), costo_soles=round(g * P.FILAMENT_PRICE / 1000, 2),
                                  voladizo_mm2=round(r["mc"]["overhang_mm2"], 1))
            print(f"slice {r['stem']:14s} {g:7.1f} g {h:5.2f} h  soportes {'si' if sup else 'no'}", flush=True)
    finally:
        os.chdir(cwd)
        shutil.rmtree(work, ignore_errors=True)
    return res, fails


def run(bottle, n, out, do_slice, render_png=True):
    d = dims(bottle, n)
    for dd in (out / "stl", out / "step"):
        dd.mkdir(parents=True, exist_ok=True)
    fails = []
    if n != 2:
        return dict(d=d, fallas=[f"cantidad {n} no soportada por el CAD (una fila con canal central: solo 2)"])
    rows = [process("B1 casco", "B1_casco", b1_casco(d), 1, out), process("B2 cubierta", "B2_cubierta", b2_cubierta(d), 1, out),
            process("B3 caja seca", "B3_caja", b3_caja(d), 1, out), process("B4 tapa", "B4_tapa", b4_tapa(d), 1, out)]
    for r in rows:
        ok = r["chk"]["ok"] and r["mc"]["watertight"] and r["mc"]["bodies"] == 1 and r["mc"]["fits_bed"]
        if not ok:
            fails.append(f"{r['stem']}: brep={r['chk']} estanco={r['mc']['watertight']} bodies={r['mc']['bodies']} cama={r['mc']['fits_bed']}")
        print(f"{r['stem']:14s} ok={ok} or={r['orient']} bbox={tuple(round(v, 1) for v in r['mc']['bbox'])}", flush=True)
    S_ = {r["stem"]: r["shape"] for r in rows}
    parts = {"B1 casco": S_["B1_casco"], "B2 cubierta": S_["B2_cubierta"], "B3 caja": S_["B3_caja"], "B4 tapa": S_["B4_tapa"]}
    dm = {k: v.val() for k, v in dummies(d).items()}
    # interferences (pieces vs pieces and dummies)
    allp = {**parts, **{f"dummy {k}": v for k, v in dm.items()}}
    names = list(allp)
    inter = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a.startswith("dummy") and b.startswith("dummy"):
                continue
            v = allp[a].intersect(allp[b]).Volume()
            if v > P.INTERF_TOL:
                inter.append((a, b, v))
    for a, b, v in inter:
        fails.append(f"interferencia {a} / {b}: {v:.2f} mm3")
    # printed mass and time: slicer, or estimate
    sl = {}
    sl_file = out / "slicer.json"
    if do_slice:
        sl, sfails = slice_pieces(rows, out)
        fails += [f"slicer {x}" for x in sfails]
        if sl:
            sl_file.write_text(json.dumps(sl, indent=1, ensure_ascii=False), encoding="utf-8")
    elif sl_file.exists():
        sl = json.loads(sl_file.read_text(encoding="utf-8"))
    est = {r["stem"]: FA.mass_g(r["shape"], 0.4) for r in rows}
    src = "slicer" if sl and len(sl) == len(rows) else "estimado"
    gp = {s: (sl[s]["g"] if src == "slicer" else est[s]) for s in est}
    hp = {s: (sl[s]["h"] if src == "slicer" else None) for s in est}
    # masses with z (global frame)
    g = layout(d)
    bm = P.BUOY_MASS
    m_pts = [(f"{k} impreso", gp[s], parts_c.Center().z, parts_c.Center().x) for (k, parts_c), s in zip(parts.items(), ("B1_casco", "B2_cubierta", "B3_caja", "B4_tapa"))]
    mid = lambda k: ((g[k][4] + g[k][5]) / 2, (g[k][0] + g[k][1]) / 2)    # noqa: E731
    comp = [("3 x celdas 18650", P.BUOY_CELLS * bm["celda_18650"], *mid("batt")), ("portabaterias", bm["portabaterias"], *mid("batt")),
            ("PCB + Heltec", bm["pcb_heltec"], *mid("pcb")), ("Waveshare D", bm["waveshare"], *mid("ws")), ("RTC", bm["rtc"], *mid("rtc")),
            ("panel solar", bm["panel"], (d["z_panel0"] + d["z_panel1"]) / 2, d["X0"]),
            ("antena LoRa (en el mastil)", bm["antena"], d["z_mast"] - 40, d["x_mast"]),
            ("cables y fusible", bm["cables_fusible"], g["zf"] + 30, d["X0"]), ("3 PG7", bm["prensaestopas"] * 1.5, g["zf"] + 30, d["X0"]),
            ("tornilleria (M3, insertos, junta)", bm["tornilleria"], d["z0"] + 40, d["X0"]),
            (f"{n} botellas vacias", n * d["m_bottle"], d["zc"], d["xc_bot"])]
    foam_V = foam_volume_mm3(d) * P.FLOT_FOAM_FILL
    if P.FLOT_FILL == "espuma_PU":
        comp.append(("espuma PU (masa)", foam_V * P.FLOT_FOAM_DENSITY * 1e-6, d["zc"], d["xc_bot"]))
    m_pts += comp
    M = sum(m[1] for m in m_pts)
    KG = sum(m[1] * m[2] for m in m_pts) / M
    LCG = sum(m[1] * m[3] for m in m_pts) / M
    base = hydro(d, M, KG, LCG)
    r, V1 = d["r"], d["V"]
    buoy_bottles_g = n * V1 * P.SEAWATER_DENSITY          # g, fully submerged
    foam_res_g = foam_V * (P.SEAWATER_DENSITY - P.FLOT_FOAM_DENSITY * 1e-3) * 1e-3 if P.FLOT_FILL == "espuma_PU" else 0.0
    res = dict(botella=bottle, cantidad=n, masa_g=M, masa_impresa_g=sum(gp.values()), fuente_masa_impresa=src, KG=KG, LCG=LCG,
               empuje_botellas_g=buoy_bottles_g, reserva_g=buoy_bottles_g - M, reserva_pct=(buoy_bottles_g - M) / M * 100,
               espuma_reserva_estimada_g=foam_res_g, espuma_volumen_cm3=foam_V / 1000, hidro=base,
               dims={k: (round(v, 2) if isinstance(v, float) else v) for k, v in d.items()},
               piezas={r_["stem"]: dict(nombre=r_["name"], qty=r_["qty"], orient=r_["orient"], bbox=list(r_["mc"]["bbox"]),
                                        voladizo_mm2=r_["mc"]["overhang_mm2"], volumen_cm3=r_["shape"].Volume() / 1000,
                                        g=gp[r_["stem"]], h=hp[r_["stem"]], g_estimado=est[r_["stem"]]) for r_ in rows},
               masas=[dict(elemento=a, g=b, z=c) for a, b, c, _ in m_pts])
    if base["flota"]:
        T = base["calado"]
        res["francobordo_caja_mm"] = d["z0"] - T
        res["francobordo_tapa_mm"] = d["z_lid_top"] - T
        res["francobordo_cubierta_mm"] = d["z_cover_top"] - T
        res["francobordo_junta_mm"] = d["z_lid"] - T
        res["francobordo_abertura_mm"] = g["umb_z"] - P.PG7_HOLE / 2 - T      # lowest opening of the dry box: the umbilical PG7
        if res["francobordo_abertura_mm"] < P.BUOY_FREEBOARD_MIN:
            fails.append(f"francobordo a la abertura mas baja de la caja {res['francobordo_abertura_mm']:.1f} < {P.BUOY_FREEBOARD_MIN:g}")
        if min(base["GM_roll"], base["GM_pitch"]) <= 0:
            fails.append(f"GM no positivo ({base['GM_roll']:.0f} / {base['GM_pitch']:.0f})")
        if abs(base["cb_y"]) > 1e-6:
            fails.append("centro de empuje fuera del eje")
    else:
        fails.append("no flota con las botellas y la caja")
    # one bottle lost (with and without the estimated foam)
    for tag, fm in (("sin_espuma", 0.0), ("con_espuma_estimada", foam_V / 2 if P.FLOT_FILL == "espuma_PU" else 0.0)):
        h1 = hydro(d, M, KG, LCG, lost=1, foam_mm3=fm)
        res[f"una_botella_perdida_{tag}"] = h1
    # tilt estimate for the lost case: transverse CB offset over GM
    for tag in ("sin_espuma", "con_espuma_estimada"):
        h1 = res[f"una_botella_perdida_{tag}"]
        if h1["flota"] and h1["GM_roll"] > 0:
            wsum_y = h1["cb_y"]
            h1["escora_est_deg"] = math.degrees(math.atan(abs(wsum_y) / h1["GM_roll"])) if abs(wsum_y) > 1e-6 else 0.0
    res["piezas_cabe_cama"] = all(r_["mc"]["fits_bed"] for r_ in rows)
    tot_g, tot_h = sum(gp[s] for s in gp), (sum(hp[s] for s in hp) if src == "slicer" else None)
    res["total_impreso_g"], res["total_impreso_h"] = tot_g, tot_h
    if src == "slicer":
        if tot_g > P.PET_MASS_TARGET:
            fails.append(f"masa impresa {tot_g:.0f} g > {P.PET_MASS_TARGET:g}")
        if tot_h > P.PET_TIME_TARGET:
            fails.append(f"tiempo {tot_h:.1f} h > {P.PET_TIME_TARGET:g}")
    res["costo_soles"] = tot_g * P.FILAMENT_PRICE / 1000
    res["fallas"] = fails
    res["interferencias"] = [(a, b, v) for a, b, v in inter]
    if render_png:
        asm = cq.Assembly(name="boya_pet")
        for k, sh in parts.items():
            asm.add(sh, name=k.replace(" ", "_"))
        for k, sh in dm.items():
            asm.add(sh, name=f"ref_{k}")
        asm.export(str(out / "ENSAMBLE_boya_pet.step"))
        fix_step_stamp(out / "ENSAMBLE_boya_pet.step")
        from render import render
        colr = {"B1 casco": "#3a7ca5", "B2 cubierta": "#e07b39", "B3 caja": "#3a9d7a", "B4 tapa": "#9fb7cc"}
        items = [(sh, colr[k], 0.55 if k == "B4 tapa" else 1.0, True, None) for k, sh in parts.items()]
        for k, sh in dm.items():
            items.append((sh, "#1d1d3a" if k == "panel" else "#5dade2" if k.startswith("botella") else "#c9a227", 0.5 if k.startswith("botella") else 1.0,
                          True, None))
        T = base["calado"] if base["flota"] else 0
        water = box(-300, 300, -250, 250, T - 0.5, T).val()
        title = (f"Boya PET {n} x {bottle}: calado {T:.0f} mm, francobordo caja {res.get('francobordo_caja_mm', 0):.0f} mm, {M:.0f} g")
        render(items + [(water, "#7fb3d5", 0.25, False, None)], out / "boya_pet_iso.png", "iso", title)
        cut = box(-500, 500, -500, 0, -100, 500).val()
        render([(sh.cut(cut), c, o, e, None) for sh, c, o, e, _ in items if sh.cut(cut).Volume() > 1e-3]
               + [(water.cut(cut), "#7fb3d5", 0.25, False, None)], out / "boya_pet_corte.png", "frontal",
               "Corte en y = 0 de la boya PET con la linea de agua")
    res["_rows"] = rows
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--botella", default=P.FLOT_BOTTLE)
    ap.add_argument("--cantidad", type=int, default=P.FLOT_COUNT)
    ap.add_argument("--sin-slicer", action="store_true")
    ap.add_argument("--sin-alternativas", action="store_true")
    a = ap.parse_args()
    res = run(a.botella, a.cantidad, OUT, not a.sin_slicer)
    alts = {}
    if not a.sin_alternativas:
        for b in P.FLOT_BOTTLES:
            if b == a.botella:
                continue
            tmp = Path(tempfile.mkdtemp(prefix="boya_pet_alt_"))
            try:
                alts[b] = run(b, a.cantidad, tmp, False, render_png=False)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
    clean = {k: v for k, v in res.items() if k != "_rows"}
    clean["alternativas"] = {b: {k: v for k, v in r.items() if k not in ("_rows", "masas", "dims")} for b, r in alts.items()}
    (OUT / "resultados.json").write_text(json.dumps(clean, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
    write_report(res, alts)
    h = res.get("hidro", {})
    if h.get("flota"):
        print(f"boya {res['masa_g']:.0f} g (impreso {res['total_impreso_g']:.0f} g, {res['fuente_masa_impresa']}), calado {h['calado']:.1f}, "
              f"francobordo caja {res['francobordo_caja_mm']:.1f}, reserva {res['reserva_pct']:.0f} %, GM {h['GM_roll']:.0f}/{h['GM_pitch']:.0f}")
    print("FALLAS:", res["fallas"] if res["fallas"] else "ninguna")
    return 1 if res["fallas"] else 0


def write_report(r, alts):
    h = r["hidro"]
    Ls = ["# Boya con botellas PET (generado por `boya_pet.py`)", "",
          f"{r['cantidad']} botellas de {r['botella']}, relleno {P.FLOT_FILL}. Masas impresas: {r['fuente_masa_impresa']}.", "",
          f"| Masa total boya | {r['masa_g']:.0f} g |", "|---|---|",
          f"| Calado | {h['calado']:.1f} mm |", f"| Francobordo a la base de la caja | {r['francobordo_caja_mm']:.1f} mm |",
          f"| Reserva | {r['reserva_pct']:.0f} % |", f"| GM balanceo / cabeceo | {h['GM_roll']:.0f} / {h['GM_pitch']:.0f} mm |", "",
          "## Chequeos que fallaron", ""] + ([f"- {f}" for f in r["fallas"]] if r["fallas"] else ["- ninguno"])
    (HERE / "reporte_boya_pet.md").write_text("\n".join(Ls) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
