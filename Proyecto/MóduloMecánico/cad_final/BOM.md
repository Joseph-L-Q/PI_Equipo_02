# BOM y bitacora del prototipo simple (generado por `bitacora.py`)

No editar a mano: `python cad_final/build.py --bitacora`. Excel con formulas: `salida/simple/BITACORA.xlsx`. Masa por pieza = la del calculo de flotacion (piel + relleno de cada pieza: 100 % cajas estancas, tapas con junta y ganchos; 40 % riel, bandejas y bisel). Parametros de costo (estimados): densidad 1.27 g/cm³, 15 g/h, 90 soles/kg. Fuente: slicer (OrcaSlicer) en el nodo.

## Resumen

| Grupo | Masa impresa g | Horas | Costo filamento S/ |
|---|---|---|---|
| nodo simple | 1358 | 47.0 | 122.26 |
| linterna de prueba | 0 | 0.0 | 0.00 |
| boya simple | 1943 | 129.5 | 174.89 |
| modular D200 | 1229 | 82.0 | 110.64 |
| nodo P2 robusto | 1400 | 46.7 | 126.02 |
| nodo P4 estetico | 1352 | 46.0 | 121.66 |
| boya PET 4 x 1 L | 863 | 32.0 | 77.69 |

El hardware no tiene precios todavia (columna amarilla de HARDWARE en el Excel).

## Piezas

| Pieza | Grupo | Cant. | X × Y × Z mm | Volumen cm³ | Orientacion | Soportes | Relleno | Masa por pieza g | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| M1s_caja_cuerpo | nodo simple | 1 | 147.0 × 146.0 × 107.0 | 383.4 | sin girar | si | 100 % | 498 | slicer |
| M2_caja_tapa | nodo simple | 1 | 63.0 × 146.0 × 147.0 | 136.0 | Y+90 | si | 100 % | 181 | slicer |
| M3s_riel_gancho | nodo simple | 2 | 141.5 × 79.4 × 50.0 | 92.3 | X+90 | si | riel 40 %, gancho 100 % | 132 | slicer |
| M3t_tapa_bolsillo | nodo simple | 2 | 117.0 × 57.0 × 3.0 | 19.9 | X180 | no | 100 % | 13 | slicer |
| M5s_capsula_tapa_pie | nodo simple | 2 | 55.2 × 64.0 × 95.9 | 74.1 | sin girar | si | 100 % | 96 | slicer |
| M11_bandeja | nodo simple | 1 | 115.0 × 114.0 × 30.0 | 39.9 | sin girar | no | 40 % | 38 | slicer |
| M11_bandeja_sup | nodo simple | 1 | 115.0 × 114.0 × 3.0 | 38.1 | sin girar | no | 40 % | 34 | slicer |
| M4_capsula_cuerpo | nodo simple | 2 | 64.0 × 64.0 × 44.0 | 46.0 | Y-90 | si | 100 % | 60 | slicer |
| M6_capsula_bisel | nodo simple | 2 | 42.0 × 42.0 × 2.5 | 1.9 | Y+90 | no | 40 % | 2 | slicer |
| B1s_casco | boya simple | 1 | 240.0 × 220.0 × 125.0 | 753.5 | X180 | si | 100 % | 957 | estimado |
| B2s_tapa | boya simple | 1 | 9.0 × 220.0 × 240.0 | 260.5 | Y+90 | si | 100 % | 331 | estimado |
| B1bs_bandeja | boya simple | 1 | 206.0 × 186.0 × 3.0 | 113.0 | sin girar | no | 40 % | 129 | estimado |
| B3s_larguero | boya simple | 2 | 24.0 × 170.0 × 21.0 | 28.4 | X180 | no | 40 % | 26 | estimado |
| B5s_flotador | boya simple | 4 | 60.0 × 100.0 × 100.0 | 91.5 | Y+90 | si | 100 % | 116 | estimado |
| B6s_ojal | boya simple | 1 | 30.0 × 24.0 × 26.0 | 8.3 | X180 | no | 100 % | 11 | estimado |
| M1_caja_cuerpo | modular D200 | 1 | 159.6 × 126.0 × 50.0 | 214.8 | sin girar | si | 100 % | 273 | estimado |
| M2_caja_tapa | modular D200 | 1 | 63.0 × 126.0 × 159.6 | 129.4 | Y+90 | si | 100 % | 164 | estimado |
| M11_bandeja | modular D200 | 1 | 127.6 × 94.0 × 18.0 | 35.6 | sin girar | no | 40 % | 41 | estimado |
| M3_riel_central | modular D200 | 1 | 69.8 × 100.0 × 140.0 | 170.1 | Y+90 | si | 100 % | 216 | estimado |
| M3_riel_ext | modular D200 | 2 | 30.0 × 30.0 × 115.0 | 44.8 | Y+90 | si | 100 % | 57 | estimado |
| M3_riel_punta | modular D200 | 2 | 30.0 × 30.0 × 60.0 | 25.3 | Y+90 | si | 40 % | 26 | estimado |
| M3_tapa_bolsillo | modular D200 | 2 | 107.0 × 35.0 × 3.0 | 9.6 | X180 | no | 40 % | 12 | estimado |
| M4_capsula_cuerpo | modular D200 | 2 | 64.0 × 64.0 × 44.0 | 46.0 | Y-90 | si | 100 % | 58 | estimado |
| M5_capsula_tapa | modular D200 | 2 | 33.0 × 64.0 × 64.0 | 23.5 | X-90 | si | 100 % | 30 | estimado |
| M6_capsula_bisel | modular D200 | 2 | 42.0 × 42.0 × 2.5 | 1.9 | Y+90 | no | 40 % | 2 | estimado |
| M9_gancho | modular D200 | 2 | 59.0 × 30.0 × 68.0 | 19.5 | Y+90 | si | 40 % | 18 | estimado |
| M10_carro_capsula | modular D200 | 2 | 80.8 × 38.6 × 85.0 | 54.5 | Y-90 | si | 40 % | 49 | estimado |
| M12_perilla | modular D200 | 4 | 30.0 × 30.0 × 12.0 | 6.7 | X180 | no | 40 % | 6 | estimado |
| M13_casquillo_D8 | modular D200 | 2 | 15.7 × 20.0 × 13.5 | 1.6 | X-90 | no | 40 % | 2 | estimado |
| M14_pestillo | modular D200 | 2 | 12.0 × 35.2 × 3.6 | 0.9 | X+90 | no | 40 % | 1 | estimado |
| M1s_caja_cuerpo | nodo P2 robusto | 1 | - | - | slicer | si | 100 % | 509 | slicer |
| M2_caja_tapa | nodo P2 robusto | 1 | - | - | slicer | si | 100 % | 181 | slicer |
| M3s_riel_gancho | nodo P2 robusto | 2 | - | - | slicer | si | 100 % | 137 | slicer |
| M3t_tapa_bolsillo | nodo P2 robusto | 2 | - | - | slicer | no | 100 % | 24 | slicer |
| M5s_capsula_tapa_pie | nodo P2 robusto | 2 | - | - | slicer | si | 100 % | 96 | slicer |
| M11_bandeja | nodo P2 robusto | 1 | - | - | slicer | no | 40 % | 38 | slicer |
| M11_bandeja_sup | nodo P2 robusto | 1 | - | - | slicer | no | 40 % | 34 | slicer |
| M4_capsula_cuerpo | nodo P2 robusto | 2 | - | - | slicer | si | 100 % | 60 | slicer |
| M6_capsula_bisel | nodo P2 robusto | 2 | - | - | slicer | no | 40 % | 2 | slicer |
| M1m_caja_riel | nodo P4 estetico | 1 | - | - | slicer | si | 100 % | 675 | slicer |
| M2_caja_tapa | nodo P4 estetico | 1 | - | - | slicer | si | 100 % | 171 | slicer |
| M3t_tapa_bolsillo | nodo P4 estetico | 2 | - | - | slicer | no | 100 % | 24 | slicer |
| M5m_extremo_pie | nodo P4 estetico | 2 | - | - | slicer | si | 100 % | 131 | slicer |
| M9c_abrazadera | nodo P4 estetico | 2 | - | - | slicer | no | 100 % | 3 | slicer |
| M11_bandeja | nodo P4 estetico | 1 | - | - | slicer | no | 40 % | 35 | slicer |
| M11_bandeja_sup | nodo P4 estetico | 1 | - | - | slicer | no | 40 % | 31 | slicer |
| M4_capsula_cuerpo | nodo P4 estetico | 2 | - | - | slicer | si | 100 % | 60 | slicer |
| M6_capsula_bisel | nodo P4 estetico | 2 | - | - | slicer | no | 40 % | 2 | slicer |
| B1_casco | boya PET 4 x 1 L | 1 | - | - | slicer | si | 40 % | 214 | slicer |
| B2_cubierta | boya PET 4 x 1 L | 1 | - | - | slicer | no | 40 % | 119 | slicer |
| B3_caja | boya PET 4 x 1 L | 1 | - | - | slicer | no | 40 % | 171 | slicer |
| B4_tapa | boya PET 4 x 1 L | 1 | - | - | slicer | no | 40 % | 57 | slicer |
| B5_cuna | boya PET 4 x 1 L | 2 | - | - | slicer | si | 40 % | 141 | slicer |
| B6_correa | boya PET 4 x 1 L | 4 | - | - | slicer | no | 40 % | 5 | slicer |

## Hardware

| Grupo | Item | Medida | Cantidad |
|---|---|---|---|
| nodo simple | Tornillo M3 x 12 + inserto termico M3 (tapa de la caja) | M3 | 12 |
| nodo simple | Tornillo M3 x 8 + inserto termico M3 (bandejas) | M3 | 4 |
| nodo simple | Tornillo M3 x 16 + tuerca (capsulas) | M3 | 8 |
| nodo simple | Tornillo M2 autorroscante (bisel) | M2 x 6 | 6 |
| nodo simple | Cordon de junta torica Ø2 (caja + 2 capsulas, +10 %) | 970 mm | 1 |
| nodo simple | Prensaestopas PG7 con contratuerca (3 caja + 2 capsulas) | PG7 | 5 |
| nodo simple | Disco de acrilico de la ventana | Ø30 x 3 | 2 |
| nodo simple | Grillete o argolla de inox (izado) | M6 | 1 |
| nodo simple | Tornillo M4 x 20 + inserto termico M4 (bridas del riel a la caja) | M4 | 8 |
| nodo simple | Tornillo M3 x 8 avellanado + inserto M3 (tapas del bolsillo) | M3 | 4 |
| nodo simple | Tornillo M4 x 45 + tuerca (pie de las capsulas) | M4 | 4 |
| nodo simple | Correa textil | 25 x 300 mm | 2 |
| nodo simple | Lastre a granel: tuercas y arandelas M8 de inox | 1140 g | 1 |
| boya simple | Tornillo M3 x 12 + inserto M3 (tapa de la boya) | M3 | 16 |
| boya simple | Tornillo M3 + inserto M3 (portabaterias y bandeja) | M3 | 8 |
| boya simple | Tornillo M3 x 30 + inserto M3 (largueros a la tapa) | M3 | 4 |
| boya simple | Tornillo M3 + inserto M3 (panel a los largueros) | M3 | 4 |
| boya simple | Perno M5 x 120 inox + inserto M5 (flotadores) | M5 | 8 |
| boya simple | Tornillo M5 + inserto M5 (ojal de amarre) | M5 | 1 |
| boya simple | Cordon de junta torica Ø2 (tapa de la boya, +10 %) | 900 mm | 1 |
| boya simple | Prensaestopas PG7 (umbilical y panel) | PG7 | 2 |
| boya simple | Tapon de la boca de llenado de los flotadores (o sello con PETG) | Ø10 | 4 |
| boya simple | Manguera flexible U1 de referencia | Ø10 | 1 |
| boya simple | Cabo de amarre C1 boya-linterna | Ø4 | 1 |
| modular D200 | Tornillo M3 x 12 + inserto termico M3 (tapa de la caja) | M3 | 12 |
| modular D200 | Tornillo M3 x 8 + inserto termico M3 (bandejas) | M3 | 4 |
| modular D200 | Tornillo M3 x 16 + tuerca (capsulas) | M3 | 8 |
| modular D200 | Tornillo M2 autorroscante (bisel) | M2 x 6 | 6 |
| modular D200 | Cordon de junta torica Ø2 (caja + 2 capsulas, +10 %) | 970 mm | 1 |
| modular D200 | Prensaestopas PG7 con contratuerca (3 caja + 2 capsulas) | PG7 | 5 |
| modular D200 | Disco de acrilico de la ventana | Ø30 x 3 | 2 |
| modular D200 | Grillete o argolla de inox (izado) | M6 | 1 |
| modular D200 | Tornillo M4 x 12 + inserto termico M4 (riel a la caja) | M4 | 4 |
| modular D200 | Varilla roscada M8 (8.8) | 451 mm | 1 |
| modular D200 | Tuerca M8 | M8 | 2 |
| modular D200 | Arandela ancha DIN 9021 | M8 | 2 |
| modular D200 | Tornillo M4 x 14 + tuerca (uniones de tramos) | M4 | 8 |
| modular D200 | Tornillo M3 x 8 avellanado + inserto M3 (tapa del bolsillo) | M3 | 4 |
| modular D200 | Perno M4 hexagonal (perillas) + tuerca en la ranura T | M4 | 4 |
| modular D200 | Perno M4 x 20 + tuerca mariposa (bisagras) | M4 | 2 |
| modular D200 | Pivote M3 del pestillo | M3 | 2 |
| modular D200 | Correa textil | 25 x 300 mm | 2 |
| modular D200 | Pletina de inox | 25 x 5 x 100 | 4 |

## Diseño

| Concepto | Valor | Unidad | De donde sale |
|---|---|---|---|
| Riel: largo / seccion x pared | 430 / 30 x 4 | mm | params.py simple.riel_L, riel.* |
| Caja: ESP32 y pisos | kit_a, 2 pisos | - | params.py simple.esp32_base (equipo), simple.caja_pisos |
| Caja: exterior (sin brida) | 127.0 x 126.0 x 77.0 | mm | layout.py (derivado de la electronica) |
| Caja: con brida | 147.0 x 146.0 | mm | layout.py + caja.brida_ancho |
| Caja: interior (cavidad) | 119.0 x 118.0 x 73.0 | mm | layout.py |
| Caja: pared / fondo | 4 / 4 | mm | params.py caja.pared, caja.fondo |
| Nodo sobre el aro (de / a) | -40 / 181 | mm | simple.py, nube de puntos del CAD |
| Capsula: exterior | 44.0 x 46.0 x 46.0 | mm | capsula.py cap_dims |
| Capsula: angulo y acimut | 30 grados, adentro | - | params.py capsula.angulo, capsula.acimut (equipo) |
| Ventana: diametro x espesor | 30 x 3 | mm | params.py ventana.* |
| Gancho en C (fusionado al riel): C interior / pared / asiento | 8.8 / 6 / 12 | mm | params.py aro.seccion, gancho.c |
| Separador LR1 | no se usa | - | params.py separador.usar (tanda 3: sin separador) |
| Lastre a granel (un bolsillo por lado) | 1140 g de tuercas y arandelas M8 de inox, a granel, bolsillo 100 x 50 x 30 | mm | params.py lastre.granel, simple.py |
| Nodo: peso en aire (bandeja 40 % / 100 %) | 2680 / 2689 | g | simple.py, masas por pieza con su relleno |
| Nodo: peso aparente (40 % / 100 %) | +350 / +359 | g | simple.py (ventana +200 a +500) |
| Nodo: BG | 20.1 | mm | simple.py |
| Punto de amarre de las cuerdas sobre el aro | 400 | mm | linterna.nudo_h |
| Aire minimo suspension-nodo | 48.0 | mm | simple.py (exigido 10) |
| FS riel (capas / entre capas) | 17.8 / 8.7 | - | simple.py §5, a mano |
| FS pie de capsula (capas / entre capas) | 4.5 / 2.2 | - | simple.py §5, a mano |
| FS gancho (capas / entre capas) | 5.8 / 2.9 | - | simple.py §5, a mano |
| Traccion por inserto M4 de las bridas al izar | 339 | N | simple.py §5 (probar con PB8) |
| Cable por camara | 379 | mm | simple.py §6 (> 300: prueba SPI) |
| Boya: masa / calado / francobordo | 2705 / 31.6 / 88.4 | g / mm / mm | boya_simple.py (agua de mar 1025) |
| Boya: reserva / GM balanceo y cabeceo | 194 % / 92 y 467 | - / mm | boya_simple.py |
| Nodo + boya en aire (limite 3000) | 5168 | g | simple.py + boya_simple.py |
| Camara en Ø200: lente a la red | 38 | mm | simple.py camera_view (FOV y enfoque estimados) |
| Camara en Ø500: lente a la red | no corta la red | mm | simple.py camera_view (FOV y enfoque estimados) |
| FEM riel_agua: desplazamiento max / tension max / FS | 2.51 / 8.4 / 5.4 | mm / MPa / - | fem |
| FEM riel_izado: desplazamiento max / tension max / FS | 0.25 / 4.1 / 10.9 | mm / MPa / - | fem |
| FEM pie: desplazamiento max / tension max / FS | 0.48 / 8.9 / 5.0 | mm / MPa / - | fem |
