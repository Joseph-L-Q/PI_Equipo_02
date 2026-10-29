"""Fase C: camera capsule (M4 body, M5 lid, M6 bezel, M7 window) and capsule carriage M10.

Builders copied from ../cad/parts.py (P4 rev. B) with minimal changes; every dimension comes from params.py.
Capsule frame: hinge axis = global Y through the origin, optical axis +X, window at the far +X end.
Carriage frame (as the rest of cad_final): X along the rail, Y across, Z up, rail bottom at z = 0. The sleeve of M10
spans x in [-CARRIAGE_L, 0]; the hinge axis is at carriage_axis(). CARRIAGE_MODE "deslizante" (default): sleeve open at
both ends, knob under it in the bottom T, axis dropped below the rail so the rail can run past the sleeve by up to
2 x CARRIAGE_TRAVEL over the capsule. "tope": the earlier version, stop plate on the rail end at x in [0, CARRIAGE_END_T].
Run from cad_final/:  python capsula.py
"""
import functools
import math
from pathlib import Path

import cadquery as cq

from checks import brep_check, export_part, mesh_checks, min_thickness, sanitize
from params import (ACRYLIC_DENSITY, BEZEL_OD, BEZEL_SCREWS, BEZEL_T, CAM_TILT_DEG, CAMERA, CAP_FLANGE, CAP_FLANGE_T,
                    CAP_FRONT, CAP_GLAND_X, CAP_LENS_GAP, CAP_LID_T, CAP_REAR_ZONE, CAP_SIDE_GAP, CAP_WALL,
                    CAPSULE_SET_DISP_CM3, CAPSULE_SET_G, CARRIAGE_END_T, CARRIAGE_EAR_H, CARRIAGE_EAR_REACH,
                    CARRIAGE_L, CARRIAGE_LIP_EDGE, CARRIAGE_TRAVEL, CARRIAGE_WALL, FIT_CLEAR, GROOVE_DEPTH,
                    CARRIAGE_AXIS_CLR, CARRIAGE_KEEL_CLR, CARRIAGE_MODE, CARRIAGE_SLIT_CLR, CARRIAGE_STEPS, KNOB_D,
                    KNOB_FLANGE_GAP, KNOB_FREE_EXTRA, KNOB_H, KNOB_WEB_GAP, RAIL_EXIT_SLOT,
                    GROOVE_WIDTH, HINGE_DISC_D, HINGE_EAR_T, HINGE_GAP, HINGE_TEETH, HINGE_TEETH_RIN,
                    HINGE_TOOTH_H, LED_RING, LED_RING_HOLE, LED_SEPARATOR, LED_SPOKES, LENS_APERTURE, LENS_D,
                    M2_PILOT, M3_CLEAR, M4_CLEAR, MIN_WALL, PETG_DENSITY, PG7_HOLE, PRINT_BED, RAIL_SECTION,
                    RAIL_TSLOT, RAIL_WALL, SHELL_T, TONGUE_LEN, WIN_DIA, WIN_SEAT_DEPTH, WIN_T)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "preliminar"
STL, STEP = OUT / "stl", OUT / "step"

# ------------------------------------------------------------------ derived from the camera
TONGUE_CORE = HINGE_GAP - 2 * HINGE_TOOTH_H
CAP_CAV_W = CAMERA[0] + 2 * CAP_SIDE_GAP
CAP_CAV_H = CAMERA[1] + 2 * CAP_SIDE_GAP
LENS_TIP_DEPTH = WIN_SEAT_DEPTH + CAP_LENS_GAP                       # lens tip behind the front face
BEHIND_WALL = CAMERA[2] - (CAP_FRONT - LENS_TIP_DEPTH)               # camera length behind the wall inner face
CAP_CAV_L = float(math.ceil(BEHIND_WALL + CAP_REAR_ZONE))
LED_STACK = LED_RING[1] + LED_SEPARATOR[1]                           # separator tube length from the wall inner face
BORE_R = LENS_D / 2 + 0.2
TUBE_R = BORE_R + LED_SEPARATOR[0]
AXIS_Z = RAIL_SECTION / 2


@functools.lru_cache(maxsize=None)   # ~50 s per call; returned Workplanes are never mutated
def serration(r_in, r_out, n, h, offset_deg=0.0):
    """Radial teeth on the y = 0 plane pointing +Y, around the Y axis (wedges whose bases share one pitch, trimmed by
    an annulus so the outer face is the cylinder r_out)."""
    a = math.pi / n

    def tri(r):
        return cq.Wire.makePolygon([cq.Vector(r * math.cos(a), 0, r * math.sin(a)),
                                    cq.Vector(r, h, 0),
                                    cq.Vector(r * math.cos(a), 0, -r * math.sin(a))], close=True)

    tooth = cq.Solid.makeLoft([tri(r_in - 1.0), tri(r_out + 1.0)], ruled=True)
    teeth = cq.Workplane().add(tooth)
    for k in range(1, n):
        teeth = teeth.union(cq.Workplane().add(tooth.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), k * 360.0 / n)))
    ring = (cq.Workplane().add(cq.Solid.makeCylinder(r_out, h + 1, cq.Vector(0, 0, 0), cq.Vector(0, 1, 0)))
            .cut(cq.Workplane().add(cq.Solid.makeCylinder(r_in, h + 1, cq.Vector(0, 0, 0), cq.Vector(0, 1, 0)))))
    teeth = teeth.intersect(ring)
    return teeth.rotate((0, 0, 0), (0, 1, 0), offset_deg) if offset_deg else teeth


# ------------------------------------------------------------------ capsule
def cap_dims():
    out_w = CAP_CAV_W + 2 * CAP_WALL
    out_h = CAP_CAV_H + 2 * CAP_WALL
    fl_w = out_w + 2 * CAP_FLANGE
    fl_h = out_h + 2 * CAP_FLANGE
    x_lid0 = TONGUE_LEN                      # lid outer face
    x_body0 = x_lid0 + CAP_LID_T             # rear opening / flange face
    x_front = x_body0 + CAP_CAV_L + CAP_FRONT
    return out_w, out_h, fl_w, fl_h, x_lid0, x_body0, x_front


def cap_screw_pts():
    _, _, fl_w, fl_h, *_ = cap_dims()
    a, b = fl_w / 2 - CAP_FLANGE / 2, fl_h / 2 - CAP_FLANGE / 2
    return [(a, b), (-a, b), (a, -b), (-a, -b)]


def _bezel_pts():
    r = (WIN_DIA / 2 + BEZEL_OD / 2) / 2
    return [(r * math.cos(math.radians(90 + k * 360 / BEZEL_SCREWS)), r * math.sin(math.radians(90 + k * 360 / BEZEL_SCREWS)))
            for k in range(BEZEL_SCREWS)]


def capsule_cavity():
    _, _, _, _, _, x0, _ = cap_dims()
    return cq.Workplane("YZ").workplane(offset=x0).rect(CAP_CAV_W, CAP_CAV_H).extrude(CAP_CAV_L).edges("|X").fillet(2)


def capsule_body():
    out_w, out_h, fl_w, fl_h, x_lid0, x0, x_front = cap_dims()
    L = CAP_CAV_L + CAP_FRONT
    x_fi = x_front - CAP_FRONT                # front wall inner face
    body = cq.Workplane("YZ").workplane(offset=x0).rect(out_w, out_h).extrude(L).edges("|X").fillet(3)
    flange = cq.Workplane("YZ").workplane(offset=x0).rect(fl_w, fl_h).extrude(CAP_FLANGE_T).edges("|X").fillet(4)
    body = body.union(flange)
    body = body.cut(capsule_cavity())
    # opaque separator tube standing on the front wall: LED ring outside it, lens inside it
    tube = cq.Workplane("YZ").workplane(offset=x_fi - LED_STACK).circle(TUBE_R).extrude(LED_STACK)
    body = body.union(tube)
    # window seat from outside; annular LED aperture held by radial spokes; lens bore through wall and tube
    seat = cq.Workplane("YZ").workplane(offset=x_front - WIN_SEAT_DEPTH).circle(WIN_DIA / 2 + 0.2).extrude(WIN_SEAT_DEPTH)
    ap = (cq.Workplane("YZ").workplane(offset=x_fi).circle(LENS_APERTURE / 2).circle(TUBE_R).extrude(CAP_FRONT))
    n_sp, w_sp = LED_SPOKES
    for k in range(int(n_sp)):
        ang = 90 + k * 360.0 / n_sp
        sp = (cq.Workplane("YZ").workplane(offset=x_fi).center(0, LENS_APERTURE / 4)
              .rect(w_sp, LENS_APERTURE / 2).extrude(CAP_FRONT).rotate((0, 0, 0), (1, 0, 0), ang))
        ap = ap.cut(sp)
    bore = cq.Workplane("YZ").workplane(offset=x_fi - LED_STACK).circle(BORE_R).extrude(LED_STACK + CAP_FRONT)
    body = body.cut(seat).cut(ap).cut(bore)
    # bezel pilot holes (blind, 4 mm into the front wall region outside the seat)
    for (y, z) in _bezel_pts():
        body = body.cut(cq.Workplane("YZ").workplane(offset=x_front - 4.0).center(y, z).circle(M2_PILOT / 2).extrude(4.0))
    # flange through-holes (M3 with nuts)
    for (y, z) in cap_screw_pts():
        body = body.cut(cq.Workplane("YZ").workplane(offset=x0).center(y, z).circle(M3_CLEAR / 2).extrude(CAP_FLANGE_T))
    # PG7 cable gland on the bottom wall, near the rear
    gx = x0 + CAP_GLAND_X
    body = body.cut(cq.Workplane("XY").workplane(offset=-out_h / 2).center(gx, 0).circle(PG7_HOLE / 2).extrude(CAP_WALL))
    return body


def capsule_lid():
    out_w, out_h, fl_w, fl_h, x_lid0, x0, _ = cap_dims()
    lid = cq.Workplane("YZ").workplane(offset=x_lid0).rect(fl_w, fl_h).extrude(CAP_LID_T).edges("|X").fillet(4)
    for (y, z) in cap_screw_pts():
        lid = lid.cut(cq.Workplane("YZ").workplane(offset=x_lid0).center(y, z).circle(M3_CLEAR / 2).extrude(CAP_LID_T))
    # O-ring groove on the inner face: centreline midway between cavity and screw circle
    cl_w = (CAP_CAV_W + (fl_w - CAP_FLANGE)) / 2
    cl_h = (CAP_CAV_H + (fl_h - CAP_FLANGE)) / 2
    lid = lid.cut(_ring_yz(cl_w, cl_h, 4.0, GROOVE_WIDTH, x0 - GROOVE_DEPTH, GROOVE_DEPTH))
    # tongue: plate in XZ (normal Y), from the hinge disc to the lid outer face
    t = TONGUE_CORE
    disc = cq.Workplane("XZ").circle(HINGE_DISC_D / 2).extrude(t / 2, both=True)
    bar = cq.Workplane("XZ").center(x_lid0 / 2, 0).rect(x_lid0, HINGE_DISC_D).extrude(t / 2, both=True)
    tongue = disc.union(bar)
    teeth_p = serration(HINGE_TEETH_RIN, HINGE_DISC_D / 2, HINGE_TEETH, HINGE_TOOTH_H).translate((0, t / 2, 0))
    teeth_n = serration(HINGE_TEETH_RIN, HINGE_DISC_D / 2, HINGE_TEETH, HINGE_TOOTH_H).mirror("XZ").translate((0, -t / 2, 0))
    tongue = tongue.union(teeth_p).union(teeth_n)
    tongue = tongue.cut(cq.Workplane("XZ").circle(M4_CLEAR / 2).extrude(20, both=True))
    return lid.union(tongue)


def _ring_yz(l, w, r, band, x_start, depth):
    outer = cq.Workplane("YZ").workplane(offset=x_start).rect(l + band, w + band).extrude(depth).edges("|X").fillet(r + band / 2)
    inner = cq.Workplane("YZ").workplane(offset=x_start).rect(l - band, w - band).extrude(depth).edges("|X").fillet(max(0.2, r - band / 2))
    return outer.cut(inner)


def window_disc():
    _, _, _, _, _, _, x_front = cap_dims()
    return cq.Workplane("YZ").workplane(offset=x_front - WIN_SEAT_DEPTH).circle(WIN_DIA / 2).extrude(WIN_T)


def bezel():
    _, _, _, _, _, _, x_front = cap_dims()
    b = cq.Workplane("YZ").workplane(offset=x_front).circle(BEZEL_OD / 2).circle(LENS_APERTURE / 2 + 1.0).extrude(BEZEL_T)
    for (y, z) in _bezel_pts():
        b = b.cut(cq.Workplane("YZ").workplane(offset=x_front).center(y, z).circle(2.4 / 2).extrude(BEZEL_T))
    return b


def camera_dummy():
    """Board slab + lens holder (LENS_D); lens tip LENS_TIP_DEPTH behind the front face. Envelope CAMERA, not printed."""
    _, _, _, _, _, _, x_front = cap_dims()
    x_tip = x_front - LENS_TIP_DEPTH
    x_back = x_tip - CAMERA[2]
    board_t = 2.0
    board = cq.Workplane("YZ").workplane(offset=x_back).rect(CAMERA[0], CAMERA[1]).extrude(board_t)
    lens = cq.Workplane("YZ").workplane(offset=x_back + board_t).circle(LENS_D / 2).extrude(CAMERA[2] - board_t)
    return board.union(lens)


def led_ring_dummy():
    _, _, _, _, _, _, x_front = cap_dims()
    x_fi = x_front - CAP_FRONT
    return (cq.Workplane("YZ").workplane(offset=x_fi - LED_RING[1]).circle(LED_RING[0] / 2).circle(LED_RING_HOLE / 2)
            .extrude(LED_RING[1]))


# ------------------------------------------------------------------ carriage M10
def carriage_axis():
    """Hinge axis (x, z) in the carriage frame."""
    if CARRIAGE_MODE == "tope":
        return CARRIAGE_END_T + CARRIAGE_EAR_REACH, RAIL_SECTION / 2
    # capsule flange top at tilt 0 sits CARRIAGE_AXIS_CLR under the rail bottom; ear tip circle starts at the sleeve end
    return CARRIAGE_EAR_H / 2, -(cap_dims()[3] / 2 + CARRIAGE_AXIS_CLR)


def carriage_axis_x():
    return carriage_axis()[0]


def knob_free():
    """Free cylinder of the knob under the sleeve (gloved hand), centred on the M4 of the bottom T."""
    c, w = FIT_CLEAR, CARRIAGE_WALL
    r = (KNOB_D + KNOB_FREE_EXTRA) / 2
    z_top = -c - w - KNOB_FLANGE_GAP
    return cq.Workplane("XY").workplane(offset=z_top - KNOB_H).center(-CARRIAGE_L + r, 0).circle(r).extrude(KNOB_H)


def carriage():
    return carriage_tope() if CARRIAGE_MODE == "tope" else carriage_slide()


def carriage_slide():
    """Sleeve open at both ends (rides +-CARRIAGE_TRAVEL), closed bottom with the knob M4 at the rear, cable slit on
    +Y over the full length, and a keel in front of the knob carrying the hinge ears below the rail.
    Capsule points above the axis always have x >= TONGUE_LEN from it (tilt 0..90 downward), so the keel is free
    everywhere behind and above the axis except around the tongue disc."""
    import riel
    c, w, S = FIT_CLEAR, CARRIAGE_WALL, RAIL_SECTION
    hw_o, hw_i = S / 2 + c + w, S / 2 + c
    z0, z1 = -c - w, S + c + w
    L = CARRIAGE_L
    a = cq.Workplane("XY").box(L, 2 * hw_o, z1 - z0, centered=False).translate((-L, -hw_o, z0))
    a = a.cut(cq.Workplane("XY").box(L, 2 * hw_i, S + 2 * c, centered=False).translate((-L, -hw_i, -c)))
    # cable slit on +Y at the height of the rail exit slot, whole length (any carriage position)
    sh = RAIL_EXIT_SLOT[0] + 2 * CARRIAGE_SLIT_CLR
    a = a.cut(cq.Workplane("XY").box(L, w + 2 * c, sh, centered=False).translate((-L, hw_i - c, riel.EXIT_SLOT_ZC - sh / 2)))
    # knob M4 through the bottom wall, on the rail centreline
    r_k = (KNOB_D + KNOB_FREE_EXTRA) / 2
    a = a.cut(cq.Workplane("XY").workplane(offset=z0).center(-L + r_k, 0).circle(M4_CLEAR / 2).extrude(w))
    # keel: ears + bridge between them, from the knob free cylinder to the axis, below the sleeve bottom
    ax, az = carriage_axis()
    x_k = -L + 2 * r_k + KNOB_WEB_GAP
    y_o = HINGE_GAP / 2 + HINGE_EAR_T
    keel = cq.Workplane("XY").box(ax - x_k, 2 * y_o, z0 + w / 2 - az, centered=False).translate((x_k, -y_o, az))
    keel = keel.cut(cq.Workplane("XZ").center(ax, az).circle(HINGE_DISC_D / 2 + CARRIAGE_KEEL_CLR)
                    .extrude(HINGE_GAP / 2, both=True))
    for s in (1, -1):
        y0 = s * HINGE_GAP / 2
        off = -(y0 + s * HINGE_EAR_T) if s > 0 else -y0
        keel = keel.union(cq.Workplane("XZ").workplane(offset=off).center(ax, az).circle(CARRIAGE_EAR_H / 2)
                          .extrude(HINGE_EAR_T))
        teeth = serration(HINGE_TEETH_RIN, HINGE_DISC_D / 2, HINGE_TEETH, HINGE_TOOTH_H).rotate((0, 0, 0), (0, 1, 0), 180.0 / HINGE_TEETH)
        keel = keel.union((teeth.mirror("XZ") if s > 0 else teeth).translate((ax, y0, az)))
    a = a.union(keel)
    return a.cut(cq.Workplane("XZ").center(ax, az).circle(M4_CLEAR / 2).extrude(30, both=True))


def carriage_tope():
    c, w, S = FIT_CLEAR, CARRIAGE_WALL, RAIL_SECTION
    hw_o, hw_i = S / 2 + c + w, S / 2 + c
    z0, z1 = -c - w, S + c + w
    sleeve = cq.Workplane("XY").box(CARRIAGE_L, 2 * hw_o, z1 - z0, centered=False).translate((-CARRIAGE_L, -hw_o, z0))
    # rail passage (open at the inner end, closed by the stop plate), lips under the rail keep |y| >= CARRIAGE_LIP_EDGE
    sleeve = sleeve.cut(cq.Workplane("XY").box(CARRIAGE_L, 2 * hw_i, S + 2 * c, centered=False).translate((-CARRIAGE_L, -hw_i, -c)))
    sleeve = sleeve.cut(cq.Workplane("XY").box(CARRIAGE_L, 2 * CARRIAGE_LIP_EDGE, w, centered=False).translate((-CARRIAGE_L, -CARRIAGE_LIP_EDGE, z0)))
    plate = cq.Workplane("XY").box(CARRIAGE_END_T, 2 * hw_o, z1 - z0, centered=False).translate((0, -hw_o, z0))
    a = sleeve.union(plate)
    # M4 hole on the rail centreline for the knob bolt
    a = a.cut(cq.Workplane("XY").workplane(offset=S + c).center(-CARRIAGE_L / 2, 0).circle(M4_CLEAR / 2).extrude(w))
    # fork: two ears with inner serrations, axis along Y, beyond the stop plate
    ax = carriage_axis_x()
    for s in (1, -1):
        y0 = s * HINGE_GAP / 2
        off = -(y0 + s * HINGE_EAR_T) if s > 0 else -y0
        ear = (cq.Workplane("XZ").workplane(offset=off).center((CARRIAGE_END_T - 2 + ax) / 2, AXIS_Z)
               .rect(ax - CARRIAGE_END_T + 2, CARRIAGE_EAR_H).extrude(HINGE_EAR_T))
        tip = cq.Workplane("XZ").workplane(offset=off).center(ax, AXIS_Z).circle(CARRIAGE_EAR_H / 2).extrude(HINGE_EAR_T)
        ear = ear.union(tip)
        teeth = serration(HINGE_TEETH_RIN, HINGE_DISC_D / 2, HINGE_TEETH, HINGE_TOOTH_H).rotate((0, 0, 0), (0, 1, 0), 180.0 / HINGE_TEETH)
        teeth = (teeth.mirror("XZ") if s > 0 else teeth).translate((ax, y0, AXIS_Z))
        a = a.union(ear).union(teeth)
    a = a.cut(cq.Workplane("XZ").center(ax, AXIS_Z).circle(M4_CLEAR / 2).extrude(30, both=True))
    return a


def rail_stub(length=100.0, x_end=-FIT_CLEAR):
    """Simplified last tramo (hollow square, T-slot opening on the bottom) ending at x_end."""
    S, W = RAIL_SECTION, RAIL_WALL
    r = cq.Workplane("XY").box(length, S, S, centered=False).translate((x_end - length, -S / 2, 0))
    r = r.cut(cq.Workplane("XY").box(length, S - 2 * W, S - 2 * W, centered=False).translate((x_end - length, -S / 2 + W, W)))
    r = r.cut(cq.Workplane("XY").box(length, RAIL_TSLOT["abertura"], W, centered=False).translate((x_end - length, -RAIL_TSLOT["abertura"] / 2, 0)))
    return r


# ------------------------------------------------------------------ placement and checks
def place_capsule(shape, tilt):
    """Capsule part -> carriage frame at tilt degrees downward (+x rotates toward -z)."""
    s = shape.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), tilt)
    ax, az = carriage_axis()
    return s.translate(cq.Vector(ax, 0, az))


def interference(parts, targets, tilt):
    tgt = cq.Compound.makeCompound(targets)
    out = {}
    for name, sh in parts.items():
        try:
            out[name] = sh_vol(place_capsule(sh, tilt).intersect(tgt))
        except Exception as e:  # noqa: BLE001
            out[name] = float("nan")
            print("   boolean failed", name, tilt, e)
    return out


def sh_vol(s):
    try:
        return s.Volume()
    except Exception:  # noqa: BLE001
        return 0.0


ORIENTS = {"sin girar": None, "X+90": ("X", 90), "X-90": ("X", -90), "Y+90": ("Y", 90), "Y-90": ("Y", -90),
           "X180": ("X", 180)}


def process(name, wp, stem, orient_name=None, printed=True):
    shape = sanitize(wp)
    chk = brep_check(shape)
    export_part(shape, stem, STL, STEP)
    path = STL / f"{stem}.stl"
    best = None
    names = [orient_name] if orient_name else list(ORIENTS)
    for on in names:
        mc = mesh_checks(str(path), PRINT_BED, ORIENTS[on])
        if mc["fits_bed"] and (best is None or mc["overhang_mm2"] < best[1]["overhang_mm2"]):
            best = (on, mc)
    on, mc = best
    p1, pmin = min_thickness(str(path))
    return dict(name=name, stem=stem, shape=shape, chk=chk, orient=on, mc=mc, p1=p1, pmin=pmin,
                vol=shape.Volume() / 1000.0, area=shape.Area())


def main():
    STL.mkdir(parents=True, exist_ok=True)
    STEP.mkdir(parents=True, exist_ok=True)
    print(f"cavity {CAP_CAV_W} x {CAP_CAV_H} x {CAP_CAV_L}; camera behind wall {BEHIND_WALL:.1f}")
    rows = []
    for name, fn, stem in (("M4 cuerpo", capsule_body, "M4_capsula_cuerpo"), ("M5 tapa", capsule_lid, "M5_capsula_tapa"),
                           ("M6 bisel", bezel, "M6_capsula_bisel"), ("M7 ventana", window_disc, "M7_capsula_ventana"),
                           ("M10 carro", carriage, "M10_carro_capsula")):
        print("building", name, flush=True)
        r = process(name, fn(), stem)
        rows.append(r)
        print(f"  ok={r['chk']['ok']} {r['chk']} wt={r['mc']['watertight']} bodies={r['mc']['bodies']} "
              f"or={r['orient']} bbox={tuple(round(v, 1) for v in r['mc']['bbox'])} ov={r['mc']['overhang_mm2']:.0f} "
              f"p1={r['p1']:.2f} min={r['pmin']:.2f}", flush=True)
    R = {r["stem"]: r for r in rows}
    body, lid, bez, win, car = (R[s]["shape"] for s in ("M4_capsula_cuerpo", "M5_capsula_tapa", "M6_capsula_bisel",
                                                           "M7_capsula_ventana", "M10_carro_capsula"))

    # hinge range x carriage position: rail tip from flush with the sleeve end (s = 0) to 2 x travel past it
    parts = {"M4": body, "M5": lid, "M6": bez}
    tilts = list(range(0, 100, 10))
    hinge = {}
    if CARRIAGE_MODE == "tope":
        positions = [0.0]
        stubs = {0.0: rail_stub().val()}
    else:
        positions = [2 * CARRIAGE_TRAVEL * k / (CARRIAGE_STEPS - 1) for k in range(CARRIAGE_STEPS)]
        stubs = {p: rail_stub(CARRIAGE_L + p + 20.0, p).val() for p in positions}
        kn = knob_free().val()
        rail_car = {p: sh_vol(stubs[p].intersect(car)) for p in positions}
        print("carro vs riel", rail_car, "perilla vs carro", sh_vol(kn.intersect(car)), flush=True)
    for t in tilts:
        ic = interference(parts, [car], t)
        ir = max(sum(interference(parts, [stubs[p]], t).values()) for p in positions)
        ik = sum(interference(parts, [kn], t).values()) if CARRIAGE_MODE != "tope" else 0.0
        hinge[t] = (sum(ic.values()), ir, ic, ik)
        print("tilt", t, "carro", round(hinge[t][0], 3), "riel", round(ir, 3), "perilla", round(ik, 3), flush=True)

    # dummies fit
    cam, led = camera_dummy().val(), led_ring_dummy().val()
    fit = {"camara-cuerpo": sh_vol(cam.intersect(body)), "camara-tapa": sh_vol(cam.intersect(lid)),
           "camara-bisel": sh_vol(cam.intersect(bez)), "led-cuerpo": sh_vol(led.intersect(body)),
           "led-camara": sh_vol(led.intersect(cam)), "ventana-cuerpo": sh_vol(win.intersect(body)),
           "ventana-bisel": sh_vol(win.intersect(bez))}
    print("fit", fit)

    # buoyancy
    cav = capsule_cavity().val()
    air = (cav.Volume() - sh_vol(cav.intersect(body))) / 1000.0
    v = {k: R[k]["vol"] for k in R}
    petg = v["M4_capsula_cuerpo"] + v["M5_capsula_tapa"] + v["M6_capsula_bisel"]
    disp = petg + air + v["M7_capsula_ventana"]

    def mass(shape, infill):
        V = shape.Volume()
        shell = min(V, shape.Area() * SHELL_T)
        return PETG_DENSITY * (shell + infill * (V - shell)) / 1000.0

    m = dict(M4=mass(body, 1.0), M5=mass(lid, 1.0), M6=mass(bez, 0.4), M6_100=mass(bez, 1.0),
             M7=ACRYLIC_DENSITY * v["M7_capsula_ventana"], M10_100=mass(car, 1.0), M10_40=mass(car, 0.4))
    m["set"] = m["M4"] + m["M5"] + m["M6"] + m["M7"]
    m["set100"] = m["M4"] + m["M5"] + m["M6_100"] + m["M7"]
    buoy = dict(petg=petg, air=air, win=v["M7_capsula_ventana"], disp=disp, m=m)
    print("buoyancy", buoy)

    # renders
    from render import render
    for t in (0, 90):
        s_end = 2 * CARRIAGE_TRAVEL if CARRIAGE_MODE != "tope" else -FIT_CLEAR
        items = [(rail_stub(CARRIAGE_L + s_end + 20.0, s_end), "#b0b0b0", 0.45, True, None), (car, "#e07b39", 1.0, True, None)]
        if CARRIAGE_MODE != "tope":
            items.append((knob_free(), "#777777", 0.35, True, None))
        for sh, col, op in ((body, "#3a7ca5", 1.0), (lid, "#2f5d7c", 1.0), (bez, "#555555", 1.0), (win, "#9fd3ff", 0.5)):
            items.append((place_capsule(sh, t), col, op, True, None))
        render(items, OUT / f"capsula_carro_{t}.png", "iso", title=f"M10 + capsula, inclinacion {t} grados")

    write_report(rows, hinge, fit, buoy)


def write_report(rows, hinge, fit, buoy):
    R = {r["stem"]: r for r in rows}
    m = buoy["m"]
    L = ["# Reporte de la capsula de camara (M4..M7) y el carro M10",
         "",
         "Generado por `capsula.py`. Base: P4 rev. B de `../cad/parts.py` con los cambios del equipo.",
         "Salida en `../salida/preliminar/` (`stl/`, `step/`, `capsula_carro_0.png`, `capsula_carro_90.png`).",
         "",
         "## Geometria",
         f"- Camara Arducam Mega 5MP AF {CAMERA[0]:g} x {CAMERA[1]:g} x {CAMERA[2]:g} (antes 25 de alto). Cavidad "
         f"{CAP_CAV_W:g} x {CAP_CAV_H:g} x {CAP_CAV_L:g} (antes 38 x 38 x 50): {CAMERA[2]:g} de camara, de los cuales "
         f"{BEHIND_WALL:.1f} quedan detras de la pared frontal, mas {CAP_REAR_ZONE:g} de zona trasera (cable + contratuerca PG7).",
         f"- Anillo LED Ø{LED_RING[0]:g} x {LED_RING[1]:g} pegado a la cara interior de la pared frontal; tubo separador opaco "
         f"(pared {LED_SEPARATOR[0]:g}, sobresale {LED_SEPARATOR[1]:g} sobre el anillo, largo total {LED_STACK:g}) alrededor del "
         f"porta-lente Ø{LENS_D:g}. Apertura anular de luz Ø{LENS_APERTURE:g} con {LED_SPOKES[0]} radios de {LED_SPOKES[1]:g} que sujetan el tubo.",
         f"- Bisagra de {HINGE_TEETH} dientes, eje M4 fuera del sello, PG7 en la pared inferior (a {CAP_GLAND_X:g} de la apertura).",
         (f"- M10 (modo deslizante): manga cerrada abierta en los dos extremos (holgura {FIT_CLEAR:g} por lado, pared {CARRIAGE_WALL:g}, "
          f"largo {CARRIAGE_L:g}); perilla abajo, atras, con el M4 al centro de la ranura T; rendija de {RAIL_EXIT_SLOT[0] + 2 * CARRIAGE_SLIT_CLR:g} "
          f"en +Y a todo lo largo para el Cat5e; quilla con las orejas delante de la perilla y eje a x = {carriage_axis()[0]:g}, "
          f"z = {carriage_axis()[1]:g} (bajo el riel, la capsula a 0 grados queda {CARRIAGE_AXIS_CLR:g} bajo el fondo del riel). "
          f"El riel puede pasar hasta {2 * CARRIAGE_TRAVEL:g} mas alla de la manga, sobre la capsula.")
         if CARRIAGE_MODE != "tope" else
         (f"- M10 (modo tope): manga con labios, M4 vertical arriba, placa de tope de {CARRIAGE_END_T:g} y eje a {carriage_axis_x():g}."),
         "",
         "## Piezas",
         "",
         "| pieza | STL | BRep/BOP | estanco | cuerpos | bbox en orientacion (mm) | voladizo mm2 | espesor min p1 (mm) | masa 100 % (g) | volumen (cm3) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    mass100 = {"M4_capsula_cuerpo": m["M4"], "M5_capsula_tapa": m["M5"], "M6_capsula_bisel": m["M6_100"],
               "M7_capsula_ventana": m["M7"], "M10_carro_capsula": m["M10_100"]}
    for r in rows:
        mc = r["mc"]
        flag = " **(< 1.2)**" if r["p1"] < MIN_WALL else ""
        L.append(f"| {r['name']} | {r['stem']}.stl | {'ok' if r['chk']['ok'] else 'FALLA'} | {'si' if mc['watertight'] else 'NO'} | "
                 f"{mc['bodies']} | {' x '.join(f'{v:.1f}' for v in mc['bbox'])} ({r['orient']}) | {mc['overhang_mm2']:.0f} | "
                 f"{r['p1']:.2f}{flag} (min {r['pmin']:.2f}) | {mass100[r['stem']]:.1f} | {r['vol']:.2f} |")
    L += ["", "M7 es el disco de acrilico (masa con densidad del acrilico); no se imprime. Orientacion de impresion: la de menor voladizo entre "
          "las seis probadas (giros de 90 grados sobre X e Y) que cabe en la cama; la columna indica el giro aplicado al marco de la pieza.",
          "", "## Rango de la bisagra (interferencia en mm3)",
          f"Inclinacion hacia abajo de 0 a 90; contra el riel se toma el peor de {CARRIAGE_STEPS} posiciones del carro, con la punta del "
          f"riel de 0 a {2 * CARRIAGE_TRAVEL:g} mas alla de la manga (recorrido +-{CARRIAGE_TRAVEL:g}).", "",
          "| inclinacion | capsula vs carro | capsula vs riel (peor posicion) | capsula vs perilla | M4 carro | M5 carro | M6 carro |",
          "|---|---|---|---|---|---|---|"]
    for t, (c, rr, ic, ik) in hinge.items():
        L.append(f"| {t} | {c:.2f} | {rr:.2f} | {ik:.2f} | {ic['M4']:.2f} | {ic['M5']:.2f} | {ic['M6']:.2f} |")
    L += ["", "Ajuste de las maquetas (mm3, debe ser 0): " + "; ".join(f"{k} {v:.2f}" for k, v in fit.items()), "",
          "## Flotabilidad por capsula",
          f"- PETG M4+M5+M6: {buoy['petg']:.1f} cm3.",
          f"- Aire encerrado (cavidad menos tubo y radios): {buoy['air']:.1f} cm3.",
          f"- Ventana: {buoy['win']:.2f} cm3.",
          f"- Volumen desplazado total: {buoy['disp']:.1f} cm3 (antes {CAPSULE_SET_DISP_CM3:g}).",
          f"- Masa con M4 y M5 al 100 % y M6 al 40 % (piel {SHELL_T:g}): M4 {m['M4']:.1f} + M5 {m['M5']:.1f} + M6 {m['M6']:.1f} + ventana {m['M7']:.1f} = "
          f"**{m['set']:.1f} g** (antes {CAPSULE_SET_G:g} g). Con M6 al 100 %: {m['set100']:.1f} g.",
          f"- Con contenido (CAPSULE_CONTENT_G) no incluido. Empuje: {buoy['disp'] * 1.025:.1f} g contra {m['set']:.1f} g de la pieza.",
          f"- M10 aparte: {m['M10_100']:.1f} g al 100 %, {m['M10_40']:.1f} g al 40 %.", ""]
    (HERE / "reporte_capsula.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
