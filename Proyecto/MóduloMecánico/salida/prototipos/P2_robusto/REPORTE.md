# Version P2_robusto del nodo, aro Ø200 (generado por `simple.py`)

No editar a mano: se regenera con `python cad_final/build.py --rapido` cuando `version = "simple"` en `params.py`. La version modular no cambia. mm, g, N, MPa.

**V2 (29/10, decisiones del equipo) y tanda 3 (30/10 noche):** ESP32-S3 sobre KIT_A en 2 pisos (caja 129.0 × 128.0 × 78.0). **Caja baja:** el PG7 de cada camara atraviesa la pared extrema de M1 a z = 14.7, el eje del conducto del riel, y el domo entra en el conducto: no hay camara de cables. Cada mitad del riel (M3s, con el gancho en C fusionado) se atornilla con una brida a un cojin de la pared extrema (4 M4 a insertos). **Lastre a granel:** un bolsillo por lado moldeado bajo el piso de M1, fuera del sello, cerrado por M3t. Capsulas fijas a 30 grados mirando **adentro** (a la malla); la tapa M5s trae el pie en silla con 2 M4 que cruzan el riel.

## 1. Piezas

| Pieza | Archivo (`salida/simple/stl`, `step`) | Cant. | BRep/BOP | Estanco | Cuerpos | Bbox en la orientacion (mm) | Voladizo mm² | Espesor p1 | Masa al 100 % g |
|---|---|---|---|---|---|---|---|---|---|
| M1 caja baja con bolsillos | M1s_caja_cuerpo | 1 | ok | si | 1 | 149.0 x 156.0 x 78.0 (sin girar) | 847 |  | 467 |
| M2 caja, tapa con asa | M2_caja_tapa | 1 | ok | si | 1 | 149.0 x 148.0 x 85.5 (sin girar) | 1576 |  | 203 |
| M3s riel con gancho, mitad | M3s_riel_gancho | 2 | ok | si | 1 | 140.5 x 81.8 x 50.0 (X+90) | 5046 | 1.50 | 214 |
| M3t tapa del bolsillo | M3t_tapa_bolsillo | 2 | ok | si | 1 | 117.0 x 61.0 x 5.0 (X180) | 0 |  | 45 |
| M5s tapa con pie | M5s_capsula_tapa_pie | 2 | ok | si | 1 | 51.9 x 66.0 x 72.2 (X180) | 895 | 1.36 | 102 |
| M3f marco del bolsillo de lastre | M3f_marco_bolsillo | 2 | ok | si | 1 | 117.0 x 77.0 x 30.0 (X180) | 0 |  | 79 |
| M11 bandeja (M11_bandeja) | M11_bandeja | 1 | ok | si | 1 | 115.0 x 114.0 x 30.0 (sin girar) | 0 |  | 55 |
| M11 bandeja (M11_bandeja_sup) | M11_bandeja_sup | 1 | ok | si | 1 | 115.0 x 114.0 x 3.0 (sin girar) | 0 |  | 50 |
| M4 capsula, cuerpo | M4_capsula_cuerpo | 2 | ok | si | 1 | 66.0 x 66.0 x 45.0 (Y+90) | 606 |  | 82 |
| M6 bisel | M6_capsula_bisel | 2 | ok | si | 1 | 42.0 x 42.0 x 2.5 (Y+90) | 0 |  | 2 |
| M7 ventana (acrilico) | M7_capsula_ventana | 2 | ok | si | 1 | 30.0 x 30.0 x 3.0 (Y+90) | 0 |  | 3 |

Piezas impresas por nodo: 16 de 10 tipos, mas las 2 ventanas M7 de acrilico. Fusionado respecto de V1: el gancho M9s dentro de cada mitad del riel (se imprimen de costado, la C y el riel en el plano de las capas) y la camara de cables dentro de la caja; los bolsillos del lastre dentro de M1. Quedan aparte, para desmontar: tapas (M2, M3t, M5s), capsulas y bandeja.
STEP del riel para SimScale y el FEM local: `salida/simple/simscale/M3s_riel_fusionado.step` (2 solido(s); dos mitades separadas por la caja: el STEP tiene las 2 mitades con sus ganchos).

## 2. Peso, lastre y peso aparente

Masa por pieza con su relleno (100 % cajas estancas, tapas con junta y ganchos; 40 % riel y bandeja; piel de 1.2): la misma que usa la bitacora. **Lastre:** tuercas y arandelas M8 de inox, a granel (densidad aparente 4.5 g/cm³ del granel, metal de 7.9; ESTIMADO, pesar un cubo lleno), UN bolsillo por lado de 100 × 50 × 30 mm (150 cm³) cerrado por M3t con 2 M3. En el ensamble es un solido por bolsillo (`lastre_izq` = +Y, `lastre_der` = -Y).

| Concepto | Bandeja 40 % | Bandeja 100 % |
|---|---|---|
| caja (M1 con bolsillos + M2 + bandejas + electronica) | 885 | 894 |
| riel con ganchos (2 M3s) | 427 | 427 |
| marcos de los bolsillos (2 M3f) | 110 | 110 |
| tapas del bolsillo (2 M3t) | 90 | 90 |
| capsulas (M4, M5, M6, M7, contenido) | 447 | 447 |
| tornilleria y correas | 40 | 40 |
| Nodo sin lastre g | 2000 | 2009 |
| Desplaza cm³ | 2496 | 2496 |
| Peso aparente sin lastre g | -558 | -549 |
| Lastre que deja el peso aparente en la ventana (200 a 500 g), total g | 871 a 1216 | 861 a 1206 |
| **Lastre puesto g (total, mitad por bolsillo)** | **990** (495) | **990** (495) |
| **Peso aparente con ese lastre g** | **+303** | **+312** |
| **Peso en aire g** | **2990** | **2999** |

Rango de lastre que mantiene ambos casos en la ventana: **871 a 1206 g** en total. El granel llena 22.0 de 30 mm del bolsillo (73 %); en el maximo del rango llenaria 26.8 mm (cabe). Con tuercas y arandelas M8 de inox, a granel: 1044 g en total, 23.2 mm llenos. Con perdigon de plomo en bolsa: 999 g en total, 15.4 mm llenos.

Estabilidad: centro de masa a 41.7 y de empuje a 58.5 sobre el aro, BG = **16.8 mm**.

## 3. Linterna de prueba, cuerdas y camaras

Aro Ø200, malla de referencia, **4 cuerdas** que suben rectas del aro (atadas por fuera de la varilla) a 45 grados del riel, por encima de la tapa, y de ahi van rectas a **un solo punto de amarre**; del nudo sale un cabo a la linea larga. Sin separador LR1, sin anillo guia y sin apice. El nodo cuelga del aro con el riel (los brazos) entre cuerdas.

| Concepto | Valor |
|---|---|
| Nodo sobre el centro de la varilla del aro | de -53 a 204 mm |
| Azimut de las cuerdas en el marco del nodo (riel en X) | 45, 135, 225, 315 grados |
| Codo de las cuerdas / punto de amarre sobre el aro | 218 / **400 mm** (`linterna.nudo_h`) |
| **Aire cuerda-brazo** (exigido 10) | **51.0 mm** |
| **Aire cuerda-capsula** (exigido 10) | **70.6 mm** |
| Aire cuerda-caja (brida de la tapa; informativo) | 7.5 mm |
| Aro y red contra el nodo | sin contacto |
| Camara en Ø200: lente a la red | 42 mm, campo diagonal 58 mm, FUERA del enfoque (80 mm a infinito, estimado) |
| Camara en Ø500 | el eje optico no corta la red |

FOV 70 grados diagonal (estimado, sin ficha). El aro LED rodea el lente: ilumina el encuadre si su haz es al menos tan ancho como el FOV (dato del LED por confirmar).

## 4. Interferencias y recorridos

Ninguna (umbral 0.01 mm³).

Contratuercas de los PG7 de las paredes contra bandeja, modulos y caja: 0.00 mm³ (la bandeja tiene una muesca en cada extremo). Los M4 del pie pasan 6.4 mm sobre el Cat5e.

## 5. Verificacion a mano (150 N de manipulacion en una capsula)

- **Riel en los ganchos (en el agua):** M = F·|x_capsula − 100| = 8784 N·mm; seccion en x = 142: I = 74313 mm⁴, c = 15.5; σ = 1.8 MPa → FS 24.6 / 12.0 entre capas.
- **Brida del riel a la caja, izado por el asa:** M = 12609 N·mm sobre 4 insertos M4 con 20 de brazo: **353 N por inserto** (PB8). En el agua, sobre los ganchos: 28 N.
- **Gancho en C (fusionado) con 150 N** (la capsula cuelga junto a su gancho: uno solo lleva la carga):** σ = 12.0 MPa → FS 3.7 / 1.8 entre capas.
- **Pie de la capsula:** M = 7400 N·mm, 146 N por M4 sobre las paredes de 6 del riel: 1.9 MPa → FS 23.2 / **11.3** entre capas (cumple FS ≥ 2 sin inserto ni pared de 6: la capsula mirando adentro queda bajo la silla y la palanca es corta).

## 6. Cable

Por camara: 60 + 25 + conducto 136 (recto, sin curva) + bucle 41 + 30 + 30 = **297 mm** (alcanza el cable de fabrica de 300).

## 7. Chequeos que fallaron

- ninguno

## 7b. Avisos (no hacen fallar el build)

- cuerda-caja (brida de la tapa) a 7.5 mm, menos que los 10 que se piden a brazos y capsulas

## 8. Constantes de modulo

- `PAD_BORE` = 30: agujero del cojin para la llave de vaso del PG7. `POCKET_END` = 8: paredes extremas de los bolsillos con los insertos M3 de M3t. `TIP_HOLE` = 8: salida del cable en la punta. `HOOK_CLR` = 10: aire entre el gancho y la capsula.
- Tiempo de `simple.py`: 34 s.
