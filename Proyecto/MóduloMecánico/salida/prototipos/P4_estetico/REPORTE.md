# Version P4_estetico del nodo, aro Ø200 (generado por `simple.py`)

No editar a mano: se regenera con `python cad_final/build.py --rapido` cuando `version = "simple"` en `params.py`. La version modular no cambia. mm, g, N, MPa.

**V2 (29/10, decisiones del equipo):** ESP32-S3 sobre KIT_A en 2 pisos (caja 127.0 × 126.0 × 77.0). **Caja baja:** el PG7 de cada camara atraviesa la pared extrema de M1 a z = 13.7, el eje del conducto del riel, y el domo entra en el conducto: no hay camara de cables. Cada mitad del riel (M3s, con el gancho en C fusionado) se atornilla con una brida a un cojin de la pared extrema (4 M4 a insertos). Los bolsillos del lastre van moldeados bajo el piso de M1, fuera del sello, cerrados por M3t. Capsulas fijas a 30 grados mirando **adentro** (a la malla); la tapa M5s trae el pie en silla con 2 M4 que cruzan el riel.

## 1. Piezas

| Pieza | Archivo (`salida/simple/stl`, `step`) | Cant. | BRep/BOP | Estanco | Cuerpos | Bbox en la orientacion (mm) | Voladizo mm² | Espesor p1 | Masa al 100 % g |
|---|---|---|---|---|---|---|---|---|---|
| M1m caja con tramos de riel | M1m_caja_riel | 1 | ok | si | 1 | 250.0 x 146.0 x 118.3 (X180) | 22610 |  | 576 |
| M2 caja, tapa con asa | M2_caja_tapa | 1 | FALLA | si | 1 | 63.0 x 146.0 x 147.0 (Y+90) | 1648 |  | 171 |
| M3t tapa del bolsillo | M3t_tapa_bolsillo | 2 | ok | si | 1 | 117.0 x 32.0 x 3.0 (X180) | 0 |  | 14 |
| M5m extremo de riel con pie y tapa | M5m_extremo_pie | 2 | ok | si | 1 | 90.0 x 64.0 x 95.9 (X180) | 3579 | 2.83 | 128 |
| M9c abrazadera (media luna del gancho) | M9c_abrazadera | 2 | ok | si | 1 | 36.8 x 10.4 x 12.0 (X+90) | 40 |  | 3 |
| M11 bandeja (M11_bandeja) | M11_bandeja | 1 | ok | si | 1 | 115.0 x 114.0 x 30.0 (sin girar) | 36 |  | 51 |
| M11 bandeja (M11_bandeja_sup) | M11_bandeja_sup | 1 | ok | si | 1 | 115.0 x 114.0 x 3.0 (sin girar) | 0 |  | 48 |
| M4 capsula, cuerpo | M4_capsula_cuerpo | 2 | ok | si | 1 | 64.0 x 64.0 x 44.0 (Y-90) | 1038 |  | 58 |
| M6 bisel | M6_capsula_bisel | 2 | ok | si | 1 | 42.0 x 42.0 x 2.5 (Y+90) | 0 |  | 2 |
| M7 ventana (acrilico) | M7_capsula_ventana | 2 | ok | si | 1 | 30.0 x 30.0 x 3.0 (Y+90) | 0 |  | 3 |

Piezas impresas por nodo: 14 de 9 tipos, mas las 2 ventanas M7 de acrilico. Fusionado respecto de V1: el gancho M9s dentro de cada mitad del riel (se imprimen de costado, la C y el riel en el plano de las capas) y la camara de cables dentro de la caja; los bolsillos del lastre dentro de M1. Quedan aparte, para desmontar: tapas (M2, M3t, M5s), capsulas y bandeja.
STEP del riel para SimScale y el FEM local: `salida/simple/simscale/M3s_riel_fusionado.step` (1 solido(s); P3/P4: riel fundido (tramo central + extremo) de un lado, con las bridas de union como cuerpo continuo).

## 2. Peso y peso aparente

Masa por pieza con su relleno (100 % cajas estancas, tapas con junta y ganchos; 40 % riel y bandeja; piel de 1.2): la misma que usa la bitacora. Pletinas de inox 25 × 5 × 100 (99 g), 5 por bolsillo, 2 bolsillos bajo la caja.

| Concepto | Bandeja 40 % | Bandeja 100 % |
|---|---|---|
| caja con tramos de riel (M1m + M2 + bandejas + electronica) | 957 | 966 |
| abrazaderas (2 M9c) | 7 | 7 |
| tapas del bolsillo (2 M3t) | 28 | 28 |
| capsulas (M4, M5, M6, M7, contenido) | 452 | 452 |
| tornilleria y correas | 40 | 40 |
| Nodo sin pletinas g | 1484 | 1493 |
| Desplaza cm³ | 2054 | 2054 |
| Peso aparente sin pletinas g | -622 | -613 |
| Pletinas por bolsillo para entrar en la ventana | 5 a 6 | 5 a 6 |
| **Peso aparente con 5 por bolsillo g** | **+237** | **+246** |
| **Peso en aire g** | **2471** | **2480** |

Estabilidad: centro de masa a 45.6 y de empuje a 64.1 sobre el aro, BG = **18.6 mm**.

## 3. Linterna, suspension y camaras

| Concepto | Valor |
|---|---|
| Nodo sobre el centro de la varilla del aro | de -40 a 181 mm |
| Separador `separador.altura` | 140 mm (minimo calculado: **136**) |
| **Apice sobre el aro** | **290 mm** |
| Aire minimo suspension-nodo (exigido 10) | **11.6 mm** |
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

Por camara: 60 + 25 + conducto 152 (recto, sin curva) + bucle 82 + 30 + 30 = **379 mm** (requiere prueba SPI a 8 y 4 MHz).

## 7. Chequeos que fallaron

- ninguno

## 8. Constantes de modulo

- `PAD_BORE` = 30: agujero del cojin para la llave de vaso del PG7. `POCKET_END` = 8: paredes extremas de los bolsillos con los insertos M3 de M3t. `TIP_HOLE` = 8: salida del cable en la punta. `HOOK_CLR` = 10: aire entre el gancho y la capsula.
- Tiempo de `simple.py`: 46 s.
