"""Central box, Fase A level: M1 body and M2 lid as PRELIMINARY envelopes sized from layout.py, the M11
tray (split der/izq) and the module dummies. Detailing (rail seat, gaskets at the cable passes, final
handle) is Fase C.

Frame as layout.py: X along the rail, box centred on x = y = 0, outer bottom z = 0.
The handle and the flange/skirt follow cad/parts.py (box_lid, box_body) with diff minimum.
"""
import math

import cadquery as cq

import layout as LY
from params import (BASE_M4_BOSS, BASE_M4_PTS, BOX_FLANGE, BOX_FLANGE_T, BOX_FLOOR, BOX_LID_T, BOX_SCREW_PITCH,
                    BOX_WALL, COMPONENTS, GAP_WALL, GROOVE_DEPTH, GROOVE_WIDTH, HANDLE_GRIP, HANDLE_H,
                    M3_CLEAR, M3_INSERT_DEPTH, M3_INSERT_HOLE, M4_INSERT_DEPTH, M4_INSERT_HOLE, PG7_HOLE,
                    PG7_INNER_H, PG7_NUT_AF, POCKET_DEPTH, POCKET_L, POCKET_RAIL_GAP, POCKET_WALL,
                    RAIL_CENTRAL_L, RAIL_SECTION, RAIL_WALL, TRAY_BOSS_D, TRAY_BOSS_INSET, TRAY_CRADLE_T,
                    TRAY_STANDOFF, TRAY_T)


# ------------------------------------------------------------------ positions
def screw_pts(lay):
    """M3 lid screws on the flange centreline, spaced <= BOX_SCREW_PITCH."""
    out_l, out_w, _ = lay.box_outer()
    a, b = out_l / 2 + BOX_FLANGE / 2, out_w / 2 + BOX_FLANGE / 2
    nx = math.ceil(2 * a / BOX_SCREW_PITCH)
    ny = math.ceil(2 * b / BOX_SCREW_PITCH)
    pts = [(-a + 2 * a * k / nx, s * b) for k in range(nx + 1) for s in (1, -1)]
    pts += [(s * a, -b + 2 * b * k / ny) for k in range(1, ny) for s in (1, -1)]
    return pts


def tray_boss_pts(lay):
    """Four per tray half: two at the outer corners, two near the split line."""
    out = []
    for x0, x1, y0, y1 in lay.tray_halves().values():
        for x in (x0 + TRAY_BOSS_INSET, x1 - TRAY_BOSS_INSET):
            for y in (y0 + TRAY_BOSS_INSET, y1 - TRAY_BOSS_INSET):
                out.append((x, y))
    return out


def pocket_rects(lay):
    """Ballast pockets under the floor, beside the rail (never under it): (x0, x1, y0, y1)."""
    _, out_w, _ = lay.box_outer()
    y0 = RAIL_SECTION / 2 + POCKET_RAIL_GAP
    return [(-POCKET_L / 2, POCKET_L / 2, y0, out_w / 2),
            (-POCKET_L / 2, POCKET_L / 2, -out_w / 2, -y0)]


def _box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def _hex(cx, cy, af, z0, h):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).polygon(6, af / math.cos(math.pi / 6)).extrude(h)


# ------------------------------------------------------------------ M1
def cavity_tool(lay):
    L, W, H = lay.cav
    return cq.Workplane("XY").workplane(offset=BOX_FLOOR).rect(L, W).extrude(H).edges("|Z").fillet(3)


def box_body(lay):
    out_l, out_w, out_h = lay.box_outer()
    body = cq.Workplane("XY").rect(out_l, out_w).extrude(out_h).edges("|Z").fillet(5)
    flange = (cq.Workplane("XY").workplane(offset=out_h - BOX_FLANGE_T)
              .rect(out_l + 2 * BOX_FLANGE, out_w + 2 * BOX_FLANGE).extrude(BOX_FLANGE_T).edges("|Z").fillet(6))
    z_sk = out_h - BOX_FLANGE_T
    skirt = (cq.Workplane("XY").workplane(offset=z_sk - BOX_FLANGE).rect(out_l, out_w)
             .workplane(offset=BOX_FLANGE).rect(out_l + 2 * BOX_FLANGE, out_w + 2 * BOX_FLANGE).loft())
    body = body.union(flange).union(skirt).cut(cavity_tool(lay))
    # M3 heat-set inserts for the lid
    for (x, y) in screw_pts(lay):
        body = body.cut(cq.Workplane("XY").workplane(offset=out_h - M3_INSERT_DEPTH).center(x, y)
                        .circle(M3_INSERT_HOLE / 2).extrude(M3_INSERT_DEPTH))
    # floor glands (cameras -> rail)
    for (x, y) in lay.floor_glands:
        body = body.cut(cq.Workplane("XY").center(x, y).circle(PG7_HOLE / 2).extrude(BOX_FLOOR))
    # rail seat: 4 blind M4 inserts from below into inner bosses (the seal is not pierced)
    d, h = BASE_M4_BOSS
    for (x, y) in BASE_M4_PTS:
        body = body.union(cq.Workplane("XY").workplane(offset=BOX_FLOOR).center(x, y).circle(d / 2).extrude(h))
        body = body.cut(cq.Workplane("XY").center(x, y).circle(M4_INSERT_HOLE / 2).extrude(M4_INSERT_DEPTH))
    # tray bosses with M3 inserts
    for (x, y) in tray_boss_pts(lay):
        body = body.union(cq.Workplane("XY").workplane(offset=BOX_FLOOR).center(x, y)
                          .circle(TRAY_BOSS_D / 2).extrude(TRAY_STANDOFF))
        body = body.cut(cq.Workplane("XY").workplane(offset=BOX_FLOOR + TRAY_STANDOFF - M3_INSERT_DEPTH)
                        .center(x, y).circle(M3_INSERT_HOLE / 2).extrude(M3_INSERT_DEPTH))
    # ballast pockets, open at the bottom (cover plate in Fase C), outside the seal
    for (x0, x1, y0, y1) in pocket_rects(lay):
        outer = _box(x0, x1, y0, y1, -POCKET_DEPTH, 0.0)
        inner = _box(x0 + POCKET_WALL, x1 - POCKET_WALL, y0 + POCKET_WALL, y1 - POCKET_WALL, -POCKET_DEPTH, 0.0)
        body = body.union(outer.cut(inner))
    return body


def pocket_volume_cm3(lay):
    return sum((x1 - x0 - 2 * POCKET_WALL) * (y1 - y0 - 2 * POCKET_WALL) * POCKET_DEPTH
               for x0, x1, y0, y1 in pocket_rects(lay)) / 1000.0


# ------------------------------------------------------------------ M2
def box_lid(lay):
    out_l, out_w, out_h = lay.box_outer()
    L, W, _ = lay.cav
    z0 = out_h
    lid = (cq.Workplane("XY").workplane(offset=z0).rect(out_l + 2 * BOX_FLANGE, out_w + 2 * BOX_FLANGE)
           .extrude(BOX_LID_T).edges("|Z").fillet(6))
    for (x, y) in screw_pts(lay):
        lid = lid.cut(cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(M3_CLEAR / 2).extrude(BOX_LID_T))
    # O-ring groove on the inner face, midway between the cavity and the screw line
    cl_l = (L + out_l + BOX_FLANGE) / 2
    cl_w = (W + out_w + BOX_FLANGE) / 2
    outer = (cq.Workplane("XY").workplane(offset=z0).rect(cl_l + GROOVE_WIDTH, cl_w + GROOVE_WIDTH)
             .extrude(GROOVE_DEPTH).edges("|Z").fillet(6))
    inner = (cq.Workplane("XY").workplane(offset=z0).rect(cl_l - GROOVE_WIDTH, cl_w - GROOVE_WIDTH)
             .extrude(GROOVE_DEPTH).edges("|Z").fillet(3.5))
    lid = lid.cut(outer.cut(inner))
    gx, gy = lay.lid_gland
    lid = lid.cut(cq.Workplane("XY").workplane(offset=z0).center(gx, gy).circle(PG7_HOLE / 2).extrude(BOX_LID_T))
    # handle: arch over y = 0, glove-sized opening, anchor eye on top (cad/parts.py box_lid)
    zt = z0 + BOX_LID_T
    leg = 12.0
    span = HANDLE_GRIP + 2 * leg
    handle = cq.Workplane("XZ").workplane(offset=-6).center(0, zt + HANDLE_H / 2).rect(span, HANDLE_H).extrude(12)
    hw, wall_h = HANDLE_GRIP / 2, 8.0
    roof = HANDLE_H - 10 - wall_h
    window = (cq.Workplane("XZ").workplane(offset=-6)
              .polyline([(-hw, zt), (hw, zt), (hw, zt + wall_h), (hw - roof, zt + wall_h + roof),
                         (-hw + roof, zt + wall_h + roof), (-hw, zt + wall_h)]).close().extrude(12))
    handle = handle.cut(window).edges("|Y").fillet(3)
    eye = cq.Workplane("XZ").workplane(offset=-6).center(0, zt + HANDLE_H + 6).circle(10).circle(5).extrude(12)
    return lid.union(handle).union(eye)


# ------------------------------------------------------------------ M11 tray + dummies
def trays(lay):
    """{name: Workplane} for each tray piece, with the access holes around the floor glands."""
    out = {}
    zt = lay.z_tray
    esp = next(b for n, k, b in lay.modules if n == "esp32")
    for name, (x0, x1, y0, y1) in lay.tray_halves().items():
        t = _box(x0, x1, y0, y1, zt - TRAY_T, zt).edges("|Z").fillet(2)
        for (gx, gy) in lay.floor_glands:
            t = t.cut(cq.Workplane("XY").workplane(offset=zt - TRAY_T).center(gx, gy)
                      .circle(lay.access_r).extrude(TRAY_T))
        for (x, y) in tray_boss_pts(lay):
            if x0 <= x <= x1:
                t = t.cut(cq.Workplane("XY").workplane(offset=zt - TRAY_T).center(x, y)
                          .circle(M3_CLEAR / 2).extrude(TRAY_T))
        ex0, ex1, ey0, ey1 = esp.xy
        if lay.base == "sin_base" and x0 <= ex0 and ex1 <= x1:
            # cradle: two ledges under the short ends of the DevKit, raising it CLR_PINS for the duponts
            for ya, yb in ((ey0, ey0 + TRAY_CRADLE_T), (ey1 - TRAY_CRADLE_T, ey1)):
                t = t.union(_box(ex0, ex1, ya, yb, zt, esp.z[0]))
        out[name] = t
    return out


def module_dummies(lay):
    return [(name, _box(*b.xy, *b.z)) for name, key, b in lay.modules]


def keepout_solids(lay):
    """(name, kind, solid) for every free zone, for the renders."""
    out = []
    for it in lay.items:
        if it.kind == "cuerpo":
            continue
        if it.shape == "box":
            s = _box(*it.xy, *it.z)
        else:
            cx, cy, r = it.xy
            s = cq.Workplane("XY").workplane(offset=it.z[0]).center(cx, cy).circle(r).extrude(it.z[1] - it.z[0])
        out.append((it.name, it.kind, s))
    return out


def gland_nuts(lay):
    """Locknuts as hex prisms: two on the floor, the umbilical one hanging from the lid."""
    nuts = [_hex(x, y, PG7_NUT_AF, BOX_FLOOR, PG7_INNER_H) for (x, y) in lay.floor_glands]
    zl = BOX_FLOOR + lay.cav[2]
    nuts.append(_hex(*lay.lid_gland, PG7_NUT_AF, zl - PG7_INNER_H, PG7_INNER_H))
    return nuts


def rail_reference():
    """Central rail as a plain hollow bar (context only; the real M3_riel_central is Fase C)."""
    s, t = RAIL_SECTION, RAIL_WALL
    bar = cq.Workplane("YZ").workplane(offset=-RAIL_CENTRAL_L / 2).center(0, -s / 2).rect(s, s).extrude(RAIL_CENTRAL_L)
    return bar.cut(cq.Workplane("YZ").workplane(offset=-RAIL_CENTRAL_L / 2).center(0, -s / 2)
                   .rect(s - 2 * t, s - 2 * t).extrude(RAIL_CENTRAL_L))
