# Aros de la linterna y estación LoRa de tierra (05/11)

Regenerar desde `cad_final/`: `aro.py` (con `LG_VERSION=P2_robusto`) y `tierra.py`. Salidas en `salida/aro/` y `salida/tierra/`.

## LR2_aro: NO cumple con 8,5 mm

| Sección | Caso | σ percentil 99,5 (MPa) | Pico de flexión (MPa) | FS entre capas, percentil | FS entre capas, pico | Flecha (mm) |
|---|---|---|---|---|---|---|
| **Ø8,5 (impresa)** | 2 kg + 150 N vertical | 40,5 | 46,0 | **0,54** | **0,48** | 9,4 |
| Ø8,5 | 2 kg + 150 N en el plano | 36,2 | 42,6 | 0,61 | 0,52 | 9,1 |
| Ø8,5 | Solo 2 kg | 0,9 | 0,8 | 24,4 | 26,8 | 0,15 |
| Ø15 | 2 kg + 150 N vertical | 7,1 | 8,7 | 3,10 | 2,52 | 1,1 |
| Ø16 | 2 kg + 150 N vertical | 5,8 | 7,6 | 3,77 | 2,91 | 0,9 |
| **Ø16,5 (propuesta)** | 2 kg + 150 N vertical | 5,4 | 6,8 | 4,11 | **3,24** | 0,8 |
| Ø16,5 | 2 kg + 150 N en el plano | 5,0 | 6,6 | 4,38 | 3,32 | 0,7 |

Con Ø8,5 el pico también llega al límite a lo largo de las capas (45 MPa, FS ≈ 1,0): a 150 N el aro cedería, y la flecha de 9 mm sale de un cálculo lineal que ya no vale ahí. Por proporción, soporta unos 20 N de manipulación además de los 2 kg con FS 3 (estimado, no simulado).

**Propuesta, sin aplicar:** aro Ø16,5 y asiento del gancho Ø16,8 (misma regla de 0,3), pared de la C 6 mm. Pesa 169 g cada aro (676 g los 4, frente a 177 g). El gancho solo, con la brida fija, da FS entre capas 13,7. Falta regenerar M3s con ese asiento, comprobar que no choque con la cápsula y repetir el FEM del riel completo.

### Supuestos del FEM
- Cada aro cuelga de 4 cuerdas a 90° y lleva su piso de malla con conchas: **2 kg, sin pesar**, repartidos en el aro.
- Los 150 N actúan en 20 mm del aro, en el punto medio entre 2 cuerdas (el peor punto). Los pisos inferiores cuelgan de las cuerdas, no del aro.
- PETG isótropo de `params.py`: E 1700 MPa, 45 MPa en capa, 22 MPa entre capas (estimados). FS entre capas = 22 / σ von Mises, como en `fem.py`.
- «Pico» es el máximo fuera de los apoyos y de la zona de carga. La flexión allí es real, y el percentil 99,5 la subestima porque esa zona es pequeña; por eso la propuesta usa el pico.
- Solver propio `fem_tet10.py` (TET10), porque CalculiX no está en esta PC ni pude descargarlo. Contra teoría de vigas: desplazamiento −1,2 %, tensión −4,3 %. Conviene repetir el caso de Ø8,5 con `fem.py` en la PC de casa.

### Decisión de sección
El asiento actual mide Ø8,8, así que la regla (asiento − 0,3) da **8,5 mm**, no 8,6. Con `aro.seccion` 8,5 y `gancho.c` 0,15 el asiento no cambia: el volumen del gancho es idéntico antes y después (37 681,758 mm³), y **M3s no se regenera ni se reimprime**.

### Impresión
- Ø208,5 × 8 mm de alto, dentro de los 230 mm. Base plana de 4 mm de ancho, relleno 100 %.
- Sin soportes, la parte baja de la sección queda con voladizo de hasta 62° respecto a la vertical. Es de esperar una cara inferior rugosa; PB_aro_tramo lo muestra.
- El aro entra con el plano hacia la boca de la C.

### Probeta PB_aro
Son 2 piezas: `PB_aro_tramo` (50 mm de aro) y `PB_aro_asiento` (el asiento real de M3s, con mordazas y ranura de correa).

En los 12 mm de asiento la curva del aro se desvía 0,18 mm. Con 0,15 de holgura radial solo calza si el aro se centra, y queda **0,06 mm de margen**. Si no entra en la probeta, hay que resolverlo antes de imprimir los 4.

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
- **Compresión de la junta:** el paso de tornillos es 76,2 × 83,2 mm y `caja.m3_paso_max` pide 76 como máximo. Con 4 tornillos, como se pidió, el lado largo se pasa un poco; probar con agua a chorro.
- **Compras:** tapón de silicona de 30 × 13 × 4 mm, acrílico de 31 × 20 × 2 mm pegado con sellador, SMA de mamparo con su junta. La pared lisa de 3 mm es el asiento de la SMA.

## Gramos estimados (sin OrcaSlicer, PETG 1,27 g/cm³, 100 % relleno)

| Pieza | Cant. | g c/u | g total |
|---|---|---|---|
| LR2_aro | 4 | 44,2 | 176,8 |
| PB_aro_tramo | 1 | 3,5 | 3,5 |
| PB_aro_asiento | 1 | 14,1 | 14,1 |
| T1_caja | 1 | 73,9 | 73,9 |
| T2_tapa | 1 | 50,1 | 50,1 |
| **Total** | | | **318,4** |

Unas 10 h y S/ 19, usando el ritmo de las placas del 05/11 (31 g/h) y S/ 60/kg. El slicer dará el dato real.
