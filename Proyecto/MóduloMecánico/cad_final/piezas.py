"""Catalogue of every printed (or bought) piece for MEDIDAS.md and the per-piece drawings (planos_piezas.py).

Each entry says, in plain Spanish for the team, what the piece is, where its STL/STEP lives, how it is printed and
which params.py values fix its important dimensions. Quantities depend on the ring (aro) through `qty(D)`.
Nothing here is a dimension: the values are read from params.REGISTRO when the documents are written.
"""
from dataclasses import dataclass, field
from pathlib import Path

import params as P

MOD = Path(__file__).resolve().parent.parent
PRE, BOYA, PROB = MOD / "salida" / "preliminar", MOD / "salida" / "boya", MOD / "salida" / "probetas"

SELLADA = f"100 %, {P.SEALED_PERIMETERS} perímetros (pieza sellada o tramo del riel)"
NORMAL = "40 % (se informa también al 100 %), 3 perímetros"
MACIZA = "100 %"


def n_ext(D):
    return P.RAIL_EXT_PER_RING[D]


@dataclass
class Pieza:
    code: str                      # M1, M3c, B5 ... (sort key and drawing code)
    stem: str                      # STL/STEP file stem
    name: str                      # plain Spanish name
    what: str                      # one line: what it does
    folder: Path
    qty: object                    # int or callable(D) -> int
    infill: str
    orient: str
    material: str = "PETG"
    keys: list = field(default_factory=list)     # [(label, param key, index or None)]
    note: str = ""

    def n(self, D):
        return self.qty(D) if callable(self.qty) else self.qty

    @property
    def stl(self):
        flat = self.folder / f"{self.stem}.stl"            # salida/probetas keeps its STL without a subfolder
        return flat if flat.exists() else self.folder / "stl" / f"{self.stem}.stl"

    @property
    def step(self):
        return self.folder / "step" / f"{self.stem}.step"   # probetas have no STEP: planos_piezas.py rebuilds them


K = lambda label, key, idx=None: (label, key, idx)   # noqa: E731

PIEZAS = [
    Pieza("M1", "M1_caja_cuerpo", "Caja, cuerpo", "Caja sellada con la electrónica del nodo", PRE, 1, SELLADA,
          "boca arriba, fondo en la cama; sin soportes",
          keys=[K("Pared", "caja.pared"), K("Fondo", "caja.fondo"), K("Ancho de la brida de la tapa", "caja.brida_ancho"),
                K("Espesor de la brida", "caja.brida_espesor"), K("Separación máxima entre tornillos M3", "caja.paso_tornillos"),
                K("Agujero del inserto M3", "m3.inserto_agujero"), K("Profundidad del inserto M3", "m3.inserto_prof"),
                K("Agujero del prensaestopas PG7", "pg7.agujero"), K("Agujero del inserto M4 del fondo", "m4.inserto_agujero"),
                K("Profundidad del inserto M4 (ciego)", "m4.inserto_prof"), K("Refuerzo del inserto M4: Ø", "caja.base_m4_boss", 0),
                K("Refuerzo del inserto M4: alto", "caja.base_m4_boss", 1), K("Aire sobre lo más alto, bajo la tapa", "caja.holgura_tapa"),
                K("Aire alrededor de cada contratuerca PG7", "holgura.contratuerca")]),
    Pieza("M2", "M2_caja_tapa", "Caja, tapa con asa", "Cierra la caja con junta tórica; el asa lleva el ojal del cabo", PRE, 1,
          SELLADA, "cara de la ranura en la cama, asa arriba; sin soportes",
          keys=[K("Espesor de la tapa", "caja.tapa"), K("Cordón de la junta (Ø)", "junta.cordon"),
                K("Ranura de la junta: ancho", "junta.ranura_ancho"), K("Ranura de la junta: profundidad", "junta.ranura_prof"),
                K("Agujero de paso M3", "m3.paso"), K("Alto del asa", "asa.alto"), K("Abertura para la mano", "asa.agarre"),
                K("Ojal: Ø exterior", "asa.ojal", 0), K("Ojal: Ø interior", "asa.ojal", 1)]),
    Pieza("M11", "M11_bandeja", "Bandeja de la electrónica", "Lleva la ESP32 y los módulos dentro de la caja", PRE, 1, NORMAL,
          "plana; sin soportes",
          keys=[K("Espesor", "bandeja.espesor"), K("Altura de apoyo sobre el fondo", "bandeja.apoyo"),
                K("Refuerzo con inserto M3 (Ø)", "bandeja.boss_D"), K("ESP32-S3 DevKitC-1: largo", "comp.esp32_devkitc1", 0),
                K("ESP32-S3 DevKitC-1: ancho", "comp.esp32_devkitc1", 1), K("XY-017: largo", "comp.xy017", 0),
                K("Lector microSD: largo", "comp.microsd", 0), K("MPU-6050: largo", "comp.mpu6050", 0),
                K("HW-517: largo", "comp.hw517", 0), K("Aire entre módulos", "holgura.entre_modulos")]),
    Pieza("M3c", "M3_riel_central", "Riel, tramo central (cámara de cables)",
          "Va atornillado bajo la caja; por dentro bajan los cables desde los PG7 y pasa la varilla M8", PRE, 1, SELLADA,
          "brida abajo (dada vuelta); necesita soportes en el techo de la cámara y los bolsillos",
          keys=[K("Sección del riel", "riel.seccion"), K("Pared del riel", "riel.pared"), K("Largo", "riel.central_L"),
                K("Inclinación de la rampa de la cámara (grados)", "riel.camara_rampa"),
                K("Brida superior: ancho mínimo", "riel.camara_brida", 0), K("Brida superior: espesor", "riel.camara_brida", 1),
                K("Ranura T: abertura", "riel.ranura_T", "abertura"), K("Ranura T: ancho del canal", "riel.ranura_T", "ancho"),
                K("Ranura T: alto del canal", "riel.ranura_T", "alto"), K("Largo de la unión", "riel.cola_milano"),
                K("Altura del plano de la unión", "riel.union_z"), K("Agujero de la varilla M8", "riel.varilla_agujero"),
                K("Tabique de la varilla (espesor)", "riel.varilla_tabique"), K("Agujero de paso M4", "m4.paso"),
                K("Pletina de lastre: ancho", "lastre.pletina", 0), K("Pletina de lastre: espesor", "lastre.pletina", 1),
                K("Pletina de lastre: largo", "lastre.pletina_largo"), K("Holgura de la pletina en su bolsillo", "lastre.holgura_pletina")]),
    Pieza("M3e", "M3_riel_ext", "Riel, extensión", "Alarga el riel 100 mm por lado (Ø200 a Ø500)", PRE, lambda D: 2 * n_ext(D),
          SELLADA, "acostada sobre una cara lateral; casi sin soportes",
          keys=[K("Paso (lo que alarga cada una)", "riel.ext_L"), K("Lengüeta de unión", "riel.cola_milano"),
                K("Sección", "riel.seccion"), K("Pared", "riel.pared"), K("Llave de la unión: base", "riel.cola_llave", 0),
                K("Llave de la unión: punta", "riel.cola_llave", 1), K("Llave de la unión: alto", "riel.cola_llave", 2),
                K("Pared engrosada en la unión", "riel.union_pared"), K("Tornillos M4 de la unión (y)", "riel.union_m4_y"),
                K("Agujero de la varilla M8", "riel.varilla_agujero"), K("Tabique de la varilla", "riel.varilla_tabique")]),
    Pieza("M3p", "M3_riel_punta", "Riel, punta", "Cierra cada extremo del riel; por su ranura lateral sale el cable a la cápsula",
          PRE, 2, SELLADA, "acostada sobre una cara lateral",
          keys=[K("Largo del cuerpo (sin la lengüeta)", "riel.punta_L"), K("Pared del extremo (apoya la arandela)", "riel.punta_tapa"),
                K("Ranura de salida del cable: alto", "riel.salida_cable", 0), K("Ranura de salida del cable: largo", "riel.salida_cable", 1),
                K("Ranura de salida: distancia a la punta", "riel.salida_cable", 2), K("Agujero de la varilla M8", "riel.varilla_agujero"),
                K("Arandela DIN 9021: Ø exterior", "riel.varilla_arandela", 0), K("Tuerca M8: entrecaras", "riel.varilla_tuerca", 0)]),
    Pieza("M3t", "M3_tapa_bolsillo", "Tapa del bolsillo del lastre", "Cierra por abajo el bolsillo de las pletinas de inox", PRE, 2,
          NORMAL, "plana", keys=[K("Espesor", "lastre.bolsillo_pletina_pared")],
          note="Todavía no tiene cómo fijarse (tornillos o pegado): está por definir."),
    Pieza("M4", "M4_capsula_cuerpo", "Cápsula de la cámara, cuerpo", "Caja sellada de la cámara con la ventana al frente", PRE, 2,
          SELLADA, "eje de la cámara vertical; soportes chicos",
          keys=[K("Pared", "capsula.pared"), K("Pared del frente", "capsula.frente"), K("Brida trasera: ancho", "capsula.brida_ancho"),
                K("Brida trasera: espesor", "capsula.brida_espesor"), K("Aire a cada lado de la cámara", "capsula.holgura_lateral"),
                K("Zona trasera (curva del cable + PG7)", "capsula.zona_trasera"), K("Cámara: lado", "camara.envolvente", 0),
                K("Cámara: fondo", "camara.envolvente", 2), K("Rebaje de la ventana", "ventana.asiento"),
                K("Apertura detrás de la ventana", "ventana.apertura"), K("Separador LED-lente: pared", "aro_led.separador", 0),
                K("PG7: distancia a la abertura trasera", "capsula.pg7_x")]),
    Pieza("M5", "M5_capsula_tapa", "Cápsula, tapa con bisagra", "Cierra la cápsula y lleva el disco dentado de la bisagra", PRE, 2,
          SELLADA, "de canto; soportes chicos",
          keys=[K("Espesor de la tapa", "capsula.tapa"), K("Disco dentado: Ø", "bisagra.disco_D"),
                K("Cantidad de dientes", "bisagra.dientes"), K("Alto del diente", "bisagra.diente_alto"),
                K("Lengua: largo", "bisagra.lengua_largo"), K("Hueco entre orejas", "bisagra.hueco")]),
    Pieza("M6", "M6_capsula_bisel", "Bisel de la ventana", "Aprieta la ventana de acrílico contra el frente", PRE, 2, NORMAL,
          "plano", keys=[K("Ø exterior", "bisel.diametro"), K("Espesor", "bisel.espesor"), K("Tornillos M2", "bisel.tornillos"),
                         K("Agujero piloto M2", "m2.piloto")]),
    Pieza("M7", "M7_capsula_ventana", "Ventana", "Disco de acrílico; se corta, no se imprime", PRE, 2, "no se imprime",
          "corte láser o torno", material="acrílico (PMMA)",
          keys=[K("Ø", "ventana.diametro"), K("Espesor", "ventana.espesor")]),
    Pieza("M9", "M9_gancho", "Gancho al aro", "Sujeta el riel a la varilla del aro", PRE, 2, NORMAL,
          "de costado; soporte bajo el escalón de la brida",
          keys=[K("Ancho del asiento", "gancho.contacto"), K("Radio de los bordes", "gancho.radio_borde"),
                K("Alojamiento del casquillo (Ø)", "gancho.alojamiento"), K("Pared mínima", "gancho.pared"),
                K("Brida: largo", "gancho.brida", 0), K("Brida: espesor", "gancho.brida", 1),
                K("Fondo del riel al centro de la varilla", "gancho.caida"), K("Ranura de la correa: ancho", "correa.ancho"),
                K("Ranura de la correa: espesor", "correa.ranura_t")]),
    Pieza("M10", "M10_carro_capsula", "Carro de la cápsula", "Desliza sobre el riel y sostiene la cápsula con la bisagra", PRE, 2,
          NORMAL, "de costado; soportes chicos",
          keys=[K("Largo", "carro.largo"), K("Pared", "carro.pared"), K("Orejas: alto", "carro.oreja_alto"),
                K("Orejas: espesor", "bisagra.oreja"), K("Hueco entre orejas", "bisagra.hueco"),
                K("Aire entre cápsula y riel", "carro.eje_holgura"), K("Recorrido de diseño (±)", "carro.recorrido")]),
    Pieza("M12", "M12_perilla", "Perilla", "Aprieta el gancho y el carro con guante (lleva un perno M4 adentro)", PRE, 4, NORMAL,
          "plana; PAUSAR la impresión para meter el perno",
          keys=[K("Ø", "perilla.diametro"), K("Alto", "perilla.alto"), K("Lóbulos", "perilla.lobulos"),
                K("Tapa sobre la cabeza del perno", "perilla.tapa_cabeza"), K("Perno M4 hexagonal: entrecaras", "m4.cabeza_hex", 0)]),
    Pieza("M13", "M13_casquillo_D8", "Casquillo de la varilla", "Adapta el gancho a la varilla del aro (Ø6, 8, 10 o 12)", PRE, 2,
          MACIZA, "de pie, pestaña en la cama",
          keys=[K("Diámetros de varilla disponibles", "casquillo.D"), K("Holgura sobre la varilla", "casquillo.holgura_varilla"),
                K("Ajuste a presión en el gancho", "casquillo.interferencia"), K("Pestaña: Ø", "casquillo.pestana", 0),
                K("Pestaña: espesor", "casquillo.pestana", 1)],
          note="Se imprime el del diámetro de la varilla real; el dibujo es el de Ø8."),
    Pieza("M14", "M14_pestillo", "Pestillo del gancho", "Traba el gancho cerrado sobre la varilla", PRE, 2, MACIZA, "plano",
          keys=[K("Pivote (M3)", "pestillo.pivote"), K("Lengüeta: largo", "pestillo.lengueta", 0),
                K("Lengüeta: ancho", "pestillo.lengueta", 1), K("Resalte de la traba", "pestillo.resalte"), K("Espesor", "pestillo.espesor")]),
    Pieza("PB8", "PB8_inserto_M4", "Probeta de arranque del inserto M4", "Prueba cuánto aguanta el inserto M4 del fondo de la caja",
          PROB, 0, SELLADA, "cara de afuera en la cama", keys=[K("Placa: lado", "probeta.inserto_M4", 0),
                                                               K("Agujeros de sujeción: separación", "probeta.inserto_M4", 1),
                                                               K("Espesor (= fondo de la caja)", "caja.fondo"),
                                                               K("Agujero del inserto", "m4.inserto_agujero")],
          note="Imprimir 3 aparte del nodo; no va en el ensamble."),
    Pieza("B1", "B1_casco_central", "Boya, casco", "Caja sellada de la boya con la placa y las baterías", BOYA, 1, MACIZA,
          "ver reporte_boya.md",
          keys=[K("Placa (PCB): largo", "boya.pcb", 0), K("Placa (PCB): ancho", "boya.pcb", 1),
                K("Portabaterías: largo", "boya.portabaterias", 0), K("Aire entre módulos", "boya.holgura_modulos"),
                K("Oreja de los flotadores: saliente", "boya.oreja", 0), K("Tornillo M5: paso", "boya.m5", 0)]),
    Pieza("B1b", "B1b_bandeja", "Boya, bandeja", "Lleva la placa, el Waveshare y el reloj", BOYA, 1, NORMAL, "plana",
          keys=[K("Margen alrededor de los módulos", "boya.bandeja_borde"), K("Postes con inserto M3 (Ø)", "boya.poste_D")]),
    Pieza("B2", "B2_tapa", "Boya, tapa", "Cierra el casco con junta tórica", BOYA, 1, MACIZA, "plana",
          keys=[K("Cordón de la junta", "junta.cordon"), K("Ranura: ancho", "junta.ranura_ancho")]),
    Pieza("B3", "B3_larguero_panel", "Boya, larguero del panel", "Eleva el panel solar sobre la tapa", BOYA, 2, NORMAL, "plano",
          keys=[K("Ancho", "boya.riel_panel", 0), K("Largo", "boya.riel_panel", 1), K("Patas (Ø)", "boya.pata_D"),
                K("Elevación del panel", "boya.panel_elevacion_usada")]),
    Pieza("B4", "B4_mastil_antena", "Boya, mástil de la antena", "Sostiene la antena LoRa fuera del panel", BOYA, 1, NORMAL,
          "de pie", keys=[K("Ø exterior", "boya.mastil", 0), K("Alto", "boya.mastil", 2), K("Placa: ancho", "boya.mastil_placa", 0)]),
    Pieza("B5", "B5_flotador", "Boya, flotador", "Uno de los 4 flotadores; se rellena con espuma", BOYA, 4, NORMAL, "boca arriba",
          keys=[K("Largo", "boya.flotador", 0), K("Ancho", "boya.flotador", 1), K("Alto", "boya.flotador", 2),
                K("Pared", "boya.flotador_pared"), K("Densidad de la espuma (g/cm³)", "boya.espuma_densidad")]),
    Pieza("B5b", "B5b_tapa_flotador", "Boya, tapa del flotador", "Cierra cada flotador", BOYA, 4, NORMAL, "plana",
          keys=[K("Espesor", "boya.flotador_pared")]),
    Pieza("B6", "B6_ojal_amarre", "Boya, ojal de amarre", "Ojal para el cabo de fondeo, separado del umbilical", BOYA, 1, MACIZA,
          "plano", keys=[K("Aro exterior", "boya.ojal", 0), K("Aro interior", "boya.ojal", 1), K("Espesor", "boya.ojal", 2)]),
]


def value(key, idx=None):
    v = P.REGISTRO[key].value
    return v if idx is None else v[idx]


def fmt(v):
    if isinstance(v, bool):
        return "sí" if v else "no"
    if isinstance(v, float):
        return f"{v:g}"
    if isinstance(v, (tuple, list)):
        return " × ".join(fmt(x) for x in v)
    if isinstance(v, dict):
        return ", ".join(f"{k}: {fmt(x)}" for k, x in v.items())
    return str(v)
