"""Ground LoRa station: T1_caja (body, printed with the floor on the bed) and T2_tapa (lid, printed inner face on the bed).

    python tierra.py              salida/tierra/ (STEP, STL, tierra.json)
    python tierra.py --ensamble   salida/tierra/step/00_ENSAMBLE_tierra.step, closed + exploded, with the collision check

Layout: Heltec and battery side by side on the floor, Heltec on 4 M2.5 posts with the USB-C end against the -X wall, SMA
bulkhead in the +X wall at the Heltec side. Mount it USB-C down: the plugged port then points away from the rain.
Sealed by a 2 mm NBR cord in a groove on the rim, closed by 4 M3 A4 screws into heat-set inserts in corner towers.
No supports: the rim and the towers rise from the walls at 45 degrees, the horizontal holes are small or end in a roof.
"""
import json
import math
from pathlib import Path

import cadquery as cq
import numpy as np
import trimesh

import params as P

OUT = Path(__file__).resolve().parent.parent / "salida" / "tierra"
T, C = P.TIERRA, P.TIERRA_CAJA
HL, HW = T["heltec"]
BL, BW, BH = T["bateria"]
GAP, WALL, FLOOR, H_IN = C["holgura"], C["pared"], C["fondo"], C["alto_int"]
L_IN = GAP + max(HL, BL) + GAP + T["sma_zona"]        # the SMA nut and pigtail take their own space at +X
POST_FOOT = C["poste_d"] / 2 + 1.5
POST_EXTRA = T["heltec_agujeros"][1] / 2 + POST_FOOT - HW / 2     # how far the foot of a post passes the edge of the board
W_IN = GAP + HW + POST_EXTRA + GAP + BW + GAP
H_T1 = FLOOR + H_IN
RIM = C["ranura_pared"] + P.GROOVE_WIDTH + C["reborde"]       # cavity edge to outer edge of the rim
OUT_RIM = RIM - WALL                                           # how far the rim stands out of the wall
HX0, HY0 = -L_IN / 2 + GAP, -W_IN / 2 + GAP                   # corner of the Heltec board
PCB_Z = FLOOR + T["heltec_poste"]
USB_Z = PCB_Z + T["heltec_pcb"] + T["usb_z"]
HOLES = [(HX0 + HL / 2 + sx * T["heltec_agujeros"][0] / 2, HY0 + HW / 2 + sy * T["heltec_agujeros"][1] / 2) for sx in (-1, 1) for sy in (-1, 1)]
TOWER_R = C["torre_d"] / 2
TX, TY = L_IN / 2 + RIM - 2, W_IN / 2 + RIM - 2    # screw axes: the towers overlap the rounded corner of the rim
SCREWS = [(sx * TX, sy * TY) for sx in (-1, 1) for sy in (-1, 1)]
WALL_MIN = 2.4                                      # encargo 05/11
RC = 6.0                                            # cavity corner radius
SMA_Z = FLOOR + 7.0                                 # the Ø12 outer face of the SMA stays under the 45 degree rim, which starts at z = 16.1


def rbox(lx, ly, h, r, z=0.0):
    return cq.Workplane("XY").workplane(offset=z).rect(lx, ly).extrude(h).edges("|Z").fillet(r)


def foot(shape):
    """0.5 mm chamfer on the bed edges of a simple prism, against the elephant foot."""
    return shape.faces("<Z").edges().chamfer(0.5)


def t1():
    h = H_T1
    body = foot(rbox(L_IN + 2 * WALL, W_IN + 2 * WALL, h, RC + WALL))
    # rim: rises from the wall at 45 degrees, so it needs no support. Under the groove there stays the minimum wall.
    z_gland = h - P.GROOVE_DEPTH - WALL_MIN
    z0 = z_gland - OUT_RIM
    body = body.union(rbox(L_IN + 2 * RIM, W_IN + 2 * RIM, h - z_gland, RC + RIM, z_gland))
    body = body.union(cq.Workplane("XY").workplane(offset=z0).sketch().rect(L_IN + 2 * WALL, W_IN + 2 * WALL).vertices().fillet(RC + WALL)
                      .finalize().extrude(OUT_RIM, taper=-45))
    # screw towers: prism of the tower cut by a 45 degree cone that starts on the rounded corner of the wall, so the
    # support grows out of the wall and no layer starts in the air
    z_tower = h - 10.0
    for x, y in SCREWS:
        cx, cy = math.copysign(L_IN / 2 - RC, x), math.copysign(W_IN / 2 - RC, y)
        r_wall = RC + WALL - 0.2
        reach = math.hypot(x - cx, y - cy) + TOWER_R - r_wall
        zs = max(z_tower - reach, 0.0)
        cone = cq.Workplane().add(cq.Solid.makeCone(r_wall, r_wall + reach + 1, reach + 1, cq.Vector(cx, cy, zs), cq.Vector(0, 0, 1)))
        prism = cq.Workplane("XY").workplane(offset=zs).center(x, y).circle(TOWER_R).extrude(h - zs)
        solid_top = cq.Workplane("XY").workplane(offset=z_tower).center(x, y).circle(TOWER_R).extrude(h - z_tower)
        body = body.union(prism.intersect(cone)).union(solid_top)
    # mounting tabs flush with the floor, with a slot each and a gusset
    tl, tw, tt = C["pestana"]
    d_ojal, l_ojal = C["ojal"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (L_IN / 2 - tl / 2 - 2), sy * (W_IN / 2 + WALL + tw / 2 - 1)
            tab = foot(cq.Workplane("XY").box(tl, tw + 2, tt, centered=(True, True, False)).translate((x, y, 0)).edges("|Z").fillet(2.5))
            yg = sy * (W_IN / 2 + WALL)
            gusset = cq.Workplane("YZ").workplane(offset=x - 3).polyline([(yg - sy, tt), (yg + sy * 6, tt), (yg - sy, tt + 7)]).close().extrude(6)
            slot = cq.Workplane("XY").center(x, y + sy * 2).slot2D(l_ojal, d_ojal, 90).extrude(tt + 1)
            body = body.union(tab).union(gusset).cut(slot)
    # pad of the USB port at -X: 45 degree underside, reaches the rim
    pw, ph = C["usb"]
    tw_, th_, td_ = C["tapon"]
    uy = HY0 + HW / 2
    uz0 = USB_Z - ph / 2
    x_out = -(L_IN / 2 + WALL)
    z_s = USB_Z - th_ / 2 - 2 - td_
    if z_s < 0:
        raise SystemExit("el pad del USB no cabe sobre la base")
    pad = (cq.Workplane("XZ").workplane(offset=-(uy + (tw_ + 8) / 2))
           .polyline([(x_out + 0.2, z_s), (x_out - td_, z_s + td_ + 0.2), (x_out - td_, z_gland), (x_out + 0.2, z_gland)]).close().extrude(tw_ + 8))
    body = body.union(pad)
    # cavity and gland: 2 mm cord in the groove of junta.*
    body = body.cut(rbox(L_IN, W_IN, h, RC, FLOOR))
    go = C["ranura_pared"]
    groove = rbox(L_IN + 2 * (go + P.GROOVE_WIDTH), W_IN + 2 * (go + P.GROOVE_WIDTH), P.GROOVE_DEPTH + 1, RC + go + P.GROOVE_WIDTH, h - P.GROOVE_DEPTH)
    groove = groove.cut(rbox(L_IN + 2 * go, W_IN + 2 * go, P.GROOVE_DEPTH + 2, RC + go, h - P.GROOVE_DEPTH - 0.5))
    body = body.cut(groove)
    # USB-C, PRG and RST through one port (short bridge over it); the silicone plug seats in the recess of the pad
    body = body.cut(cq.Workplane("YZ").workplane(offset=x_out - td_ - 1).center(uy, USB_Z).rect(pw, ph).extrude(td_ + WALL + 2))
    body = body.cut(cq.Workplane("YZ").workplane(offset=x_out - td_ - 0.01).center(uy, USB_Z).rect(tw_, th_).extrude(td_ + 0.01))
    # SMA bulkhead at +X: round hole in the plain wall, whose outer face seats its washer
    body = body.cut(cq.Workplane("YZ").workplane(offset=L_IN / 2 - 1).center(uy, SMA_Z).circle(T["sma_d"] / 2).extrude(WALL + 2))
    # posts for the Heltec: M2.5 heat-set inserts, 45 degree foot
    ins_d, ins_h = C["inserto_m25"]
    for x, y in HOLES:
        post = cq.Workplane("XY").workplane(offset=FLOOR - 0.01).center(x, y).circle(C["poste_d"] / 2).extrude(T["heltec_poste"] + 0.01)
        cone = cq.Workplane().add(cq.Solid.makeCone(C["poste_d"] / 2 + 1.5, C["poste_d"] / 2, 1.5, cq.Vector(x, y, FLOOR - 0.01), cq.Vector(0, 0, 1)))
        body = body.union(post).union(cone).cut(cq.Workplane("XY").workplane(offset=PCB_Z - ins_h).center(x, y).circle(ins_d / 2).extrude(ins_h + 0.5))
    # M3 heat-set inserts in the towers
    for x, y in SCREWS:
        body = body.cut(cq.Workplane("XY").workplane(offset=h - P.M3_INSERT_DEPTH).center(x, y).circle(P.M3_INSERT_HOLE / 2).extrude(P.M3_INSERT_DEPTH + 0.5))
    return body


def t2():
    th = C["tapa"]
    plate = foot(rbox(L_IN + 2 * RIM, W_IN + 2 * RIM, th, RC + RIM))
    plate = plate.faces(">Z").edges().chamfer(1.0)
    for x, y in SCREWS:
        boss = cq.Workplane("XY").center(x, y).circle(TOWER_R).extrude(th).faces(">Z").edges().chamfer(1.0).faces("<Z").edges().chamfer(0.5)
        plate = plate.union(boss)
    ow, oh = T["oled"]
    ox, oy = HX0 + T["oled_x"], HY0 + HW / 2
    margin, depth = C["ventana_rebaje"]
    plate = plate.cut(cq.Workplane("XY").center(ox, oy).rect(ow, oh).extrude(th + 1))
    plate = plate.cut(cq.Workplane("XY").workplane(offset=th - depth).center(ox, oy).rect(ow + margin, oh + margin).extrude(depth + 1))
    for x, y in SCREWS:
        plate = plate.cut(cq.Workplane("XY").center(x, y).circle(P.M3_CLEAR / 2).extrude(th + 1))
    return plate


def overhang(stl):
    """Area of faces looking more than 45 degrees downward (mm2), away from the bed plane."""
    m = trimesh.load(stl)
    z0 = m.bounds[0, 2]
    down = (m.face_normals[:, 2] < -math.sqrt(0.5)) & (m.triangles_center[:, 2] > z0 + 0.5)
    return round(float(m.area_faces[down].sum()), 1), round(float(m.area), 1), down, m


def export(shape, stem):
    (OUT / "step").mkdir(parents=True, exist_ok=True)
    (OUT / "stl").mkdir(parents=True, exist_ok=True)
    cq.exporters.export(shape, str(OUT / "step" / f"{stem}.step"))
    stl = OUT / "stl" / f"{stem}.stl"
    cq.exporters.export(shape, str(stl), tolerance=0.05, angularTolerance=0.1)
    v = shape.val()
    bb = v.BoundingBox()
    area, total, down, m = overhang(stl)
    out = dict(volumen_cm3=round(v.Volume() / 1000, 2), gramos=round(v.Volume() / 1000 * P.PETG_DENSITY, 1), caja_mm=[round(bb.xlen, 1), round(bb.ylen, 1), round(bb.zlen, 1)],
               valido=bool(v.isValid()), solidos=len(shape.solids().vals()), voladizo_mm2=area, area_mm2=total, watertight=bool(m.is_watertight))
    if area:
        c = m.triangles_center[down]
        out["voladizo_z"] = [round(float(c[:, 2].min()), 1), round(float(c[:, 2].max()), 1)]
    return out


def checks(t1_shape):
    """Components as boxes against T1: no collision, and the clearance to the walls and to each other."""
    bx0 = -L_IN / 2 + GAP
    by0 = HY0 + HW + POST_EXTRA + GAP
    box = lambda x0, y0, z0, lx, ly, lz: cq.Workplane("XY").box(lx, ly, lz, centered=False).translate((x0, y0, z0))
    heltec = box(HX0, HY0, PCB_Z, HL, HW, T["heltec_pcb"] + T["heltec_sobre_pcb"])
    bat = box(bx0, by0, FLOOR, BL, BW, BH)
    def vol(a, b):
        try:
            return round(a.intersect(b).val().Volume(), 3)
        except ValueError:
            return 0.0
    bo = bat.val().BoundingBox()
    he = heltec.val().BoundingBox()
    out = dict(choque_heltec=vol(heltec, t1_shape), choque_bateria=vol(bat, t1_shape), choque_entre_ellos=vol(heltec, bat),
               holgura_bateria_paredes=[round(bo.xmin + L_IN / 2, 2), round(L_IN / 2 - bo.xmax, 2), round(W_IN / 2 - bo.ymax, 2)],
               holgura_bateria_techo=round(H_T1 - bo.zmax, 2), holgura_heltec_techo=round(H_T1 - he.zmax, 2),
               holgura_heltec_paredes=[round(he.xmin + L_IN / 2, 2), round(L_IN / 2 - he.xmax, 2), round(he.ymin + W_IN / 2, 2)],
               holgura_pie_poste_bateria=round(by0 - max(y + POST_FOOT for _, y in HOLES), 2),
               usb_z=round(USB_Z, 2), ventana_centro=[round(HX0 + T["oled_x"], 2), round(HY0 + HW / 2, 2)])
    m = trimesh.load(OUT / "stl" / "T1_caja.stl")
    z0 = m.bounds[0, 2]
    down = (m.face_normals[:, 2] < -math.sqrt(0.5) - 1e-3) & (m.triangles_center[:, 2] > z0 + 0.5)
    bins = {}
    for z, a in zip(np.round(m.triangles_center[down, 2], 0), m.area_faces[down]):
        bins[float(z)] = round(bins.get(float(z), 0.0) + float(a), 1)
    out["voladizo_por_z"] = dict(sorted(bins.items()))
    return out


# references of the assembly: dimensions of tierra.medidas. Generic hardware, simplified: boxes and cylinders, not catalogue parts.
SCREW_L, HEAD_D, HEAD_H = 10.0, 5.5, 3.0            # M3 x 10 DIN 912
INSERT_L, THREAD_D = 5.7, 3.0                        # heat-set insert M3 x 5.7, bore simplified to the nominal thread
SMA_BARREL, SMA_NUT, SMA_INNER, SMA_OUTER, SMA_T = 6.4, 10.0, 5.0, 5.0, 2.0
CORD_W = 2.1                                         # closed, the cord is compressed to the groove depth: same area as the 2 mm circle
EXPLODE_Z, EXPLODE_X = 40.0, 200.0


def _cyl(x, y, z, d, h):
    return cq.Workplane("XY").workplane(offset=z).center(x, y).circle(d / 2).extrude(h)


def references():
    """Closed position. The cord is shown compressed; everything else is at its nominal size."""
    th = C["tapa"]
    box = lambda x0, y0, z0, lx, ly, lz: cq.Workplane("XY").box(lx, ly, lz, centered=False).translate((x0, y0, z0))  # noqa: E731
    by0 = HY0 + HW + POST_EXTRA + GAP
    uy, sma_z = HY0 + HW / 2, SMA_Z
    ow, oh = T["oled"]
    margin, depth = C["ventana_rebaje"]
    ox, oy = HX0 + T["oled_x"], HY0 + HW / 2
    wx = L_IN / 2
    axis = lambda x0, d, l: cq.Workplane("YZ").workplane(offset=x0).center(uy, sma_z).circle(d / 2).extrude(l)  # noqa: E731
    sma = axis(wx - SMA_INNER, SMA_BARREL, SMA_INNER + WALL + SMA_OUTER).union(axis(wx - SMA_T, SMA_NUT, SMA_T)).union(axis(wx + WALL, T["sma_cara"], SMA_T))
    go = C["ranura_pared"] + P.GROOVE_WIDTH / 2
    z_cord = H_T1 - P.GROOVE_DEPTH
    cord = rbox(L_IN + 2 * go + CORD_W, W_IN + 2 * go + CORD_W, P.GROOVE_DEPTH, RC + go + CORD_W / 2, z_cord).cut(
        rbox(L_IN + 2 * go - CORD_W, W_IN + 2 * go - CORD_W, P.GROOVE_DEPTH + 1, RC + go - CORD_W / 2, z_cord - 0.5))
    out = dict(REF_Heltec=box(HX0, HY0, PCB_Z, HL, HW, T["heltec_pcb"] + T["heltec_sobre_pcb"]),
               REF_bateria=box(-L_IN / 2 + GAP, by0, FLOOR, BL, BW, BH),
               REF_SMA=sma,
               REF_acrilico_OLED=box(ox - (ow + margin) / 2, oy - (oh + margin) / 2, H_T1 + th - depth, ow + margin, oh + margin, 2.0),
               REF_cordon_NBR=cord)
    for k, (x, y) in enumerate(SCREWS, 1):
        out[f"REF_tornillo_M3_{k}"] = _cyl(x, y, H_T1 + th - SCREW_L, THREAD_D, SCREW_L).union(_cyl(x, y, H_T1 + th, HEAD_D, HEAD_H))
        out[f"REF_inserto_M3_{k}"] = _cyl(x, y, H_T1 - INSERT_L, P.M3_INSERT_HOLE, INSERT_L).cut(_cyl(x, y, H_T1 - INSERT_L - 1, THREAD_D, INSERT_L + 2))
    return out


LID_GROUP = ("T2_tapa", "REF_acrilico_OLED", "REF_tornillo")


def assembly():
    """Closed station at the origin and, beside it, the exploded copy (EXP_*): the lid group raised EXPLODE_Z mm."""
    import itertools
    closed = dict(T1_caja=t1(), T2_tapa=t2().translate((0, 0, H_T1)), **references())
    hits = {}
    for (a, sa), (b, sb) in itertools.combinations(closed.items(), 2):
        ba, bb = sa.val().BoundingBox(), sb.val().BoundingBox()
        if ba.xmax < bb.xmin or bb.xmax < ba.xmin or ba.ymax < bb.ymin or bb.ymax < ba.ymin or ba.zmax < bb.zmin or bb.zmax < ba.zmin:
            continue
        try:
            v = sa.intersect(sb).val().Volume()
        except ValueError:
            v = 0.0
        if v > P.INTERF_TOL:
            hits[f"{a} / {b}"] = round(v, 3)
    bad = {k: len(v.solids().vals()) for k, v in closed.items() if len(v.solids().vals()) != 1 or not v.val().isValid()}
    asm = cq.Assembly(name="LG_tierra")
    for k, v in closed.items():
        asm.add(v, name=k)
    for k, v in closed.items():
        dz = EXPLODE_Z if k.startswith(LID_GROUP) else 0.0
        asm.add(v.translate((EXPLODE_X, 0, dz)), name=f"EXP_{k}")
    path = OUT / "step" / "00_ENSAMBLE_tierra.step"
    asm.export(str(path))
    back = cq.importers.importStep(str(path)).solids().vals()
    res = dict(piezas=list(closed), solidos_esperados=2 * len(closed), solidos_step=len(back), choques_mm3=hits, no_validos=bad,
               T1_cm3=round(closed["T1_caja"].val().Volume() / 1000, 2), T2_cm3=round(closed["T2_tapa"].val().Volume() / 1000, 2))
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return res


def main():
    import sys
    if "--ensamble" in sys.argv:
        res = assembly()
        (OUT / "ensamble.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
        return
    body = t1()
    res = dict(interior=[round(L_IN, 2), round(W_IN, 2), H_IN], reborde=RIM, tornillos_paso=[round(2 * TX, 1), round(2 * TY, 1)], T1_caja=export(body, "T1_caja"), T2_tapa=export(t2(), "T2_tapa"))
    res["comprobaciones"] = checks(body)
    go = C["ranura_pared"] + P.GROOVE_WIDTH / 2
    res["cordon_mm"] = round(2 * (L_IN + W_IN + 4 * go) - 8 * (RC + go) + 2 * math.pi * (RC + go), 0)
    res["compresion_junta_pct"] = round((P.ORING_CORD - P.GROOVE_DEPTH) / P.ORING_CORD * 100, 1)
    res["gramos_total"] = round(res["T1_caja"]["gramos"] + res["T2_tapa"]["gramos"], 1)
    (OUT / "tierra.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
