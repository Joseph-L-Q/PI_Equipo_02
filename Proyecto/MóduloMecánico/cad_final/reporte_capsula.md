# Reporte de la capsula de camara (M4..M7) y el carro M10

Generado por `capsula.py`. Base: P4 rev. B de `../cad/parts.py` con los cambios del equipo.
Salida en `../salida/preliminar/` (`stl/`, `step/`, `capsula_carro_0.png`, `capsula_carro_90.png`).

## Geometria
- Camara Arducam Mega 5MP AF 33 x 33 x 17 (antes 25 de alto). Cavidad 38 x 38 x 38 (antes 38 x 38 x 50): 17 de camara, de los cuales 14.7 quedan detras de la pared frontal, mas 23 de zona trasera (cable + contratuerca PG7).
- Anillo LED Ø30 x 3 pegado a la cara interior de la pared frontal; tubo separador opaco (pared 1.2, sobresale 3 sobre el anillo, largo total 6) alrededor del porta-lente Ø16. Apertura anular de luz Ø26 con 3 radios de 2 que sujetan el tubo.
- Bisagra de 36 dientes, eje M4 fuera del sello, PG7 en la pared inferior (a 10 de la apertura).
- M10 (modo deslizante): manga cerrada abierta en los dos extremos (holgura 0.3 por lado, pared 4, largo 60); perilla abajo, atras, con el M4 al centro de la ranura T; rendija de 10 en +Y a todo lo largo para el Cat5e; quilla con las orejas delante de la perilla y eje a x = 12.5, z = -34 (bajo el riel, la capsula a 0 grados queda 2 bajo el fondo del riel). El riel puede pasar hasta 100 mas alla de la manga, sobre la capsula.

## Piezas

| pieza | STL | BRep/BOP | estanco | cuerpos | bbox en orientacion (mm) | voladizo mm2 | espesor min p1 (mm) | masa 100 % (g) | volumen (cm3) |
|---|---|---|---|---|---|---|---|---|---|
| M4 cuerpo | M4_capsula_cuerpo.stl | ok | si | 1 | 64.0 x 64.0 x 44.0 (Y-90) | 1038 | 1.19 **(< 1.2)** (min 1.19) | 58.4 | 45.95 |
| M5 tapa | M5_capsula_tapa.stl | ok | si | 1 | 33.0 x 64.0 x 64.0 (X-90) | 499 | 0.62 **(< 1.2)** (min 0.62) | 29.8 | 23.47 |
| M6 bisel | M6_capsula_bisel.stl | ok | si | 1 | 42.0 x 42.0 x 2.5 (Y+90) | 0 | 1.79 (min 1.78) | 2.4 | 1.89 |
| M7 ventana | M7_capsula_ventana.stl | ok | si | 1 | 30.0 x 30.0 x 3.0 (Y+90) | 0 | 3.00 (min 3.00) | 2.5 | 2.12 |
| M10 carro | M10_carro_capsula.stl | ok | si | 1 | 80.8 x 38.6 x 85.0 (Y-90) | 899 | 0.62 **(< 1.2)** (min 0.62) | 69.2 | 54.50 |

M7 es el disco de acrilico (masa con densidad del acrilico); no se imprime. Orientacion de impresion: la de menor voladizo entre las seis probadas (giros de 90 grados sobre X e Y) que cabe en la cama; la columna indica el giro aplicado al marco de la pieza.

## Rango de la bisagra (interferencia en mm3)
Inclinacion hacia abajo de 0 a 90; contra el riel se toma el peor de 5 posiciones del carro, con la punta del riel de 0 a 100 mas alla de la manga (recorrido +-50).

| inclinacion | capsula vs carro | capsula vs riel (peor posicion) | capsula vs perilla | M4 carro | M5 carro | M6 carro |
|---|---|---|---|---|---|---|
| 0 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 10 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 20 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 40 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 50 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 60 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 70 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 80 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 90 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

Ajuste de las maquetas (mm3, debe ser 0): camara-cuerpo 0.00; camara-tapa 0.00; camara-bisel 0.00; led-cuerpo 0.00; led-camara 0.00; ventana-cuerpo 0.00; ventana-bisel 0.00

## Flotabilidad por capsula
- PETG M4+M5+M6: 71.3 cm3.
- Aire encerrado (cavidad menos tubo y radios): 54.3 cm3.
- Ventana: 2.12 cm3.
- Volumen desplazado total: 127.8 cm3 (antes 154).
- Masa con M4 y M5 al 100 % y M6 al 40 % (piel 1.2): M4 58.4 + M5 29.8 + M6 2.4 + ventana 2.5 = **93.1 g** (antes 104 g). Con M6 al 100 %: 93.1 g.
- Con contenido (CAPSULE_CONTENT_G) no incluido. Empuje: 131.0 g contra 93.1 g de la pieza.
- M10 aparte: 69.2 g al 100 %, 49.2 g al 40 %.
