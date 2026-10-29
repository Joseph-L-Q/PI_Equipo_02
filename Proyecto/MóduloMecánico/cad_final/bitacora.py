"""Bitacora of the simple prototype: dimensions, weight and cost (modular D200 and the buoy for comparison).

    python bitacora.py          (from cad_final/; or: python build.py --bitacora)
Writes salida/simple/BITACORA.xlsx (copy in Downloads/LanternGuard_simple_para_Drive/) and cad_final/BOM.md from the
same data. Sheets: MEDIDAS (the team template filled with what params.py uses today), DISENO (outputs of simple.py),
PIEZAS, HARDWARE, RESUMEN (formulas, not pasted values). Inputs in yellow, formulas in black, Arial.
Reads: params.py, salida/simple/resultados.json (run simple.py first), the STEP/STL of every piece, and
salida/simple/slicer.json if slicer.py ran (its mass and time replace the estimate and are marked "slicer").
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

# (group, stem, folder of the STEP, quantity per node, description)
SIMPLE = [("M1_caja_cuerpo", 1, "Caja, cuerpo"), ("M2_caja_tapa", 1, "Caja, tapa con asa"), ("M11_bandeja", 1, "Bandeja"),
          ("M3s_riel_mitad", 2, "Riel, mitad"), ("M3t_tapa_bolsillo", 2, "Tapa del bolsillo del lastre"),
          ("M5s_capsula_tapa_pie", 2, "Capsula, tapa con pie"), ("M9s_gancho", 2, "Gancho en C"),
          ("M4_capsula_cuerpo", 2, "Capsula, cuerpo"), ("M6_capsula_bisel", 2, "Bisel de la ventana")]
MODULAR = [("M1_caja_cuerpo", 1, "Caja, cuerpo"), ("M2_caja_tapa", 1, "Caja, tapa con asa"), ("M11_bandeja", 1, "Bandeja"),
           ("M3_riel_central", 1, "Riel, tramo central"), ("M3_riel_ext", 2, "Riel, extension"), ("M3_riel_punta", 2, "Riel, punta"),
           ("M3_tapa_bolsillo", 2, "Tapa del bolsillo"), ("M4_capsula_cuerpo", 2, "Capsula, cuerpo"), ("M5_capsula_tapa", 2, "Capsula, tapa con bisagra"),
           ("M6_capsula_bisel", 2, "Bisel"), ("M9_gancho", 2, "Gancho al aro"), ("M10_carro_capsula", 2, "Carro"),
           ("M12_perilla", 4, "Perilla"), ("M13_casquillo_D8", 2, "Casquillo Ø8"), ("M14_pestillo", 2, "Pestillo")]
BOYA = [("B1_casco_central", 1, "Casco"), ("B1b_bandeja", 1, "Bandeja"), ("B2_tapa", 1, "Tapa"), ("B3_larguero_panel", 2, "Larguero del panel"),
        ("B4_mastil_antena", 1, "Mastil de la antena"), ("B5_flotador", 4, "Flotador"), ("B5b_tapa_flotador", 4, "Tapa del flotador"),
        ("B6_ojal_amarre", 1, "Ojal de amarre")]
GROUPS = [("nodo simple", SAL / "simple", SIMPLE), ("linterna de prueba", SAL / "linterna_prueba", [("LR1_separador", 1, "Separador LR1")]),
          ("boya", SAL / "boya", BOYA), ("modular D200", SAL / "preliminar", MODULAR)]

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
       "umbilical.diametro": ("umbilical", 0, ""), "umbilical.longitud": ("umbilical", 1, ""),
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
    """[(group, stem, qty, description, volume cm3, bbox in the print orientation, orientation, supports)]."""
    from checks import mesh_checks
    from capsula import ORIENTS
    res = json.loads((SAL / "simple" / "resultados.json").read_text(encoding="utf-8"))
    rows = []
    for group, folder, pieces in GROUPS:
        step_dir = folder / "step" if (folder / "step").exists() else folder
        stl_dir = folder / "stl" if (folder / "stl").exists() else folder
        for stem, qty, desc in pieces:
            vol = cq.importers.importStep(str(step_dir / f"{stem}.step")).val().Volume() / 1000
            info = res["piezas"].get(stem) if group in ("nodo simple", "linterna de prueba") else None
            if info:
                bb, orient, sup = info["bbox"], info["orient"], info["soportes"]
            else:
                best = None
                for on, o in ORIENTS.items():
                    mc = mesh_checks(str(stl_dir / f"{stem}.stl"), P.PRINT_BED, o)
                    if mc["fits_bed"] and (best is None or mc["overhang_mm2"] < best[1]["overhang_mm2"]):
                        best = (on, mc)
                bb, orient, sup = best[1]["bbox"], best[0], best[1]["overhang_mm2"] > res["soporte_umbral_mm2"]
            rows.append((group, stem, qty, desc, vol, bb, orient, sup))
    return rows, res


def hardware(res):
    """[(group, item, size, quantity)] counted from the layout where the CAD fixes them."""
    import caja_central as CC
    import capsula as CP
    import layout
    lay = layout.build(floors=1)
    n_lid, n_tray = len(CC.screw_pts(lay)), len(layout.tray_boss_pts(lay))
    ol, ow, _ = lay.box_outer()
    L, Wd, _ = lay.cav
    box_cord = 2 * ((L + ol + P.BOX_FLANGE) / 2 + (Wd + ow + P.BOX_FLANGE) / 2)
    _, _, fl_w, fl_h, *_ = CP.cap_dims()
    cap_cord = 2 * ((CP.CAP_CAV_W + fl_w - P.CAP_FLANGE) / 2 + (CP.CAP_CAV_H + fl_h - P.CAP_FLANGE) / 2)
    cord = round((box_cord + 2 * cap_cord) * 1.1 / 10) * 10
    k = res["pletinas"]["por_bolsillo"] * res["pletinas"]["bolsillos"]
    common = [("Tornillo M3 x 12 + inserto termico M3 (tapa de la caja)", "M3", n_lid),
              ("Tornillo M3 x 8 + inserto termico M3 (bandeja)", "M3", n_tray),
              ("Tornillo M3 x 16 + tuerca (capsulas)", "M3", 8),
              ("Tornillo M4 x 12 + inserto termico M4 (riel a la caja)", "M4", 4),
              ("Tornillo M2 autorroscante (bisel)", "M2 x 6", 6),
              ("Cordon de junta torica Ø2 (caja + 2 capsulas, +10 %)", f"{cord:.0f} mm", 1),
              ("Prensaestopas PG7 con contratuerca (3 caja + 2 capsulas)", "PG7", 5),
              ("Disco de acrilico de la ventana", f"Ø{P.WIN_DIA:g} x {P.WIN_T:g}", 2),
              ("Grillete o argolla de inox (izado)", "M6", 1)]
    simple = common + [("Tornillo M3 x 20 + tuerca (union del riel)", "M3", 4),
                       ("Tornillo M3 x 8 avellanado + inserto M3 (tapa del bolsillo)", "M3", 4),
                       ("Tornillo M4 x 12 + tuerca M4 en la ranura T (ganchos)", "M4", 4),
                       ("Tornillo M4 x 45 + tuerca (pie de las capsulas)", "M4", 4),
                       ("Correa textil", f"{P.STRAP_W:g} x 300 mm", 2),
                       ("Pletina de inox", "25 x 5 x 100", k)]
    modular = common + [("Varilla roscada M8 (8.8)", "451 mm", 1), ("Tuerca M8", "M8", 2), ("Arandela ancha DIN 9021", "M8", 2),
                        ("Tornillo M4 x 14 + tuerca (uniones de tramos)", "M4", 8),
                        ("Tornillo M3 x 8 avellanado + inserto M3 (tapa del bolsillo)", "M3", 4),
                        ("Perno M4 hexagonal (perillas) + tuerca en la ranura T", "M4", 4),
                        ("Perno M4 x 20 + tuerca mariposa (bisagras)", "M4", 2), ("Pivote M3 del pestillo", "M3", 2),
                        ("Correa textil", f"{P.STRAP_W:g} x 300 mm", 2), ("Pletina de inox", "25 x 5 x 100", 4)]
    return [("nodo simple", *h) for h in simple] + [("modular D200", *h) for h in modular]


def design_rows(res):
    r = res
    w4, w1 = r["peso"]["40"], r["peso"]["100"]
    cx = r["caja"]
    return [("Riel: largo", r["riel"]["largo"], "mm", "params.py simple.riel_L"),
            ("Riel: seccion x pared", f"{r['riel']['seccion']:g} x {r['riel']['pared']:g}", "mm", "params.py riel.seccion, riel.pared"),
            ("Caja: exterior (sin brida)", " x ".join(f"{v:.1f}" for v in cx["exterior"]), "mm", "layout.py (derivado de la electronica)"),
            ("Caja: con brida", " x ".join(f"{v:.1f}" for v in cx["con_brida"]), "mm", "layout.py + caja.brida_ancho"),
            ("Caja: interior (cavidad)", " x ".join(f"{v:.1f}" for v in cx["interior"]), "mm", "layout.py"),
            ("Caja: pared / fondo", f"{cx['pared']:g} / {cx['fondo']:g}", "mm", "params.py caja.pared, caja.fondo"),
            ("Capsula: exterior (largo x ancho x alto)", " x ".join(f"{v:.1f}" for v in r["capsula"]["exterior"]), "mm", "capsula.py cap_dims"),
            ("Capsula: cavidad", " x ".join(f"{v:.1f}" for v in r["capsula"]["cavidad"]), "mm", "capsula.py (camara + holguras)"),
            ("Capsula: angulo fijo", r["capsula"]["angulo"], "grados", "params.py capsula.angulo"),
            ("Ventana: diametro x espesor", f"{r['ventana']['diametro']:g} x {r['ventana']['espesor']:g}", "mm", "params.py ventana.*"),
            ("Gancho: C interior / pared / asiento", f"{r['gancho']['c_interior']:g} / {r['gancho']['pared']:g} / {r['gancho']['asiento']:g}", "mm", "params.py aro.seccion, gancho.c"),
            ("Gancho: fondo del riel al centro de la varilla", r["gancho"]["caida"], "mm", "params.py gancho.caida"),
            ("Separador LR1: tipo, seccion", f"{r['separador']['tipo']}, {r['separador']['seccion'][0]:g} x {r['separador']['seccion'][1]:g}", "mm", "params.py separador.*"),
            ("Separador: altura (minima calculada)", f"{r['separador']['altura']:g} ({r['separador']['altura_min']:.0f})", "mm", "simple.py min_separator_h"),
            ("Pletinas de lastre", f"{r['pletinas']['por_bolsillo']} x {r['pletinas']['bolsillos']} de {' x '.join(f'{v:g}' for v in r['pletinas']['medida'])}", "mm", "params.py lastre.pletinas"),
            ("Peso en aire (bandeja 40 % / 100 %)", f"{w4['aire_g']:.0f} / {w1['aire_g']:.0f}", "g", "simple.py, volumenes del CAD"),
            ("Peso aparente en el agua (40 % / 100 %)", f"{w4['aparente_g']:+.0f} / {w1['aparente_g']:+.0f}", "g", "simple.py (ventana +200 a +500)"),
            ("Estabilidad BG", f"{r['bg_mm']:.1f}", "mm", "simple.py centros de masa y empuje"),
            ("Apice sobre el aro", f"{r['apice_sobre_aro']:.0f}", "mm", "separador.altura + apice.altura"),
            ("Aire minimo suspension-nodo", f"{r['aire_min']:.1f}", "mm", "simple.py, nube de puntos del CAD (exigido 10)"),
            ("FS del riel (a lo largo / entre capas)", f"{r['fs']['riel']:.1f} / {r['fs']['riel_capas']:.1f}", "-", "simple.py §5"),
            ("FS del pie de capsula (a lo largo / entre capas)", f"{r['fs']['pie']:.1f} / {r['fs']['pie_capas']:.1f}", "-", "simple.py §5 (punto debil)"),
            ("Traccion por inserto M4 al izar", f"{r['insertos_N']:.0f}", "N", "simple.py §5"),
            ("Cable por camara", f"{r['cable_mm']:.0f}", "mm", "simple.py §6 (> 300: prueba SPI)")]


def build_book(rows, hw, res, slicer):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    yellow = PatternFill("solid", fgColor="FFF2CC")
    head = Font(name="Arial", bold=True)
    wb = openpyxl.load_workbook(TEMPLATE) if TEMPLATE.exists() else openpyxl.Workbook()

    # MEDIDAS: the team template filled with today's params.py values (simple mode)
    ws = wb["MEDIDAS"] if "MEDIDAS" in wb.sheetnames else wb.create_sheet("MEDIDAS")
    ws.cell(1, 10, "nombre_en_params").font = head
    ws.cell(1, 11, "nota").font = head
    for r in range(3, ws.max_row + 1):
        name = ws.cell(r, 1).value
        if not name or name not in MAP and name not in NOT_IN_CAD:
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

    # RESUMEN first (PIEZAS and HARDWARE point at its parameter cells)
    rs = wb.create_sheet("RESUMEN", 0)
    rs["A1"] = "LanternGuard, prototipo simple Ø200: masa impresa, horas y costo"
    rs["A1"].font = Font(name="Arial", bold=True, size=14)
    params = [("Densidad del PETG g/cm³ (estimado)", P.PETG_DENSITY, "petg.densidad"),
              ("Factor de relleno (estimado)", P.FILL_FACTOR, "costo.factor_relleno"),
              ("Impresora g/h (estimado)", P.PRINT_RATE_GH, "costo.g_por_h"),
              ("Filamento soles/kg (estimado)", P.FILAMENT_PRICE, "costo.filamento_soles_kg")]
    rs["A2"], rs["C2"] = "Parametros (amarillo = entrada; vienen de params.py)", "nombre en params.py"
    for i, (lab, v, key) in enumerate(params):
        rs.cell(3 + i, 1, lab)
        rs.cell(3 + i, 2, v).fill = yellow
        rs.cell(3 + i, 3, key)
    hdr = ["grupo", "masa impresa g (estimado o slicer)", "horas (estimado o slicer)", "costo filamento S/",
           "costo hardware S/", "total S/"]
    for j, h in enumerate(hdr):
        rs.cell(9, 1 + j, h).font = head
    for i, (g, *_x) in enumerate(GROUPS):
        r = 10 + i
        rs.cell(r, 1, g)
        rs.cell(r, 2, f"=SUMIF(PIEZAS!$B:$B,$A{r},PIEZAS!$L:$L)")
        rs.cell(r, 3, f"=SUMIF(PIEZAS!$B:$B,$A{r},PIEZAS!$N:$N)")
        rs.cell(r, 4, f"=SUMIF(PIEZAS!$B:$B,$A{r},PIEZAS!$O:$O)")
        rs.cell(r, 5, f"=SUMIF(HARDWARE!$A:$A,$A{r},HARDWARE!$F:$F)")
        rs.cell(r, 6, f"=D{r}+E{r}")
    r = 10 + len(GROUPS)
    rs.cell(r, 1, "nodo simple + linterna + boya").font = head
    for col in "BCDEF":
        rs[f"{col}{r}"] = f"=SUM({col}10:{col}12)"
    rs.cell(r + 2, 1, "Costo de hardware: llenar los precios amarillos de HARDWARE. La fila modular D200 es para comparar.")

    # PIEZAS
    ps = wb.create_sheet("PIEZAS", 1)
    hdr = ["pieza", "grupo", "descripcion", "cantidad", "X mm (orientacion de impresion)", "Y mm", "Z mm",
           "volumen solido cm³ (CadQuery)", "orientacion", "soportes", "masa por pieza g (estimado)",
           "masa total g", "horas por pieza (estimado)", "horas total", "costo S/", "fuente masa y horas"]
    for j, h in enumerate(hdr):
        ps.cell(1, 1 + j, h).font = head
    for i, (g, stem, q, desc, vol, bb, orient, sup) in enumerate(rows):
        r = 2 + i
        for j, v in enumerate([stem, g, desc, q, round(bb[0], 1), round(bb[1], 1), round(bb[2], 1), round(vol, 2), orient,
                               "si" if sup else "no"]):
            ps.cell(r, 1 + j, v)
        sl = slicer.get(stem) if g in ("nodo simple", "linterna de prueba") else None
        if sl:
            ps.cell(r, 11, round(sl["g"], 1))
            ps.cell(r, 13, round(sl["h"], 2))
            ps.cell(r, 16, "slicer")
        else:
            ps.cell(r, 11, f"=H{r}*RESUMEN!$B$3*RESUMEN!$B$4")
            ps.cell(r, 13, f"=K{r}/RESUMEN!$B$5")
            ps.cell(r, 16, "estimado")
        ps.cell(r, 12, f"=K{r}*D{r}")
        ps.cell(r, 14, f"=M{r}*D{r}")
        ps.cell(r, 15, f"=L{r}/1000*RESUMEN!$B$6")
    ps.cell(len(rows) + 3, 1, f"Soportes: si el voladizo en la orientacion de impresion pasa de {res['soporte_umbral_mm2']:g} mm². "
            "Masa estimada = volumen x densidad x factor de relleno; horas = masa / g por hora (RESUMEN).")

    # HARDWARE
    hs = wb.create_sheet("HARDWARE", 2)
    for j, h in enumerate(["grupo", "item", "medida", "cantidad", "precio unitario S/ (llenar)", "subtotal S/"]):
        hs.cell(1, 1 + j, h).font = head
    for i, (g, item, size, q) in enumerate(hw):
        r = 2 + i
        for j, v in enumerate([g, item, size, q]):
            hs.cell(r, 1 + j, v)
        hs.cell(r, 5).fill = yellow
        hs.cell(r, 6, f"=D{r}*E{r}")

    # DISENO
    ds = wb.create_sheet("DISEÑO", 3)
    for j, h in enumerate(["concepto", "valor", "unidad", "de donde sale"]):
        ds.cell(1, 1 + j, h).font = head
    for i, row in enumerate(design_rows(res)):
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


def totals(rows, hw, slicer):
    """Same numbers as the RESUMEN formulas, for BOM.md (hardware prices are empty: cost 0 until filled)."""
    out = {}
    for g, *_x in GROUPS:
        m = h = 0.0
        for gg, stem, q, desc, vol, *_r in rows:
            if gg != g:
                continue
            sl = slicer.get(stem) if g in ("nodo simple", "linterna de prueba") else None
            mu = sl["g"] if sl else vol * P.PETG_DENSITY * P.FILL_FACTOR
            hu = sl["h"] if sl else mu / P.PRINT_RATE_GH
            m += mu * q
            h += hu * q
        out[g] = dict(masa=m, horas=h, costo=m / 1000 * P.FILAMENT_PRICE)
    return out


def write_md(rows, hw, res, slicer):
    t = totals(rows, hw, slicer)
    L = ["# BOM y bitacora del prototipo simple (generado por `bitacora.py`)", "",
         f"No editar a mano: `python cad_final/build.py --bitacora`. Excel con formulas: `salida/simple/BITACORA.xlsx`. "
         f"Parametros de costo (estimados, `params.py`): densidad {P.PETG_DENSITY:g} g/cm³, factor de relleno {P.FILL_FACTOR:g}, "
         f"{P.PRINT_RATE_GH:g} g/h, {P.FILAMENT_PRICE:g} soles/kg. Fuente de masa y horas: "
         f"{'slicer (OrcaSlicer) en las piezas del nodo simple' if slicer else 'estimado (sin slicer todavia)'}.", "",
         "## Resumen", "", "| Grupo | Masa impresa g | Horas | Costo filamento S/ |", "|---|---|---|---|"]
    for g, v in t.items():
        L.append(f"| {g} | {v['masa']:.0f} | {v['horas']:.1f} | {v['costo']:.2f} |")
    L += ["", "El hardware no tiene precios todavia (columna amarilla de HARDWARE en el Excel).", "",
          "## Piezas", "", "| Pieza | Grupo | Cant. | X × Y × Z mm | Volumen cm³ | Orientacion | Soportes | Masa por pieza g | Fuente |",
          "|---|---|---|---|---|---|---|---|---|"]
    for g, stem, q, desc, vol, bb, orient, sup in rows:
        sl = slicer.get(stem) if g in ("nodo simple", "linterna de prueba") else None
        mu = sl["g"] if sl else vol * P.PETG_DENSITY * P.FILL_FACTOR
        L.append(f"| {stem} | {g} | {q} | {bb[0]:.1f} × {bb[1]:.1f} × {bb[2]:.1f} | {vol:.1f} | {orient} | {'si' if sup else 'no'} | "
                 f"{mu:.0f} | {'slicer' if sl else 'estimado'} |")
    L += ["", "## Hardware", "", "| Grupo | Item | Medida | Cantidad |", "|---|---|---|---|"]
    L += [f"| {g} | {it} | {sz} | {q} |" for g, it, sz, q in hw]
    L += ["", "## Diseño (salidas de `simple.py`)", "", "| Concepto | Valor | Unidad | De donde sale |", "|---|---|---|---|"]
    L += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in design_rows(res)]
    (HERE / "BOM.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    return t


def main():
    rows, res = piece_rows()
    hw = hardware(res)
    sf = SAL / "simple" / "slicer.json"
    slicer = json.loads(sf.read_text(encoding="utf-8")) if sf.exists() else {}
    wb = build_book(rows, hw, res, slicer)
    wb.save(OUT_XLSX)
    if DRIVE_COPY.parent.exists():
        shutil.copy2(OUT_XLSX, DRIVE_COPY)
    t = write_md(rows, hw, res, slicer)
    for g, v in t.items():
        print(f"{g:20s} masa {v['masa']:7.0f} g  horas {v['horas']:6.1f}  filamento S/ {v['costo']:7.2f}")
    print("written", OUT_XLSX, "and BOM.md", "(slicer)" if slicer else "(estimado)")


if __name__ == "__main__":
    main()
