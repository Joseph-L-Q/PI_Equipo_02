"""05/11: clean Onshape document "LanternGuard - PIEZAS PARA IMPRIMIR", a workspace copy of LG_IMPRIMIR_P2 (never written to).

    python documento_limpio.py --local       3 assemblies, 5 probeta STEPs and 00_LEEME.pdf; no API
    python documento_limpio.py --copiar      copy, folder, description
    python documento_limpio.py --limpiar     delete what is not kept, rename what is
    python documento_limpio.py --subir       assemblies, probetas, 00_LEEME, link sharing
    python documento_limpio.py --planos      missing drawings, in print order
    python documento_limpio.py --verificar   broken references, missing and surplus tabs

Every step is resumable from salida/limpio/estado.json. Counter in salida/limpio/_llamadas.txt, hard stop at 250. Any write
to the source document stops the run.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request

os.environ.setdefault("LG_VERSION", "P2_robusto")

import publicar_nuevas as N  # noqa: E402

cq, OS, OP, P, Q, aro = N.cq, N.OS, N.OP, N.P, N.Q, N.aro
MOD = N.MOD
OUT = MOD / "salida" / "limpio"
STEP = OUT / "step"
STATE = OUT / "estado.json"
COUNT = OUT / "_llamadas.txt"
MAX = 250
SRC_DID, SRC_WID = N.DID, N.WID
TITLE = "LanternGuard - PIEZAS PARA IMPRIMIR"
LEEME = OUT / "00_LEEME.pdf"
DRIVE = "https://drive.google.com/drive/folders/1T8cv6NW7W2cESde3SLp9HgS4VRJMWwCO"
PROTO, BOYA = P.P2 / "step", P.BOYA / "step"
GRAY = cq.Color(0.6, 0.6, 0.6)
SEAL = "0,2 mm; 5 sup + 5 inf"
STD = "0,2 mm; sup/inf del perfil"
RING = "0,2 mm; 26 sup + 26 inf (5,2 mm)"
FULL, SIMPLE = 11, 5     # calls of one drawing with dimensions and of one without

# number_name, source tab (None: uploaded here), code, step, qty, g each, h each, perimeters, infill, layers, supports, source of g and h
PZ = [
    ("10_M1s_caja_cuerpo", "M1s_caja_cuerpo", "M1s_caja_cuerpo", PROTO / "M1s_caja_cuerpo.step", 1, 436, 9.25, 4, "100 %", SEAL, "sí", "slicer"),
    ("11_M2_caja_tapa", "M2_caja_tapa", "M2_caja_tapa", PROTO / "M2_caja_tapa.step", 1, 194, 4.80, 4, "100 %", SEAL, "sí", "slicer"),
    ("12_M3s_riel_gancho_x2", "M3s_riel_gancho", "M3s_riel_gancho", N.STEPS["M3s_riel_gancho"], 2, 214, 6.14, 4, "100 %", SEAL, "sí", "por volumen*"),
    ("13_M3t_tapa_bolsillo_x2", "M3t_tapa_bolsillo", "M3t_tapa_bolsillo", PROTO / "M3t_tapa_bolsillo.step", 2, 42, 0.87, 3, "100 %", STD, "no", "slicer"),
    ("14_M3f_marco_bolsillo_x2", "M3f_marco_bolsillo", "M3f_marco_bolsillo", PROTO / "M3f_marco_bolsillo.step", 2, 52, 1.95, 3, "40 %", STD, "no", "slicer"),
    ("15_M4_capsula_cuerpo_x2", "M4_capsula_cuerpo", "M4_capsula_cuerpo", PROTO / "M4_capsula_cuerpo.step", 2, 77, 2.04, 4, "100 %", SEAL, "sí", "slicer"),
    ("16_M5s_capsula_tapa_pie_x2", "M5s_capsula_tapa_pie", "M5s_capsula_tapa_pie", PROTO / "M5s_capsula_tapa_pie.step", 2, 97, 2.80, 4, "100 %", SEAL, "sí", "slicer"),
    ("17_M6_capsula_bisel_x2", "M6_capsula_bisel", "M6_capsula_bisel", PROTO / "M6_capsula_bisel.step", 2, 2, 0.20, 3, "40 %", STD, "no", "slicer"),
    ("18_M11_bandeja", "M11_bandeja", "M11_bandeja", PROTO / "M11_bandeja.step", 1, 42, 1.79, 3, "40 %", STD, "no", "slicer"),
    ("19_M11_bandeja_sup", "M11_bandeja_sup", "M11_bandeja_sup", PROTO / "M11_bandeja_sup.step", 1, 35, 1.15, 3, "40 %", STD, "no", "slicer"),
    ("30_B1_casco_mitad_x2", "B1_casco", "B1_casco", BOYA / "B1_casco.step", 2, 173, 7.21, 3, "40 %", STD, "sí", "slicer"),
    ("31_B2_cubierta_lisa", "B2_cubierta_lisa", "B2_cubierta_lisa", BOYA / "B2_cubierta_lisa.step", 1, 210, 10.41, 3, "40 %", STD, "no", "slicer"),
    ("32_B2_cubierta_mastil", "B2_cubierta_mastil", "B2_cubierta_mastil", BOYA / "B2_cubierta_mastil.step", 1, 230, 11.38, 3, "40 %", STD, "no", "slicer"),
    ("33_B3_caja", "B3_caja", "B3_caja", BOYA / "B3_caja.step", 1, 247, 4.96, 4, "100 %", SEAL, "no", "placa P16"),
    ("34_B4_tapa", "B4_tapa", "B4_tapa", BOYA / "B4_tapa.step", 1, 111, 2.90, 4, "100 %", SEAL, "no", "placa P16"),
    ("35_B5_cuna_base_x2", "B5_cuna_base", "B5_cuna_base", BOYA / "B5_cuna_base.step", 2, 79, 3.26, 3, "40 %", STD, "no", "slicer"),
    ("36_B5_cuna_cuello_x2", "B5_cuna_cuello", "B5_cuna_cuello", BOYA / "B5_cuna_cuello.step", 2, 81, 3.28, 3, "40 %", STD, "no", "slicer"),
    ("37_B6_correa_x4", "B6_correa", "B6_correa", BOYA / "B6_correa.step", 4, 6, 0.34, 3, "40 %", STD, "no", "slicer"),
    ("40_LR2_aro_x4", "LR2_aro", "LR2_aro", N.STEPS["LR2_aro"], 4, 150, 10.0, 13, "15 % gyroid", RING, "no", "estimado"),
    ("50_T1_caja", "T1_caja", "T1_caja", N.STEPS["T1_caja"], 1, 72, 4.8, 4, "100 %", SEAL, "no", "estimado"),
    ("51_T2_tapa", "T2_tapa", "T2_tapa", N.STEPS["T2_tapa"], 1, 49, 3.3, 4, "100 %", SEAL, "no", "estimado"),
]
PROBETAS_FUERA = ("01_P01_probeta_calibracion", "02_P02_probeta_inserto_M4_x3", "03_P03_probeta_junta", "04_P04_probeta_gancho", "05_P05_probeta_bahia_botella", "06_PB_aro")
# number_name -> existing drawing that already points at the live tab
PLANOS_OK = {"10_M1s_caja_cuerpo": "PLANO_A4_M1s_caja_cuerpo (1)", "11_M2_caja_tapa": "PLANO_A4_M2_caja_tapa (1)",
             "14_M3f_marco_bolsillo_x2": "PLANO_A4_M3f_marco_bolsillo", "15_M4_capsula_cuerpo_x2": "PLANO_A4_M4_capsula_cuerpo", "17_M6_capsula_bisel_x2": "Drawing 13 M6",
             "30_B1_casco_mitad_x2": "PLANO_A4_B1_casco (1)", "31_B2_cubierta_lisa": "PLANO_A4_B2_cubierta_lisa (1)", "32_B2_cubierta_mastil": "PLANO_A4_B2_cubierta_mastil (1)",
             "33_B3_caja": "PLANO_A4_B3_caja", "34_B4_tapa": "PLANO_A4_B4_tapa", "35_B5_cuna_base_x2": "PLANO_A4_B5_cuna_base", "36_B5_cuna_cuello_x2": "PLANO_A4_B5_cuna_cuello",
             "40_LR2_aro_x4": "PLANO_A4_LR2_aro", "50_T1_caja": "PLANO_A4_T1_caja", "51_T2_tapa": "PLANO_A4_T2_tapa"}
ENSAMBLES = ("00_ENSAMBLE_nodo", "00_ENSAMBLE_boya", "00_ENSAMBLE_tierra")
ESPERADO = {"00_ENSAMBLE_nodo": 20, "00_ENSAMBLE_boya": 14, "00_ENSAMBLE_tierra": 2}
EN_USO = {f"{p[1]}.step" for p in PZ if p[1]}
plano_de = lambda name: re.sub(r"^(\d+)_", r"\1_PLANO_", name)
_orig = N._orig
_names = {}
_new = {}


def used():
    return int(COUNT.read_text()) if COUNT.exists() else 3          # 3 read-only calls of the first look at the source


def call(self, method, path, body=None, content_type="application/json"):
    if used() >= MAX:
        raise SystemExit(f"tope de {MAX} llamadas")
    if method != "GET" and SRC_DID in path and not path.endswith(f"/workspaces/{SRC_WID}/copy"):     # copying only reads the source
        raise SystemExit(f"escritura en el documento original: {method} {path}")
    if path.endswith("/create") and isinstance(body, dict) and body.get("drawingName"):
        body["drawingName"] = _names.get(body["drawingName"], body["drawingName"])
    if method == "GET" and "/metadata/" in path and path.rsplit("/", 1)[1] in _new and "md" in _new:      # property ids repeat in every drawing
        return _new["md"]
    COUNT.write_text(str(used() + 1))
    r = _orig(self, method, path, body, content_type)
    if path.endswith("/create"):
        _new[r["id"]] = True
    elif method == "GET" and "/metadata/" in path and path.rsplit("/", 1)[1] in _new:
        _new["md"] = r
    return r


def client():
    OS.Client.call = call
    OS.API = OP.API_V6
    OS.POLL_S, OS.POLL_MAX = 20, 6
    return P.client()


def state():
    return OS.read_json(STATE, {})


def keep(S):
    OUT.mkdir(parents=True, exist_ok=True)
    OS.write_json(STATE, S)


def spread(parts):
    """Solids side by side along X, 10 mm apart, so a multi-solid coupon reads in a drawing."""
    out, x = {}, 0.0
    for k, v in parts.items():
        b = v.val().BoundingBox()
        out[k] = v.translate((x - b.xmin, -b.center.y, -b.zmin))
        x += b.xlen + 10.0
    return out


def write(path, parts, gray=()):
    asm = cq.Assembly(name=path.stem)
    for k, v in parts.items():
        asm.add(v, name=k, color=GRAY if k in gray else None)
    asm.export(str(path))
    return OP.step_parts(path)[1]


def assemblies():
    import tierra as T
    items = Q.build_assembly(None, keep_ref=("ref_linterna_", "ref_botella"))
    z_rod, levels = N.ring_levels()
    nodo, boya, refs = {}, {}, []
    for n, s in items:
        if n.startswith("lastre"):
            continue
        if n.lower().startswith("ref_botella") or n.startswith("B"):
            boya[n] = s.moved(cq.Location(cq.Vector(-Q.BUOY_DX, 0, 0)))
        else:
            nodo[n] = s
        if n.lower().startswith("ref"):
            refs.append(n)
    for k, z in enumerate(levels, 1):
        nodo[f"LR2_aro_{k}"] = aro.ring().val().moved(cq.Location(cq.Vector(0, 0, z)))
    tierra = {"T1_caja": T.t1(), "T2_tapa": T.t2().translate((0, 0, T.H_T1))}
    res = {}
    for name, parts in (("00_ENSAMBLE_nodo", nodo), ("00_ENSAMBLE_boya", boya), ("00_ENSAMBLE_tierra", tierra)):
        gray = [k for k in parts if k.lower().startswith("ref")]
        solids = write(STEP / f"{name}.step", parts, gray)
        printed = len(parts) - len(gray)
        res[name] = dict(solidos=solids, impresas=printed, referencias_gris=gray, nombres=sorted(k for k in parts if k not in gray))
        if printed != ESPERADO[name] or solids != len(parts):
            raise SystemExit(f"{name}: {printed} piezas y {solids} solidos, BOM {ESPERADO[name]}")
    return res


def cut(step, box):
    s = cq.importers.importStep(str(step))
    (x0, x1), (y0, y1), (z0, z1) = box
    return s.intersect(cq.Workplane().box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0)))


def probetas():
    import params as PR
    import probetas as PB
    r = PR.SIMPLE_RING_D / 2
    x0 = -PR.PET_HULL_MAX / 2
    plates = {"P01": spread(PB.pb7()), "P02": PB.pb8(), "P03": spread(PB.pb6()),
              "P04": {"PB10_gancho_tramo": cut(PROTO / "M3s_riel_gancho.step", ((r - 25, r + 25), (-60, 60), (-200, 200)))},
              "P05": {"PB9_bahia_botella": cut(BOYA / "B1_casco.step", ((x0 - 1, x0 + 80), (-200, 0), (-1, 300)))}}
    return {k: dict(solidos=write(STEP / f"{k}.step", v), nombres=list(v)) for k, v in plates.items()}


def hardware():
    keep_groups = {"nodo simple": "Nodo", "boya PET 4 x 1 L": "Boya", "estacion de tierra": "Tierra"}
    rows = []
    for line in (N.MOD / "cad_final" / "BOM.md").read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) == 4 and c[0] in keep_groups and not c[1].replace(".", "").isdigit():     # not the rows of the summary table
            if c[1].startswith("Lastre"):
                c[2] = "990 g calculado (pesar en agua)"
            rows.append((keep_groups[c[0]], c[1], c[2], c[3]))
    return rows


REVISAR = {
    "40_LR2_aro_x4": "Base plana sin despegar ni alabeo; apoya entero en la mesa. Sin hilos ni costuras gruesas en la sección Ø16,5: es lo que entra en el gancho.",
    "12_M3s_riel_gancho_x2": "Asiento C limpio de soporte, Ø17,1. Ranura de la brida 2,6 x 1,6 sin rebabas. 4 agujeros M4 y canal interior libres, sin capas abiertas.",
    "10_M1s_caja_cuerpo": "Ranura del cordón y cara de la brida planas. Sin grietas entre capas en las esquinas. Soporte fuera de las 2 ventanas. Agujeros de insertos abiertos.",
    "11_M2_caja_tapa": "Cara de cierre plana contra un vidrio, sin luz. Paso del PG7 limpio. Los 12 agujeros M3 coinciden con M1s.",
    "13_M3t_tapa_bolsillo_x2": "Plana, sin alabeo. Avellanados limpios; cierra sobre M3f.",
    "14_M3f_marco_bolsillo_x2": "Agujeros de insertos M3 abiertos. Asienta en las orejas de M1s.",
    "15_M4_capsula_cuerpo_x2": "Asiento de la ventana Ø30 limpio y sin hilos. Cara de junta plana. Sin capas abiertas.",
    "16_M5s_capsula_tapa_pie_x2": "Ranura de junta limpia. Ranura de cable 8 x 22 libre. Silla y agujeros M3 sin restos de soporte.",
    "17_M6_capsula_bisel_x2": "Anillo plano y entero. 3 agujeros M2 abiertos en cada uno.",
    "18_M11_bandeja": "Plana. Muescas y postes enteros; 4 pasantes M3 libres.",
    "19_M11_bandeja_sup": "Plana y sin alabeo: tiene 3 mm. Coinciden sus agujeros con M11.",
    "30_B1_casco_mitad_x2": "Postes de 16 mm enteros. Costillas sin capas abiertas. Soporte fuera de las bahías. Pines Ø5 y agujeros de unión coinciden entre mitades.",
    "31_B2_cubierta_lisa": "Barras rectas y enteras. Agujeros M3 limpios. Pilares sin grietas en la base.",
    "32_B2_cubierta_mastil": "Igual que la lisa; además, base del mástil entera y sin grietas.",
    "33_B3_caja": "Ranura del cordón limpia y brida plana. 3 pasos PG7 abiertos. Sin capas abiertas: es volumen seco.",
    "34_B4_tapa": "Cara de cierre plana contra un vidrio. 14 agujeros M3 coinciden con B3.",
    "35_B5_cuna_base_x2": "Lengüetas enteras. Agujeros M3 limpios. La botella asienta sin forzar.",
    "36_B5_cuna_cuello_x2": "Lengüetas enteras. Asiento del cuello limpio. Agujeros de unión coinciden con la base.",
    "37_B6_correa_x4": "Sin grietas en los extremos. Agujeros M3 abiertos.",
    "50_T1_caja": "PLA. Ranura 2,6 x 1,5 limpia. 4 postes M2,5 enteros. Agujero de la SMA y boca USB-C libres.",
    "51_T2_tapa": "PLA. Cara plana. Rebaje de la ventana OLED limpio. 4 agujeros M3 coinciden con T1.",
}
FASES = [
    ("Fase 1. Aro y gancho: la prueba más barata", [("40_LR2_aro_x4", 1), ("12_M3s_riel_gancho_x2", 1)],
     "Imprimir solo 1 aro y 1 riel. Comprobar a mano: el gancho de M3s entra en el aro sin forzar y no baila de más (juego de diseño: 0,3 mm por lado). Si no encaja, parar aquí: no imprimir nada más."),
    ("Fase 2. Caja y prueba de agua", [("10_M1s_caja_cuerpo", 1), ("11_M2_caja_tapa", 1)],
     "Prueba con la caja vacía, ANTES de meter electrónica: cordón Ø2 en la ranura y tapa cerrada con sus 12 M3. Tapar las 2 ventanas de las paredes con placas planas de prueba y junta (4 M4 cada una) y el paso PG7 con prensaestopas y tapón: si no, entra agua por ahí. Papel seco adentro, sumergir 30 min en un balde con peso encima. Abrir: el papel debe salir seco. Si se moja, corregir antes de seguir."),
    ("Fase 3. Resto del nodo", [("12_M3s_riel_gancho_x2", 1), ("40_LR2_aro_x4", 3), ("13_M3t_tapa_bolsillo_x2", 2), ("14_M3f_marco_bolsillo_x2", 2), ("15_M4_capsula_cuerpo_x2", 2),
                                ("16_M5s_capsula_tapa_pie_x2", 2), ("17_M6_capsula_bisel_x2", 2), ("18_M11_bandeja", 1), ("19_M11_bandeja_sup", 1)], "Incluye el segundo riel y los otros 3 aros."),
    ("Fase 4. Boya", [("30_B1_casco_mitad_x2", 2), ("31_B2_cubierta_lisa", 1), ("32_B2_cubierta_mastil", 1), ("33_B3_caja", 1), ("34_B4_tapa", 1), ("35_B5_cuna_base_x2", 2), ("36_B5_cuna_cuello_x2", 2), ("37_B6_correa_x4", 4)], ""),
    ("Fase 5. Caja de tierra, en PLA", [("50_T1_caja", 1), ("51_T2_tapa", 1)], "Antes de imprimir, confirmar las medidas reales del Heltec, la batería y la SMA."),
]


def leeme():
    import pymupdf as fitz
    font = "C:/Windows/Fonts/arial.ttf"
    bold = "C:/Windows/Fonts/arialbd.ttf"
    doc = fitz.open()
    W, H, M = 842, 595, 28
    y = [H]
    page = [None]

    def new():
        page[0] = doc.new_page(width=W, height=H)
        page[0].insert_font(fontname="a", fontfile=font)
        page[0].insert_font(fontname="b", fontfile=bold)
        y[0] = M

    def text(s, size=9, name="a", gap=3):
        width = W - 2 * M
        h = (int(fitz.get_text_length(s, fontname="helv", fontsize=size) * 1.15 / width) + 1) * size * 1.3 + 5
        if y[0] + h > H - M:
            new()
        page[0].insert_textbox(fitz.Rect(M, y[0], M + width, y[0] + h + 2), s, fontname=name, fontsize=size)
        y[0] += h + gap

    def table(head, rows, widths, size=7.4):
        def row(cells, name, fill=None):
            n = max(int(fitz.get_text_length(str(v), fontname="helv", fontsize=size) * 1.04 / (w - 5)) + 1 for v, w in zip(cells, widths))
            h = n * size * 1.28 + 3.5
            if y[0] + h > H - M:
                new()
                row(head, "b", (0.88, 0.91, 0.95))
            if fill:
                page[0].draw_rect(fitz.Rect(M, y[0], M + sum(widths), y[0] + h), color=None, fill=fill)
            x = M
            for v, w in zip(cells, widths):
                page[0].insert_textbox(fitz.Rect(x + 2, y[0] + 1, x + w - 1, y[0] + h + 2), str(v), fontname=name, fontsize=size)
                x += w
            page[0].draw_line((M, y[0] + h), (M + sum(widths), y[0] + h), color=(0.75, 0.75, 0.75), width=0.4)
            y[0] += h
        row(head, "b", (0.88, 0.91, 0.95))
        for r in rows:
            row(r, "a")
        y[0] += 5

    es = lambda v, d=0: f"{v:.{d}f}".replace(".", ",")
    by = {p[0]: p for p in PZ}
    m = re.search(r"\*\*Total: (\d+) g, (\d+) h\*\*", (MOD / "cad_final" / "BOM.md").read_text(encoding="utf-8"))
    tg, th = int(m[1]), int(m[2])
    new()
    text(TITLE, 15, "b", gap=2)
    text("Orden pensado para fallar barato. Bambu Lab P1P, boquilla 0,4 mm, capa de 0,2 mm, PETG; solo T1 y T2 en PLA. No se imprimen probetas. "
         "El número de cada pestaña identifica la pieza y su plano; el orden de impresión es el de estas fases, no el de los números.", 9)
    text(f"Total: {es(tg)} g y unas {es(th)} h, {sum(p[4] for p in PZ)} piezas. Con 4 rollos de 1 kg quedan unos {es(4000 - tg)} g: no alcanza para repetir una pieza grande. "
         "Los gramos y horas de aro, T1, T2 y M3s son estimados; el resto, de slicer.", 8.5, "b")
    head = ("Imprimir", "Pieza", "g c/u", "h c/u", "Per.", "Relleno", "Capas", "Sop.", "Qué revisar al sacarla de la cama")
    widths = (34, 122, 26, 26, 22, 58, 104, 24, 370)
    for title, rows, note in FASES:
        text(title, 10.5, "b", gap=1)
        if note:
            text(note, 8.2, gap=2)
        table(head, [(f"{q} de {by[n][4]}" if q != by[n][4] else str(q), n, es(by[n][5]), es(by[n][6], 1), by[n][7], by[n][8], by[n][9], by[n][10], REVISAR[n]) for n, q in rows], widths)
    text("Dónde están los archivos", 10.5, "b", gap=1)
    text(f"Drive, carpeta LanternGuard_CAD / 08_PARA_IMPRIMIR: STL, 3MF y PDF de planos con estos mismos números. PENDIENTE: se crea desde la PC de casa; hasta entonces no existe. Raíz: {DRIVE}", 8.2)
    text("Faltan 3MF con perfil real de LR2_aro, T1, T2 y M3s con el asiento Ø17,1: la placa P12 anterior NO sirve. Pasarlos por OrcaSlicer en la PC de casa.", 8.2)
    new()
    text("Tornillos, espuma y materiales que no se imprimen (BOM.md)", 11, "b")
    table(("Conjunto", "Componente", "Medida", "Cant."), hardware(), (46, 560, 130, 50), size=7.2)
    text("Para la prueba de agua de la fase 2, además: 2 placas planas (acrílico o aluminio) con junta, 8 M4 y 1 tapón para el PG7. "
         "Lastre: 990 g calculado; confirmar pesando en agua. La espuma de poliuretano es obligatoria.", 8.5, "b")
    OUT.mkdir(parents=True, exist_ok=True)
    doc.save(LEEME)
    return dict(paginas=len(doc), gramos=round(tg), horas=round(th, 1), piezas=sum(p[4] for p in PZ))


def local():
    STEP.mkdir(parents=True, exist_ok=True)
    res = dict(ensambles=assemblies(), leeme=leeme())
    (OUT / "local.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False)[:1800])


def copiar(c):
    S = state()
    if S.get("did"):
        return S
    r = c.call("POST", f"/documents/{SRC_DID}/workspaces/{SRC_WID}/copy", {"newName": TITLE, "isPublic": False})
    S.update(did=r["newDocumentId"], wid=r["newWorkspaceId"], url=f"https://cad.onshape.com/documents/{r['newDocumentId']}/w/{r['newWorkspaceId']}")
    keep(S)
    c.call("POST", f"/documents/{S['did']}", {"parentId": OP.FOLDER, "description": "Piezas de LanternGuard listas para imprimir. Empieza por la pestaña 00_LEEME."})
    print("copia", S["url"], used())
    return S


def tabs_of(c, S):
    return OP.tabs(c, S["did"], S["wid"])


def limpiar(c):
    S = state()
    did, wid = S["did"], S["wid"]
    tabs = tabs_of(c, S)
    by = {e["name"]: e for e in tabs}
    if "pid" not in S:
        S["pid"] = next(p["propertyId"] for p in c.call("GET", f"/metadata/d/{did}/w/{wid}/e/{by['T2_tapa']['id']}")["properties"] if p["name"] == "Name")
        keep(S)
    studios = {p[1]: p[0] for p in PZ if p[1]}
    planos = {v: plano_de(k) for k, v in PLANOS_OK.items()}
    missing = [n for n in list(studios) + list(planos) if n not in by and n not in S.get("renombradas", {})]
    if missing:
        raise SystemExit(f"faltan en la copia: {missing}")
    made = {i for u in S.get("subidas", {}).values() for i in [u["blob"], *u["elementos"]]} | {S.get("leeme")} | {d["id"] for d in S.get("planos", {}).values()}
    doomed = [e for e in tabs if e["name"] not in studios and e["name"] not in planos and e["name"] not in EN_USO
              and e["name"] not in S.get("renombradas", {}).values() and e["id"] not in made]
    if not S.get("renombradas") and len(doomed) != 64:              # 65 less the blob of the deletion test, already gone
        raise SystemExit(f"se esperaban 64 pestanas a borrar, salen {len(doomed)}")
    order = {"APPLICATION": 0, "ASSEMBLY": 2, "PARTSTUDIO": 1, "BILLOFMATERIALS": 3, "BLOB": 4}
    doomed.sort(key=lambda e: order.get(e["elementType"], 9))
    print("a borrar", len(doomed), "a renombrar", len(studios) + len(planos), "usadas", used(), flush=True)
    test = S.setdefault("prueba_blob", {})
    if not test.get("hecha"):
        st = by["OLD (usado por Drawing 10) M3t_tapa_bolsillo"]
        f = c.call("GET", f"/partstudios/d/{did}/w/{wid}/e/{st['id']}/features")
        fs = f.get("featureStates", {})
        fs = fs.items() if isinstance(fs, dict) else [(x.get("key"), x.get("value")) for x in fs]
        test.update(hecha=True, borrado=True, estado={k: (v or {}).get("featureStatus") for k, v in fs}, tipos=[x.get("featureType") for x in f.get("features", [])])
        keep(S)
        print("prueba blob", test, flush=True)
    bom_gone = False
    for e in doomed:
        if e["elementType"] == "BILLOFMATERIALS" and not bom_gone:
            now = {x["id"] for x in tabs_of(c, S)}
            bom_gone = True
            doomed_ids = {x["id"] for x in doomed}
            S["bom_en_cascada"] = sum(1 for i in doomed_ids if i not in now)
            skip = doomed_ids - now
            keep(S)
        if bom_gone and e["id"] in skip:
            continue
        c.call("DELETE", f"/elements/d/{did}/w/{wid}/e/{e['id']}")
    print("borradas", len(doomed), "usadas", used(), flush=True)
    ren = S.setdefault("renombradas", {})
    for old, new in {**studios, **planos}.items():
        if old in ren:
            continue
        c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{by[old]['id']}", {"properties": [{"propertyId": S["pid"], "value": new}]})
        ren[old] = new
        keep(S)
    print("renombradas", len(ren), "usadas", used(), flush=True)


def upload(c, S, name, path):
    did, wid = S["did"], S["wid"]
    body, ctype = OS.multipart({"encodedFilename": f"{name}.step", "translate": "true", "storeInDocument": "true", "importWithinDocument": "true",
                                "yAxisIsUp": "false", "flattenAssemblies": "true"}, path)
    r = c.call("POST", f"/blobelements/d/{did}/w/{wid}", body, ctype)
    t = c.wait_translation(r["translationId"])
    if t.get("requestState") != "DONE":
        raise OS.OnshapeError(f"{name}: traduccion {t.get('requestState')}: {t.get('failureReason')}")
    return r["id"], t["resultElementIds"]


def subir(c):
    S = state()
    did, wid = S["did"], S["wid"]
    U = S.setdefault("subidas", {})
    todo = [(n, STEP / f"{n}.step") for n in ENSAMBLES] + [(p[0], p[3]) for p in PZ if not p[1]]
    for name, path in todo:
        if name in U:
            continue
        blob, res = upload(c, S, name, path)
        sid = next((e for e in res if e != blob), res[0])
        parts = c.call("GET", f"/parts/d/{did}/w/{wid}/e/{sid}")
        solids = OP.step_parts(path)[1]
        refs = [p for p in parts if p.get("name", "").lower().startswith("ref")]
        U[name] = dict(blob=blob, estudio=sid, elementos=res, partes=len(parts), solidos=solids, verificado=len(parts) == solids, part0=parts[0]["partId"],
                       impresas=len(parts) - len(refs), refs=len(refs), color_ref=(refs[0].get("appearance", {}).get("color") if refs else None))
        keep(S)
        print(name, {k: U[name][k] for k in ("partes", "solidos", "impresas", "refs", "color_ref")}, used(), flush=True)
    if not S.get("leeme"):
        body, ctype = OS.multipart({"encodedFilename": "00_LEEME.pdf", "translate": "false", "storeInDocument": "true"}, LEEME)
        S["leeme"] = c.call("POST", f"/blobelements/d/{did}/w/{wid}", body, ctype)["id"]
        keep(S)
    if "link" not in S:
        try:
            c.call("POST", f"/documents/{did}/acl/anonymousAccess", {"anonymousAccessAllowed": True, "anonymousAllowsExport": True})
            S["link"] = "ok"
        except OS.OnshapeError as e:
            S["link"] = f"a mano: {str(e)[:120]}"
        keep(S)
    print("leeme", S["leeme"], "link", S["link"], "usadas", used(), flush=True)


def pid_of(c, S, name, tabs):
    U = S.get("subidas", {}).get(name)
    if U:
        return U["estudio"], U["part0"]
    eid = next(e["id"] for e in tabs if e["name"] == name)
    return eid, None


def planos(c, reserve=4):
    """Full A4 sheet (views, dimensions, notes) while calls allow; PDFs stay for the home PC."""
    S = state()
    did, wid = S["did"], S["wid"]
    P.REG = OUT / "registro_planos.json"
    OUT.mkdir(parents=True, exist_ok=True)
    P.export_pdf = lambda *a, **k: None
    P.use_format("equipo")
    P.LIMIT = P.LIMIT_A4 = 2500
    import publicar_tierra as T
    P.wait_modify = lambda cl, d, w, e, reqs, desc: wm(cl, d, w, e, reqs, desc, T)
    R = P.reg()
    R["documento"] = {"did": did, "wid": wid}
    P.save(R)
    tabs = tabs_of(c, S)
    D = S.setdefault("planos", {})
    want = [p for p in PZ if p[0] not in PLANOS_OK]
    want.sort(key=lambda p: (p[1] is None, p[0]))                  # pieces of the BOM before the probetas
    for row in want:
        name, code, stp, qty = row[0], row[2], row[3], row[4]
        if name in D:
            continue
        left = sum(1 for p in want if p[0] not in D) - 1
        remaining = MAX - used() - reserve
        full = remaining - FULL >= SIMPLE * left
        if remaining < SIMPLE:
            S["planos_faltan"] = [p[0] for p in want if p[0] not in D]
            keep(S)
            print("sin presupuesto; faltan", S["planos_faltan"], flush=True)
            return
        eid, pid = pid_of(c, S, name, tabs)
        _names[f"PLANO_A4_{code}"] = plano_de(name)
        R = P.reg()
        rec = R.setdefault("piezas", {}).setdefault(code, {"partstudio": eid, "pestana": name, "propiedades": []})      # keeps a drawing already started
        if pid:
            rec["pid"] = pid
        P.save(R)
        if not full:
            D[name] = sin_cotas(c, did, wid, name, code, stp, qty, eid, pid)
            keep(S)
            print(name, "sin cotas", "usadas", used(), flush=True)
            continue
        a4 = P.piece_a4(code, stp, qty, c, {"elements": {}, "name_pid": None}, chamfer=None if row[1] else ())
        D[name] = dict(id=a4["drawing"], url=f"https://cad.onshape.com/documents/{did}/w/{wid}/e/{a4['drawing']}", cotas=a4.get("cotas"), escala=a4.get("escala"))
        keep(S)
        print(name, a4.get("cotas", {}).get("creadas"), "usadas", used(), flush=True)


def sin_cotas(c, did, wid, name, code, stp, qty, eid, pid):
    """Views, title block and notes when the budget no longer pays for dimensions."""
    lo, hi = P.bbox(stp)
    (num, den), iso, centres, _ = P.best_layout(lo, hi)
    d = c.call("POST", f"/drawings/d/{did}/w/{wid}/create", {
        "drawingName": plano_de(name), "elementId": eid, "partId": pid, "views": "zero", "titleblock": True, "border": True, "units": "MILLIMETER",
        "projection": "First", "size": "A4", "standard": "ISO", "decimalSeparator": "COMMA"})
    md = _new.get("md") or c.call("GET", f"/metadata/d/{did}/w/{wid}/e/{d['id']}")
    ids = {p["name"]: p["propertyId"] for p in md.get("properties", [])}
    want = {k: v for k, v in P.CAJETIN(code).items() if k in ids}
    c.call("POST", f"/metadata/d/{did}/w/{wid}/e/{d['id']}", {"properties": [{"propertyId": ids[k], "value": v} for k, v in want.items()]})
    views = [{"viewType": "TopLevel", "position": {"x": x, "y": y}, "orientation": o, "reference": {"elementId": eid},
              "scale": {"scaleSource": "Custom", "numerator": (iso if o == "isometric" else (num, den))[0], "denumerator": (iso if o == "isometric" else (num, den))[1]}}
             for o, (x, y) in centres.items()]
    P.wait_modify(c, did, wid, d["id"], [{"messageName": "onshapeCreateViews", "formatVersion": "2021-01-01", "views": views}], f"vistas {code}")
    note = f"Cantidad: {qty}   ·   Material: PETG   ·   Sin cotas: medidas en el modelo"
    anns = P.title_notes(code) + [{"type": "Onshape::Note", "note": {"position": {"type": "Onshape::Reference::Point", "coordinate": [P.TITLE[0] + 2, P.TITLE[3] + 4, 0]},
                                                                      "contents": note, "textHeight": P.TEXT_H}}]
    c.call("POST", f"/drawings/d/{did}/w/{wid}/e/{d['id']}/modify", {"description": f"notas {code}"[:32], "jsonRequests": [
        {"messageName": "onshapeCreateAnnotations", "formatVersion": "2021-01-01", "annotations": anns}]})
    return dict(id=d["id"], url=f"https://cad.onshape.com/documents/{did}/w/{wid}/e/{d['id']}", cotas=None, escala=f"{num}:{den}")


def wm(c, did, wid, eid, reqs, desc, T):
    r = c.call("POST", f"/drawings/d/{did}/w/{wid}/e/{eid}/modify", {"description": desc[:32], "jsonRequests": reqs})
    time.sleep(35)
    for _ in range(4):
        s = c.call("GET", f"/drawings/modify/status/{r['id']}")
        if s.get("requestState") != "ACTIVE":
            res = json.loads(s["output"]) if s.get("output") else s
            q = reqs[0]
            bad = [i for i, x in enumerate(res.get("results", [])) if x.get("status") != "OK"]
            if bad and "annotations" in q and not desc.endswith("(2)"):
                T.clean(q)
                q["annotations"][:] = [a for i, a in enumerate(q["annotations"]) if i not in bad]
                return wm(c, did, wid, eid, reqs, desc + " (2)", T)
            return res
        time.sleep(25)
    raise OS.OnshapeError(f"modify {desc} sigue ACTIVE")


def verificar(c):
    S = state()
    did, wid = S["did"], S["wid"]
    tabs = tabs_of(c, S)
    refs = c.call("GET", f"/appelements/d/{did}/w/{wid}/resolvereferences")
    by = {e["name"]: e for e in tabs}
    ids = {e["id"]: e["name"] for e in tabs}
    rotas = [e["name"] for e in tabs if e["id"] in refs and (refs[e["id"]].get("unresolvedReferenceIds") or any(
        r.get("errorCode") or r.get("targetElementId") not in ids for r in refs[e["id"]]["resolvedReferences"]))]
    mal, faltan, esperadas = [], [], set(ENSAMBLES) | {"00_LEEME.pdf", "00_LEEME"}
    for p in PZ:
        name, pl = p[0], plano_de(p[0])
        esperadas |= {name, pl, f"{name}.step"}
        if p[1]:
            esperadas.add(f"{p[1]}.step")
        if name not in by:
            faltan.append(name)
        if pl not in by:
            faltan.append(pl)
        elif name in by:
            tg = {r.get("targetElementId") for r in refs.get(by[pl]["id"], {}).get("resolvedReferences", [])}
            if tg != {by[name]["id"]}:
                mal.append((pl, sorted(ids.get(t, t) for t in tg)))
    esperadas |= {f"{n}.step" for n in ENSAMBLES}
    sobran = [e["name"] for e in tabs if e["name"] not in esperadas]
    S["verificacion"] = dict(pestanas=len(tabs), rotas=rotas, faltan=faltan, plano_mal_apuntado=mal, sobran=sobran,
                             blobs_en_uso=sum(e["elementType"] == "BLOB" for e in tabs) - 1, llamadas=used())
    keep(S)
    print(json.dumps(S["verificacion"], ensure_ascii=False))


def nuevo(pl, txt):
    """T1 and T2 in PLA; the ring drawing quotes the hook seat."""
    if "LR2" in pl:
        return re.sub(r"juego(\s+)0,3", r"juego\g<1>0,6", txt.replace("Ø16,8", "Ø17,1"))
    return txt.replace("PETG", "PLA")


def sin_probetas(c):
    """Team decision of 05/11: no probetas, M3s with the Ø17.1 seat, T1 and T2 in PLA. Counter of its own: the 250 belonged to the previous job."""
    S = state()
    did, wid = S["did"], S["wid"]
    tabs = tabs_of(c, S)
    by = {e["name"]: e for e in tabs}
    doomed = []
    for n in PROBETAS_FUERA:
        doomed += [n, plano_de(n), "PB_aro.step" if n == "06_PB_aro" else f"{n}.step"]
    doomed += [plano_de("12_M3s_riel_gancho_x2"), "12_M3s_riel_gancho_x2", "M3s_riel_gancho.step", "00_ENSAMBLE_nodo", "00_ENSAMBLE_nodo.step", "00_LEEME.pdf"]
    done = S.setdefault("cambio_0511", {})
    if not done.get("borradas"):
        for n in doomed:                                            # drawings before studios before blobs: the order of the list
            if n in by:
                c.call("DELETE", f"/elements/d/{did}/w/{wid}/e/{by[n]['id']}")
        for n in PROBETAS_FUERA:
            S["planos"].pop(n, None)
            S["subidas"].pop(n, None)
        S["subidas"].pop("00_ENSAMBLE_nodo", None)
        done["borradas"] = doomed
        keep(S)
    print("borradas", len(doomed), "usadas", used(), flush=True)
    U = S["subidas"]
    for name, path in (("12_M3s_riel_gancho_x2", N.STEPS["M3s_riel_gancho"]), ("00_ENSAMBLE_nodo", STEP / "00_ENSAMBLE_nodo.step")):
        if name in U:
            continue
        blob, res = upload(c, S, name, path)
        sid = next((e for e in res if e != blob), res[0])
        parts = c.call("GET", f"/parts/d/{did}/w/{wid}/e/{sid}")
        refs = [p for p in parts if p.get("name", "").lower().startswith("ref")]
        U[name] = dict(blob=blob, estudio=sid, elementos=res, partes=len(parts), solidos=OP.step_parts(path)[1], part0=parts[0]["partId"], impresas=len(parts) - len(refs), refs=len(refs))
        keep(S)
        print(name, U[name]["partes"], U[name]["solidos"], U[name]["impresas"], "usadas", used(), flush=True)
    planos(c)
    S = state()
    if not done.get("leeme"):
        body, ctype = OS.multipart({"encodedFilename": "00_LEEME.pdf", "translate": "false", "storeInDocument": "true"}, LEEME)
        S["leeme"] = c.call("POST", f"/blobelements/d/{did}/w/{wid}", body, ctype)["id"]
        S.setdefault("cambio_0511", {})["leeme"] = True
        keep(S)
    print("leeme", S["leeme"], "usadas", used(), flush=True)
    import publicar_tierra as T
    P.wait_modify = lambda cl, d, w, e, reqs, desc: wm(cl, d, w, e, reqs, desc, T)
    tabs = {e["name"]: e for e in tabs_of(c, S)}
    for pl in (plano_de("50_T1_caja"), plano_de("51_T2_tapa"), plano_de("40_LR2_aro_x4")):
        if S["cambio_0511"].get(pl):
            continue
        eid = tabs[pl]["id"]
        t = c.call("POST", f"/drawings/d/{did}/w/{wid}/e/{eid}/translations", {"formatName": "DRAWING_JSON", "storeInDocument": False})
        time.sleep(30)
        t = c.call("GET", f"/translations/{t['id']}")
        COUNT.write_text(str(used() + 1))
        req = urllib.request.Request(OS.API + f"/documents/d/{did}/externaldata/{t['resultExternalDataIds'][0]}", headers={"Authorization": c.auth})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode("utf-8"))
        edits = [{"type": "Onshape::Note", "note": {"logicalId": a["note"]["logicalId"], "contents": nuevo(pl, a["note"]["contents"])}}
                 for a in d["sheets"][0]["annotations"] if a["type"] == "Onshape::Note" and nuevo(pl, a["note"].get("contents") or "") != (a["note"].get("contents") or "")]
        r = wm(c, did, wid, eid, [{"messageName": "onshapeEditAnnotations", "formatVersion": "2021-01-01", "annotations": edits}], f"PLA {pl}", T)
        S["cambio_0511"][pl] = dict(notas=len(edits), resultado=[x.get("status") for x in r.get("results", [])])
        keep(S)
        print(pl, S["cambio_0511"][pl], "usadas", used(), flush=True)


def main():
    ap = argparse.ArgumentParser()
    for f in ("local", "copiar", "limpiar", "subir", "planos", "verificar", "sin_probetas"):
        ap.add_argument(f"--{f}", action="store_true")
    a = ap.parse_args()
    if a.sin_probetas:                                              # new job, new counter and a lower stop
        global COUNT, MAX
        COUNT, MAX = OUT / "_llamadas_sin_probetas.txt", 70
        if not COUNT.exists():
            COUNT.write_text("0")
    if a.local:
        local()
    if not (a.copiar or a.limpiar or a.subir or a.planos or a.verificar or a.sin_probetas):
        return
    c = client()
    if a.copiar:
        copiar(c)
    if a.limpiar:
        limpiar(c)
    if a.subir:
        subir(c)
    if a.planos:
        planos(c)
    if a.sin_probetas:
        sin_probetas(c)
    if a.verificar:
        verificar(c)
    print("llamadas", used())


if __name__ == "__main__":
    sys.exit(main())
