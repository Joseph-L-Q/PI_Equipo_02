"""Fase A (revision 28/10): layout of the central box. Builds the 1-floor and 2-floor layouts, M1/M2
(preliminary), M11, the dummies, the cable chamber (M3_riel_central) and the ballast plates; runs the checks;
computes mass / sealed air / buoyancy / plates per ring; picks the layout with less sealed air; writes
cad_final/reporte_fase_a.md and the renders.

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
import camara as CH  # noqa: E402
import layout as LY  # noqa: E402
import params as P  # noqa: E402
from checks import brep_check, sanitize  # noqa: E402
from render import render  # noqa: E402

MOD = HERE.parent
OUT = MOD / "salida" / "faseA"
OUT.mkdir(parents=True, exist_ok=True)

LABEL = {"esp32": "ESP32-S3 DevKitC-1", "kit_a": "KIT A", "xy017": "XY-017 RS-485", "microsd": "microSD SPI",
         "mpu6050": "MPU-6050", "hw517_1": "HW-517 #1", "hw517_2": "HW-517 #2"}
RHO_W = P.SEAWATER_DENSITY
NET_STEEL = 1 - RHO_W / P.STEEL_DENSITY          # net sinking per gram of steel


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


def r1(t):
    return fmt(tuple(round(x, 1) for x in t))


def mass_g(shape, infill):
    """PETG mass with SHELL_T solid skin and `infill` inside (skin volume = area x SHELL_T, capped at V)."""
    V = shape.Volume()
    shell = min(V, shape.Area() * P.SHELL_T)
    return P.PETG_DENSITY * (shell + infill * (V - shell)) / 1000.0


def solid_g(shape):
    """Sealed pieces and rail tramos: printed at INFILL_SEALED (100 %)."""
    return mass_g(shape, P.INFILL_SEALED)


def vol(a, b):
    try:
        return a.intersect(b).Volume()
    except Exception:
        return float("nan")


# ------------------------------------------------------------------ box
def analyse_box(lay):
    m1 = sanitize(C.box_body(lay))
    m2 = sanitize(C.box_lid(lay))
    trays = {k: sanitize(v) for k, v in C.trays(lay).items()}
    dummies = C.module_dummies(lay)
    checks = {"M1_caja_cuerpo (preliminar)": brep_check(m1), "M2_caja_tapa (preliminar)": brep_check(m2)}
    for k, t in trays.items():
        checks[k] = brep_check(t)
    filled = m1.fuse(C.cavity_tool(lay).val()).clean()
    nuts = C.gland_nuts(lay)
    v_air = (filled.Volume() - m1.Volume() - sum(t.Volume() for t in trays.values())
             - sum(d.val().Volume() for _, d in dummies) - sum(n.val().Volume() for n in nuts)) / 1000.0
    return dict(lay=lay, m1=m1, m2=m2, trays=trays, dummies=dummies, checks=checks, filled=filled, nuts=nuts,
                v_air=v_air, v_disp=(filled.Volume() + m2.Volume()) / 1000.0,
                fixed_g=sum(P.COMPONENTS[key][3] for _, key, _ in lay.modules)
                + 3 * P.GLAND_MASS_G + P.BOX_HARDWARE_G + P.BOX_WIRING_G)


# ------------------------------------------------------------------ node balance with plates
A_EXT = P.RAIL_SECTION ** 2 - (P.RAIL_SECTION - 2 * P.RAIL_WALL) ** 2     # extension section, mm2 (old layout)


def outer_rail_cm3(lay, n):
    """PETG volume of the rail pieces outboard of the central, both sides (CAD volumes of riel.py)."""
    import riel
    if not riel.PASO_100:
        return A_EXT * 2 * n * P.RAIL_EXT_L / 1000.0
    c = CH.dims(lay)
    if "v" not in outer_rail_cm3.__dict__:
        outer_rail_cm3.v = (riel.ext(c).val().Volume() / 1000.0, riel.punta(c).val().Volume() / 1000.0)
    v_ext, v_tip = outer_rail_cm3.v
    return 2 * (n * v_ext + v_tip)


def node_rows(an, f, layers):
    """Per ring: node without plates, then the number of plates (pairs) that lands the apparent weight in the
    target window. The chamber is built with `layers` plates per side of pocket."""
    lay = an["lay"]
    ch = {k: sanitize(v) for k, v in CH.chamber_solid(lay, layers).items()}
    ch_g = sum(solid_g(s) for s in ch.values())
    ch_v = sum(s.Volume() for s in ch.values()) / 1000.0
    box_g = solid_g(an["m1"]) + solid_g(an["m2"]) + sum(mass_g(t, f) for t in an["trays"].values()) + an["fixed_g"]
    plate_g = CH.plate_mass_g()
    rows = []
    for D in P.RING_DIAMETERS:
        n = P.RAIL_EXT_PER_RING[D]
        v_ext = outer_rail_cm3(lay, n)
        ext_g = P.PETG_DENSITY * P.INFILL_SEALED * v_ext
        cap_g = 2 * (P.CAPSULE_SET_G + P.CAPSULE_CONTENT_G)
        rod = rod_g(n)
        node_g = box_g + ch_g + ext_g + cap_g + P.OTHER_NODE_G + rod
        disp = (an["v_disp"] + ch_v + v_ext + 2 * P.CAPSULE_SET_DISP_CM3 + P.OTHER_NODE_G / P.PETG_DENSITY
                + rod / P.STEEL_DENSITY)
        app0 = node_g - RHO_W * disp
        lo, hi = (t * 1000 for t in P.BALLAST_TARGET_KGF)
        k = 0
        while app0 + k * P.PLATE_SIDES * plate_g * NET_STEEL < lo:
            k += 1
        app = app0 + k * P.PLATE_SIDES * plate_g * NET_STEEL
        rows.append(dict(D=D, n=n, L=2 * rail_tip(n), rod_g=rod, node_g=node_g, disp=disp, app0=app0,
                         layers=k, steel_g=k * P.PLATE_SIDES * plate_g, app=app, in_window=lo <= app <= hi,
                         total=node_g + k * P.PLATE_SIDES * plate_g,
                         need_g=max(0.0, (lo - app0) / NET_STEEL), need_hi_g=max(0.0, (hi - app0) / NET_STEEL)))
    return dict(f=f, layers=layers, ch=ch, ch_g=ch_g, ch_v=ch_v, box_g=box_g,
                box_app=box_g - RHO_W * an["v_disp"], rows=rows)


def rail_tip(n):
    import riel
    return riel.tip_x(n)


def rod_g(n):
    """M8 rod with its 2 wide washers and 2 nuts (C19), steel."""
    import riel
    if not P.RAIL_ROD_M8:
        return 0.0
    m = P.ROD_PARTS_G
    return riel.rod_length(n) * m["g_por_mm"] + 2 * (m["tuerca"] + m["arandela"])


def balance(an, f):
    """Pocket sized for the ring that needs the most plates; iterate because the pocket changes the chamber."""
    layers = 1
    for _ in range(6):
        res = node_rows(an, f, layers)
        need = max(r["layers"] for r in res["rows"])
        if need <= layers:
            return res
        layers = need
    raise SystemExit("plate pocket sizing did not converge")


def capsule_z(lay, tilt=0.0):
    """z of the capsule centre (mass and volume, taken equal) in the box frame, carriage geometry of capsula.py."""
    import capsula as CP
    _, _, _, _, _, x0, x_front = CP.cap_dims()
    xc = (x0 + x_front) / 2
    return CH.dims(lay).z_rail + CP.carriage_axis()[1] - xc * math.sin(math.radians(tilt))


def stability(an, res, D, tilt=0.0):
    """Centre of mass and centre of buoyancy (z) of the whole node with its plates, approximate. Capsules at their real
    height (hinge below the rail, tilt in degrees); extensions and other parts at rail mid-height."""
    lay = an["lay"]
    row = next(r for r in res["rows"] if r["D"] == D)
    c = CH.dims(lay)
    z_rail_c = c.z_rail + P.RAIL_SECTION / 2
    f = res["f"]
    z_cap = capsule_z(lay, tilt)
    mass = [(an["m1"].Center().z, solid_g(an["m1"])), (an["m2"].Center().z, solid_g(an["m2"]))]
    mass += [(t.Center().z, mass_g(t, f)) for t in an["trays"].values()]
    mass += [((b.z[0] + b.z[1]) / 2, P.COMPONENTS[key][3]) for _, key, b in lay.modules]
    mass.append((P.BOX_FLOOR + lay.cav[2] / 2, an["fixed_g"] - sum(P.COMPONENTS[k][3] for _, k, _ in lay.modules)))
    mass += [(s.Center().z, solid_g(s)) for s in res["ch"].values()]
    mass.append((z_cap, 2 * (P.CAPSULE_SET_G + P.CAPSULE_CONTENT_G)))
    rest_g = row["node_g"] - sum(m for _, m in mass)            # extensions and other parts at rail level
    mass.append((z_rail_c, rest_g))
    plates = CH.plates_solid(lay, row["layers"])                # steel is not in node_g: added on top
    mass += [(pl.val().Center().z, CH.plate_mass_g()) for pl in plates]
    buoy = [(an["filled"].Center().z, an["filled"].Volume() / 1000), (an["m2"].Center().z, an["m2"].Volume() / 1000)]
    buoy += [(s.Center().z, s.Volume() / 1000) for s in res["ch"].values()]
    buoy += [(pl.val().Center().z, pl.val().Volume() / 1000) for pl in plates]
    buoy.append((z_cap, 2 * P.CAPSULE_SET_DISP_CM3))
    rest_v = row["disp"] - sum(v for _, v in buoy) + row["steel_g"] / P.STEEL_DENSITY
    buoy.append((z_rail_c, rest_v))
    zg = sum(z * m for z, m in mass) / sum(m for _, m in mass)
    zb = sum(z * v for z, v in buoy) / sum(v for _, v in buoy)
    return zg, zb


# ------------------------------------------------------------------ cable path solid (render)
def cable_solids(lay):
    c = CH.dims(lay)
    R, dl = c.bend_r, P.PG7_DOME[1]
    out = []
    for gx, _ in lay.floor_glands:
        s = 1 if gx > 0 else -1
        x0 = gx
        arc = cq.Edge.makeThreePointArc(cq.Vector(x0, 0, -dl),
                                        cq.Vector(x0 + s * R * (1 - math.cos(math.pi / 4)), 0, -dl - R * math.sin(math.pi / 4)),
                                        cq.Vector(x0 + s * R, 0, -dl - R))
        line = cq.Edge.makeLine(cq.Vector(x0 + s * R, 0, -dl - R), cq.Vector(s * P.RAIL_CENTRAL_L / 2, 0, -dl - R))
        up = cq.Edge.makeLine(cq.Vector(x0, 0, P.BOX_FLOOR + 5), cq.Vector(x0, 0, -dl))
        path = cq.Wire.assembleEdges([up, arc, line])
        prof = cq.Workplane("XY").workplane(offset=P.BOX_FLOOR + 5).center(x0, 0).circle(P.CAT5E_D / 2)
        try:
            out.append(prof.sweep(cq.Workplane().add(path), transition="round"))
        except Exception:
            pass
    return out


def main():
    cands = LY.candidates()
    an_all = {}
    for fl, lay in cands.items():
        s = LY.summary(lay)
        if s["conflictos"] or s["fuera_de_cavidad"] or None in s["modulo_en_bandeja"].values():
            print(f"layout {fl} floors rejected: {s['conflictos']} {s['fuera_de_cavidad']}")
            continue
        an = analyse_box(lay)
        if not all(c["ok"] for k, c in an["checks"].items() if k.startswith("M11")):
            print(f"layout {fl} floors: tray B-rep check failed")
            continue
        an["summary"] = s
        an["bal"] = {f: balance(an, f) for f in P.INFILL_CASES}
        an_all[fl] = an
    if not an_all:
        raise SystemExit("no valid layout")
    chosen = min(an_all, key=lambda k: an_all[k]["v_air"])
    an = an_all[chosen]
    lay, s = an["lay"], an["summary"]
    kit = {fl: LY.summary(LY.build("kit_a", floors=fl)) for fl in (1, 2)}
    cdim = CH.dims(lay)
    if not cdim.checks["ok"]:
        raise SystemExit(f"chamber cable check failed: {cdim.checks}")

    # checks of the chamber and covers at the pocket depth actually used
    bal40 = an["bal"][P.INFILL_CASES[0]]
    for k, v in bal40["ch"].items():
        an["checks"][f"{k} (referencia)"] = brep_check(v)
    inter = []
    trays = an["trays"]
    for name, d in an["dummies"]:
        dv = d.val()
        inter.append((LABEL[name], vol(dv, an["m1"]), min(vol(dv, t) for t in trays.values())))
    for k, t in trays.items():
        inter.append((f"{k} ↔ M1", vol(t, an["m1"]), float("nan")))
    inter.append(("M3_riel_central ↔ M1", vol(bal40["ch"]["M3_riel_central"], an["m1"]), float("nan")))

    stab = {D: stability(an, an["bal"][f], D) for f in P.INFILL_CASES[:1] for D in (min(P.RING_DIAMETERS), max(P.RING_DIAMETERS))}

    # ---------------------------------------------------------------- renders
    m1, m2 = an["m1"], an["m2"]
    zones = C.keepout_solids(lay)
    zone_items = [(z, "#F4D03F" if k == "cable" else "#5DADE2", 0.16 if k == "cable" else 0.13, False, None)
                  for _, k, z in zones]
    tray_items = [(t, "#5D6D7E", 1.0, True, None) for t in trays.values()]
    mod_items = [(d, "#117A65" if n.startswith("esp32") else "#1E8449", 1.0, True, LABEL[n]) for n, d in an["dummies"]]
    nut_items = [(n, "#7F8C8D", 1.0, True, None) for n in an["nuts"]]
    ch = bal40["ch"]["M3_riel_central"]
    covers = [v for k, v in bal40["ch"].items() if k.startswith("tapa")]
    plates = CH.plates_solid(lay, bal40["rows"][0]["layers"])
    exts = CH.extension_solid(1, cdim)
    cables = cable_solids(lay)
    render(tray_items + mod_items + nut_items[:2] + zone_items, OUT / "faseA_bandeja_iso.png", "iso",
           f"M11 bandeja ({chosen} piso{'s' if chosen > 1 else ''}) con módulos dummy. Amarillo: cables. Azul: acceso")
    lid_up = m2.moved(cq.Location(cq.Vector(0, 0, 140)))
    render([(m1, "#C0392B", 1.0, True, "M1 caja (preliminar)"), (lid_up, "#C9CCD1", 0.35, True, "M2 tapa"),
            (ch, "#2B2B2E", 0.85, True, "M3_riel_central (cámara)")] + [(e, "#2B2B2E", 0.4, True, None) for e in exts]
           + tray_items + mod_items + nut_items, OUT / "faseA_caja_abierta_iso.png", "iso_alto",
           "Caja central abierta (tapa levantada 140 mm) sobre la cámara de cables")
    render([(m1, "#C0392B", 1.0, True, None)] + tray_items + mod_items + nut_items + zone_items,
           OUT / "faseA_caja_superior.png", "superior", "Vista superior: layout y zonas libres")
    render([(m1, "#C0392B", 1.0, True, None), (ch, "#2B2B2E", 1.0, True, "cámara + bolsillos de pletina")]
           + [(p, "#A6ACAF", 1.0, True, None) for p in plates],
           OUT / "faseA_caja_bajo.png", "iso_bajo", "Fondo: cámara de cables, 4 M4 y pletinas de inox (tapas quitadas)")
    half = cq.Workplane("XY").box(400, 200, 400).translate((0, -100, 0))   # keep y > 0, seen from -Y
    cut_items = ([(m1.cut(half.val()), "#C0392B", 1.0, True, None), (ch.cut(half.val()), "#2B2B2E", 1.0, True, None)]
           + [(e.cut(half), "#2B2B2E", 0.6, True, None) for e in exts]
           + [(cb, "#E67E22", 1.0, False, "Cat5e R25") for cb in cables[:1]] + [(cb, "#E67E22", 1.0, False, None) for cb in cables[1:]]
           + [(cv.cut(half.val()), "#5D6D7E", 1.0, True, None) for cv in covers]
           + [(p.cut(half), "#A6ACAF", 1.0, True, None) for p in plates])
    cut_items = [it for it in cut_items if (it[0].val() if hasattr(it[0], "val") else it[0]).Volume() > 1e-3]
    render(cut_items, OUT / "faseA_camara_corte.png", "frontal", "Corte en y = 0: el cable baja del domo y dobla con R25 al conducto")
    other = next((a for k, a in an_all.items() if k != chosen), None)
    if other:
        ol = other["lay"]
        render([(t, "#5D6D7E", 1.0, True, None) for t in other["trays"].values()]
               + [(d, "#1E8449", 1.0, True, LABEL[n]) for n, d in other["dummies"]]
               + [(z, "#F4D03F" if k == "cable" else "#5DADE2", 0.14, False, None) for _, k, z in C.keepout_solids(ol)],
               OUT / f"faseA_variante_{ol.floors}pisos_iso.png", "iso",
               f"Variante descartada: {ol.floors} piso{'s' if ol.floors > 1 else ''} (más aire sellado)")

    # ---------------------------------------------------------------- report
    L, W, H = s["cavidad"]
    r = ["# Reporte Fase A, layout de la caja central (generado por `fase_a.py`, revisión 28/10)", "",
         "No editar a mano: se regenera. mm, cm³, g. Todo valor `estimado` sigue por verificar.", "",
         "## 1. Parámetros (`cad_final/params.py`)", "",
         "| Parámetro | Anterior | Nuevo | Razón | Origen | Estado |", "|---|---|---|---|---|---|"]
    for prm in P.REGISTRO.values():
        r.append(f"| `{prm.key}` | {fmt(prm.anterior) or 'nuevo'} | {fmt(prm.value)} | {prm.razon} | "
                 f"{prm.origen} | {prm.estado} |")
    r += ["", "## 2. 1 piso contra 2 pisos (holgura de contratuerca 5 mm, relleno de bandeja 40 %)", "",
          "| Concepto | " + " | ".join(f"{k} piso{'s' if k > 1 else ''}" for k in an_all) + " |",
          "|---|" + "---|" * len(an_all)]

    def rowc(name, fn):
        r.append(f"| {name} | " + " | ".join(fn(a) for a in an_all.values()) + " |")
    rowc("Cavidad", lambda a: r1(a["summary"]["cavidad"]))
    rowc("Caja con brida y tapa", lambda a: r1(a["summary"]["caja_con_brida"]))
    rowc("Volumen de la cavidad cm³", lambda a: f"{math.prod(a['summary']['cavidad']) / 1000:.0f}")
    rowc("**Aire sellado cm³**", lambda a: f"**{a['v_air']:.0f}**")
    rowc("Desplaza la caja (cuerpo cerrado + tapa) cm³", lambda a: f"{a['v_disp']:.0f}")
    rowc("Empuje de la caja g", lambda a: f"{RHO_W * a['v_disp']:.0f}")
    rowc("Caja en aire g (M1+M2 al 100 %, bandejas 40 %, electrónica)", lambda a: f"{a['bal'][0.4]['box_g']:.0f}")
    rowc("Peso aparente de la caja sola g (+ hunde)", lambda a: f"{a['bal'][0.4]['box_app']:+.0f}")
    rowc("Pletinas por lado (Ø100 / Ø500)", lambda a: f"{a['bal'][0.4]['rows'][0]['layers']} / {a['bal'][0.4]['rows'][-1]['layers']}")
    rowc("Bandejas", lambda a: fmt({k: r1(v) for k, v in a["summary"]["bandejas"].items()}))
    rowc("Choques", lambda a: str(len(a["summary"]["conflictos"])))
    r += ["", f"**Elegido: {chosen} piso{'s' if chosen > 1 else ''}** (menor aire sellado). "
          "La variante descartada queda a un switch: `caja.pisos` = 1 o 2 en `params.py`.", ""]
    ox, oy, oz = s["caja_exterior"]
    r += ["## 3. Caja elegida (derivada del layout)", "",
          "| Concepto | sin_base (por defecto) | kit_a 1 piso | kit_a 2 pisos |", "|---|---|---|---|",
          f"| Cavidad | {r1(s['cavidad'])} | {r1(kit[1]['cavidad'])} | {r1(kit[2]['cavidad'])} |",
          f"| Exterior del cuerpo | {r1(s['caja_exterior'])} | {r1(kit[1]['caja_exterior'])} | {r1(kit[2]['caja_exterior'])} |",
          f"| Con brida y tapa | {r1(s['caja_con_brida'])} | {r1(kit[1]['caja_con_brida'])} | {r1(kit[2]['caja_con_brida'])} |",
          f"| Cabe en cama {fmt(P.PRINT_BED)} | {'sí' if s['cabe_en_cama'] else 'NO'} | {'sí' if kit[1]['cabe_en_cama'] else 'NO'} | {'sí' if kit[2]['cabe_en_cama'] else 'NO'} |",
          f"| Bandejas ≤ {P.PIECE_MAX_L:g} | {'sí' if s['bandejas_ok_150'] else 'NO'} | {'sí' if kit[1]['bandejas_ok_150'] else 'NO'} | {'sí' if kit[2]['bandejas_ok_150'] else 'NO'} |",
          f"| Choques | {len(s['conflictos'])} | {len(kit[1]['conflictos'])} | {len(kit[2]['conflictos'])} |", "",
          f"Prensaestopas del fondo en x = ±{lay.floor_glands[0][0]:.2f}, y = 0. Agujero de la bandeja sobre cada "
          f"contratuerca: radio {lay.access_r:.2f} (esquina {P.nut_corner_r():.2f} + {P.CLR_NUT:g}); se aprietan con "
          "la caja vacía. Umbilical: "
          + (f"en la tapa en {r1(lay.lid_gland)}." if lay.lid_gland else
             f"en la pared -X, y = {lay.wall_gland[1]:g}, z = {lay.wall_gland[2]:.1f} (en la tapa la contratuerca chocaba)."),
          "", "| Módulo | Cuerpo x0, x1, y0, y1, z0, z1 | Bandeja |", "|---|---|---|"]
    for n, k, b in lay.modules:
        r.append(f"| {LABEL[n]} | {', '.join(f'{v:.1f}' for v in (*b.xy, *b.z))} | {s['modulo_en_bandeja'][n]} |")
    r += ["", "## 4. Cámara de cables (M3_riel_central, C12)", "",
          "| Concepto | Valor |", "|---|---|",
          f"| Radio de curvatura usado | {cdim.bend_r:g} (máx de {P.CABLE_BEND_K:g} × Ø{P.CAT5E_D:g} y {P.CABLE_BEND_R_MIN:g}) |",
          f"| Alto interior (domo {P.PG7_DOME[1]:g} + radio {cdim.bend_r:g} + medio cable {P.CAT5E_D / 2:g} + nervio {P.RAIL_TSLOT['alto']:g}) | {cdim.h_int:.1f} |",
          f"| Fondo del riel bajo la caja | z = {cdim.z_rail:.1f} (el tramo cuelga {-cdim.z_rail:.1f} bajo el fondo de la caja) |",
          f"| Conducto de 22 | z {cdim.z_floor:.1f} a {cdim.z_conduit_top:.1f}; el cable corre a z = {cdim.z_cable:.1f} |",
          f"| Zona abierta bajo la caja | |x| ≤ {cdim.x_high:.1f}; rampa a {P.CHAMBER_RAMP_DEG:g}° hasta |x| = {cdim.x_joint:g} (empieza la unión) |",
          f"| Brida superior | {P.RAIL_CENTRAL_L:g} × {cdim.flange_w:.1f} × {P.CHAMBER_FLANGE_W[1]:g}, con los 4 M4 a la caja en {fmt(P.BASE_M4_PTS)} |",
          f"| Chequeos del recorrido | " + ", ".join(f"{k}: {('sí' if v else 'NO') if isinstance(v, bool) else f'{v:.1f} mm'}" for k, v in cdim.checks.items() if k != 'ok') + " |",
          ""]
    r += ["## 5. Chequeos de sólidos", "", "| Pieza | BRepCheck | BOPAlgo | Sólidos | Arista mín | Cara mín | Resultado |",
          "|---|---|---|---|---|---|---|"]
    for k, c in an["checks"].items():
        r.append(f"| {k} | {'ok' if c['brep'] else 'FALLA'} | {'ok' if c['bop'] else 'FALLA'} | {c['solids']} | "
                 f"{c['min_edge']:.2f} | {c['min_face']:.2f} | {'ok' if c['ok'] else 'FALLA'} |")
    r += ["", "| Par | Interferencia con M1 mm³ | con la bandeja mm³ |", "|---|---|---|"]
    for a, v1, v2 in inter:
        r.append(f"| {a} | {v1:.2f} | {'' if math.isnan(v2) else f'{v2:.2f}'} |")
    plate_g = CH.plate_mass_g()
    r += ["", "## 6. Aire sellado, empuje y lastre (C13)", "",
          f"M1, M2, M4, M5 y los tramos del riel al {P.INFILL_SEALED * 100:.0f} % con {P.SEALED_PERIMETERS} perímetros. "
          "Bandeja y piezas no selladas: 40 % y 100 %.", "",
          "| Concepto | Valor |", "|---|---|",
          f"| Aire sellado (cavidad − bandejas − módulos − contratuercas) | {an['v_air']:.0f} cm³ |",
          f"| Volumen desplazado por la caja | {an['v_disp']:.0f} cm³ → empuje {RHO_W * an['v_disp']:.0f} g |",
          f"| Cámara + tapas de bolsillo (100 %) | {bal40['ch_v']:.0f} cm³, {bal40['ch_g']:.0f} g |",
          f"| Electrónica + 3 PG7 + tornillería + cables (estimado) | {an['fixed_g']:.0f} g |",
          f"| Pletina de inox {fmt(P.PLATE_BAR)} × {P.PLATE_L:g} | {plate_g:.0f} g cada una, hunde {plate_g * NET_STEEL:.0f} g; "
          f"se ponen de a {P.PLATE_SIDES} (una por lado) |",
          f"| Bolsillos (uno por lado, fuera del sello, "
          f"{'pegados a la cámara al nivel del fondo del riel' if P.PLATE_LEVEL == 'abajo' else 'colgados de la brida'}) | "
          f"{bal40['layers']} pletinas por lado, "
          f"{CH.pocket_depth(bal40['layers']):.1f} de hondo |", "",
          f"**Nodo completo** (extensiones y puntas con su volumen CAD al 100 %, {P.OTHER_NODE_G:g} g de "
          "ganchos/carros/perillas sin modelar; la varilla M8 obligatoria (C19) ya está dentro y es lastre: las pletinas se "
          "cuentan con ella). Objetivo: "
          f"{P.BALLAST_TARGET_KGF[0]:g} a {P.BALLAST_TARGET_KGF[1]:g} kgf hacia abajo:", "",
          "| Relleno bandeja | Aro | Riel mm | Varilla M8 con tuercas g | Nodo sin pletinas g | Desplaza cm³ | Peso aparente sin lastre g | "
          "Acero para la ventana g | Pletinas por lado | Peso aparente final g | Total en aire g |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for f, b in an["bal"].items():
        for row in b["rows"]:
            r.append(f"| {f * 100:.0f} % | Ø{row['D']:g} | {row['L']:g} | {row['rod_g']:.0f} | {row['node_g']:.0f} | {row['disp']:.0f} | "
                     f"{row['app0']:+.0f} | {row['need_g']:.0f} a {row['need_hi_g']:.0f} | {row['layers']} | "
                     f"{row['app']:+.0f}{'' if row['in_window'] else ' (fuera de la ventana)'} | {row['total']:.0f} |")
    r += ["", "Estabilidad del nodo completo (aproximada; bandeja al 40 %, cápsulas a 0° con el eje bajo el riel, extensiones a media altura del riel):", ""]
    for D, (zg, zb) in stab.items():
        r.append(f"- Ø{D:g}: centro de masa z = {zg:.1f}, centro de empuje z = {zb:.1f} → "
                 f"{'el de masa queda {:.1f} mm debajo: no se voltea'.format(zb - zg) if zg < zb else 'centro de masa ARRIBA del de empuje: revisar'}.")
    r += ["", "El cálculo completo (momentos, metacentro) es la Fase E.", ""]
    (HERE / "reporte_fase_a.md").write_text("\n".join(r), encoding="utf-8")
    print("written reporte_fase_a.md; chosen floors:", chosen)
    for k, a in an_all.items():
        b = a["bal"][0.4]
        print(k, "cav", r1(a["summary"]["cavidad"]), "flange", r1(a["summary"]["caja_con_brida"]), "air", round(a["v_air"]),
              "disp", round(a["v_disp"]), "box_app", round(b["box_app"]),
              [(row["D"], round(row["app0"]), row["layers"], round(row["app"]), round(row["total"])) for row in b["rows"]])
    print({k: c["ok"] for k, c in an["checks"].items()})
    print("chamber", cdim.checks, "stab", stab)


if __name__ == "__main__":
    main()
