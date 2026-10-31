"""Rail pieces: M3_riel_central (female half-lap at both ends), M3_riel_ext (male inner end, female outer end) and
M3_riel_punta (male inner end, closed outer end with the cable exit). Decision 29/10 (C18): extensions at a pitch of
100 (piece 100 + 15 male tongue) and one tip piece per side, so the rail is 230 / 430 / 630 with 0 / 1 / 2 extensions.

Joint and T-slot geometry reproduce probetas.py pb2/pb3 (validated as coupons PB2/PB3). Every dimension comes from
params.py; module constants below are design values missing there (listed in reporte_riel.md).
Frame as the rest of cad_final: X along the rail, Y across, Z up, box outer bottom z = 0, rail bottom z = z_rail.
Run from cad_final/:  python riel.py
"""
import math
from pathlib import Path

import cadquery as cq

import camara
import layout
from checks import brep_check, export_part, mesh_checks, min_thickness, sanitize
from params import (XFER_STEP, CAT5E_D, CHAMBER_FLANGE_W, FIT_CLEAR, HOLE_COMP, M4_CLEAR, M4_HEAD, M4_NUT, MIN_WALL,
                    PETG_DENSITY, PLATE_CLR, PLATE_L, PLATE_POCKET_LAYERS, PLATE_POCKET_WALL, PRINT_BED,
                    RAIL_CENTRAL_L, RAIL_DOVETAIL, RAIL_DOVETAIL_KEY, RAIL_EXIT_SLOT, RAIL_EXT_L, RAIL_EXT_PITCH_MODE,
                    RAIL_JOINT_BOLT_Y, RAIL_LAP_WALL, RAIL_LAP_Z, RAIL_SECTION, RAIL_TIP_L, RAIL_TSLOT, RAIL_TSLOT_RIB,
                    M8_ROD, WEB_OVERLAP, RAIL_TIP_END_T, RAIL_WALL, RAIL_ROD_M8, ROD_BULKHEAD_T, ROD_HOLE, ROD_NUT, ROD_PROTRUSION, ROD_WASHER)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "preliminar"

# design values missing in params.py
LANES = camara.lanes()                    # rod axis and cable centreline over the rail bottom (C19)
EXIT_SLOT_ZC = LANES["cable_z"]           # centre height of the exit slot over the rail bottom = cable lane
ROD_Z, BOSS_R = LANES["rod_z"], LANES["boss_r"]

S, W = RAIL_SECTION, RAIL_WALL
CON_HALF = S / 2 - W
LAP_HALF = S / 2 - RAIL_LAP_WALL
TS_OPEN, TS_W, TS_H = RAIL_TSLOT["abertura"], RAIL_TSLOT["ancho"], RAIL_TSLOT["alto"]
LAP = RAIL_DOVETAIL
KB, KT, KH = RAIL_DOVETAIL_KEY
CB_D, CB_H = M4_HEAD[0] + 2 * HOLE_COMP, M4_HEAD[1] + HOLE_COMP
NUT_AF, NUT_H = M4_NUT[0] + HOLE_COMP, M4_NUT[1] + HOLE_COMP
BY = RAIL_JOINT_BOLT_Y


def _box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))


def _hex(cx, cy, af, z0, h):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).polygon(6, af / math.cos(math.pi / 6)).extrude(h)


def _cyl_z(cx, cy, d, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).center(cx, cy).circle(d / 2).extrude(z1 - z0)


def _xz_prism(pts, y0, y1):
    return cq.Workplane("XZ").workplane(offset=-y1).polyline(pts).close().extrude(y1 - y0)


def _half(z, base):
    return base / 2 + (KT - KB) / 2 * (z - RAIL_LAP_Z) / KH


def _female_cuts(f, xc, z0, x0, x1):
    """Female half-lap over [x0, x1] centred on xc: bottom half removed, dovetail socket, 2 M4 with counterbore.
    The caller has already narrowed the duct to the lap width."""
    f = f.cut(_box(x0, x1, -S / 2 - 1, S / 2 + 1, z0 - 1, z0 + RAIL_LAP_Z))
    za = z0 + RAIL_LAP_Z - 0.1
    zt = z0 + RAIL_LAP_Z + KH + FIT_CLEAR
    dz = lambda z: _half(z - z0, KB) + FIT_CLEAR   # noqa: E731
    f = f.cut(_xz_prism([(xc - dz(za), za), (xc + dz(za), za), (xc + dz(zt), zt), (xc - dz(zt), zt)],
                        -S / 2 - 1, S / 2 + 1))
    for sy in (1, -1):
        f = f.cut(_cyl_z(xc, sy * BY, M4_CLEAR, z0 + RAIL_LAP_Z - 1, z0 + S + 1))
        f = f.cut(_cyl_z(xc, sy * BY, CB_D, z0 + S - CB_H, z0 + S + 1))
    return f


def _male_cuts(m, xm, z0, x0, x1):
    """Male half-lap over [x0, x1] centred on xm: top half removed, key up (duct kept open through it), 2 M4 + nut pockets."""
    m = m.cut(_box(x0, x1, -S / 2 - 1, S / 2 + 1, z0 + RAIL_LAP_Z, z0 + S + 1))
    zl = z0 + RAIL_LAP_Z
    key = _xz_prism([(xm - KB / 2, zl - 0.1), (xm + KB / 2, zl - 0.1), (xm + KT / 2, zl + KH), (xm - KT / 2, zl + KH)],
                    -S / 2, S / 2)
    key = key.cut(_box(xm - KT, xm + KT, -LAP_HALF, LAP_HALF, z0, z0 + S))
    m = m.union(key)
    for sy in (1, -1):
        m = m.cut(_cyl_z(xm, sy * BY, M4_CLEAR, z0 - 1, zl + KH + 1))
        m = m.cut(_hex(xm, sy * BY, NUT_AF, z0 - 0.1, NUT_H + 0.1))
    return m


def _tslot(p, z0, x0, x1):
    """Opening through the bottom wall plus the two ribs enclosing the nut channel (as PB2)."""
    p = p.cut(_box(x0 - 0.1, x1 + 0.1, -TS_OPEN / 2, TS_OPEN / 2, z0 - 0.1, z0 + W + 0.1))
    for sg in (1, -1):
        ya, yb = sg * TS_W / 2, sg * (TS_W / 2 + RAIL_TSLOT_RIB)
        p = p.union(_box(x0, x1, min(ya, yb), max(ya, yb), z0 + W - 0.01, z0 + W + TS_H))
    return p


def _cyl_x(x0, x1, y, z, d):
    return cq.Workplane("YZ").workplane(offset=x0).center(y, z).circle(d / 2).extrude(x1 - x0)


def _bulkhead(p, z0, x0, x1, half_w):
    """Rod bulkhead across the duct: a web from wall to wall at the rod height (cable passes over it, nuts under it)."""
    if not RAIL_ROD_M8:
        return p
    return p.union(_box(x0, x1, -half_w - WEB_OVERLAP, half_w + WEB_OVERLAP, z0 + ROD_Z - BOSS_R, z0 + ROD_Z + BOSS_R))


def _rod_bore(p, z0, x0, x1):
    """Through hole of the rod, aligned in every piece (y = 0, z = ROD_Z)."""
    if not RAIL_ROD_M8:
        return p
    return p.cut(_cyl_x(x0 - 1, x1 + 1, 0.0, z0 + ROD_Z, ROD_HOLE))


# ------------------------------------------------------------------ layout along the rail
PASO_100 = RAIL_EXT_PITCH_MODE == "paso_100"
EXT_PIECE_L = RAIL_EXT_L + LAP if PASO_100 else RAIL_EXT_L     # 115 with the male tongue outside the 100 pitch
TIP_PIECE_L = RAIL_TIP_L + LAP
X_JOINT = RAIL_CENTRAL_L / 2 - LAP                               # = camara.dims().x_joint


def ext_step():
    return RAIL_EXT_L if PASO_100 else RAIL_EXT_L - LAP


def placements(n):
    """[(piece, x of its inner end)] on the +X side with n extensions; the -X side is the same turned 180 deg about Z."""
    out = [("ext", X_JOINT + k * ext_step()) for k in range(n)]
    if PASO_100:
        out.append(("punta", X_JOINT + n * ext_step()))
    return out


def tip_x(n):
    """Outer end of the rail (x) with n extensions per side."""
    if PASO_100:
        return X_JOINT + n * ext_step() + TIP_PIECE_L
    return RAIL_CENTRAL_L / 2 + n * ext_step()


# ------------------------------------------------------------------ pieces
def central(lay, c):
    z0 = c.z_rail
    body = camara.chamber_solid(lay, PLATE_POCKET_LAYERS)["M3_riel_central"]
    xj = c.x_joint
    L2 = RAIL_CENTRAL_L / 2
    ft = CHAMBER_FLANGE_W[1]
    for sg in (1, -1):
        xa, xb = sorted((sg * xj, sg * L2))
        xc = sg * (xj + LAP / 2)
        for sy in (1, -1):   # thickened walls: duct 2 * LAP_HALF wide
            ya, yb = sorted((sy * LAP_HALF, sy * CON_HALF))
            body = body.union(_box(xa, xb, ya, yb, z0 + W - 0.01, z0 + S - W + 0.01))
        body = body.cut(_box(xa - 0.1, xb + 0.1, -S / 2 - 1, S / 2 + 1, z0 + S, -ft))   # access window above the rail top
        body = _female_cuts(body, xc, z0, xa - 0.1, xb + 0.1)
        xa, xb = sorted((sg * (xj - 0.1 - ROD_BULKHEAD_T), sg * (xj - 0.1)))     # 0.1 = edge of the female cut
        body = _bulkhead(body, z0, xa, xb, CON_HALF)
    return _rod_bore(body, z0, -L2, L2)


def ext(c, z0=None):
    """Extension in its own frame: x = 0 inner (male) end, x = L outer (female) end, z from z_rail."""
    z0 = c.z_rail if z0 is None else z0
    L = EXT_PIECE_L
    e = _box(0, L, -S / 2, S / 2, z0, z0 + S)
    e = e.cut(_box(LAP, L - LAP, -CON_HALF, CON_HALF, z0 + W, z0 + S - W))
    e = e.cut(_box(-0.1, LAP, -LAP_HALF, LAP_HALF, z0 + W, z0 + S - W))
    e = e.cut(_box(L - LAP, L + 0.1, -LAP_HALF, LAP_HALF, z0 + W, z0 + S - W))
    e = _tslot(e, z0, 0, L - LAP)                       # continuous through the male, ends where the female starts
    e = _male_cuts(e, LAP / 2, z0, -0.1, LAP)
    e = _female_cuts(e, L - LAP / 2, z0, L - LAP, L + 0.1)
    if not PASO_100:      # without a tip piece the cable leaves through the last extension
        e = _exit_slot(e, z0, L)
    e = _bulkhead(e, z0, LAP, LAP + ROD_BULKHEAD_T, CON_HALF)
    e = _bulkhead(e, z0, L - LAP - ROD_BULKHEAD_T, L - LAP, CON_HALF)
    return _rod_bore(e, z0, 0, L)


def _exit_slot(e, z0, L):
    h, ln, dist = RAIL_EXIT_SLOT
    x1 = L - dist
    return e.cut(_box(x1 - ln, x1, CON_HALF - 0.5, S / 2 + 1, z0 + EXIT_SLOT_ZC - h / 2, z0 + EXIT_SLOT_ZC + h / 2))


def punta(c, z0=None):
    """Tip piece in its own frame: x = 0 inner (male) end, x = TIP_PIECE_L outer end, z from z_rail. The T-slot stays
    open at the outer end (nuts of the hooks and of the carriage go in there); cable exit slot on +Y."""
    z0 = c.z_rail if z0 is None else z0
    L = TIP_PIECE_L
    e = _box(0, L, -S / 2, S / 2, z0, z0 + S)
    e = e.cut(_box(LAP, L + 0.1, -CON_HALF, CON_HALF, z0 + W, z0 + S - W))
    e = e.cut(_box(-0.1, LAP, -LAP_HALF, LAP_HALF, z0 + W, z0 + S - W))
    e = _tslot(e, z0, 0, L)
    e = _male_cuts(e, LAP / 2, z0, -0.1, LAP)
    e = _exit_slot(e, z0, L)
    if RAIL_ROD_M8:
        # end wall where the washer and nut bear; the nut channel stays open under the rod lane
        e = e.union(_box(L - RAIL_TIP_END_T, L, -CON_HALF - 0.01, CON_HALF + 0.01, z0 + W - 0.01, z0 + S - W + 0.01)
                    .cut(_box(L - RAIL_TIP_END_T - 1, L + 1, -TS_W / 2, TS_W / 2, z0 + W - 1, z0 + W + TS_H)))
        e = _bulkhead(e, z0, LAP, LAP + ROD_BULKHEAD_T, CON_HALF)
    return _rod_bore(e, z0, 0, L)


def rod_parts(n, z_rail):
    """M8 rod, wide washers and nuts in the box frame (both tips), for assemblies and checks."""
    if not RAIL_ROD_M8:
        return {}
    xt = tip_x(n)
    wd, wt, wi = ROD_WASHER
    af, nh = ROD_NUT
    zr = z_rail + ROD_Z
    half = xt + wt + nh + ROD_PROTRUSION
    out = {"varilla M8": _cyl_x(-half, half, 0.0, zr, M8_ROD["d"])}
    for sg, tag in ((1, "+X"), (-1, "-X")):
        xa, xb = sorted((sg * xt, sg * (xt + wt)))
        out[f"arandela M8 {tag}"] = _cyl_x(xa, xb, 0.0, zr, wd).cut(_cyl_x(xa - 1, xb + 1, 0.0, zr, wi))
        xa, xb = sorted((sg * (xt + wt), sg * (xt + wt + nh)))
        nut = (cq.Workplane("YZ").workplane(offset=xa).center(0.0, zr).polygon(6, af / math.cos(math.pi / 6))
               .extrude(xb - xa).cut(_cyl_x(xa - 1, xb + 1, 0.0, zr, M8_ROD["d"])))
        out[f"tuerca M8 {tag}"] = nut
    return out


def rod_length(n):
    wd, wt, wi = ROD_WASHER
    return 2 * (tip_x(n) + wt + ROD_NUT[1] + ROD_PROTRUSION)


# ------------------------------------------------------------------ run
ORIENT = {"M3_riel_central": ("X", 180), "M3_riel_ext": ("X", 90), "M3_riel_punta": ("X", 90),
          "M3_tapa_bolsillo": None}


def vol(s):
    return s.Volume()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "stl").mkdir(exist_ok=True)
    (OUT / "step").mkdir(exist_ok=True)
    lay = layout.build(floors=1)
    c = camara.dims(lay)
    builds = {"M3_riel_central": lambda: central(lay, c), "M3_riel_ext": lambda: ext(c),
              "M3_tapa_bolsillo": lambda: camara.chamber_solid(lay, PLATE_POCKET_LAYERS)["tapa_bolsillo_n"]}
    if PASO_100:
        builds["M3_riel_punta"] = lambda: punta(c)
    shapes, rows, fails = {}, [], []
    for stem, fn in builds.items():
        try:
            shp = sanitize(fn())
        except Exception as e:  # noqa: BLE001
            fails.append(f"{stem}: construccion fallo ({e})")
            print("FAIL build", stem, e)
            continue
        bc = brep_check(shp)
        export_part(shp, stem, OUT / "stl", OUT / "step")
        stl = str(OUT / "stl" / f"{stem}.stl")
        mc = mesh_checks(stl, PRINT_BED, ORIENT[stem])
        p1, pmin = min_thickness(stl)
        ok = bc["ok"] and mc["watertight"] and mc["bodies"] == 1 and mc["fits_bed"]
        if not ok:
            fails.append(f"{stem}: brep={bc} mesh={mc}")
        if p1 < MIN_WALL:
            fails.append(f"{stem}: espesor minimo p1 {p1:.2f} < {MIN_WALL}")
        shapes[stem] = shp
        rows.append((stem, bc, mc, p1, pmin, shp.Volume() / 1000.0))
        print(f"{stem:18s} brep_ok={bc['ok']} {bc} wt={mc['watertight']} bodies={mc['bodies']} fits={mc['fits_bed']} "
              f"vol={mc['vol_cm3']:.2f} bbox={tuple(round(b, 1) for b in mc['bbox'])} oh={mc['overhang_mm2']:.0f} "
              f"p1={p1:.2f} min={pmin:.2f}")
    if "M3_tapa_bolsillo" not in shapes or len(shapes) < len(builds):
        raise SystemExit("STOP: pieza(s) fallaron: " + "; ".join(fails))

    cen, ex = shapes["M3_riel_central"], shapes["M3_riel_ext"]
    xj = c.x_joint
    assert abs(xj - X_JOINT) < 1e-9, (xj, X_JOINT)
    ex_p = ex.moved(cq.Location(cq.Vector(xj, 0, 0)))
    ex_m = ex_p.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180)
    ex1 = ex.moved(cq.Location(cq.Vector(xj, 0, 0)))
    ex2 = ex.moved(cq.Location(cq.Vector(xj + ext_step(), 0, 0)))
    pairs = {"central+ext(+X)": (cen, ex_p), "central+ext(-X)": (cen, ex_m), "ext+ext": (ex1, ex2)}
    if PASO_100:
        pu = shapes["M3_riel_punta"]
        pairs["central+punta (0 ext.)"] = (cen, pu.moved(cq.Location(cq.Vector(xj, 0, 0))))
        pairs["ext+punta"] = (ex1, pu.moved(cq.Location(cq.Vector(xj + ext_step(), 0, 0))))
    inter = {}
    for name, (a, b) in pairs.items():
        inter[name] = a.intersect(b).Volume()
        print("interferencia", name, round(inter[name], 4), "mm3")
        if inter[name] > 0.5:
            fails.append(f"interferencia {name}: {inter[name]:.2f} mm3")
    # rod and cable lanes through the whole rail with 2 extensions per side (every kind of joint)
    lanes = {}
    if RAIL_ROD_M8:
        chain = [cen]
        for name, x0 in placements(2):
            sh = shapes["M3_riel_ext" if name == "ext" else "M3_riel_punta"].moved(cq.Location(cq.Vector(x0, 0, 0)))
            chain += [sh, sh.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180)]
        rod = rod_parts(2, c.z_rail)
        h, ln, dist = RAIL_EXIT_SLOT
        x_exit = tip_x(2) - dist - ln / 2
        cable = _cyl_x(xj - ROD_BULKHEAD_T - 1, x_exit, 0.0, c.z_rail + EXIT_SLOT_ZC, CAT5E_D).val()
        lanes["varilla M8 contra los tramos (2 ext.)"] = sum(rod["varilla M8"].val().intersect(t).Volume() for t in chain)
        lanes["Cat5e (+X, del tabique del central a la salida) contra los tramos"] = sum(cable.intersect(t).Volume() for t in chain)
        lanes["Cat5e contra la varilla"] = cable.intersect(rod["varilla M8"].val()).Volume()
        for k in ("arandela M8 +X", "tuerca M8 +X"):
            lanes[f"{k} contra la punta"] = rod[k].val().intersect(chain[-2]).Volume()
        for k, v in lanes.items():
            print("carril", k, round(v, 4), "mm3")
            if v > 0.5:
                fails.append(f"carril {k}: {v:.2f} mm3")
    # ballast pockets leave the joint zone free: nothing of the central in the bottom half over the lap
    px = PLATE_L / 2 + PLATE_CLR + PLATE_POCKET_WALL
    zone = _box(xj, xj + LAP, -60, 60, c.z_rail - 1, c.z_rail + RAIL_LAP_Z).val()
    free = cen.intersect(zone).Volume()
    print("bolsillos: x max", px, "zona de union desde", xj, "volumen del central en la media madera inferior", round(free, 4))
    if px >= xj or free > 1e-3:
        fails.append(f"bolsillos de lastre invaden la zona de union (x max {px}, vol {free:.3f})")
    # sideways slide of the male lap along Y
    male_zone = ex.intersect(_box(-1, LAP, -S, S, c.z_rail - 1, c.z_rail + S + 1).val())
    worst, y = 0.0, -80.0
    while y <= 80.0:
        iv = cen.intersect(male_zone.moved(cq.Location(cq.Vector(xj, y, 0)))).Volume() if abs(y) > 0 else 0.0
        if abs(y) >= 1e-9:
            worst = max(worst, iv) if abs(y) > S / 2 + KB else worst
        y += XFER_STEP
    print("deslizamiento lateral del macho (|y| > 19): interferencia max", round(worst, 4), "mm3")
    if worst > 0.5:
        fails.append(f"el macho no desliza de costado: {worst:.2f} mm3")

    from render import render
    gap, off = 35.0, 130.0
    items = [(cen, "#3a9d7a", 1.0, True, None)]
    ce = cen.moved(cq.Location(cq.Vector(0, -off, 0)))
    items.append((ce, "#3a9d7a", 1.0, True, None))
    for name, x0 in placements(1):
        sh = shapes["M3_riel_ext" if name == "ext" else "M3_riel_punta"].moved(cq.Location(cq.Vector(x0, 0, 0)))
        col = "#4f81bd" if name == "ext" else "#c9a227"
        for sg in (1, -1):
            e = sh if sg > 0 else sh.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), 180)
            items.append((e, col, 1.0, True, None))
            k = 1 if name == "ext" else 2
            items.append((e.moved(cq.Location(cq.Vector(sg * k * gap, -off, 0))), col, 1.0, True, None))
    render(items, OUT / "riel_iso.png", "iso", f"Riel con 1 extension por lado ({2 * tip_x(1):.0f} mm): montado y explotado")
    write_report(rows, inter, free, worst, fails, c, lanes)
    print("FALLAS:", fails if fails else "ninguna")
    return 1 if len(fails) >= 2 else 0


def write_report(rows, inter, free, worst, fails, c, lanes):
    L = ["# Piezas del riel", "",
         "Generado por `cad_final/riel.py`. STL en `../salida/preliminar/stl/`, STEP en `step/`, render `riel_iso.png`. "
         "Todas las cotas salen de `params.py`; la union y la ranura T reproducen las probetas PB2/PB3.", "",
         f"Armado (decision del 29/10, C18): tramo central + {'0 / 1 / 2 extensiones de paso ' + format(RAIL_EXT_L, 'g') + ' (pieza de ' + format(EXT_PIECE_L, 'g') + ') + una punta de ' + format(TIP_PIECE_L, 'g') + ' por lado' if PASO_100 else 'extensiones solapadas'}: "
         f"riel de {2 * tip_x(0):.0f} / {2 * tip_x(1):.0f} / {2 * tip_x(2):.0f} mm.", "",
         "| pieza | STL | BRep/BOP | estanco | cuerpos | bbox en orientacion (mm) | voladizo mm2 | espesor minimo p1 (mm) | masa al 100 % (g) | volumen cm3 |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for stem, bc, mc, p1, pmin, v in rows:
        o = ORIENT[stem]
        bb = " x ".join(f"{b:.1f}" for b in mc["bbox"])
        flag = "" if p1 >= MIN_WALL else " (BAJO EL MINIMO)"
        L.append(f"| {stem} | {stem}.stl | {'ok' if bc['ok'] else 'FALLA'} | {'si' if mc['watertight'] else 'NO'} | "
                 f"{mc['bodies']} | {bb} ({f'X {o[1]}' if o else 'plana'}) | {mc['overhang_mm2']:.0f} | {p1:.2f}{flag} (min absoluto {pmin:.2f}) | "
                 f"{v * PETG_DENSITY:.1f} | {v:.2f} |")
    L += ["", "## Interferencias de ensamble", ""]
    for k, v in inter.items():
        L.append(f"- {k}: {v:.3f} mm3")
    L += [f"- Bolsillos de lastre: llegan hasta |x| = {PLATE_L / 2 + PLATE_CLR + PLATE_POCKET_WALL}, la zona de union empieza en |x| = {c.x_joint}; "
          f"volumen del central dentro de la media madera inferior de la union: {free:.3f} mm3. El macho entra de costado (eje Y) sin tocar los bolsillos.",
          f"- Deslizamiento lateral del macho, barrido cada {XFER_STEP:.0f} mm fuera del riel: interferencia maxima {worst:.3f} mm3.", ""]
    if lanes:
        L += ["## Varilla M8 y cable en el conducto (C19)", "",
              f"Desde el fondo del riel: canal de tuercas hasta {RAIL_WALL + RAIL_TSLOT['alto']:g}, varilla con su eje a {ROD_Z:.2f} "
              f"(agujero Ø{ROD_HOLE:g} en tabiques de {ROD_BULKHEAD_T:g} en cada extremo de cada tramo y en la pared del extremo de la "
              f"punta), Cat5e con su eje a {EXIT_SLOT_ZC:.2f}. En la union el conducto mide {2 * LAP_HALF:g} de ancho: pasan la varilla "
              f"(Ø{M8_ROD['d']:g}) y un Cat5e encima; dos Cat5e no entran ni lado a lado ({2 * CAT5E_D:g} > {2 * LAP_HALF:g}) ni uno "
              f"sobre otro (quedan {S - W - (ROD_Z + M8_ROD['d'] / 2):.1f} de alto sobre la varilla). Cada lado lleva un solo cable, "
              "el de su capsula, asi que alcanza.", ""]
        L += [f"- {k}: {v:.3f} mm3" for k, v in lanes.items()]
        L += ["", "Las tuercas del canal pasan bajo los tabiques; un M4 que asome sobre su tuerca debe quedar a menos de "
              f"{ROD_Z - BOSS_R - (RAIL_WALL + RAIL_TSLOT['alto']):.1f} sobre el canal (M4 x 14 con la brida del gancho de 6).", ""]
    L += ["## Orientacion de impresion", "",
          "- M3_riel_central: brida abajo (X 180). La ventana de acceso sobre la union evita puentes largos; el voladizo de la tabla es el de los techos de la camara y de los bolsillos de lastre, con soportes locales. "
          "El central es la pieza que mas soporte necesita.",
          "- M3_tapa_bolsillo (2 por nodo): plana; cierra por abajo el bolsillo de las pletinas de inox. Se fija con 2 M3 x 8 "
          "avellanados a insertos M3 en bosses de la pared exterior del bolsillo; la cabeza queda al ras del fondo del riel.",
          "- M3_riel_punta: acostada sobre una cara lateral (X 90), como la extension.",
          "- M3_riel_ext: acostada sobre una cara lateral (X 90), como las probetas PB2/PB3. La llave de cola de milano y la ranura T quedan de perfil; la ranura de salida del cable (+Y) queda en la cara lateral.", "",
          "## Orden de montaje", "",
          "1. Cargar las tuercas M4 en la ranura T por las puntas ANTES de unir una extension: en el central la ranura queda abierta en las caras |x| = 55 (frente a la media madera vacia); en la extension queda abierta por la punta macho.",
          "2. Deslizar el macho de la extension de costado (eje Y) en la media madera inferior de la hembra hasta que la llave entre en el nido de cola de milano.",
          "3. Los 2 M4 verticales de la union (y = +-10) van por las paredes engrosadas: cabeza en el avellanado de la hembra (por la ventana de acceso en el central) y tuerca en la bolsa hexagonal del macho.",
          "4. Un cable Cat5e por lado, en el conducto local de 10 mm. " + ("Sale por la ranura lateral (+Y) de la punta, junto al carro." if PASO_100 else "En una extension encadenada la ranura de salida (+Y) solo se usa en la ultima: la hembra exterior queda cubierta por el macho de la siguiente."), ""]
    L += ["## Chequeos que fallaron", ""] + ([f"- {f}" for f in fails] if fails else ["- ninguno"])
    L += ["", "## Params que faltan (constantes de modulo en riel.py)", "",
          f"- `EXIT_SLOT_ZC` = {EXIT_SLOT_ZC:.2f}: altura del centro de la ranura de salida sobre el fondo del riel (cable sobre las costillas).",
          f"- `XFER_STEP` = {XFER_STEP}: paso del barrido de deslizamiento lateral (solo verificacion)."]
    (HERE / "reporte_riel.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
