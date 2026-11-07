# Aros de la linterna y estación LoRa de tierra (05/11)

> **05/11, decisión de equipo:** sin probetas. `gancho.c` pasa a 0,30 mm por lado, asiento Ø17,1, FS entre capas 3,95 / 5,19 y sin choques. Total 3887 g, 4 rollos. Donde abajo dice Ø16,8, PB_aro o 5 rollos, vale esto; detalle en `ESTADO.md`.

Regenerar desde `cad_final/`: `aro.py` (con `LG_VERSION=P2_robusto`) y `tierra.py`. Salidas en `salida/aro/` y `salida/tierra/`.

## LR2_aro: Ø16,5 parejo en los 4 aros

**Decisión final del 05/11:** sección Ø16,5 en los 4 aros, sin tramos delgados. Reemplaza a la decisión anterior de Ø8,5.

> **Diseñado para 2 kg por piso + 150 N de manipulación; FS entre capas ≥ 3.**

| Caso, aro macizo (malla 2,5) | σ percentil 99,5 (MPa) | σ pico de flexión (MPa) | FS entre capas (percentil / pico) | Flecha (mm) |
|---|---|---|---|---|
| **2 kg + 150 N vertical** | 5,36 | 6,79 | 4,11 / **3,24** | 0,81 |
| 2 kg + 150 N en el plano del aro | 5,02 | 6,63 | 4,38 / 3,32 | 0,71 |

El pico de flexión es el σ máximo lejos de apoyos y carga: es más exigente que el percentil de `fem.py` y es el que pide FS ≥ 3.

### Supuestos del FEM
- Cada aro cuelga de 4 cuerdas a 90° y lleva su piso: **2 kg, sin pesar**. Los 150 N se aplican en un punto entre dos cuerdas. Carga estática: no incluye olas ni tirones.
- Los pisos inferiores cuelgan de las cuerdas, no del aro.
- PETG isótropo de `params.py`: E 1700 MPa, 45 MPa en capa, 22 MPa entre capas (estimados).
- Solver propio `fem_tet10.py` (TET10), porque CalculiX no está en esta PC. Contra teoría de vigas: desplazamiento −1,2 %, tensión −4,3 %. Falta repetirlo con `fem.py` en la PC de casa.

### M3s con asiento Ø16,8
`aro.seccion` 16,5 y `gancho.c` 0,15 dan un asiento Ø16,8. **M3s cambia y hay que reimprimirlo:** 168,2 cm³ (antes 170,8) y 81,8 mm en su lado mayor del gancho (antes 79,4). Las otras 10 piezas del nodo quedaron con el mismo volumen y la misma caja, y se dejaron sin tocar.

| Verificación del riel completo | Resultado | Pedido |
|---|---|---|
| FEM en el agua, 150 N en la cápsula (`riel_agua`) | **FS entre capas 3,94**, flecha 1,36 mm | ≥ 3 |
| FEM izado por el asa, 150 N (`riel_izado`) | FS entre capas 5,19, flecha 0,21 mm | ≥ 3 |
| Choque con la cápsula y resto del nodo | ninguno (`simple.py` sin fallas) | sin choque |
| Aire cuerda-caja | **7,5 mm** (antes 3,2) | ≥ 3 |
| Aire cuerda-brazo / cuerda-cápsula | 51,0 / 70,6 mm | ≥ 10 |
| Cama | M3s 140,5 × 81,7 × 50; aro Ø216,5 | ≤ 230 |

- **Calibración del FEM:** `fem_riel.py` usa las mismas caras que `fem.py`, pero reparte la carga en vez de usar un cuerpo rígido. Sobre el M3s anterior, con la misma malla (65 800 elementos), dio FS 3,47 / 5,19 contra 3,37 / 5,83 de CalculiX; la flecha, 1,80 contra 1,81 mm. Corregido por esa diferencia, `riel_agua` queda en unos 3,8.
- **Cuenta a mano del gancho en `REPORTE.md`:** da FS 1,9 entre capas (antes 2,9). Es muy conservadora: trata la C como una viga abierta de 12 mm con toda la carga. El FEM del gancho solo con 150 N da FS 13,7. Rige el FEM, pero conviene probarlo con la probeta PB_aro.
- **Lastre:** M3s pesa 7 g menos el par y desplaza menos, así que el lastre calculado sube de 980 a 990 g (peso aparente +303 g).

### Calce: agujero corrido 0,09 mm
El asiento es recto y el aro se curva 0,18 mm en sus 12 mm. Con el agujero centrado, el aro rozaba 0,03 mm en los extremos (0,12 mm³ por gancho) y `simple.py` lo marcaba como falla. Como los dos ganchos están enfrentados, el aro no puede acomodarse solo. **El agujero del asiento se corrió 0,09 mm hacia el eje del nodo** (`simple.seat_shift()`), con Ø16,8 igual.

Ahora la interferencia es 0, pero el margen real es **0,06 mm por lado**, no 0,15. Es menor que la tolerancia de impresión: **probar PB_aro antes de imprimir los 4 aros y los M3s.**

### Impresión elegida: 13 perímetros + 15 % de gyroid
**Es la configuración más liviana con FS ≥ 3: 150,0 g por aro y FS entre capas 3,01** (2 kg + 150 N). Ninguna combinación de 4 a 6 perímetros con 15–25 % de gyroid llega: se quedan entre 1,70 y 2,35.

| Perímetros (pared) | Relleno gyroid | g por aro | FS entre capas | ¿Cumple? |
|---|---|---|---|---|
| 4 (1,6 mm) | 15 % | 76,0 | 1,70 | no |
| 4 (1,6 mm) | 20 % | 81,5 | 1,75 | no |
| 4 (1,6 mm) | 25 % | 87,0 | 1,79 | no |
| 5 (2,0 mm) | 15 % | 87,0 | 2,00 | no |
| 5 (2,0 mm) | 20 % | 91,8 | 2,04 | no |
| 5 (2,0 mm) | 25 % | 96,7 | 2,08 | no |
| 6 (2,4 mm) | 15 % | 97,3 | 2,28 | no |
| 6 (2,4 mm) | 20 % | 101,5 | 2,31 | no |
| 6 (2,4 mm) | 25 % | 105,7 | 2,35 | no |
| 6 (2,4 mm) | 50 % | 126,8 | 2,56 | no |
| 6 (2,4 mm) | 80 % | 152,2 | 2,90 | no |
| 8 (3,2 mm) | 15 % | 115,8 | 2,60 | no |
| 9 (3,6 mm) | 15 % | 124,0 | 2,71 | no |
| 10 (4,0 mm) | 15 % | 131,5 | 2,86 | no |
| 11 (4,4 mm) | 15 % | 138,4 | 2,93 | no |
| 12 (4,8 mm) | 15 % | 144,6 | 2,95 | no |
| **13 (5,2 mm)** | 15 % | **150,1** | **3,01** | sí |
| 14 (5,6 mm) | 15 % | 154,9 | 3,03 | sí |
| macizo | — | 169,1 | 3,16 | sí |

- **Margen muy justo:** FS 3,01 frente a 3,16 del macizo en este mismo modelo. El ahorro es de 19 g por aro (76 g en los 4): en este aro la flexión la lleva sobre todo la periferia de la sección, y una pared delgada pierde rigidez y tensión admisible enseguida.
- **Modelo:** pared maciza más núcleo con E = E_PETG × ρ² (Gibson-Ashby con C = 1, **sin ensayo**), en FEM TET10 de malla 1,6 mm en la pared y 3,5 mm en el núcleo (`aro_relleno.py`, resultados en `salida/aro/relleno.json`). El FS usa el pico de von Mises en la pared, lejos de apoyos y carga. Al ser el núcleo tan pequeño, el valor de su rigidez apenas influye.
- **Núcleo:** su tensión queda muy por debajo de su resistencia estimada (FS 15 con ρ^1,5 × 22 MPa).
- **Hay que ajustar el slicer:** el modelo supone una cáscara uniforme de 5,2 mm, así que las capas superiores e inferiores también deben sumar 5,2 mm (26 capas de 0,2). Con los valores por defecto el FS real sería menor.
- **Sin probar:** contacto local bajo la cuerda y en el asiento del gancho con la pieza real.

### Impresión
- Ø216,5 × 16 mm de alto, dentro de los 230 mm. Base plana de 5,7 mm de ancho.
- Sin soportes, la parte baja de la sección queda con voladizo de hasta 62° respecto a la vertical. Es de esperar una cara inferior rugosa; PB_aro_tramo lo muestra.
- El aro entra con el plano hacia la boca de la C.

### Probeta PB_aro
Son 2 sólidos: `PB_aro_tramo` (50 mm de aro Ø16,5, con la misma impresión del aro) y `PB_aro_asiento` (el asiento Ø16,8 real de M3s, con mordazas y ranura de correa).

## Posición en el ensamble
Los 4 aros van centrados en el eje del nodo y con la base plana hacia abajo: uno a la altura del asiento del gancho y los otros cada 50 mm hacia abajo (`linterna.alto` / (`linterna.pisos` + 1)). **Esa separación viene de la red de referencia del modelo:** corregirla si la linterna real usa otra.

## T1_caja y T2_tapa

| Dato | Valor |
|---|---|
| Interior | 64,2 × 71,25 × 22 mm |
| Exterior | T1: 86,3 × 121,3 × 25 mm con pestañas; T2: 86,2 × 93,3 × 6 mm |
| Holguras | 3 mm a paredes y entre componentes; 7,4 mm del Heltec a la tapa; 12 mm de la batería a la tapa |
| Junta | Cordón NBR Ø2, unos 284 mm, ranura 2,6 × 1,5, compresión 25 % |
| Tornillos | 4 M3 inox A4 a insertos térmicos, Ø3,4 en la tapa |
| Heltec | 4 postes Ø8,5 de 8 mm con inserto M2,5 |
| Fijación | 4 pestañas de 6 mm con ojal de 5,5 × 12 |

- **Montaje:** con el USB-C hacia abajo y la SMA arriba, para que el puerto abierto no mire a la lluvia.
- **Sin soportes:** el reborde y las torres salen de la pared a 45°. Las únicas caras planas al aire son 2 puentes en el puerto USB: 24 × 3 mm y 30 × 4 mm.
- **Comprobado:** sólidos válidos y cerrados, sin choques de componentes (como bloques) contra la caja. Paredes de 2,4 mm o más por diseño, no medidas en una sección.

### Antes de imprimir
- **Medir el Heltec y la batería:** todas las medidas son típicas. La distancia entre agujeros (44 × 19,5) y la posición de la pantalla son **estimadas**; confirma también que tu placa tenga agujeros M2,5 y que los postes no toquen los pines.
- **PRG y RST:** comparten el puerto del USB-C. No verifiqué en qué cara de la placa están ni si se alcanzan por ahí.
- **Compresión de la junta:** el paso de tornillos es 76,2 × 83,2 mm y `caja.paso_tornillos` pide 76 como máximo. Con 4 tornillos, como se pidió, el lado largo se pasa un poco; probar con agua a chorro.
- **Compras:** tapón de silicona de 30 × 13 × 4 mm, acrílico de 31 × 20 × 2 mm pegado con sellador, SMA de mamparo con su junta. La pared lisa de 3 mm es el asiento de la SMA.

## Ensamble de la estación de tierra
`tierra.py --ensamble` genera `salida/tierra/step/00_ENSAMBLE_tierra.step`, con **30 sólidos sin choques**: 15 en posición cerrada y, a 200 mm en X, la copia explosionada `EXP_*` con la tapa, el acrílico y los tornillos levantados 40 mm. En Onshape: 30 partes contra 30 sólidos.

- **Referencias `REF_` simplificadas:** Heltec, batería, SMA, acrílico OLED, cordón NBR, 4 tornillos M3 × 10 y 4 insertos M3. Bloques y cilindros con las medidas de `tierra.medidas`, no modelos de catálogo. El cordón se muestra comprimido.
- **Corrección de T1:** el agujero de la SMA bajó 1 mm (z = 10), porque su cara Ø12 chocaba 0,9 mm con el chaflán del reborde. No cambian ni el volumen ni los gramos.

## Gramos del proyecto (estimados por volumen, sin OrcaSlicer: PETG 1,27 g/cm³)

| Pieza | Cant. | Impresión | g c/u | g total |
|---|---|---|---|---|
| LR2_aro | 4 | 13 perímetros + 15 % gyroid | 150,0 | 600,0 |
| PB_aro_tramo | 1 | 13 perímetros + 15 % gyroid | 12,0 | 12,0 |
| PB_aro_asiento | 1 | 100 % | 15,7 | 15,7 |
| T1_caja | 1 | 100 % | 73,9 | 73,9 |
| T2_tapa | 1 | 100 % | 50,1 | 50,1 |
| **Piezas nuevas** | | | | **751,7** |
| Las 20 placas del 05/11 (slicer) | | | | 3427 |
| Cambio del par de M3s (por volumen y relleno) | | | | −7 |
| **Total del proyecto** | | | | **≈ 4172 g** |

**Rollos: 5 de 1 kg.** El objetivo de 4 rollos con 150 g de margen pedía 3850 g como máximo; el total se pasa por 322 g, y por 172 g de los 4000 g aun sin margen. Para llegar, cada aro debería pesar unos 70 g, y el más liviano probado (76 g) tiene FS 1,70.

Las piezas nuevas suman unas 24 h y S/ 45, con el ritmo de las placas del 05/11 (31 g/h) y S/ 60/kg; el proyecto, unas 135 h y S/ 251. El slicer dará el dato real, también para el M3s nuevo: su placa actual es del asiento anterior.

## Links en Onshape (LG_IMPRIMIR_P2)

| Pieza | Pestaña | Plano A4 |
|---|---|---|
| LR2_aro | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/0105e147c7a4e8f46f07161a) | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/b64dbc5d60c83da533be9d16) |
| PB_aro | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/80b871519eaba8cd1f27bd1f) | no aplica |
| T1_caja | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/081fe1777b92ade3e58b5980) | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/ff8fd312cba1b15897893cdb) |
| T2_tapa | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/f76a01b7833bfd0c4e619446) | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/3f6976556319bf5b1aeb0f9a) |
| M3s_riel_gancho | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/b72266e724b98f2af5bae60e) | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/02675b967c8f513dbfaa5ebc) |
| 00_ENSAMBLE | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/9f5db126d529a7a6219ab47f) | no aplica |
| 00_ENSAMBLE_tierra | [abrir](https://cad.onshape.com/documents/b2a875b87e1322c259f4cd3b/w/3bda440db9eda84724dc5cff/e/5516991cd254ef9b0bc3baca) | no aplica |
