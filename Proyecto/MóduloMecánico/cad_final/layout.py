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

from params import (BASE_M4_BOSS, BASE_M4_PTS, BOX_FLANGE, BOX_FLOOR, BOX_LID_GAP, BOX_LID_T, BOX_WALL, CLR_CONN,
                    CLR_NUT, CLR_PINS, CLR_SD, CLR_USB, COMPONENTS, CONNECTORS, ESP32_BASE, GAP_MOD, GAP_WALL,
                    LAYOUT_FLOORS, PG7_INNER_H, PIECE_MAX_L, PRINT_BED, TRAY2_POST_D, TRAY_BOSS_D,
                    TRAY_BOSS_INSET, TRAY_CRADLE_T, TRAY_SPLIT, TRAY_STANDOFF, TRAY_T, UMB_GLAND, UMB_GLAND_XY,
                    HANDLE_KEEP_Y, nut_corner_r)

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
    lid_gland: tuple = None                             # umbilical PG7 on the lid (x, y)
    wall_gland: tuple = None                            # or on the -X wall: (x outer face, y, z)
    access_r: float = 0.0
    cav: tuple = (0.0, 0.0, 0.0)                        # L, W, H of the cavity
    z_floor: float = BOX_FLOOR
    z_tray: float = 0.0                                 # tray top face
    modules: list = field(default_factory=list)         # (name, comp key, body Item)
    floors: int = 1
    z_tray2: float = 0.0                                # upper tray top face (2 floors)
    tray_upper: tuple = None                            # upper tray plan (x0, x1, y0, y1)

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
        split = (2 * hx > PIECE_MAX_L) if TRAY_SPLIT == "auto" else TRAY_SPLIT
        if not split:
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


def _devkit(lay, xa, ya, z_tray, base):
    """ESP32 slot along X with the USB toward +X; (xa, ya) is the min corner of the DevKit or of KIT A.
    sin_base: DevKit pins down on a cradle CLR_PINS high (dupont zone below).
    kit_a: KIT A at z_tray with the DevKit plugged on top."""
    Ld, Wd, Hd, _ = COMPONENTS["esp32_devkitc1"]
    if base == "sin_base":
        body = _place(lay, "esp32_devkitc1", "esp32", "X", xa, ya, z_tray + CLR_PINS)
        # cradle ledges under the two short ends (the headers run along the long sides)
        for k, (a, b) in enumerate(((xa, xa + TRAY_CRADLE_T), (xa + Ld - TRAY_CRADLE_T, xa + Ld))):
            lay.items.append(Item(f"esp32:cuna_{k}", "cuerpo", "esp32", "box", (a, b, ya, ya + Wd),
                                  [z_tray, z_tray + CLR_PINS]))
        return body
    Lk, Wk, Hk, _ = COMPONENTS["kit_a"]
    kb = _place(lay, "kit_a", "kit_a", "X", xa, ya, z_tray)
    _place(lay, "esp32_devkitc1", "esp32", "X", xa + (Lk - Ld) / 2, ya + (Wk - Wd) / 2, kb.z[1],
           pins="ninguno", group="kit_a")
    return kb


def _row(lay, specs, x_start, y_edge, z0, north=True):
    """Modules along X one after the other, starting at x_start. specs: [(key, name, su, sv, lead)], lead =
    free length before the body (the zone on that side, shared with the previous module's zone).
    north: bodies start at y_edge going +Y; otherwise they end at y_edge going -Y."""
    x = x_start
    for key, name, su, sv, lead in specs:
        L, W, *_ = COMPONENTS[key]
        x += lead
        _place(lay, key, name, "X", x, y_edge if north else y_edge - W, z0, su, sv)
        x += L
    return x


def build(base=ESP32_BASE, clr_nut=CLR_NUT, floors=1):
    """floors = 1: everything on one tray; the DevKit cradle sits over the floor glands (they are tightened
    with the box empty, so only the rising cable column must stay clear under it).
    floors = 2: XY-017, MPU-6050 and both HW-517 on the lower tray; DevKit and microSD on an upper tray on
    four posts, so USB and card stay reachable from above. clr_nut is the locknut clearance (params.CLR_NUT)."""
    lay = Layout(base=base, floors=floors)
    rc = nut_corner_r()
    rk = rc + clr_nut                     # hole in the tray / free column above each floor locknut
    gx = rc + clr_nut / 2                 # corner-to-corner distance between the two nuts = clr_nut
    lay.access_r = rk
    lay.floor_glands = [(gx, 0.0), (-gx, 0.0)]
    zf = BOX_FLOOR
    lay.z_tray = zt = zf + TRAY_STANDOFF + TRAY_T
    # the tray bottom sits below the locknut top: then the tray hole must clear the nut
    assert TRAY_STANDOFF >= PG7_INNER_H or rk >= rc + GAP_MOD, "tray hole does not clear the PG7 nut"
    for (x, y) in lay.floor_glands:
        nm = f"pg7_fondo_{'der' if x > 0 else 'izq'}"
        lay.items.append(Item(nm, "cuerpo", nm, "cyl", (x, y, rc), [zf, zf + PG7_INNER_H]))
        lay.items.append(Item(f"{nm}:llave", "acceso", nm, "cyl", (x, y, rk), [zf, zt]))   # with the box empty
        lay.items.append(Item(f"{nm}:cable", "cable", nm, "cyl", (x, y, rk), [zt, zt + CLR_PINS]))
    d4, h4 = BASE_M4_BOSS
    for k, (x, y) in enumerate(BASE_M4_PTS):
        lay.items.append(Item(f"inserto_m4_{k}", "cuerpo", "caja", "cyl", (x, y, d4 / 2), [zf, zf + h4]))

    Lk, Wk, *_ = COMPONENTS["kit_a"] if base == "kit_a" else COMPONENTS["esp32_devkitc1"]
    Lh, Wh, *_ = COMPONENTS["hw517"]
    Lm, Wm, *_ = COMPONENTS["microsd"]
    Lx, Wx, *_ = COMPONENTS["xy017"]
    Lu, Wu, *_ = COMPONENTS["mpu6050"]
    C = CLR_CONN
    span = Lk + CLR_USB                   # DevKit (or KIT A) + USB plug along X
    if floors == 1:
        # DevKit or KIT A along X over the glands, raised CLR_PINS so it clears their cable columns; its
        # +X cradle ledge just outside the right gland column, USB toward +X
        xa = gx + rk + GAP_MOD + TRAY_CRADLE_T - Lk
        _devkit(lay, xa, -Wk / 2, zt if base == "sin_base" else zt + CLR_PINS, base)
        yb = Wk / 2 + C
        # north: microSD (card toward -X) then XY-017; south: HW-517, HW-517, MPU-6050 (header toward +Y)
        north = CLR_SD + Lm + C + Lx + C
        _row(lay, [("microsd", "microsd", -1, 1, CLR_SD), ("xy017", "xy017", 1, 1, C)], -north / 2, yb, zt)
        south = C + Lh + C + Lh + C + Lu
        _row(lay, [("hw517", "hw517_1", 1, 1, C), ("hw517", "hw517_2", 1, 1, C),
                   ("mpu6050", "mpu6050", 1, -1, C)], -south / 2, -yb, zt, north=False)
    else:
        # lower tray: XY-017 + MPU-6050 north of the glands (header toward the glands), both HW-517 south
        yb = rk
        north = C + Lx + C + Lu
        _row(lay, [("xy017", "xy017", 1, 1, C), ("mpu6050", "mpu6050", 1, 1, C)], -north / 2, yb, zt)
        south = C + Lh + C + Lh + C
        _row(lay, [("hw517", "hw517_1", 1, 1, C), ("hw517", "hw517_2", 1, 1, C)], -south / 2, -yb, zt,
             north=False)
        z_low = max(it.z[1] for it in lay.items if it.z[1] is not TOP)
        lay.z_tray2 = zt2 = z_low + TRAY_T
        # upper tray: DevKit (USB toward +X) and the microSD beside it, across its side cable zone
        band = C + Wk + C + Wm
        ye = -band / 2 + C
        _devkit(lay, -span / 2, ye, zt2, base)
        _row(lay, [("microsd", "microsd", -1, 1, CLR_SD)], -(CLR_SD + Lm + C) / 2, ye + Wk + C, zt2)

    # cavity: symmetric about x = y = 0 (box centred on the rail)
    hx = hy = 0.0
    ztop = 0.0
    for it in lay.items:
        x0, x1, y0, y1 = it.bbox2()
        pad = GAP_WALL if it.kind == "cuerpo" else 0.0
        hx = max(hx, abs(x0) + pad, abs(x1) + pad)
        hy = max(hy, abs(y0) + pad, abs(y1) + pad)
        if it.z[1] is not TOP:
            ztop = max(ztop, it.z[1])
    ztop += BOX_LID_GAP
    lay.cav = (2 * hx, 2 * hy, ztop - zf)
    for it in lay.items:
        if it.z[1] is TOP:
            it.z[1] = ztop
    # floor bosses that carry the lower tray
    for k, (x, y) in enumerate(tray_boss_pts(lay)):
        lay.items.append(Item(f"boss_bandeja_{k}", "cuerpo", "caja", "cyl", (x, y, TRAY_BOSS_D / 2),
                              [zf, zf + TRAY_STANDOFF]))
    if floors == 2:
        # the upper tray and its posts are bodies: checked against everything below them
        lay.tray_upper = (-hx + GAP_WALL, hx - GAP_WALL, -hy + GAP_WALL, hy - GAP_WALL)
        lay.items.append(Item("bandeja_sup", "cuerpo", "bandeja_sup", "box", lay.tray_upper,
                              [lay.z_tray2 - TRAY_T, lay.z_tray2]))
        ux0, ux1, uy0, uy1 = lay.tray_upper
        i = TRAY_BOSS_INSET
        for k, corner in enumerate((x, y) for x in (ux0 + i, ux1 - i) for y in (uy0 + i, uy1 - i)):
            post = _first_free(lay, corner, (ux0 + i, ux1 - i, uy0 + i, uy1 - i),
                               lambda x, y: Item(f"poste_{k}", "cuerpo", "bandeja_sup", "cyl",
                                                 (x, y, TRAY2_POST_D / 2), [zt, lay.z_tray2 - TRAY_T]))
            assert post is not None, f"no free spot for upper tray post {k}"
            lay.items.append(post)
    _umbilical(lay, rc, hx, hy, ztop)
    return lay


def _hits(lay, item):
    """True if `item` (a body) breaks the overlap rule against what is already placed."""
    for b in lay.items:
        if b.group == item.group or (item.on_lid and b.kind == "acceso"):
            continue
        if _overlap(item, b):
            return True
    return False


def _first_free(lay, start, region, make, step=1.0):
    """The free spot nearest to `start` inside region (x0, x1, y0, y1); make(x, y) -> Item."""
    x0, x1, y0, y1 = region
    nx, ny = int((x1 - x0) / step) + 1, int((y1 - y0) / step) + 1
    pts = sorted(((x0 + a * step, y0 + b * step) for a in range(nx) for b in range(ny)),
                 key=lambda q: math.hypot(q[0] - start[0], q[1] - start[1]))
    for x, y in pts:
        it = make(x, y)
        if not _hits(lay, it):
            return it
    return None


def _umbilical(lay, rc, hx, hy, ztop):
    """Umbilical PG7: on the lid (its locknut hangs PG7_INNER_H) if a free spot exists outside the handle
    strip, otherwise on the -X end wall (locknut horizontal, axis along X). UMB_GLAND forces either."""
    it = None
    if UMB_GLAND in ("auto", "tapa"):
        for sgn in (1, -1):
            region = (-hx + rc, hx - rc, HANDLE_KEEP_Y, hy - rc) if sgn > 0 else (-hx + rc, hx - rc, -hy + rc, -HANDLE_KEEP_Y)
            if region[2] > region[3]:
                continue
            cand = _first_free(lay, UMB_GLAND_XY, region, lambda x, y: Item(
                "pg7_umbilical", "cuerpo", "pg7_umbilical", "cyl", (x, y, rc), [ztop - PG7_INNER_H, ztop],
                on_lid=True))
            if cand and (it is None or math.dist(cand.xy[:2], UMB_GLAND_XY) < math.dist(it.xy[:2], UMB_GLAND_XY)):
                it = cand
        if it:
            lay.lid_gland = it.xy[:2]
    if it is None and UMB_GLAND in ("auto", "pared"):
        # -X wall: a square of side 2 rc in the YZ plane, PG7_INNER_H deep, as low as it fits above the tray
        zf = lay.z_floor
        for zc in [lay.z_tray + rc + k for k in range(int(ztop - rc - lay.z_tray - rc) + 1)]:
            for yc in sorted(range(int(-hy + rc), int(hy - rc) + 1), key=abs):
                cand = Item("pg7_umbilical", "cuerpo", "pg7_umbilical", "box",
                            (-hx, -hx + PG7_INNER_H, yc - rc, yc + rc), [zc - rc, zc + rc])
                if not _hits(lay, cand):
                    it = cand
                    lay.wall_gland = (-hx - BOX_WALL, float(yc), zc)
                    break
            if it:
                break
    assert it is not None, "no free place for the umbilical PG7"
    lay.items.append(it)


def tray_boss_pts(lay):
    """Four floor bosses per lower tray piece: at its corners, TRAY_BOSS_INSET in."""
    out = []
    for x0, x1, y0, y1 in lay.tray_halves().values():
        for x in (x0 + TRAY_BOSS_INSET, x1 - TRAY_BOSS_INSET):
            for y in (y0 + TRAY_BOSS_INSET, y1 - TRAY_BOSS_INSET):
                out.append((x, y))
    return out


def candidates(base=ESP32_BASE, clr_nut=CLR_NUT, floors=LAYOUT_FLOORS):
    """{floors: layout} for the variants to compare ('auto' = 1 and 2)."""
    return {f: build(base, clr_nut, f) for f in ((1, 2) if floors == "auto" else (floors,))}


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
        "pisos": lay.floors,
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
    for base, fl in (("sin_base", 1), ("sin_base", 2), ("kit_a", 1), ("kit_a", 2)):
        s = summary(build(base, floors=fl))
        for k, v in s.items():
            print(f"{base:9s} {k}: {v}")
        print()
