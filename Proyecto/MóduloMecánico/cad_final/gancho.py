"""Fase C ring hook: M9_gancho, M13_casquillo_D*, M14_pestillo, M12_perilla. Every dimension comes from params.py;
module constants below are design values still missing there (listed in reporte_gancho.md).

Frame: X along the rail, Y across, Z up, rail bottom face (= flange top) at z = 0. Seat-local frame (jaw_dims, jaw_body,
bushings, latch): bore axis along Y through x = z = 0, J mouth toward +X. jaw_body/bushings/latch/knob are shared with
probetas.py (PB1, PB4, PB5).
Run from cad_final/:  python gancho.py
"""
import math
from pathlib import Path

import cadquery as cq

from checks import brep_check, export_part, mesh_checks, min_thickness, sanitize
from params import (KNOB_FREE_EXTRA, KNOB_WEB_GAP, KNOB_FLANGE_GAP, BUSHING_TIP_MARGIN, WEB_OVERLAP, BUSHING_DIAMETERS, BUSHING_FLANGE, BUSHING_PRESS, BUSHING_ROD_CLR, FIT_CLEAR, HOLE_COMP,
                    HOOK_CONTACT_W, HOOK_DROP, HOOK_EDGE_R, HOOK_FLANGE, HOOK_LOAD_N, JAW_BORE, JAW_LIP_H, JAW_WALL,
                    KNOB_CAP, KNOB_D, KNOB_H, KNOB_LOBE_R, KNOB_LOBES, LATCH_ARM_W, LATCH_BUMP, LATCH_PIVOT,
                    LATCH_RIDGE_W, LATCH_SWING, LATCH_T, LATCH_TAB, LATCH_TIP_GAP, M3_CLEAR, M4_CLEAR, M4_HEX_HEAD,
                    MIN_WALL, PETG_DENSITY, PRINT_BED, RAIL_SECTION, SHELL_T, STRAP_SLOT_T, STRAP_W, STEM_H)

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "salida" / "preliminar"

# ------------------------------------------------------------------ design values missing from params.py


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


# ------------------------------------------------------------------ seat-local pieces (shared with probetas.py)
def jaw_dims():
    R = JAW_BORE / 2
    mouth = max(BUSHING_DIAMETERS) + BUSHING_ROD_CLR
    x0 = -(R + JAW_WALL)
    x_end = x0 + STRAP_W + 2 * JAW_WALL
    z_top = mouth / 2 + JAW_LIP_H
    z_strap1 = -(R + JAW_WALL)
    z_strap0 = z_strap1 - STRAP_SLOT_T
    z_bot = z_strap0 - JAW_WALL
    xp = x_end - (0.6 + LATCH_RIDGE_W + 0.1 + LATCH_BUMP + LATCH_ARM_W / 2)
    zp = mouth / 2 + JAW_LIP_H / 2
    return dict(R=R, mouth=mouth, x0=x0, x_end=x_end, z_top=z_top, z_strap0=z_strap0, z_strap1=z_strap1,
                z_bot=z_bot, xp=xp, zp=zp, slot_w=LATCH_T + 2 * FIT_CLEAR)


def jaw_body(stem_up=STEM_H, stem_hole=True, warnings=None):
    """J jaw with seat, mouth, strap slot, latch pivot + slot and catch ridge; a stem of stem_up above the lip top."""
    d = jaw_dims()
    R, mouth, x0, xe = d["R"], d["mouth"], d["x0"], d["x_end"]
    hw = HOOK_CONTACT_W / 2
    assert JAW_BORE > max(BUSHING_DIAMETERS), "seat smaller than rod"
    jaw = _box(x0, xe, -hw, hw, d["z_bot"], d["z_top"]).edges("|Y").fillet(HOOK_EDGE_R)
    stem_w = R + JAW_WALL
    jaw = jaw.union(_box(x0, x0 + stem_w, -hw, hw, d["z_top"] - HOOK_EDGE_R, d["z_top"] + stem_up))
    jaw = jaw.cut(_cyl_y(0, 0, JAW_BORE, -hw - 1, hw + 1))
    jaw = jaw.cut(_box(0, xe + 1, -hw - 1, hw + 1, -mouth / 2, mouth / 2))
    lip_x = math.sqrt(R * R - (mouth / 2) ** 2)
    try:
        jaw = jaw.edges(cq.selectors.BoxSelector((lip_x - 0.5, -1, -mouth / 2 - 0.5), (lip_x + 0.5, 1, mouth / 2 + 0.5))
                        ).fillet(HOOK_EDGE_R)
    except Exception as e:  # noqa: BLE001
        if warnings is not None:
            warnings.append(f"jaw: el redondeo R{HOOK_EDGE_R} del labio de la J fallo ({e}); queda en arista viva")
    jaw = jaw.cut(_box(-STRAP_W / 2 + (x0 + xe) / 2, STRAP_W / 2 + (x0 + xe) / 2, -hw - 1, hw + 1,
                       d["z_strap0"], d["z_strap1"]))
    jaw = jaw.cut(_cyl_y(d["xp"], d["zp"], M3_CLEAR, -hw - 1, hw + 1))
    jaw = jaw.cut(_box(d["xp"] - LATCH_SWING, xe + 1, -d["slot_w"] / 2, d["slot_w"] / 2, mouth / 2 - 0.5,
                       d["z_top"] + 1))
    if stem_hole:
        jaw = jaw.cut(_cyl_z(x0 + stem_w / 2, 0, M4_CLEAR, R * 0.5, d["z_top"] + stem_up + 1))
    xr0 = d["xp"] + LATCH_ARM_W / 2 + LATCH_BUMP + 0.1
    zl = -mouth / 2
    ridge = _xz_prism([(xr0, zl - 0.01), (xr0 + 0.3, zl + LATCH_BUMP), (xr0 + LATCH_RIDGE_W - 0.3, zl + LATCH_BUMP),
                       (xr0 + LATCH_RIDGE_W, zl - 0.01)], -hw, hw)
    return jaw.union(ridge)


def bushings():
    """C bushings, one per rod size; mouth = rod D + clearance toward +X, tips trimmed to MIN_WALL + margin."""
    hw = HOOK_CONTACT_W / 2
    od = JAW_BORE + BUSHING_PRESS
    out = {}
    for dia in BUSHING_DIAMETERS:
        idia = dia + BUSHING_ROD_CLR
        fl_y = hw + BUSHING_FLANGE[1]
        b = _cyl_y(0, 0, od, -hw, hw).union(_cyl_y(0, 0, BUSHING_FLANGE[0], hw - 0.01, fl_y))
        b = b.cut(_cyl_y(0, 0, idia, -hw - 1, fl_y + 1))
        b = b.cut(_box(0, od, -hw - 1, fl_y + 1, -idia / 2, idia / 2))
        t = MIN_WALL + BUSHING_TIP_MARGIN
        x_trim = math.sqrt((od / 2) ** 2 - (idia / 2 + t) ** 2)    # outer circle meets z = idia/2 + t
        assert idia / 2 + t < od / 2, "bushing wall too thin for the tip trim"
        b = b.cut(_box(x_trim, od, -hw - 1, fl_y + 1, -od, od))
        out[f"M13_casquillo_D{int(dia)}"] = b
    return out


def latch():
    d = jaw_dims()
    tip = -(d["zp"] + d["mouth"] / 2 - LATCH_TIP_GAP)
    aw = LATCH_ARM_W / 2
    zn = d["z_top"] + 1 - d["zp"]
    tab_l, tab_w = LATCH_TAB
    pts = [(-aw, tip), (aw + LATCH_BUMP, tip), (aw + LATCH_BUMP, tip + 0.7), (aw, tip + 1.3), (aw, zn),
           (tab_w / 2, zn), (tab_w / 2, tab_l), (-tab_w / 2, tab_l), (-tab_w / 2, zn), (-aw, zn)]
    p = _xz_prism(pts, -LATCH_T / 2, LATCH_T / 2)
    # boss around the pivot: the 5-wide arm left 0.8 beside the hole; centred on the pivot, it sweeps only itself
    hole = LATCH_PIVOT + 0.4                                            # M3 + 0.4 pivot clearance
    p = p.union(_cyl_y(0, 0, hole + 2 * (MIN_WALL + BUSHING_TIP_MARGIN), -LATCH_T / 2, LATCH_T / 2))
    return p.cut(_cyl_y(0, 0, hole, -LATCH_T, LATCH_T))


def knob():
    r_base = KNOB_D / 2 - KNOB_LOBE_R
    k = cq.Workplane("XY").circle(r_base).extrude(KNOB_H)
    for i in range(KNOB_LOBES):
        a = 2 * math.pi * i / KNOB_LOBES
        k = k.union(_cyl_z(r_base * math.cos(a), r_base * math.sin(a), 2 * KNOB_LOBE_R, 0, KNOB_H))
    pocket_h = M4_HEX_HEAD[1] + HOLE_COMP
    z_top = KNOB_H - KNOB_CAP
    k = k.cut(_hex(0, 0, M4_HEX_HEAD[0] + HOLE_COMP, z_top - pocket_h, pocket_h))
    return k.cut(_cyl_z(0, 0, M4_CLEAR, -1, z_top - pocket_h + 0.1))


# ------------------------------------------------------------------ M9_gancho
FL_L, FL_T = HOOK_FLANGE
FL_W = RAIL_SECTION


def hook_layout():
    d = jaw_dims()
    free_d = KNOB_D + KNOB_FREE_EXTRA
    xk = d["x0"] - KNOB_WEB_GAP - free_d / 2
    fx0 = xk - free_d / 2
    return dict(d=d, free_d=free_d, xk=xk, fx0=fx0, fx1=fx0 + FL_L, jaw_top_abs=d["z_top"] - HOOK_DROP)


def gancho():
    L = hook_layout()
    d = L["d"]
    assert L["fx1"] > 0 + 1 and L["fx1"] > d["x0"] + (d["R"] + JAW_WALL), "flange does not cover the seat axis"
    stem_up = (HOOK_DROP - FL_T + WEB_OVERLAP) - d["z_top"]
    jaw = jaw_body(stem_up=stem_up, stem_hole=False).translate((0, 0, -HOOK_DROP))
    fl = _box(L["fx0"], L["fx1"], -FL_W / 2, FL_W / 2, -FL_T, 0)
    h = jaw.union(fl)
    return h.cut(_cyl_z(L["xk"], 0, M4_CLEAR, -FL_T - 1, 1))


def placed_parts():
    """Latch (closed) and knob (flipped, bolt exits upward) in hook coordinates."""
    L = hook_layout()
    d = L["d"]
    lat = latch().val().moved(cq.Location(cq.Vector(d["xp"], 0, d["zp"] - HOOK_DROP)))
    kn = knob().val().rotate((0, 0, 0), (1, 0, 0), 180).moved(
        cq.Location(cq.Vector(L["xk"], 0, -FL_T - KNOB_FLANGE_GAP)))
    return lat, kn


# ------------------------------------------------------------------ run
ORIENT = {"M9_gancho": ("X", 90), "M14_pestillo": ("X", 90), "M12_perilla": None}
for _d in BUSHING_DIAMETERS:
    ORIENT[f"M13_casquillo_D{int(_d)}"] = ("X", -90)   # flange on the bed

NOTES = {
    "M9_gancho": ("Cargar la J con el casquillo y la varilla real; tirar 75 N con dinamometro de equipaje y medir la "
                  "flexion del alma; comprobar HOOK_DROP con el aro real; pasar la correa de 25 x 3."),
    "M14_pestillo": "Clic de cierre sobre la cresta (LATCH_BUMP) sin trabarse; probar con guante.",
    "M12_perilla": "Pausar la impresion en el bolsillo hexagonal, colocar el perno M4 y reanudar; torque con guante.",
}
for _d in BUSHING_DIAMETERS:
    NOTES[f"M13_casquillo_D{int(_d)}"] = (f"Fuerza de entrada y salida de la varilla D{int(_d)} (dinamometro); "
                                          "apriete a presion en el asiento.")


def masses(stl_path, vol_cm3):
    import trimesh
    m = trimesh.load(stl_path)
    skin = min(m.area * SHELL_T / 1000.0, vol_cm3)
    return (skin + 0.4 * (vol_cm3 - skin)) * PETG_DENSITY, vol_cm3 * PETG_DENSITY


def main():
    stl_dir, step_dir = OUT / "stl", OUT / "step"
    stl_dir.mkdir(parents=True, exist_ok=True)
    step_dir.mkdir(parents=True, exist_ok=True)
    warns = []
    parts = {"M9_gancho": gancho()}
    parts.update(bushings())
    parts["M14_pestillo"] = latch()
    parts["M12_perilla"] = knob()
    shapes, rows, fails = {}, [], []
    for stem, wp in parts.items():
        try:
            shp = sanitize(wp)
            bc = brep_check(shp)
            export_part(shp, stem, stl_dir, step_dir)
            stl = str(stl_dir / f"{stem}.stl")
            mc = mesh_checks(stl, PRINT_BED, ORIENT[stem])
            p1, pmin = min_thickness(stl)
            m40, m100 = masses(stl, mc["vol_cm3"])
        except Exception as e:  # noqa: BLE001
            fails.append(f"{stem}: {e}")
            print("FAIL", stem, e)
            continue
        ok = bc["ok"] and mc["watertight"] and mc["bodies"] == 1 and mc["fits_bed"]
        if not ok:
            fails.append(f"{stem}: brep={bc} mesh={mc}")
        if p1 < MIN_WALL:
            warns.append(f"{stem}: espesor p1 {p1:.2f} < {MIN_WALL}")
        shapes[stem] = shp
        rows.append((stem, bc, mc, p1, pmin, m40, m100))
        print(f"{stem:20s} ok={ok} brep={bc['ok']} wt={mc['watertight']} bodies={mc['bodies']} vol={mc['vol_cm3']:.2f} "
              f"bbox={tuple(round(b, 1) for b in mc['bbox'])} oh={mc['overhang_mm2']:.0f} p1={p1:.2f} min={pmin:.2f} "
              f"m40={m40:.1f} m100={m100:.1f}")
    if len(fails) >= 2:
        print("STOP: 2+ piezas fallaron", fails)
        return 1

    # checks: knob clearance, latch closed vs jaw, assembly
    L = hook_layout()
    h = shapes["M9_gancho"]
    lat, kn = placed_parts()
    free = cq.Workplane("XY").add(cq.Solid.makeCylinder(L["free_d"] / 2, -FL_T - L["jaw_top_abs"], cq.Vector(L["xk"], 0, L["jaw_top_abs"]),
                                                          cq.Vector(0, 0, 1))).val()
    free_iv = h.intersect(free).Volume()
    assert free_iv < 1e-3, f"knob free cylinder hits the hook ({free_iv} mm3)"
    kn_iv = h.intersect(kn).Volume()
    iv = h.intersect(lat).Volume()
    b10 = shapes["M13_casquillo_D10"].moved(cq.Location(cq.Vector(0, 0, -HOOK_DROP)))
    iv_b = lat.intersect(b10).Volume()
    print(f"free cylinder d={L['free_d']} z[{L['jaw_top_abs']:.1f},{-FL_T}] interference {free_iv:.4f}; "
          f"knob/hook {kn_iv:.4f}; latch/jaw {iv:.4f}; latch/bushing D10 {iv_b:.4f}")
    if iv > 0.5:
        fails.append(f"pestillo cerrado interfiere con el gancho ({iv:.2f} mm3)")

    from render import render
    rod = cq.Workplane("XZ").workplane(offset=-40).center(0, -HOOK_DROP).circle(5).extrude(80).val()
    rail = _box(-70, 50, -RAIL_SECTION / 2, RAIL_SECTION / 2, 0.0, RAIL_SECTION).val()
    items = [(rail, "#4f81bd", 0.3, True, None), (rod, "#7f7f7f", 0.55, True, None),
             (h, "#c9a227", 1.0, True, None), (b10, "#d98c3a", 1.0, True, None),
             (lat, "#c0504d", 1.0, True, None), (kn, "#8064a2", 1.0, True, None)]
    render(items, OUT / "gancho_iso.png", "iso", "Gancho Fase C (D10, pestillo cerrado)")

    write_report(rows, warns, fails, L, free_iv, kn_iv, iv, iv_b)
    print("FALLAS:", fails if fails else "ninguna", "| AVISOS:", warns if warns else "ninguno")
    return 1 if len(fails) >= 2 else 0


def write_report(rows, warns, fails, L, free_iv, kn_iv, iv, iv_b):
    lines = ["# Gancho de la Fase C", "",
             "Generado por `cad_final/gancho.py`. STL y STEP en `../salida/preliminar/`; render `gancho_iso.png`. "
             "Todas las cotas salen de `params.py`.", "",
             "| pieza | STL | BRep/BOP | estanco | cuerpos | bbox en orientacion (mm) | voladizo mm2 | espesor min p1 (mm) | "
             "masa 40 % (g) | masa 100 % (g) | que medir |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for stem, bc, mc, p1, pmin, m40, m100 in rows:
        o = ORIENT[stem]
        ot = f"X {o[1]}" if o else "plano"
        bb = " x ".join(f"{b:.1f}" for b in mc["bbox"])
        flag = " (BAJO MIN_WALL)" if p1 < MIN_WALL else ""
        lines.append(f"| {stem} | {stem}.stl | {'ok' if bc['ok'] else 'FALLA'} | {'si' if mc['watertight'] else 'NO'} | "
                     f"{mc['bodies']} | {bb} ({ot}) | {mc['overhang_mm2']:.0f} | {p1:.2f} (min {pmin:.2f}){flag} | "
                     f"{m40:.1f} | {m100:.1f} | {NOTES[stem]} |")
    lines += ["", "## Chequeos", "",
              f"- Holgura de la perilla: cilindro libre de D{L['free_d']:.0f} (KNOB_D + {KNOB_FREE_EXTRA}) centrado en "
              f"x = {L['xk']:.1f}, desde la cara inferior de la brida (z = {-FL_T}) hasta la cara superior de la mandibula "
              f"(z = {L['jaw_top_abs']:.1f}): interferencia con el gancho {free_iv:.4f} mm3 (assert < 0.001). "
              f"Perilla montada (invertida, perno hacia arriba) contra el gancho: {kn_iv:.4f} mm3.",
              f"- Pestillo cerrado contra la mandibula: {iv:.4f} mm3 (esperado 0). Contra el casquillo D10: {iv_b:.4f} mm3.",
              f"- Brida {FL_L} x {FL_W} x {FL_T}, agujero M4 de paso en x = {L['xk']:.1f}, fuera del alma "
              f"(alma en x de {L['d']['x0']:.0f} a 0). Centro de varilla {HOOK_DROP} mm bajo la cara superior de la brida.",
              f"- Carga {HOOK_LOAD_N} N en el asiento: orientacion de impresion con el perfil XZ sobre la cama (X 90), "
              "capas en planos XZ; la carga vertical sobre el asiento y el alma va a lo largo de las capas, no a traves. "
              "Los ejes del asiento, del pivote y de la correa quedan verticales (sin voladizo). El voladizo medido viene "
              "del escalon de ancho 30 (brida) a 12 (alma y mandibula): la cara -Y del alma queda en el aire y pide soporte.",
              "- Casquillos: las puntas de la C se recortan con un plano en x para dejar un espesor radial de "
              f"MIN_WALL + {BUSHING_TIP_MARGIN} (antes eran cuñas de 0.2 mm); la boca sigue siendo varilla + {BUSHING_ROD_CLR}.",
              "- Perilla: se monta invertida (el perno sale por la cara que mira a la brida); imprimir con esa cara sobre la cama.",
              "", "## Avisos", ""] + ([f"- {w}" for w in warns] if warns else ["- ninguno"])
    lines += ["", "## Chequeos que fallaron", ""] + ([f"- {f}" for f in fails] if fails else ["- ninguno"])
    lines += ["", "## Params que faltan (constantes de modulo en gancho.py)", "",
              f"- `KNOB_FREE_EXTRA` = {KNOB_FREE_EXTRA}", f"- `KNOB_WEB_GAP` = {KNOB_WEB_GAP}",
              f"- `KNOB_FLANGE_GAP` = {KNOB_FLANGE_GAP}", f"- `BUSHING_TIP_MARGIN` = {BUSHING_TIP_MARGIN}",
              f"- `WEB_OVERLAP` = {WEB_OVERLAP}"]
    (HERE / "reporte_gancho.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
