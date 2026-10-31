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
    if umb is not None:
        foot = umb.intersect(cq.Solid.makeBox(600, 600, 4, cq.Vector(-300, -300, z0 - 0.5)))
        if foot.Volume() > 1:
            c = foot.Center()
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


def fit_text(txt, size, room, h):
    """Raised bold text centred on the origin, base on z = 0, shrunk only if it does not fit in room (mm)."""
    t = cq.Workplane("XY").text(txt, size, h, combine=False, halign="center", valign="center", kind="bold").val()
    w = t.BoundingBox().xlen
    if w > room:
        size *= room / w
        t = cq.Workplane("XY").text(txt, size, h, combine=False, halign="center", valign="center", kind="bold").val()
    return t, size


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
    # scallop: hinge in front of the handle, fan towards -y
    n = P.SKIN_RIBS
    a0, a1 = math.radians(196), math.radians(344)
    R = max(8.0, (w + P.SKIN_WALL_MIN) / ((a1 - a0) / (n - 1)))         # umbo: ribs leave it with a full wall between them
    hx, hy = 0.0, hb.ymin - cl - R
    if pearl:                    # widen the pearl until no rib grazes it (a grazing cut leaves a sliver of rib)
        while graze(hx, hy, angles(a0, a1, n), pearl, w) < P.SKIN_WALL_MIN:
            pearl[2] += 1.0
    parts.append(cq.Solid.makeCylinder(R, h_in + 0.5, cq.Vector(hx, hy, z0)))     # proud of the ribs: no slivers
    for th in angles(a0, a1, n):
        d = ray_to_rect(hx, hy, th, ix0, ix1, iy0, iy1)
        parts.append(rib(hx, hy, th, R - 1.0, d + 1.5, z0, w, h_in, h_out))
    # wavy lip: band between a smooth wave (spline, lobes reaching out at every rib) and the frame's inner face, so it
    # shares that face with the frame instead of crossing it
    e = 0.12
    b0, b1 = a0 - e, a1 + e
    wave = []
    for i in range(121):
        th = b0 + (b1 - b0) * i / 120
        d = ray_to_rect(hx, hy, th, ix0, ix1, iy0, iy1)
        k = (th - a0) / ((a1 - a0) / (n - 1))                             # 0 at a rib, 0.5 between ribs
        r = d - depth * (0.5 - 0.5 * math.cos(2 * math.pi * k)) - 2.2
        wave.append(cq.Vector(hx + r * math.cos(th), hy + r * math.sin(th), 0))
    edges = [cq.Edge.makeSpline(wave), cq.Edge.makeLine(wave[-1], cq.Vector(hx, hy, 0)),
             cq.Edge.makeLine(cq.Vector(hx, hy, 0), wave[0])]
    inside = cq.Solid.extrudeLinear(cq.Face.makeFromWires(cq.Wire.assembleEdges(edges)), cq.Vector(0, 0, TALL))         .moved(cq.Location(cq.Vector(0, 0, z0 - 1)))
    far = 400.0
    sector = prism([(hx, hy), (hx + far * math.cos(b0), hy + far * math.sin(b0)), (-far, -far), (far, -far),
                    (hx + far * math.cos(b1), hy + far * math.sin(b1))], lip_h, z0)
    parts.append(prism(L["outline"], lip_h, z0, -(P.SKIN_INSET + P.SKIN_FRAME_W)).intersect(sector).cut(inside))
    # auricles (the two "ears" beside the hinge)
    for sx in (1, -1):
        parts.append(prism([(sx * (R - 2), hy + 0.4 * R), (sx * (R + 16), hy + 0.4 * R), (sx * (R + 12), hy - 3),
                            (sx * (R - 2), hy - 0.5 * R)], 3.0, z0))
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
    txt1, s1 = fit_text(t1, 16.0, (ix1 - ix0) - 10.0, P.SKIN_RELIEF)
    txt1 = txt1.moved(cq.Location(cq.Vector((ix0 + ix1) / 2, (by0 + by1) / 2, z0 + base)))
    if LOGO_SVG.exists():
        raise SystemExit(f"{LOGO_SVG.name} existe: falta importar el SVG en relieve (no estaba al construir skin.py)")
    txt2, s2 = fit_text(t2, 20.0, (ix1 - gx) - 8.0, P.SKIN_RELIEF)
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
                      letra_mm=[round(s1, 1), round(s2, 1)])


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
    clash = {k: round(skin.intersect(v).Volume(), 2) for k, v in parts.items()
             if v.BoundingBox().zmax > L["z0"] - 1 and skin.intersect(v).Volume() > 1e-3}
    rep = dict(prototipo=proto, tema=theme, volumen_cm3=round(vol, 2), masa_100_g=round(vol * P.PETG_DENSITY, 1),
               solidos=len(skin.Solids()), brep_ok=chk["ok"], pared_p1_mm=round(p_wall, 2), pared_min_mm=round(min_wall, 2),
               bbox_mm=[round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)],
               dentro_de_la_tapa=bb.xmin >= ob.xmin - 1e-6 and bb.xmax <= ob.xmax + 1e-6 and bb.ymin >= ob.ymin - 1e-6 and bb.ymax <= ob.ymax + 1e-6,
               margen_a_la_tapa_mm=round(min(bb.xmin - ob.xmin, ob.xmax - bb.xmax, bb.ymin - ob.ymin, ob.ymax - bb.ymax), 2),
               z_cambio_color_mm=P.SKIN_BASE, interferencias_mm3=clash, tornillos=len(L["screws"]), umbilical=L["gland"], **info)
    (out / "skin.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    print(proto, theme, json.dumps({k: rep[k] for k in ("volumen_cm3", "masa_100_g", "solidos", "brep_ok", "pared_p1_mm",
                                                        "bbox_mm", "dentro_de_la_tapa", "margen_a_la_tapa_mm", "tornillos")}))
    return skin, L, rep, out


if __name__ == "__main__":
    for pr in sys.argv[1:] or ["P4_estetico", "P2_robusto"]:
        build(pr)
