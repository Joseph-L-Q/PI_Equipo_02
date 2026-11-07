# Imprimir hoy: nodo simple V2 (aro Ø200)

Rama `cad/version-final`, generado el 30/10/2026 desde `salida/simple/stl/` y `salida/probetas/`. Impresora **Bambu Lab
P1P, boquilla 0.4, placa PEI texturizada**, filamento **PETG** (Bambu PETG Basic), proceso **0.20 mm Standard**. Todas
las piezas: 3 paredes, relleno giroide con el porcentaje de la tabla.

**Los STL de esta carpeta ya vienen girados a su orientación de impresión y apoyados en la cama.** En Orca: importar,
**no rotar**, *Arrange* y cortar. La columna "Orientación" dice cómo quedan respecto del modelo (`X180` = dada vuelta,
`Y±90` / `X+90` = de costado, `sin girar` = como en el CAD). El número del archivo es el orden y `_xN` es la cantidad.

Gramos y horas: OrcaSlicer nightly 2.5.0-dev por CLI con los perfiles de `cad_final/orca/`, **una pieza por placa**.
Cada placa suma ~6 min de rutina de arranque de la P1P: si se juntan varias piezas en una placa, el total baja.

## (a) Listo para imprimir ya

No dependen de medidas pendientes. **Excepción para las piezas largas:** las probetas 01 a 05 calibran la holgura, el
agujero del inserto y la junta, que usan M1, M2 y M4. Por eso van primero. Si PB7 o PB8 piden otro valor, se cambia
en `params.py`, se corre `--rapido` (1.5 min) y se reexporta **antes** de mandar M1 (16.8 h).

| # | STL | Cant. | Orientación | Soportes | Relleno | g c/u | h c/u | Para qué / ojo |
|---|---|---|---|---|---|---|---|---|
| 01 | `01_PB7_peine_holguras_x1.stl` | 1 | plano | no | 40 % | 8.4 | 0.46 | **La primera.** Pines en los 4 agujeros (0.2, 0.3, 0.4, 0.5 de izquierda a derecha): fija `impresion.holgura` (0.3) y `impresion.comp_agujero` (0.2) |
| 02 | `02_PB7_pines_x1.stl` | 1 | plano | no | 40 % | 1.8 | 0.27 | Los pines del peine. Cortar del sprue |
| 03 | `03_PB8_inserto_M4_x3.stl` | 3 | plano, cara de afuera en la cama | no | 100 %, **5 paredes** | 7.7 | 0.42 | Arranque del inserto M4 con dinamómetro. Las bridas del riel piden 339 N por inserto al izar (REPORTE_CAD §10.6) |
| 04 | `04_PB6_junta_base_x1.stl` | 1 | plano | no | 100 % | 37.3 | 0.97 | Insertos M3 + junta Ø2. Prueba de estanqueidad con la tapa 05 |
| 05 | `05_PB6_junta_tapa_x1.stl` | 1 | plano | no (el CAD mide 511 mm² de voladizo: revisar la vista previa) | 100 % | 20.2 | 0.56 | Compresión de la junta en la ranura 2.6 × 1.5. Sumergir |
| 06 | `06_M6_bisel_x2.stl` | 2 | Y+90 (queda plano) | no | 40 % | 2.0 | 0.20 | Bisel de la ventana |
| 07 | `07_M11_bandeja_x1.stl` | 1 | sin girar | no | 40 % | 38.3 | 1.73 | Bandeja inferior del KIT A |
| 08 | `08_M11_bandeja_sup_x1.stl` | 1 | sin girar | no | 40 % | 34.1 | 1.13 | Bandeja superior (2.º piso) |
| 09 | `09_M3t_tapa_bolsillo_x2.stl` | 2 | X180 | no | 100 % | 13.3 | 0.38 | Tapas de los bolsillos del lastre |
| 10 | `10_M4_capsula_cuerpo_x2.stl` | 2 | Y-90 (de costado) | sí | 100 % | 59.6 | 2.05 | Cuerpo de la cápsula de cámara |
| 11 | `11_M2_caja_tapa_x1.stl` | 1 | Y+90 (de canto, 147 de alto) | sí | 100 % | 181.2 | 5.11 | Tapa de la caja con el asa |
| 12 | `12_M1_caja_cuerpo_x1.stl` | 1 | X180 (dada vuelta) | sí (15 793 mm² de voladizo) | 100 % | 498.1 | 16.80 | Caja baja con bolsillos. La pieza más larga: mandarla cuando 01 a 05 estén aprobadas |
| 13 | `13_M5s_capsula_tapa_pie_x2.stl` | 2 | sin girar | sí | 100 % | 96.2 | 3.19 | **Condicional:** trae fijo el ángulo de la cámara (`capsula.angulo` = 30°). REPORTE_CAD §10.3 deja abierto pasar a 70° (en Ø200 la red queda a 38 mm del lente). Imprimir solo si el equipo confirma 30° |

**Total (a): 1185 g, 39.9 h** (con las cantidades; 13 placas sueltas). Sin M5s: 992 g, 33.5 h.
No se imprime: **M7 ventana**, acrílico de 3 mm comprado y cortado (2 discos Ø30).

**Probetas que no van hoy** (están en `salida/probetas/`; misma configuración, una por placa): PB1_garra (9.2 g, 0.49 h),
M13_casquillo_D6/D8/D10/D12 (1.0 a 2.0 g, 0.35 h c/u), M14_pestillo (1.0 g, 0.18 h), M12_perilla (5.3 g, 0.39 h),
PB2_ranura_T (19.9 g, 0.77 h), PB3_macho y PB3_hembra (18.4 y 16.8 g, 0.79 h c/u). Son del riel modular (garra con
casquillo, pestillo, perilla, ranura T y unión de tramos), que la versión simple no usa. Si el equipo quiere probar el
ajuste del gancho sobre la varilla real, eso va con el grupo (b).

## (b) Espera medida: `aro.seccion`

Hoy `aro.seccion` = 8 mm, estimado. Hay que medir con calibrador la varilla del aro Ø200 real (MEDIDAS.md, fila 1),
ponerla en `params.py`, correr `--rapido` y recién entonces exportar estas piezas.

| STL (en `salida/simple/stl/` o `salida/linterna_prueba/`) | Cant. | Orientación | Soportes | Relleno | g c/u | h c/u | Depende de |
|---|---|---|---|---|---|---|---|
| `M3s_riel_gancho.stl` | 2 | X+90 (de costado) | sí | riel 40 %, gancho 100 % (*) | 132.2 | 5.29 | la C del gancho fusionado abraza la varilla |
| `LR1_separador.stl` | 1 | sin girar (plano) | no | 40 % | 37.0 | 1.56 | separador de la linterna de prueba |

Total (b): 301 g, 12.1 h. (*) El slicer lo cortó todo al 100 % para quedar del lado seguro. Al imprimirlo, poner en
Orca un modificador de 40 % en el tramo del riel: así pesa y tarda menos que lo que dice la tabla.

## (c) No imprimir aún: boya simple

Falta la decisión de peso y flotación. Nodo + boya = **5168 g contra la exigencia de 3 kg** (REPORTE_CAD §10.4). Si la
decisión es bajar el casco y la tapa a 40 % o cambiar los flotadores, cambian las piezas. La tabla trae los gramos de
la bitácora (volumen × densidad) y las horas a 15 g/h, el valor por defecto de la bitácora. Los dos son
**estimados** y las horas quedan altas: en el nodo, el slicer dio unos 29 g/h. La única corrida de slicer de la boya
(REPORTE_CAD §10.5, en la laptop) dio **2179 g / 72.5 h** en total:

| STL (en `salida/simple/boya/stl/`) | Cant. | Orientación | Soportes | Relleno | g c/u | h c/u |
|---|---|---|---|---|---|---|
| `B1s_casco.stl` | 1 | X180 | sí | 100 % | 957 | 64 |
| `B2s_tapa.stl` | 1 | Y+90 | sí | 100 % | 331 | 22 |
| `B1bs_bandeja.stl` | 1 | sin girar | no | 40 % | 129 | 8.6 |
| `B3s_larguero.stl` | 2 | X180 | no | 40 % | 26 | 1.7 |
| `B5s_flotador.stl` | 4 | Y+90 | sí | 100 % | 116 | 7.7 |
| `B6s_ojal.stl` | 1 | X180 | no | 100 % | 11 | 0.7 |

Total (c): 1943 g y ~130 h según la bitácora; según el slicer de §10.5, 2179 g y 72.5 h.

## Si cambia una medida

Estos STL son una copia girada del commit en el que se generaron. Si se toca `params.py`, se regenera
(`CAMBIOS_RAPIDOS.md`) y esta carpeta queda vieja: hay que volver a exportarla.
