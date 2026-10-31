# Version P4_estetico del nodo, aro Ø200 (generado por `simple.py`)

No editar a mano: se regenera con `python cad_final/build.py --rapido` cuando `version = "simple"` en `params.py`. La version modular no cambia. mm, g, N, MPa.

**V2 (29/10, decisiones del equipo) y tanda 3 (30/10 noche):** ESP32-S3 sobre KIT_A en 2 pisos (caja 117.0 × 126.0 × 77.0). **Caja baja:** el PG7 de cada camara atraviesa la pared extrema de M1 a z = 13.7, el eje del conducto del riel, y el domo entra en el conducto: no hay camara de cables. Cada mitad del riel (M3s, con el gancho en C fusionado) se atornilla con una brida a un cojin de la pared extrema (4 M4 a insertos). **Lastre a granel:** un bolsillo por lado moldeado bajo el piso de M1, fuera del sello, cerrado por M3t. Capsulas fijas a 30 grados mirando **adentro** (a la malla); la tapa M5s trae el pie en silla con 2 M4 que cruzan el riel.

## 1. Piezas

| Pieza | Archivo (`salida/simple/stl`, `step`) | Cant. | BRep/BOP | Estanco | Cuerpos | Bbox en la orientacion (mm) | Voladizo mm² | Espesor p1 | Masa al 100 % g |
|---|---|---|---|---|---|---|---|---|---|
| M1m caja con tramos de riel | M1m_caja_riel | 1 | ok | si | 1 | 250.0 x 146.0 x 118.3 (X180) | 22165 |  | 597 |
| M2 caja, tapa con asa | M2_caja_tapa | 1 | FALLA | si | 1 | 63.0 x 146.0 x 137.0 (Y+90) | 1622 |  | 162 |
| M3t tapa del bolsillo | M3t_tapa_bolsillo | 2 | ok | si | 1 | 117.0 x 57.0 x 3.0 (X180) | 0 |  | 25 |
| M5m extremo de riel con pie y tapa | M5m_extremo_pie | 2 | ok | si | 1 | 90.0 x 64.0 x 95.9 (X180) | 3579 | 2.83 | 128 |
| M9c abrazadera (media luna del gancho) | M9c_abrazadera | 2 | ok | si | 1 | 36.8 x 10.4 x 12.0 (X+90) | 40 |  | 3 |
| M11 bandeja (M11_bandeja) | M11_bandeja | 1 | ok | si | 1 | 105.0 x 114.0 x 30.0 (sin girar) | 36 |  | 46 |
| M11 bandeja (M11_bandeja_sup) | M11_bandeja_sup | 1 | ok | si | 1 | 105.0 x 114.0 x 3.0 (sin girar) | 0 |  | 44 |
| M4 capsula, cuerpo | M4_capsula_cuerpo | 2 | ok | si | 1 | 64.0 x 64.0 x 44.0 (Y-90) | 1038 |  | 58 |
| M6 bisel | M6_capsula_bisel | 2 | ok | si | 1 | 42.0 x 42.0 x 2.5 (Y+90) | 0 |  | 2 |
| M7 ventana (acrilico) | M7_capsula_ventana | 2 | ok | si | 1 | 30.0 x 30.0 x 3.0 (Y+90) | 0 |  | 3 |

Piezas impresas por nodo: 14 de 9 tipos, mas las 2 ventanas M7 de acrilico. Fusionado respecto de V1: el gancho M9s dentro de cada mitad del riel (se imprimen de costado, la C y el riel en el plano de las capas) y la camara de cables dentro de la caja; los bolsillos del lastre dentro de M1. Quedan aparte, para desmontar: tapas (M2, M3t, M5s), capsulas y bandeja.
STEP del riel para SimScale y el FEM local: `salida/simple/simscale/M3s_riel_fusionado.step` (1 solido(s); P3/P4: riel fundido (tramo central + extremo) de un lado, con las bridas de union como cuerpo continuo).

## 2. Peso, lastre y peso aparente

Masa por pieza con su relleno (100 % cajas estancas, tapas con junta y ganchos; 40 % riel y bandeja; piel de 1.2): la misma que usa la bitacora. **Lastre:** tuercas y arandelas M8 de inox, a granel (densidad aparente 4.5 g/cm³ del granel, metal de 7.9; ESTIMADO, pesar un cubo lleno), UN bolsillo por lado de 100 × 50 × 28 mm (140 cm³) cerrado por M3t con 2 M3. En el ensamble es un solido por bolsillo (`lastre_izq` = +Y, `lastre_der` = -Y).

| Concepto | Bandeja 40 % | Bandeja 100 % |
|---|---|---|
| caja con tramos de riel (M1m + M2 + bandejas + electronica) | 961 | 969 |
| abrazaderas (2 M9c) | 7 | 7 |
| tapas del bolsillo (2 M3t) | 51 | 51 |
| capsulas (M4, M5, M6, M7, contenido) | 452 | 452 |
| tornilleria y correas | 40 | 40 |
| Nodo sin lastre g | 1510 | 1518 |
| Desplaza cm³ | 1995 | 1995 |
| Peso aparente sin lastre g | -535 | -527 |
| Lastre que deja el peso aparente en la ventana (200 a 500 g), total g | 844 a 1189 | 835 a 1180 |
| **Lastre puesto g (total, mitad por bolsillo)** | **1020** (510) | **1020** (510) |
| **Peso aparente con ese lastre g** | **+353** | **+361** |
| **Peso en aire g** | **2530** | **2538** |

Rango de lastre que mantiene ambos casos en la ventana: **844 a 1180 g** en total. El granel llena 22.7 de 28 mm del bolsillo (81 %); en el maximo del rango llenaria 26.2 mm (cabe). Con tuercas y arandelas M8 de inox, a granel: 1017 g en total, 22.6 mm llenos. Con perdigon de plomo en bolsa: 973 g en total, 15.0 mm llenos.

Estabilidad: centro de masa a 42.7 y de empuje a 61.9 sobre el aro, BG = **19.2 mm**.

## 3. Linterna de prueba, cuerdas y camaras

Aro Ø200, malla de referencia, **4 cuerdas** que suben rectas del aro (atadas por fuera de la varilla) a 45 grados del riel, por encima de la tapa, y de ahi van rectas a **un solo punto de amarre**; del nudo sale un cabo a la linea larga. Sin separador LR1, sin anillo guia y sin apice. El nodo cuelga del aro con el riel (los brazos) entre cuerdas.

| Concepto | Valor |
|---|---|
| Nodo sobre el centro de la varilla del aro | de -40 a 181 mm |
| Azimut de las cuerdas en el marco del nodo (riel en X) | 45, 135, 225, 315 grados |
| Codo de las cuerdas / punto de amarre sobre el aro | 195 / **400 mm** (`linterna.nudo_h`) |
| **Aire cuerda-brazo** (exigido 10) | **56.5 mm** |
| **Aire cuerda-capsula** (exigido 10) | **68.3 mm** |
| Aire cuerda-caja (brida de la tapa; informativo) | 6.8 mm |
| Aro y red contra el nodo | sin contacto |
| Camara en Ø200: lente a la red | 38 mm, campo diagonal 53 mm, FUERA del enfoque (80 mm a infinito, estimado) |
| Camara en Ø500 | el eje optico no corta la red |

FOV 70 grados diagonal (estimado, sin ficha). El aro LED rodea el lente: ilumina el encuadre si su haz es al menos tan ancho como el FOV (dato del LED por confirmar).

## 4. Interferencias y recorridos

Ninguna (umbral 0.01 mm³).

Contratuercas de los PG7 de las paredes contra bandeja, modulos y caja: 0.00 mm³ (la bandeja tiene una muesca en cada extremo). Los M4 del pie pasan 8.4 mm sobre el Cat5e.

## 5. Verificacion a mano (150 N de manipulacion en una capsula)

- **Riel en los ganchos (en el agua):** M = F·|x_capsula − 100| = 8066 N·mm; seccion en x = 142: I = 43707 mm⁴, c = 16.1; σ = 3.0 MPa → FS 15.1 / 7.4 entre capas.
- **Brida del riel a la caja, izado por el asa:** M = 4316 N·mm sobre 4 insertos M4 con 20 de brazo: **145 N por inserto** (PB8). En el agua, sobre los ganchos: 0 N.
- **Gancho en C (fusionado) con 150 N** (la capsula cuelga junto a su gancho: uno solo lleva la carga):** σ = 7.7 MPa → FS 5.8 / 2.9 entre capas.
- **Pie de la capsula:** M = 7850 N·mm, 337 N por M4 sobre las paredes de 4 del riel: 10.0 MPa → FS 4.5 / **2.2** entre capas (cumple FS ≥ 2 sin inserto ni pared de 6: la capsula mirando adentro queda bajo la silla y la palanca es corta).

## 6. Cable

Por camara: 60 + 25 + conducto 156 (recto, sin curva) + bucle 82 + 30 + 30 = **384 mm** (requiere prueba SPI a 8 y 4 MHz).

## 7. Chequeos que fallaron

- ninguno

## 7b. Avisos (no hacen fallar el build)

- cuerda-caja (brida de la tapa) a 6.8 mm, menos que los 10 que se piden a brazos y capsulas

## 8. Constantes de modulo

- `PAD_BORE` = 30: agujero del cojin para la llave de vaso del PG7. `POCKET_END` = 8: paredes extremas de los bolsillos con los insertos M3 de M3t. `TIP_HOLE` = 8: salida del cable en la punta. `HOOK_CLR` = 10: aire entre el gancho y la capsula.
- Tiempo de `simple.py`: 78 s.
