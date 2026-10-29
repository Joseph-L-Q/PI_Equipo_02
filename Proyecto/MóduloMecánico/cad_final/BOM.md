# BOM y bitacora del prototipo simple (generado por `bitacora.py`)

No editar a mano: `python cad_final/build.py --bitacora`. Excel con formulas: `salida/simple/BITACORA.xlsx`. Parametros de costo (estimados, `params.py`): densidad 1.27 g/cm³, factor de relleno 0.45, 15 g/h, 90 soles/kg. Fuente de masa y horas: estimado (sin slicer todavia).

## Resumen

| Grupo | Masa impresa g | Horas | Costo filamento S/ |
|---|---|---|---|
| nodo simple | 584 | 38.9 | 52.58 |
| linterna de prueba | 26 | 1.7 | 2.31 |
| boya | 533 | 35.5 | 47.98 |
| modular D200 | 590 | 39.3 | 53.07 |

El hardware no tiene precios todavia (columna amarilla de HARDWARE en el Excel).

## Piezas

| Pieza | Grupo | Cant. | X × Y × Z mm | Volumen cm³ | Orientacion | Soportes | Masa por pieza g | Fuente |
|---|---|---|---|---|---|---|---|---|
| M1_caja_cuerpo | nodo simple | 1 | 159.6 × 126.0 × 50.0 | 214.8 | sin girar | si | 123 | estimado |
| M2_caja_tapa | nodo simple | 1 | 63.0 × 126.0 × 159.6 | 129.4 | Y+90 | si | 74 | estimado |
| M11_bandeja | nodo simple | 1 | 127.6 × 94.0 × 18.0 | 35.6 | sin girar | no | 20 | estimado |
| M3s_riel_mitad | nodo simple | 2 | 215.0 × 100.0 × 57.3 | 148.5 | X180 | si | 85 | estimado |
| M3t_tapa_bolsillo | nodo simple | 2 | 107.0 × 35.0 × 3.0 | 9.6 | X180 | no | 5 | estimado |
| M5s_capsula_tapa_pie | nodo simple | 2 | 96.8 × 64.0 × 95.9 | 94.3 | X180 | si | 54 | estimado |
| M9s_gancho | nodo simple | 2 | 50.0 × 47.2 × 33.0 | 21.0 | X+90 | no | 12 | estimado |
| M4_capsula_cuerpo | nodo simple | 2 | 64.0 × 64.0 × 44.0 | 46.0 | Y-90 | si | 26 | estimado |
| M6_capsula_bisel | nodo simple | 2 | 42.0 × 42.0 × 2.5 | 1.9 | Y+90 | no | 1 | estimado |
| LR1_separador | linterna de prueba | 1 | 211.9 × 211.9 × 6.0 | 44.9 | sin girar | no | 26 | estimado |
| B1_casco_central | boya | 1 | 209.0 × 141.0 × 76.0 | 312.7 | sin girar | si | 179 | estimado |
| B1b_bandeja | boya | 1 | 124.0 × 85.0 × 3.0 | 31.5 | sin girar | no | 18 | estimado |
| B2_tapa | boya | 1 | 197.0 × 117.0 × 5.0 | 112.5 | X180 | no | 64 | estimado |
| B3_larguero_panel | boya | 2 | 24.0 × 140.0 × 33.0 | 33.6 | X180 | no | 19 | estimado |
| B4_mastil_antena | boya | 1 | 30.0 × 123.0 × 144.0 | 29.1 | sin girar | no | 17 | estimado |
| B5_flotador | boya | 4 | 150.0 × 109.0 × 48.4 | 72.1 | sin girar | si | 41 | estimado |
| B5b_tapa_flotador | boya | 4 | 150.0 × 90.0 × 1.6 | 21.4 | sin girar | no | 12 | estimado |
| B6_ojal_amarre | boya | 1 | 50.0 × 24.0 × 6.0 | 5.8 | sin girar | no | 3 | estimado |
| M1_caja_cuerpo | modular D200 | 1 | 159.6 × 126.0 × 50.0 | 214.8 | sin girar | si | 123 | estimado |
| M2_caja_tapa | modular D200 | 1 | 63.0 × 126.0 × 159.6 | 129.4 | Y+90 | si | 74 | estimado |
| M11_bandeja | modular D200 | 1 | 127.6 × 94.0 × 18.0 | 35.6 | sin girar | no | 20 | estimado |
| M3_riel_central | modular D200 | 1 | 69.8 × 100.0 × 140.0 | 170.1 | Y+90 | si | 97 | estimado |
| M3_riel_ext | modular D200 | 2 | 30.0 × 30.0 × 115.0 | 44.8 | Y+90 | si | 26 | estimado |
| M3_riel_punta | modular D200 | 2 | 30.0 × 30.0 × 60.0 | 25.3 | Y+90 | si | 14 | estimado |
| M3_tapa_bolsillo | modular D200 | 2 | 107.0 × 35.0 × 3.0 | 9.6 | X180 | no | 5 | estimado |
| M4_capsula_cuerpo | modular D200 | 2 | 64.0 × 64.0 × 44.0 | 46.0 | Y-90 | si | 26 | estimado |
| M5_capsula_tapa | modular D200 | 2 | 33.0 × 64.0 × 64.0 | 23.5 | X-90 | si | 13 | estimado |
| M6_capsula_bisel | modular D200 | 2 | 42.0 × 42.0 × 2.5 | 1.9 | Y+90 | no | 1 | estimado |
| M9_gancho | modular D200 | 2 | 59.0 × 30.0 × 68.0 | 19.5 | Y+90 | si | 11 | estimado |
| M10_carro_capsula | modular D200 | 2 | 80.8 × 38.6 × 85.0 | 54.5 | Y-90 | si | 31 | estimado |
| M12_perilla | modular D200 | 4 | 30.0 × 30.0 × 12.0 | 6.7 | X180 | no | 4 | estimado |
| M13_casquillo_D8 | modular D200 | 2 | 15.7 × 20.0 × 13.5 | 1.6 | X-90 | no | 1 | estimado |
| M14_pestillo | modular D200 | 2 | 12.0 × 35.2 × 3.6 | 0.9 | X+90 | no | 1 | estimado |

## Hardware

| Grupo | Item | Medida | Cantidad |
|---|---|---|---|
| nodo simple | Tornillo M3 x 12 + inserto termico M3 (tapa de la caja) | M3 | 10 |
| nodo simple | Tornillo M3 x 8 + inserto termico M3 (bandeja) | M3 | 4 |
| nodo simple | Tornillo M3 x 16 + tuerca (capsulas) | M3 | 8 |
| nodo simple | Tornillo M4 x 12 + inserto termico M4 (riel a la caja) | M4 | 4 |
| nodo simple | Tornillo M2 autorroscante (bisel) | M2 x 6 | 6 |
| nodo simple | Cordon de junta torica Ø2 (caja + 2 capsulas, +10 %) | 950 mm | 1 |
| nodo simple | Prensaestopas PG7 con contratuerca (3 caja + 2 capsulas) | PG7 | 5 |
| nodo simple | Disco de acrilico de la ventana | Ø30 x 3 | 2 |
| nodo simple | Grillete o argolla de inox (izado) | M6 | 1 |
| nodo simple | Tornillo M3 x 20 + tuerca (union del riel) | M3 | 4 |
| nodo simple | Tornillo M3 x 8 avellanado + inserto M3 (tapa del bolsillo) | M3 | 4 |
| nodo simple | Tornillo M4 x 12 + tuerca M4 en la ranura T (ganchos) | M4 | 4 |
| nodo simple | Tornillo M4 x 45 + tuerca (pie de las capsulas) | M4 | 4 |
| nodo simple | Correa textil | 25 x 300 mm | 2 |
| nodo simple | Pletina de inox | 25 x 5 x 100 | 6 |
| modular D200 | Tornillo M3 x 12 + inserto termico M3 (tapa de la caja) | M3 | 10 |
| modular D200 | Tornillo M3 x 8 + inserto termico M3 (bandeja) | M3 | 4 |
| modular D200 | Tornillo M3 x 16 + tuerca (capsulas) | M3 | 8 |
| modular D200 | Tornillo M4 x 12 + inserto termico M4 (riel a la caja) | M4 | 4 |
| modular D200 | Tornillo M2 autorroscante (bisel) | M2 x 6 | 6 |
| modular D200 | Cordon de junta torica Ø2 (caja + 2 capsulas, +10 %) | 950 mm | 1 |
| modular D200 | Prensaestopas PG7 con contratuerca (3 caja + 2 capsulas) | PG7 | 5 |
| modular D200 | Disco de acrilico de la ventana | Ø30 x 3 | 2 |
| modular D200 | Grillete o argolla de inox (izado) | M6 | 1 |
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

## Diseño (salidas de `simple.py`)

| Concepto | Valor | Unidad | De donde sale |
|---|---|---|---|
| Riel: largo | 430.0 | mm | params.py simple.riel_L |
| Riel: seccion x pared | 30 x 4 | mm | params.py riel.seccion, riel.pared |
| Caja: exterior (sin brida) | 139.6 x 106.0 x 50.0 | mm | layout.py (derivado de la electronica) |
| Caja: con brida | 159.6 x 126.0 | mm | layout.py + caja.brida_ancho |
| Caja: interior (cavidad) | 131.6 x 98.0 x 46.0 | mm | layout.py |
| Caja: pared / fondo | 4 / 4 | mm | params.py caja.pared, caja.fondo |
| Capsula: exterior (largo x ancho x alto) | 44.0 x 46.0 x 46.0 | mm | capsula.py cap_dims |
| Capsula: cavidad | 38.0 x 38.0 x 38.0 | mm | capsula.py (camara + holguras) |
| Capsula: angulo fijo | 30.0 | grados | params.py capsula.angulo |
| Ventana: diametro x espesor | 30 x 3 | mm | params.py ventana.* |
| Gancho: C interior / pared / asiento | 8.8 / 4 / 12 | mm | params.py aro.seccion, gancho.c |
| Gancho: fondo del riel al centro de la varilla | 40.0 | mm | params.py gancho.caida |
| Separador LR1: tipo, seccion | aro, 12 x 6 | mm | params.py separador.* |
| Separador: altura (minima calculada) | 250 (165) | mm | simple.py min_separator_h |
| Pletinas de lastre | 3 x 2 de 25 x 5 x 100 | mm | params.py lastre.pletinas |
| Peso en aire (bandeja 40 % / 100 %) | 2079 / 2083 | g | simple.py, volumenes del CAD |
| Peso aparente en el agua (40 % / 100 %) | +265 / +269 | g | simple.py (ventana +200 a +500) |
| Estabilidad BG | 17.4 | mm | simple.py centros de masa y empuje |
| Apice sobre el aro | 400 | mm | separador.altura + apice.altura |
| Aire minimo suspension-nodo | 21.6 | mm | simple.py, nube de puntos del CAD (exigido 10) |
| FS del riel (a lo largo / entre capas) | 6.9 / 3.4 | - | simple.py §5 |
| FS del pie de capsula (a lo largo / entre capas) | 2.5 / 1.2 | - | simple.py §5 (punto debil) |
| Traccion por inserto M4 al izar | 254 | N | simple.py §5 |
| Cable por camara | 420 | mm | simple.py §6 (> 300: prueba SPI) |
