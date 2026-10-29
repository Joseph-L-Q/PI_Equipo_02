"""Fase A: layout of the central box. Builds M1/M2 (preliminary), M11 and the dummies, runs the checks,
computes mass / sealed air / buoyancy / ballast, writes cad_final/reporte_fase_a.md and the renders.

    python fase_a.py            (from cad_final/)
Outputs: cad_final/reporte_fase_a.md, salida/faseA/*.png
"""
import math
import sys
from pathlib import Path

import cadquery as cq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import caja_central as C  # noqa: E402
import layout as LY  # noqa: E402
import params as P  # noqa: E402
from checks import brep_check, sanitize  # noqa: E402
from render import render  # noqa: E402

MOD = HERE.parent
OUT = MOD / "salida" / "faseA"
OUT.mkdir(parents=True, exist_ok=True)

LABEL = {"esp32": "ESP32-S3 DevKitC-1", "kit_a": "KIT A", "xy017": "XY-017 RS-485", "microsd": "microSD SPI",
         "mpu6050": "MPU-6050", "hw517_1": "HW-517 #1", "hw517_2": "HW-517 #2"}


def fmt(v):
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, tuple) and all(isinstance(x, (int, float)) for x in v):
        return " × ".join(f"{x:g}" for x in v)
    if isinstance(v, tuple):
        return "; ".join(fmt(x) for x in v)
    if isinstance(v, dict):
        return ", ".join(f"{k}: {fmt(x)}" for k, x in v.items())
    return "" if v is None else str(v)


def mass_g(shape, infill):
    """PETG mass with SHELL_T solid skin and `infill` inside (skin volume = area x SHELL_T, capped at V)."""
    V = shape.Volume()
    shell = min(V, shape.Area() * P.SHELL_T)
    return P.PETG_DENSITY * (shell + infill * (V - shell)) / 1000.0


def vol(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception:
        return float("nan")


def main():
    lay = LY.build()
    s = LY.summary(lay)
    if s["conflictos"] or s["fuera_de_cavidad"] or None in s["modulo_en_bandeja"].values():
        raise SystemExit(f"layout failed: {s}")
    kit = LY.summary(LY.build("kit_a"))

    # ---------------------------------------------------------------- solids + checks
    m1 = sanitize(C.box_body(lay))
    m2 = sanitize(C.box_lid(lay))
    trays = {k: sanitize(v) for k, v in C.trays(lay).items()}
    dummies = C.module_dummies(lay)
    checks = {"M1_caja_cuerpo (preliminar)": brep_check(m1), "M2_caja_tapa (preliminar)": brep_check(m2)}
    for k, t in trays.items():
        checks[k] = brep_check(t)
    if not all(c["ok"] for k, c in checks.items() if k.startswith("M11")):
        raise SystemExit(f"tray B-rep check failed: {checks}")
    inter = []
    for name, d in dummies:
        dv = d.val()
        inter.append((LABEL[name], vol(dv, m1), min(vol(dv, t) for t in trays.values())))
    for k, t in trays.items():
        inter.append((f"{k} ↔ M1", vol(t, m1), float("nan")))

    # ---------------------------------------------------------------- volumes, mass, buoyancy (box only)
    filled = m1.fuse(C.cavity_tool(lay).val()).clean()
    v_filled = filled.Volume() / 1000.0                     # cm3, body + sealed cavity (pockets flood)
    v_m1, v_m2 = m1.Volume() / 1000.0, m2.Volume() / 1000.0
    v_tray = sum(t.Volume() for t in trays.values()) / 1000.0
    v_mod = sum(d.val().Volume() for _, d in dummies) / 1000.0
    v_nuts = sum(n.val().Volume() for n in C.gland_nuts(lay)) / 1000.0
    v_air = v_filled - v_m1 - v_tray - v_mod - v_nuts
    v_disp = v_filled + v_m2
    comp_g = sum(P.COMPONENTS[key][3] for _, key, _ in lay.modules)
    fixed_g = comp_g + 3 * P.GLAND_MASS_G + P.BOX_HARDWARE_G + P.BOX_WIRING_G
    pocket_cm3 = C.pocket_volume_cm3(lay)
    k_ballast = 1 - P.SEAWATER_DENSITY / P.STEEL_DENSITY       # net sinking per gram of steel

    cases = []
    for f in P.INFILL_CASES:
        pet = mass_g(m1, f) + mass_g(m2, f) + sum(mass_g(t, f) for t in trays.values())
        box_g = pet + fixed_g
        box_app = box_g - P.SEAWATER_DENSITY * v_disp        # g, + = sinks
        # whole node, PRELIMINARY: rail by section, old capsules, other parts lumped
        f_eff = (mass_g(m1, f) / (P.PETG_DENSITY * v_m1))     # skin + infill fraction seen on M1
        a_rail = P.RAIL_SECTION ** 2 - (P.RAIL_SECTION - 2 * P.RAIL_WALL) ** 2
        rows = []
        for D in P.RING_DIAMETERS:
            n = P.RAIL_EXT_PER_RING[D]
            L = P.RAIL_CENTRAL_L + 2 * n * P.RAIL_EXT_L
            v_rail = a_rail * L / 1000.0
            rail_g = P.PETG_DENSITY * v_rail * max(f_eff, f)
            cap_g = 2 * (P.CAPSULE_SET_G * max(f_eff, f) + P.CAPSULE_CONTENT_G)
            node_g = box_g + rail_g + cap_g + P.OTHER_NODE_G
            node_disp = v_disp + v_rail + 2 * P.CAPSULE_SET_DISP_CM3 + P.OTHER_NODE_G / P.PETG_DENSITY
            app = node_g - P.SEAWATER_DENSITY * node_disp
            ball = [(t * 1000 - app) / k_ballast for t in P.BALLAST_TARGET_KGF]
            rows.append(dict(D=D, n=n, L=L, node_g=node_g, disp=node_disp, app=app, ball=ball,
                             total=[node_g + b for b in ball]))
        cases.append(dict(f=f, pet=pet, box_g=box_g, box_app=box_app, rows=rows))

    # rough upright check of the box: centre of mass vs centre of buoyancy (z)
    cob_z = filled.Center().z
    parts_cm = [(m1.Center().z, mass_g(m1, 1.0)), (m2.Center().z, mass_g(m2, 1.0))]
    parts_cm += [(t.Center().z, mass_g(t, 1.0)) for t in trays.values()]
    parts_cm += [((b.z[0] + b.z[1]) / 2, P.COMPONENTS[key][3]) for _, key, b in lay.modules]
    ball_mid = cases[-1]["rows"][-1]["ball"][0]
    parts_cm.append((-P.POCKET_DEPTH / 2, ball_mid))
    com_z = sum(z * m for z, m in parts_cm) / sum(m for _, m in parts_cm)

    # ---------------------------------------------------------------- renders
    zones = C.keepout_solids(lay)
    zone_items = [(z, "#F4D03F" if k == "cable" else "#5DADE2", 0.16 if k == "cable" else 0.13, False, None)
                  for _, k, z in zones]
    tray_items = [(t, "#5D6D7E", 1.0, True, None) for t in trays.values()]
    mod_items = [(d, "#117A65" if n.startswith("esp32") else "#1E8449", 1.0, True, LABEL[n]) for n, d in dummies]
    nut_items = [(n, "#7F8C8D", 1.0, True, None) for n in C.gland_nuts(lay)]
    render(tray_items + mod_items + nut_items[:2] + zone_items, OUT / "faseA_bandeja_iso.png", "iso",
           "M11 bandeja (der/izq) con modulos dummy. Amarillo: cables. Azul: acceso")
    lid_up = m2.moved(cq.Location(cq.Vector(0, 0, 140)))
    rail = C.rail_reference()
    render([(m1, "#C0392B", 1.0, True, "M1 caja (preliminar)"), (lid_up, "#C9CCD1", 0.35, True, "M2 tapa"),
            (rail, "#2B2B2E", 0.5, True, "riel central (referencia)")] + tray_items + mod_items + nut_items,
           OUT / "faseA_caja_abierta_iso.png", "iso_alto", "Caja central abierta, tapa levantada 140 mm")
    render([(m1, "#C0392B", 1.0, True, None)] + tray_items + mod_items + nut_items + zone_items,
           OUT / "faseA_caja_superior.png", "superior", "Vista superior: layout y zonas libres")
    render([(m1, "#C0392B", 1.0, True, "bolsillos de lastre")],
           OUT / "faseA_caja_bajo.png", "iso_bajo", "Fondo: 2 PG7, 4 insertos M4 y bolsillos de lastre")

    # ---------------------------------------------------------------- report
    L, W, H = s["cavidad"]
    r = ["# Reporte Fase A, layout de la caja central (generado por `fase_a.py`)", "",
         "No editar a mano: se regenera. mm, cm³, g. Todo valor `estimado` sigue por verificar.", "",
         "## 1. Parámetros (`cad_final/params.py`)", "",
         "| Parámetro | Anterior | Nuevo | Razón | Origen | Estado |", "|---|---|---|---|---|---|"]
    for prm in P.REGISTRO.values():
        r.append(f"| `{prm.key}` | {fmt(prm.anterior) or 'nuevo'} | {fmt(prm.value)} | {prm.razon} | "
                 f"{prm.origen} | {prm.estado} |")
    ox, oy, oz = s["caja_exterior"]
    fx, fy, fz = s["caja_con_brida"]
    r += ["", "## 2. Caja resultante (derivada del layout)", "",
          "| Concepto | sin_base (por defecto) | kit_a (alternativa) |", "|---|---|---|",
          f"| Cavidad | {fmt(tuple(round(x, 1) for x in s['cavidad']))} | {fmt(tuple(round(x, 1) for x in kit['cavidad']))} |",
          f"| Exterior del cuerpo | {fmt(tuple(round(x, 1) for x in s['caja_exterior']))} | {fmt(tuple(round(x, 1) for x in kit['caja_exterior']))} |",
          f"| Con brida y tapa (lo que va a la cama) | {fmt(tuple(round(x, 1) for x in s['caja_con_brida']))} | {fmt(tuple(round(x, 1) for x in kit['caja_con_brida']))} |",
          f"| Cabe en cama {fmt(P.PRINT_BED)} | {'sí' if s['cabe_en_cama'] else 'NO'} | {'sí' if kit['cabe_en_cama'] else 'NO'} |",
          f"| Bandejas | {fmt({k: fmt(tuple(round(x, 1) for x in v)) for k, v in s['bandejas'].items()})} | {fmt({k: fmt(tuple(round(x, 1) for x in v)) for k, v in kit['bandejas'].items()})} |",
          f"| Bandejas ≤ {P.PIECE_MAX_L:g} | {'sí' if s['bandejas_ok_150'] else 'NO'} | {'sí' if kit['bandejas_ok_150'] else 'NO'} |",
          f"| Choques de cuerpos con zonas | {len(s['conflictos'])} | {len(kit['conflictos'])} |", "",
          f"Prensaestopas del fondo en x = ±{lay.floor_glands[0][0]:.2f}, y = 0 (ventanas del tramo central). "
          f"Zona libre de cada contratuerca: radio {lay.access_r:.2f} (esquina {P.nut_corner_r():.2f} + {P.CLR_NUT:g}). "
          f"Umbilical en la tapa en {fmt(lay.lid_gland)}.", "",
          "| Módulo | Cuerpo x0, x1, y0, y1, z0, z1 | Bandeja |", "|---|---|---|"]
    for n, k, b in lay.modules:
        r.append(f"| {LABEL[n]} | {', '.join(f'{v:.1f}' for v in (*b.xy, *b.z))} | {s['modulo_en_bandeja'][n]} |")
    r += ["", "## 3. Chequeos", "", "| Pieza | BRepCheck | BOPAlgo | Sólidos | Arista mín | Cara mín | Resultado |",
          "|---|---|---|---|---|---|---|"]
    for k, c in checks.items():
        r.append(f"| {k} | {'ok' if c['brep'] else 'FALLA'} | {'ok' if c['bop'] else 'FALLA'} | {c['solids']} | "
                 f"{c['min_edge']:.2f} | {c['min_face']:.2f} | {'ok' if c['ok'] else 'FALLA'} |")
    r += ["", "| Par | Interferencia con M1 mm³ | con la bandeja mm³ |", "|---|---|---|"]
    for a, v1, v2 in inter:
        r.append(f"| {a} | {v1:.2f} | {'' if math.isnan(v2) else f'{v2:.2f}'} |")
    r += ["", "## 4. Aire sellado, empuje y lastre", "",
          "| Concepto | Valor |", "|---|---|",
          f"| Volumen cerrado del cuerpo (PETG + cavidad; los bolsillos se inundan) | {v_filled:.0f} cm³ |",
          f"| Tapa M2 | {v_m2:.0f} cm³ |",
          f"| Volumen desplazado por la caja | {v_disp:.0f} cm³ → empuje {P.SEAWATER_DENSITY * v_disp:.0f} g |",
          f"| Aire sellado (cavidad − bandeja − módulos − contratuercas) | {v_air:.0f} cm³ |",
          f"| Electrónica + 3 PG7 + tornillería + cables (estimado) | {fixed_g:.0f} g |",
          f"| Capacidad de los 2 bolsillos | {pocket_cm3:.0f} cm³ → {pocket_cm3 * P.BALLAST_PACKING['tuercas'] * P.STEEL_DENSITY:.0f} g en tuercas, "
          f"{pocket_cm3 * P.BALLAST_PACKING['barra'] * P.STEEL_DENSITY:.0f} g en barra |",
          f"| Acero: hunde {k_ballast:.3f} g por g | |", "",
          "| Relleno | PETG caja (M1+M2+M11) g | Caja en aire g | Peso aparente de la caja g (+ hunde) |",
          "|---|---|---|---|"]
    for c in cases:
        r.append(f"| {c['f'] * 100:.0f} % | {c['pet']:.0f} | {c['box_g']:.0f} | {c['box_app']:+.0f} |")
    r += ["", "**Nodo completo, PRELIMINAR** (riel por sección, cápsulas P4 rev. B viejas, "
          f"{P.OTHER_NODE_G:g} g de ganchos/carros/perillas sin modelar). Lastre de acero para quedar en "
          f"{P.BALLAST_TARGET_KGF[0]:g} a {P.BALLAST_TARGET_KGF[1]:g} kgf hacia abajo:", "",
          "| Relleno | Aro | Ext/lado | Riel (tramos) mm | Nodo en aire g | Desplaza cm³ | Peso aparente g | Lastre g | Total en aire g |",
          "|---|---|---|---|---|---|---|---|---|"]
    for c in cases:
        for row in c["rows"]:
            r.append(f"| {c['f'] * 100:.0f} % | Ø{row['D']:g} | {row['n']} | {row['L']:g} | {row['node_g']:.0f} | "
                     f"{row['disp']:.0f} | {row['app']:+.0f} | {row['ball'][0]:.0f} a {row['ball'][1]:.0f} | "
                     f"{row['total'][0]:.0f} a {row['total'][1]:.0f} |")
    r += ["", f"Estabilidad de la caja (aproximada, 100 % relleno, lastre {ball_mid:.0f} g en los bolsillos): "
          f"centro de masa z = {com_z:.1f}, centro de empuje z = {cob_z:.1f} → "
          f"{'el centro de masa queda debajo: no se voltea' if com_z < cob_z else 'centro de masa ARRIBA del de empuje: revisar'}. "
          "El cálculo completo con riel y cápsulas es la Fase E.", ""]
    (HERE / "reporte_fase_a.md").write_text("\n".join(r), encoding="utf-8")
    print("written reporte_fase_a.md")
    print({k: c["ok"] for k, c in checks.items()})
    print("cav", s["cavidad"], "flange", s["caja_con_brida"], "air", round(v_air), "disp", round(v_disp))
    for c in cases:
        print(c["f"], round(c["box_g"]), round(c["box_app"]), [(row["D"], round(row["app"]), [round(b) for b in row["ball"]]) for row in c["rows"]])


if __name__ == "__main__":
    main()
