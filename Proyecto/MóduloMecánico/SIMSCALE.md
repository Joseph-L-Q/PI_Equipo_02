# SimScale: casos para comparar con la verificación a mano (Fase F)

Los STEP salen de `cad_final/simscale.py` (se regeneran con `python simscale.py` desde `cad_final/`) y quedan en `salida/simscale/`. Los números "a mano" se copian de `cad_final/reporte_verificacion.md` sin recalcular. **Este documento no trae resultados de simulación: los corre el usuario en SimScale y los compara con la columna "Resultado a mano".**

## Material y reglas comunes

| Dato | Valor |
|---|---|
| PETG (manual, estimado) | E 1700 MPa, ν 0.38, ρ 1270 kg/m³ |
| σy a lo largo de las capas | 45 MPa |
| σ entre capas (tracción perpendicular a las capas) | 22 MPa |
| Pasador M4 del caso 4 (acero, valor típico, no sale de `params.py`) | E 200000 MPa, ν 0.3 |
| Acrílico de la ventana (caso 4, dato típico no medido) | E 3000 MPa, ν 0.37 |

- Análisis lineal estático, pequeños desplazamientos. Elementos tetraédricos de segundo orden. Mínimo 2 elementos a través de cada pared de 3 o 4 mm.
- FS a mano = σ admisible / σ calculada. Cuando el esfuerzo principal máximo de SimScale cae **en el plano de las capas** se compara con 45; cuando es tracción **a través de las capas** (σ perpendicular a la capa) se compara con 22. La orientación de impresión de cada pieza está en su caso.
- Un STEP con varios cuerpos trae **sólidos separados**: hay que definir los contactos. "Unido" (bonded) da la rigidez de una pieza monolítica, que es lo que supone la mano; "contacto" (sin fricción o con fricción μ 0.3, estimado) muestra si una unión se abre.
- Todos los sólidos pasaron `checks.brep_check` (BRep válido, BOP sin fallas, 1 sólido por pieza, arista mínima ≥ 0.05 mm, cara mínima ≥ 0.01 mm²) y se releyeron del STEP con el mismo volumen.

| Archivo | Cuerpos | Marco de coordenadas |
|---|---|---|
| `simscale_1_union_riel.step` | `riel_central_x10a70`, `riel_ext`, `varilla_M8_acero` | Marco de la caja: X a lo largo del riel, Z arriba, fondo exterior de la caja en z = 0. Fondo del riel en z_rail = -69.75; el riel ocupa z de -69.75 a -39.75 (sección 30). Eje de la varilla en y = 0, z = -55.70. |
| `simscale_2_gancho.step` | `gancho` | Marco del gancho: cara inferior del riel (= cara superior de la brida) en z = 0; eje de la varilla en x = 0, z = -40. |
| `simscale_3_caja_tapa.step` | `caja_cuerpo`, `caja_tapa` | Marco de la caja: centrada en x = y = 0, fondo en z = 0, tapa de z = 50 a 113 (con el asa). |
| `simscale_4_carro_capsula.step` | `carro`, `cap_cuerpo_M4`, `cap_tapa_M5`, `cap_bisel_M6`, `cap_ventana_M7`, `pasador_M4_acero` | Marco del carro: fondo del riel en z = 0, manga de x = -60 a 0, eje de la bisagra en x = 12.5, z = -34, cápsula a 0 grados (eje óptico +X). |

---

## Caso 1: unión de tramos (media madera + cola de milano + varilla M8)

**Geometría (decisión del 29/10, C18 y C19).** Central recortado a su tramo exterior (x de 10 a 70) y una extensión de 115 colocada como en `riel.main()` y `ensambles.py` (macho interior en x = 55, extremo en x = 170). Zona de la media madera: x de 55 a 70. La varilla M8 (Ø8 de acero, sin rosca) va de x = 10 a 170 por los agujeros de Ø8.5 de los tabiques (central: x de 51.9 a 54.9; extensión: x de 70 a 73 y de 152 a 155).

**Simplificado.** Sólo el recorte del central en x = 10 (se quita el resto de la cámara, que no influye en la unión). No se quitó ningún detalle de la unión: los 2 M4 (agujero de paso, avellanado y bolsa hexagonal), la ranura T con sus nervios y los tabiques de la varilla se conservan. Roscas: no existen en el CAD. Arista mínima del central: 0.10 mm (pide malla local). **Los tornillos M4 no están modelados** (los agujeros quedan vacíos).

**Apoyo.** Cara plana de corte del central en x = 10 (todo el contorno, incluida la brida) y la cara x = 10 de la varilla, empotradas. Es más rígido que la realidad: el riel entra a la caja por 4 M4 de la brida de la cámara.

**Carga.** Fuerza remota (acoplamiento rígido) a la cara de extremo de la extensión (x = 170) **y** a la cara x = 170 de la varilla (en el nodo real la varilla sigue hasta la tuerca de la punta, más allá de la unión), de 150 N hacia abajo (−Z), aplicada en el punto (327.5, 0, −103.75): eje de la bisagra con el carro a ras de la punta de Ø500 (punta en 315). Momento en la unión M = 150·(327.5 − 70) = **38625 N·mm**. Segunda corrida con la carga hacia arriba (+Z).

**Contactos.**
- Corrida 1 (comparar con la mano sin varilla): varilla suprimida, todas las caras de contacto unidas (bonded).
- Corrida 2 (la que importa): contacto con fricción μ 0.3 (estimado) en el plano de la media madera (z = −54.75, x de 55 a 70), en las caras de la cola de milano (llave 8 × 11 × 4) y en las caras de tope x = 55 (macho contra el hombro del central) y x = 70. Varilla sin contacto con los agujeros (pasa suelta). Precarga de la varilla: 500 N (en SimScale, como precarga de perno en el cuerpo de la varilla o deformación térmica equivalente); si no se puede, correr sin precarga: cambia poco el resultado con la unión abierta.

**Malla sugerida.** Global 4 mm. Refinar a 1.5 mm en toda la media madera (x de 55 a 70) de las dos piezas, en la llave y en las caras de tope. Varilla: 2 mm.

**Material y orientación de impresión.** PETG manual; varilla de acero E 200000 MPa, ν 0.3. Central: brida abajo (giro X 180), capas perpendiculares a Z. Extensión: acostada sobre una cara lateral (giro X 90), capas perpendiculares a Y. La flexión y la compresión de tope van **en el plano de las capas**: aplica 45 MPa.

**Resultado a mano (`reporte_verificacion.md` §3, §3b, §3c).**

| Magnitud | Mano |
|---|---|
| σ en la media madera sin varilla, M/Z_mitad (697 mm³) | **55.4 MPa**, FS 0.8 (45) |
| Tracción en la varilla, M / brazo (12.05) | **3205 N**, σ 88 MPa en el área resistente de 36.6 mm² |
| Compresión en la cara de tope x = 55, sólo pared del fondo (102 mm²) | **31.5 MPa**, FS 1.4 |
| Rotura con bloque uniforme a 45 MPa | M_u 78565 N·mm, FS 2.0 |
| Carga hacia arriba: tracción en la varilla / compresión en la pared de arriba | 2769 N / 23.1 MPa |

Comparar en SimScale (corrida 2): fuerza axial en la varilla contra 3205 N, presión de contacto en la cara de tope x = 55 contra 31.5 MPa, y abertura de la unión en x = 70 arriba. La mano ignora la concentración en los hombros, así que SimScale puede dar más.

---

## Caso 2: gancho con 75 N

**Geometría.** `gancho.gancho()`: brida de 50 × 30 × 6 (x de -47 a 3, z de -6 a 0), agujero M4 de paso en x = -30, alma de 12 × 12 de x = -12 a 0 y mandíbula en J con asiento de Ø16 centrado en x = 0, z = -40 (boca hacia +X).

**Simplificado.** Se quitó la cresta de traba del pestillo (resalte de 0.6 mm, `LATCH_BUMP`). Se conservan el agujero del eje del pestillo (M3) y la ranura del pestillo (no se exporta el pestillo, la perilla ni el casquillo). Los redondeos son de R3, mayores que 1 mm. La cara superior de la brida está **dividida** en una franja de 3 mm en el extremo del lado de la perilla (x de -47 a -44), para poder apoyar sólo ahí.

**Apoyos** (reproducen el modelo de la mano: el riel sólo empuja en el extremo de la brida y el M4 toma la suma):
1. Cara cilíndrica del agujero M4 de la brida (x = -30): soporte fijo. Es el perno, que toma F + R.
2. Franja de la cara superior de la brida, x de -47 a -44: soporte sin fricción (sólo desplazamiento normal restringido). Es el apoyo contra el fondo del riel. El resto de la cara superior queda libre.

**Carga.** 75 N, dirección -Z (la varilla empuja hacia abajo, fuera del riel; es el sentido que reproduce la reacción "perno = F + R" de la mano), sobre la mitad inferior de la cara cilíndrica del asiento de Ø16 (centro x = 0, z = -40). Si SimScale ofrece carga de apoyo (bearing), usarla; si no, fuerza distribuida sobre esa mitad.

**Contactos.** Una sola pieza: ninguno.

**Malla sugerida.** Global 3 mm. Refinar a 1.5 mm en el alma (12 × 12, x de -12 a 0, donde se unen brida y mandíbula), en la cara del asiento de Ø16, alrededor del agujero M4 y en el borde de apoyo de la brida (x de -47 a -44).

**Material y orientación de impresión.** PETG manual. El gancho se imprime de costado (giro X 90): capas perpendiculares a Y, de modo que la carga vertical queda **en el plano de las capas** y aplica 45 MPa. La tracción y el aplastamiento a través de las capas aparecerían en Y (poco esperable aquí).

**Resultado a mano (§5).**
- Alma: σ = F/A + F·e/Z = **2.1 MPa**, FS 21.6 (45).
- Reacción en el extremo de la brida R = **106 N**; fuerza en el perno M4 = **181 N** (esta es la reacción del soporte 1; la del soporte 2 debe dar 106 N).
- Brida en el perno: M = 1800 N·mm, σ = **11.6 MPa**, FS 3.9 / 1.9.
- Tuerca contra los labios de la ranura T: σ = 10.8 MPa (no se modela aquí: la tuerca no está en el STEP).
- Asiento recto: flecha de la curva del aro sobre 12 mm de contacto, 0.36 mm (Ø100) a 0.07 mm (Ø500): geometría, no de la simulación.

---

## Caso 3: caja y tapa, asa con 150 N de izado

**Geometría.** `box_body` (x e y de ±79.82 y ±63, altura 50 con brida y falda) y `box_lid` (5 mm de tapa, asa con puente de 12 × 10 de sección y ojal anclado).

**Simplificado.** Se quitaron la ranura de junta tórica de la tapa (1.5 × 2.6 mm) y los postes de bandeja con sus insertos M3. Se conservan: los 10 agujeros M3 de la tapa y los 10 agujeros de inserto M3 de la brida de la caja (puntos de apoyo), los 4 refuerzos con insertos M4 del fondo (±40, ±20), los pasacables PG7 y todos los redondeos (R3 a R6).

**Apoyo (caso 3A, el que compara con la mano).** Las 10 caras cilíndricas de los agujeros M3 de la tapa: soporte fijo (supone que **sólo los tornillos llevan el izado**, como en la mano). Se puede correr la tapa sola, desactivando el cuerpo de la caja.

**Carga.** 150 N en +Z (izado), repartida sobre la cara inferior del techo de la ventana del asa (plana, z = 87, |x| ≤ 19.8, 12 mm de ancho en y) y sobre las dos rampas a 45° contiguas. Son las caras donde la mano agarra el puente.

**Contactos.** Si se corre la caja con la tapa: tapa contra brida en contacto sin fricción (se separa al tirar); los tornillos no existen, así que el modelo con la caja sólo sirve con apoyo en los agujeros de la tapa. Por eso el caso 3A es la tapa sola.

**Caso opcional 3B (presión a 1 m, 0.0101 MPa, §8).** Presión de 0.0101 MPa hacia adentro sobre la cara exterior de la tapa, del fondo y de las paredes; apoyo: tapa descansando en la brida (contacto sin fricción) y caja apoyada por las 4 caras de los insertos M4 del fondo. Es otro cálculo, aparte del izado.

**Malla sugerida.** Global 5 mm. Refinar a 2 mm en las dos patas del asa, el puente y sus redondeos R3, y alrededor de cada agujero M3 de la tapa. En la brida y paredes de 4 mm usar 2 elementos de espesor como mínimo.

**Material y orientación de impresión.** PETG manual. Tapa: cara interior en la cama, asa arriba (capas perpendiculares a Z). El puente flexa en el plano de las capas (aplica 45 MPa); las patas del asa trabajan en tracción a través de las capas en Z (aplica 22 MPa). Caja: boca arriba, fondo en la cama.

**Resultado a mano (§6; §8 para el caso 3B).**
- Barra del asa, viga apoyada de 90, sección 12 × 10: M = 3375 N·mm, σ = **16.9 MPa**, FS 2.7 (45).
- Patas del asa, tracción a través de las capas: **0.52 MPa**, FS 42 (22).
- 10 tornillos M3: **15.0 N por inserto** (reacción de cada agujero fijo), sin la reacción de la junta tórica (no está en el modelo).
- Caso 3B (placas simplemente apoyadas, Roark): tapa 1.67 MPa y flecha 0.317 mm; fondo 2.60 MPa y 0.619 mm; pared larga 0.93 MPa y 0.054 mm; pared corta 0.83 MPa y 0.047 mm.

---

## Caso 4: carro y cápsula, bisagra con 150 N en el frente

**Geometría.** Carro `capsula.carriage()` (manga abierta en ambos extremos, quilla y orejas de la bisagra), la cápsula en cuatro piezas (cuerpo M4, tapa M5 con la lengüeta, bisel M6, ventana M7) a 0 grados con `capsula.place_capsule(shape, 0)`, y un pasador M4 de acero (cilindro liso de Ø4, 18.4 mm de largo, a lo largo de Y por el eje de la bisagra en x = 12.5, z = -34). El pasador no es una pieza impresa: se agregó para medir el aplastamiento en las orejas y en la lengüeta, que la mano calcula.

**Simplificado.**
- Dientes de la bisagra (1.2 mm): reemplazados por anillos planos de 0.6 mm (radio 7 a 12) en la lengüeta y en cada oreja. Quedan en contacto cara con cara en y = ±3.6, así que la lengüeta (grueso 6 + 2 × 0.6 = 7.2) llena el hueco entre orejas con 0.6 mm de anillo por cada pieza.
- Sin pilotos M2 del bisel (4, ciegos) ni agujeros de 2.4 mm del bisel.
- Sin ranura de junta tórica en la tapa de la cápsula.
- No se quitaron: los 4 agujeros M3 de la brida de la cápsula y de la tapa, el pasacable PG7, el asiento y la apertura de la ventana, el tubo separador del LED con sus rayos (puede suprimirse en SimScale si agrega malla), los redondeos (R2 a R4).
- Roscas y herrajes: no existen en el CAD.

**Apoyo.** Las caras interiores de la manga del carro que abrazan el riel: soporte fijo en la cara plana superior e inferior del paso del riel (z = -0.3 y z = 30.3) y en las caras laterales (|y| = 15.3). Esto equivale a un carro apretado sobre el riel con la perilla; no se modela el riel.

**Carga.** 150 N en Z (sentido a elegir, correr los dos) como fuerza remota (rígida) aplicada en (77.5, 0, -34) y acoplada a la cara frontal exterior del cuerpo M4 (x = 77.5). Brazo respecto del eje de la bisagra: 77.5 - 12.5 = **65 mm**, par T = 150 × 65 = 9750 N·mm.

**Contactos.**
- Lengüeta (tapa M5) contra orejas del carro: anillos planos en y = ±3.6. Corrida 1: unidos. Corrida 2: contacto con fricción μ 0.3 (estimado) y precarga axial del pasador de **166 N** (la mínima de la mano); sin precarga la lengüeta gira y no es comparable.
- Pasador contra los agujeros de las orejas y la lengüeta (agujero Ø4.2, pasador Ø4): contacto sin fricción, o unido a las orejas y libre en la lengüeta.
- Cuerpo M4 y tapa M5 (cara de brida en x = 33.5): unidos. Bisel M6 y ventana M7 contra el cuerpo: unidos.

**Malla sugerida.** Global 3 mm. Refinar a 1.5 mm en las orejas y la lengüeta (todo el disco de Ø24), en los agujeros del pasador y en la raíz de las orejas sobre la quilla. En la manga, 2 elementos por la pared de 4 mm.

**Material y orientación de impresión.** PETG manual para carro, cuerpo y tapa; acero para el pasador; acrílico para la ventana. Carro: giro Y -90 (sale parado, el eje X del riel queda vertical en la cama, capas perpendiculares a X). Cuerpo M4: giro Y -90. Tapa M5: giro X -90 (capas perpendiculares a Y, con la lengüeta en el plano de las capas). La carga de la lengüeta va en el plano de las capas (45); la de las orejas del carro depende de cómo caigan las capas: verificar contra 22.

**Resultado a mano (§7).**
- Peso de la cápsula con contenido en aire 128 g, par T = 54 N·mm (casi neutra en el agua).
- Precarga axial para no saltar un diente contra 150 N en el frente (palanca 65): N ≥ **166 N**, que un M4 da con unos 0.13 N·m de apriete.
- Aplastamiento del M4 con 150 N: **en las orejas 3.8 MPa** (2 × 4 × 5), **en la lengüeta 6.2 MPa** (4 × 6.0). FS > 4 aun entre capas.
- Comparar la presión de contacto en el pasador contra esas dos cifras.

El modelo con anillos planos no reproduce el engrane de los dientes: el resultado de la corrida 1 (unido) da la distribución de cargas sin el salto de diente, y la corrida 2 comprueba el deslizamiento con la precarga de la mano.

---

## Constantes agregadas en `simscale.py` (no están en `params.py`)

- `CENTRAL_X0` = 10 mm: x donde se corta el central.
- `PIN_D` = 4.0 mm: diámetro del pasador M4 liso del caso 4.
- `HOOK_PAD_W` = 3.0 mm: ancho de la franja de apoyo de la brida del gancho.
- Valores de material del pasador de acero y de la ventana de acrílico (arriba): típicos, sin respaldo en el proyecto.
