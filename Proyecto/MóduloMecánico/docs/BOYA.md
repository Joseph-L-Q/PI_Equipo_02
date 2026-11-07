# Boya con botellas PET (bloque C)

La flotación la dan **botellas PET selladas** (más espuma PU como reserva) y el PETG impreso solo hace de estructura. Reemplaza a la boya de plataforma `boya_simple.py`. Todo sale de `cad_final/boya_pet.py` y de los parámetros `flotacion.*` y `boya_pet.*` de `cad_final/params.py`.

Regenerar: `python boya_pet.py` desde `cad_final/` (CAD, chequeos, OrcaSlicer, flotación). Por parámetro (o por bandera de línea de comandos):

- `flotacion.botella = "500ml" | "1L" | "2L"` (`--botella`)
- `flotacion.cantidad = 4 | 2` (`--cantidad`): **4 = disposición en cruz (segunda vuelta, por defecto)**, 2 = fila (primera vuelta, sigue disponible).
- `--salida DIR` escribe en otra carpeta; `--limpiar-stl` borra STL y STEP al terminar; `--alternativas` modela también las otras botellas (sin laminar).

Resultados: `salida/boya_pet/` es la configuración por defecto (`resultados.json`, `slicer.json`, `step/`, `stl/`, `boya_pet_iso.png`, `boya_pet_corte.png`, `ENSAMBLE_boya_pet.step`). Las dos configuraciones que se comparan están en `salida/boya_pet/config_4x500ml/` y `salida/boya_pet/config_2x1L/` (solo JSON, imágenes y el ensamble).

## Recomendación (cerrada)

**4 botellas de 1 L en cruz** (`flotacion.botella = "1L"`, `flotacion.cantidad = 4`), que es lo que genera la compilación por defecto. Es la única de las tres que cumple los dos GM objetivo con holgura grande (112 / 762 mm contra 40), tiene reserva de 136 % y francobordo de 82 mm, y la única que, perdiendo una botella, sigue a flote y estable (con la espuma estimada). Cuesta más material y es más grande que la de 500 ml. Para pruebas en piscina sobra margen; si se prioriza el tamaño y el costo, la de 4 x 500 ml en cruz también cumple el GM (56 / 242) pero **vuelca si se pierde una botella**.

Qué objetivo falla y por cuánto, en la recomendada:

| Objetivo | Resultado | Falla por |
|---|---|---|
| GM balanceo y cabeceo >= 40 mm | 112 / 762 mm | cumple |
| Francobordo a la abertura más baja de la caja >= 50 mm | 82.0 mm | cumple |
| Con una botella perdida: flota derecha, GM > 0, escora pequeña (criterio propio: <= 10 grados), abertura sobre el agua | **sin espuma: no se encontró actitud estable (vuelca)**; con la espuma estimada: escora de 6 a 12 grados según la botella perdida, GM 89 a 104 mm de balanceo, abertura 69 a 84 mm sobre el agua | sin espuma no cumple; con espuma cumple el GM y la abertura y se pasa 2 grados de escora en el peor caso (botella longitudinal perdida) |
| Masa impresa <= 700 g | 863 g | 163 g |
| Tiempo de impresión <= 25 h | 32.0 h | 7.0 h |

La masa y el tiempo se pasan por el tamaño del conjunto (cruz de 474 mm de largo); no se subieron los objetivos para que pasen. Todo lo de espuma es **estimado** (llenado de 50 % de los huecos, celda cerrada, 30 kg/m3).

## Cómo se llegó a la cruz

Con 4 botellas de 500 ml no hay disposición con GM >= 40 en ambos ejes dentro de un casco de 254 x 226 de una pieza. Cálculo hidrostático con masas aproximadas (estimado, antes de modelar), botellas de 500 ml, caja y panel sobre la cubierta:

| Disposición (4 x 500 ml) | GM balanceo / cabeceo (mm) | Por qué |
|---|---|---|
| Dos pisos de 2 (2 por lado, apiladas) | -17 / -71 | solo el piso alto toca el agua; calado 101 mm, KG 159 mm |
| De pie en las cuatro esquinas | -78 / -60 | calado 159 mm: KG 226 mm |
| Tres filas + una encima | -84 / -94 | el piso alto queda seco, KG 159 mm |
| Cuatro en fila a lo largo de Y | -15 / 84 | no cabe en 254 (4 x 68 = 272) y el balanceo solo tiene la inercia propia de la botella |
| Rejilla de dos pisos | -71 / 18 | calado 101 mm |
| Molino de viento (las cuatro en el mismo plano, cuellos entrelazados) | 42 / 74 | **no cabe**: necesita unos 275 x 275 (largo de botella + diámetro) |
| **Cruz**: 2 a lo largo de X en el casco + 2 a lo largo de Y en cunas en los extremos | 63 / 257 | cabe con un casco central de 218 x 253 y dos cunas |

Las cuatro botellas tienen que estar en el mismo plano para que la inercia de la línea de flotación sea grande y el calado bajo; el único plano que las admite es la cruz, que supera los 254 mm, por eso el casco se parte en el casco central y dos cunas atornilladas. El casco central de 500 ml se imprime con el lado largo en Y (218 x 253, corrido fuera de la esquina excluida de 18 x 28 mm); el de 1 L, 254 x 225.6.

## Qué es

- **B1 casco central**: dos bahías con botellas a lo largo de X y cuellos opuestos (simetría C2), cinco costillas por bahía con ranuras en U, paredes laterales exteriores solo hasta poco sobre el eje de la botella, parche de amarre en el centro de la quilla, 8 postes M3 para la cubierta y 2 o 4 agujeros de paso M3 por extremo para las cunas. El canal central queda **abierto por el fondo**: el umbilical baja del PG7 de la caja directamente al agua (paso de cable).
- **B5 cuna** (x2, la misma pieza para ambos extremos): una bahía con la botella a lo largo de Y, dos paredes, cinco costillas, lenguetas con inserto M3 que se atornillan a las costillas extremas de B1 (el tornillo entra desde la bahía del casco, a nivel del piso), 4 postes para las correas.
- **B6 correa** (x4): cierra cada cuna sobre la botella (dos por cuna, M3 en los postes).
- **B2 cubierta** (solo sobre el casco central): barras, 4 pilares bajo las orejas de la caja, **4 columnas del panel** (panel de 170 x 170, 25 mm sobre la tapa, columnas a y = +-77 para que queden bajo el panel), mástil de antena.
- **B3 caja seca** y **B4 tapa**: sin cambios de diseño, salvo que el PG7 del umbilical sube de 15 a 30 mm sobre el piso interior (`boya_pet.pg7_umbilical_z`) para cumplir el francobordo con el casco más bajo.
- Paredes de 2.4 mm con costillas, todas las piezas caben en la cama de 256 (B1 de 1 L: 254 x 225.6; B5: 254 x 114.6).

Botellas modeladas como cilindros con el **volumen nominal** (conservador); la espuma no entra en el cálculo base.

## Comparación (agua de mar 1025 kg/m3)

Las tres filas salen del mismo código (inercia de la línea de flotación respecto de su centroide). Con esta corrección el cabeceo de la fila de 2 x 1 L pasa de 15.5 a 12.7 mm respecto del cálculo de la primera vuelta, y el francobordo de la abertura de 51.4 a 66.4 mm por el PG7 subido; las masas son las del laminador.

| | 2 x 1 L fila (1ª vuelta) | 4 x 500 ml cruz | **4 x 1 L cruz (recomendada)** |
|---|---|---|---|
| Piezas impresas | B1..B4 (4) | B1..B6 (10 con cantidades) | B1..B6 (10 con cantidades) |
| g impresos (laminador) | 624.4 | 720.5 | **863.2** |
| h de impresión | 20.87 | 26.83 | **31.96** |
| Costo (PETG a 90 S/kg) | S/ 56.20 | S/ 64.84 | **S/ 77.69** |
| Masa total de la boya | 1412 g | 1586 g | **1739 g** |
| Calado | 55.1 mm | 50.0 mm | **39.5 mm** |
| Francobordo (abertura de la caja) | 66.4 mm | 56.5 mm | **82.0 mm** |
| Reserva (empuje de botellas - masa) | 638 g (45 %) | 464 g (29 %) | **2361 g (136 %)** |
| GM balanceo / cabeceo | 30.6 / 12.7 mm | 55.6 / 242 mm | **112 / 762 mm** |
| Con una botella perdida, sin espuma | vuelca | vuelca | vuelca (sin actitud estable) |
| Con una botella perdida, con espuma estimada | vuelca | vuelca | **estable, escora 6 a 12 grados** |
| Dimensión mayor | 254 x 226 | 380 x 253 | 474 x 254 |

Piezas de la recomendada (laminador, PETG, 0.2 mm, 3 paredes, giroide al 40 %):

| Pieza | Cant. | Orientación | Soportes | g | h | Costo (S/) |
|---|---|---|---|---|---|---|
| B1 casco central | 1 | sin girar | **sí** (voladizo 331 mm2, apenas sobre el umbral de 300) | 213.6 | 7.38 | 19.23 |
| B2 cubierta | 1 | sin girar | no | 119.0 | 5.80 | 10.71 |
| B3 caja seca | 1 | sin girar | no | 171.0 | 5.46 | 15.39 |
| B4 tapa | 1 | X180 | no | 57.2 | 2.10 | 5.15 |
| B5 cuna | 2 | sin girar | **sí** (voladizo 342 mm2) | 141.0 | 5.01 | 12.69 |
| B6 correa | 4 | sin girar | no | 5.1 | 0.30 | 0.46 |
| **Total** | 10 | | | **863.2** | **31.96** | **77.69** |

Si se quisiera evitar los soportes de B1 y B5, el voladizo sale de la ranura del cuello (circular en una placa vertical); queda como mejora.

### Si se pierde una botella

Se probó cada botella por separado y se buscó la actitud (escora y cabeceo) en la que el centro de empuje queda bajo el de gravedad, con GM numérico en esa actitud y la altura de la abertura más baja de la caja (volúmenes muestreados, resolución de unos 1.5 mm en la línea de agua: sirve para ángulos, no para décimas de grado). Las botellas de 500 ml y la fila vuelcan en todos los casos, aun con espuma estimada. Las de 1 L en cruz sin espuma no tienen actitud estable; con la espuma estimada (919 g de reserva adicional estimada) quedan estables con escora de 12 grados al perder una botella del casco y de 6 al perder una de cuna, con la abertura a 69 mm o más sobre el agua. Es un resultado de formas simples, no una prueba.

## Flotación de la recomendada

| Magnitud | Valor |
|---|---|
| Masa total (impreso 863 g + componentes + 4 botellas vacías 100 g + espuma) | 1739 g |
| Empuje máximo de las botellas (4 x 1 L) | 4100 g |
| Calado | 39.5 mm |
| Francobordo a la abertura más baja de la caja (borde del PG7 del umbilical) | 82.0 mm (mínimo 50) |
| KG | 109.0 mm |
| GM balanceo / cabeceo | 112 / 762 mm |

Verificación independiente: el equilibrio 3D muestreado reproduce el GM analítico en posición recta (por ejemplo 42 contra 43 mm en la de 500 ml).

## Material

PETG alcanza para una piscina; si la boya va a estar semanas al sol, imprimir en ASA. Hay que confirmar con la boleta el precio de 90 soles/kg.

## 04/11/2026: piezas en mitades (cama útil 230) y topes bajos

**Qué cambió.** B1, B2 y B5 medían 254 mm de largo. OrcaSlicer daba error y el equipo fijó la cama útil en 230 × 230.

| Pieza | Antes | Ahora | Unión |
|---|---|---|---|
| B1 casco | 1 pieza, 254 × 226 | **2 mitades iguales** de 132 × 226 (un solo STL, se imprime 2 veces) | Brida de 5 + 5 mm en x = 0: 2 columnas en el canal (cada una con una **lengüeta** de 6 × 16 × 4 mm y su ranura) y 2 almohadillas bajas en las paredes, **6 tornillos M3 × 25 inox A2 con tuerca** y 2 pines Ø5 de alineación (holgura 0,2, la de PB7) |
| B2 cubierta | 1 pieza, 254 × 226 | Lado liso + lado mástil, 127 × 226 cada uno | Cada mitad es un marco cerrado (barra nueva en x = 0, con 4 **lengüetas** verticales de alineación) atornillado a sus propios 4 postes del casco. La caja y el panel atornillados encima amarran las dos mitades |
| B5 cuna (× 2) | 1 pieza, 254 × 115 | Lado base + lado cuello, 127 × 118 cada uno (× 2) | Cada mitad va atornillada al casco por su lengüeta. Entre mitades: brida 5 + 5 mm con 2 M3 en almohadillas bajas, cada una con una **lengüeta** vertical (sin pines: no caben junto a la botella) |

**El ojal de amarre** estaba justo en x = 0, donde se parte el casco. Ahora hay **2 ojales**, uno por mitad, en x = ±21: el cabo de amarre va en pata de gallo (dos ramales a un nudo). Así no se corta el punto que recibe la carga y queda redundante.

**¿Achicar en vez de partir?** No es viable sin perder flotación. El casco ya es más corto que la botella (270 mm, el cuello sobresale 21). Para bajar de 230 de largo habría que pasar a botellas de 500 ml, y con 4 × 500 ml la boya **vuelca al perder una botella** (ver la comparación de arriba). El ancho de 225,6 queda 4,4 mm bajo 230 y no se reduce, porque de él depende el GM de balanceo. Partir es la opción por defecto.

**Soportes delgados (pregunta de la profesora).** Las costillas intermedias seguían por encima del eje de la botella como varillas de 2,4 × 3 mm y 41 mm de alto, en el lado del canal. Por encima del eje la botella se angosta, así que esas varillas no la tocan ni la sujetan. Lo que retiene a la botella hacia arriba, la única carga real en el agua, son las barras de B2 en el casco y las correas B6 en las cunas, atornilladas a los postes. Por eso **se eliminaron**:
- las costillas intermedias quedan como sillas bajas de 4 mm, a ≤ 15 mm sobre el patín, con chaflán de 45° en la unión con el patín;
- los postes de tornillo pasan de Ø8 a Ø10 y llevan un collar a 45° donde salen de la silla;
- los postes de las correas también pasan a Ø10 y se corren 1 mm hacia afuera para no tocar la botella.

Interruptores: `boya_pet.partir` y `boya_pet.topes_bajos` (`params.py`).

| Resultado (slicer, agua de mar) | Antes | Ahora |
|---|---|---|
| Impreso | 864 g, 32,1 h, S/ 77,8 | **958 g, 39,6 h, S/ 86,3** |
| Masa total con botellas y electrónica | 1740 g | 1834 g |
| Calado | 39,5 mm | 40,8 mm |
| Francobordo a la abertura más baja (PG7) | 82,0 mm | 80,7 mm (≥ 50) |
| GM balanceo / cabeceo | 112 / 762 mm | 107 / 733 mm |
| Reserva de flotación | 136 % | 124 % |
| Con una botella perdida | sin espuma vuelca; con espuma 12 a 13° | igual (sin espuma vuelca; con espuma 13°) |

Tornillería nueva: 8 M3 × 20 inox A2 con tuerca y arandela (6 en el casco, 1 por cada unión de cuna) y 2 pines impresos.

## Pendiente de medir o confirmar

- Dimensiones reales de las botellas (cuerpo, largo, cuello, hombro) y su volumen: están como "estimado" en `flotacion.botellas`. Con otra marca cambia la ranura del cuello y la longitud de las cunas.
- Masa real de los componentes, sobre todo el panel (350 g estimado) y las botellas vacías (25 g estimado): es lo que más mueve el KG y la escora con una botella perdida.
- Cuánto llena de verdad la espuma PU (`flotacion.espuma_llenado = 0.5` es un supuesto): de eso depende toda la columna "con espuma estimada".
- Resistencia de las lenguetas de las cunas y de los postes (sin FEM) y del parche de amarre.
- El criterio de "escora pequeña" (10 grados) es propio, no del dueño.
- Hidrostática de formas simples: sin oleaje, viento ni tensión del umbilical; no es una certificación.
- Si el umbilical con el PG7 a 30 mm del piso interior se puede tender dentro de la caja sin chocar con el portabaterías (la reserva de 14 mm junto a la pared -X lo permite en el modelo, sin comprobar con el cable real).

## 05/11/2026: panel que aguanta golpes, espuma obligatoria y lo que aguanta en el mar

**Panel lateral (golpe de 200 N de lado).** Antes las capas de la cubierta aguantaban 0.41 veces el golpe (había que llegar a 3). Se probó en orden y se acumuló lo que hacía falta:

| Paso (se suma al anterior) | Qué es | Resultado |
|---|---|---|
| Partida | panel a 25 mm, columnas Ø12 | 0.41 entre capas (0.54 en general) |
| a. | panel a 15 mm sobre la tapa (`boya_pet.panel_elevacion`) | 0.46 |
| b. | columnas de Ø14 con chaflán de 3 mm (`boya_pet.columna_D`) | 0.52 |
| c. | 4 tirantes impresos de 10 mm (`boya_pet.tirante`) | 0.53 |
| d. | marco de 14 x 12 mm bajo el panel (`boya_pet.marco_panel`) | 0.75 |
| e. | barras altas de 20 x 20 mm en las dos líneas de tornillos y en el extremo (`boya_pet.barra_cruz`), pilares de 1 mm | **3.05 (lisa) y 3.13 (mástil) entre capas; 2.7 en el plano 6.2; flecha 2.2 mm** |

Lo que se rompía no eran las columnas sino las barras de la cubierta, que se doblaban sobre las dos líneas de tornillos; por eso hizo falta subirles la altura. Cada mitad de B2 pasa de 93 g a 214 g (lisa) y de 117 g a 236 g (mástil). El panel libra la tapa B4 y el mástil de la antena. Ola vertical de 200 N sobre la cubierta: 3.7 entre capas. Para volver atrás, cada paso es un valor de `params.py` (poner `0` en tirante o marco, 25 en elevación, 12 en columna).

**Espuma de poliuretano: obligatoria.** `flotacion.relleno = "espuma_PU"` queda fijo. La espuma (30 kg/m3) rellena todos los huecos entre botellas, ranuras y bahías (unos 1.8 litros, 54 g) y entra por las ventanas hexagonales y por los huecos entre barras. Sin espuma la boya vuelca si se pierde una botella. Se calcula con el volumen de huecos al 100 % (`flotacion.espuma_llenado = 1.0`); el supuesto viejo de 50 % se sigue calculando como control.

| Una botella perdida, peor caso | GM balanceo / cabeceo (mm) | Escora | Abertura sobre el agua |
|---|---|---|---|
| Sin espuma | negativo: vuelca | 68° | bajo el agua |
| Espuma en todos los huecos (obligatoria) | **85 / 506** (objetivo 40) | 11.6° (criterio propio 10°) | 87 mm |
| Espuma solo al 50 % (control) | -49 / -116: **vuelca** | 68° | bajo el agua |

Con la espuma llena el GM pasa con holgura (antes 38 en el peor caso) y la boya queda estable, pero la escora de 11.6° pasa 1.6° del criterio propio. **Falla abierta:** si la espuma llena solo la mitad de los huecos, con la cubierta más pesada la boya vuelca al perder una botella; no se encontró reserva que lo arregle (ver la quinta botella más abajo). Por eso al armar hay que comprobar que la espuma llene bien (pesar el spray usado: unos 55 g).

**Armado de la espuma (paso nuevo).** Después de atornillar casco, cunas y correas con las 4 botellas ya selladas y antes de cerrar la cubierta B2: (1) agitar el spray 1 minuto, (2) inyectar por las ventanas hexagonales y por los huecos entre barras, de abajo hacia arriba, en capas finas, (3) esperar 30 minutos entre capas, (4) cortar lo que sobresalga y atornillar B2. La lista de materiales incluye la lata de 750 ml (`bitacora.py`).

**Las botellas no se mueven.** Se midió cuánto se puede desplazar cada botella en cada dirección antes de chocar con una pieza impresa (máximo 2.25 mm, todas ≤ 2.3 mm):

| Botella | ±X | ±Y | +Z (arriba) | -Z (abajo) |
|---|---|---|---|---|
| 1 y 2 (en el casco) | 1.25 a 2.0 mm (costilla y hombro del cuello) | 1.25 a 1.75 mm (ranura del cuello y paredes) | 1.75 mm (barras de la cubierta B2) | 0.75 mm (patín del casco) |
| 3 y 4 (en las cunas) | 1.0 mm (paredes de la cuna) | 1.25 a 2.25 mm (cuello y base de la cuna) | 1.75 mm (correa B6) | 0.75 mm (patín de la cuna) |

**Amarre (tirón del cabo de 300 N a 45°): ahora cumple.** Se probó en orden, con el elemento local de cada mitad del casco (FS entre capas):

| Paso | Qué es | FS entre capas | g de B1 (mitad) |
|---|---|---|---|
| 0 | ojal en la quilla delgada, un ramal con los 300 N | 0.24 | 148 |
| 1 | ojal bajo el poste de la cubierta (parche 28 x 10), un ramal con 300 N | 0.71 | 145 |
| d | pata de gallo de dos ramales a 60° (cada uno 300/(2 cos 30) = 173 N) con el parche anterior | 1.2 | 145 |
| b | postes de la cubierta de Ø10 a Ø16 (`boya_pet.poste_cubierta_D`), ojal a 20 mm del poste | 2.9 | ~170 (estimado) |
| **final** | parche de 34 x 14 mm (`boya_pet.ojal`) | **3.20** (FS general 2.4, flecha 2.1 mm) | **173** (+28 en total) |

No se probó subir el ojal a las barras (a): el cabo tira desde la quilla, y un amarre alto inclinaría la boya. Tampoco hizo falta un yugo impreso (c). **Hay que hacer la pata de gallo:** dos ramales de cabo trenzado Ø6 de 350 mm con ojos cosidos (rotura mayor de 3 kN cada uno), a 60° entre sí, unidos en un anillo inox al que va el cabo de amarre. Cada ramal va a un tornillo M10 inox A2 con arandela grande y tuerca nylock en el parche de su mitad (en la lista de materiales). Si un ramal se rompe, el otro carga los 300 N completos y el margen baja a menos de la mitad. Los postes más gruesos mueven los tornillos de la cubierta de y = ±23 a ±20 mm; la cubierta se recalculó (golpe lateral 3.02 y 3.11, ola vertical 3.77 y 3.72).

**¿Una quinta botella en el canal?** No. Se probó con una botella de 1 L entera en el centro (el mejor caso posible; una de 500 ml ayuda menos): con la espuma al 50 % la peor botella perdida sigue con GM de 23 / 39 mm (hace falta 40) y 18° de escora, y además no cabe entre los postes ni deja libre el paso del umbilical. Se mantiene el diseño: **riesgo conocido** si la espuma llena solo la mitad de los huecos; comprobar al armar que se usaron al menos 55 g de espuma (pesar la lata antes y después).

**Cuánto aguanta en el mar** (cuentas en `salida/capacidad_mar.md` y `.json`). Golpe lateral en el panel: seguro hasta unos 200 N, equivalente a agua empujando a 4.4 m/s. Golpe vertical sobre la cubierta: seguro hasta 250 N (5.6 m/s). Nodo colgado del gancho con corriente de 1.5 m/s: seguro hasta unos 170 N; la corriente solo suma 2 N, el límite es el peso que cuelga. Cabo de amarre (pata de gallo): seguro hasta unos 320 N de tirón total (agua a 18 m/s sobre la cápsula).

**Resultado de impresión (laminador):** 1394 g, 60.2 h, S/ 83.66 a S/ 60 el kilo (antes 1105 g, 46.9 h). Masa total 2297 g, calado 47.4 mm, francobordo 85.1 mm, GM 72 / 577 mm.

**Cubierta B2 sin soportes (05/11, tarde).** El marco de 14 x 12 mm bajo el panel cruzaba 140 mm en el aire y obligaba a soportes (14.6 % en la lisa, 14.0 % en la del mástil). Se quitó el marco (`boya_pet.marco_panel = (0, 0)`) y las barras altas de las líneas de tornillos pasaron de 20 a 26 mm de ancho (`boya_pet.barra_cruz = (26, 20, 113, True)`). Resultado con soportes forzados: 0.1 % y 0.4 %. Resistencia: golpe lateral 3.42 y 3.47 entre capas (flecha 2.4 mm), ola vertical 4.89 y 4.79. Con 23 mm de ancho quedaba justo en 3.03, por eso 26. Para volver al marco: `marco_panel = (14, 12)` y `barra_cruz = (20, 20, 113, True)`.
