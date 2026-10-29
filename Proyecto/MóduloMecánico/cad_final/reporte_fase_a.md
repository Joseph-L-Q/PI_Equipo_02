# Reporte Fase A, layout de la caja central (generado por `fase_a.py`)

No editar a mano: se regenera. mm, cm³, g. Todo valor `estimado` sigue por verificar.

## 1. Parámetros (`cad_final/params.py`)

| Parámetro | Anterior | Nuevo | Razón | Origen | Estado |
|---|---|---|---|---|---|
| `impresora.cama` | 220 × 220 × 250 | 220 × 220 × 250 | Impresora real desconocida | estimado | por_verificar |
| `pieza.largo_max` | nuevo | 150 | Prompt v2: ninguna pieza > 150 salvo la caja | equipo | confirmado |
| `impresion.espesor_min` | 1.2 | 1.2 | 3 perimetros de 0.4 | equipo | confirmado |
| `impresion.cascara` | nuevo | 1.2 | Perimetros + capas sup/inf macizos, para la masa con relleno | estimado | por_verificar |
| `impresion.relleno` | nuevo | 0.4 × 1 | Prompt v2 Fase E: 40 % y 100 % | equipo | confirmado |
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
| `riel.ventana_cable` | nuevo | 24 × 14 | Ventana en la cara superior del tramo central, bajo cada PG7 del fondo | estimado | por_verificar |
| `gancho.contacto` | nuevo | 12 | Asiento de 12 con bordes R3 | equipo | confirmado |
| `gancho.radio_borde` | nuevo | 3 |  | equipo | confirmado |
| `gancho.carga_N` | nuevo | 75 | 150 N repartidos en 2 ganchos | equipo | confirmado |
| `perilla.diametro` | nuevo | 30 | M12_perilla, para guante | equipo | confirmado |
| `casquillo.D` | nuevo | 6 × 8 × 10 × 12 | M13_casquillo_D6...D12 | equipo | confirmado |
| `pestillo.resalte` | nuevo | 0.6 | Traba del M14; probar en probeta | equipo | por_verificar |
| `correa.ancho` | 26 | 25 | Correa textil de seguridad | equipo | confirmado |
| `carro.recorrido` | nuevo | 50 | M10_carro_capsula, +-50 | equipo | confirmado |
| `carga.manipulacion_N` | nuevo | 150 | Caso de diseno a 1 m | equipo | confirmado |
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
| `caja.base_m4` | nuevo | 51.5 × 6; 51.5 × -6; -51.5 × 6; -51.5 × -6 | 4 M4 desde el riel a insertos ciegos en el fondo (no perforan el sello); |x| < 55 para no caer en la cola de milano del tramo central | estimado | por_verificar |
| `caja.base_m4_boss` | nuevo | 10 × 6 | Ø x alto del refuerzo interior del inserto M4 | estimado | por_verificar |
| `asa.alto` | 42 | 42 | Asa con ojal para el cabo | equipo | confirmado |
| `asa.agarre` | 90 | 90 | Ancho de mano con guante | estimado | por_verificar |
| `pg7.agujero` | 12.6 | 12.6 | Rosca PG7 12.5 | estimado | por_verificar |
| `pg7.contratuerca_AF` | 15 | 15 | Comprar y medir | estimado | por_verificar |
| `pg7.alto_interior` | nuevo | 9 | Rosca que asoma + contratuerca por dentro | estimado | por_verificar |
| `caja.pg7_fondo` | 2 | 2 | 2 x PG7 en el fondo hacia el riel (camaras) | equipo | confirmado |
| `caja.pg7_umbilical` | PG9 en la tapa | tapa | En la tapa, sobre la zona libre central; el umbilical sube a la boya | estimado | por_verificar |
| `caja.pg7_umbilical_xy` | 0 × 18 | -20 × 16 | Fuera del asa (y = +-6) y de la zona de cables del MPU-6050 | estimado | por_verificar |
| `holgura.pines` | nuevo | 15 | Dupont + curva del cable sobre los pines | equipo | confirmado |
| `holgura.conector` | nuevo | 10 | Lateral en el lado de cada conector | equipo | confirmado |
| `holgura.contratuerca` | 20 | 20 | Libre alrededor de cada contratuerca PG7, medido desde sus esquinas (lectura literal) | equipo | confirmado |
| `holgura.usb` | nuevo | 35 | Enchufe USB-C con su moldeado + curva, sin sacar la bandeja | estimado | por_verificar |
| `holgura.microsd` | nuevo | 15 | Dedo para sacar la tarjeta | estimado | por_verificar |
| `holgura.entre_modulos` | nuevo | 2 | Cuerpo a cuerpo o cuerpo a zona de acceso | estimado | por_verificar |
| `holgura.pared` | 1 | 2 | Cuerpo o bandeja a la pared interior | estimado | por_verificar |
| `bandeja.espesor` | nuevo | 3 |  | estimado | por_verificar |
| `bandeja.apoyo` | nuevo | 8 | Por encima de los refuerzos M4 (6) del fondo | estimado | por_verificar |
| `bandeja.partir` | nuevo | True | La bandeja entera pasa de 150: se parte en der/izq; False = una sola pieza | estimado | por_verificar |
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

## 2. Caja resultante (derivada del layout)

| Concepto | sin_base (por defecto) | kit_a (alternativa) |
|---|---|---|
| Cavidad | 184.6 × 108 × 46 | 258.6 × 119 × 43 |
| Exterior del cuerpo | 192.6 × 116 × 50 | 266.6 × 127 × 47 |
| Con brida y tapa (lo que va a la cama) | 212.6 × 136 × 55 | 286.6 × 147 × 52 |
| Cabe en cama 220 × 220 × 250 | sí | NO |
| Bandejas | M11_bandeja_izq: 89.3 × 104, M11_bandeja_der: 89.3 × 104 | M11_bandeja_izq: 126.3 × 115, M11_bandeja_der: 126.3 × 115 |
| Bandejas ≤ 150 | sí | sí |
| Choques de cuerpos con zonas | 0 | 0 |

Prensaestopas del fondo en x = ±18.66, y = 0 (ventanas del tramo central). Zona libre de cada contratuerca: radio 28.66 (esquina 8.66 + 20). Umbilical en la tapa en -20 × 16.

| Módulo | Cuerpo x0, x1, y0, y1, z0, z1 | Bandeja |
|---|---|---|
| HW-517 #1 | -36.0, -2.0, 30.7, 47.7, 15.0, 27.0 | M11_bandeja_izq |
| MPU-6050 | 8.0, 29.0, 30.7, 46.7, 15.0, 27.0 | M11_bandeja_der |
| HW-517 #2 | 2.0, 36.0, -47.7, -30.7, 15.0, 27.0 | M11_bandeja_der |
| ESP32-S3 DevKitC-1 | 49.3, 75.3, -52.0, 17.0, 30.0, 45.0 | M11_bandeja_der |
| microSD SPI | -73.3, -49.3, -23.5, 18.5, 15.0, 27.0 | M11_bandeja_izq |
| XY-017 RS-485 | -90.3, -75.3, -22.5, 22.5, 15.0, 27.0 | M11_bandeja_izq |

## 3. Chequeos

| Pieza | BRepCheck | BOPAlgo | Sólidos | Arista mín | Cara mín | Resultado |
|---|---|---|---|---|---|---|
| M1_caja_cuerpo (preliminar) | ok | ok | 1 | 4.00 | 5.37 | ok |
| M2_caja_tapa (preliminar) | ok | ok | 1 | 1.50 | 8.25 | ok |
| M11_bandeja_izq | ok | ok | 1 | 3.00 | 9.42 | ok |
| M11_bandeja_der | ok | ok | 1 | 3.00 | 9.42 | ok |

| Par | Interferencia con M1 mm³ | con la bandeja mm³ |
|---|---|---|
| HW-517 #1 | 0.00 | 0.00 |
| MPU-6050 | 0.00 | 0.00 |
| HW-517 #2 | 0.00 | 0.00 |
| ESP32-S3 DevKitC-1 | 0.00 | 0.00 |
| microSD SPI | 0.00 | 0.00 |
| XY-017 RS-485 | 0.00 | 0.00 |
| M11_bandeja_izq ↔ M1 | 0.00 |  |
| M11_bandeja_der ↔ M1 | 0.00 |  |

## 4. Aire sellado, empuje y lastre

| Concepto | Valor |
|---|---|
| Volumen cerrado del cuerpo (PETG + cavidad; los bolsillos se inundan) | 1227 cm³ |
| Tapa M2 | 173 cm³ |
| Volumen desplazado por la caja | 1400 cm³ → empuje 1435 g |
| Aire sellado (cavidad − bandeja − módulos − contratuercas) | 797 cm³ |
| Electrónica + 3 PG7 + tornillería + cables (estimado) | 94 g |
| Capacidad de los 2 bolsillos | 207 cm³ → 817 g en tuercas, 1470 g en barra |
| Acero: hunde 0.870 g por g | |

| Relleno | PETG caja (M1+M2+M11) g | Caja en aire g | Peso aparente de la caja g (+ hunde) |
|---|---|---|---|
| 40 % | 500 | 594 | -841 |
| 100 % | 676 | 770 | -665 |

**Nodo completo, PRELIMINAR** (riel por sección, cápsulas P4 rev. B viejas, 200 g de ganchos/carros/perillas sin modelar). Lastre de acero para quedar en 0.2 a 0.5 kgf hacia abajo:

| Relleno | Aro | Ext/lado | Riel (tramos) mm | Nodo en aire g | Desplaza cm³ | Peso aparente g | Lastre g | Total en aire g |
|---|---|---|---|---|---|---|---|---|
| 40 % | Ø100 | 0 | 140 | 1071 | 1924 | -901 | 1266 a 1610 | 2336 a 2681 |
| 40 % | Ø200 | 1 | 340 | 1148 | 2007 | -909 | 1275 a 1620 | 2423 a 2767 |
| 40 % | Ø300 | 1 | 340 | 1148 | 2007 | -909 | 1275 a 1620 | 2423 a 2767 |
| 40 % | Ø500 | 2 | 540 | 1225 | 2090 | -917 | 1284 a 1629 | 2509 a 2854 |
| 100 % | Ø100 | 0 | 140 | 1322 | 1924 | -650 | 976 a 1321 | 2299 a 2643 |
| 100 % | Ø200 | 1 | 340 | 1428 | 2007 | -629 | 953 a 1298 | 2381 a 2726 |
| 100 % | Ø300 | 1 | 340 | 1428 | 2007 | -629 | 953 a 1298 | 2381 a 2726 |
| 100 % | Ø500 | 2 | 540 | 1534 | 2090 | -609 | 930 a 1274 | 2463 a 2808 |

Estabilidad de la caja (aproximada, 100 % relleno, lastre 930 g en los bolsillos): centro de masa z = 8.2, centro de empuje z = 25.5 → el centro de masa queda debajo: no se voltea. El cálculo completo con riel y cápsulas es la Fase E.
