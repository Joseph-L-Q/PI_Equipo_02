# Version simple del nodo, aro Ø200 (generado por `simple.py`)

No editar a mano: se regenera con `python cad_final/build.py --rapido` cuando `version = "simple"` en `params.py`. La version modular (`version = "modular"`) no cambia. mm, g, N, MPa.

Riel de una pieza de 430 en 2 mitades iguales M3s (union plana en x = 0 bajo la caja, 4 M3 en orejas), sin varilla M8, extensiones ni puntas. Ganchos en C fijos M9s a x = ±100 con ranura para correa de 25, sin casquillo, pestillo ni perilla. Capsulas fijas a 30 grados: la tapa M5s trae un pie en silla que se atornilla con 2 M4 horizontales que cruzan el riel (sin bisagra dentada). Caja, tapa, bandeja, capsula, bisel y ventana iguales a la modular. Los cables van por dentro del riel y salen por la ranura lateral junto a la capsula.

## 1. Piezas

| Pieza | Archivo (`salida/simple/stl`, `step`) | Cant. | BRep/BOP | Estanco | Cuerpos | Bbox en la orientacion (mm) | Voladizo mm² | Espesor p1 | Masa al 100 % g |
|---|---|---|---|---|---|---|---|---|---|
| M3s riel, mitad | M3s_riel_mitad | 2 | ok | si | 1 | 215.0 x 100.0 x 57.3 (X180) | 11296 | 2.54 | 189 |
| M9s gancho en C | M9s_gancho | 2 | ok | si | 1 | 50.0 x 47.2 x 33.0 (X+90) | 182 | 2.12 | 27 |
| M5s tapa con pie | M5s_capsula_tapa_pie | 2 | ok | si | 1 | 96.8 x 64.0 x 95.9 (X180) | 2880 | 2.83 | 120 |
| M3t tapa del bolsillo | M3t_tapa_bolsillo | 2 | ok | si | 1 | 107.0 x 35.0 x 3.0 (X180) | 0 |  | 12 |
| M1 caja, cuerpo | M1_caja_cuerpo | 1 | ok | si | 1 | 159.6 x 126.0 x 50.0 (sin girar) | 651 |  | 273 |
| M2 caja, tapa con asa | M2_caja_tapa | 1 | ok | si | 1 | 63.0 x 126.0 x 159.6 (Y+90) | 1375 |  | 164 |
| M11 bandeja (M11_bandeja) | M11_bandeja | 1 | ok | si | 1 | 127.6 x 94.0 x 18.0 (sin girar) | 0 |  | 45 |
| M4 capsula, cuerpo | M4_capsula_cuerpo | 2 | ok | si | 1 | 64.0 x 64.0 x 44.0 (Y-90) | 1038 |  | 58 |
| M6 bisel | M6_capsula_bisel | 2 | ok | si | 1 | 42.0 x 42.0 x 2.5 (Y+90) | 0 |  | 2 |
| M7 ventana (acrilico) | M7_capsula_ventana | 2 | ok | si | 1 | 30.0 x 30.0 x 3.0 (Y+90) | 0 |  | 3 |

Tipos impresos: 9 (M1, M2, M11, M3s, M3t, M9s, M4, M5s, M6) mas la ventana M7 de acrilico. Piezas impresas por nodo: 15. El espesor p1 se mide en las piezas nuevas; las demas son las de la modular, ya medidas.
STEP del riel como un solo solido para SimScale: `salida/simple/simscale/M3s_riel_fusionado.step` (1 solido).

## 2. Peso y peso aparente

Pletinas de inox 25 × 5 × 100 (99 g, hunde 86 g cada una), 3 por bolsillo (`lastre.pletinas`), 2 bolsillos. Ventana: 200 a 500 g hacia abajo; en aire ≤ 3 kg. Desplazamiento con los volumenes reales de los solidos (las piezas con relleno parcial cuentan su volumen entero: la piel cierra el aire) y el aire sellado de la caja y de las capsulas.

| Concepto | Bandeja 40 % | Bandeja 100 % |
|---|---|---|
| caja (M1 + M2 + bandeja + electronica) | 572 | 576 |
| riel (2 M3s al 100 %) | 377 | 377 |
| tapas del bolsillo (2 M3t) | 24 | 24 |
| ganchos (2 M9s al 40 %) | 36 | 36 |
| capsulas (M4 + M5s al 100 %, M6 al 40 %, M7, contenido) | 436 | 436 |
| tornilleria y correas | 40 | 40 |
| Nodo sin pletinas g | 1486 | 1490 |
| Desplaza cm³ | 1695 | 1695 |
| Peso aparente sin pletinas g | -251 | -247 |
| Pletinas por bolsillo para entrar en la ventana | 3 a 4 | 3 a 4 |
| **Peso aparente con 3 por bolsillo g** | **+265** | **+269** |
| **Peso en aire g** | **2079** | **2083** |

Estabilidad (bandeja al 40 %, capsulas a 30 grados): centro de masa z = -30.8, centro de empuje z = -13.4, BG = **17.4 mm** (no se voltea).

## 3. Linterna de prueba y suspension

La linterna cuelga de su propia brida: 4 cuerdas a 60, 120, 240, 300 grados suben verticales del aro al separador LR1 (aro, 12 × 6) y de ahi al apice; del apice sube el cabo central al punto fijo (`linterna.punto_fijo` = estructura). El nodo no carga la linterna: va enganchado al aro con los ganchos y la correa; el ojal del asa queda solo para izarlo. El umbilical baja de la boya al PG7 de la tapa con 80 mm de comba (sin tension).

| Concepto | Valor |
|---|---|
| Techo del nodo sobre el centro de la varilla del aro | 210 mm |
| Separador (plano medio) sobre el aro, `separador.altura` | 250 mm (minimo calculado con 10 mm de aire: **165 mm**) |
| Apice sobre el separador, `apice.altura` | 150 mm |
| **Apice sobre el aro** | **400 mm** |
| Aire minimo suspension-nodo (exigido 10) | **21.6 mm** |
| aire cuerda vertical 120 | 21.6 mm |
| aire cuerda vertical 240 | 21.6 mm |
| aire cuerda vertical 300 | 21.6 mm |
| aire cuerda vertical 60 | 21.6 mm |
| aire LR1 separador | 65.2 mm |
| aire cuerda al apice 60 | 96.0 mm |
| aire cuerda al apice 120 | 96.0 mm |
| aire cuerda al apice 300 | 96.0 mm |
| aire cuerda al apice 240 | 96.0 mm |
| aire cabo central | 187.7 mm |
| Aro contra el nodo (ganchos con holgura 0.4) | sin contacto |
| Red contra el nodo | sin contacto |

LR1 (`salida/linterna_prueba/LR1_separador.stl` y `.step`): pieza de referencia de la linterna, no del nodo; se imprime plana en PETG si hace falta. Bbox 211.9 x 211.9 x 6.0 (sin girar), cabe en la cama: si. Con `separador.tipo` = cruceta son rayos al centro y la altura minima sube (pasa sobre el asa).

## 4. Interferencias del nodo

Ninguna (umbral 0.01 mm³; las caras en contacto dan 0).
Solapes de modelado de 0.01 mm, no son choques (las tapas del bolsillo entran 0.01 en la pared para unirse, igual que en la modular): M3t tapa bolsillo n / M3s riel +X 1.6 mm³; M3t tapa bolsillo n / M3s riel -X 1.6 mm³; M3t tapa bolsillo s / M3s riel +X 1.6 mm³; M3t tapa bolsillo s / M3s riel -X 1.6 mm³.
Los M4 del pie cruzan el conducto 4.8 mm por encima del Cat5e.

## 5. Verificacion a mano (150 N de manipulacion en una capsula)

- **Riel apoyado en los ganchos (en el agua, caso normal):** voladizo desde el gancho, M = F·(x_capsula − 100) = 19619 N·mm. Seccion del tubo en x = 129 (corte del CAD): A = 412 mm², I = 46051 mm⁴, c = 15.3. σ = 6.5 MPa → FS 6.9 (45, flexion a lo largo de las capas) / 3.4 (22). Flecha de la capsula ≈ 1.4 mm.
- **Union plana sin contar la caja:** el gancho del otro lado tira hacia abajo (correa) y en x = 0 queda M = 9809 N·mm con traccion arriba. Brazo de los M3 al fondo del riel 39.9: T = 246 N, 61 N por M3 → 12 MPa en el acero (A2-70 del orden de 450) y 3.6 MPa bajo la tuerca en el PETG. La caja, atornillada a las dos mitades con 4 M4, hace de puente: en la realidad la union carga menos.
- **Izado por el asa fuera del agua (150 N en una capsula):** traccion por inserto M4 del fondo de la caja **254 N** (la modular pedia 251 en Ø200): se prueba con PB8.
- **Gancho M9s con 75 N:** C como viga curva, M = F·r/2 = 240 N·mm sobre 12 × 4: σ = 7.5 MPa → FS 6.0 (se imprime de costado, carga en el plano de las capas). Tuerca M4 contra los labios de la ranura T: 2.2 MPa. La correa solo toma el levantamiento.
- **Pie de la capsula:** M = 15810 N·mm desde el frente de la capsula al centro de la silla; con 2 M4 a 30 la mayor fuerza por perno es 602 N y aplasta las 2 paredes del riel (Ø4.2 × 4) a 17.9 MPa → FS 2.5 (45) / **1.2** (22: el riel se imprime con la brida abajo y la carga del perno va a traves de las capas). El alma del pie no se calculo: conviene llevar M5s a SimScale o probarla con la mano antes del agua.

## 6. Cable

Por camara: 60 + 25 + riel 198 + bucle 77 + 30 + 30 = **420 mm** (requiere prueba SPI a 8 y 4 MHz).

## 7. Chequeos que fallaron

- ninguno

## 8. Constantes de modulo

- `SLOT_MARGIN` = 2: aire en x entre la silla del pie y la ranura de salida del cable.
- Tiempo de `simple.py`: 34 s.
