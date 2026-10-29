"""M3_riel_central as a cable chamber under the box (revision 28/10, C12), and the ballast plate pockets (C13).

Frame as layout.py: X along the rail, box centred on x = y = 0, box outer bottom z = 0 (the chamber hangs below).
Every height is derived:
  interior height (floor to box underside) = PG7 dome + bend radius + cable radius + T-slot rib,
so the Cat5e leaves the dome downward, turns 90 deg with R >= CABLE_BEND_R_MIN and lands on the rib tops at
the conduit height of the extensions. Toward each end the roof ramps down to the 22 mm conduit before the
dovetail zone. Level of detail: reference for mass, volume and the cable check; joints and T-slot detail are
Fase C.
"""
import math
from dataclasses import dataclass

import cadquery as cq

from params import (BASE_M4_PTS, CABLE_BEND_K, CABLE_BEND_R_MIN, CAT5E_D, CHAMBER_FLANGE_W, CHAMBER_RAMP_DEG,
                    M4_CLEAR, PG7_DOME, PLATE_BAR, PLATE_CLR, PLATE_L, PLATE_LEVEL, PLATE_POCKET_WALL, PLATE_POCKET_Y0,
                    PLATE_SIDES, RAIL_CENTRAL_L, RAIL_DOVETAIL, RAIL_SECTION, RAIL_TSLOT, RAIL_TSLOT_RIB,
                    RAIL_WALL)


@dataclass
class Chamber:
    bend_r: float          # cable bend radius used
    h_int: float           # chamber floor to box underside
    z_floor: float         # chamber floor (= conduit floor of the extensions)
    z_rail: float          # rail bottom
    z_conduit_top: float
    x_high: float          # |x| up to which the chamber is open to the box underside
    x_joint: float         # |x| where the standard section (dovetail zone) starts
    z_cable: float         # cable centreline on the horizontal run
    flange_w: float
    checks: dict


def bend_radius():
    return max(CABLE_BEND_K * CAT5E_D, CABLE_BEND_R_MIN)


def dims(lay):
    s, t = RAIL_SECTION, RAIL_WALL
    ft = CHAMBER_FLANGE_W[1]
    dome_d, dome_l = PG7_DOME
    R = bend_radius()
    rib = RAIL_TSLOT["alto"]
    h_int = dome_l + R + CAT5E_D / 2 + rib
    z_floor = -h_int
    z_rail = z_floor - t
    z_ct = z_rail + s - t
    x_joint = RAIL_CENTRAL_L / 2 - RAIL_DOVETAIL
    drop = (-ft) - z_ct
    x_high = x_joint - drop / math.tan(math.radians(CHAMBER_RAMP_DEG))
    z_cable = -dome_l - R
    gx = max(abs(x) for x, _ in lay.floor_glands)

    def roof(x):
        x = abs(x)
        if x <= x_high:
            return 0.0
        return max(z_ct, -ft - (x - x_high) * math.tan(math.radians(CHAMBER_RAMP_DEG)))

    # sample the cable centreline: dome tip, 90 deg arc, horizontal run to the end of the piece
    worst = math.inf
    for k in range(91):
        ph = math.radians(k)
        x, z = gx + R - R * math.cos(ph), -dome_l - R * math.sin(ph)
        worst = min(worst, roof(x) - (z + CAT5E_D / 2))
    for k in range(101):
        x = gx + R + (RAIL_CENTRAL_L / 2 - gx - R) * k / 100
        worst = min(worst, roof(x) - (z_cable + CAT5E_D / 2))
    pts = [(x, y) for x, y in BASE_M4_PTS]
    checks = {
        "radio_curva_ok": R >= CABLE_BEND_R_MIN,
        "cable_sobre_nervios": z_cable - CAT5E_D / 2 >= z_floor + rib - 1e-9,
        "cable_en_conducto": z_cable + CAT5E_D / 2 <= z_ct + 1e-9,
        "tramo_recto_antes_de_la_union": gx + R <= x_joint,
        "holgura_min_techo": worst,
        "domo_en_la_abertura": gx + dome_d / 2 <= x_high and dome_d / 2 <= s / 2 - t,
        "m4_fuera_de_la_camara": all(abs(y) - M4_CLEAR / 2 >= s / 2 for _, y in pts),
    }
    checks["ok"] = all(v for k, v in checks.items() if k != "holgura_min_techo") and worst >= 0
    flange_w = CHAMBER_FLANGE_W[0] if PLATE_LEVEL == "abajo" else max(CHAMBER_FLANGE_W[0], 2 * pocket_y1())
    return Chamber(R, h_int, z_floor, z_rail, z_ct, x_high, x_joint, z_cable, flange_w, checks)


# ------------------------------------------------------------------ ballast plates
def plate_mass_g():
    from params import STEEL_DENSITY
    w, th = PLATE_BAR
    return w * th * PLATE_L * STEEL_DENSITY / 1000.0


def pocket_y0():
    """Inner face of a plate pocket (|y|): the chamber wall itself ('abajo') or clear of the M4 heads ('brida')."""
    return RAIL_SECTION / 2 if PLATE_LEVEL == "abajo" else PLATE_POCKET_Y0 + PLATE_POCKET_WALL


def pocket_y1():
    """Outer face of a plate pocket (|y|)."""
    return pocket_y0() + PLATE_BAR[0] + 2 * PLATE_CLR + PLATE_POCKET_WALL


def pocket_z(c, layers):
    """(z of the cover bottom, z of the lowest plate, z of the pocket roof top) for the chosen level."""
    w, d = PLATE_POCKET_WALL, pocket_depth(layers)
    if PLATE_LEVEL == "abajo":
        return c.z_rail, c.z_rail + w, c.z_rail + w + d + w
    ft = CHAMBER_FLANGE_W[1]
    return -ft - d - w, -ft - d, -ft


def pocket_depth(layers):
    return layers * PLATE_BAR[1] + PLATE_CLR


def _box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def _xz(pts, y0, y1):
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts).close().extrude(y1 - y0)


def chamber_solid(lay, layers):
    """{name: Workplane}: the central piece (chamber + flange + plate pockets, open at the bottom) and the two
    pocket covers. `layers` = plates stacked per side."""
    c = dims(lay)
    s, t = RAIL_SECTION, RAIL_WALL
    ft = CHAMBER_FLANGE_W[1]
    L2 = RAIL_CENTRAL_L / 2
    hw = s / 2
    body = _box(-L2, L2, -hw, hw, c.z_rail, -ft)
    body = body.union(_box(-L2, L2, -c.flange_w / 2, c.flange_w / 2, -ft, 0.0))
    # interior profile (XZ), extruded over the conduit width
    tan = math.tan(math.radians(CHAMBER_RAMP_DEG))
    xr = c.x_high + (-ft - c.z_conduit_top) / tan
    prof = [(-L2 - 1, c.z_floor), (L2 + 1, c.z_floor), (L2 + 1, c.z_conduit_top), (xr, c.z_conduit_top),
            (c.x_high, -ft), (c.x_high, 1.0), (-c.x_high, 1.0), (-c.x_high, -ft), (-xr, c.z_conduit_top),
            (-L2 - 1, c.z_conduit_top)]
    body = body.cut(_xz(prof, -(hw - t), hw - t))
    # T-slot: opening through the bottom wall, nut channel between two ribs on the floor
    ts = RAIL_TSLOT
    body = body.cut(_box(-L2 - 1, L2 + 1, -ts["abertura"] / 2, ts["abertura"] / 2, c.z_rail - 1, c.z_floor + 0.01))
    for sg in (1, -1):
        y0 = sg * ts["ancho"] / 2
        y1 = sg * (ts["ancho"] / 2 + RAIL_TSLOT_RIB)
        body = body.union(_box(-L2, L2, min(y0, y1), max(y0, y1), c.z_floor - 0.01, c.z_floor + ts["alto"]))
    # M4 to the box, through the flange
    for x, y in BASE_M4_PTS:
        body = body.cut(cq.Workplane("XY").workplane(offset=-ft - 1).center(x, y).circle(M4_CLEAR / 2).extrude(ft + 2))
    # plate pockets, open at the bottom (cover screwed on, flush with the rail bottom when 'abajo')
    out = {}
    if layers > 0:
        w = PLATE_POCKET_WALL
        px = PLATE_L / 2 + PLATE_CLR
        zc, zp, zr = pocket_z(c, layers)
        ya, yb = pocket_y0(), pocket_y1()
        for sg, side in ((1, "n"), (-1, "s"))[:PLATE_SIDES]:
            y0, y1 = (ya - 0.01, yb) if sg > 0 else (-yb, -ya + 0.01)
            outer = _box(-px - w, px + w, y0, y1, zc + w, zr)
            inner = _box(-px, px, (ya if sg > 0 else -yb + w), (yb - w if sg > 0 else -ya), zc + w - 1, zr - w)
            body = body.union(outer.cut(inner))
            out[f"tapa_bolsillo_{side}"] = _box(-px - w, px + w, y0, y1, zc, zc + w)
    out["M3_riel_central"] = body
    return out


def plates_solid(lay, layers):
    """Steel plates in place, stacked up from the pocket floor (for renders and the centre of mass)."""
    c = dims(lay)
    w, th = PLATE_BAR
    _, zp, _ = pocket_z(c, layers)
    y0 = pocket_y0() + PLATE_CLR
    out = []
    for sg in (1, -1)[:PLATE_SIDES]:
        for k in range(layers):
            ya, yb = (y0, y0 + w) if sg > 0 else (-y0 - w, -y0)
            out.append(_box(-PLATE_L / 2, PLATE_L / 2, ya, yb, zp + k * th, zp + (k + 1) * th))
    return out


def extension_solid(n_side, c):
    """Plain extension tramos (section x length) on both sides of the chamber, for renders."""
    s, t = RAIL_SECTION, RAIL_WALL
    out = []
    for sg in (1, -1):
        for k in range(n_side):
            from params import RAIL_EXT_L
            x0 = RAIL_CENTRAL_L / 2 + k * RAIL_EXT_L
            xa, xb = (x0, x0 + RAIL_EXT_L) if sg > 0 else (-x0 - RAIL_EXT_L, -x0)
            bar = _box(xa, xb, -s / 2, s / 2, c.z_rail, c.z_rail + s)
            out.append(bar.cut(_box(xa - 1, xb + 1, -s / 2 + t, s / 2 - t, c.z_rail + t, c.z_rail + s - t)))
    return out
