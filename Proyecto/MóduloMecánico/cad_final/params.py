"""LanternGuard CAD final: single source of truth for every dimension (mm, g, MPa, kg/m3 as noted).

Every value is registered with p(key, value, origen, estado, razon, anterior):
  origen  : medido | fabricante | equipo | estimado
            ("equipo" = decided by the team or fixed by PROMPT_CC_CAD_FINAL.md;
             "estimado" = assumption or design proposal, to be confirmed)
  estado  : confirmado | por_verificar
  anterior: value in cad/params.py (or the handoff when the old script had none); None = new.
Derived quantities (cavity, box size, positions) are NOT entered here: layout.py computes them.
The table "parametro | anterior | nuevo | razon | estado" is generated from REGISTRO.
"""
import math
from dataclasses import dataclass

ORIGENES = ("medido", "fabricante", "equipo", "estimado")
ESTADOS = ("confirmado", "por_verificar")


@dataclass(frozen=True)
class Param:
    key: str
    value: object
    origen: str
    estado: str
    razon: str = ""
    anterior: object = None


REGISTRO: dict = {}


def p(key, value, origen, estado, razon="", anterior=None):
    assert origen in ORIGENES, f"{key}: origen '{origen}' no valido"
    assert estado in ESTADOS, f"{key}: estado '{estado}' no valido"
    assert key not in REGISTRO, f"{key} registrado dos veces"
    REGISTRO[key] = Param(key, value, origen, estado, razon, anterior)
    return value


EST, VER, OK = "estimado", "por_verificar", "confirmado"

# =====================================================================================
# COMUN (lo leen nodo y boya; si una fase necesita cambiarlo, lo reporta, no lo edita)
# =====================================================================================
PRINT_BED = p("impresora.cama", (220.0, 220.0, 250.0), EST, VER,
              "Impresora real desconocida", (220.0, 220.0, 250.0))
PIECE_MAX_L = p("pieza.largo_max", 150.0, "equipo", OK,
                "Prompt v2: ninguna pieza > 150 salvo la caja")
MIN_WALL = p("impresion.espesor_min", 1.2, "equipo", OK, "3 perimetros de 0.4", 1.2)
SHELL_T = p("impresion.cascara", 1.2, EST, VER,
            "Perimetros + capas sup/inf macizos, para la masa con relleno", None)
INFILL_CASES = p("impresion.relleno", (0.40, 1.00), "equipo", OK,
                 "Piezas no selladas (bandeja, ganchos, carros...): se reportan 40 % y 100 %")
INFILL_SEALED = p("impresion.relleno_sellado", 1.0, "equipo", OK,
                  "M1, M2, M4, M5 y tramos del riel al 100 % (revision 28/10, C13)", 0.4)
SEALED_PIECES = p("impresion.piezas_selladas", ("M1", "M2", "M4", "M5", "M3_riel_central", "M3_riel_ext"),
                  "equipo", OK, "Piezas que van al 100 % con 5 perimetros")
SEALED_PERIMETERS = p("impresion.perimetros_sellado", 5, "equipo", OK, "5 perimetros (2.0 mm con boquilla 0.4)")
FIT_CLEAR = p("impresion.holgura", 0.3, EST, VER, "Handoff; probar con el peine de la Fase B", 1.0)
HOLE_COMP = p("impresion.comp_agujero", 0.2, EST, VER, "Handoff; probar en impresora real")

PETG_DENSITY = p("petg.densidad", 1.27, EST, VER, "Sustituir por el dato del slicer", 1.27)   # g/cm3
PETG_E = p("petg.E", 1700.0, EST, VER, "PETG manual para SimScale")                            # MPa
PETG_NU = p("petg.nu", 0.38, EST, VER, "PETG manual")
PETG_YIELD = p("petg.sigma_y", 45.0, EST, VER, "Macizo, a lo largo de las capas", 45.0)        # MPa
PETG_YIELD_Z = p("petg.sigma_capas", 22.0, EST, VER, "Entre capas, mitad del macizo")          # MPa
ACRYLIC_DENSITY = p("acrilico.densidad", 1.19, "fabricante", OK, "PMMA", 1.19)                 # g/cm3
STEEL_DENSITY = p("acero_inox.densidad", 7.9, "fabricante", OK, "Lastre de tuercas o pernos A2")  # g/cm3

SEAWATER_DENSITY = p("agua.densidad", 1.025, EST, OK, "Agua de mar de referencia", 1.025)      # g/cm3
DESIGN_DEPTH_M = p("profundidad_m", 1.0, "equipo", OK, "Prueba real: 1 m varios dias. No se afirma 15 m", 15.0)
DESIGN_PRESSURE = SEAWATER_DENSITY * 1000 * 9.81 * DESIGN_DEPTH_M / 1e6   # MPa (0.0101), derivado
AIR_MASS_MAX_KG = p("peso_aire_max_kg", 3.0, "equipo", OK, "Lista de exigencias", 3.0)

# =====================================================================================
# NODO SUMERGIDO
# =====================================================================================
# ---------------------------------------------------------------- linterna de prueba
RING_DIAMETERS = p("aro.diametros", (100.0, 200.0, 300.0, 500.0), "equipo", OK,
                   "Nodo ajustable de Ø100 a Ø500; un ensamble por aro", 500.0)
RING_OFFSET = p("aro.offset_cuerda", 0.0, "equipo", OK, "La barra cruza el aro por el centro", 0.0)
RING_ROD_DIAMETERS = p("aro.varilla_D", (6.0, 8.0, 10.0, 12.0), EST, VER,
                       "Varilla real sin medir: un casquillo por diametro", 12.0)
RING_CORDS = p("aro.cuerdas", 4, "equipo", VER, "3 o 4 cuerdas desde el borde; sin cabo central")

# ---------------------------------------------------------------- riel modular (M3)
RAIL_SECTION = p("riel.seccion", 30.0, "equipo", OK, "Cuadrado 30 x 30, hueco = conducto inundado", (30.0, 25.0))
RAIL_WALL = p("riel.pared", 4.0, "equipo", OK, "Prompt v2", 3.0)
RAIL_CENTRAL_L = p("riel.central_L", 140.0, "equipo", OK, "M3_riel_central bajo la caja", 190.0)
RAIL_EXT_L = p("riel.ext_L", 100.0, "equipo", OK,
               "Paso de M3_riel_ext: cada extension suma 100; la pieza mide 100 + 15 de lengueta macho (decision 29/10, C18)")
RAIL_EXT_PER_RING = p("riel.extensiones", {100.0: 0, 200.0: 1, 300.0: 1, 500.0: 2}, "equipo", OK,
                      "0 / 1 / 2 extensiones por lado: riel de 230 (Ø100), 430 (Ø200-300), 630 (Ø400-500)")
RAIL_TIP_L = p("riel.punta_L", 45.0, "equipo", OK,
               "M3_riel_punta: 45 de cuerpo + 15 de union (pieza de 60), una por lado en todos los aros (29/10, C18)")
RAIL_TIP_END_T = p("riel.punta_tapa", 5.0, EST, VER,
                   "Pared del extremo de la punta donde apoyan la arandela y la tuerca de la varilla M8; deja abierta la "
                   "ranura T para meter las tuercas")
RAIL_DOVETAIL = p("riel.cola_milano", 15.0, "equipo", OK, "Macho/hembra 15 + 2 M4 pasantes")
RAIL_TSLOT = p("riel.ranura_T", {"abertura": 4.6, "ancho": 8.0, "alto": 3.6}, EST, VER,
               "Para tuerca M4 (AF7 x 3.2); se ajusta con la probeta de la Fase B")
RAIL_ROD_M8 = p("riel.varilla_M8", True, "equipo", OK,
                "Varilla roscada M8 obligatoria en todo el riel, tensada con tuerca + arandela en las dos puntas (29/10, C19)",
                False)
ROD_HOLE = p("riel.varilla_agujero", 8.5, "equipo", OK, "Agujero pasante de la varilla en cada tramo, alineado")
ROD_GRADE = p("riel.varilla_grado", "8.8", EST, VER, "8.8 o 4.6 (la que se compre); el calculo se hace con las dos")
ROD_CHANNEL_GAP = p("riel.varilla_aire_ranura", 1.0, EST, VER,
                    "Aire entre el techo del canal de tuercas (nervios) y el refuerzo de la varilla: pasan las tuercas y la "
                    "punta de un M4 x 14")
ROD_BOSS_WALL = p("riel.varilla_pared", 1.2, EST, VER, "Pared del refuerzo alrededor del agujero de 8.5 (minimo de impresion)")
ROD_CABLE_GAP = p("riel.varilla_aire_cable", 0.5, EST, VER, "Aire entre el refuerzo de la varilla y el Cat5e que va encima")
ROD_BULKHEAD_T = p("riel.varilla_tabique", 3.0, EST, VER,
                   "Espesor (a lo largo del riel) del tabique con el agujero de 8.5; uno en cada extremo del cuerpo de cada tramo")
ROD_WASHER = p("riel.varilla_arandela", (24.0, 2.0, 8.4), "fabricante", VER,
               "Arandela ancha DIN 9021 M8: Ø ext x espesor x Ø int (reparte el apriete sobre el PETG)")
ROD_NUT = p("riel.varilla_tuerca", (13.0, 6.5), "fabricante", VER, "Tuerca M8 DIN 934: entrecaras x alto")
ROD_PROTRUSION = p("riel.varilla_sobrante", 2.0, EST, VER, "Rosca que asoma pasada la tuerca en cada punta")
ROD_PRELOAD_N = p("riel.varilla_precarga", 500.0, EST, VER,
                  "Tension de apriete; con T = 0.2 d F son unos 0.8 N m. Reapretar tras unos dias (fluencia del PETG)")
ROD_PARTS_G = p("riel.varilla_masas", {"g_por_mm": 0.32, "tuerca": 5.0, "arandela": 6.5}, EST, VER,
                "Varilla M8 de acero cincado o inox, por mm; tuerca y arandela DIN 9021. Pesar")
# tramo central = camara de cables bajo la caja (revision 28/10, C12)
CHAMBER_H_TARGET = p("riel.camara_alto", 50.0, "equipo", OK,
                     "'Unos 50' de alto interior; el valor real se deriva (domo + radio + cable + nervio)")
CHAMBER_RAMP_DEG = p("riel.camara_rampa", 60.0, EST, VER,
                     "Techo en rampa hacia el conducto de 22. Con la varilla (C19) la camara crece 12.4 y a 45 grados la "
                     "rampa tapaba el domo del PG7; el central se imprime boca abajo, asi que la rampa queda como piso", 45.0)
CHAMBER_FLANGE_W = p("riel.camara_brida", (56.0, 4.0), EST, VER,
                     "Brida superior (ancho minimo x espesor): lleva los 4 M4 a la caja y cuelga los bolsillos "
                     "de la pletina; el ancho real lo fijan los bolsillos")
RAIL_WINDOW = p("riel.ventana_cable", (24.0, 14.0), EST, VER,
                "OBSOLETO desde la revision del 28/10: el tramo central es una camara de cables (riel.camara_*)")

# ---------------------------------------------------------------- ganchos y pequenas piezas
HOOK_CONTACT_W = p("gancho.contacto", 12.0, "equipo", OK, "Asiento de 12 con bordes R3")
HOOK_EDGE_R = p("gancho.radio_borde", 3.0, "equipo", OK, "")
HOOK_LOAD_N = p("gancho.carga_N", 75.0, "equipo", OK, "150 N repartidos en 2 ganchos")
KNOB_D = p("perilla.diametro", 30.0, "equipo", OK, "M12_perilla, para guante")
BUSHING_DIAMETERS = p("casquillo.D", (6.0, 8.0, 10.0, 12.0), "equipo", OK, "M13_casquillo_D6...D12")
LATCH_BUMP = p("pestillo.resalte", 0.6, "equipo", VER, "Traba del M14; probar en probeta")
STRAP_W = p("correa.ancho", 25.0, "equipo", OK, "Correa textil de seguridad", 26.0)
CARRIAGE_TRAVEL = p("carro.recorrido", 50.0, "equipo", OK, "M10_carro_capsula, +-50")
HANDLING_LOAD_N = p("carga.manipulacion_N", 150.0, "equipo", OK, "Caso de diseno a 1 m")

# ---------------------------------------------------------------- detalle de uniones (probetas Fase B)
M4_NUT = p("m4.tuerca", (7.0, 3.2), "fabricante", VER, "AF x espesor, DIN 934")
M4_HEAD = p("m4.cabeza", (7.0, 4.0), "fabricante", VER, "Allen DIN 912: Ø x alto")
M4_HEX_HEAD = p("m4.cabeza_hex", (7.0, 2.8), "fabricante", VER, "Perno hexagonal DIN 933: AF x alto (perilla)")
M3_NUT = p("m3.tuerca", (5.5, 2.4), "fabricante", VER, "AF x espesor, DIN 934")
RAIL_TSLOT_RIB = p("riel.ranura_T_nervio", 2.0, EST, VER,
                   "Nervios que encierran el canal de la tuerca sobre el fondo; la tuerca entra por la punta del tramo")
RAIL_LAP_Z = p("riel.union_z", 15.0, EST, VER,
               "Media madera: el macho conserva la mitad de abajo (con la ranura T), la hembra la de arriba")
RAIL_DOVETAIL_KEY = p("riel.cola_llave", (8.0, 11.0, 4.0), EST, VER,
                      "Llave en cola de milano vista de lado (base, punta, alto) en la cara de la media madera; "
                      "entra deslizando de costado")
RAIL_LAP_WALL = p("riel.union_pared", 10.0, EST, VER,
                  "Paredes engrosadas hacia adentro en la union para la tuerca M4 con 1.4 de piel; conducto local "
                  "10 de ancho: cada lado del riel lleva un solo Cat5e (5.5)")
RAIL_JOINT_BOLT_Y = p("riel.union_m4_y", 10.0, EST, VER,
                      "2 M4 verticales dentro de las paredes (y = +-10): no cruzan el conducto de cables")
JAW_BORE = p("gancho.alojamiento", 16.0, EST, VER, "Ø del asiento del casquillo en la J (varilla max 12 + pared)")
BUSHING_PRESS = p("casquillo.interferencia", 0.15, EST, VER, "Exceso de Ø del casquillo sobre el asiento")
BUSHING_ROD_CLR = p("casquillo.holgura_varilla", 0.4, EST, VER, "Ø interior = varilla + holgura")
BUSHING_FLANGE = p("casquillo.pestana", (20.0, 1.5), EST, VER, "Ø x espesor de la pestana de tope")
LATCH_PIVOT = p("pestillo.pivote", 3.0, "equipo", OK, "Pivote M3")
LATCH_TAB = p("pestillo.lengueta", (18.0, 12.0), EST, VER, "Largo x ancho de la lengueta para el pulgar con guante")
KNOB_H = p("perilla.alto", 12.0, EST, VER, "Alto de la perilla")
KNOB_LOBES = p("perilla.lobulos", 8, EST, VER, "Moleteado grueso para guante")
COMB_CLEARANCES = p("peine.holguras", (0.2, 0.3, 0.4, 0.5), "equipo", OK, "Peine de holguras de la Fase B")
COMB_PIN_D = p("peine.pin_D", 8.0, EST, VER, "Pin de prueba")
SEAL_COUPON = p("probeta.junta", (60.0, 60.0), "equipo", OK, "Cuadrado de 60 x 60 con ranura y 4 M3")

# probetas (Fase B): constantes de forma que propuso el modelado; Fase C reutiliza las del gancho/pestillo/perilla
COUPON_L = p("probeta.tramo_L", 40.0, EST, VER, "PB2/PB3 rail length per segment")
JAW_WALL = p("gancho.pared", 4.0, EST, VER, "minimum wall around the hook seat")
JAW_LIP_H = p("gancho.labio_alto", 10.0, EST, VER, "height of the upper lip that carries the latch pivot")
STRAP_SLOT_T = p("correa.ranura_t", 3.0, EST, VER, "strap slot thickness (slot is STRAP_W x this)")
STEM_H = p("gancho.vastago_alto", 20.0, EST, VER, "stem above the jaw, carries the M4 hole to bolt PB1 to PB2")
LATCH_T = p("pestillo.espesor", 3.6, EST, VER, "latch plate thickness (Y)")
LATCH_ARM_W = p("pestillo.brazo_ancho", 5.0, EST, VER, "latch arm width (X)")
LATCH_RIDGE_W = p("pestillo.cresta_ancho", 1.2, EST, VER, "catch ridge width on the jaw lip")
LATCH_TIP_GAP = p("pestillo.holgura_punta", 0.2, EST, VER, "closed latch tip to lip clearance")
LATCH_SWING = p("pestillo.giro_media_ranura", 4.5, EST, VER, "half width of the latch slot in the upper lip (swing room)")
KNOB_LOBE_R = p("perilla.lobulo_r", 3.5, EST, VER, "radius of each grip lobe")
KNOB_CAP = p("perilla.tapa_cabeza", 1.2, EST, VER, "roof over the embedded bolt head (print pause)")
SEAL_CAV_CORNER = p("probeta.junta_radio_cavidad", 14.0, EST, VER, "inner corner radius of the seal base cavity (land follows the groove path)")
SEAL_FILLET = p("probeta.junta_radio_ext", 2.0, EST, VER, "outer corner radius of the 60 x 60 seal parts")
COMB_PITCH = p("peine.paso", 18.0, EST, VER, "spacing of the comb holes")
COMB_T = p("peine.espesor", 6.0, EST, VER, "comb plate thickness")
COMB_W = p("peine.ancho", 26.0, EST, VER, "comb plate width")
COMB_TEXT_H = p("peine.texto_alto", 4.5, EST, VER, "engraved text height")
COMB_TEXT_DEPTH = p("peine.texto_prof", 0.6, EST, VER, "engraved text depth")
PIN_L = p("peine.pin_L", 8.0, EST, VER, "comb pin length")

# ---------------------------------------------------------------- piezas de la Fase C (formas propuestas, por verificar)
HOOK_FLANGE = p("gancho.brida", (50.0, 6.0), EST, VER,
                "Largo (a lo largo del riel) x espesor de la placa que apoya bajo el riel; el M4 de la perilla "
                "va en un extremo, fuera del alma, para que la perilla quede al alcance")
HOOK_DROP = p("gancho.caida", 40.0, EST, VER, "Fondo del riel al centro de la varilla del aro; medir con el aro real")
CARRIAGE_L = p("carro.largo", 60.0, EST, VER,
                "M10 a lo largo del riel: perilla atras (cilindro libre de 34) + 25 de quilla abulonada adelante", 40.0)
CARRIAGE_WALL = p("carro.pared", 4.0, EST, VER, "Manga en U invertida que abraza el tramo; la perilla aprieta en la T")
RAIL_EXIT_SLOT = p("riel.salida_cable", (8.0, 20.0, 10.0), EST, VER,
                   "Ranura lateral de salida del Cat5e en cada extension: alto x largo x distancia a la punta "
                   "exterior (prompt: sale junto al carro con bucle de 40)")
LENS_D = p("camara.lente_D", 16.0, EST, VER, "Porta-lente de la Arducam Mega; medir")
LED_SEPARATOR = p("aro_led.separador", (1.2, 3.0), EST, VER,
                  "Tubo opaco entre LED y lente: pared x alto sobre el aro. Con 1.5 el tubo (r 9.7) chocaba con el "
                  "agujero supuesto del anillo LED (r 9.5); el p1 de 1.19 es teselado sobre una pared de 1.2 exacta")

# ---------------------------------------------------------------- caja central (M1, M2)
ESP32_BASE = p("esp32.base", "sin_base", "equipo", OK, "Por defecto sin KIT A; 'kit_a' es la alternativa")
BOX_WALL = p("caja.pared", 4.0, "equipo", OK, "A 1 m la presion no manda (0.0101 MPa)", 5.0)
BOX_FLOOR = p("caja.fondo", 4.0, "equipo", OK, "Igual que la pared", 6.0)
BOX_LID_T = p("caja.tapa", 5.0, EST, VER, "Ranura de 1.5 deja 3.5 bajo la junta", 6.0)
BOX_FLANGE = p("caja.brida_ancho", 10.0, EST, VER, "Ranura + inserto M3 (agujero 4.0) con 3 mm de pared", 9.0)
BOX_FLANGE_T = p("caja.brida_espesor", 8.0, EST, VER, "Inserto M3 de 5.7 + 2 de fondo", 6.0)
BOX_SCREW_PITCH = p("caja.paso_tornillos", 65.0, EST, VER,
                    "Separacion maxima entre M3 de la tapa: compresion pareja de la junta", 76.0)
BOX_LID_GAP = p("caja.holgura_tapa", 5.0, EST, VER, "Aire libre entre lo mas alto y la tapa")
ORING_CORD = p("junta.cordon", 2.0, "equipo", OK, "Cordon Ø2, como ya esta", 2.0)
GROOVE_WIDTH = p("junta.ranura_ancho", 2.6, "equipo", OK, "", 2.6)
GROOVE_DEPTH = p("junta.ranura_prof", 1.5, "equipo", OK, "25 % de compresion", 1.5)
M3_CLEAR = p("m3.paso", 3.4, EST, VER, "", 3.4)
M3_INSERT_HOLE = p("m3.inserto_agujero", 4.0, EST, VER, "Inserto termico M3 x 5.7", 4.0)
M3_INSERT_DEPTH = p("m3.inserto_prof", 6.0, EST, VER, "", 6.0)
M4_CLEAR = p("m4.paso", 4.2, EST, VER, "", 4.2)
M4_INSERT_HOLE = p("m4.inserto_agujero", 5.6, EST, VER, "Inserto termico M4 x 8.1")
M4_INSERT_DEPTH = p("m4.inserto_prof", 8.5, EST, VER, "")
BASE_M4_PTS = p("caja.base_m4", ((40.0, 20.0), (40.0, -20.0), (-40.0, 20.0), (-40.0, -20.0)), EST, VER,
                "4 M4 desde la brida superior de la camara a insertos ciegos en el fondo (no perforan el sello); "
                "|y| = 20: la cabeza (Ø7) queda entre la camara (|y| 15) y el bolsillo de la pletina; "
                "se aprieta desde abajo",
                ((51.5, 6.0), (51.5, -6.0), (-51.5, 6.0), (-51.5, -6.0)))
BASE_M4_BOSS = p("caja.base_m4_boss", (10.0, 6.0), EST, VER, "Ø x alto del refuerzo interior del inserto M4")
HANDLE_H = p("asa.alto", 42.0, "equipo", OK, "Asa con ojal para el cabo", 42.0)
HANDLE_GRIP = p("asa.agarre", 90.0, EST, VER, "Ancho de mano con guante", 90.0)

# prensaestopas
PG7_HOLE = p("pg7.agujero", 12.6, EST, VER, "Rosca PG7 12.5", 12.6)
PG7_NUT_AF = p("pg7.contratuerca_AF", 15.0, EST, VER, "Comprar y medir", 15.0)
PG7_INNER_H = p("pg7.alto_interior", 9.0, EST, VER, "Rosca que asoma + contratuerca por dentro")
PG7_DOME = p("pg7.domo", (19.0, 22.0), EST, VER,
             "Cuerpo + domo bajo el fondo: Ø maximo x largo desde la cara exterior. Comprar y medir")
FLOOR_GLANDS = p("caja.pg7_fondo", 2, "equipo", OK, "2 x PG7 en el fondo hacia el riel (camaras)", 2)
UMB_GLAND = p("caja.pg7_umbilical", "auto", EST, VER,
              "'auto': en la tapa si la contratuerca colgada no choca con nada; si no, en la pared -X "
              "(el prompt admite 'de costado o arriba'). 'tapa' / 'pared' lo fuerzan", "tapa")
UMB_GLAND_XY = p("caja.pg7_umbilical_xy", (-20.0, 16.0), EST, VER,
                 "Posicion preferida en la tapa; se busca la libre mas cercana", (0.0, 18.0))
HANDLE_KEEP_Y = p("asa.franja_libre_y", 17.5, EST, VER,
                  "|y| minimo del PG7 de la tapa: asa de 12 de ancho + radio del domo + 2")

# holguras del layout (Prompt v2 punto 5)
CLR_PINS = p("holgura.pines", 15.0, "equipo", OK, "Dupont + curva del cable sobre los pines")
CLR_CONN = p("holgura.conector", 10.0, "equipo", OK, "Lateral en el lado de cada conector")
CLR_NUT = p("holgura.contratuerca", 5.0, "equipo", OK,
            "Libre alrededor de cada contratuerca PG7 desde sus esquinas. Los prensaestopas se aprietan con la "
            "caja vacia, antes de meter las bandejas", 20.0)
CLR_USB = p("holgura.usb", 35.0, EST, VER, "Enchufe USB-C con su moldeado + curva, sin sacar la bandeja")
CLR_SD = p("holgura.microsd", 15.0, EST, VER, "Dedo para sacar la tarjeta")
GAP_MOD = p("holgura.entre_modulos", 2.0, EST, VER, "Cuerpo a cuerpo o cuerpo a zona de acceso")
GAP_WALL = p("holgura.pared", 2.0, EST, VER, "Cuerpo o bandeja a la pared interior", 1.0)

# bandeja M11
TRAY_T = p("bandeja.espesor", 3.0, EST, VER, "")
TRAY_STANDOFF = p("bandeja.apoyo", 8.0, EST, VER, "Por encima de los refuerzos M4 (6) del fondo")
TRAY_SPLIT = p("bandeja.partir", "auto", EST, VER,
               "'auto': se parte en der/izq solo si pasa de 150; True / False fuerzan", True)
LAYOUT_FLOORS = p("caja.pisos", "auto", "equipo", OK,
                  "Se comparan 1 y 2 pisos y se usa el de menor aire sellado; 1 o 2 lo fuerzan")
TRAY2_POST_D = p("bandeja.poste_D", 8.0, EST, VER, "Postes del piso superior (2 pisos), con M3")
TRAY_CRADLE_T = p("bandeja.cuna_apoyo", 4.0, EST, VER, "Repisas de la cuna bajo los extremos cortos de la ESP32")
TRAY_BOSS_D = p("bandeja.boss_D", 8.0, EST, VER, "Refuerzo del fondo con inserto M3 que sujeta la bandeja")
TRAY_BOSS_INSET = p("bandeja.boss_margen", 6.0, EST, VER, "Centro del refuerzo al borde de la bandeja")

# componentes del sumergido: (L, A, alto con pines, masa g); conectores en ejes locales u (largo), v (ancho)
COMPONENTS = {
    "esp32_devkitc1": p("comp.esp32_devkitc1", (69.0, 26.0, 15.0, 10.0), EST, VER,
                        "ESP32-S3-DevKitC-1 N16R8, pines hacia abajo", (52.0, 28.0, 13.0, 10.0)),
    "kit_a": p("comp.kit_a", (80.0, 70.0, 12.0, 25.0), EST, VER, "Alternativa paramétrica, medir la pieza"),
    "xy017": p("comp.xy017", (45.0, 15.0, 12.0, 4.0), EST, VER, "XY-017 RS-485", (44.0, 14.0, 12.0, 3.0)),
    "microsd": p("comp.microsd", (42.0, 24.0, 12.0, 4.0), EST, VER, "Lector microSD SPI", (42.0, 24.0, 12.0, 4.0)),
    "mpu6050": p("comp.mpu6050", (21.0, 16.0, 12.0, 3.0), EST, VER, "GY-521, atornillado rigido"),
    "hw517": p("comp.hw517", (34.0, 17.0, 12.0, 4.0), EST, VER, "HW-517 (x2), bornes en ambos extremos"),
}
# lados con conector en ejes locales: lateral 10 mm; acceso = zona que puede solaparse con otras zonas
CONNECTORS = {
    "esp32_devkitc1": {"conector": ("v+", "v-"), "acceso": {"u+": "usb"}, "pines": "abajo"},
    "kit_a": {"conector": ("v+", "v-"), "acceso": {"u+": "usb"}, "pines": "arriba"},
    "xy017": {"conector": ("u+", "u-"), "acceso": {}, "pines": "arriba"},
    "microsd": {"conector": ("u-",), "acceso": {"u+": "microsd"}, "pines": "arriba"},
    "mpu6050": {"conector": ("v-",), "acceso": {}, "pines": "arriba"},
    "hw517": {"conector": ("u+", "u-"), "acceso": {}, "pines": "arriba"},
}
GLAND_MASS_G = p("masa.pg7", 5.0, EST, VER, "Prensaestopas de nylon con contratuerca")
BOX_HARDWARE_G = p("masa.tornilleria_caja", 30.0, EST, VER, "M3/M4 + insertos de la caja", 60.0)
BOX_WIRING_G = p("masa.cables_caja", 20.0, EST, VER, "Dupont + Cat5e dentro de la caja", 40.0)

# lastre (bolsillos en la base, por fuera del sello)
BALLAST_TARGET_KGF = p("lastre.objetivo_kgf", (0.2, 0.5), "equipo", OK, "Peso aparente hacia abajo")
BALLAST_PACKING = p("lastre.empaque", {"tuercas": 0.5, "barra": 0.9}, EST, VER,
                    "Fraccion de acero en el volumen del bolsillo")
POCKET_DEPTH = p("lastre.bolsillo_prof", 20.0, EST, VER, "Menor que el alto del riel (30)")
POCKET_WALL = p("lastre.bolsillo_pared", 2.0, EST, VER, "")
POCKET_RAIL_GAP = p("lastre.holgura_riel", 1.0, EST, VER, "Bolsillos al lado del riel, no debajo")
POCKET_L = p("lastre.bolsillo_largo", 140.0, EST, VER, "Igual al tramo central")
POCKET_IN_BOX = p("lastre.bolsillos_caja", False, "equipo", OK,
                  "Reemplazados por la pletina de inox bajo el tramo central (revision 28/10)", True)
PLATE_BAR = p("lastre.pletina", (25.0, 5.0), EST, VER,
              "Pletina de inox comercial (ancho x espesor); se apilan. Medir la comprada")
PLATE_L = p("lastre.pletina_largo", 100.0, EST, VER,
            "Largo de cada trozo: el bolsillo (|x| <= 53.5) deja libre la zona de la union (|x| > 55) para que la "
            "extension entre de costado", 130.0)
PLATE_SIDES = p("lastre.pletina_lados", 2, EST, VER, "Una pila a cada lado de la camara, simetricas")
PLATE_POCKET_WALL = p("lastre.bolsillo_pletina_pared", 3.0, EST, VER, "Pared y tapa del bolsillo de la pletina")
PLATE_CLR = p("lastre.holgura_pletina", 0.5, EST, VER, "Holgura de la pletina en su bolsillo")
PLATE_POCKET_LAYERS = p("lastre.bolsillo_capacidad", 4, EST, VER,
                        "Pletinas por lado que entran en cada bolsillo (fase_a.py verifica que alcance en todos los aros)")
PLATE_LEVEL = p("lastre.pletina_nivel", "abajo", EST, VER,
                "'abajo': bolsillos pegados a los costados de la camara, al nivel del fondo del riel (baja el "
                "centro de masa); 'brida': colgados de la brida, justo bajo la caja")
PLATE_POCKET_Y0 = p("lastre.bolsillo_pletina_y", 24.5, EST, VER,
                    "Cara interior del bolsillo: deja libre la cabeza del M4 de la caja (y 20 + 3.5 + 1)")

# ---------------------------------------------------------------- capsulas (M4..M7), base P4 rev. B
CAMERA = p("camara.envolvente", (33.0, 33.0, 17.0, 20.0), "fabricante", OK,
           "Arducam Mega 5MP AF, 33 x 33 x 17", (33.0, 33.0, 25.0, 20.0))
CAMERA_CABLE = p("camara.cable_incluido", 300.0, "fabricante", VER, "Medir el recibido")
LED_RING = p("aro_led.envolvente", (30.0, 3.0), EST, VER, "Ø exterior x espesor, sin comprar")
WIN_DIA = p("ventana.diametro", 30.0, EST, VER, "Acrilico, cubre lente + LED", 30.0)
WIN_T = p("ventana.espesor", 3.0, EST, VER, "", 3.0)
CAP_WALL = p("capsula.pared", 4.0, "equipo", OK, "", 4.0)
HINGE_TEETH = p("bisagra.dientes", 36, "equipo", OK, "Bisagra dentada M4 se conserva", 36)
CAM_TILT_DEG = p("bisagra.inclinacion", 40.0, EST, VER, "Multiplo de 10", 40.0)
CAPSULE_SET_G = p("masa.capsula_set", 93.1, EST, VER,
                  "M4+M5 al 100 % + M6 + ventana, de capsula.py (Fase C, cavidad 38 x 38 x 38)", 104.0)
CAPSULE_SET_DISP_CM3 = p("volumen.capsula_set", 127.8, EST, VER,
                         "PETG 71.5 + aire 54.2 + ventana 2.1 cm3 por capsula, de capsula.py (Fase C)", 154.0)
CAPSULE_CONTENT_G = p("masa.capsula_contenido", 35.0, EST, VER, "Camara 20 + LED + cable + PG7")
OTHER_NODE_G = p("masa.otras_piezas", 200.0, EST, VER,
                 "Ganchos, carros, perillas, casquillos, pestillos, tornilleria del riel (sin modelar)")

# ---------------------------------------------------------------- cables (C6)
CAT5E_D = p("cable.cat5e_D", 5.5, EST, VER, "Cat5e de exterior, entra en PG7")
CABLE_BEND_K = p("cable.radio_curva_xD", 4.0, EST, VER, "Radio minimo = 4 x diametro")
CABLE_BEND_R_MIN = p("cable.radio_curva_min", 25.0, "equipo", OK, "Revision 28/10: radio del Cat5e >= 25")
CABLE_ALLOW = p("cable.holguras", {"caja": 60.0, "prensaestopas": 25.0, "bucle": 40.0,
                                    "capsula": 30.0, "holgura": 30.0}, "equipo", OK, "Prompt v2 punto 7")
SPI_TEST_LIMIT = p("cable.limite_sin_prueba", 300.0, "equipo", OK, "> 300: prueba SPI a 8 y 4 MHz")

# =====================================================================================
# BOYA (Fase G; aqui solo se registran los datos de partida)
# =====================================================================================
BUOY_PCB = p("boya.pcb", (70.0, 73.5, 1.6), "equipo", VER, "Placa fabricada; agujeros por verificar")
BUOY_WAVESHARE = p("boya.waveshare_D", (45.0, 40.0, 10.1), "fabricante", OK, "Solar Power Manager (D)")
BUOY_BATT_HOLDER = p("boya.portabaterias", (80.0, 70.0, 30.0), EST, VER, "3 x 18650")
BUOY_RTC = p("boya.rtc_reserva", (40.0, 25.0, 15.0), "equipo", VER, "DS3231, montaje sin confirmar")
BUOY_PANEL = p("boya.panel", (170.0, 170.0, 3.0), EST, VER, "Por anuncio; medir")
BUOY_PANEL_LIFT = p("boya.panel_elevacion", (20.0, 30.0), "equipo", OK, "")
BUOY_FREEBOARD_MIN = p("boya.francobordo_min", 50.0, "equipo", OK, "")
UMBILICAL = p("umbilical", (6.0, 3000.0), EST, VER, "Ø x largo; medir el cable real")


def nut_corner_r():
    """Locknut circumradius from the across-flats size."""
    return PG7_NUT_AF / math.sqrt(3)


# capsula y carro (Fase C)
CAP_FRONT = p("capsula.frente", 6.0, EST, VER, "Pared frontal (ventana + hombro de 2.8)", 6.0)
CAP_FLANGE = p("capsula.brida_ancho", 9.0, EST, VER, "Brida alrededor de la apertura trasera", 9.0)
CAP_FLANGE_T = p("capsula.brida_espesor", 6.0, EST, VER, "", 6.0)
CAP_LID_T = p("capsula.tapa", 5.0, EST, VER, "Espesor de la tapa M5", 5.0)
CAP_GLAND_X = p("capsula.pg7_x", 10.0, EST, VER, "Centro del PG7 desde la apertura trasera (pared inferior)", 10.0)
CAP_SIDE_GAP = p("capsula.holgura_lateral", 2.5, EST, VER, "Camara 33 + 2 x 2.5 por lado = cavidad 38", 2.5)
CAP_REAR_ZONE = p("capsula.zona_trasera", 23.0, EST, VER,
                  "Detras de la placa: curva del cable + contratuerca PG7 (50 - 25 - 2 de la P4 rev. B)", 23.0)
CAP_LENS_GAP = p("capsula.holgura_lente", 0.5, EST, VER, "Punta del lente a la cara trasera de la ventana", 1.0)
WIN_SEAT_DEPTH = p("ventana.asiento", 3.2, EST, VER, "Rebaje desde fuera; el agua empuja el disco al hombro", 3.2)
LENS_APERTURE = p("ventana.apertura", 26.0, EST, VER,
                  "Apertura libre tras la ventana: deja pasar el anillo LED (Ø30) con 2.2 de hombro para el acrilico", 22.0)
LED_RING_HOLE = p("aro_led.agujero", 19.0, EST, VER, "Ø interior supuesto del anillo LED; medir el comprado")
LED_SPOKES = p("aro_led.radios", (3, 2.0), EST, VER,
               "Radios (cantidad, ancho) que sujetan el tubo separador al frente; tapan algo de luz del LED")
BEZEL_OD = p("bisel.diametro", 42.0, EST, VER, "", 42.0)
BEZEL_T = p("bisel.espesor", 2.5, EST, VER, "", 2.5)
BEZEL_SCREWS = p("bisel.tornillos", 3, EST, VER, "M2 autorroscante en la pared frontal", 3)
M2_PILOT = p("m2.piloto", 1.8, EST, VER, "", 1.8)
HINGE_DISC_D = p("bisagra.disco_D", 24.0, "equipo", OK, "CONTEXTO_SESION_CHAT s4", 24.0)
HINGE_TOOTH_H = p("bisagra.diente_alto", 1.2, "equipo", OK, "CONTEXTO_SESION_CHAT s4", 1.2)
HINGE_TEETH_RIN = p("bisagra.anillo_dientes_rin", 7.0, EST, VER, "Anillo 7-12; el M4 de 4.2 queda libre", 7.0)
HINGE_EAR_T = p("bisagra.oreja", 5.0, "equipo", OK, "CONTEXTO_SESION_CHAT s4: orejas de 5", 5.0)
HINGE_GAP = p("bisagra.hueco", 8.4, "equipo", OK, "CONTEXTO_SESION_CHAT s4", 8.4)
TONGUE_LEN = p("bisagra.lengua_largo", 16.0, EST, VER, "Eje a cara exterior de la tapa (fuera del sello)", 16.0)
CARRIAGE_EAR_H = p("carro.oreja_alto", 25.0, EST, VER, "Alto de las orejas de la horquilla del M10", 25.0)
CARRIAGE_EAR_REACH = p("carro.oreja_alcance", 36.0, EST, VER,
                       "Placa de tope a eje: la tapa (semiancho 32) a 90 grados queda 4 mm detras de la placa")
CARRIAGE_END_T = p("carro.placa_tope", 4.0, EST, VER, "Placa que cierra la manga en el extremo exterior y lleva las orejas")
CARRIAGE_LIP_EDGE = p("carro.labio_borde", 6.0, EST, VER,
                      "|y| del borde interior de los labios: deja libre la abertura de la ranura T (2.3) y el perno")
CARRIAGE_MODE = p("carro.modo", "deslizante", EST, VER,
                  "deslizante: manga abierta en los dos extremos, perilla abajo en la T, bisagra bajo el riel (+-50). "
                  "tope: version del agente con placa de tope sobre el eje del riel (solo a ras de la punta)", "tope")
CARRIAGE_AXIS_CLR = p("carro.eje_holgura", 2.0, EST, VER,
                      "Aire entre la cara superior de la capsula a 0 grados y el fondo del riel; fija la caida del eje")
CARRIAGE_KEEL_CLR = p("carro.quilla_holgura", 1.0, EST, VER, "Aire radial entre el disco de la lengua y la quilla")
CARRIAGE_SLIT_CLR = p("carro.rendija_holgura", 1.0, EST, VER,
                      "Margen por lado de la rendija lateral de la manga sobre el alto de la ranura de salida del cable")
CARRIAGE_STEPS = p("carro.posiciones", 5, EST, VER, "Posiciones del barrido de 0 a 2 x recorrido desde la punta del riel")

# gancho y riel (Fase C, antes constantes de modulo)
KNOB_FREE_EXTRA = p("perilla.cilindro_libre_extra", 4.0, EST, VER, "Cilindro libre bajo la perilla = KNOB_D + esto (guante)")
KNOB_WEB_GAP = p("perilla.aire_alma", 1.0, EST, VER, "Aire entre el cilindro libre y el alma o la quilla")
KNOB_FLANGE_GAP = p("perilla.aire_brida", 0.5, EST, VER, "Aire entre la cara donde sale el perno y la perilla")
BUSHING_TIP_MARGIN = p("casquillo.margen_punta", 0.3, EST, VER,
                       "Puntas de la C recortadas a MIN_WALL + esto; tambien el buje del pivote del pestillo")
WEB_OVERLAP = p("gancho.solape_alma", 0.5, EST, VER, "El alma entra en la brida para que la union sea un solido")
XFER_STEP = p("riel.paso_deslizamiento", 10.0, EST, VER, "Paso del barrido del macho deslizando de costado (verificacion)")


# ensambles (Fase D)
LANTERN_ROD_D = p("ensamble.aro_varilla_D", 8.0, EST, VER, "Diametro de la varilla del aro de la linterna de referencia (esquematica)")
LANTERN_CORD_D = p("ensamble.cuerda_D", 4.0, EST, VER, "Diametro de las cuerdas de la linterna de referencia")
LANTERN_CORD_AZ = p("ensamble.cuerda_azimut", (45.0, 135.0, 225.0, 315.0), "equipo", VER,
                    "Cuerdas entre los dos lados de la barra: la barra cruza el aro por el centro, orientada entre dos cuerdas")
LANTERN_APEX_H = p("ensamble.apice_alto", 400.0, EST, VER, "Altura del apice de las cuerdas sobre el aro; desconocida, se calcula el minimo")
LANTERN_NET_K = p("ensamble.red_alto_k", 1.0, EST, VER, "Alto de la red = k x diametro del aro")
LANTERN_NET_T = p("ensamble.red_espesor", 1.0, EST, VER, "Espesor de la cascara cilindrica que representa la red")
CORD_CLEAR = p("ensamble.holgura_cuerda", 10.0, EST, VER, "Distancia libre minima entre cuerda y cualquier pieza del nodo")
INTERF_TOL = p("ensamble.tol_interferencia", 0.01, EST, VER, "Volumen comun (mm3) por encima del cual se marca interferencia")
SWEEP_S = p("ensamble.barrido_s", (0.0, 50.0, 100.0), EST, VER, "Posiciones del carro (punta del riel pasada la manga) del barrido de la bisagra")
SWEEP_TILT_STEP = p("ensamble.barrido_paso", 10.0, EST, VER, "Paso de inclinacion (grados) del barrido de la bisagra, de 0 a 90")

# largo del riel (Fase D, decision pendiente del equipo; los valores por defecto reproducen la geometria actual)
RAIL_EXT_PITCH_MODE = p("riel.paso_extension", "paso_100", "equipo", OK,
                        "paso_100 (decision 29/10): la lengueta macho sale fuera del cuerpo de 100 (pieza de 115) y cada "
                        "extension suma 100. solape: la version anterior, extension de 100 solapada 15 (suma 85), sin punta",
                        "solape")
RAIL_EXT_RULE = p("riel.regla_extensiones", "equipo", "equipo", OK,
                  "equipo: RAIL_EXT_PER_RING. auto: el menor n con la punta >= lo que piden gancho + carro (largo_riel.py)")
LANTERN_HANG = p("ensamble.cuerdas_al_asa", (100.0, 200.0), "equipo", OK,
                 "Aros en los que las cuerdas de la linterna se amarran al ojal del asa del nodo (la linterna cuelga del "
                 "nodo); en los demas van al apice sobre el aro (29/10)")
LANTERN_WATER_N = p("ensamble.linterna_peso_agua_N", 30.0, EST, VER,
                    "Peso en el agua de la linterna (aro, red, cuerdas y carga) que cuelga del asa; pesarla")
RAIL_LAYOUT_GAP = p("riel.holgura_gancho_carro", 1.0, EST, VER, "Aire a lo largo del riel entre la brida del gancho y la manga del carro")
M8_ROD = p("riel.varilla_M8_datos", {"d": 8.0, "d_nucleo": 6.47, "A_s": 36.6, "E": 200000.0, "fy_8.8": 640.0, "fy_4.6": 240.0},
           "fabricante", VER,
           "Varilla roscada M8 de acero (ISO 898-1): nucleo, area resistente, modulo y fluencia de los grados 8.8 y 4.6",
           {"d_nucleo": 6.47, "E": 200000.0})


# boya (Fase G)
BUOY_MASS = p("boya.masas", {"celda_18650": 47.0, "portabaterias": 25.0, "pcb_heltec": 35.0, "waveshare": 15.0,
                              "rtc": 8.0, "panel": 350.0, "antena": 20.0, "cables_fusible": 40.0,
                              "prensaestopas": 20.0, "tornilleria": 60.0}, EST, VER,
              "Masas de componentes en g, tipicas; pesar cada una. Celda 18650 ~47 g")
BUOY_CELLS = p("boya.celdas", 3, "equipo", OK, "3 x 18650 en el portabaterias")
BUOY_SMA_G = p("boya.sma_pasamuros_g", 5.0, EST, VER, "Opcional, solo suma si boya.sma_pasamuros es True")
BUOY_ANTENNA_L = p("boya.antena_largo", 110.0, EST, VER, "Antena LoRa incluida con la Heltec; medir")
BUOY_SMA_BULKHEAD = p("boya.sma_pasamuros", False, "equipo", OK, "Pasamuros SMA exterior opcional y desactivado")
BUOY_SMA_HOLE = p("boya.sma_agujero", 6.5, EST, VER, "Agujero del pasamuros SMA en la tapa del mastil")
BUOY_COMP_GAP = p("boya.holgura_modulos", 5.0, EST, VER, "Aire entre modulos sobre la bandeja")
BUOY_TOP_COMP_H = p("boya.alto_pcb_conectores", 25.0, EST, VER, "PCB con Heltec en cabezal y conectores sobre la bandeja")
BUOY_BATT_STANDOFF = p("boya.apoyo_bateria", 6.0, EST, VER, "Refuerzo M3 bajo el portabaterias (inserto de 6 sin tocar el fondo)")
BUOY_TRAY_GAP = p("boya.aire_bateria_bandeja", 3.0, EST, VER, "Aire entre el portabaterias y la bandeja")
BUOY_HOLDER_HOLES = p("boya.portabaterias_agujeros", (66.0, 56.0), EST, VER, "Paso de los 4 agujeros del portabaterias; medir")
BUOY_TRAY_EDGE = p("boya.bandeja_borde", 2.0, EST, VER, "Margen de la bandeja alrededor de los modulos")
BUOY_POST_D = p("boya.poste_D", 8.0, EST, VER, "Postes de la bandeja con inserto M3")
BUOY_POST_WALL_GAP = p("boya.poste_aire_pared", 1.0, EST, VER, "Aire entre poste y pared interior")
BUOY_UMB_MARGIN = p("boya.umbilical_margen", 3.0, EST, VER, "Del borde de la contratuerca a la pared, ademas de GAP_WALL")
BUOY_CABLE_CLEAR = p("boya.cable_aire", 1.0, EST, VER, "Aire entre el codo del umbilical y la bandeja")
BUOY_SOLAR_GLAND = p("boya.pg7_solar", (25.0, 55.0), EST, VER, "(y, z) del PG7 del cable solar en la pared -X")
BUOY_PANEL_LIFT_USED = p("boya.panel_elevacion_usada", 25.0, EST, VER, "Dentro de 20..30")
BUOY_RAIL = p("boya.riel_panel", (24.0, 140.0, 8.0), EST, VER, "B3: ancho x largo x espesor del larguero; largo <= PIECE_MAX_L")
BUOY_LEG_D = p("boya.pata_D", 14.0, EST, VER, "Patas del larguero sobre los tornillos M3 de la tapa (sin perforar)")
BUOY_CBORE = p("boya.avellanado", (6.5, 3.0), EST, VER, "Cabeza del M3 largo en el larguero: diametro, profundidad")
BUOY_PANEL_HOLE_Y = p("boya.panel_agujeros_y", 20.0, EST, VER, "Dos insertos M3 por larguero a +-y; medir los agujeros del panel real")
BUOY_MAST = p("boya.mastil", (14.0, 8.0, 140.0), EST, VER, "B4: diametro exterior, interior, alto sobre la placa")
BUOY_MAST_PLATE = p("boya.mastil_placa", (30.0, 4.0), EST, VER, "Ancho en X y espesor; usa los tornillos de la tapa del extremo +X")
BUOY_MAST_OFFSET = p("boya.mastil_desfase", 11.0, EST, VER, "Eje del mastil a la linea de tornillos del extremo")
BUOY_FLOAT = p("boya.flotador", (150.0, 90.0, 50.0), EST, VER, "B5: largo x ancho x alto de cada modulo (4 modulos)")
BUOY_FLOAT_SHELL = p("boya.flotador_pared", 1.6, EST, VER, "Pared de PETG del flotador, 4 perimetros")
BUOY_FLOAT_INNER_WALL = p("boya.flotador_pared_interior", 3.0, EST, VER, "Cara hacia el casco, donde nace la lengueta")
BUOY_FLOAT_GAP = p("boya.flotador_separacion", 26.0, EST, VER, "Pared del casco a la cara interior del flotador")
BUOY_FLOAT_PORT = p("boya.flotador_boca", 10.0, EST, VER, "Boca de llenado de espuma, se tapa y sella")
BUOY_FOAM_DENSITY = p("boya.espuma_densidad", 0.030, EST, VER, "g/cm3, celda cerrada; sin absorcion de agua (supuesto)")
BUOY_EAR = p("boya.oreja", (22.0, 12.0, 7.0), EST, VER, "Oreja del casco: saliente, ancho, espesor (al fondo, sin voladizo)")
BUOY_EAR_X = p("boya.oreja_x", 55.0, EST, VER, "x de las 4 orejas; el flotador tiene agujeros en x = 55 y 95 (simetrico)")
BUOY_TAB = p("boya.lengueta", (19.0, 70.0, 5.0), EST, VER, "Lengueta del flotador: saliente, largo, espesor; apoya sobre la oreja")
BUOY_TAB_HOLES = p("boya.lengueta_agujeros", (55.0, 95.0), EST, VER, "x local de los 2 agujeros (el flotador es simetrico)")
BUOY_M5 = p("boya.m5", (5.4, 8.0, 4.2), EST, VER, "Paso, tuerca AF y bolsillo de tuerca; tornillo M5 x 25 de acero inox")
BUOY_EYE = p("boya.ojal", (24.0, 12.0, 6.0, 32.0), EST, VER, "B6: aro exterior, aro interior, espesor, distancia del tornillo al centro del aro")
BUOY_EYE_EAR_W = p("boya.ojal_oreja_ancho", 24.0, EST, VER, "Ancho de la oreja de amarre del casco (extremo +X)")
BUOY_EAR_HOLE_TIP = p("boya.oreja_agujero_punta", 7.5, EST, VER, "Del agujero M5 a la punta de oreja y lengueta")
BUOY_FLOAT_R = p("boya.flotador_radio", 8.0, EST, VER, "Radio de las aristas verticales del flotador")
