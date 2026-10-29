# Reporte Fase A, layout de la caja central (generado por `fase_a.py`, revisión 28/10)

No editar a mano: se regenera. mm, cm³, g. Todo valor `estimado` sigue por verificar.

## 1. Parámetros (`cad_final/params.py`)

| Parámetro | Anterior | Nuevo | Razón | Origen | Estado |
|---|---|---|---|---|---|
| `impresora.cama` | 220 × 220 × 250 | 220 × 220 × 250 | Impresora real desconocida | estimado | por_verificar |
| `pieza.largo_max` | nuevo | 150 | Prompt v2: ninguna pieza > 150 salvo la caja | equipo | confirmado |
| `impresion.espesor_min` | 1.2 | 1.2 | 3 perimetros de 0.4 | equipo | confirmado |
| `impresion.cascara` | nuevo | 1.2 | Perimetros + capas sup/inf macizos, para la masa con relleno | estimado | por_verificar |
| `impresion.relleno` | nuevo | 0.4 × 1 | Piezas no selladas (bandeja, ganchos, carros...): se reportan 40 % y 100 % | equipo | confirmado |
| `impresion.relleno_sellado` | 0.4 | 1 | M1, M2, M4, M5 y tramos del riel al 100 % (revision 28/10, C13) | equipo | confirmado |
| `impresion.piezas_selladas` | nuevo | M1; M2; M4; M5; M3_riel_central; M3_riel_ext | Piezas que van al 100 % con 5 perimetros | equipo | confirmado |
| `impresion.perimetros_sellado` | nuevo | 5 | 5 perimetros (2.0 mm con boquilla 0.4) | equipo | confirmado |
| `impresion.holgura` | 1 | 0.3 | Handoff; probar con el peine de la Fase B | estimado | por_verificar |
| `impresion.comp_agujero` | nuevo | 0.2 | Handoff; probar en impresora real | estimado | por_verificar |
| `petg.densidad` | 1.27 | 1.27 | Sustituir por el dato del slicer | estimado | por_verificar |
| `petg.E` | nuevo | 1700 | PETG manual para SimScale | estimado | por_verificar |
| `petg.nu` | nuevo | 0.38 | PETG manual | estimado | por_verificar |
| `petg.sigma_y` | 45 | 45 | Macizo, a lo largo de las capas | estimado | por_verificar |
| `petg.sigma_capas` | nuevo | 22 | Entre capas, mitad del macizo | estimado | por_verificar |
| `acrilico.densidad` | 1.19 | 1.19 | PMMA | fabricante | confirmado |
| `acero_inox.densidad` | nuevo | 7.9 | Lastre de tuercas o pernos A2 | fabricante | confirmado |
| `agua.densidad` | 1.025 | 1.025 | Agua de mar de referencia | estimado | confirmado |
| `profundidad_m` | 15 | 1 | Prueba real: 1 m varios dias. No se afirma 15 m | equipo | confirmado |
| `peso_aire_max_kg` | 3 | 3 | Lista de exigencias | equipo | confirmado |
| `aro.diametros` | 500 | 100 × 200 × 300 × 500 | Nodo ajustable de Ø100 a Ø500; un ensamble por aro | equipo | confirmado |
| `aro.offset_cuerda` | 0 | 0 | La barra cruza el aro por el centro | equipo | confirmado |
| `aro.varilla_D` | 12 | 6 × 8 × 10 × 12 | Varilla real sin medir: un casquillo por diametro | estimado | por_verificar |
| `aro.cuerdas` | nuevo | 4 | 3 o 4 cuerdas desde el borde; sin cabo central | equipo | por_verificar |
| `riel.seccion` | 30 × 25 | 30 | Cuadrado 30 x 30, hueco = conducto inundado | equipo | confirmado |
| `riel.pared` | 3 | 4 | Prompt v2 | equipo | confirmado |
| `riel.central_L` | 190 | 140 | M3_riel_central bajo la caja | equipo | confirmado |
| `riel.ext_L` | nuevo | 100 | M3_riel_ext intercambiable | equipo | confirmado |
| `riel.extensiones` | nuevo | 100.0: 0, 200.0: 1, 300.0: 1, 500.0: 2 | 0 / 1 / 2 extensiones por lado | equipo | confirmado |
| `riel.cola_milano` | nuevo | 15 | Macho/hembra 15 + 2 M4 pasantes | equipo | confirmado |
| `riel.ranura_T` | nuevo | abertura: 4.6, ancho: 8, alto: 3.6 | Para tuerca M4 (AF7 x 3.2); se ajusta con la probeta de la Fase B | estimado | por_verificar |
| `riel.varilla_M8` | nuevo | False | Refuerzo opcional por dentro | equipo | confirmado |
| `riel.camara_alto` | nuevo | 50 | 'Unos 50' de alto interior; el valor real se deriva (domo + radio + cable + nervio) | equipo | confirmado |
| `riel.camara_rampa` | nuevo | 45 | Techo en rampa hacia el conducto de 22 (imprimible) | estimado | por_verificar |
| `riel.camara_brida` | nuevo | 56 × 4 | Brida superior (ancho minimo x espesor): lleva los 4 M4 a la caja y cuelga los bolsillos de la pletina; el ancho real lo fijan los bolsillos | estimado | por_verificar |
| `riel.ventana_cable` | nuevo | 24 × 14 | OBSOLETO desde la revision del 28/10: el tramo central es una camara de cables (riel.camara_*) | estimado | por_verificar |
| `gancho.contacto` | nuevo | 12 | Asiento de 12 con bordes R3 | equipo | confirmado |
| `gancho.radio_borde` | nuevo | 3 |  | equipo | confirmado |
| `gancho.carga_N` | nuevo | 75 | 150 N repartidos en 2 ganchos | equipo | confirmado |
| `perilla.diametro` | nuevo | 30 | M12_perilla, para guante | equipo | confirmado |
| `casquillo.D` | nuevo | 6 × 8 × 10 × 12 | M13_casquillo_D6...D12 | equipo | confirmado |
| `pestillo.resalte` | nuevo | 0.6 | Traba del M14; probar en probeta | equipo | por_verificar |
| `correa.ancho` | 26 | 25 | Correa textil de seguridad | equipo | confirmado |
| `carro.recorrido` | nuevo | 50 | M10_carro_capsula, +-50 | equipo | confirmado |
| `carga.manipulacion_N` | nuevo | 150 | Caso de diseno a 1 m | equipo | confirmado |
| `m4.tuerca` | nuevo | 7 × 3.2 | AF x espesor, DIN 934 | fabricante | por_verificar |
| `m4.cabeza` | nuevo | 7 × 4 | Allen DIN 912: Ø x alto | fabricante | por_verificar |
| `m4.cabeza_hex` | nuevo | 7 × 2.8 | Perno hexagonal DIN 933: AF x alto (perilla) | fabricante | por_verificar |
| `m3.tuerca` | nuevo | 5.5 × 2.4 | AF x espesor, DIN 934 | fabricante | por_verificar |
| `riel.ranura_T_nervio` | nuevo | 2 | Nervios que encierran el canal de la tuerca sobre el fondo; la tuerca entra por la punta del tramo | estimado | por_verificar |
| `riel.union_z` | nuevo | 15 | Media madera: el macho conserva la mitad de abajo (con la ranura T), la hembra la de arriba | estimado | por_verificar |
| `riel.cola_llave` | nuevo | 8 × 11 × 4 | Llave en cola de milano vista de lado (base, punta, alto) en la cara de la media madera; entra deslizando de costado | estimado | por_verificar |
| `riel.union_pared` | nuevo | 10 | Paredes engrosadas hacia adentro en la union para la tuerca M4 con 1.4 de piel; conducto local 10 de ancho: cada lado del riel lleva un solo Cat5e (5.5) | estimado | por_verificar |
| `riel.union_m4_y` | nuevo | 10 | 2 M4 verticales dentro de las paredes (y = +-10): no cruzan el conducto de cables | estimado | por_verificar |
| `gancho.alojamiento` | nuevo | 16 | Ø del asiento del casquillo en la J (varilla max 12 + pared) | estimado | por_verificar |
| `casquillo.interferencia` | nuevo | 0.15 | Exceso de Ø del casquillo sobre el asiento | estimado | por_verificar |
| `casquillo.holgura_varilla` | nuevo | 0.4 | Ø interior = varilla + holgura | estimado | por_verificar |
| `casquillo.pestana` | nuevo | 20 × 1.5 | Ø x espesor de la pestana de tope | estimado | por_verificar |
| `pestillo.pivote` | nuevo | 3 | Pivote M3 | equipo | confirmado |
| `pestillo.lengueta` | nuevo | 18 × 12 | Largo x ancho de la lengueta para el pulgar con guante | estimado | por_verificar |
| `perilla.alto` | nuevo | 12 | Alto de la perilla | estimado | por_verificar |
| `perilla.lobulos` | nuevo | 8 | Moleteado grueso para guante | estimado | por_verificar |
| `peine.holguras` | nuevo | 0.2 × 0.3 × 0.4 × 0.5 | Peine de holguras de la Fase B | equipo | confirmado |
| `peine.pin_D` | nuevo | 8 | Pin de prueba | estimado | por_verificar |
| `probeta.junta` | nuevo | 60 × 60 | Cuadrado de 60 x 60 con ranura y 4 M3 | equipo | confirmado |
| `probeta.tramo_L` | nuevo | 40 | PB2/PB3 rail length per segment | estimado | por_verificar |
| `gancho.pared` | nuevo | 4 | minimum wall around the hook seat | estimado | por_verificar |
| `gancho.labio_alto` | nuevo | 10 | height of the upper lip that carries the latch pivot | estimado | por_verificar |
| `correa.ranura_t` | nuevo | 3 | strap slot thickness (slot is STRAP_W x this) | estimado | por_verificar |
| `gancho.vastago_alto` | nuevo | 20 | stem above the jaw, carries the M4 hole to bolt PB1 to PB2 | estimado | por_verificar |
| `pestillo.espesor` | nuevo | 3.6 | latch plate thickness (Y) | estimado | por_verificar |
| `pestillo.brazo_ancho` | nuevo | 5 | latch arm width (X) | estimado | por_verificar |
| `pestillo.cresta_ancho` | nuevo | 1.2 | catch ridge width on the jaw lip | estimado | por_verificar |
| `pestillo.holgura_punta` | nuevo | 0.2 | closed latch tip to lip clearance | estimado | por_verificar |
| `pestillo.giro_media_ranura` | nuevo | 4.5 | half width of the latch slot in the upper lip (swing room) | estimado | por_verificar |
| `perilla.lobulo_r` | nuevo | 3.5 | radius of each grip lobe | estimado | por_verificar |
| `perilla.tapa_cabeza` | nuevo | 1.2 | roof over the embedded bolt head (print pause) | estimado | por_verificar |
| `probeta.junta_radio_cavidad` | nuevo | 14 | inner corner radius of the seal base cavity (land follows the groove path) | estimado | por_verificar |
| `probeta.junta_radio_ext` | nuevo | 2 | outer corner radius of the 60 x 60 seal parts | estimado | por_verificar |
| `peine.paso` | nuevo | 18 | spacing of the comb holes | estimado | por_verificar |
| `peine.espesor` | nuevo | 6 | comb plate thickness | estimado | por_verificar |
| `peine.ancho` | nuevo | 26 | comb plate width | estimado | por_verificar |
| `peine.texto_alto` | nuevo | 4.5 | engraved text height | estimado | por_verificar |
| `peine.texto_prof` | nuevo | 0.6 | engraved text depth | estimado | por_verificar |
| `peine.pin_L` | nuevo | 8 | comb pin length | estimado | por_verificar |
| `esp32.base` | nuevo | sin_base | Por defecto sin KIT A; 'kit_a' es la alternativa | equipo | confirmado |
| `caja.pared` | 5 | 4 | A 1 m la presion no manda (0.0101 MPa) | equipo | confirmado |
| `caja.fondo` | 6 | 4 | Igual que la pared | equipo | confirmado |
| `caja.tapa` | 6 | 5 | Ranura de 1.5 deja 3.5 bajo la junta | estimado | por_verificar |
| `caja.brida_ancho` | 9 | 10 | Ranura + inserto M3 (agujero 4.0) con 3 mm de pared | estimado | por_verificar |
| `caja.brida_espesor` | 6 | 8 | Inserto M3 de 5.7 + 2 de fondo | estimado | por_verificar |
| `caja.paso_tornillos` | 76 | 65 | Separacion maxima entre M3 de la tapa: compresion pareja de la junta | estimado | por_verificar |
| `caja.holgura_tapa` | nuevo | 5 | Aire libre entre lo mas alto y la tapa | estimado | por_verificar |
| `junta.cordon` | 2 | 2 | Cordon Ø2, como ya esta | equipo | confirmado |
| `junta.ranura_ancho` | 2.6 | 2.6 |  | equipo | confirmado |
| `junta.ranura_prof` | 1.5 | 1.5 | 25 % de compresion | equipo | confirmado |
| `m3.paso` | 3.4 | 3.4 |  | estimado | por_verificar |
| `m3.inserto_agujero` | 4 | 4 | Inserto termico M3 x 5.7 | estimado | por_verificar |
| `m3.inserto_prof` | 6 | 6 |  | estimado | por_verificar |
| `m4.paso` | 4.2 | 4.2 |  | estimado | por_verificar |
| `m4.inserto_agujero` | nuevo | 5.6 | Inserto termico M4 x 8.1 | estimado | por_verificar |
| `m4.inserto_prof` | nuevo | 8.5 |  | estimado | por_verificar |
| `caja.base_m4` | 51.5 × 6; 51.5 × -6; -51.5 × 6; -51.5 × -6 | 40 × 20; 40 × -20; -40 × 20; -40 × -20 | 4 M4 desde la brida superior de la camara a insertos ciegos en el fondo (no perforan el sello); |y| = 20: la cabeza (Ø7) queda entre la camara (|y| 15) y el bolsillo de la pletina; se aprieta desde abajo | estimado | por_verificar |
| `caja.base_m4_boss` | nuevo | 10 × 6 | Ø x alto del refuerzo interior del inserto M4 | estimado | por_verificar |
| `asa.alto` | 42 | 42 | Asa con ojal para el cabo | equipo | confirmado |
| `asa.agarre` | 90 | 90 | Ancho de mano con guante | estimado | por_verificar |
| `pg7.agujero` | 12.6 | 12.6 | Rosca PG7 12.5 | estimado | por_verificar |
| `pg7.contratuerca_AF` | 15 | 15 | Comprar y medir | estimado | por_verificar |
| `pg7.alto_interior` | nuevo | 9 | Rosca que asoma + contratuerca por dentro | estimado | por_verificar |
| `pg7.domo` | nuevo | 19 × 22 | Cuerpo + domo bajo el fondo: Ø maximo x largo desde la cara exterior. Comprar y medir | estimado | por_verificar |
| `caja.pg7_fondo` | 2 | 2 | 2 x PG7 en el fondo hacia el riel (camaras) | equipo | confirmado |
| `caja.pg7_umbilical` | tapa | auto | 'auto': en la tapa si la contratuerca colgada no choca con nada; si no, en la pared -X (el prompt admite 'de costado o arriba'). 'tapa' / 'pared' lo fuerzan | estimado | por_verificar |
| `caja.pg7_umbilical_xy` | 0 × 18 | -20 × 16 | Posicion preferida en la tapa; se busca la libre mas cercana | estimado | por_verificar |
| `asa.franja_libre_y` | nuevo | 17.5 | |y| minimo del PG7 de la tapa: asa de 12 de ancho + radio del domo + 2 | estimado | por_verificar |
| `holgura.pines` | nuevo | 15 | Dupont + curva del cable sobre los pines | equipo | confirmado |
| `holgura.conector` | nuevo | 10 | Lateral en el lado de cada conector | equipo | confirmado |
| `holgura.contratuerca` | 20 | 5 | Libre alrededor de cada contratuerca PG7 desde sus esquinas. Los prensaestopas se aprietan con la caja vacia, antes de meter las bandejas | equipo | confirmado |
| `holgura.usb` | nuevo | 35 | Enchufe USB-C con su moldeado + curva, sin sacar la bandeja | estimado | por_verificar |
| `holgura.microsd` | nuevo | 15 | Dedo para sacar la tarjeta | estimado | por_verificar |
| `holgura.entre_modulos` | nuevo | 2 | Cuerpo a cuerpo o cuerpo a zona de acceso | estimado | por_verificar |
| `holgura.pared` | 1 | 2 | Cuerpo o bandeja a la pared interior | estimado | por_verificar |
| `bandeja.espesor` | nuevo | 3 |  | estimado | por_verificar |
| `bandeja.apoyo` | nuevo | 8 | Por encima de los refuerzos M4 (6) del fondo | estimado | por_verificar |
| `bandeja.partir` | True | auto | 'auto': se parte en der/izq solo si pasa de 150; True / False fuerzan | estimado | por_verificar |
| `caja.pisos` | nuevo | auto | Se comparan 1 y 2 pisos y se usa el de menor aire sellado; 1 o 2 lo fuerzan | equipo | confirmado |
| `bandeja.poste_D` | nuevo | 8 | Postes del piso superior (2 pisos), con M3 | estimado | por_verificar |
| `bandeja.cuna_apoyo` | nuevo | 4 | Repisas de la cuna bajo los extremos cortos de la ESP32 | estimado | por_verificar |
| `bandeja.boss_D` | nuevo | 8 | Refuerzo del fondo con inserto M3 que sujeta la bandeja | estimado | por_verificar |
| `bandeja.boss_margen` | nuevo | 6 | Centro del refuerzo al borde de la bandeja | estimado | por_verificar |
| `comp.esp32_devkitc1` | 52 × 28 × 13 × 10 | 69 × 26 × 15 × 10 | ESP32-S3-DevKitC-1 N16R8, pines hacia abajo | estimado | por_verificar |
| `comp.kit_a` | nuevo | 80 × 70 × 12 × 25 | Alternativa paramétrica, medir la pieza | estimado | por_verificar |
| `comp.xy017` | 44 × 14 × 12 × 3 | 45 × 15 × 12 × 4 | XY-017 RS-485 | estimado | por_verificar |
| `comp.microsd` | 42 × 24 × 12 × 4 | 42 × 24 × 12 × 4 | Lector microSD SPI | estimado | por_verificar |
| `comp.mpu6050` | nuevo | 21 × 16 × 12 × 3 | GY-521, atornillado rigido | estimado | por_verificar |
| `comp.hw517` | nuevo | 34 × 17 × 12 × 4 | HW-517 (x2), bornes en ambos extremos | estimado | por_verificar |
| `masa.pg7` | nuevo | 5 | Prensaestopas de nylon con contratuerca | estimado | por_verificar |
| `masa.tornilleria_caja` | 60 | 30 | M3/M4 + insertos de la caja | estimado | por_verificar |
| `masa.cables_caja` | 40 | 20 | Dupont + Cat5e dentro de la caja | estimado | por_verificar |
| `lastre.objetivo_kgf` | nuevo | 0.2 × 0.5 | Peso aparente hacia abajo | equipo | confirmado |
| `lastre.empaque` | nuevo | tuercas: 0.5, barra: 0.9 | Fraccion de acero en el volumen del bolsillo | estimado | por_verificar |
| `lastre.bolsillo_prof` | nuevo | 20 | Menor que el alto del riel (30) | estimado | por_verificar |
| `lastre.bolsillo_pared` | nuevo | 2 |  | estimado | por_verificar |
| `lastre.holgura_riel` | nuevo | 1 | Bolsillos al lado del riel, no debajo | estimado | por_verificar |
| `lastre.bolsillo_largo` | nuevo | 140 | Igual al tramo central | estimado | por_verificar |
| `lastre.bolsillos_caja` | True | False | Reemplazados por la pletina de inox bajo el tramo central (revision 28/10) | equipo | confirmado |
| `lastre.pletina` | nuevo | 25 × 5 | Pletina de inox comercial (ancho x espesor); se apilan. Medir la comprada | estimado | por_verificar |
| `lastre.pletina_largo` | nuevo | 130 | Largo de cada trozo; cabe bajo la brida de 140 | estimado | por_verificar |
| `lastre.pletina_lados` | nuevo | 2 | Una pila a cada lado de la camara, simetricas | estimado | por_verificar |
| `lastre.bolsillo_pletina_pared` | nuevo | 3 | Pared y tapa del bolsillo de la pletina | estimado | por_verificar |
| `lastre.holgura_pletina` | nuevo | 0.5 | Holgura de la pletina en su bolsillo | estimado | por_verificar |
| `lastre.pletina_nivel` | nuevo | abajo | 'abajo': bolsillos pegados a los costados de la camara, al nivel del fondo del riel (baja el centro de masa); 'brida': colgados de la brida, justo bajo la caja | estimado | por_verificar |
| `lastre.bolsillo_pletina_y` | nuevo | 24.5 | Cara interior del bolsillo: deja libre la cabeza del M4 de la caja (y 20 + 3.5 + 1) | estimado | por_verificar |
| `camara.envolvente` | 33 × 33 × 25 × 20 | 33 × 33 × 17 × 20 | Arducam Mega 5MP AF, 33 x 33 x 17 | fabricante | confirmado |
| `camara.cable_incluido` | nuevo | 300 | Medir el recibido | fabricante | por_verificar |
| `aro_led.envolvente` | nuevo | 30 × 3 | Ø exterior x espesor, sin comprar | estimado | por_verificar |
| `ventana.diametro` | 30 | 30 | Acrilico, cubre lente + LED | estimado | por_verificar |
| `ventana.espesor` | 3 | 3 |  | estimado | por_verificar |
| `capsula.pared` | 4 | 4 |  | equipo | confirmado |
| `bisagra.dientes` | 36 | 36 | Bisagra dentada M4 se conserva | equipo | confirmado |
| `bisagra.inclinacion` | 40 | 40 | Multiplo de 10 | estimado | por_verificar |
| `masa.capsula_set` | nuevo | 104 | M4+M5+M6 (100 %) + ventana, de cad/reporte_verificacion.md (P4 rev. B vieja) | estimado | por_verificar |
| `volumen.capsula_set` | nuevo | 154 | PETG 79.5 + aire 72 + ventana 2.1 cm3 por capsula (P4 rev. B vieja) | estimado | por_verificar |
| `masa.capsula_contenido` | nuevo | 35 | Camara 20 + LED + cable + PG7 | estimado | por_verificar |
| `masa.otras_piezas` | nuevo | 200 | Ganchos, carros, perillas, casquillos, pestillos, tornilleria del riel (sin modelar) | estimado | por_verificar |
| `cable.cat5e_D` | nuevo | 5.5 | Cat5e de exterior, entra en PG7 | estimado | por_verificar |
| `cable.radio_curva_xD` | nuevo | 4 | Radio minimo = 4 x diametro | estimado | por_verificar |
| `cable.radio_curva_min` | nuevo | 25 | Revision 28/10: radio del Cat5e >= 25 | equipo | confirmado |
| `cable.holguras` | nuevo | caja: 60, prensaestopas: 25, bucle: 40, capsula: 30, holgura: 30 | Prompt v2 punto 7 | equipo | confirmado |
| `cable.limite_sin_prueba` | nuevo | 300 | > 300: prueba SPI a 8 y 4 MHz | equipo | confirmado |
| `boya.pcb` | nuevo | 70 × 73.5 × 1.6 | Placa fabricada; agujeros por verificar | equipo | por_verificar |
| `boya.waveshare_D` | nuevo | 45 × 40 × 10.1 | Solar Power Manager (D) | fabricante | confirmado |
| `boya.portabaterias` | nuevo | 80 × 70 × 30 | 3 x 18650 | estimado | por_verificar |
| `boya.rtc_reserva` | nuevo | 40 × 25 × 15 | DS3231, montaje sin confirmar | equipo | por_verificar |
| `boya.panel` | nuevo | 170 × 170 × 3 | Por anuncio; medir | estimado | por_verificar |
| `boya.panel_elevacion` | nuevo | 20 × 30 |  | equipo | confirmado |
| `boya.francobordo_min` | nuevo | 50 |  | equipo | confirmado |
| `umbilical` | nuevo | 6 × 3000 | Ø x largo; medir el cable real | estimado | por_verificar |

## 2. 1 piso contra 2 pisos (holgura de contratuerca 5 mm, relleno de bandeja 40 %)

| Concepto | 1 piso | 2 pisos |
|---|---|---|
| Cavidad | 131.6 × 98 × 46 | 108 × 74 × 76 |
| Caja con brida y tapa | 159.6 × 126 × 55 | 136 × 102 × 85 |
| Volumen de la cavidad cm³ | 593 | 607 |
| **Aire sellado cm³** | **484** | **485** |
| Desplaza la caja (cuerpo cerrado + tapa) cm³ | 935 | 912 |
| Empuje de la caja g | 958 | 935 |
| Caja en aire g (M1+M2 al 100 %, bandejas 40 %, electrónica) | 573 | 541 |
| Peso aparente de la caja sola g (+ hunde) | -385 | -394 |
| Pletinas por lado (Ø100 / Ø500) | 3 / 3 | 3 / 3 |
| Bandejas | M11_bandeja: 127.6 × 94 | M11_bandeja: 104 × 70 |
| Choques | 0 | 0 |

**Elegido: 1 piso** (menor aire sellado). La variante descartada queda a un switch: `caja.pisos` = 1 o 2 en `params.py`.

## 3. Caja elegida (derivada del layout)

| Concepto | sin_base (por defecto) | kit_a 1 piso | kit_a 2 pisos |
|---|---|---|---|
| Cavidad | 131.6 × 98 × 46 | 131.6 × 142 × 58 | 119 × 118 × 73 |
| Exterior del cuerpo | 139.6 × 106 × 50 | 139.6 × 150 × 62 | 127 × 126 × 77 |
| Con brida y tapa | 159.6 × 126 × 55 | 159.6 × 170 × 67 | 147 × 146 × 82 |
| Cabe en cama 220 × 220 × 250 | sí | sí | sí |
| Bandejas ≤ 150 | sí | sí | sí |
| Choques | 0 | 0 | 0 |

Prensaestopas del fondo en x = ±11.16, y = 0. Agujero de la bandeja sobre cada contratuerca: radio 13.66 (esquina 8.66 + 5); se aprietan con la caja vacía. Umbilical: en la tapa en -53.2 × 17.5.

| Módulo | Cuerpo x0, x1, y0, y1, z0, z1 | Bandeja |
|---|---|---|
| ESP32-S3 DevKitC-1 | -38.2, 30.8, -13.0, 13.0, 30.0, 45.0 | M11_bandeja |
| microSD SPI | -46.0, -4.0, 23.0, 47.0, 15.0, 27.0 | M11_bandeja |
| XY-017 RS-485 | 6.0, 51.0, 23.0, 38.0, 15.0, 27.0 | M11_bandeja |
| HW-517 #1 | -49.5, -15.5, -40.0, -23.0, 15.0, 27.0 | M11_bandeja |
| HW-517 #2 | -5.5, 28.5, -40.0, -23.0, 15.0, 27.0 | M11_bandeja |
| MPU-6050 | 38.5, 59.5, -39.0, -23.0, 15.0, 27.0 | M11_bandeja |

## 4. Cámara de cables (M3_riel_central, C12)

| Concepto | Valor |
|---|---|
| Radio de curvatura usado | 25 (máx de 4 × Ø5.5 y 25) |
| Alto interior (domo 22 + radio 25 + medio cable 2.75 + nervio 3.6) | 53.4 |
| Fondo del riel bajo la caja | z = -57.4 (el tramo cuelga 57.4 bajo el fondo de la caja) |
| Conducto de 22 | z -53.4 a -31.4; el cable corre a z = -47.0 |
| Zona abierta bajo la caja | |x| ≤ 27.6; rampa a 45° hasta |x| = 55 (empieza la unión) |
| Brida superior | 140 × 56.0 × 4, con los 4 M4 a la caja en 40 × 20; 40 × -20; -40 × 20; -40 × -20 |
| Chequeos del recorrido | radio_curva_ok: sí, cable_sobre_nervios: sí, cable_en_conducto: sí, tramo_recto_antes_de_la_union: sí, holgura_min_techo: 12.9 mm, domo_en_la_abertura: sí, m4_fuera_de_la_camara: sí |

## 5. Chequeos de sólidos

| Pieza | BRepCheck | BOPAlgo | Sólidos | Arista mín | Cara mín | Resultado |
|---|---|---|---|---|---|---|
| M1_caja_cuerpo (preliminar) | ok | ok | 1 | 4.00 | 5.37 | ok |
| M2_caja_tapa (preliminar) | ok | ok | 1 | 1.50 | 8.25 | ok |
| M11_bandeja | ok | ok | 1 | 3.00 | 9.42 | ok |
| tapa_bolsillo_n (referencia) | ok | ok | 1 | 3.00 | 87.03 | ok |
| tapa_bolsillo_s (referencia) | ok | ok | 1 | 3.00 | 87.03 | ok |
| M3_riel_central (referencia) | ok | ok | 1 | 1.70 | 52.78 | ok |

| Par | Interferencia con M1 mm³ | con la bandeja mm³ |
|---|---|---|
| ESP32-S3 DevKitC-1 | 0.00 | 0.00 |
| microSD SPI | 0.00 | 0.00 |
| XY-017 RS-485 | 0.00 | 0.00 |
| HW-517 #1 | 0.00 | 0.00 |
| HW-517 #2 | 0.00 | 0.00 |
| MPU-6050 | 0.00 | 0.00 |
| M11_bandeja ↔ M1 | 0.00 |  |
| M3_riel_central ↔ M1 | 0.00 |  |

## 6. Aire sellado, empuje y lastre (C13)

M1, M2, M4, M5 y los tramos del riel al 100 % con 5 perímetros. Bandeja y piezas no selladas: 40 % y 100 %.

| Concepto | Valor |
|---|---|
| Aire sellado (cavidad − bandejas − módulos − contratuercas) | 484 cm³ |
| Volumen desplazado por la caja | 935 cm³ → empuje 958 g |
| Cámara + tapas de bolsillo (100 %) | 198 cm³, 251 g |
| Electrónica + 3 PG7 + tornillería + cables (estimado) | 94 g |
| Pletina de inox 25 × 5 × 130 | 128 g cada una, hunde 112 g; se ponen de a 2 (una por lado) |
| Bolsillos (uno por lado, fuera del sello, pegados a la cámara al nivel del fondo del riel) | 3 pletinas por lado, 15.5 de hondo |

**Nodo completo** (extensiones por sección al 100 %, cápsulas P4 rev. B viejas, 200 g de ganchos/carros/perillas sin modelar). Objetivo: 0.2 a 0.5 kgf hacia abajo:

| Relleno bandeja | Aro | Riel mm | Nodo sin lastre g | Desplaza cm³ | Peso aparente sin lastre g | Acero para la ventana g | Pletinas por lado | Peso aparente final g | Total en aire g |
|---|---|---|---|---|---|---|---|---|---|
| 40 % | Ø100 | 140 | 1302 | 1598 | -336 | 616 a 961 | 3 | +334 | 2072 |
| 40 % | Ø200 | 340 | 1407 | 1681 | -316 | 593 a 937 | 3 | +355 | 2178 |
| 40 % | Ø300 | 340 | 1407 | 1681 | -316 | 593 a 937 | 3 | +355 | 2178 |
| 40 % | Ø500 | 540 | 1513 | 1764 | -295 | 569 a 914 | 3 | +375 | 2283 |
| 100 % | Ø100 | 140 | 1306 | 1598 | -332 | 611 a 956 | 3 | +338 | 2076 |
| 100 % | Ø200 | 340 | 1411 | 1681 | -312 | 588 a 933 | 3 | +359 | 2182 |
| 100 % | Ø300 | 340 | 1411 | 1681 | -312 | 588 a 933 | 3 | +359 | 2182 |
| 100 % | Ø500 | 540 | 1517 | 1764 | -291 | 565 a 909 | 3 | +379 | 2287 |

Estabilidad del nodo completo (aproximada; bandeja al 40 %, cápsulas y extensiones a la altura del riel):

- Ø100: centro de masa z = -8.9, centro de empuje z = -0.7 → el de masa queda 8.2 mm debajo: no se voltea.
- Ø500: centro de masa z = -13.6, centro de empuje z = -4.4 → el de masa queda 9.1 mm debajo: no se voltea.

El cálculo completo (momentos, metacentro) es la Fase E.
