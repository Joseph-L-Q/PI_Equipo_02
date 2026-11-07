"""Decorative SKIN for presenting: a cover that sits on the lid M2 of P2/P4 and is held by the lid's own 12 M3 screws
(2 mm longer), no glue. The node geometry is not touched: the lid, its handle, the umbilical gland and the P4 logo are
read from the prototype's assembly STEP and kept free.

    python skin.py [P4_estetico|P2_robusto ...]     (default: both; theme = params skin.tema)

Theme "concha": scallop shell. Fan of radial ribs from a hinge just in front of the handle, a wavy lip where the ribs
meet the perimeter frame, and on the back half a plate with "LanternGuard" / "UPCH" raised skin.relieve. Everything
is extruded up from the face that rests on the lid, so it prints face down without supports and roofs nothing: the lid
shows between the ribs and no air is trapped. The whole skin is clipped by the lid outline inset skin.retiro, so in
plan it never leaves the lid (the cords pass 2.9 mm from the flange in P2).

Outputs in salida/skin/<proto>/<tema>/: SKIN_<tema>.step (in assembly position, for Onshape), SKIN_<tema>.stl (print
orientation, base on z = 0), skin.json (volume, checks, apparent weight and ballast with the skin on).
"""
import json
import math
import sys
from pathlib import Path

import cadquery as cq

import params as P
from checks import brep_check, fix_step_stamp, min_thickness

MOD = Path(__file__).resolve().parent.parent
RHO_W = 1.025                    # g/cm3, sea water (same as simple.py)
LOGO_SVG = MOD / "assets" / "logo_upch.svg"
TALL = 40.0
LIP_W = 3.0                      # uniform width of the wavy lip band along the frame (mm)
LIP_GAP = 2.0                    # clearance from a lobe to the rib sides: wider than a wall, so no sliver is born


def by_volume(proto):
    """Solids of the prototype assembly with their names (ensamble_solidos.json, matched by volume)."""
    folder = MOD / "salida" / "prototipos" / proto
    solids = cq.importers.importStep(str(folder / "ensamble_simple_D200.step")).solids().vals()
    table = json.loads((folder / "ensamble_solidos.json").read_text(encoding="utf-8"))["solidos"]
    out = {}
    for s in solids:
        v = s.Volume()
        hit = min(table, key=lambda t: abs(t["volumen_mm3"] - v))
        out.setdefault(hit["nombre"], s)
    return out


def lid_data(parts):
    m2 = parts["M2_caja_tapa"]
    ups = [f for f in m2.Faces() if f.geomType() == "PLANE" and f.normalAt().z > 0.99]
    z0 = min(f.Center().z for f in ups if f.Area() > 5000)
    plate = max((f for f in ups if abs(f.Center().z - z0) < 0.05), key=lambda f: f.Area())
    outline = plate.outerWire()
    slab = cq.Solid.makeBox(600, 600, 300, cq.Vector(-300, -300, z0 + 0.15))
    above = [s for s in m2.intersect(slab).Solids()]
    handle = [s.BoundingBox() for s in above if s.BoundingBox().zlen > 2]
    logo = [s.BoundingBox() for s in above if s.BoundingBox().zlen <= 2]
    screws = sorted({(round(e.arcCenter().x, 1) + 0.0, round(e.arcCenter().y, 1) + 0.0) for e in m2.Edges()
                     if e.geomType() == "CIRCLE" and abs(e.radius() - 1.7) < 0.15 and abs(e.arcCenter().z - z0) < 0.6})
    umb = parts.get("REF_umbilical")
    gland = None
    if umb is not None:              # foot = the umbilical's flat end face resting on the lid (a boolean here took minutes)
        feet = [f for f in umb.Faces() if f.geomType() == "PLANE" and abs(f.Center().z - z0) < 0.6]
        if feet:
            c = max(feet, key=lambda f: f.Area()).Center()
            gland = (c.x, c.y)
    return dict(m2=m2, z0=z0, outline=outline, handle=handle, logo=logo, screws=screws, gland=gland)


def prism(wire_or_pts, h, z, d=0.0):
    """Vertical prism of a closed wire (offset by d, negative = inward) or of a point list, from z to z + h."""
    if isinstance(wire_or_pts, list):
        w = cq.Wire.makePolygon([cq.Vector(x, y, 0) for x, y in wire_or_pts], close=True)
    else:
        w = wire_or_pts.moved(cq.Location(cq.Vector(0, 0, -wire_or_pts.Center().z)))
    if d:
        w = w.offset2D(d, "arc")[0]
    return cq.Solid.extrudeLinear(cq.Face.makeFromWires(w), cq.Vector(0, 0, h)).moved(cq.Location(cq.Vector(0, 0, z)))


def box(x0, x1, y0, y1, z, h):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, h, cq.Vector(x0, y0, z))


def ellipse(cx, cy, a, b, z, h):
    return cq.Workplane("XY").workplane(offset=z).center(cx, cy).ellipse(a, b).extrude(h).val()


def angles(a0, a1, n):
    return [a0 + (a1 - a0) * i / (n - 1) for i in range(n)]


def graze(hx, hy, ths, pearl, w):
    """Worst rib against the pearl ellipse: for a rib that misses it, the gap between rib side and ellipse; for one
    that crosses it, the depth of the ellipse beyond the rib side. Both must reach skin.pared_min."""
    cx, cy, a, b = pearl
    pts = [(cx + a * math.cos(t), cy + b * math.sin(t)) for t in (2 * math.pi * k / 720 for k in range(720))]
    worst = 1e9
    for th in ths:
        ux, uy = math.cos(th), math.sin(th)
        side = [(-(px - hx) * uy + (py - hy) * ux) for px, py in pts if (px - hx) * ux + (py - hy) * uy > 0]
        if not side:
            continue
        lo, hi = min(side), max(side)
        if lo > 0 or hi < 0:                                              # misses: clearance to the rib side
            worst = min(worst, min(abs(lo), abs(hi)) - w / 2)
        else:                                                             # crosses: ellipse beyond each rib side
            worst = min(worst, hi - w / 2, -lo - w / 2)
    return worst


def ray_to_rect(hx, hy, th, x0, x1, y0, y1):
    """Distance from (hx, hy) along angle th to the boundary of the rectangle that contains the point."""
    c, s = math.cos(th), math.sin(th)
    ts = []
    if abs(c) > 1e-9:
        ts += [(x0 - hx) / c, (x1 - hx) / c]
    if abs(s) > 1e-9:
        ts += [(y0 - hy) / s, (y1 - hy) / s]
    return min(t for t in ts if t > 0)


def rib(hx, hy, th, r0, r1, z, w, h_in, h_out):
    prof = cq.Workplane("XZ").polyline([(r0, 0), (r1, 0), (r1, h_out), (r0, h_in)]).close().extrude(w / 2, both=True)
    return prof.val().rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), math.degrees(th)).moved(cq.Location(cq.Vector(hx, hy, z)))


FONT = Path("C:/Windows/Fonts/ariblk.ttf")     # Arial Black: plain sans, no serifs, stems ~0.2 em (>= pared_min at 8 mm caps)
CAP_MIN = 8.0                                   # minimum cap height of the lettering (mm)
SINK = 0.05                                     # text sunk into the plate: the fuse never meets two coplanar faces


BOLD = 0.3                                      # outline grown on each side: the thinnest diagonal of Arial Black at 11 mm
                                                # caps is ~1.3 mm, + 2 x 0.2 clears pared_min


def _outline(txt, size):
    """Letters as clean shapely polygons: the font's B-spline outline (self-intersecting in OCCT's builder) sampled
    every 0.1 mm, unioned and grown by BOLD with round joins. Polygons only: the later fuse sees planar faces."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    kw = dict(combine=False, halign="center", valign="center")
    if FONT.exists():
        kw["fontPath"] = str(FONT)
    else:
        kw["kind"] = "bold"
    t = cq.Workplane("XY").text(txt, size, 1.0, **kw).val()

    def pts(w):
        out = []
        for e in w.Edges():
            k = max(2, int(e.Length() / 0.1) + 1)
            out += [e.positionAt(i / k).toTuple()[:2] for i in range(k)]
        return out

    polys = [Polygon(pts(f.outerWire()), [pts(h) for h in f.innerWires()]).buffer(0)
             for f in t.Faces() if f.normalAt().z < -0.99]
    r = P.SKIN_WALL_MIN / 2 + 0.02             # opening: whatever is thinner than pared_min (tapered tails) goes away
    return unary_union(polys).buffer(BOLD, quad_segs=4).buffer(-r, quad_segs=4).buffer(r, quad_segs=4).simplify(0.03)


def sparse(pts, step=0.15):
    """Drop ring points closer than step to the last kept one (and to the first): no edge below checks.MIN_EDGE."""
    out = [pts[0]]
    for x, y in pts[1:]:
        if math.hypot(x - out[-1][0], y - out[-1][1]) >= step:
            out.append((x, y))
    while len(out) > 3 and math.hypot(out[-1][0] - out[0][0], out[-1][1] - out[0][1]) < step:
        out.pop()
    return out


def _text(txt, size, h):
    from shapely.geometry import MultiPolygon
    g = _outline(txt, size)
    solids = []
    for poly in (g.geoms if isinstance(g, MultiPolygon) else [g]):
        ring = lambda c: cq.Wire.makePolygon([cq.Vector(x, y, -SINK) for x, y in sparse(list(c.coords)[:-1])], close=True)
        face = cq.Face.makeFromWires(ring(poly.exterior), [ring(i) for i in poly.interiors])
        solids.append(cq.Solid.extrudeLinear(face, cq.Vector(0, 0, h + SINK)))
    return cq.Compound.makeCompound(solids)


def stroke_loss(txt, size, wall):
    """Share of the letter area (%) thinner than wall: lost by a morphological opening of radius wall / 2."""
    g = _outline(txt, size)
    return 100 * (g.area - g.buffer(-wall / 2).buffer(wall / 2).area) / g.area


def fit_text(txt, size, room, h):
    """Raised text centred on the origin, sunk SINK below z = 0, shrunk only if it does not fit in room (mm), but never
    below CAP_MIN of cap height. Returns (solid, font size, cap height)."""
    t = _text(txt, size, h)
    w = t.BoundingBox().xlen
    if w > room:
        size *= room / w
        t = _text(txt, size, h)
    cap = _text(txt[0], size, h).BoundingBox().ylen - 2 * BOLD   # first letter is a capital (L, U); font height
    if cap < CAP_MIN:
        raise SystemExit(f"'{txt}' no cabe con {CAP_MIN} mm de alto de letra (queda {cap:.1f} mm en {room:.0f} mm)")
    return t, size, cap


def concha(L):
    z0, base = L["z0"], P.SKIN_BASE
    region = prism(L["outline"], TALL, z0, -P.SKIN_INSET)                 # never leaves the lid in plan
    inner = prism(L["outline"], TALL, z0 - 1, -(P.SKIN_INSET + P.SKIN_FRAME_W))
    rb = inner.BoundingBox()
    ix0, ix1, iy0, iy1 = rb.xmin, rb.xmax, rb.ymin, rb.ymax
    cl = P.SKIN_CLEAR
    hb = L["handle"][0]
    w, h_in, h_out = P.SKIN_RIB
    depth, lip_h = P.SKIN_WAVE
    pearl = None
    if L["logo"]:                # P4: the 0.4 mm logo on the lid stays in view inside an oval ring, the "pearl"
        x0, x1 = min(b.xmin for b in L["logo"]), max(b.xmax for b in L["logo"])
        y0, y1 = min(b.ymin for b in L["logo"]), max(b.ymax for b in L["logo"])
        pearl = [(x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2 + 4.0, (y1 - y0) / 2 + 3.0]

    parts = [prism(L["outline"], base, z0, -P.SKIN_INSET).cut(inner)]     # perimeter frame
    inner_lip = prism(L["outline"], lip_h, z0, -(P.SKIN_INSET + P.SKIN_FRAME_W))
    # scallop: hinge in front of the handle, fan towards -y
    n = P.SKIN_RIBS
    a0, a1 = math.radians(196), math.radians(344)
    R = max(8.0, (w + P.SKIN_WALL_MIN) / ((a1 - a0) / (n - 1)))         # umbo: ribs leave it with a full wall between them
    hx, hy = 0.0, hb.ymin - cl - R
    if pearl:                    # widen the pearl until no rib grazes it (a grazing cut leaves a sliver of rib)
        while graze(hx, hy, angles(a0, a1, n), pearl, w) < P.SKIN_WALL_MIN:
            pearl[2] += 1.0
    parts.append(cq.Solid.makeCylinder(R, h_in + 0.5, cq.Vector(hx, hy, z0)))     # proud of the ribs: no slivers
    # wavy lip, on the real (rounded) inner outline of the frame, not on its bounding box: a uniform band LIP_W wide
    # along the frame's inner face (front half only), plus one half-disc lobe between every two ribs, centred on the
    # band's inner edge so it meets it at 90 deg (no cusp, no sliver) and kept LIP_GAP clear of the rib sides
    edge = prism(L["outline"], 1, 0, -(P.SKIN_INSET + P.SKIN_FRAME_W + LIP_W)).Faces()
    edge = max((f for f in edge if f.normalAt().z < -0.99), key=lambda f: f.Area()).outerWire()
    ring = [edge.positionAt(i / 1440).toTuple()[:2] for i in range(1440)]

    def on_edge(th):
        """Point of the band's inner edge seen from the hinge at angle th (front half)."""
        def gap(q):
            return abs(math.remainder(math.atan2(q[1] - hy, q[0] - hx) - th, 2 * math.pi))
        return min((q for q in ring if q[1] < hy), key=gap)

    ths = angles(a0, a1, n)
    for th in ths:
        q = on_edge(th)
        d = math.hypot(q[0] - hx, q[1] - hy) + LIP_W + P.SKIN_FRAME_W / 2          # into the frame
        parts.append(rib(hx, hy, th, R - 1.0, d, z0, w, h_in, h_out))
    front = box(-300, 300, -300, hy, z0 - 1, TALL)
    parts.append(prism(L["outline"], lip_h, z0, -(P.SKIN_INSET + P.SKIN_FRAME_W + 0.0))
                 .cut(prism(L["outline"], TALL, z0 - 1, -(P.SKIN_INSET + P.SKIN_FRAME_W + LIP_W))).intersect(front))
    lobes = []
    for t0, t1 in zip(ths, ths[1:]):
        p0, p1, m = on_edge(t0), on_edge(t1), on_edge((t0 + t1) / 2)
        rho = min(0.5 * math.hypot(p1[0] - p0[0], p1[1] - p0[1]) - w / 2 - LIP_GAP, depth * 2.5)
        if rho >= P.SKIN_WALL_MIN:
            lobes.append(cq.Solid.makeCylinder(rho, lip_h, cq.Vector(m[0], m[1], z0)))
            parts.append(lobes[-1].intersect(inner_lip))
    # auricles (the two "ears" beside the hinge)
    for sx in (1, -1):
        parts.append(prism([(sx * (R - 4), hy + 0.4 * R), (sx * (R + 16), hy + 0.4 * R), (sx * (R + 12), hy - 3),
                            (sx * (R - 4), hy - 0.5 * R)], 3.0, z0))       # inner corners deep in the umbo: no sliver
    # back half, L-shaped plate: a band across the width behind the handle for "LanternGuard", and the block beside
    # the umbilical gland for "UPCH"
    t1, t2 = P.SKIN_TEXT
    by0 = hb.ymax + cl + 2.0
    gy = L["gland"][1] - P.SKIN_GLAND_R - cl if L["gland"] else iy1
    gx = L["gland"][0] + P.SKIN_GLAND_R + cl if L["gland"] else ix0
    by1 = min(gy, by0 + 20.0)
    band = box(ix0 - 2, ix1 + 2, by0, by1, z0, base)
    block = box(gx, ix1 + 2, by1 - 1, iy1 + 2, z0, base)
    parts.append(band.fuse(block).clean())
    txt1, s1, c1 = fit_text(t1, 16.0, (ix1 - ix0) - 10.0, P.SKIN_RELIEF)
    txt1 = txt1.moved(cq.Location(cq.Vector((ix0 + ix1) / 2, (by0 + by1) / 2, z0 + base)))
    if LOGO_SVG.exists():
        raise SystemExit(f"{LOGO_SVG.name} existe: falta importar el SVG en relieve (no estaba al construir skin.py)")
    txt2, s2, c2 = fit_text(t2, 14.0, (ix1 - gx) - 8.0, P.SKIN_RELIEF)      # "UPCH" smaller than "LanternGuard"
    txt2 = txt2.moved(cq.Location(cq.Vector((gx + ix1) / 2, (by1 + iy1) / 2, z0 + base)))
    skin = parts[0]
    for s in parts[1:]:
        skin = skin.fuse(s)
    # keep-outs: handle (lifting point), umbilical gland, P4 logo (then the pearl ring closes the ribs around it)
    cuts = [box(hb.xmin - cl, hb.xmax + cl, hb.ymin - cl, hb.ymax + cl, z0 - 1, TALL)]
    if L["gland"]:
        cuts.append(cq.Solid.makeCylinder(P.SKIN_GLAND_R, TALL, cq.Vector(L["gland"][0], L["gland"][1], z0 - 1)))
    if pearl:
        cuts.append(ellipse(*pearl, z0 - 1, TALL))
    for c in cuts:
        skin = skin.cut(c)
    if pearl:
        cx, cy, ea, eb = pearl
        skin = skin.fuse(ellipse(cx, cy, ea + 2.2, eb + 2.2, z0, lip_h).cut(ellipse(*pearl, z0 - 1, TALL)))
    skin = skin.fuse(txt1).fuse(txt2)
    for x, y in L["screws"]:
        skin = skin.cut(cq.Solid.makeCylinder(P.SKIN_SCREW_D / 2, TALL, cq.Vector(x, y, z0 - 1)))
    skin = skin.intersect(region).clean()
    return skin, dict(bisagra=(hx, hy), umbo_r=round(R, 1), costillas=n, perla_logo=pearl and [round(v, 1) for v in pearl],
                      roce_perla_mm=pearl and round(graze(hx, hy, angles(a0, a1, n), pearl, w), 2),
                      letra_mm=[round(s1, 1), round(s2, 1)], alto_mayuscula_mm=[round(c1, 1), round(c2, 1)],
                      fuente=FONT.name if FONT.exists() else "CadQuery bold")


def apparent(proto, skin_g, skin_cm3):
    """Apparent weight in sea water with the skin on, and the ballast that keeps lastre.objetivo_medio_kgf."""
    res = json.loads((MOD / "salida" / "prototipos" / proto / "resultados.json").read_text(encoding="utf-8"))
    bulk = P.BALLAST_BULK["opciones"][P.BALLAST_BULK["material"]]
    net = 1 - RHO_W / bulk["solido"]
    mid = P.BALLAST_MID_KGF * 1000
    lo, hi = (t * 1000 for t in P.BALLAST_TARGET_KGF)
    add = skin_g - RHO_W * skin_cm3
    out = {"skin_aparente_g": round(add, 1)}
    for case, w in res["peso"].items():
        app0 = w["sin_lastre_g"]
        g_now = w["lastre_g"]
        g_mid = (mid - app0 - add) / net
        g_new = max(0.0, round(g_mid / 10.0) * 10.0)
        out[case] = dict(aparente_antes_g=round(w["aparente_g"], 1), aparente_con_skin_g=round(w["aparente_g"] + add, 1),
                         lastre_actual_g=g_now, lastre_con_skin_g=g_new, cambia=g_new != g_now,
                         en_ventana=lo <= w["aparente_g"] + add <= hi)
    return out


def build(proto, theme=None):
    theme = theme or P.SKIN_THEME
    if theme != "concha":
        raise SystemExit(f"skin.tema = {theme}: por ahora solo 'concha' esta construido")
    parts = by_volume(proto)
    L = lid_data(parts)
    skin, info = concha(L)
    out = MOD / "salida" / "skin" / proto / theme
    out.mkdir(parents=True, exist_ok=True)
    step = out / f"SKIN_{theme}.step"
    asm = cq.Assembly(name=f"skin_{theme}_{proto}")
    asm.add(skin, name=f"SKIN_{theme}")
    asm.save(str(step), exportType="STEP")
    fix_step_stamp(step)
    flat = skin.moved(cq.Location(cq.Vector(0, 0, -L["z0"])))           # base on the bed, relief up
    stl = out / f"SKIN_{theme}.stl"
    cq.exporters.export(cq.Workplane().add(flat), str(stl), tolerance=0.02, angularTolerance=0.1)
    chk = brep_check(skin)
    p_wall, min_wall = min_thickness(str(stl))
    bb = skin.BoundingBox()
    ob = prism(L["outline"], 1, L["z0"]).BoundingBox()
    vol = skin.Volume() / 1000
    clash = {}
    for k, v in parts.items():                                         # only parts whose box reaches the skin's box
        vb = v.BoundingBox()
        if vb.zmax < bb.zmin or vb.zmin > bb.zmax or vb.xmax < bb.xmin or vb.xmin > bb.xmax or vb.ymax < bb.ymin or vb.ymin > bb.ymax:
            continue
        iv = skin.intersect(v).Volume()
        if iv > 1e-3:
            clash[k] = round(iv, 2)
    rep = dict(prototipo=proto, tema=theme, volumen_cm3=round(vol, 2), masa_100_g=round(vol * P.PETG_DENSITY, 1),
               solidos=len(skin.Solids()), brep_ok=chk["ok"], brep=chk, pared_p1_mm=round(p_wall, 2), pared_min_mm=round(min_wall, 2), pared_ok=p_wall >= P.SKIN_WALL_MIN,
               bbox_mm=[round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)],
               dentro_de_la_tapa=bb.xmin >= ob.xmin - 1e-6 and bb.xmax <= ob.xmax + 1e-6 and bb.ymin >= ob.ymin - 1e-6 and bb.ymax <= ob.ymax + 1e-6,
               margen_a_la_tapa_mm=round(min(bb.xmin - ob.xmin, ob.xmax - bb.xmax, bb.ymin - ob.ymin, ob.ymax - bb.ymax), 2),
               z_cambio_color_mm=P.SKIN_BASE, interferencias_mm3=clash, tornillos=len(L["screws"]), umbilical=L["gland"], **info)
    (out / "skin.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(proto, theme, json.dumps({k: rep[k] for k in ("volumen_cm3", "masa_100_g", "solidos", "brep_ok", "brep", "pared_p1_mm", "pared_min_mm", "interferencias_mm3", "alto_mayuscula_mm",
                                                        "bbox_mm", "dentro_de_la_tapa", "margen_a_la_tapa_mm", "tornillos")}))
    return skin, L, rep, out


if __name__ == "__main__":
    for pr in sys.argv[1:] or ["P4_estetico", "P2_robusto"]:
        build(pr)
