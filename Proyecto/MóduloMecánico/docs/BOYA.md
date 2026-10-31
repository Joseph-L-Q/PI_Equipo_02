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

## Pendiente de medir o confirmar

- Dimensiones reales de las botellas (cuerpo, largo, cuello, hombro) y su volumen: están como "estimado" en `flotacion.botellas`. Con otra marca cambia la ranura del cuello y la longitud de las cunas.
- Masa real de los componentes, sobre todo el panel (350 g estimado) y las botellas vacías (25 g estimado): es lo que más mueve el KG y la escora con una botella perdida.
- Cuánto llena de verdad la espuma PU (`flotacion.espuma_llenado = 0.5` es un supuesto): de eso depende toda la columna "con espuma estimada".
- Resistencia de las lenguetas de las cunas y de los postes (sin FEM) y del parche de amarre.
- El criterio de "escora pequeña" (10 grados) es propio, no del dueño.
- Hidrostática de formas simples: sin oleaje, viento ni tensión del umbilical; no es una certificación.
- Si el umbilical con el PG7 a 30 mm del piso interior se puede tender dentro de la caja sin chocar con el portabaterías (la reserva de 14 mm junto a la pared -X lo permite en el modelo, sin comprobar con el cable real).
