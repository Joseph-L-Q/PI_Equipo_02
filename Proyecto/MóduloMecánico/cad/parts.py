"""Part builders. Each returns a CadQuery Workplane in its own local frame.

Local frames
  capsule : hinge axis = global Y through the origin; optical axis +X; window at the far +X end.
  arm     : root face at x = 0 on the box pad, tube along +X, centreline z = 0, hinge axis at x = arm_axis_x().
  box     : cavity centred on x = y = 0, outer bottom at z = 0.
  frame   : mesh plane z = 0, centred on the origin.
"""
import functools
import math

import cadquery as cq

from params import *  # noqa: F403  (all dimensions)


# ------------------------------------------------------------------ helpers
@functools.lru_cache(maxsize=None)   # ~50 s per call; returned Workplanes are never mutated
def serration(r_in, r_out, n, h, offset_deg=0.0):
    """Radial teeth on the y = 0 plane pointing +Y, around the Y axis.

    Each tooth is a wedge: its base spans exactly one pitch angle, so neighbours share their radial
    base edge and no sliver is left between them (the old constant-width prisms left 0.003 mm gaps
    that Parasolid/Onshape reports as faults). Height h is constant, so at every radius the profile
    is the same triangle wave and a set offset by half a pitch meshes flank to flank.
    Teeth are built past both radii and trimmed by an annulus, so the outer face is the cylinder
    r_out (flush with the disc edge) instead of a chord."""
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


def capsule_body():
    out_w, out_h, fl_w, fl_h, x_lid0, x0, x_front = cap_dims()
    L = CAP_CAV_L + CAP_FRONT
    body = cq.Workplane("YZ").workplane(offset=x0).rect(out_w, out_h).extrude(L).edges("|X").fillet(3)
    flange = cq.Workplane("YZ").workplane(offset=x0).rect(fl_w, fl_h).extrude(CAP_FLANGE_T).edges("|X").fillet(4)
    body = body.union(flange)
    cav = cq.Workplane("YZ").workplane(offset=x0).rect(CAP_CAV_W, CAP_CAV_H).extrude(CAP_CAV_L).edges("|X").fillet(2)
    body = body.cut(cav)
    # window seat from outside + clear aperture
    seat = cq.Workplane("YZ").workplane(offset=x_front - WIN_SEAT_DEPTH).circle(WIN_DIA / 2 + 0.2).extrude(WIN_SEAT_DEPTH)
    ap = cq.Workplane("YZ").workplane(offset=x_front - CAP_FRONT).circle(LENS_APERTURE / 2).extrude(CAP_FRONT)
    body = body.cut(seat).cut(ap)
    # bezel pilot holes (blind, 6 mm into the front wall region outside the seat)
    for k in range(BEZEL_SCREWS):
        a = math.radians(90 + k * 360 / BEZEL_SCREWS)
        r = (WIN_DIA / 2 + BEZEL_OD / 2) / 2
        h = (cq.Workplane("YZ").workplane(offset=x_front - 4.0)
             .center(r * math.cos(a), r * math.sin(a)).circle(M2_PILOT / 2).extrude(4.0))
        body = body.cut(h)
    # flange through-holes (M3 with nuts)
    for (y, z) in cap_screw_pts():
        body = body.cut(cq.Workplane("YZ").workplane(offset=x0).center(y, z).circle(M3_CLEAR / 2).extrude(CAP_FLANGE_T))
    # PG7 cable gland on the bottom wall, near the rear (cable runs back to the arm)
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
    for k in range(BEZEL_SCREWS):
        a = math.radians(90 + k * 360 / BEZEL_SCREWS)
        r = (WIN_DIA / 2 + BEZEL_OD / 2) / 2
        b = b.cut(cq.Workplane("YZ").workplane(offset=x_front).center(r * math.cos(a), r * math.sin(a))
                  .circle(2.4 / 2).extrude(BEZEL_T))
    return b


def camera_dummy():
    L, W, H, *_ = COMPONENTS["arducam_mega_5mp"]
    _, _, _, _, _, x0, x_front = cap_dims()
    # board + lens envelope, lens touching 1 mm behind the window shoulder
    x_end = x_front - CAP_FRONT - 1.0
    return cq.Workplane("YZ").workplane(offset=x_end - H).rect(W, L).extrude(H)


# ------------------------------------------------------------------ box
def box_dims():
    out_l = BOX_CAV_L + 2 * BOX_WALL
    out_w = BOX_CAV_W + 2 * BOX_WALL
    out_h = BOX_FLOOR + BOX_CAV_H
    return out_l, out_w, out_h


def box_screw_pts():
    out_l, out_w, _ = box_dims()
    a = out_l / 2 + BOX_FLANGE / 2
    b = out_w / 2 + BOX_FLANGE / 2
    return [(a, b), (-a, b), (a, -b), (-a, -b), (0, b), (0, -b)]


def arm_z():
    """Arm centreline height above the box bottom."""
    return BOX_FLOOR + GLAND_Z


def box_body():
    out_l, out_w, out_h = box_dims()
    body = cq.Workplane("XY").rect(out_l, out_w).extrude(out_h).edges("|Z").fillet(5)
    flange = (cq.Workplane("XY").workplane(offset=out_h - BOX_FLANGE_T)
              .rect(out_l + 2 * BOX_FLANGE, out_w + 2 * BOX_FLANGE).extrude(BOX_FLANGE_T).edges("|Z").fillet(6))
    body = body.union(flange)
    z_sk = out_h - BOX_FLANGE_T
    skirt = (cq.Workplane("XY").workplane(offset=z_sk - BOX_FLANGE).rect(out_l, out_w)
             .workplane(offset=BOX_FLANGE).rect(out_l + 2 * BOX_FLANGE, out_w + 2 * BOX_FLANGE).loft())
    body = body.union(skirt)
    cav = cq.Workplane("XY").workplane(offset=BOX_FLOOR).rect(BOX_CAV_L, BOX_CAV_W).extrude(BOX_CAV_H).edges("|Z").fillet(3)
    body = body.cut(cav)
    for (x, y) in box_screw_pts():
        body = body.cut(cq.Workplane("XY").workplane(offset=out_h - BOX_FLANGE_T).center(x, y)
                        .circle(M3_CLEAR / 2).extrude(BOX_FLANGE_T))
    # arm pads on both end walls, with PG7 hole and 4 heat-set insert holes
    z = arm_z()
    for s in (1, -1):
        x_face = s * out_l / 2
        pad = (cq.Workplane("YZ").workplane(offset=x_face if s > 0 else x_face - ARM_PAD_T)
               .center(0, z).rect(ARM_PAD, ARM_PAD).extrude(ARM_PAD_T).edges("|X").fillet(3))
        x_out = x_face + s * ARM_PAD_T
        z_b = z - ARM_PAD / 2
        gusset = (cq.Workplane("XZ").polyline([(x_face, z_b), (x_out, z_b), (x_face, z_b - ARM_PAD_T)]).close()
                  .extrude(ARM_PAD / 2, both=True))
        body = body.union(pad).union(gusset)
        g = (cq.Workplane("YZ").workplane(offset=(x_out if s < 0 else x_face - BOX_WALL))
             .center(0, z).circle(PG7_HOLE / 2).extrude(ARM_PAD_T + BOX_WALL))
        body = body.cut(g)
        for (dy, dz) in ((12, 12), (-12, 12), (12, -12), (-12, -12)):
            x_ins = x_out - s * M3_INSERT_DEPTH
            ins = (cq.Workplane("YZ").workplane(offset=min(x_out, x_ins)).center(dy, z + dz)
                   .circle(M3_INSERT_HOLE / 2).extrude(M3_INSERT_DEPTH))
            body = body.cut(ins)
    # JSN-SR04T probe through the floor, centred
    body = body.cut(cq.Workplane("XY").circle(JSN_PROBE_DIA / 2 + 0.2).extrude(BOX_FLOOR))
    return body


def box_lid():
    out_l, out_w, out_h = box_dims()
    z0 = out_h
    lid = (cq.Workplane("XY").workplane(offset=z0).rect(out_l + 2 * BOX_FLANGE, out_w + 2 * BOX_FLANGE)
           .extrude(BOX_LID_T).edges("|Z").fillet(6))
    for (x, y) in box_screw_pts():
        lid = lid.cut(cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(M3_CLEAR / 2).extrude(BOX_LID_T))
    cl_l = (BOX_CAV_L + out_l + BOX_FLANGE) / 2
    cl_w = (BOX_CAV_W + out_w + BOX_FLANGE) / 2
    outer = cq.Workplane("XY").workplane(offset=z0).rect(cl_l + GROOVE_WIDTH, cl_w + GROOVE_WIDTH).extrude(GROOVE_DEPTH).edges("|Z").fillet(6)
    inner = cq.Workplane("XY").workplane(offset=z0).rect(cl_l - GROOVE_WIDTH, cl_w - GROOVE_WIDTH).extrude(GROOVE_DEPTH).edges("|Z").fillet(3.5)
    lid = lid.cut(outer.cut(inner))
    # PG9 umbilical gland beside the handle
    lid = lid.cut(cq.Workplane("XY").workplane(offset=z0).center(0, LID_GLAND_Y).circle(PG9_HOLE / 2).extrude(BOX_LID_T))
    # handle: arch over y = 0, glove-sized opening, with an anchor eye at the top
    zt = z0 + BOX_LID_T
    leg = 12.0
    span = HANDLE_GRIP + 2 * leg
    handle = (cq.Workplane("XZ").workplane(offset=-6).center(0, zt + HANDLE_H / 2)
              .rect(span, HANDLE_H).extrude(12))
    hw, wall_h = HANDLE_GRIP / 2, 8.0
    roof = HANDLE_H - 10 - wall_h
    window = (cq.Workplane("XZ").workplane(offset=-6)
              .polyline([(-hw, zt), (hw, zt), (hw, zt + wall_h), (hw - roof, zt + wall_h + roof),
                         (-hw + roof, zt + wall_h + roof), (-hw, zt + wall_h)]).close().extrude(12))
    handle = handle.cut(window).edges("|Y").fillet(3)
    eye = (cq.Workplane("XZ").workplane(offset=-6).center(0, zt + HANDLE_H + 6).circle(10).circle(5).extrude(12))
    return lid.union(handle).union(eye)


def box_components():
    """Dummy envelopes (component name, solid) placed on 5 mm standoffs."""
    z = BOX_FLOOR + 5.0
    xl, xr = -BOX_CAV_L / 2 + 2.0, BOX_CAV_L / 2 - 2.0
    yf, yb = -BOX_CAV_W / 2 + 2.0, BOX_CAV_W / 2 - 2.0
    out = []

    def place(name, x0, y0, flip_x=False, flip_y=False):
        L, W, H, *_ = COMPONENTS[name]
        x = x0 - L if flip_x else x0
        y = y0 - W if flip_y else y0
        out.append((name, cq.Workplane("XY").box(L, W, H, centered=False).translate((x, y, z))))

    place("esp32_devkit_wroom32u", xl, yf)
    place("microsd_module", xl, yb, flip_y=True)
    place("max485_module", xr, yf, flip_x=True)
    place("jsn_sr04t_board", xr, yb, flip_x=True, flip_y=True)
    probe = cq.Workplane("XY").circle(JSN_PROBE_DIA / 2).extrude(JSN_PROBE_LEN).translate((0, 0, BOX_FLOOR - 4))
    out.append(("jsn_sr04t_probe", probe))
    return out


# ------------------------------------------------------------------ arm
def ring_pos():
    """Saddle position along the arm so that it lands on the lantern ring."""
    out_l = BOX_CAV_L + 2 * BOX_WALL
    pos = LANTERN_RING_D / 2 - out_l / 2 - ARM_PAD_T
    assert 24 <= pos <= ARM_LEN - 16, f"saddle at {pos:.0f} mm is off the arm: change ARM_LEN or the ring"
    return pos


def arm_axis_x():
    return ARM_LEN + FORK_REACH - ARM_H / 2


def arm():
    t = ARM_WALL
    tube = cq.Workplane("YZ").rect(ARM_W, ARM_H).extrude(ARM_LEN).edges("|X").fillet(2)
    tube = tube.cut(cq.Workplane("YZ").workplane(offset=ARM_FLANGE_T).rect(ARM_W - 2 * t, ARM_H - 2 * t)
                    .extrude(ARM_LEN - ARM_FLANGE_T - 4.0))
    flange = cq.Workplane("YZ").rect(ARM_PAD, ARM_PAD).extrude(ARM_FLANGE_T).edges("|X").fillet(3)
    a = tube.union(flange)
    # root: clearance for the PG7 gland body + 4 screws; tip: cable exit hole downward
    a = a.cut(cq.Workplane("YZ").circle(10.0).extrude(ARM_FLANGE_T))
    for (dy, dz) in ((12, 12), (-12, 12), (12, -12), (-12, -12)):
        a = a.cut(cq.Workplane("YZ").center(dy, dz).circle(M3_CLEAR / 2).extrude(ARM_FLANGE_T))
    a = a.cut(cq.Workplane("XY").workplane(offset=-ARM_H / 2).center(ARM_LEN - 14, 0).circle(5.0).extrude(t))
    # fork: two ears with inner serrations, axis along Y
    ax = arm_axis_x()
    for s in (1, -1):
        y0 = s * HINGE_GAP / 2
        ear = (cq.Workplane("XZ").workplane(offset=-(y0 + s * HINGE_EAR_T) if s > 0 else -y0)
               .center((ARM_LEN - 4 + ax) / 2, 0).rect(ax - ARM_LEN + 4, ARM_H).extrude(HINGE_EAR_T))
        tip = (cq.Workplane("XZ").workplane(offset=-(y0 + s * HINGE_EAR_T) if s > 0 else -y0)
               .center(ax, 0).circle(ARM_H / 2).extrude(HINGE_EAR_T))
        ear = ear.union(tip)
        teeth = serration(HINGE_TEETH_RIN, HINGE_DISC_D / 2, HINGE_TEETH, HINGE_TOOTH_H, offset_deg=180.0 / HINGE_TEETH)
        teeth = (teeth.mirror("XZ") if s > 0 else teeth).translate((ax, y0, 0))
        a = a.union(ear).union(teeth)
    a = a.cut(cq.Workplane("XZ").center(ax, 0).circle(M4_CLEAR / 2).extrude(30, both=True))
    # saddle on the lantern ring + strap slot
    sx = ring_pos()
    saddle = cq.Workplane("XY").workplane(offset=-ARM_H / 2 - 12).center(sx, 0).rect(24, ARM_W).extrude(12)
    rod = cq.Workplane("XZ").center(sx, -ARM_H / 2 - 12).circle(RING_ROD_D / 2 + 0.5).extrude(ARM_W, both=True)
    slot = (cq.Workplane("YZ").workplane(offset=sx - 12).center(0, -ARM_H / 2 - 4)
            .rect(STRAP_SLOT[0], STRAP_SLOT[1]).extrude(24))
    zb = -ARM_H / 2 - 12
    ramp = (cq.Workplane("XZ").polyline([(sx - 12, -ARM_H / 2), (sx - 12, zb), (sx - 24, -ARM_H / 2)]).close()
            .extrude(ARM_W / 2, both=True))
    a = a.union(saddle.union(ramp).cut(rod).cut(slot))
    return a


# ------------------------------------------------------------------ test frame
def mesh_frame():
    f = cq.Workplane("XY").rect(FRAME_OUT, FRAME_OUT).extrude(FRAME_T)
    inner = FRAME_OUT - 2 * FRAME_BAR
    f = f.cut(cq.Workplane("XY").rect(inner, inner).extrude(FRAME_T))
    pitch = MESH_OPENING + MESH_BAR
    n = int(inner // pitch)
    grid = None
    for k in range(-n // 2, n // 2 + 1):
        for horiz in (False, True):
            bar = cq.Workplane("XY").rect(inner, MESH_BAR) if horiz else cq.Workplane("XY").rect(MESH_BAR, inner)
            bar = bar.extrude(MESH_T).translate((0, k * pitch, 0) if horiz else (k * pitch, 0, 0))
            grid = bar if grid is None else grid.union(bar)
    f = f.union(grid)
    for x in (-1, 1):
        for y in (-1, 1):
            f = f.cut(cq.Workplane("XY").center(x * (FRAME_OUT / 2 - FRAME_BAR / 2), y * (FRAME_OUT / 2 - FRAME_BAR / 2))
                      .circle(M4_CLEAR / 2).extrude(FRAME_T))
    return f.translate((0, 0, -FRAME_T / 2))
