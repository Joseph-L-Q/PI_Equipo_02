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
INFILL_CASES = p("impresion.relleno", (0.40, 1.00), "equipo", OK, "Prompt v2 Fase E: 40 % y 100 %")
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
RAIL_EXT_L = p("riel.ext_L", 100.0, "equipo", OK, "M3_riel_ext intercambiable")
RAIL_EXT_PER_RING = p("riel.extensiones", {100.0: 0, 200.0: 1, 300.0: 1, 500.0: 2}, "equipo", OK,
                      "0 / 1 / 2 extensiones por lado")
RAIL_DOVETAIL = p("riel.cola_milano", 15.0, "equipo", OK, "Macho/hembra 15 + 2 M4 pasantes")
RAIL_TSLOT = p("riel.ranura_T", {"abertura": 4.6, "ancho": 8.0, "alto": 3.6}, EST, VER,
               "Para tuerca M4 (AF7 x 3.2); se ajusta con la probeta de la Fase B")
RAIL_ROD_M8 = p("riel.varilla_M8", False, "equipo", OK, "Refuerzo opcional por dentro")
RAIL_WINDOW = p("riel.ventana_cable", (24.0, 14.0), EST, VER,
                "Ventana en la cara superior del tramo central, bajo cada PG7 del fondo")

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
BASE_M4_PTS = p("caja.base_m4", ((51.5, 6.0), (51.5, -6.0), (-51.5, 6.0), (-51.5, -6.0)), EST, VER,
                "4 M4 desde el riel a insertos ciegos en el fondo (no perforan el sello); "
                "|x| < 55 para no caer en la cola de milano del tramo central")
BASE_M4_BOSS = p("caja.base_m4_boss", (10.0, 6.0), EST, VER, "Ø x alto del refuerzo interior del inserto M4")
HANDLE_H = p("asa.alto", 42.0, "equipo", OK, "Asa con ojal para el cabo", 42.0)
HANDLE_GRIP = p("asa.agarre", 90.0, EST, VER, "Ancho de mano con guante", 90.0)

# prensaestopas
PG7_HOLE = p("pg7.agujero", 12.6, EST, VER, "Rosca PG7 12.5", 12.6)
PG7_NUT_AF = p("pg7.contratuerca_AF", 15.0, EST, VER, "Comprar y medir", 15.0)
PG7_INNER_H = p("pg7.alto_interior", 9.0, EST, VER, "Rosca que asoma + contratuerca por dentro")
FLOOR_GLANDS = p("caja.pg7_fondo", 2, "equipo", OK, "2 x PG7 en el fondo hacia el riel (camaras)", 2)
UMB_GLAND = p("caja.pg7_umbilical", "tapa", EST, VER,
              "En la tapa, sobre la zona libre central; el umbilical sube a la boya", "PG9 en la tapa")
UMB_GLAND_XY = p("caja.pg7_umbilical_xy", (-20.0, 16.0), EST, VER,
                 "Fuera del asa (y = +-6) y de la zona de cables del MPU-6050", (0.0, 18.0))

# holguras del layout (Prompt v2 punto 5)
CLR_PINS = p("holgura.pines", 15.0, "equipo", OK, "Dupont + curva del cable sobre los pines")
CLR_CONN = p("holgura.conector", 10.0, "equipo", OK, "Lateral en el lado de cada conector")
CLR_NUT = p("holgura.contratuerca", 20.0, "equipo", OK,
            "Libre alrededor de cada contratuerca PG7, medido desde sus esquinas (lectura literal)", 20.0)
CLR_USB = p("holgura.usb", 35.0, EST, VER, "Enchufe USB-C con su moldeado + curva, sin sacar la bandeja")
CLR_SD = p("holgura.microsd", 15.0, EST, VER, "Dedo para sacar la tarjeta")
GAP_MOD = p("holgura.entre_modulos", 2.0, EST, VER, "Cuerpo a cuerpo o cuerpo a zona de acceso")
GAP_WALL = p("holgura.pared", 2.0, EST, VER, "Cuerpo o bandeja a la pared interior", 1.0)

# bandeja M11
TRAY_T = p("bandeja.espesor", 3.0, EST, VER, "")
TRAY_STANDOFF = p("bandeja.apoyo", 8.0, EST, VER, "Por encima de los refuerzos M4 (6) del fondo")
TRAY_SPLIT = p("bandeja.partir", True, EST, VER,
               "La bandeja entera pasa de 150: se parte en der/izq; False = una sola pieza")
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
CAPSULE_SET_G = p("masa.capsula_set", 104.0, EST, VER,
                  "M4+M5+M6 (100 %) + ventana, de cad/reporte_verificacion.md (P4 rev. B vieja)")
CAPSULE_SET_DISP_CM3 = p("volumen.capsula_set", 154.0, EST, VER,
                         "PETG 79.5 + aire 72 + ventana 2.1 cm3 por capsula (P4 rev. B vieja)")
CAPSULE_CONTENT_G = p("masa.capsula_contenido", 35.0, EST, VER, "Camara 20 + LED + cable + PG7")
OTHER_NODE_G = p("masa.otras_piezas", 200.0, EST, VER,
                 "Ganchos, carros, perillas, casquillos, pestillos, tornilleria del riel (sin modelar)")

# ---------------------------------------------------------------- cables (C6)
CAT5E_D = p("cable.cat5e_D", 5.5, EST, VER, "Cat5e de exterior, entra en PG7")
CABLE_BEND_K = p("cable.radio_curva_xD", 4.0, EST, VER, "Radio minimo = 4 x diametro")
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
