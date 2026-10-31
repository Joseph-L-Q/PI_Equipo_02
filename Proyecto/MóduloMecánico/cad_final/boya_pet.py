"""Buoy with sealed PET bottles + PU spray foam (block C of the CAD job); replaces the platform buoy of boya_simple.py.

    python boya_pet.py                       (from cad_final/) CAD + checks + OrcaSlicer + flotation + report
    python boya_pet.py --sin-slicer          reuse salida/boya_pet/slicer.json (or estimate masses if missing)
    python boya_pet.py --botella 500ml|1L|2L --cantidad 2|4   override flotacion.botella / flotacion.cantidad
    python boya_pet.py --salida DIR --limpiar-stl            write somewhere else (comparison configs), drop STL/STEP after
    python boya_pet.py --alternativas                        also model the other bottle types (no slicing)

cantidad 2 = "fila": two bottles along X in one hull (pieces B1..B4, below).
cantidad 4 = "cruz": hull B1 with two bottles along X (opposite necks) + two cradles B5 (one per X end, bottle along Y,
             bolted to the end ribs of B1 with M3 through the end rib into inserts of B5 tongues) + 4 straps B6;
             B2 cover over the central hull only. The cross is C2 symmetric, so one B5 STL serves both ends.

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
import os
import shutil
import tempfile
from pathlib import Path

import cadquery as cq
import numpy as np

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
def _bottle_radius(d, s):
    """Bottle radius at distance s from the base (body, 30 mm conical shoulder, neck)."""
    ns = d["Lb"] - d["neck_len"]
    if s >= ns:
        return d["neck_D"] / 2
    if s >= ns - 30.0:
        return d["neck_D"] / 2 + (d["r"] - d["neck_D"] / 2) * (ns - s) / 30.0
    return d["r"]


def _dims_fila(bottle, n):
    """Two bottles along X in one hull with a central channel (the first design)."""
    b = P.FLOT_BOTTLES[bottle]
    D, Lb = b["D"], b["L"]
    r = D / 2
    wall, rib, clr, wc = P.PET_WALL, P.PET_RIB, P.FLOT_CLEAR, P.FLOT_CHANNEL
    d = dict(layout="fila", bottle=bottle, n=n, D=D, r=r, Lb=Lb, V=b["V"], neck_D=b["neck_D"], neck_len=b["neck_len"], m_bottle=b["m_g"], wall=wall, rib=rib, clr=clr, wc=wc)
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
    xn = d["LH"] / 2 - rib / 2                                      # centre of the neck rib
    d["neck_slot_r"] = min(r + clr, _bottle_radius(d, xn - d["x_bot0"]) + 1.0)
    d["bots"] = [dict(axis="x", x=d["xc_bot"], y=s * d["yb"]) for s in (-1, 1)]
    d["bays"] = [(d["x_bot0"] - rib, d["LH"] / 2 - rib, s * d["yb"] - d["slot_w"] / 2, s * d["yb"] + d["slot_w"] / 2, d["LH"] - 2 * rib) for s in (-1, 1)]
    d["col_y"] = d["yb"]
    return d


def _dims_cruz(bottle, n):
    """Cross: two bottles along X in the central hull (opposite necks) + two cradles at the X ends with the bottle along Y."""
    b = P.FLOT_BOTTLES[bottle]
    D, Lb = b["D"], b["L"]
    r = D / 2
    wall, rib, clr, ec = P.PET_WALL, P.PET_RIB, P.FLOT_CLEAR, P.FLOT_END_CLR
    d = dict(layout="cruz", bottle=bottle, n=n, D=D, r=r, Lb=Lb, V=b["V"], neck_D=b["neck_D"], neck_len=b["neck_len"], m_bottle=b["m_g"], wall=wall, rib=rib, clr=clr, end_clr=ec)
    d["slot_w"] = D + 2 * clr
    d["Wb"] = d["slot_w"] + 2 * wall                                # width of one bay
    lh_nat = Lb + 2 * rib + 2 * ec
    d["LH"] = min(lh_nat, P.PET_HULL_MAX)
    wmax = P.PET_HULL_W_MAX if d["LH"] <= P.PET_HULL_L_ALT else 256.0 - P.PET_EXCLUDE[1] - 2.4
    d["yb"] = wmax / 2 - d["Wb"] / 2
    d["WH"] = wmax
    d["wc"] = 2 * (d["yb"] - d["slot_w"] / 2 - wall)                # channel between the two X bays (open at the bottom)
    d["zc"] = wall + clr + r
    d["z_top"] = d["zc"] + r + clr
    d["L1"] = d["LH"] / 4
    d["x_bot0"] = -d["LH"] / 2 + rib + ec
    d["tip_x"] = d["x_bot0"] + Lb
    d["poke"] = max(0.0, d["tip_x"] - d["LH"] / 2)                  # neck beyond the outer face of the end rib
    d["X0"] = 0.0
    d["xc_bot"] = d["x_bot0"] + Lb / 2
    xn = d["LH"] / 2 - rib / 2
    d["neck_slot_r"] = min(r + clr, _bottle_radius(d, xn - d["x_bot0"]) + 1.0)
    tw, th, tmin = P.PET_TONGUE
    d["tongue_w"], d["tongue_h"] = tw, th
    d["tongue_l"] = max(tmin, d["tip_x"] + 2.0 - d["LH"] / 2 - 0.2)  # reaches back from the cradle wall to the end rib
    d["x_wall"] = d["LH"] / 2 + 0.2 + d["tongue_l"]                 # outer face of the cradle wall facing the hull
    d["Xc"] = d["x_wall"] + d["Wb"] / 2
    ys = [d["yb"] - 22.0]
    if d["yb"] + 22.0 + tw / 2 <= d["LH"] / 2 - 2.0:
        ys.append(d["yb"] + 22.0)
    d["tongue_y"] = sorted(ys + [-y for y in ys])
    c = d["xc_bot"]
    d["bots"] = [dict(axis="x", x=c, y=d["yb"]), dict(axis="x", x=-c, y=-d["yb"]),
                 dict(axis="y", x=d["Xc"], y=c), dict(axis="y", x=-d["Xc"], y=-c)]
    xb = d["x_bot0"]
    d["bottle_bases"] = [((xb, d["yb"]), (1, 0)), ((-xb, -d["yb"]), (-1, 0)), ((d["Xc"], xb), (0, 1)), ((-d["Xc"], -xb), (0, -1))]
    bay = d["LH"] - 2 * rib
    d["bays"] = [(-d["LH"] / 2 + rib, d["LH"] / 2 - rib, d["yb"] * s - d["slot_w"] / 2, d["yb"] * s + d["slot_w"] / 2, bay) for s in (1, -1)]
    d["bays"] += [(d["Xc"] * s - d["slot_w"] / 2, d["Xc"] * s + d["slot_w"] / 2, -(d["LH"] / 2 - rib), d["LH"] / 2 - rib, bay) for s in (1, -1)]
    d["col_y"] = min(d["yb"], 77.0)
    d["wall_h"] = d["zc"] + 10.0                                    # side walls only up to just above the bottle axis (mass); the ribs go to z_top
    return d


def dims(bottle, n):
    """Every derived dimension of the buoy for a bottle type and count (frame in the module docstring)."""
    if n not in (2, 4):
        raise ValueError(f"cantidad {n}: el CAD cubre 2 (fila) y 4 (cruz)")
    d = _dims_fila(bottle, n) if n == 2 else _dims_cruz(bottle, n)
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


def hex_wall(d, y0, y1, xs):
    """Side wall between y0 and y1 along the whole hull length (height wall_h), hexagon windows between the ribs xs when they fit."""
    t, zt, LH = d["rib"], d.get("wall_h", d["z_top"]), d["LH"]
    w = box(-LH / 2, LH / 2, y0, y1, 0, zt)
    for xa, xb in zip(xs[:-1], xs[1:]):
        xa += t / 2 + 5
        xb -= t / 2 + 5
        z0, z1 = 9.0, zt - 9.0
        hh = (z1 - z0) / 2
        if xb - xa > 2 * hh + 10:
            w = w.cut(poly_prism_y([(xa + hh, z0), (xb - hh, z0), (xb, (z0 + z1) / 2), (xb - hh, z1), (xa + hh, z1), (xa, (z0 + z1) / 2)], y0 - 1, y1 + 1))
    return w


def bay_rib(d, x, yc, kind):
    """Rib plate of one bay (width Wb centred on y = yc). base: closed with a lightening diamond; tip: slot for a poking neck,
    or a closed stop when the neck stays inside; mid: U slot with clearance."""
    t, zt, zc, Wb = d["rib"], d["z_top"], d["zc"], d["Wb"]
    rb = box(x - t / 2, x + t / 2, yc - Wb / 2, yc + Wb / 2, 0, zt)
    if kind == "base" or (kind == "tip" and d["poke"] <= 0):
        return rb.cut(diamond_x(x, yc, zc, 0.42 * d["D"], t))
    rs = d["neck_slot_r"] if kind == "tip" else d["r"] + d["clr"]
    ws = 2 * rs if kind == "tip" else d["slot_w"]
    return rb.cut(cyl((x - t, yc, zc), (1, 0, 0), rs, 2 * t)).cut(box(x - t, x + t, yc - ws / 2, yc + ws / 2, zc, zt + 1))


def bay_solid(d, yc, kinds, walls):
    """One bottle bay along X, centred on y = yc: 5 ribs (kinds = (end at -x, end at +x)), side walls on the given sides
    (+1: at yc + Wb/2, -1: at yc - Wb/2) and the skid under the bottle."""
    t, wall, LH, Wb, L1 = d["rib"], d["wall"], d["LH"], d["Wb"], d["L1"]
    ribs = [(-LH / 2 + t / 2, kinds[0]), (-L1, "mid"), (0.0, "mid"), (L1, "mid"), (LH / 2 - t / 2, kinds[1])]
    h = None
    for x, kind in ribs:
        rb = bay_rib(d, x, yc, kind)
        h = rb if h is None else h.union(rb)
    xs = [x for x, _ in ribs]
    for s in walls:
        y0, y1 = (yc + Wb / 2 - wall, yc + Wb / 2) if s > 0 else (yc - Wb / 2, yc - Wb / 2 + wall)
        h = h.union(hex_wall(d, y0, y1, xs))
    return h.union(box(-LH / 2, LH / 2, yc - 12, yc + 12, 0, wall))


def b1_cruz(d):
    """Central hull of the cross: two X bays with opposite necks, tied by the bottom plates across the channel and the mooring pad."""
    t, wall, zt, yb, wc, LH = d["rib"], d["wall"], d["z_top"], d["yb"], d["wc"], d["LH"]
    h = bay_solid(d, yb, ("base", "tip"), (1,)).union(bay_solid(d, -yb, ("tip", "base"), (-1,)))
    for x in (-LH / 2 + t / 2, -d["L1"], 0.0, d["L1"], LH / 2 - t / 2):          # ties across the (bottom-open) channel
        h = h.union(box(x - t / 2, x + t / 2, -wc / 2 - 0.5, wc / 2 + 0.5, 0, wall))
    ew, et, eh = P.PET_EYE
    h = h.union(box(-ew / 2, ew / 2, -(wc / 2 + 1.0), wc / 2 + 1.0, 0, et).cut(cyl((0, 0, -1), (0, 0, 1), eh / 2, et + 2)))
    for x, kind in rib_x(d):                                                     # M3 insert bosses for the cover
        if kind == "mid0":
            continue
        for s in (1, -1):
            x = boss_x(d, x)
            h = h.union(cyl((x, s * boss_y(d), 0), (0, 0, 1), 4.0, zt))
            h = h.cut(cyl((x, s * boss_y(d), zt - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    for y in d["tongue_y"]:                                                      # clearance holes for the cradle M3 (through the end ribs)
        for x0 in (-LH / 2 - 1, LH / 2 - t - 1):
            h = h.cut(cyl((x0, y, d["tongue_h"] / 2), (1, 0, 0), P.M3_CLEAR / 2, t + 2))
    return h


def b5_cuna(d):
    """Cradle of one Y bottle, built with the bottle along +X and the hull side at +y (placed by cradle_world)."""
    wall, zt, Wb, L1 = d["wall"], d["z_top"], d["Wb"], d["L1"]
    h = bay_solid(d, 0.0, ("base", "tip"), (1, -1))
    tw, th, tl = d["tongue_w"], d["tongue_h"], d["tongue_l"]
    for xl in d["tongue_y"]:
        tg = box(xl - tw / 2, xl + tw / 2, Wb / 2 - 1.0, Wb / 2 + tl, 0, th)
        tg = tg.cut(cyl((xl, Wb / 2 + tl - P.M3_INSERT_DEPTH, th / 2), (0, 1, 0), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
        h = h.union(tg)
    ls = L1 if d["poke"] <= 0 else d["yb"] - 22.0                                # strap stations: clear of a poking neck of the hull bottle
    for x in (-ls, ls):                                                          # posts for the straps
        for s in (1, -1):
            y = s * (Wb / 2 + 1.0)                                               # outside the slot: clear of the bottle
            h = h.union(cyl((x, y, 0), (0, 0, 1), 4.0, zt))
            h = h.cut(cyl((x, y, zt - P.M3_INSERT_DEPTH), (0, 0, 1), P.M3_INSERT_HOLE / 2, P.M3_INSERT_DEPTH + 0.1))
    return h


def b6_correa(d):
    """Strap that closes a cradle over the bottle (flat on the bed)."""
    w, t = P.PET_STRAP
    span = d["Wb"] + 2.0
    s = box(-w / 2, w / 2, -span / 2 - 7.0, span / 2 + 7.0, 0, t)
    for sg in (1, -1):
        s = s.cut(cyl((0, sg * span / 2, -1), (0, 0, 1), P.M3_CLEAR / 2, t + 2))
    return s


def to_world(shape, side, d, shift=(0.0, 0.0, 0.0)):
    """Cradle frame -> world: +1 = cradle at +x (bottle towards +y), -1 = at -x. shift is applied in the cradle frame."""
    s = shape.translate(cq.Vector(*shift)) if any(shift) else shape
    return s.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 90 * side).translate(cq.Vector(side * d["Xc"], 0, 0))


def box_ear_pts(d):
    return [(d["X0"] + sx * d["L1"], sy * (d["Wy"] / 2 + P.PET_EAR[1] / 2)) for sx in (1, -1) for sy in (1, -1)]


def col_pts(d):
    return [(d["X0"] + sx * d["L1"], sy * d["col_y"]) for sx in (1, -1) for sy in (1, -1)]


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
             umb_z=zf + P.PET_UMB_Z, solar=(-25.0, zf + 62.0), pig=(25.0, zf + 62.0))
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


def bottle_dummy(d, base, direction):
    """Body cylinder + conical shoulder + neck; base = (x, y) of the base end, direction = unit (dx, dy) along the axis."""
    nl, sh = d["neck_len"], 30.0
    body = d["Lb"] - nl - sh
    (x0, y0), (dx, dy) = base, direction
    z = d["zc"]
    vec = (dx, dy, 0)
    b = cyl((x0, y0, z), vec, d["r"], body)
    cone = cq.Workplane().add(cq.Solid.makeCone(d["r"], d["neck_D"] / 2, sh, cq.Vector(x0 + dx * body, y0 + dy * body, z), cq.Vector(*vec)))
    neck = cyl((x0 + dx * (body + sh), y0 + dy * (body + sh), z), vec, d["neck_D"] / 2, nl)
    return b.union(cone).union(neck)


def bottle_bases(d):
    if d["layout"] == "cruz":
        return d["bottle_bases"]
    return [((d["x_bot0"], s * d["yb"]), (1, 0)) for s in (-1, 1)]


def dummies(d):
    g = layout(d)
    pl, pw, pt = P.BUOY_PANEL
    out = {k: box(*g[k]) for k in ("batt", "pcb", "ws", "rtc")}
    out["panel"] = box(d["X0"] - pl / 2, d["X0"] + pl / 2, -pw / 2, pw / 2, d["z_panel0"], d["z_panel1"])
    for i, (base, direc) in enumerate(bottle_bases(d)):
        out[f"botella{i + 1}"] = bottle_dummy(d, base, direc)
    return out


# ---------------------------------------------------------------- flotation
def foam_volume_mm3(d):
    """Void between the slots and the round bottles inside every bay (the estimated fill factor applies later)."""
    tot = 0.0
    for _x0, _x1, _y0, _y1, bay in d["bays"]:
        tot += d["slot_w"] * (d["z_top"] - d["wall"]) * bay - math.pi * d["r"] ** 2 * min(d["Lb"], bay)
    return max(0.0, tot)


def eff_bottle(d):
    """Effective cylinder of a bottle for the hydrostatics: length leff (body + half the shoulder) and the radius that keeps the NOMINAL volume."""
    leff = d["Lb"] - d["neck_len"] - 15.0
    return leff, math.sqrt(d["V"] * 1000.0 / (math.pi * leff))


def hydro(d, M, KG, cg_xy=(0.0, 0.0), lost=None, foam_mm3=0.0):
    """Upright equilibrium of the sealed volumes (bottles as cylinders of the nominal volume + the dry box) by slicing in z.
    Draft, KB, GM roll / pitch from the inertia of the waterplane about ITS centroid, centre of buoyancy in plan.
    lost = index of a bottle removed from d["bots"]; foam_mm3 = displaced foam volume (its mass is already in M)."""
    leff, r = eff_bottle(d)
    zc = d["zc"]
    bots = [b for i, b in enumerate(d["bots"]) if i != lost]
    zb0, zb1 = d["z0"], d["z0"] + d["HB"] + P.PET_LID_T
    Lx, Wy, X0 = d["Lx"], d["Wy"], d["X0"]
    zf0, zf1 = d["wall"], d["z_top"]

    def chord(z):
        dz = abs(z - zc)
        return 0.0 if dz >= r else 2 * math.sqrt(r * r - dz * dz)

    def area(z):
        a = leff * chord(z) * len(bots)
        if zb0 <= z <= zb1:
            a += Lx * Wy
        if foam_mm3 and zf0 <= z <= zf1:
            a += foam_mm3 / (zf1 - zf0)
        return a

    dz_ = 0.25
    V = mz = 0.0
    z = 0.0
    T = None
    while z < zb1 + 80:
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
    c = chord(T)
    parts = []                                         # (A, x, y, own inertia for roll (about x), own inertia for pitch (about y))
    for b in bots:
        if c > 0:
            if b["axis"] == "x":
                parts.append((leff * c, b["x"], b["y"], leff * c ** 3 / 12, c * leff ** 3 / 12))
            else:
                parts.append((leff * c, b["x"], b["y"], c * leff ** 3 / 12, leff * c ** 3 / 12))
    if zb0 <= T <= zb1:
        parts.append((Lx * Wy, X0, 0.0, Lx * Wy ** 3 / 12, Wy * Lx ** 3 / 12))
    A = sum(p_[0] for p_ in parts)
    xw = sum(p_[0] * p_[1] for p_ in parts) / A
    yw = sum(p_[0] * p_[2] for p_ in parts) / A
    ixx = sum(p_[3] + p_[0] * (p_[2] - yw) ** 2 for p_ in parts)
    iyy = sum(p_[4] + p_[0] * (p_[1] - xw) ** 2 for p_ in parts)
    vs = xs = ys = 0.0                                 # immersed volume per element -> centre of buoyancy in plan
    for b in bots:
        vb = sum(leff * chord(i * 0.25 + 0.125) * 0.25 for i in range(int(T / 0.25) + 1) if i * 0.25 < T)
        vs += vb
        xs += vb * b["x"]
        ys += vb * b["y"]
    if T > zb0:
        vb = Lx * Wy * (min(T, zb1) - zb0)
        vs += vb
        xs += vb * X0
    cbx, cby = xs / vs, ys / vs
    return dict(flota=True, calado=T, V=V, KB=KB, GM_roll=KB + ixx / V - KG, GM_pitch=KB + iyy / V - KG, BMr=ixx / V, BMp=iyy / V,
                cb_x=cbx, cb_y=cby, arm_x=cbx - cg_xy[0], arm_y=cby - cg_xy[1], area_flot=A)


# --- 3D equilibrium (heel and trim) by sampling the sealed volumes: smooth waterline, so the root finder has a gradient
def _pts_cyl(c, axis, r, L, na=16, nc=36):
    """Cylinder as an na x (nc x nc grid inside the circle) cloud: uniform vertical resolution of about 2r/nc."""
    a = (np.arange(na) + .5) / na * L - L / 2
    g = (np.arange(nc) + .5) / nc * 2 * r - r
    U, V_ = np.meshgrid(g, g, indexing="ij")
    ins = U ** 2 + V_ ** 2 <= r * r
    u, v = U[ins], V_[ins]
    A_ = np.repeat(a, len(u))
    uu, vv = np.tile(u, na), np.tile(v, na)
    P3 = np.stack([A_, uu, vv], -1) if axis == "x" else np.stack([uu, A_, vv], -1)
    return P3 + np.array(c), np.full(len(P3), L * np.pi * r * r / len(P3))


def _pts_box(x0, x1, y0, y1, z0, z1, vol=None, n=(14, 10, 10)):
    g = [(np.arange(k) + .5) / k for k in n]
    X, Y, Z = np.meshgrid(x0 + (x1 - x0) * g[0], y0 + (y1 - y0) * g[1], z0 + (z1 - z0) * g[2], indexing="ij")
    P3 = np.stack([X, Y, Z], -1).reshape(-1, 3)
    v = (x1 - x0) * (y1 - y0) * (z1 - z0) if vol is None else vol
    return P3, np.full(len(P3), v / len(P3))


def _rotm(phi, th):
    cp, sp, ct, st = math.cos(phi), math.sin(phi), math.cos(th), math.sin(th)
    return np.array([[ct, 0, st], [0, 1, 0], [-st, 0, ct]]) @ np.array([[1, 0, 0], [0, cp, -sp], [0, sp, cp]])


def sealed_points(d, lost=None, foam_mm3=0.0):
    leff, r = eff_bottle(d)
    Ps, Ws = [], []
    for i, b in enumerate(d["bots"]):
        if i != lost:
            p_, w_ = _pts_cyl((b["x"], b["y"], d["zc"]), b["axis"], r, leff)
            Ps.append(p_)
            Ws.append(w_)
    p_, w_ = _pts_box(d["X0"] - d["Lx"] / 2, d["X0"] + d["Lx"] / 2, -d["Wy"] / 2, d["Wy"] / 2, d["z0"], d["z0"] + d["HB"] + P.PET_LID_T)
    Ps.append(p_)
    Ws.append(w_)
    if foam_mm3:
        tot = sum((b[1] - b[0]) * (b[3] - b[2]) for b in d["bays"])
        for x0, x1, y0, y1, _bay in d["bays"]:
            p_, w_ = _pts_box(x0, x1, y0, y1, d["wall"], d["z_top"], vol=foam_mm3 * (x1 - x0) * (y1 - y0) / tot, n=(8, 6, 6))
            Ps.append(p_)
            Ws.append(w_)
    return np.vstack(Ps), np.concatenate(Ws)


def _eq_state(Pt, Wt, M, cg, phi, th, s=0.6):
    pw = (Pt - cg) @ _rotm(phi, th).T
    z = pw[:, 2]
    lo, hi = z.min() - 5, z.max() + 5
    for _ in range(46):
        h = (lo + hi) / 2
        if RHO * (Wt / (1 + np.exp(-(h - z) / s))).sum() > M:
            hi = h
        else:
            lo = h
    ws = Wt / (1 + np.exp(-(h - z) / s))
    return h, (pw * ws[:, None]).sum(0) / ws.sum()


def attitude(d, M, cg, lost=None, foam_mm3=0.0, open_pt=None):
    """Heel / trim (deg) at which the centre of buoyancy sits under the centre of gravity, GM about that attitude (numerical),
    freeboard of the lowest opening of the box. Sampled volumes: coarse (about 1 mm in the waterline), enough for angles."""
    from scipy.optimize import root
    cg = np.array(cg)
    Pt, Wt = sealed_points(d, lost, foam_mm3)

    def f(q):
        h, cb = _eq_state(Pt, Wt, M, cg, q[0], q[1])
        return [cb[1], cb[0]]

    dd = 0.01

    def at(phi, th):
        h, cb = _eq_state(Pt, Wt, M, cg, phi, th)
        gr = -(_eq_state(Pt, Wt, M, cg, phi + dd, th)[1][1] - _eq_state(Pt, Wt, M, cg, phi - dd, th)[1][1]) / (2 * dd)
        gp = (_eq_state(Pt, Wt, M, cg, phi, th + dd)[1][0] - _eq_state(Pt, Wt, M, cg, phi, th - dd)[1][0]) / (2 * dd)
        return h, float(np.hypot(cb[0], cb[1])), float(gr), float(gp)

    cands = []
    for g0 in [(0, 0), (.2, 0), (-.2, 0), (0, .2), (0, -.2), (.4, 0), (-.4, 0), (0, .4), (0, -.4), (.25, .25), (-.25, -.25), (.25, -.25), (-.25, .25)]:
        sol = root(f, list(g0), method="hybr", options=dict(eps=0.002, xtol=1e-8))
        h, resid, gr, gp = at(*sol.x)
        tilt0 = math.degrees(math.acos(max(-1.0, min(1.0, _rotm(*sol.x)[2, 2]))))        # angle between the body z axis and the vertical
        cands.append((resid < 0.5, gr > 0 and gp > 0 and tilt0 < 90.0, -tilt0, sol.x, h, resid, gr, gp))
        if g0 == (0, 0) and cands[-1][0] and cands[-1][1] and tilt0 < 5.0:      # upright and stable: nothing nearer to find
            break
    ok = [c for c in cands if c[0] and c[1]]
    best = max(ok, key=lambda c: c[2]) if ok else min(cands, key=lambda c: c[5])     # nearest stable root, else the least bad one
    _, _, _, (phi, th), h, resid, gr, gp = best
    out = dict(escora_deg=math.degrees(phi), cabeceo_deg=math.degrees(th), residuo_mm=resid, GM_roll=float(gr), GM_pitch=float(gp),
               inclinacion_deg=math.degrees(math.acos(max(-1.0, min(1.0, _rotm(phi, th)[2, 2])))), converge=bool(resid < 0.5),
               estable=bool(ok))
    if open_pt is not None:
        pz = ((np.array(open_pt) - cg) @ _rotm(phi, th).T)[2]
        out["francobordo_abertura_mm"] = float(pz - h)
    return out


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


def _bb_overlap(a, b):
    x, y = a.BoundingBox(), b.BoundingBox()
    return not (x.xmax < y.xmin or y.xmax < x.xmin or x.ymax < y.ymin or y.ymax < x.ymin or x.zmax < y.zmin or y.zmax < x.zmin)


def run(bottle, n, out, do_slice, render_png=True):
    d = dims(bottle, n)
    cruz = d["layout"] == "cruz"
    for dd in (out / "stl", out / "step"):
        dd.mkdir(parents=True, exist_ok=True)
    fails = []
    rows = [process("B1 casco", "B1_casco", b1_cruz(d) if cruz else b1_casco(d), 1, out), process("B2 cubierta", "B2_cubierta", b2_cubierta(d), 1, out),
            process("B3 caja seca", "B3_caja", b3_caja(d), 1, out), process("B4 tapa", "B4_tapa", b4_tapa(d), 1, out)]
    if cruz:
        rows += [process("B5 cuna", "B5_cuna", b5_cuna(d), 2, out), process("B6 correa", "B6_correa", b6_correa(d), 4, out)]
    for r in rows:
        ok = r["chk"]["ok"] and r["mc"]["watertight"] and r["mc"]["bodies"] == 1 and r["mc"]["fits_bed"]
        if not ok:
            fails.append(f"{r['stem']}: brep={r['chk']} estanco={r['mc']['watertight']} bodies={r['mc']['bodies']} cama={r['mc']['fits_bed']}")
        print(f"{r['stem']:14s} ok={ok} or={r['orient']} bbox={tuple(round(v, 1) for v in r['mc']['bbox'])}", flush=True)
    S_ = {r["stem"]: r["shape"] for r in rows}
    # world parts: (label, stem, shape); the cradles and straps are built in their own frame
    world = [("B1 casco", "B1_casco", S_["B1_casco"]), ("B2 cubierta", "B2_cubierta", S_["B2_cubierta"]), ("B3 caja", "B3_caja", S_["B3_caja"]),
             ("B4 tapa", "B4_tapa", S_["B4_tapa"])]
    if cruz:
        for side, nm in ((1, "D"), (-1, "I")):
            world.append((f"B5 cuna {nm}", "B5_cuna", to_world(S_["B5_cuna"], side, d)))
            ls = d["L1"] if d["poke"] <= 0 else d["yb"] - 22.0
            for k, x in enumerate((-ls, ls)):
                world.append((f"B6 correa {nm}{k + 1}", "B6_correa", to_world(S_["B6_correa"], side, d, (x, 0.0, d["z_top"]))))
    parts = {lab: sh for lab, _st, sh in world}
    dm = {k: v.val() for k, v in dummies(d).items()}
    # interferences (pieces vs pieces and dummies)
    allp = {**parts, **{f"dummy {k}": v for k, v in dm.items()}}
    names = list(allp)
    inter = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a.startswith("dummy") and b.startswith("dummy"):
                continue
            if not _bb_overlap(allp[a], allp[b]):
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
    src = "slicer" if sl and all(r["stem"] in sl for r in rows) else "estimado"
    gp = {s: (sl[s]["g"] if src == "slicer" else est[s]) for s in est}
    hp = {s: (sl[s]["h"] if src == "slicer" else None) for s in est}
    qty = {r["stem"]: r["qty"] for r in rows}
    # masses (global frame): (name, g, z, x, y)
    g = layout(d)
    bm = P.BUOY_MASS
    m_pts = []
    for lab, st, sh in world:
        c = sh.Center()
        m_pts.append((f"{lab} impreso", gp[st], c.z, c.x, c.y))
    mid = lambda k: ((g[k][4] + g[k][5]) / 2, (g[k][0] + g[k][1]) / 2)    # noqa: E731
    comp = [("3 x celdas 18650", P.BUOY_CELLS * bm["celda_18650"], *mid("batt"), 0.0), ("portabaterias", bm["portabaterias"], *mid("batt"), 0.0),
            ("PCB + Heltec", bm["pcb_heltec"], *mid("pcb"), 0.0), ("Waveshare D", bm["waveshare"], *mid("ws"), 0.0), ("RTC", bm["rtc"], *mid("rtc"), 0.0),
            ("panel solar", bm["panel"], (d["z_panel0"] + d["z_panel1"]) / 2, d["X0"], 0.0),
            ("antena LoRa (en el mastil)", bm["antena"], d["z_mast"] - 40, d["x_mast"], 0.0),
            ("cables y fusible", bm["cables_fusible"], g["zf"] + 30, d["X0"], 0.0), ("3 PG7", bm["prensaestopas"] * 1.5, g["zf"] + 30, d["X0"], 0.0),
            ("tornilleria (M3, insertos, junta)", bm["tornilleria"] + (4 * 6 * 1.0 if cruz else 0.0), d["z0"] + 40, d["X0"], 0.0)]
    for i, b_ in enumerate(d["bots"]):
        comp.append((f"botella {i + 1} vacia", d["m_bottle"], d["zc"], b_["x"], b_["y"]))
    foam_V = foam_volume_mm3(d) * P.FLOT_FOAM_FILL
    if P.FLOT_FILL == "espuma_PU":
        comp.append(("espuma PU (masa)", foam_V * P.FLOT_FOAM_DENSITY * 1e-6, d["zc"], d["X0"], 0.0))
    m_pts += comp
    M = sum(m[1] for m in m_pts)
    cg = (sum(m[1] * m[3] for m in m_pts) / M, sum(m[1] * m[4] for m in m_pts) / M, sum(m[1] * m[2] for m in m_pts) / M)
    KG = cg[2]
    base = hydro(d, M, KG, cg[:2])
    buoy_bottles_g = n * d["V"] * P.SEAWATER_DENSITY          # g, fully submerged
    foam_res_g = foam_V * (P.SEAWATER_DENSITY - P.FLOT_FOAM_DENSITY * 1e-3) * 1e-3 if P.FLOT_FILL == "espuma_PU" else 0.0
    tot_g = sum(gp[s] * qty[s] for s in gp)
    tot_h = sum(hp[s] * qty[s] for s in hp) if src == "slicer" else None
    res = dict(botella=bottle, cantidad=n, disposicion=d["layout"], masa_g=M, masa_impresa_g=tot_g, fuente_masa_impresa=src, KG=KG, LCG=cg[0], YCG=cg[1],
               empuje_botellas_g=buoy_bottles_g, reserva_g=buoy_bottles_g - M, reserva_pct=(buoy_bottles_g - M) / M * 100,
               espuma_reserva_estimada_g=foam_res_g, espuma_volumen_cm3=foam_V / 1000, hidro=base,
               dims={k: (round(v, 2) if isinstance(v, float) else v) for k, v in d.items() if k not in ("bots", "bays", "bottle_bases")},
               botellas=[dict(eje=b_["axis"], x=round(b_["x"], 1), y=round(b_["y"], 1)) for b_ in d["bots"]],
               piezas={r_["stem"]: dict(nombre=r_["name"], qty=r_["qty"], orient=r_["orient"], bbox=list(r_["mc"]["bbox"]),
                                        voladizo_mm2=r_["mc"]["overhang_mm2"], volumen_cm3=r_["shape"].Volume() / 1000,
                                        g=gp[r_["stem"]], h=hp[r_["stem"]], g_estimado=est[r_["stem"]]) for r_ in rows},
               masas=[dict(elemento=a, g=b, z=c, x=x_, y=y_) for a, b, c, x_, y_ in m_pts])
    open_edge = g["umb_z"] - P.PG7_HOLE / 2
    open_pt = (d["X0"] - d["Lx"] / 2, 0.0, open_edge)
    objetivos = []
    if base["flota"]:
        T = base["calado"]
        res["francobordo_caja_mm"] = d["z0"] - T
        res["francobordo_tapa_mm"] = d["z_lid_top"] - T
        res["francobordo_cubierta_mm"] = d["z_cover_top"] - T
        res["francobordo_junta_mm"] = d["z_lid"] - T
        res["francobordo_abertura_mm"] = open_edge - T      # lowest opening of the dry box: the umbilical PG7
        if res["francobordo_abertura_mm"] < P.BUOY_FREEBOARD_MIN:
            objetivos.append(f"francobordo a la abertura mas baja de la caja {res['francobordo_abertura_mm']:.1f} < {P.BUOY_FREEBOARD_MIN:g}")
        for ax, k in (("balanceo", "GM_roll"), ("cabeceo", "GM_pitch")):
            if base[k] < GM_TARGET:
                objetivos.append(f"GM de {ax} {base[k]:.0f} < {GM_TARGET:g}")
        if min(base["GM_roll"], base["GM_pitch"]) <= 0:
            fails.append(f"GM no positivo ({base['GM_roll']:.0f} / {base['GM_pitch']:.0f})")
        if abs(base["arm_y"]) > 1.0:
            fails.append(f"centro de empuje fuera del eje en y ({base['arm_y']:.1f} mm)")
        res["verificacion_3d_base"] = attitude(d, M, cg, None, 0.0, open_pt)
    else:
        fails.append("no flota con las botellas y la caja")
    # one bottle lost, each bottle in turn, without and with the estimated foam
    perdida = {}
    foam_disp = foam_V
    for tag, fm in (("sin_espuma", 0.0), ("con_espuma_estimada", foam_disp if P.FLOT_FILL == "espuma_PU" else 0.0)):
        rows_l = []
        for i, b_ in enumerate(d["bots"]):
            Mi = M - d["m_bottle"]
            cgi = tuple((M * cg[k] - d["m_bottle"] * v) / Mi for k, v in enumerate((b_["x"], b_["y"], d["zc"])))
            h1 = hydro(d, Mi, cgi[2], cgi[:2], lost=i, foam_mm3=fm)
            at = attitude(d, Mi, cgi, i, fm, open_pt)
            rows_l.append(dict(botella_perdida=i + 1, eje=b_["axis"], x=round(b_["x"], 1), y=round(b_["y"], 1), masa_g=Mi,
                               empuje_restante_g=(n - 1) * d["V"] * P.SEAWATER_DENSITY, vertical=h1, equilibrio=at))
        perdida[tag] = rows_l
    res["una_botella_perdida"] = perdida
    res["piezas_cabe_cama"] = all(r_["mc"]["fits_bed"] for r_ in rows)
    res["total_impreso_g"], res["total_impreso_h"] = tot_g, tot_h
    res["costo_soles"] = tot_g * P.FILAMENT_PRICE / 1000
    if src == "slicer":
        if tot_g > P.PET_MASS_TARGET:
            objetivos.append(f"masa impresa {tot_g:.0f} g > {P.PET_MASS_TARGET:g}")
        if tot_h > P.PET_TIME_TARGET:
            objetivos.append(f"tiempo {tot_h:.1f} h > {P.PET_TIME_TARGET:g}")
    # verdict of the lost-bottle case (worst bottle): positive GM, small tilt, opening above water
    for tag in perdida:
        peor = max(perdida[tag], key=lambda r_: (not r_["equilibrio"]["estable"], r_["equilibrio"]["inclinacion_deg"]))
        eq_ = peor["equilibrio"]
        ok = (eq_["converge"] and eq_["estable"] and eq_["GM_roll"] > 0 and eq_["GM_pitch"] > 0 and eq_["inclinacion_deg"] <= TILT_MAX
              and eq_.get("francobordo_abertura_mm", -1) > 0 and peor["vertical"].get("flota"))
        res[f"veredicto_perdida_{tag}"] = dict(cumple=bool(ok), peor_botella=peor["botella_perdida"], inclinacion_deg=eq_["inclinacion_deg"],
                                               GM_roll=eq_["GM_roll"], GM_pitch=eq_["GM_pitch"], francobordo_abertura_mm=eq_.get("francobordo_abertura_mm"),
                                               equilibrio_estable=eq_["estable"])
        if not ok and tag == "sin_espuma":
            objetivos.append("con una botella perdida (sin espuma) no cumple: flota derecha, GM > 0, escora pequena y abertura sobre el agua")
    res["fallas"] = fails
    res["objetivos_no_cumplidos"] = objetivos
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
        colr = {"B1": "#3a7ca5", "B2": "#e07b39", "B3": "#3a9d7a", "B4": "#9fb7cc", "B5": "#8e6bbf", "B6": "#c0504d"}
        items = [(sh, colr[k[:2]], 0.55 if k.startswith("B4") else 1.0, True, None) for k, sh in parts.items()]
        for k, sh in dm.items():
            items.append((sh, "#1d1d3a" if k == "panel" else "#5dade2" if k.startswith("botella") else "#c9a227", 0.5 if k.startswith("botella") else 1.0,
                          True, None))
        T = base["calado"] if base["flota"] else 0
        water = box(-500, 500, -300, 300, T - 0.5, T).val()
        title = (f"Boya PET {n} x {bottle} ({d['layout']}): calado {T:.0f} mm, francobordo caja {res.get('francobordo_caja_mm', 0):.0f} mm, {M:.0f} g")
        render(items + [(water, "#7fb3d5", 0.25, False, None)], out / "boya_pet_iso.png", "iso", title)
        cut = box(-700, 700, -500, 0, -100, 500).val()
        render([(sh.cut(cut), c, o, e, None) for sh, c, o, e, _ in items if sh.cut(cut).Volume() > 1e-3]
               + [(water.cut(cut), "#7fb3d5", 0.25, False, None)], out / "boya_pet_corte.png", "frontal",
               "Corte en y = 0 de la boya PET con la linea de agua")
    res["_rows"] = rows
    return res


GM_TARGET = 40.0      # mm, both axes (owner)
TILT_MAX = 10.0       # deg, "small heel" with a bottle lost (estimated criterion)


def _num(o):
    if isinstance(o, (np.floating, np.integer)):
        return o.item()
    if isinstance(o, np.bool_):
        return bool(o)
    return str(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--botella", default=P.FLOT_BOTTLE)
    ap.add_argument("--cantidad", type=int, default=P.FLOT_COUNT)
    ap.add_argument("--sin-slicer", action="store_true")
    ap.add_argument("--alternativas", action="store_true", help="also model the other bottle types (no slicing)")
    ap.add_argument("--salida", default=str(OUT), help="output folder (default salida/boya_pet)")
    ap.add_argument("--limpiar-stl", action="store_true", help="delete stl/ and step/ after the run (comparison configs)")
    a = ap.parse_args()
    out = Path(a.salida).resolve()
    res = run(a.botella, a.cantidad, out, not a.sin_slicer)
    alts = {}
    if a.alternativas:
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
    (out / "resultados.json").write_text(json.dumps(clean, indent=1, ensure_ascii=False, default=_num), encoding="utf-8")
    if out == OUT:
        write_report(res, alts, out)
    h = res.get("hidro", {})
    if h.get("flota"):
        print(f"boya {res['masa_g']:.0f} g (impreso {res['total_impreso_g']:.0f} g, {res['fuente_masa_impresa']}), calado {h['calado']:.1f}, "
              f"francobordo abertura {res['francobordo_abertura_mm']:.1f}, reserva {res['reserva_pct']:.0f} %, GM {h['GM_roll']:.0f}/{h['GM_pitch']:.0f}")
    print("OBJETIVOS NO CUMPLIDOS:", res["objetivos_no_cumplidos"] if res["objetivos_no_cumplidos"] else "ninguno")
    print("FALLAS:", res["fallas"] if res["fallas"] else "ninguna")
    if a.limpiar_stl:
        for sub in ("stl", "step"):
            shutil.rmtree(out / sub, ignore_errors=True)
    return 1 if res["fallas"] else 0


def write_report(r, alts, out=OUT):
    h = r["hidro"]
    Ls = ["# Boya con botellas PET (generado por `boya_pet.py`)", "",
          f"{r['cantidad']} botellas de {r['botella']} ({r['disposicion']}), relleno {P.FLOT_FILL}. Masas impresas: {r['fuente_masa_impresa']}.", "",
          "| Magnitud | Valor |", "|---|---|", f"| Masa total boya | {r['masa_g']:.0f} g |",
          f"| Calado | {h['calado']:.1f} mm |", f"| Francobordo a la abertura mas baja de la caja | {r['francobordo_abertura_mm']:.1f} mm |",
          f"| Reserva | {r['reserva_pct']:.0f} % |", f"| GM balanceo / cabeceo | {h['GM_roll']:.0f} / {h['GM_pitch']:.0f} mm |", "",
          "## Chequeos geometricos que fallaron", ""] + ([f"- {f}" for f in r["fallas"]] if r["fallas"] else ["- ninguno"]) + \
         ["", "## Objetivos no cumplidos", ""] + ([f"- {f}" for f in r["objetivos_no_cumplidos"]] if r["objetivos_no_cumplidos"] else ["- ninguno"])
    (HERE / "reporte_boya_pet.md").write_text("\n".join(Ls) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
