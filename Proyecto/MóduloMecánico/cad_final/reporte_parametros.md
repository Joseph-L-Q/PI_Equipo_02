# Parámetros (generado por `reporte_parametros.py` desde `params.py`)

350 parámetros. Por origen y estado: equipo / confirmado: 72; equipo / por_verificar: 16; estimado / confirmado: 1; estimado / por_verificar: 245; fabricante / confirmado: 7; fabricante / por_verificar: 9.

## 1. Qué cambió (tienen valor anterior)

| Parámetro | Anterior | Nuevo | Origen | Estado | Razón |
|---|---|---|---|---|---|
| `impresora.cama` | 220 × 220 × 250 | 256 × 256 × 256 | fabricante | confirmado | Bambu Lab P1P (volumen de impresion de la hoja del fabricante) |
| `impresion.relleno_sellado` | 0.4 | 1 | equipo | confirmado | M1, M2, M4, M5 y tramos del riel al 100 % (revision 28/10, C13) |
| `impresion.holgura` | 1 | 0.3 | estimado | por_verificar | Handoff; probar con el peine de la Fase B |
| `profundidad_m` | 15 | 1 | equipo | confirmado | Prueba real: 1 m varios dias. No se afirma 15 m |
| `aro.diametros` | 500 | 100 × 200 × 300 × 500 | equipo | confirmado | Nodo ajustable de Ø100 a Ø500; un ensamble por aro |
| `aro.varilla_D` | 12 | 6 × 8 × 10 × 12 | estimado | por_verificar | Varilla real sin medir: un casquillo por diametro |
| `riel.seccion` | 30 × 25 | 30 | equipo | confirmado | Cuadrado 30 x 30, hueco = conducto inundado |
| `riel.pared` | 3 | 4 | equipo | confirmado | Prompt v2 |
| `riel.central_L` | 190 | 140 | equipo | confirmado | M3_riel_central bajo la caja |
| `riel.varilla_M8` | False | True | equipo | confirmado | Varilla roscada M8 obligatoria en todo el riel, tensada con tuerca + arandela en las dos puntas (29/10, C19) |
| `riel.camara_rampa` | 45 | 60 | estimado | por_verificar | Techo en rampa hacia el conducto de 22. Con la varilla (C19) la camara crece 12.4 y a 45 grados la rampa tapaba el domo del PG7; el central se imprime boca abajo, asi que la rampa queda como piso |
| `correa.ancho` | 26 | 25 | equipo | confirmado | Correa textil de seguridad |
| `carro.largo` | 40 | 60 | estimado | por_verificar | M10 a lo largo del riel: perilla atras (cilindro libre de 34) + 25 de quilla abulonada adelante |
| `caja.pared` | 5 | 4 | equipo | confirmado | A 1 m la presion no manda (0.0101 MPa) |
| `caja.fondo` | 6 | 4 | equipo | confirmado | Igual que la pared |
| `caja.tapa` | 6 | 5 | estimado | por_verificar | Ranura de 1.5 deja 3.5 bajo la junta |
| `caja.brida_ancho` | 9 | 10 | estimado | por_verificar | Ranura + inserto M3 (agujero 4.0) con 3 mm de pared |
| `caja.brida_espesor` | 6 | 8 | estimado | por_verificar | Inserto M3 de 5.7 + 2 de fondo |
| `caja.paso_tornillos` | 76 | 65 | estimado | por_verificar | Separacion maxima entre M3 de la tapa: compresion pareja de la junta |
| `caja.base_m4` | 51.5 × 6 × 51.5 × -6 × -51.5 × 6 × -51.5 × -6 | 40 × 20 × 40 × -20 × -40 × 20 × -40 × -20 | estimado | por_verificar | 4 M4 desde la brida superior de la camara a insertos ciegos en el fondo (no perforan el sello); /y/ = 20: la cabeza (Ø7) queda entre la camara (/y/ 15) y el bolsillo de la pletina; se aprieta desde abajo |
| `caja.pg7_umbilical` | tapa | auto | estimado | por_verificar | 'auto': en la tapa si la contratuerca colgada no choca con nada; si no, en la pared -X (el prompt admite 'de costado o arriba'). 'tapa' / 'pared' lo fuerzan |
| `caja.pg7_umbilical_xy` | 0 × 18 | -20 × 16 | estimado | por_verificar | Posicion preferida en la tapa; se busca la libre mas cercana |
| `holgura.contratuerca` | 20 | 5 | equipo | confirmado | Libre alrededor de cada contratuerca PG7 desde sus esquinas. Los prensaestopas se aprietan con la caja vacia, antes de meter las bandejas |
| `holgura.pared` | 1 | 2 | estimado | por_verificar | Cuerpo o bandeja a la pared interior |
| `bandeja.partir` | True | auto | estimado | por_verificar | 'auto': se parte en der/izq solo si pasa de 150; True / False fuerzan |
| `comp.esp32_devkitc1` | 52 × 28 × 13 × 10 | 69 × 26 × 15 × 10 | estimado | por_verificar | ESP32-S3-DevKitC-1 N16R8, pines hacia abajo |
| `comp.xy017` | 44 × 14 × 12 × 3 | 45 × 15 × 12 × 4 | estimado | por_verificar | XY-017 RS-485 |
| `masa.tornilleria_caja` | 60 | 30 | estimado | por_verificar | M3/M4 + insertos de la caja |
| `masa.cables_caja` | 40 | 20 | estimado | por_verificar | Dupont + Cat5e dentro de la caja |
| `lastre.bolsillos_caja` | True | False | equipo | confirmado | Reemplazados por la pletina de inox bajo el tramo central (revision 28/10) |
| `lastre.pletina_largo` | 130 | 100 | estimado | por_verificar | Largo de cada trozo: el bolsillo (/x/ <= 53.5) deja libre la zona de la union (/x/ > 55) para que la extension entre de costado |
| `lastre.tapa_tornillo_x` | 40 | 30 | estimado | por_verificar | /x/ de los 2 tornillos M3 avellanados de cada tapa del bolsillo (decision 29/10: 2 M3 a insertos); en Ø100 las cuerdas al asa pasan cerca de x = 40 (a 40 rozan la orejeta, a 30 quedan a 9 mm) |
| `camara.envolvente` | 33 × 33 × 25 × 20 | 33 × 33 × 17 × 20 | fabricante | confirmado | Arducam Mega 5MP AF, 33 x 33 x 17 |
| `masa.capsula_set` | 104 | 93.1 | estimado | por_verificar | M4+M5 al 100 % + M6 + ventana, de capsula.py (Fase C, cavidad 38 x 38 x 38) |
| `volumen.capsula_set` | 154 | 127.8 | estimado | por_verificar | PETG 71.5 + aire 54.2 + ventana 2.1 cm3 por capsula, de capsula.py (Fase C) |
| `capsula.holgura_lente` | 1 | 0.5 | estimado | por_verificar | Punta del lente a la cara trasera de la ventana |
| `ventana.apertura` | 22 | 26 | estimado | por_verificar | Apertura libre tras la ventana: deja pasar el anillo LED (Ø30) con 2.2 de hombro para el acrilico |
| `carro.modo` | tope | deslizante | estimado | por_verificar | deslizante: manga abierta en los dos extremos, perilla abajo en la T, bisagra bajo el riel (+-50). tope: version del agente con placa de tope sobre el eje del riel (solo a ras de la punta) |
| `riel.paso_extension` | solape | paso_100 | equipo | confirmado | paso_100 (decision 29/10): la lengueta macho sale fuera del cuerpo de 100 (pieza de 115) y cada extension suma 100. solape: la version anterior, extension de 100 solapada 15 (suma 85), sin punta |
| `riel.varilla_M8_datos` | d_nucleo: 6.47, E: 200000 | d: 8, d_nucleo: 6.47, A_s: 36.6, E: 200000, fy_8.8: 640, fy_4.6: 240 | fabricante | por_verificar | Varilla roscada M8 de acero (ISO 898-1): nucleo, area resistente, modulo y fluencia de los grados 8.8 y 4.6 |
| `separador.altura` | 250 | 140 | equipo | confirmado | Plano medio del separador sobre el centro de la varilla del aro. V2 (caja baja): el minimo calculado con 10 mm de aire es 136, se usa 140 (antes 250) |

## 2. Qué hay que medir o confirmar (estado por_verificar)

### Origen fabricante (9)

| Parámetro | Valor | Razón |
|---|---|---|
| `riel.varilla_arandela` | 24 × 2 × 8.4 | Arandela ancha DIN 9021 M8: Ø ext x espesor x Ø int (reparte el apriete sobre el PETG) |
| `riel.varilla_tuerca` | 13 × 6.5 | Tuerca M8 DIN 934: entrecaras x alto |
| `m4.tuerca` | 7 × 3.2 | AF x espesor, DIN 934 |
| `m4.cabeza` | 7 × 4 | Allen DIN 912: Ø x alto |
| `m4.cabeza_hex` | 7 × 2.8 | Perno hexagonal DIN 933: AF x alto (perilla) |
| `m3.tuerca` | 5.5 × 2.4 | AF x espesor, DIN 934 |
| `m3.cabeza_avellanada` | 6.72 × 1.86 | ISO 10642 M3 (cabeza a 90 grados): diametro y alto; la tapa queda al ras del fondo del riel |
| `camara.cable_incluido` | 300 | Medir el recibido |
| `riel.varilla_M8_datos` | d: 8, d_nucleo: 6.47, A_s: 36.6, E: 200000, fy_8.8: 640, fy_4.6: 240 | Varilla roscada M8 de acero (ISO 898-1): nucleo, area resistente, modulo y fluencia de los grados 8.8 y 4.6 |

### Origen equipo (16)

| Parámetro | Valor | Razón |
|---|---|---|
| `aro.cuerdas` | 4 | 3 o 4 cuerdas desde el borde; sin cabo central |
| `pestillo.resalte` | 0.6 | Traba del M14; probar en probeta |
| `boya.pcb` | 70 × 73.5 × 1.6 | Placa fabricada; agujeros por verificar |
| `boya.rtc_reserva` | 40 × 25 × 15 | DS3231, montaje sin confirmar |
| `ensamble.cuerda_azimut` | 45 × 135 × 225 × 315 | Cuerdas entre los dos lados de la barra: la barra cruza el aro por el centro, orientada entre dos cuerdas |
| `material` | PETG opaco | Melissa 29/10: PETG opaco en todas las piezas, no ASA |
| `simple.esp32_base` | kit_a | Melissa 29/10: ESP32-S3 N16R8 sobre KIT A + modulos sueltos (acelerometro, microSD) en la caja. esp32.base sigue en sin_base para la modular |
| `capsula.acimut` | adentro | Melissa 29/10: camaras inclinadas hacia la malla. adentro: miran al eje de la linterna; afuera: hacia las puntas del riel (version V1) |
| `ventana.antibiofouling` | spray | Melissa 29/10: antibiofouling en spray sobre las ventanas (no cambia la geometria) |
| `enlace.nodo_boya` | RS-485 en el umbilical | Melissa 29/10: modulo XY-017 en la caja, par trenzado del umbilical |
| `boya.caja_exterior` | 220 × 200 × 120 | Melissa 29/10: caja central hermetica de la boya ~220 x 200 x 120 exterior (cuerpo; la brida de la tapa sale aparte) |
| `boya.caja_interior` | 210 × 190 | Melissa 29/10: 210 x 190 interior (pared de 5) |
| `boya.flotadores_esquinas` | 4 | Melissa 29/10: flotadores modulares en las 4 esquinas |
| `boya.antena_interior` | True | Melissa 29/10: antena LoRa pequena de la Heltec dentro de la carcasa, despejada de metal y del panel: sin mastil |
| `boya.sma_ciego` | True | Melissa 29/10: agujero ciego reservado para un SMA de panel (antena externa futura), lejos de los cables |
| `linterna.profundidad` | 1000 | Aro de la linterna a 1 m bajo la superficie (prueba real) |

### Origen estimado (245)

| Parámetro | Valor | Razón |
|---|---|---|
| `impresion.cascara` | 1.2 | Perimetros + capas sup/inf macizos, para la masa con relleno |
| `impresion.holgura` | 0.3 | Handoff; probar con el peine de la Fase B |
| `impresion.comp_agujero` | 0.2 | Handoff; probar en impresora real |
| `petg.densidad` | 1.27 | Sustituir por el dato del slicer |
| `costo.factor_relleno` | 0.45 | EN DESUSO desde el 29/10 (bloque J): la bitacora usa la masa por pieza del calculo de flotacion (piel + relleno de cada pieza) |
| `costo.g_por_h` | 15 | Bitacora: gramos por hora de la impresora; el slicer lo reemplaza |
| `costo.filamento_soles_kg` | 90 | Bitacora: precio del PETG en soles por kg; confirmar con la boleta |
| `petg.E` | 1700 | PETG manual para SimScale |
| `petg.nu` | 0.38 | PETG manual |
| `petg.sigma_y` | 45 | Macizo, a lo largo de las capas |
| `petg.sigma_capas` | 22 | Entre capas, mitad del macizo |
| `aro.varilla_D` | 6 × 8 × 10 × 12 | Varilla real sin medir: un casquillo por diametro |
| `riel.punta_tapa` | 5 | Pared del extremo de la punta donde apoyan la arandela y la tuerca de la varilla M8; deja abierta la ranura T para meter las tuercas |
| `riel.ranura_T` | abertura: 4.6, ancho: 8, alto: 3.6 | Para tuerca M4 (AF7 x 3.2); se ajusta con la probeta de la Fase B |
| `riel.varilla_grado` | 8.8 | 8.8 o 4.6 (la que se compre); el calculo se hace con las dos |
| `riel.varilla_aire_ranura` | 1 | Aire entre el techo del canal de tuercas (nervios) y el refuerzo de la varilla: pasan las tuercas y la punta de un M4 x 14 |
| `riel.varilla_pared` | 1.2 | Pared del refuerzo alrededor del agujero de 8.5 (minimo de impresion) |
| `riel.varilla_aire_cable` | 0.5 | Aire entre el refuerzo de la varilla y el Cat5e que va encima |
| `riel.varilla_tabique` | 3 | Espesor (a lo largo del riel) del tabique con el agujero de 8.5; uno en cada extremo del cuerpo de cada tramo |
| `riel.varilla_sobrante` | 2 | Rosca que asoma pasada la tuerca en cada punta |
| `riel.varilla_precarga` | 500 | Tension de apriete; con T = 0.2 d F son unos 0.8 N m. Reapretar tras unos dias (fluencia del PETG) |
| `riel.varilla_masas` | g_por_mm: 0.32, tuerca: 5, arandela: 6.5 | Varilla M8 de acero cincado o inox, por mm; tuerca y arandela DIN 9021. Pesar |
| `riel.camara_rampa` | 60 | Techo en rampa hacia el conducto de 22. Con la varilla (C19) la camara crece 12.4 y a 45 grados la rampa tapaba el domo del PG7; el central se imprime boca abajo, asi que la rampa queda como piso |
| `riel.camara_brida` | 56 × 4 | Brida superior (ancho minimo x espesor): lleva los 4 M4 a la caja y cuelga los bolsillos de la pletina; el ancho real lo fijan los bolsillos |
| `riel.ventana_cable` | 24 × 14 | OBSOLETO desde la revision del 28/10: el tramo central es una camara de cables (riel.camara_*) |
| `riel.ranura_T_nervio` | 2 | Nervios que encierran el canal de la tuerca sobre el fondo; la tuerca entra por la punta del tramo |
| `riel.union_z` | 15 | Media madera: el macho conserva la mitad de abajo (con la ranura T), la hembra la de arriba |
| `riel.cola_llave` | 8 × 11 × 4 | Llave en cola de milano vista de lado (base, punta, alto) en la cara de la media madera; entra deslizando de costado |
| `riel.union_pared` | 10 | Paredes engrosadas hacia adentro en la union para la tuerca M4 con 1.4 de piel; conducto local 10 de ancho: cada lado del riel lleva un solo Cat5e (5.5) |
| `riel.union_m4_y` | 10 | 2 M4 verticales dentro de las paredes (y = +-10): no cruzan el conducto de cables |
| `gancho.alojamiento` | 16 | Ø del asiento del casquillo en la J (varilla max 12 + pared) |
| `casquillo.interferencia` | 0.15 | Exceso de Ø del casquillo sobre el asiento |
| `casquillo.holgura_varilla` | 0.4 | Ø interior = varilla + holgura |
| `casquillo.pestana` | 20 × 1.5 | Ø x espesor de la pestana de tope |
| `pestillo.lengueta` | 18 × 12 | Largo x ancho de la lengueta para el pulgar con guante |
| `perilla.alto` | 12 | Alto de la perilla |
| `perilla.lobulos` | 8 | Moleteado grueso para guante |
| `peine.pin_D` | 8 | Pin de prueba |
| `probeta.inserto_M4` | 40 × 30 | PB8: placa de 40 x 40 con el espesor del fondo de la caja y el refuerzo del inserto; 4 agujeros M4 a 30 para atornillarla a un marco con hueco central y tirar del inserto (29/10) |
| `probeta.tramo_L` | 40 | PB2/PB3 rail length per segment |
| `gancho.pared` | 4 | minimum wall around the hook seat |
| `gancho.labio_alto` | 10 | height of the upper lip that carries the latch pivot |
| `correa.ranura_t` | 3 | strap slot thickness (slot is STRAP_W x this) |
| `gancho.vastago_alto` | 20 | stem above the jaw, carries the M4 hole to bolt PB1 to PB2 |
| `pestillo.espesor` | 3.6 | latch plate thickness (Y) |
| `pestillo.brazo_ancho` | 5 | latch arm width (X) |
| `pestillo.cresta_ancho` | 1.2 | catch ridge width on the jaw lip |
| `pestillo.holgura_punta` | 0.2 | closed latch tip to lip clearance |
| `pestillo.giro_media_ranura` | 4.5 | half width of the latch slot in the upper lip (swing room) |
| `perilla.lobulo_r` | 3.5 | radius of each grip lobe |
| `perilla.tapa_cabeza` | 1.2 | roof over the embedded bolt head (print pause) |
| `probeta.junta_radio_cavidad` | 14 | inner corner radius of the seal base cavity (land follows the groove path) |
| `probeta.junta_radio_ext` | 2 | outer corner radius of the 60 x 60 seal parts |
| `peine.paso` | 18 | spacing of the comb holes |
| `peine.espesor` | 6 | comb plate thickness |
| `peine.ancho` | 26 | comb plate width |
| `peine.texto_alto` | 4.5 | engraved text height |
| `peine.texto_prof` | 0.6 | engraved text depth |
| `peine.pin_L` | 8 | comb pin length |
| `gancho.brida` | 50 × 6 | Largo (a lo largo del riel) x espesor de la placa que apoya bajo el riel; el M4 de la perilla va en un extremo, fuera del alma, para que la perilla quede al alcance |
| `gancho.caida` | 40 | Fondo del riel al centro de la varilla del aro; medir con el aro real |
| `carro.largo` | 60 | M10 a lo largo del riel: perilla atras (cilindro libre de 34) + 25 de quilla abulonada adelante |
| `carro.pared` | 4 | Manga en U invertida que abraza el tramo; la perilla aprieta en la T |
| `riel.salida_cable` | 8 × 20 × 10 | Ranura lateral de salida del Cat5e en cada extension: alto x largo x distancia a la punta exterior (prompt: sale junto al carro con bucle de 40) |
| `camara.lente_D` | 16 | Porta-lente de la Arducam Mega; medir |
| `aro_led.separador` | 1.2 × 3 | Tubo opaco entre LED y lente: pared x alto sobre el aro. Con 1.5 el tubo (r 9.7) chocaba con el agujero supuesto del anillo LED (r 9.5); el p1 de 1.19 es teselado sobre una pared de 1.2 exacta |
| `caja.tapa` | 5 | Ranura de 1.5 deja 3.5 bajo la junta |
| `caja.brida_ancho` | 10 | Ranura + inserto M3 (agujero 4.0) con 3 mm de pared |
| `caja.brida_espesor` | 8 | Inserto M3 de 5.7 + 2 de fondo |
| `caja.paso_tornillos` | 65 | Separacion maxima entre M3 de la tapa: compresion pareja de la junta |
| `caja.holgura_tapa` | 5 | Aire libre entre lo mas alto y la tapa |
| `m3.paso` | 3.4 |  |
| `m3.inserto_agujero` | 4 | Inserto termico M3 x 5.7 |
| `m3.inserto_prof` | 6 |  |
| `m4.paso` | 4.2 |  |
| `m4.inserto_agujero` | 5.6 | Inserto termico M4 x 8.1 |
| `m4.inserto_prof` | 8.5 |  |
| `caja.base_m4` | 40 × 20 × 40 × -20 × -40 × 20 × -40 × -20 | 4 M4 desde la brida superior de la camara a insertos ciegos en el fondo (no perforan el sello); /y/ = 20: la cabeza (Ø7) queda entre la camara (/y/ 15) y el bolsillo de la pletina; se aprieta desde abajo |
| `caja.base_m4_boss` | 10 × 6 | Ø x alto del refuerzo interior del inserto M4 |
| `asa.agarre` | 90 | Ancho de mano con guante |
| `asa.ojal` | 20 × 10 × 6 | Ojal del cabo sobre el asa: Ø exterior, Ø interior, altura del centro sobre el asa (de cad/parts.py). En Ø100 y Ø200 tambien se amarran ahi las 4 cuerdas de la linterna |
| `pg7.agujero` | 12.6 | Rosca PG7 12.5 |
| `pg7.contratuerca_AF` | 15 | Comprar y medir |
| `pg7.alto_interior` | 9 | Rosca que asoma + contratuerca por dentro |
| `pg7.domo` | 19 × 22 | Cuerpo + domo bajo el fondo: Ø maximo x largo desde la cara exterior. Comprar y medir |
| `caja.pg7_umbilical` | auto | 'auto': en la tapa si la contratuerca colgada no choca con nada; si no, en la pared -X (el prompt admite 'de costado o arriba'). 'tapa' / 'pared' lo fuerzan |
| `caja.pg7_umbilical_xy` | -20 × 16 | Posicion preferida en la tapa; se busca la libre mas cercana |
| `asa.franja_libre_y` | 17.5 | /y/ minimo del PG7 de la tapa: asa de 12 de ancho + radio del domo + 2 |
| `holgura.usb` | 35 | Enchufe USB-C con su moldeado + curva, sin sacar la bandeja |
| `holgura.microsd` | 15 | Dedo para sacar la tarjeta |
| `holgura.entre_modulos` | 2 | Cuerpo a cuerpo o cuerpo a zona de acceso |
| `holgura.pared` | 2 | Cuerpo o bandeja a la pared interior |
| `bandeja.espesor` | 3 |  |
| `bandeja.apoyo` | 8 | Por encima de los refuerzos M4 (6) del fondo |
| `bandeja.partir` | auto | 'auto': se parte en der/izq solo si pasa de 150; True / False fuerzan |
| `bandeja.poste_D` | 8 | Postes del piso superior (2 pisos), con M3 |
| `bandeja.cuna_apoyo` | 4 | Repisas de la cuna bajo los extremos cortos de la ESP32 |
| `bandeja.boss_D` | 8 | Refuerzo del fondo con inserto M3 que sujeta la bandeja |
| `bandeja.boss_margen` | 6 | Centro del refuerzo al borde de la bandeja |
| `comp.esp32_devkitc1` | 69 × 26 × 15 × 10 | ESP32-S3-DevKitC-1 N16R8, pines hacia abajo |
| `comp.kit_a` | 80 × 70 × 12 × 25 | Alternativa paramétrica, medir la pieza |
| `comp.xy017` | 45 × 15 × 12 × 4 | XY-017 RS-485 |
| `comp.microsd` | 42 × 24 × 12 × 4 | Lector microSD SPI |
| `comp.mpu6050` | 21 × 16 × 12 × 3 | GY-521, atornillado rigido |
| `comp.hw517` | 34 × 17 × 12 × 4 | HW-517 (x2), bornes en ambos extremos |
| `masa.pg7` | 5 | Prensaestopas de nylon con contratuerca |
| `masa.tornilleria_caja` | 30 | M3/M4 + insertos de la caja |
| `masa.cables_caja` | 20 | Dupont + Cat5e dentro de la caja |
| `lastre.empaque` | tuercas: 0.5, barra: 0.9 | Fraccion de acero en el volumen del bolsillo |
| `lastre.bolsillo_prof` | 20 | Menor que el alto del riel (30) |
| `lastre.bolsillo_pared` | 2 |  |
| `lastre.holgura_riel` | 1 | Bolsillos al lado del riel, no debajo |
| `lastre.bolsillo_largo` | 140 | Igual al tramo central |
| `lastre.pletina` | 25 × 5 | Pletina de inox comercial (ancho x espesor); se apilan. Medir la comprada |
| `lastre.pletina_largo` | 100 | Largo de cada trozo: el bolsillo (/x/ <= 53.5) deja libre la zona de la union (/x/ > 55) para que la extension entre de costado |
| `lastre.pletina_lados` | 2 | Una pila a cada lado de la camara, simetricas |
| `lastre.bolsillo_pletina_pared` | 3 | Pared y tapa del bolsillo de la pletina |
| `lastre.holgura_pletina` | 0.5 | Holgura de la pletina en su bolsillo |
| `lastre.bolsillo_capacidad` | 4 | Pletinas por lado que entran en cada bolsillo (fase_a.py verifica que alcance en todos los aros) |
| `lastre.pletina_nivel` | abajo | 'abajo': bolsillos pegados a los costados de la camara, al nivel del fondo del riel (baja el centro de masa); 'brida': colgados de la brida, justo bajo la caja |
| `lastre.bolsillo_pletina_y` | 24.5 | Cara interior del bolsillo: deja libre la cabeza del M4 de la caja (y 20 + 3.5 + 1) |
| `lastre.tapa_tornillo_x` | 30 | /x/ de los 2 tornillos M3 avellanados de cada tapa del bolsillo (decision 29/10: 2 M3 a insertos); en Ø100 las cuerdas al asa pasan cerca de x = 40 (a 40 rozan la orejeta, a 30 quedan a 9 mm) |
| `lastre.tapa_boss` | 10 × 6 | Boss del inserto M3 en la pared exterior del bolsillo (3 de pared no alcanzan para el inserto de 4): ancho en x y saliente hacia afuera; deja 2.5 de pared hacia las pletinas y 2.5 hacia afuera, y aire para el avellanado de la tapa |
| `aro_led.envolvente` | 30 × 3 | Ø exterior x espesor, sin comprar |
| `ventana.diametro` | 30 | Acrilico, cubre lente + LED |
| `ventana.espesor` | 3 |  |
| `bisagra.inclinacion` | 40 | Multiplo de 10 |
| `masa.capsula_set` | 93.1 | M4+M5 al 100 % + M6 + ventana, de capsula.py (Fase C, cavidad 38 x 38 x 38) |
| `volumen.capsula_set` | 127.8 | PETG 71.5 + aire 54.2 + ventana 2.1 cm3 por capsula, de capsula.py (Fase C) |
| `masa.capsula_contenido` | 35 | Camara 20 + LED + cable + PG7 |
| `masa.otras_piezas` | 200 | Ganchos, carros, perillas, casquillos, pestillos, tornilleria del riel (sin modelar) |
| `cable.cat5e_D` | 5.5 | Cat5e de exterior, entra en PG7 |
| `cable.radio_curva_xD` | 4 | Radio minimo = 4 x diametro |
| `boya.portabaterias` | 80 × 70 × 30 | 3 x 18650 |
| `boya.panel` | 170 × 170 × 3 | Por anuncio; medir |
| `umbilical` | 6 × 3000 | Ø x largo; medir el cable real |
| `capsula.frente` | 6 | Pared frontal (ventana + hombro de 2.8) |
| `capsula.brida_ancho` | 9 | Brida alrededor de la apertura trasera |
| `capsula.brida_espesor` | 6 |  |
| `capsula.tapa` | 5 | Espesor de la tapa M5 |
| `capsula.pg7_x` | 10 | Centro del PG7 desde la apertura trasera (pared inferior) |
| `capsula.holgura_lateral` | 2.5 | Camara 33 + 2 x 2.5 por lado = cavidad 38 |
| `capsula.zona_trasera` | 23 | Detras de la placa: curva del cable + contratuerca PG7 (50 - 25 - 2 de la P4 rev. B) |
| `capsula.holgura_lente` | 0.5 | Punta del lente a la cara trasera de la ventana |
| `ventana.asiento` | 3.2 | Rebaje desde fuera; el agua empuja el disco al hombro |
| `ventana.apertura` | 26 | Apertura libre tras la ventana: deja pasar el anillo LED (Ø30) con 2.2 de hombro para el acrilico |
| `aro_led.agujero` | 19 | Ø interior supuesto del anillo LED; medir el comprado |
| `aro_led.radios` | 3 × 2 | Radios (cantidad, ancho) que sujetan el tubo separador al frente; tapan algo de luz del LED |
| `bisel.diametro` | 42 |  |
| `bisel.espesor` | 2.5 |  |
| `bisel.tornillos` | 3 | M2 autorroscante en la pared frontal |
| `m2.piloto` | 1.8 |  |
| `bisagra.anillo_dientes_rin` | 7 | Anillo 7-12; el M4 de 4.2 queda libre |
| `bisagra.lengua_largo` | 16 | Eje a cara exterior de la tapa (fuera del sello) |
| `carro.oreja_alto` | 25 | Alto de las orejas de la horquilla del M10 |
| `carro.oreja_alcance` | 36 | Placa de tope a eje: la tapa (semiancho 32) a 90 grados queda 4 mm detras de la placa |
| `carro.placa_tope` | 4 | Placa que cierra la manga en el extremo exterior y lleva las orejas |
| `carro.labio_borde` | 6 | /y/ del borde interior de los labios: deja libre la abertura de la ranura T (2.3) y el perno |
| `carro.modo` | deslizante | deslizante: manga abierta en los dos extremos, perilla abajo en la T, bisagra bajo el riel (+-50). tope: version del agente con placa de tope sobre el eje del riel (solo a ras de la punta) |
| `carro.eje_holgura` | 2 | Aire entre la cara superior de la capsula a 0 grados y el fondo del riel; fija la caida del eje |
| `carro.quilla_holgura` | 1 | Aire radial entre el disco de la lengua y la quilla |
| `carro.rendija_holgura` | 1 | Margen por lado de la rendija lateral de la manga sobre el alto de la ranura de salida del cable |
| `carro.posiciones` | 5 | Posiciones del barrido de 0 a 2 x recorrido desde la punta del riel |
| `perilla.cilindro_libre_extra` | 4 | Cilindro libre bajo la perilla = KNOB_D + esto (guante) |
| `perilla.aire_alma` | 1 | Aire entre el cilindro libre y el alma o la quilla |
| `perilla.aire_brida` | 0.5 | Aire entre la cara donde sale el perno y la perilla |
| `casquillo.margen_punta` | 0.3 | Puntas de la C recortadas a MIN_WALL + esto; tambien el buje del pivote del pestillo |
| `gancho.solape_alma` | 0.5 | El alma entra en la brida para que la union sea un solido |
| `riel.paso_deslizamiento` | 10 | Paso del barrido del macho deslizando de costado (verificacion) |
| `ensamble.aro_varilla_D` | 8 | Diametro de la varilla del aro de la linterna de referencia (esquematica) |
| `ensamble.cuerda_D` | 4 | Diametro de las cuerdas de la linterna de referencia |
| `ensamble.apice_alto` | 400 | Altura del apice de las cuerdas sobre el aro; desconocida, se calcula el minimo |
| `ensamble.red_alto_k` | 1 | Alto de la red = k x diametro del aro |
| `ensamble.red_espesor` | 1 | Espesor de la cascara cilindrica que representa la red |
| `ensamble.holgura_cuerda` | 10 | Distancia libre minima entre cuerda y cualquier pieza del nodo |
| `ensamble.tol_interferencia` | 0.01 | Volumen comun (mm3) por encima del cual se marca interferencia |
| `ensamble.barrido_s` | 0 × 50 × 100 | Posiciones del carro (punta del riel pasada la manga) del barrido de la bisagra |
| `ensamble.barrido_paso` | 10 | Paso de inclinacion (grados) del barrido de la bisagra, de 0 a 90 |
| `ensamble.cuerda_aire_borde` | 0.5 | Aire del modelo entre la cuerda y el borde de la caja por donde la rodea (en la realidad apoya) |
| `ensamble.linterna_peso_agua_N` | 30 | Peso en el agua de la linterna (aro, red, cuerdas y carga) que cuelga del asa; pesarla |
| `riel.holgura_gancho_carro` | 1 | Aire a lo largo del riel entre la brida del gancho y la manga del carro |
| `boya.masas` | celda_18650: 47, portabaterias: 25, pcb_heltec: 35, waveshare: 15, rtc: 8, panel: 350, antena: 20, cables_fusible: 40, prensaestopas: 20, tornilleria: 60 | Masas de componentes en g, tipicas; pesar cada una. Celda 18650 ~47 g |
| `boya.sma_pasamuros_g` | 5 | Opcional, solo suma si boya.sma_pasamuros es True |
| `boya.antena_largo` | 110 | Antena LoRa incluida con la Heltec; medir |
| `boya.sma_agujero` | 6.5 | Agujero del pasamuros SMA en la tapa del mastil |
| `boya.holgura_modulos` | 5 | Aire entre modulos sobre la bandeja |
| `boya.alto_pcb_conectores` | 25 | PCB con Heltec en cabezal y conectores sobre la bandeja |
| `boya.apoyo_bateria` | 6 | Refuerzo M3 bajo el portabaterias (inserto de 6 sin tocar el fondo) |
| `boya.aire_bateria_bandeja` | 3 | Aire entre el portabaterias y la bandeja |
| `boya.portabaterias_agujeros` | 66 × 56 | Paso de los 4 agujeros del portabaterias; medir |
| `boya.bandeja_borde` | 2 | Margen de la bandeja alrededor de los modulos |
| `boya.poste_D` | 8 | Postes de la bandeja con inserto M3 |
| `boya.poste_aire_pared` | 1 | Aire entre poste y pared interior |
| `boya.umbilical_margen` | 3 | Del borde de la contratuerca a la pared, ademas de GAP_WALL |
| `boya.cable_aire` | 1 | Aire entre el codo del umbilical y la bandeja |
| `boya.pg7_solar` | 25 × 55 | (y, z) del PG7 del cable solar en la pared -X |
| `boya.panel_elevacion_usada` | 25 | Dentro de 20..30 |
| `boya.riel_panel` | 24 × 140 × 8 | B3: ancho x largo x espesor del larguero; largo <= PIECE_MAX_L |
| `boya.pata_D` | 14 | Patas del larguero sobre los tornillos M3 de la tapa (sin perforar) |
| `boya.avellanado` | 6.5 × 3 | Cabeza del M3 largo en el larguero: diametro, profundidad |
| `boya.panel_agujeros_y` | 20 | Dos insertos M3 por larguero a +-y; medir los agujeros del panel real |
| `boya.mastil` | 14 × 8 × 140 | B4: diametro exterior, interior, alto sobre la placa |
| `boya.mastil_placa` | 30 × 4 | Ancho en X y espesor; usa los tornillos de la tapa del extremo +X |
| `boya.mastil_desfase` | 11 | Eje del mastil a la linea de tornillos del extremo |
| `boya.flotador` | 150 × 90 × 50 | B5: largo x ancho x alto de cada modulo (4 modulos) |
| `boya.flotador_pared` | 1.6 | Pared de PETG del flotador, 4 perimetros |
| `boya.flotador_pared_interior` | 3 | Cara hacia el casco, donde nace la lengueta |
| `boya.flotador_separacion` | 26 | Pared del casco a la cara interior del flotador |
| `boya.flotador_boca` | 10 | Boca de llenado de espuma, se tapa y sella |
| `boya.espuma_densidad` | 0.03 | g/cm3, celda cerrada; sin absorcion de agua (supuesto) |
| `boya.oreja` | 22 × 12 × 7 | Oreja del casco: saliente, ancho, espesor (al fondo, sin voladizo) |
| `boya.oreja_x` | 55 | x de las 4 orejas; el flotador tiene agujeros en x = 55 y 95 (simetrico) |
| `boya.lengueta` | 19 × 70 × 5 | Lengueta del flotador: saliente, largo, espesor; apoya sobre la oreja |
| `boya.lengueta_agujeros` | 55 × 95 | x local de los 2 agujeros (el flotador es simetrico) |
| `boya.m5` | 5.4 × 8 × 4.2 | Paso, tuerca AF y bolsillo de tuerca; tornillo M5 x 25 de acero inox |
| `boya.ojal` | 24 × 12 × 6 × 32 | B6: aro exterior, aro interior, espesor, distancia del tornillo al centro del aro |
| `boya.ojal_oreja_ancho` | 24 | Ancho de la oreja de amarre del casco (extremo +X) |
| `boya.oreja_agujero_punta` | 7.5 | Del agujero M5 a la punta de oreja y lengueta |
| `boya.flotador_radio` | 8 | Radio de las aristas verticales del flotador |
| `simple.union_oreja` | 10 × 8 | Orejas de la union plana a cada lado de la camara, sobre el bolsillo del lastre: ancho en y fuera de la pared, espesor en x de cada mitad. 2 M3 por oreja (4 en total) con tuerca, a lo largo del riel |
| `aro.seccion` | 8 | Diametro de la varilla del aro Ø200 real: fija la C de M9s; medir |
| `gancho.c` | 0.4 × 4 × 12 | M9s: holgura sobre la varilla, pared de la C y largo del asiento sobre la varilla (la curva del aro Ø200 corre la varilla 0.18 mm en 12, 1.4 mm en 33) |
| `gancho.m4_x` | 15 | /x/ de los 2 M4 de la brida de M9s a tuercas en la ranura T |
| `capsula.angulo` | 30 | Inclinacion fija de las capsulas hacia abajo (version simple); se cambia reimprimiendo solo M5s |
| `capsula.pie` | 50 × 6 × 5 | Pie de M5s en silla sobre el riel: largo, espesor de la placa bajo el riel, espesor de las mejillas |
| `capsula.pie_alma` | 20 | Ancho en y del alma que une la silla con la tapa |
| `capsula.pie_m4` | 30 × 20 | 2 M4 horizontales que cruzan el riel y las mejillas: separacion en x y altura sobre el fondo del riel (sobre el Cat5e) |
| `capsula.pie_aire` | 2 | Aire entre lo mas alto de la capsula inclinada y la placa de la silla |
| `simple.bolsillo_capacidad` | 5 | Pletinas que entran en cada bolsillo bajo la caja (V2: la caja con KIT A en 2 pisos encierra mas aire) |
| `lastre.pletinas` | 5 | Pletinas por bolsillo (hay 2) en la version simple; simple.py verifica que el peso aparente quede en la ventana y dice cuantas hacen falta |
| `masa.tornilleria_simple` | 40 | 4 M3 de la union, 4 M4 + tuercas T de los ganchos, 4 M4 de los pies, 4 M3 de las tapas del bolsillo y 2 correas; pesar |
| `simple.caja_pisos` | 2 | Con KIT A en 1 piso la caja mide 159.6 x 170 con brida y la brida queda a 1.6 mm de las cuerdas a 60 grados; en 2 pisos mide 147 x 146 y deja unos 11 mm |
| `camara.fov_diagonal` | 70 | Arducam Mega 5MP: sin ficha a mano; 70 grados diagonal estimado |
| `camara.enfoque` | 80 × 1e+06 | Rango de enfoque del autofoco (mm): 8 cm a infinito, estimado; confirmar con la ficha |
| `simple.cojin_riel` | 10 × 6 × 25 | Version simple, caja baja: cojin en cada pared extrema de M1 con 4 insertos M4 (sale 10 de la pared), brida del riel de 6 y semiancho 25. El PG7 de cada camara pasa por la pared extrema y su domo entra en el conducto del riel: sin camara de cables |
| `boya.flotador_esquina` | 100 × 100 × 60 | Flotador de esquina (simple): largo x ancho x alto, hueco y sellado |
| `umbilical.diametro_manguera` | 10 | U1: manguera flexible de referencia alrededor del cable |
| `umbilical.longitud` | 3000 | Largo del umbilical comprado (igual que umbilical[1]) |
| `umbilical.radio_min` | 60 | Radio minimo de la manguera Ø10 (6 x D) |
| `separador.seccion` | 12 × 6 | Ancho x espesor del anillo o de los rayos (se imprime plano) |
| `separador.agujero` | 4.5 | Agujero por donde pasa cada cuerda (cuerda de Ø4) |
| `linterna.alto` | 200 | Alto de la red de la linterna de referencia |
| `linterna.pisos` | 3 | Pisos (bandejas) dentro de la red; solo renders y STEP |
| `linterna.cabo_largo` | 300 | Largo del cabo central que se dibuja |
| `umbilical.comba` | 80 | Cuanto cuelga el umbilical bajo la recta boya-nodo (sin tension; render) |

