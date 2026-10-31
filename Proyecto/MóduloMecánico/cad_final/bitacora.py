"""Bitacora of the simple prototype: dimensions, weight and cost (node V2, test lantern, our buoy; modular D200 to
compare).

    python bitacora.py          (from cad_final/; or: python build.py --bitacora; run simple.py and boya_simple.py first)
Writes salida/simple/BITACORA.xlsx (copy in Downloads/LanternGuard_simple_para_Drive/) and cad_final/BOM.md from the
same data. Sheets: RESUMEN, PIEZAS, HARDWARE, DISENO, MEDIDAS (the team template filled with what params.py uses today).
The printed mass of each piece is the SAME one the buoyancy uses (simple.py and boya_simple.py): solid skin of
impresion.cascara plus the infill of the piece (relleno_%), written as volume x density x solid fraction. If slicer.py
ran, its grams and hours replace the estimate and are marked "slicer". Inputs in yellow, formulas in black, Arial.
"""
import datetime as dt
import json
import shutil
from pathlib import Path

import cadquery as cq

import params as P

HERE = Path(__file__).resolve().parent
MOD = HERE.parent
SAL = MOD / "salida"
OUT_XLSX = SAL / "simple" / "BITACORA.xlsx"
DRIVE_COPY = Path.home() / "Downloads" / "LanternGuard_simple_para_Drive" / "BITACORA.xlsx"
TEMPLATE = Path.home() / "Downloads" / "LanternGuard_MEDIDAS.xlsx"
TODAY = dt.date.today().isoformat()

QTY_SIMPLE = {"M3s_riel_gancho": 2, "M3t_tapa_bolsillo": 2, "M5s_capsula_tapa_pie": 2, "M4_capsula_cuerpo": 2, "M6_capsula_bisel": 2}
MODULAR = [("M1_caja_cuerpo", 1, "Caja, cuerpo"), ("M2_caja_tapa", 1, "Caja, tapa con asa"), ("M11_bandeja", 1, "Bandeja"),
           ("M3_riel_central", 1, "Riel, tramo central"), ("M3_riel_ext", 2, "Riel, extension"), ("M3_riel_punta", 2, "Riel, punta"),
           ("M3_tapa_bolsillo", 2, "Tapa del bolsillo"), ("M4_capsula_cuerpo", 2, "Capsula, cuerpo"), ("M5_capsula_tapa", 2, "Capsula, tapa con bisagra"),
           ("M6_capsula_bisel", 2, "Bisel"), ("M9_gancho", 2, "Gancho al aro"), ("M10_carro_capsula", 2, "Carro"),
           ("M12_perilla", 4, "Perilla"), ("M13_casquillo_D8", 2, "Casquillo Ø8"), ("M14_pestillo", 2, "Pestillo")]
SLICER_GROUPS = {"nodo P2 robusto": SAL / "prototipos" / "P2_robusto", "nodo P4 estetico": SAL / "prototipos" / "P4_estetico",
                 "boya PET 4 x 1 L": SAL / "boya_pet"}
MODULAR_SEALED = ("M1_", "M2_", "M4_", "M5_", "M3_riel_central", "M3_riel_ext")

# MEDIDAS template name -> (params key, index in the tuple or None, note)
MAP = {"aro.diametro": ("simple.aro_D", None, ""), "aro.seccion": ("aro.seccion", None, ""),
       "linterna.altura": ("linterna.alto", None, "alto de la red de la linterna de referencia"),
       "linterna.pisos": ("linterna.pisos", None, ""),
       "camara.largo": ("camara.envolvente", 0, ""), "camara.ancho": ("camara.envolvente", 1, ""),
       "camara.alto": ("camara.envolvente", 2, ""), "camara.cable_incluido": ("camara.cable_incluido", None, ""),
       "aro_led.exterior": ("aro_led.envolvente", 0, ""), "aro_led.interior": ("aro_led.agujero", None, ""),
       "aro_led.espesor": ("aro_led.envolvente", 1, ""),
       "esp32.largo": ("comp.esp32_devkitc1", 0, ""), "esp32.ancho": ("comp.esp32_devkitc1", 1, ""),
       "esp32.alto_con_headers": ("comp.esp32_devkitc1", 2, ""),
       "pcb_boya.largo": ("boya.pcb", 0, ""), "pcb_boya.ancho": ("boya.pcb", 1, ""),
       "pcb_boya.alto_componentes": ("boya.alto_pcb_conectores", None, ""),
       "portabaterias.largo": ("boya.portabaterias", 0, ""), "portabaterias.ancho": ("boya.portabaterias", 1, ""),
       "portabaterias.alto": ("boya.portabaterias", 2, ""),
       "waveshare.largo": ("boya.waveshare_D", 0, ""), "waveshare.ancho": ("boya.waveshare_D", 1, ""),
       "waveshare.alto": ("boya.waveshare_D", 2, ""),
       "panel.largo": ("boya.panel", 0, ""), "panel.ancho": ("boya.panel", 1, ""), "panel.espesor": ("boya.panel", 2, ""),
       "umbilical.diametro": ("umbilical", 0, ""), "umbilical.longitud": ("umbilical.longitud", None, ""),
       "oring.seccion": ("junta.cordon", None, ""),
       "impresora.modelo": ("impresora.modelo", None, ""), "impresora.cama_x": ("impresora.cama", 0, ""),
       "impresora.cama_y": ("impresora.cama", 1, ""), "impresora.cama_z": ("impresora.cama", 2, ""),
       "impresora.boquilla": ("impresora.boquilla", None, "")}
NOT_IN_CAD = {"camara.agujero_diametro": "el CAD no usa los agujeros de la placa (la camara va calzada en la cavidad)",
              "camara.agujero_distancia": "idem",
              "esp32.lado_usb": "el layout supone el USB en el lado corto u+ (layout.py), no es un parametro",
              "pcb_boya.agujero_diametro": "la boya no fija la PCB por sus agujeros todavia", "pcb_boya.agujero_dist_esquina": "idem",
              "prensaestopas.rosca": "el CAD usa PG7 (pg7.agujero 12.6); anotar la rosca del comprado",
              "prensaestopas.diametro_cable": "el CAD usa el cable de Ø5.5 (cable.cat5e_D), no el rango",
              "oring.diametro_interior": "el CAD usa cordon cortado a medida (junta.cordon), no O-rings cerrados"}


def piece_rows():
    """[(group, stem, qty, description, volume cm3, bbox, orientation, supports, infill text, mass g per piece)]."""
    import fase_a as FA
    from capsula import ORIENTS
    from checks import mesh_checks
    res = json.loads((SAL / "simple" / "resultados.json").read_text(encoding="utf-8"))
    rb = json.loads((SAL / "simple" / "boya" / "resultados_boya.json").read_text(encoding="utf-8"))
    thr = res["soporte_umbral_mm2"]
    rows = []
    for stem, p in res["piezas"].items():
        if stem.startswith("M7"):
            continue
        group = "linterna de prueba" if stem.startswith("LR1") else "nodo simple"
        rel = p["relleno"] if isinstance(p["relleno"], str) else f"{p['relleno'] * 100:.0f} %"
        rows.append((group, stem, QTY_SIMPLE.get(stem, 1), p["nombre"], p["volumen_cm3"], p["bbox"], p["orient"], p["soportes"], rel, p["masa_g"]))
    for stem, p in rb["piezas"].items():
        rows.append(("boya simple", stem, p["qty"], p["nombre"], p["volumen_cm3"], p["bbox"], p["orient"], p["voladizo_mm2"] > thr,
                     f"{p['relleno'] * 100:.0f} %", p["masa_g"]))
    for stem, qty, desc in MODULAR:
        sh = cq.importers.importStep(str(SAL / "preliminar" / "step" / f"{stem}.step")).val()
        inf = 1.0 if stem.startswith(MODULAR_SEALED) else 0.4
        best = None
        for on, o in ORIENTS.items():
            mc = mesh_checks(str(SAL / "preliminar" / "stl" / f"{stem}.stl"), P.PRINT_BED, o)
            if mc["fits_bed"] and (best is None or mc["overhang_mm2"] < best[1]["overhang_mm2"]):
                best = (on, mc)
        rows.append(("modular D200", stem, qty, desc, sh.Volume() / 1000, best[1]["bbox"], best[0], best[1]["overhang_mm2"] > thr,
                     f"{inf * 100:.0f} %", FA.mass_g(sh, inf)))
    rows += slicer_rows()
    return rows, res, rb


def slicer_rows():
    """Rows of the groups that come only from slicer.json (g, h per piece; quantity from resultados.json "cantidades" or qty)."""
    rows = []
    for g, d in SLICER_GROUPS.items():
        sl = json.loads((d / "slicer.json").read_text(encoding="utf-8"))
        qtys = {}
        if g != "boya PET 4 x 1 L":
            qtys = json.loads((d / "resultados.json").read_text(encoding="utf-8"))["cantidades"]
        for stem, v in sl.items():
            q = v["qty"] if "qty" in v else qtys.get(stem, 1)
            rows.append((g, stem, q, v.get("nombre", stem), 0.0, (0, 0, 0), "slicer", v["soportes"], f"{v['relleno_pct']} %", v["g"]))
            SLICER_DATA.setdefault(g, {})[stem] = v
    return rows


SLICER_DATA = {}


def slicer_of(g, stem, slicer):
    if g in SLICER_GROUPS:
        return SLICER_DATA[g][stem]
    return slicer.get(stem) if g in ("nodo simple", "linterna de prueba") else None


def hardware(res, rb):
    """[(group, item, size, quantity)] counted from the models where they fix them."""
    import boya_simple as BS
    import caja_central as CC
    import capsula as CP
    import layout
    lay = layout.build(P.SIMPLE_ESP32_BASE, floors=P.SIMPLE_FLOORS)
    n_lid, n_tray = len(CC.screw_pts(lay)), len(layout.tray_boss_pts(lay))
    ol, ow, _ = lay.box_outer()
    L, Wd, _ = lay.cav
    box_cord = 2 * ((L + ol + P.BOX_FLANGE) / 2 + (Wd + ow + P.BOX_FLANGE) / 2)
    _, _, fl_w, fl_h, *_ = CP.cap_dims()
    cap_cord = 2 * ((CP.CAP_CAV_W + fl_w - P.CAP_FLANGE) / 2 + (CP.CAP_CAV_H + fl_h - P.CAP_FLANGE) / 2)
    cord = round((box_cord + 2 * cap_cord) * 1.1 / 10) * 10
    lastre_g = res["lastre"]["total_g"]
    common = [("Tornillo M3 x 12 + inserto termico M3 (tapa de la caja)", "M3", n_lid),
              ("Tornillo M3 x 8 + inserto termico M3 (bandejas)", "M3", n_tray),
              ("Tornillo M3 x 16 + tuerca (capsulas)", "M3", 8),
              ("Tornillo M2 autorroscante (bisel)", "M2 x 6", 6),
              ("Cordon de junta torica Ø2 (caja + 2 capsulas, +10 %)", f"{cord:.0f} mm", 1),
              ("Prensaestopas PG7 con contratuerca (3 caja + 2 capsulas)", "PG7", 5),
              ("Disco de acrilico de la ventana", f"Ø{P.WIN_DIA:g} x {P.WIN_T:g}", 2),
              ("Grillete o argolla de inox (izado)", "M6", 1)]
    simple = common + [("Tornillo M4 x 20 + inserto termico M4 (bridas del riel a la caja)", "M4", 8),
                       ("Tornillo M3 x 8 avellanado + inserto M3 (tapas del bolsillo)", "M3", 4),
                       ("Tornillo M4 x 45 + tuerca (pie de las capsulas)", "M4", 4),
                       ("Correa textil", f"{P.STRAP_W:g} x 300 mm", 2), ("Lastre a granel: tuercas y arandelas M8 de inox", f"{lastre_g:.0f} g", 1)]
    bl = 2 * ((BS.LI + BS.L) / 2 + (BS.WI + BS.Wd) / 2) * 1.1
    boya = [("Tornillo M3 x 12 + inserto M3 (tapa de la boya)", "M3", len(BS.screw_pts())),
            ("Tornillo M3 + inserto M3 (portabaterias y bandeja)", "M3", 8),
            ("Tornillo M3 x 30 + inserto M3 (largueros a la tapa)", "M3", 4),
            ("Tornillo M3 + inserto M3 (panel a los largueros)", "M3", 4),
            ("Perno M5 x 120 inox + inserto M5 (flotadores)", "M5", 8),
            ("Tornillo M5 + inserto M5 (ojal de amarre)", "M5", 1),
            ("Cordon de junta torica Ø2 (tapa de la boya, +10 %)", f"{round(bl / 10) * 10:.0f} mm", 1),
            ("Prensaestopas PG7 (umbilical y panel)", "PG7", 2),
            ("Tapon de la boca de llenado de los flotadores (o sello con PETG)", "Ø10", 4),
            ("Manguera flexible U1 de referencia", f"Ø{P.UMB_HOSE_D:g}", 1),
            ("Cabo de amarre C1 boya-linterna", "Ø4", 1)]
    modular = common + [("Tornillo M4 x 12 + inserto termico M4 (riel a la caja)", "M4", 4),
                        ("Varilla roscada M8 (8.8)", "451 mm", 1), ("Tuerca M8", "M8", 2), ("Arandela ancha DIN 9021", "M8", 2),
                        ("Tornillo M4 x 14 + tuerca (uniones de tramos)", "M4", 8),
                        ("Tornillo M3 x 8 avellanado + inserto M3 (tapa del bolsillo)", "M3", 4),
                        ("Perno M4 hexagonal (perillas) + tuerca en la ranura T", "M4", 4),
                        ("Perno M4 x 20 + tuerca mariposa (bisagras)", "M4", 2), ("Pivote M3 del pestillo", "M3", 2),
                        ("Correa textil", f"{P.STRAP_W:g} x 300 mm", 2), ("Pletina de inox", "25 x 5 x 100", 4)]
    return ([("nodo simple", *h) for h in simple] + [("boya simple", *h) for h in boya]
            + [("modular D200", *h) for h in modular])


def design_rows(res, rb):
    r = res
    w4, w1 = r["peso"]["40"], r["peso"]["100"]
    cx = r["caja"]
    fem_f = SAL / "simple" / "fem" / "fem.json"
    rows = [("Riel: largo / seccion x pared", f"{r['riel']['largo']:g} / {r['riel']['seccion']:g} x {r['riel']['pared']:g}", "mm", "params.py simple.riel_L, riel.*"),
            ("Caja: ESP32 y pisos", f"{cx['esp32']}, {cx['pisos']} pisos", "-", "params.py simple.esp32_base (equipo), simple.caja_pisos"),
            ("Caja: exterior (sin brida)", " x ".join(f"{v:.1f}" for v in cx["exterior"]), "mm", "layout.py (derivado de la electronica)"),
            ("Caja: con brida", " x ".join(f"{v:.1f}" for v in cx["con_brida"]), "mm", "layout.py + caja.brida_ancho"),
            ("Caja: interior (cavidad)", " x ".join(f"{v:.1f}" for v in cx["interior"]), "mm", "layout.py"),
            ("Caja: pared / fondo", f"{cx['pared']:g} / {cx['fondo']:g}", "mm", "params.py caja.pared, caja.fondo"),
            ("Nodo sobre el aro (de / a)", f"{r['zmin_sobre_aro']:.0f} / {r['zmax_sobre_aro']:.0f}", "mm", "simple.py, nube de puntos del CAD"),
            ("Capsula: exterior", " x ".join(f"{v:.1f}" for v in r["capsula"]["exterior"]), "mm", "capsula.py cap_dims"),
            ("Capsula: angulo y acimut", f"{r['capsula']['angulo']:g} grados, {r['capsula']['acimut']}", "-", "params.py capsula.angulo, capsula.acimut (equipo)"),
            ("Ventana: diametro x espesor", f"{r['ventana']['diametro']:g} x {r['ventana']['espesor']:g}", "mm", "params.py ventana.*"),
            ("Gancho en C (fusionado al riel): C interior / pared / asiento", f"{r['gancho']['c_interior']:g} / {r['gancho']['pared']:g} / {r['gancho']['asiento']:g}", "mm", "params.py aro.seccion, gancho.c"),
            ("Separador LR1", "no se usa" if not r["separador"].get("usar", True) else f"{r['separador']['tipo']}, {r['separador']['altura']:g}", "-", "params.py separador.usar (tanda 3: sin separador)"),
            ("Lastre a granel (un bolsillo por lado)", f"{r['lastre']['total_g']:.0f} g de {r['lastre']['nombre']}, bolsillo {' x '.join(f'{v:g}' for v in r['lastre']['medida_bolsillo'])}", "mm", "params.py lastre.granel, simple.py"),
            ("Nodo: peso en aire (bandeja 40 % / 100 %)", f"{w4['aire_g']:.0f} / {w1['aire_g']:.0f}", "g", "simple.py, masas por pieza con su relleno"),
            ("Nodo: peso aparente (40 % / 100 %)", f"{w4['aparente_g']:+.0f} / {w1['aparente_g']:+.0f}", "g", "simple.py (ventana +200 a +500)"),
            ("Nodo: BG", f"{r['bg_mm']:.1f}", "mm", "simple.py"),
            ("Punto de amarre de las cuerdas sobre el aro", f"{r['apice_sobre_aro']:.0f}", "mm", "linterna.nudo_h"),
            ("Aire minimo suspension-nodo", f"{r['aire_min']:.1f}", "mm", "simple.py (exigido 10)"),
            ("FS riel (capas / entre capas)", f"{r['fs']['riel']:.1f} / {r['fs']['riel_capas']:.1f}", "-", "simple.py §5, a mano"),
            ("FS pie de capsula (capas / entre capas)", f"{r['fs']['pie']:.1f} / {r['fs']['pie_capas']:.1f}", "-", "simple.py §5, a mano"),
            ("FS gancho (capas / entre capas)", f"{r['fs']['gancho']:.1f} / {r['fs']['gancho_capas']:.1f}", "-", "simple.py §5, a mano"),
            ("Traccion por inserto M4 de las bridas al izar", f"{r['insertos_N']:.0f}", "N", "simple.py §5 (probar con PB8)"),
            ("Cable por camara", f"{r['cable_mm']:.0f}", "mm", "simple.py §6 (> 300: prueba SPI)"),
            ("Boya: masa / calado / francobordo", f"{rb['masa_g']:.0f} / {rb['calado']:.1f} / {rb['francobordo']:.1f}", "g / mm / mm", "boya_simple.py (agua de mar 1025)"),
            ("Boya: reserva / GM balanceo y cabeceo", f"{rb['reserva'] * 100:.0f} % / {rb['GM'][0]:.0f} y {rb['GM'][1]:.0f}", "- / mm", "boya_simple.py"),
            ("Nodo + boya en aire (limite 3000)", f"{rb['total_g']:.0f}", "g", "simple.py + boya_simple.py")]
    for cam in r.get("camaras", []):
        rows.append((f"Camara en Ø{cam['D']:g}: lente a la red", f"{cam['dist']:.0f}" if cam["dist"] else "no corta la red", "mm",
                     "simple.py camera_view (FOV y enfoque estimados)"))
    if fem_f.exists():
        fem = json.loads(fem_f.read_text(encoding="utf-8"))
        for k, v in fem.get("casos", {}).items():
            rows.append((f"FEM {k}: desplazamiento max / tension max / FS", f"{v['umax']:.2f} / {v['smax']:.1f} / {v['fs']:.1f}", "mm / MPa / -", "fem"))
    return rows


def build_book(rows, hw, res, rb, slicer):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    yellow = PatternFill("solid", fgColor="FFF2CC")
    head = Font(name="Arial", bold=True)
    wb = openpyxl.load_workbook(TEMPLATE) if TEMPLATE.exists() else openpyxl.Workbook()
    ws = wb["MEDIDAS"] if "MEDIDAS" in wb.sheetnames else wb.create_sheet("MEDIDAS")
    ws.cell(1, 10, "nombre_en_params").font = head
    ws.cell(1, 11, "nota").font = head
    for r in range(3, ws.max_row + 1):
        name = ws.cell(r, 1).value
        if not name or (name not in MAP and name not in NOT_IN_CAD):
            continue
        if name in NOT_IN_CAD:
            ws.cell(r, 11, NOT_IN_CAD[name])
            continue
        key, idx, note = MAP[name]
        prm = P.REGISTRO[key]
        val = prm.value[idx] if idx is not None else prm.value
        for c, v in ((5, val), (6, prm.origen), (7, prm.estado), (8, "CAD"), (9, TODAY)):
            ws.cell(r, c, v).fill = yellow
        ws.cell(r, 10, key + (f"[{idx}]" if idx is not None else ""))
        ws.cell(r, 11, note)

    rs = wb.create_sheet("RESUMEN", 0)
    rs["A1"] = "LanternGuard, prototipo simple Ø200 (nodo V2 + boya): masa impresa, horas y costo"
    rs["A1"].font = Font(name="Arial", bold=True, size=14)
    rs["A2"], rs["C2"] = "Parametros (amarillo = entrada; vienen de params.py)", "nombre en params.py"
    for i, (lab, v, key) in enumerate([("Densidad del PETG g/cm³ (estimado)", P.PETG_DENSITY, "petg.densidad"),
                                       ("Impresora g/h (estimado)", P.PRINT_RATE_GH, "costo.g_por_h"),
                                       ("Filamento soles/kg (estimado)", P.FILAMENT_PRICE, "costo.filamento_soles_kg")]):
        rs.cell(3 + i, 1, lab)
        rs.cell(3 + i, 2, v).fill = yellow
        rs.cell(3 + i, 3, key)
    hdr = ["grupo", "masa impresa g (estimado o slicer)", "horas (estimado o slicer)", "costo filamento S/", "costo hardware S/", "total S/"]
    for j, h in enumerate(hdr):
        rs.cell(9, 1 + j, h).font = head
    groups = ["nodo simple", "linterna de prueba", "boya simple", "modular D200"]
    for i, g in enumerate(groups):
        r = 10 + i
        rs.cell(r, 1, g)
        rs.cell(r, 2, f"=SUMIF(PIEZAS!$B:$B,$A{r},PIEZAS!$N:$N)")
        rs.cell(r, 3, f"=SUMIF(PIEZAS!$B:$B,$A{r},PIEZAS!$P:$P)")
        rs.cell(r, 4, f"=SUMIF(PIEZAS!$B:$B,$A{r},PIEZAS!$Q:$Q)")
        rs.cell(r, 5, f"=SUMIF(HARDWARE!$A:$A,$A{r},HARDWARE!$F:$F)")
        rs.cell(r, 6, f"=D{r}+E{r}")
    r = 10 + len(groups)
    rs.cell(r, 1, "nodo simple + linterna + boya").font = head
    for col in "BCDEF":
        rs[f"{col}{r}"] = f"=SUM({col}10:{col}12)"
    for i, g in enumerate(SLICER_GROUPS):
        r2 = r + 2 + i
        rs.cell(r2, 1, g)
        rs.cell(r2, 2, f"=SUMIF(PIEZAS!$B:$B,$A{r2},PIEZAS!$N:$N)")
        rs.cell(r2, 3, f"=SUMIF(PIEZAS!$B:$B,$A{r2},PIEZAS!$P:$P)")
        rs.cell(r2, 4, f"=SUMIF(PIEZAS!$B:$B,$A{r2},PIEZAS!$Q:$Q)")
        rs.cell(r2, 5, f"=SUMIF(HARDWARE!$A:$A,$A{r2},HARDWARE!$F:$F)")
        rs.cell(r2, 6, f"=D{r2}+E{r2}")
    r += len(SLICER_GROUPS) + 1
    rs.cell(r + 2, 1, "Masa por pieza = la misma del calculo de flotacion (piel + relleno de cada pieza). Llenar los precios "
                      "amarillos de HARDWARE para el costo total. La fila modular D200 es para comparar.")

    ps = wb.create_sheet("PIEZAS", 1)
    hdr = ["pieza", "grupo", "descripcion", "cantidad", "X mm (orientacion de impresion)", "Y mm", "Z mm",
           "volumen solido cm³ (CadQuery)", "orientacion", "soportes", "relleno_%", "fraccion maciza (piel + relleno)",
           "masa por pieza g (estimado o slicer)", "masa total g", "horas por pieza (estimado o slicer)", "horas total",
           "costo S/", "fuente masa y horas"]
    for j, h in enumerate(hdr):
        ps.cell(1, 1 + j, h).font = head
    for i, (g, stem, q, desc, vol, bb, orient, sup, rel, m) in enumerate(rows):
        r = 2 + i
        frac = m / (vol * P.PETG_DENSITY) if vol else 0
        for j, v in enumerate([stem, g, desc, q, round(bb[0], 1), round(bb[1], 1), round(bb[2], 1), round(vol, 2), orient,
                               "si" if sup else "no", rel, round(frac, 3)]):
            ps.cell(r, 1 + j, v)
        sl = slicer_of(g, stem, slicer)
        if sl:
            ps.cell(r, 13, round(sl["g"], 1))
            ps.cell(r, 15, round(sl["h"], 2))
            ps.cell(r, 18, "slicer")
        else:
            ps.cell(r, 13, f"=H{r}*RESUMEN!$B$3*L{r}")
            ps.cell(r, 15, f"=M{r}/RESUMEN!$B$4")
            ps.cell(r, 18, "estimado")
        ps.cell(r, 14, f"=M{r}*D{r}")
        ps.cell(r, 16, f"=O{r}*D{r}")
        ps.cell(r, 17, f"=N{r}/1000*RESUMEN!$B$5")
    ps.cell(len(rows) + 3, 1, f"Soportes: voladizo en la orientacion de impresion > {res['soporte_umbral_mm2']:g} mm². Masa = volumen x "
            "densidad x fraccion maciza (piel de impresion.cascara + relleno); horas = masa / g por hora (RESUMEN).")

    hs = wb.create_sheet("HARDWARE", 2)
    for j, h in enumerate(["grupo", "item", "medida", "cantidad", "precio unitario S/ (llenar)", "subtotal S/"]):
        hs.cell(1, 1 + j, h).font = head
    for i, (g, item, size, q) in enumerate(hw):
        r = 2 + i
        for j, v in enumerate([g, item, size, q]):
            hs.cell(r, 1 + j, v)
        hs.cell(r, 5).fill = yellow
        hs.cell(r, 6, f"=D{r}*E{r}")

    ds = wb.create_sheet("DISEÑO", 3)
    for j, h in enumerate(["concepto", "valor", "unidad", "de donde sale"]):
        ds.cell(1, 1 + j, h).font = head
    for i, row in enumerate(design_rows(res, rb)):
        for j, v in enumerate(row):
            ds.cell(2 + i, 1 + j, v)

    for sh in wb.worksheets:
        for row in sh.iter_rows():
            for cell in row:
                f = cell.font
                cell.font = Font(name="Arial", bold=f.bold, size=f.size if f.size else 10, color="FF000000")
                if isinstance(cell.value, str) and len(cell.value) > 60:
                    cell.alignment = Alignment(wrap_text=True, vertical="top")
        for c in range(1, sh.max_column + 1):
            width = max((len(str(sh.cell(r, c).value)) for r in range(1, min(sh.max_row, 80) + 1)
                         if sh.cell(r, c).value is not None and not str(sh.cell(r, c).value).startswith("=")), default=8)
            sh.column_dimensions[get_column_letter(c)].width = min(max(10, width + 2), 60)
    return wb


def totals(rows, slicer):
    """Same numbers as the RESUMEN formulas (hardware prices are empty: cost 0 until filled)."""
    out = {}
    for g in ("nodo simple", "linterna de prueba", "boya simple", "modular D200", *SLICER_GROUPS):
        m = h = 0.0
        for gg, stem, q, desc, vol, bb, orient, sup, rel, mu in rows:
            if gg != g:
                continue
            sl = slicer_of(g, stem, slicer)
            mu = sl["g"] if sl else mu
            hu = sl["h"] if sl else mu / P.PRINT_RATE_GH
            m += mu * q
            h += hu * q
        out[g] = dict(masa=m, horas=h, costo=m / 1000 * (P.PETG_PRICE if g in SLICER_GROUPS else P.FILAMENT_PRICE))
    return out


def write_md(rows, hw, res, rb, slicer):
    t = totals(rows, slicer)
    L = ["# BOM y bitacora del prototipo simple (generado por `bitacora.py`)", "",
         f"No editar a mano: `python cad_final/build.py --bitacora`. Excel con formulas: `salida/simple/BITACORA.xlsx`. "
         f"Masa por pieza = la del calculo de flotacion (piel + relleno de cada pieza: 100 % cajas estancas, tapas con junta y "
         f"ganchos; 40 % riel, bandejas y bisel). Parametros de costo (estimados): densidad {P.PETG_DENSITY:g} g/cm³, "
         f"{P.PRINT_RATE_GH:g} g/h, {P.FILAMENT_PRICE:g} soles/kg. Fuente: "
         f"{'slicer (OrcaSlicer) en el nodo' if slicer else 'estimado (sin slicer todavia)'}.", "",
         "## Resumen", "", "| Grupo | Masa impresa g | Horas | Costo filamento S/ |", "|---|---|---|---|"]
    for g, v in t.items():
        L.append(f"| {g} | {v['masa']:.0f} | {v['horas']:.1f} | {v['costo']:.2f} |")
    L += ["", "El hardware no tiene precios todavia (columna amarilla de HARDWARE en el Excel).", "",
          "## Piezas", "", "| Pieza | Grupo | Cant. | X × Y × Z mm | Volumen cm³ | Orientacion | Soportes | Relleno | Masa por pieza g | Fuente |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for g, stem, q, desc, vol, bb, orient, sup, rel, mu in rows:
        sl = slicer_of(g, stem, slicer)
        L.append(f"| {stem} | {g} | {q} | {bb[0]:.1f} × {bb[1]:.1f} × {bb[2]:.1f} | {vol:.1f} | {orient} | {'si' if sup else 'no'} | "
                 f"{rel} | {sl['g'] if sl else mu:.0f} | {'slicer' if sl else 'estimado'} |" if g not in SLICER_GROUPS else f"| {stem} | {g} | {q} | - | - | {sl and 'slicer'} | {'si' if sup else 'no'} | {rel} | {sl['g']:.0f} | slicer |")
    L += ["", "## Hardware", "", "| Grupo | Item | Medida | Cantidad |", "|---|---|---|---|"]
    L += [f"| {g} | {it} | {sz} | {q} |" for g, it, sz, q in hw]
    L += ["", "## Diseño", "", "| Concepto | Valor | Unidad | De donde sale |", "|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in design_rows(res, rb)]
    (HERE / "BOM.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return t


def main():
    rows, res, rb = piece_rows()
    hw = hardware(res, rb)
    sf = SAL / "simple" / "slicer.json"
    slicer = json.loads(sf.read_text(encoding="utf-8")) if sf.exists() else {}
    wb = build_book(rows, hw, res, rb, slicer)
    wb.save(OUT_XLSX)
    if DRIVE_COPY.parent.exists():
        shutil.copy2(OUT_XLSX, DRIVE_COPY)
    t = write_md(rows, hw, res, rb, slicer)
    for g, v in t.items():
        print(f"{g:20s} masa {v['masa']:7.0f} g  horas {v['horas']:6.1f}  filamento S/ {v['costo']:7.2f}")
    print("written", OUT_XLSX, "and BOM.md", "(slicer)" if slicer else "(estimado)")


if __name__ == "__main__":
    main()
