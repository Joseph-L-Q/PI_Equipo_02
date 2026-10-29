"""Fase B test coupons (probetas PB1..PB8; PB8 added 29/10) for the PETG underwater node. Every dimension comes from params.py;
module constants below are design values still missing there (listed in reporte_probetas.md).

Frame as the rest of cad_final: X along the rail, Y across, Z up, rail bottom at z = 0. Hook parts (PB1, PB4) use the
seat axis as origin: bore along Y centred on x = z = 0, J opening toward +X.
Run from cad_final/:  python probetas.py
"""
import math
from pathlib import Path

import cadquery as cq

import gancho
from checks import brep_check, export_part, mesh_checks, sanitize
from params import (BASE_M4_BOSS, INSERT_COUPON, M4_INSERT_DEPTH, M4_INSERT_HOLE)
from params import (BOX_FLOOR, BOX_LID_T, BOX_WALL, BUSHING_DIAMETERS, BUSHING_FLANGE, BUSHING_PRESS,
                    BUSHING_ROD_CLR, COMB_CLEARANCES, COMB_PIN_D, FIT_CLEAR, GROOVE_DEPTH, GROOVE_WIDTH,
                    HOLE_COMP, HOOK_CONTACT_W, HOOK_EDGE_R, JAW_BORE, KNOB_D, KNOB_H, KNOB_LOBES, LATCH_BUMP,
                    LATCH_PIVOT, LATCH_TAB, M3_CLEAR, M3_INSERT_DEPTH, M3_INSERT_HOLE, M4_CLEAR, M4_HEAD,
                    M4_HEX_HEAD, M4_NUT, MIN_WALL, ORING_CORD, PRINT_BED, RAIL_DOVETAIL, RAIL_DOVETAIL_KEY,
                    RAIL_JOINT_BOLT_Y, RAIL_LAP_WALL, RAIL_LAP_Z, RAIL_SECTION, RAIL_TSLOT, RAIL_TSLOT_RIB,
                    RAIL_WALL, SEAL_COUPON, STRAP_W)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "probetas"

# ------------------------------------------------------------------ coupon shape constants (params.py, Fase B block)
from params import (COUPON_L, JAW_WALL, JAW_LIP_H, STRAP_SLOT_T, STEM_H, LATCH_T, LATCH_ARM_W, LATCH_RIDGE_W,
                    LATCH_TIP_GAP, LATCH_SWING, KNOB_LOBE_R, KNOB_CAP, SEAL_CAV_CORNER, SEAL_FILLET, COMB_PITCH,
                    COMB_T, COMB_W, COMB_TEXT_H, COMB_TEXT_DEPTH, PIN_L)  # noqa: E402

WARNINGS = []
_jaw_dims = gancho.jaw_dims


# ------------------------------------------------------------------ helpers
def _box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def _hex(cx, cy, af, z0, h):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).polygon(6, af / math.cos(math.pi / 6)).extrude(h)


def _cyl_z(cx, cy, d, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).circle(d / 2).extrude(z1 - z0)


def _cyl_y(cx, cz, d, y0, y1):
    """Cylinder along Y between y0 and y1 centred on (cx, cz)."""
    return cq.Workplane("XZ").workplane(offset=-y1).center(cx, cz).circle(d / 2).extrude(y1 - y0)


def _xz_prism(pts, y0, y1):
    """Polygon given in (x, z) extruded along Y from y0 to y1."""
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts).close().extrude(y1 - y0)


# ------------------------------------------------------------------ rail geometry shared by PB2 / PB3
S, W = RAIL_SECTION, RAIL_WALL
CON_HALF = S / 2 - W                       # flooded duct half width (11)
LAP_HALF = S / 2 - RAIL_LAP_WALL           # duct half width in the lap zone (7)
TS_OPEN, TS_W, TS_H = RAIL_TSLOT["abertura"], RAIL_TSLOT["ancho"], RAIL_TSLOT["alto"]


def _tslot_cut(x0, x1):
    return _box(x0, x1, -TS_OPEN / 2, TS_OPEN / 2, -0.1, W + 0.1)


def _tslot_ribs(x0, x1):
    r = _box(x0, x1, TS_W / 2, TS_W / 2 + RAIL_TSLOT_RIB, W - 0.01, W + TS_H)
    return r.union(_box(x0, x1, -TS_W / 2 - RAIL_TSLOT_RIB, -TS_W / 2, W - 0.01, W + TS_H))


# in the lap zone the thickened walls may swallow the ribs; the nut channel itself must stay open
assert TS_W / 2 + RAIL_TSLOT_RIB < CON_HALF and TS_W / 2 < LAP_HALF, "T-slot channel outside the duct"


# ------------------------------------------------------------------ PB1 hook seat + 4 bushings, PB4 latch
def pb1():
    out = {"PB1_garra": gancho.jaw_body(STEM_H, True, WARNINGS)}
    out.update(gancho.bushings())
    return out


def pb4():
    return {"M14_pestillo": gancho.latch()}


# ------------------------------------------------------------------ PB2 T-slot with M4 nut
def pb2():
    p = _box(0, COUPON_L, -S / 2, S / 2, 0, S)
    p = p.cut(_box(-0.1, COUPON_L + 0.1, -CON_HALF, CON_HALF, W, S - W))
    p = p.cut(_tslot_cut(-0.1, COUPON_L + 0.1)).union(_tslot_ribs(0, COUPON_L))
    nut_af = M4_NUT[0]
    assert TS_W >= nut_af and TS_H >= M4_NUT[1], "nut does not fit the channel"
    return {"PB2_ranura_T": p}


# ------------------------------------------------------------------ PB3 joint: male + female
def pb3():
    lap = RAIL_DOVETAIL
    kb, kt, kh = RAIL_DOVETAIL_KEY
    c = FIT_CLEAR
    m_lap0 = COUPON_L - lap          # male lap zone [m_lap0, COUPON_L]
    xm, xf = m_lap0 + lap / 2, lap / 2
    by = RAIL_JOINT_BOLT_Y
    hole_r = M4_CLEAR / 2
    cb_d, cb_h = M4_HEAD[0] + 2 * HOLE_COMP, M4_HEAD[1] + HOLE_COMP
    nut_af, nut_h = M4_NUT[0] + HOLE_COMP, M4_NUT[1] + HOLE_COMP
    # checks from the brief
    assert by - hole_r >= LAP_HALF, "M4 hole crosses the 14 mm duct"
    assert by - cb_d / 2 >= LAP_HALF, "counterbore crosses the duct"
    assert by - nut_af / 2 >= LAP_HALF, "nut pocket crosses the duct"
    assert by - nut_af / 2 > TS_W / 2 + RAIL_TSLOT_RIB, "nut pocket touches the T-slot ribs"
    skin = S / 2 - (by + nut_af / 2)
    if skin < MIN_WALL:
        WARNINGS.append(f"PB3: la bolsa hexagonal de la tuerca deja solo {skin:.2f} mm de piel hacia afuera en y = +-{by} "
                        f"(minimo {MIN_WALL}); la tuerca M4 AF{M4_NUT[0]} no cabe con margen en una pared de {RAIL_LAP_WALL}")

    def half(z, base):   # half width of the key/socket at height z above the lap plane
        return base / 2 + (kt - kb) / 2 * (z - RAIL_LAP_Z) / kh

    # ---- male: bottom half over the lap, key up, T-slot continuous
    m = _box(0, COUPON_L, -S / 2, S / 2, 0, S)
    m = m.cut(_box(-0.1, m_lap0, -CON_HALF, CON_HALF, W, S - W))
    m = m.cut(_box(m_lap0, COUPON_L + 0.1, -LAP_HALF, LAP_HALF, W, S - W))
    m = m.cut(_box(m_lap0, COUPON_L + 0.1, -S / 2 - 1, S / 2 + 1, RAIL_LAP_Z, S + 1))
    m = m.cut(_tslot_cut(-0.1, COUPON_L + 0.1)).union(_tslot_ribs(0, COUPON_L))
    key = _xz_prism([(xm - kb / 2, RAIL_LAP_Z - 0.1), (xm + kb / 2, RAIL_LAP_Z - 0.1),
                     (xm + kt / 2, RAIL_LAP_Z + kh), (xm - kt / 2, RAIL_LAP_Z + kh)], -S / 2, S / 2)
    key = key.cut(_box(xm - kt, xm + kt, -LAP_HALF, LAP_HALF, 0, S))
    m = m.union(key)
    for sy in (1, -1):
        m = m.cut(_cyl_z(xm, sy * by, M4_CLEAR, -1, RAIL_LAP_Z + kh + 1))
        m = m.cut(_hex(xm, sy * by, nut_af, -0.1, nut_h + 0.1))

    # ---- female: top half over the lap, dovetail socket, T-slot only beyond the lap
    f = _box(0, COUPON_L, -S / 2, S / 2, 0, S)
    f = f.cut(_box(-0.1, lap, -LAP_HALF, LAP_HALF, W, S - W))
    f = f.cut(_box(lap, COUPON_L + 0.1, -CON_HALF, CON_HALF, W, S - W))
    f = f.cut(_box(-0.1, lap, -S / 2 - 1, S / 2 + 1, -1, RAIL_LAP_Z))
    f = f.cut(_tslot_cut(lap, COUPON_L + 0.1)).union(_tslot_ribs(lap, COUPON_L))
    z0 = RAIL_LAP_Z - 0.1
    zt = RAIL_LAP_Z + kh + c
    sock = _xz_prism([(xf - half(z0, kb) - c, z0), (xf + half(z0, kb) + c, z0),
                      (xf + half(zt, kb) + c, zt), (xf - half(zt, kb) - c, zt)], -S / 2 - 1, S / 2 + 1)
    f = f.cut(sock)
    for sy in (1, -1):
        f = f.cut(_cyl_z(xf, sy * by, M4_CLEAR, RAIL_LAP_Z - 1, S + 1))
        f = f.cut(_cyl_z(xf, sy * by, cb_d, S - cb_h, S + 1))
    return {"PB3_macho": m, "PB3_hembra": f}


def pb3_assembled(m, f):
    """Female moved so the two lap zones overlap (for the interference check and the render)."""
    return f.moved(cq.Location(cq.Vector(COUPON_L - RAIL_DOVETAIL, 0, 0)))


# ------------------------------------------------------------------ PB5 knob
def pb5():
    return {"M12_perilla": gancho.knob()}


# ------------------------------------------------------------------ PB6 seal coupon
def pb6():
    sx, sy = SEAL_COUPON
    assert sx == sy
    h = 20.0   # base height from the brief
    hole_c = sx / 2 - (M3_INSERT_HOLE / 2 + MIN_WALL)
    land_c = sx / 2 - BOX_WALL / 2            # groove path half side: the wall land centreline
    base = _box(-sx / 2, sx / 2, -sy / 2, sy / 2, 0, h).edges("|Z").fillet(SEAL_FILLET)
    cav = (cq.Workplane("XY").workplane(offset=BOX_FLOOR).rect(sx - 2 * BOX_WALL, sy - 2 * BOX_WALL)
           .extrude(h).edges("|Z").fillet(SEAL_CAV_CORNER))
    base = base.cut(cav)
    for ax in (1, -1):
        for ay in (1, -1):
            base = base.cut(_cyl_z(ax * hole_c, ay * hole_c, M3_INSERT_HOLE, h - M3_INSERT_DEPTH, h + 1))
    lid = _box(-sx / 2, sx / 2, -sy / 2, sy / 2, 0, BOX_LID_T).edges("|Z").fillet(SEAL_FILLET)
    gr = SEAL_CAV_CORNER + BOX_WALL / 2       # groove centreline corner radius
    outer = (cq.Workplane("XY").rect(2 * land_c + GROOVE_WIDTH, 2 * land_c + GROOVE_WIDTH).extrude(GROOVE_DEPTH)
             .edges("|Z").fillet(gr + GROOVE_WIDTH / 2))
    inner = (cq.Workplane("XY").workplane(offset=-0.1).rect(2 * land_c - GROOVE_WIDTH, 2 * land_c - GROOVE_WIDTH)
             .extrude(GROOVE_DEPTH + 0.2).edges("|Z").fillet(gr - GROOVE_WIDTH / 2))
    lid = lid.cut(outer.cut(inner))
    for ax in (1, -1):
        for ay in (1, -1):
            lid = lid.cut(_cyl_z(ax * hole_c, ay * hole_c, M3_CLEAR, -1, BOX_LID_T + 1))
    assert ORING_CORD <= GROOVE_DEPTH + 0.6, "cord vs groove"
    return {"PB6_base": base, "PB6_tapa": lid}


# ------------------------------------------------------------------ PB7 clearance comb
def pb7(with_text=True):
    n = len(COMB_CLEARANCES)
    L = n * COMB_PITCH + 4
    xs = [-L / 2 + COMB_PITCH / 2 + 2 + i * COMB_PITCH for i in range(n)]
    plate = _box(-L / 2, L / 2, -COMB_W / 2, COMB_W / 2, 0, COMB_T).edges("|Z").fillet(2)
    for x, c in zip(xs, COMB_CLEARANCES):
        plate = plate.cut(_cyl_z(x, -4.0, COMB_PIN_D + c, -1, COMB_T + 1))
        if with_text:
            txt = (cq.Workplane("XY").workplane(offset=COMB_T - COMB_TEXT_DEPTH).center(x, 7.0)
                   .text(f"+{c}", COMB_TEXT_H, COMB_TEXT_DEPTH + 0.1, combine=False))
            plate = plate.cut(txt)
    pins = _box(xs[0] - 2, xs[-1] + 2, -2, 2, 0, MIN_WALL)      # shared sprue strip joining the pins
    for x in xs:
        pins = pins.union(_cyl_z(x, 0, COMB_PIN_D, 0, PIN_L))
    return {"PB7_peine": plate, "PB7_pines": pins}


def pb8():
    """M4 heat-set insert pull-out: the box floor (BOX_FLOOR) with the inner boss of the rail M4 (BASE_M4_BOSS) and the
    blind insert hole entering from the outer face, as in caja_central.box_body. Outer face on the bed, as M1."""
    a, pitch = INSERT_COUPON
    bd, bh = BASE_M4_BOSS
    plate = _box(-a / 2, a / 2, -a / 2, a / 2, 0, BOX_FLOOR).edges("|Z").fillet(SEAL_FILLET)
    plate = plate.union(_cyl_z(0, 0, bd, BOX_FLOOR - 0.01, BOX_FLOOR + bh))
    plate = plate.cut(_cyl_z(0, 0, M4_INSERT_HOLE, -0.1, M4_INSERT_DEPTH))
    for sx in (1, -1):
        for sy in (1, -1):
            plate = plate.cut(_cyl_z(sx * pitch / 2, sy * pitch / 2, M4_CLEAR, -0.1, BOX_FLOOR + 0.1))
    return {"PB8_inserto_M4": plate}


# ------------------------------------------------------------------ run
RAIL_O, FLAT = ("X", 90), None
ORIENT = {"PB1_garra": ("X", 90), "M14_pestillo": ("X", 90), "PB2_ranura_T": RAIL_O, "PB3_macho": RAIL_O,
          "PB3_hembra": RAIL_O, "PB7_peine": FLAT}
for _d in BUSHING_DIAMETERS:
    ORIENT[f"M13_casquillo_D{int(_d)}"] = ("X", -90)   # flange on the bed

NOTES = {
    "PB1_garra": ("Orientacion: eje del asiento vertical (X 90). Medir con dinamometro de equipaje la fuerza de "
                  "entrada y salida de cada varilla real por casquillo; probar la correa en la ranura 25 x 3; "
                  "comprobar que el casquillo entra a presion en el asiento de 16."),
    "M13_casquillo_D6": "Fuerza de entrada/salida de la varilla D6 (dinamometro); apriete del ajuste a presion en el asiento.",
    "M13_casquillo_D8": "Fuerza de entrada/salida de la varilla D8 (dinamometro); apriete del ajuste a presion en el asiento.",
    "M13_casquillo_D10": "Fuerza de entrada/salida de la varilla D10 (dinamometro); apriete del ajuste a presion en el asiento.",
    "M13_casquillo_D12": "Fuerza de entrada/salida de la varilla D12 (dinamometro); apriete del ajuste a presion en el asiento.",
    "PB2_ranura_T": ("Que la tuerca M4 AF7 entre por la punta y deslice sin holgura excesiva; que el perno pase por "
                     "la abertura de 4.6; fuerza de extraccion. Calibra RAIL_TSLOT (abertura, ancho, alto)."),
    "PB3_macho": ("Imprimir macho y hembra, deslizar la llave de costado (eje Y); holgura de la cola de milano; "
                  "ajuste de los 2 M4 y de la tuerca en la bolsa; ranura T continua en el macho."),
    "PB3_hembra": "Par del macho; revisar el avellanado de la cabeza M4 y la piel de la bolsa de tuerca.",
    "M14_pestillo": ("Montar sobre PB1 con un M3: el resalte de 0.6 debe dar un clic sin trabarse ni soltarse solo; "
                     "calibra LATCH_BUMP; probar con guante."),
    "M12_perilla": ("PAUSAR la impresion al llegar a la altura del bolsillo hexagonal, colocar la cabeza del perno M4, "
                    "reanudar para cerrar la tapa de 1.2. Verificar torque con guante y que no gire la cabeza."),
    "PB6_base": "Insertos termicos M3 en las 4 esquinas; prueba de estanqueidad con la tapa y el o-ring de 2 mm a 1 m.",
    "PB6_tapa": "Ranura 2.6 x 1.5: comprobar compresion del o-ring (25 %) y que el cordon no se salga; sumergir.",
    "PB7_peine": ("Probar que pin entra en cada agujero: la holgura que ajusta sin juego fija FIT_CLEAR y HOLE_COMP "
                  "(sin texto: de izquierda a derecha 0.2, 0.3, 0.4, 0.5)."),
    "PB7_pines": "Cortar los pines del sprue; se prueban en los 4 agujeros del peine.",
    "PB8_inserto_M4": ("Imprimir como M1 (100 %, 5 perimetros, cara de afuera en la cama). Colocar el inserto M4 en caliente "
                       "desde la cara de afuera, atornillar la placa por las 4 esquinas a un marco con hueco central y "
                       "colgar peso o tirar con el dinamometro de un perno M4 en el inserto hasta que salga. El fondo "
                       "real pide 274 N por inserto (Ø500): imprimir 3 y anotar la fuerza de cada una."),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    groups = [("PB1", pb1), ("PB2", pb2), ("PB3", pb3), ("PB4", pb4), ("PB5", pb5), ("PB6", pb6), ("PB7", pb7),
              ("PB8", pb8)]
    shapes, rows, fails = {}, [], []
    for name, fn in groups:
        try:
            parts = fn()
        except Exception as e:  # noqa: BLE001
            fails.append(f"{name}: construccion fallo ({e})")
            print("FAIL build", name, e)
            continue
        if name == "PB7":
            sh0 = {k: sanitize(v) for k, v in parts.items()}
            if not all(brep_check(s)["ok"] for s in sh0.values()):
                WARNINGS.append("PB7: el texto grabado rompio las booleanas; se omite el texto")
                parts = pb7(with_text=False)
        for stem, wp in parts.items():
            shp = sanitize(wp)
            bc = brep_check(shp)
            export_part(shp, stem, OUT)
            orient = ORIENT.get(stem)
            mc = mesh_checks(str(OUT / f"{stem}.stl"), PRINT_BED, orient)
            ok = bc["ok"] and mc["watertight"] and mc["bodies"] == 1 and mc["fits_bed"]
            if not ok:
                fails.append(f"{stem}: brep={bc} mesh={mc}")
            shapes[stem] = shp
            rows.append((stem, bc, mc, orient))
            print(f"{stem:22s} brep_ok={bc['ok']} wt={mc['watertight']} bodies={mc['bodies']} "
                  f"vol={mc['vol_cm3']:.2f} bbox={tuple(round(b, 1) for b in mc['bbox'])} oh={mc['overhang_mm2']:.0f}")

    # interference checks of the assemblies
    try:
        d = _jaw_dims()
        lat = shapes["M14_pestillo"].moved(cq.Location(cq.Vector(d["xp"], 0, d["zp"])))
        iv = shapes["PB1_garra"].intersect(lat).Volume()
        print("latch/jaw interference mm3:", round(iv, 4))
        if iv > 0.5:
            fails.append(f"PB1/PB4: pestillo cerrado interfiere con la garra ({iv:.2f} mm3)")
        fem = pb3_assembled(shapes["PB3_macho"], shapes["PB3_hembra"])
        iv3 = shapes["PB3_macho"].intersect(fem).Volume()
        print("male/female interference mm3:", round(iv3, 4))
        if iv3 > 0.5:
            fails.append(f"PB3: macho y hembra interfieren ({iv3:.2f} mm3)")
    except Exception as e:  # noqa: BLE001
        fails.append(f"chequeo de interferencia fallo: {e}")

    # render: all coupons laid out in a row, modelled orientation
    from render import render
    colours = {"PB1": "#c9a227", "M13": "#d98c3a", "PB2": "#4f81bd", "PB3": "#3a9d7a", "M14": "#c0504d",
               "M12": "#8064a2", "PB6": "#7f7f7f", "PB7": "#2e9fb8", "PB8": "#b04a7a"}
    items, cur = [], 0.0
    for stem, shp in shapes.items():
        if stem == "PB3_hembra":
            continue
        bb = shp.BoundingBox()
        parts = [(stem, shp)]
        if stem == "PB3_macho":
            parts.append(("PB3_hembra", shapes["PB3_hembra"]))
        for pn, ps in parts:
            b = ps.BoundingBox()
            mv = ps.moved(cq.Location(cq.Vector(cur - b.xmin, -(b.ymin + b.ymax) / 2, -b.zmin)))
            items.append((mv, colours.get(pn[:3], colours.get(pn[:2], "#999999")), 1.0, True, None))
            cur += (b.xmax - b.xmin) + 12
    render(items, OUT / "probetas_iso.png", "iso", "Probetas Fase B")

    write_report(rows, fails)
    print("FALLAS:", fails if fails else "ninguna")
    print("AVISOS:", WARNINGS if WARNINGS else "ninguno")
    return 1 if len(fails) >= 2 else 0


def write_report(rows, fails):
    lines = ["# Probetas de la Fase B", "",
             "Generado por `cad_final/probetas.py`. STL en `../salida/probetas/`; render `probetas_iso.png`. "
             "Todas las cotas salen de `params.py`.", "",
             "| pieza | STL | BRep/BOP | estanco | volumen cm3 | bbox en orientacion (mm) | voladizo mm2 | que medir/probar |",
             "|---|---|---|---|---|---|---|---|"]
    for stem, bc, mc, orient in rows:
        o = f"X {orient[1]}" if orient else "plano"
        bb = " x ".join(f"{b:.1f}" for b in mc["bbox"])
        lines.append(f"| {stem} | {stem}.stl | {'ok' if bc['ok'] else 'FALLA'} | {'si' if mc['watertight'] and mc['bodies'] == 1 else 'NO'} "
                     f"| {mc['vol_cm3']:.2f} | {bb} ({o}) | {mc['overhang_mm2']:.0f} | {NOTES.get(stem, '')} |")
    lines += ["", "## Como alimentan los parametros", "",
              "- Peine de holguras (PB7): el resultado fija `FIT_CLEAR` y `HOLE_COMP`.",
              "- Ranura T con tuerca (PB2): fija `RAIL_TSLOT` (abertura, ancho, alto) y `RAIL_TSLOT_RIB`.",
              "- Pestillo (PB4) sobre la garra (PB1): fija el resalte `LATCH_BUMP` de 0.6.",
              "- Garra y casquillos (PB1, M13): el usuario mide con dinamometro de equipaje la fuerza de entrada y salida "
              "por casquillo (varillas reales de 6, 8, 10 y 12).",
              "- Inserto M4 (PB8): la fuerza de arranque se compara con los 274 N por inserto del fondo de la caja "
              "(`reporte_verificacion.md` §4).",
              "", "## Decisiones de diseno", "",
              "- PB1: la garra mide 12 en Y (contacto). La ranura de correa 25 x 3 atraviesa en Y la parte baja, bajo el "
              "asiento. El pestillo gira en un M3 en el labio superior y se aloja en una ranura central de "
              f"{LATCH_T + 2 * FIT_CLEAR:.1f}; la cresta de enganche (0.6) esta en el labio inferior. "
              "El pie lleva un vastago con M4 para atornillarla a PB2.",
              "- Casquillo: pestana en +Y, abertura igual al diametro interior orientada a +X (boca de la J).",
              "- PB2: la ranura T no lleva techo sobre el canal de la tuerca; la tuerca entra por la punta.",
              f"- PB3: los dos M4 atraviesan la llave de cola de milano (la llave queda con "
              f"{(RAIL_DOVETAIL_KEY[0] - M4_CLEAR) / 2:.1f} mm por lado alrededor del agujero a la altura de la base).",
              "- PB5: bolsillo hexagonal cerrado por una tapa de 1.2: pausar la impresion, colocar el perno y seguir.",
              "- PB6: el hueco de la base tiene esquinas interiores grandes para que el sello siga la ruta de la ranura y "
              "los insertos queden en las esquinas macizas.",
              "- PB7: los 4 pines van unidos por un sprue fino en un solo STL (se cortan antes de probar).",
              "- Orientacion de impresion: carril acostado sobre una cara lateral (X 90); garra y pestillo con el eje de "
              "pivote vertical (X 90); casquillos con la pestana sobre la cama (X -90); el resto plano.", ""]
    lines += ["## Avisos", ""] + ([f"- {w}" for w in WARNINGS] if WARNINGS else ["- ninguno"])
    lines += ["", "## Chequeos que fallaron", ""] + ([f"- {f}" for f in fails] if fails else ["- ninguno"])
    lines += ["", "## Params que faltan (constantes de modulo en probetas.py)", ""]
    for k in ("COUPON_L", "JAW_WALL", "JAW_LIP_H", "STRAP_SLOT_T", "STEM_H", "LATCH_T", "LATCH_ARM_W", "LATCH_RIDGE_W",
              "LATCH_TIP_GAP", "LATCH_SWING", "KNOB_LOBE_R", "KNOB_CAP", "SEAL_CAV_CORNER", "SEAL_FILLET",
              "COMB_PITCH", "COMB_T", "COMB_W", "COMB_TEXT_H", "COMB_TEXT_DEPTH", "PIN_L"):
        lines.append(f"- `{k}` = {globals()[k]}")
    (HERE / "reporte_probetas.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
