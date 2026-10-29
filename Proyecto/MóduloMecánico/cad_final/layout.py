"""Central box layout in plain numbers (no CadQuery): where every module, keep-out zone and gland goes,
and the cavity that results. The cavity is DERIVED from the layout, never entered by hand.

Frame: X along the rail, Y across, Z up; box centred on x = y = 0 (over the rail), outer bottom z = 0.

Zone kinds and the overlap rule
  cuerpo : a solid (module, locknut). Overlaps nothing.
  cable  : free space for wires (15 mm over the pins, 10 mm on each connector side).
  acceso : free space for a hand or a plug (20 mm around each PG7 locknut, USB plug, microSD card).
  cable and acceso zones may overlap each other (wires are flexible and access is occasional), but never
  a cuerpo. A module's own zones are not checked against its own body.
"""
import math
from dataclasses import dataclass, field

from params import (BOX_FLANGE, BOX_FLOOR, BOX_LID_GAP, BOX_LID_T, BOX_WALL, CLR_CONN, CLR_NUT, CLR_PINS,
                    CLR_SD, CLR_USB, COMPONENTS, CONNECTORS, ESP32_BASE, GAP_MOD, GAP_WALL, PG7_INNER_H,
                    PIECE_MAX_L, PRINT_BED, TRAY_SPLIT, TRAY_STANDOFF, TRAY_T, UMB_GLAND_XY, nut_corner_r)

ACCESS_DEPTH = {"usb": CLR_USB, "microsd": CLR_SD}
TOP = None   # z1 placeholder: zone open up to the lid


@dataclass
class Item:
    name: str
    kind: str                 # cuerpo | cable | acceso
    group: str                # owner (a module never conflicts with its own zones)
    shape: str                # box | cyl
    xy: tuple                 # box: (x0, x1, y0, y1); cyl: (cx, cy, r)
    z: list                   # [z0, z1]; z1 may be TOP until the cavity height is known
    on_lid: bool = False      # mounted on the lid: absent while the lid is off, so access zones ignore it

    def bbox2(self):
        if self.shape == "box":
            return self.xy
        cx, cy, r = self.xy
        return (cx - r, cx + r, cy - r, cy + r)


@dataclass
class Layout:
    base: str
    items: list = field(default_factory=list)
    floor_glands: list = field(default_factory=list)   # (x, y)
    lid_gland: tuple = (0.0, 0.0)
    access_r: float = 0.0
    cav: tuple = (0.0, 0.0, 0.0)                        # L, W, H of the cavity
    z_floor: float = BOX_FLOOR
    z_tray: float = 0.0                                 # tray top face
    modules: list = field(default_factory=list)         # (name, comp key, body Item)

    # ------------------------------------------------------------ derived sizes
    def box_outer(self):
        L, W, H = self.cav
        return (L + 2 * BOX_WALL, W + 2 * BOX_WALL, BOX_FLOOR + H)

    def box_with_flange(self):
        L, W, H = self.box_outer()
        return (L + 2 * BOX_FLANGE, W + 2 * BOX_FLANGE, H + BOX_LID_T)

    def fits_bed(self):
        L, W, H = self.box_with_flange()
        return L <= PRINT_BED[0] and W <= PRINT_BED[1] and H <= PRINT_BED[2]

    def tray_halves(self):
        """Plan bbox of each tray piece (x0, x1, y0, y1): cavity inset by GAP_WALL, split at x = 0."""
        L, W, _ = self.cav
        hx, hy = L / 2 - GAP_WALL, W / 2 - GAP_WALL
        if not TRAY_SPLIT:
            return {"M11_bandeja": (-hx, hx, -hy, hy)}
        g = GAP_MOD / 2
        return {"M11_bandeja_izq": (-hx, -g, -hy, hy), "M11_bandeja_der": (g, hx, -hy, hy)}


def _place(lay, key, name, orient, x0, y0, z0, su=1, sv=1, pins=None, group=None):
    """Body of COMPONENTS[key] with its min corner at (x0, y0, z0); u along `orient` ('X' or 'Y').
    su/sv = +1 if local u+/v+ point to the positive global axis."""
    L, W, H, _ = COMPONENTS[key]
    dx, dy = (L, W) if orient == "X" else (W, L)
    body = Item(name, "cuerpo", group or name, "box", (x0, x0 + dx, y0, y0 + dy), [z0, z0 + H])
    lay.items.append(body)
    lay.modules.append((name, key, body))
    con = CONNECTORS[key]
    pins = pins or con["pines"]
    x1, y1, z1 = x0 + dx, y0 + dy, z0 + H
    g = group or name
    if pins == "arriba":
        lay.items.append(Item(f"{name}:pines", "cable", g, "box", (x0, x1, y0, y1), [z1, z1 + CLR_PINS]))
        ztop = z1 + CLR_PINS
    elif pins == "abajo":
        lay.items.append(Item(f"{name}:pines", "cable", g, "box", (x0, x1, y0, y1), [z0 - CLR_PINS, z0]))
        ztop = z1
    else:
        ztop = z1

    def face(side, depth):
        axis_u = orient == "X"
        local, sgn = side[0], (1 if side[1] == "+" else -1)
        s = sgn * (su if local == "u" else sv)
        along_x = (local == "u") == axis_u
        if along_x:
            return (x1, x1 + depth, y0, y1) if s > 0 else (x0 - depth, x0, y0, y1)
        return (x0, x1, y1, y1 + depth) if s > 0 else (x0, x1, y0 - depth, y0)

    zc0 = z0 - CLR_PINS if pins == "abajo" else z0
    for side in con["conector"]:
        lay.items.append(Item(f"{name}:conector{side}", "cable", g, "box", face(side, CLR_CONN), [zc0, ztop]))
    for side, what in con["acceso"].items():
        lay.items.append(Item(f"{name}:{what}", "acceso", g, "box", face(side, ACCESS_DEPTH[what]), [z0, TOP]))
    return body


def build(base=ESP32_BASE, clr_nut=CLR_NUT):
    """clr_nut is a what-if switch for the report; the design value is params.CLR_NUT."""
    lay = Layout(base=base)
    rc = nut_corner_r()
    rk = rc + clr_nut                     # access radius around each floor locknut
    gx = rc + clr_nut / 2                 # gland x: corner-to-corner distance between the two nuts = clr_nut
    lay.access_r = rk
    lay.floor_glands = [(gx, 0.0), (-gx, 0.0)]
    zf = BOX_FLOOR
    lay.z_tray = zt = zf + TRAY_STANDOFF + TRAY_T
    for k, (x, y) in enumerate(lay.floor_glands):
        nm = f"pg7_fondo_{'der' if x > 0 else 'izq'}"
        lay.items.append(Item(nm, "cuerpo", nm, "cyl", (x, y, rc), [zf, zf + PG7_INNER_H]))
        lay.items.append(Item(f"{nm}:acceso", "acceso", nm, "cyl", (x, y, rk), [zf, TOP]))
    sx, sy = gx + rk, rk                  # bbox of the two access columns

    # bands beside the access columns (y > 0 north, y < 0 south); each body stays on one tray half
    yb = sy + GAP_MOD
    L, W, *_ = COMPONENTS["hw517"]
    _place(lay, "hw517", "hw517_1", "X", -GAP_MOD - L, yb, zt)
    _place(lay, "mpu6050", "mpu6050", "X", -GAP_MOD + CLR_CONN, yb, zt)          # clear of hw517_1's u+ zone; header (v-) toward -Y
    _place(lay, "hw517", "hw517_2", "X", GAP_MOD, -yb - W, zt)

    # +X end block: ESP32 along Y, USB toward +Y
    xe = sx + GAP_MOD
    Ld, Wd, Hd, _ = COMPONENTS["esp32_devkitc1"]
    if base == "sin_base":
        y0 = -(Ld + CLR_USB) / 2
        _place(lay, "esp32_devkitc1", "esp32", "Y", xe, y0, zt + CLR_PINS)     # cradle: dupont zone below
    else:
        Lk, Wk, Hk, _ = COMPONENTS["kit_a"]
        y0 = -(Lk + CLR_USB) / 2
        _place(lay, "kit_a", "kit_a", "Y", xe, y0, zt)
        # the DevKit plugs into the KIT A sockets: same group, its pins are inside the KIT A zone
        _place(lay, "esp32_devkitc1", "esp32", "Y", xe + (Wk - Wd) / 2, y0 + (Lk - Ld) / 2, zt + Hk,
               pins="ninguno", group="kit_a")

    # -X end block: microSD along Y (card toward +Y), XY-017 outboard of it
    Lm, Wm, *_ = COMPONENTS["microsd"]
    xm1 = -xe
    _place(lay, "microsd", "microsd", "Y", xm1 - Wm, -(Lm + CLR_CONN + CLR_SD) / 2 + CLR_CONN, zt)
    Lx, Wx, *_ = COMPONENTS["xy017"]
    _place(lay, "xy017", "xy017", "Y", xm1 - Wm - GAP_MOD - Wx, -Lx / 2, zt)

    # cavity: symmetric about x = y = 0 (box centred on the rail)
    hx = hy = 0.0
    ztop = 0.0
    for it in lay.items:
        x0, x1, y0, y1 = it.bbox2()
        pad = GAP_WALL if it.kind == "cuerpo" else 0.0
        if it.kind == "acceso" and it.shape == "cyl":
            pad = 0.0
        hx = max(hx, abs(x0) + pad, abs(x1) + pad)
        hy = max(hy, abs(y0) + pad, abs(y1) + pad)
        if it.z[1] is not TOP:
            ztop = max(ztop, it.z[1])
    ztop += BOX_LID_GAP
    # umbilical locknut hangs from the lid, inside the free central zone
    lay.lid_gland = UMB_GLAND_XY
    lay.items.append(Item("pg7_umbilical", "cuerpo", "pg7_umbilical", "cyl", (*UMB_GLAND_XY, rc),
                          [ztop - PG7_INNER_H, ztop], on_lid=True))
    for it in lay.items:
        if it.z[1] is TOP:
            it.z[1] = ztop
    lay.cav = (2 * hx, 2 * hy, ztop - zf)
    return lay


# ------------------------------------------------------------------ checks
def _overlap(a, b, tol=1e-6):
    if a.z[1] <= b.z[0] + tol or b.z[1] <= a.z[0] + tol:
        return False
    if a.shape == "cyl" and b.shape == "cyl":
        (ax, ay, ar), (bx, by, br) = a.xy, b.xy
        return math.hypot(ax - bx, ay - by) < ar + br - tol
    if a.shape == "cyl" or b.shape == "cyl":
        c, r_ = (a, b) if a.shape == "cyl" else (b, a)
        cx, cy, r = c.xy
        x0, x1, y0, y1 = r_.xy
        dx = max(x0 - cx, 0, cx - x1)
        dy = max(y0 - cy, 0, cy - y1)
        return math.hypot(dx, dy) < r - tol
    ax0, ax1, ay0, ay1 = a.xy
    bx0, bx1, by0, by1 = b.xy
    return ax0 < bx1 - tol and bx0 < ax1 - tol and ay0 < by1 - tol and by0 < ay1 - tol


def conflicts(lay):
    """Pairs that break the rule: a body against anything that is not its own."""
    out = []
    its = lay.items
    for i, a in enumerate(its):
        for b in its[i + 1:]:
            if a.group == b.group or (a.kind != "cuerpo" and b.kind != "cuerpo"):
                continue
            if (a.on_lid and b.kind == "acceso") or (b.on_lid and a.kind == "acceso"):
                continue
            if _overlap(a, b):
                out.append((a.name, b.name))
    return out


def inside_cavity(lay, tol=1e-6):
    L, W, H = lay.cav
    bad = []
    for it in lay.items:
        x0, x1, y0, y1 = it.bbox2()
        if x0 < -L / 2 - tol or x1 > L / 2 + tol or y0 < -W / 2 - tol or y1 > W / 2 + tol:
            bad.append(it.name)
        if it.z[0] < lay.z_floor - tol or it.z[1] > lay.z_floor + H + tol:
            bad.append(it.name)
    return bad


def tray_bodies_ok(lay):
    """Every module body lies entirely on one tray half (none straddles the split)."""
    halves = lay.tray_halves()
    out = {}
    for name, key, body in lay.modules:
        x0, x1, y0, y1 = body.xy
        home = [h for h, (a0, a1, b0, b1) in halves.items() if a0 <= x0 and x1 <= a1 and b0 <= y0 and y1 <= b1]
        out[name] = home[0] if home else None
    return out


def summary(lay):
    L, W, H = lay.cav
    halves = lay.tray_halves()
    return {
        "base": lay.base,
        "cavidad": (L, W, H),
        "caja_exterior": lay.box_outer(),
        "caja_con_brida": lay.box_with_flange(),
        "cabe_en_cama": lay.fits_bed(),
        "bandejas": {k: (v[1] - v[0], v[3] - v[2]) for k, v in halves.items()},
        "bandejas_ok_150": all(max(v[1] - v[0], v[3] - v[2]) <= PIECE_MAX_L for v in halves.values()),
        "conflictos": conflicts(lay),
        "fuera_de_cavidad": inside_cavity(lay),
        "modulo_en_bandeja": tray_bodies_ok(lay),
    }


if __name__ == "__main__":
    for base in ("sin_base", "kit_a"):
        s = summary(build(base))
        for k, v in s.items():
            print(f"{base:9s} {k}: {v}")
        print()
