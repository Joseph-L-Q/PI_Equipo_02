"""45 degree chamfer feet where a support (post, standoff, boss, rib, wall) meets its base plate: params
chaflan.base_soportes (default) and chaflan.base_soportes_max (tried first). Observation of the lab instructor, 01/11/2026,
for B2_cubierta, B3_caja, B5_cuna and M1s_caja_cuerpo.

The feet are built as solids and unioned (never .chamfer() on selected edges, which breaks after many booleans):
  cone()      frustum r + c at the plate face -> r at c above it (posts, pillars, columns, standoffs, bosses)
  frustum()   the support footprint grown by c at the plate face -> the footprint at c above it (ribs, walls, ears)
  inner_ring() the 45 degree strip along the inside of a rounded-rect cavity (floor <-> inner walls)
Each foot is clipped to the prism of its plate (it never overhangs the plate edge) and tried at the largest size first;
if it touches a keep-out (screw heads, components, bottles, gland nuts) the next smaller size is tried. LOG keeps what
was placed, per piece, for the report. With chaflan.base_soportes = 0 nothing is added (the previous version).
"""
import cadquery as cq

import params as P

LOG = {}


def sizes():
    c0, cm = P.CHAMFER_BASE, P.CHAMFER_BASE_MAX
    if c0 <= 0:
        return []
    return ([cm] if cm > c0 else []) + [c0] + [c for c in (1.0, 0.5) if c < c0]


def on():
    return bool(sizes())


def cone(x, y, z, r, c, down=False):
    return cq.Workplane().add(cq.Solid.makeCone(r + c, r, c, cq.Vector(x, y, z), cq.Vector(0, 0, -1 if down else 1)))


def frustum(x0, x1, y0, y1, z, c, down=False):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return (cq.Workplane("XY").workplane(offset=z).center(cx, cy).rect(x1 - x0 + 2 * c, y1 - y0 + 2 * c)
            .workplane(offset=-c if down else c).rect(x1 - x0, y1 - y0).loft(combine=True))


def slab(rects, z, c, down=False):
    """Prism of the plate(s) (x0, x1, y0, y1) from the plate face z to c above (or below) it: the feet are clipped to it."""
    s = None
    for x0, x1, y0, y1 in rects:
        za, zb = (z - c, z) if down else (z, z + c)
        b = cq.Workplane("XY").box(x1 - x0, y1 - y0, zb - za, centered=False).translate((x0, y0, za))
        s = b if s is None else s.union(b)
    return s


def inner_ring(L, W, r, z, c, down=False):
    """Material left by a 45 degree chamfer along the inside of an L x W cavity with corner radius r, at the floor z
    (down=True: at a ceiling z, the pocket hangs below)."""
    za = z - c if down else z
    full = cq.Workplane("XY").workplane(offset=za).rect(L, W).extrude(c).edges("|Z").fillet(r)
    s_small = cq.Sketch().rect(L - 2 * c, W - 2 * c).vertices().fillet(max(r - c, 0.4))
    s_big = cq.Sketch().rect(L, W).vertices().fillet(r)
    a, b = (s_big, s_small) if down else (s_small, s_big)
    tool = cq.Workplane("XY").workplane(offset=za).placeSketch(a, b.moved(cq.Location(cq.Vector(0, 0, c)))).loft()
    return full.cut(tool)


def inner_ring_rect(cx, cy, L, W, z, c, down=False):
    """inner_ring for a sharp-cornered L x W cavity centred on (cx, cy)."""
    za = z - c if down else z
    full = cq.Workplane("XY").box(L, W, c, centered=False).translate((cx - L / 2, cy - W / 2, za))
    lo, hi = ((L, W), (L - 2 * c, W - 2 * c)) if down else ((L - 2 * c, W - 2 * c), (L, W))
    tool = (cq.Workplane("XY").workplane(offset=za).center(cx, cy).rect(*lo).workplane(offset=c).rect(*hi).loft(combine=True))
    return full.cut(tool)


def _vol(w):
    try:
        return sum(s.Volume() for s in w.solids().vals())
    except Exception:
        return 0.0


def _wp(k):
    return k if isinstance(k, cq.Workplane) else cq.Workplane().add(k)


def _hits(s, keepouts):
    bb = s.val().BoundingBox()
    for k in map(_wp, keepouts):
        kb = k.val().BoundingBox()
        if bb.xmax < kb.xmin or kb.xmax < bb.xmin or bb.ymax < kb.ymin or kb.ymax < bb.ymin or bb.zmax < kb.zmin or kb.zmax < bb.zmin:
            continue
        if _vol(s.intersect(k)) > 1e-3:
            return True
    return False


def fit(piece, joint, make, plate=None, keepouts=(), cut=()):
    """Largest size c whose foot make(c), clipped to plate(c) and minus the cut solids, touches no keep-out.
    Returns the foot (or None) and logs (joint, c)."""
    for c in sizes():
        s = make(c)
        if plate is not None:
            s = s.intersect(plate(c))
        for k in cut:
            s = s.cut(_wp(k))
        if _vol(s) < 1e-3:
            continue
        if keepouts and _hits(s, keepouts):
            continue
        LOG.setdefault(piece, []).append((joint, c))
        return s
    LOG.setdefault(piece, []).append((joint, 0.0))
    return None


def add(shape, feet):
    for f in feet:
        if f is not None:
            shape = shape.union(f)
    return shape


def summary(piece):
    """{joint group: (n, min c, max c)}; the group is the joint name up to the first '#'."""
    out = {}
    for j, c in LOG.get(piece, []):
        g = j.split("#")[0].strip()
        n, a, b = out.get(g, (0, 99.0, 0.0))
        out[g] = (n + 1, min(a, c), max(b, c))
    return out


def head_keepout(x, y, z, h=12.0, r=3.5):
    """Seat of an M3 head / washer (Ø5.5 + 0.75 around) on a hole at (x, y) on the face z: no foot may cover it."""
    return cq.Workplane().add(cq.Solid.makeCylinder(r, h, cq.Vector(x, y, z), cq.Vector(0, 0, 1)))
