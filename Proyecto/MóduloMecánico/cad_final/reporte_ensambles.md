# Ensambles (Fase D)

Nodo completo sobre la linterna de referencia (esquematica: aro Ø8 en el plano horizontal a la altura del centro de la barra de la linterna donde engancha M9, 4 cuerdas Ø4 a 45/135/225/315 grados, red cilindro de 1 mm de espesor y alto D). En Ø100 y Ø200 las cuerdas se amarran al ojal del asa del nodo; en Ø300 y Ø500 van a un apice sobre el aro. Todos los valores de la linterna son `estimado / por_verificar` (ver `params.py`, bloque `# ensambles (Fase D)`). Umbral de interferencia: volumen comun > 0.01 mm3.
Posicion nominal: carro con s = 0 (manga a ras de la punta del riel), capsula a 40 grados. El lado -X es la misma pieza girada 180 grados sobre Z (como `riel.py`). El barrido de bisagra se calcula en el lado +X.

## Resumen

| Caso | Ext/lado | Largo del riel | Bbox X | Bbox Y | Bbox Z | Pares con interferencia | Nodo vs linterna | Apice minimo (10 mm) |
|---|---|---|---|---|---|---|---|---|
| D100 | 0 | 230 | -193 a 193 | -63 a 63 | -163 a 113 | 2 | 6 | al ojal del asa |
| D200 | 1 | 430 | -293 a 293 | -63 a 63 | -163 a 113 | 0 | 6 | al ojal del asa |
| D300 | 1 | 430 | -293 a 293 | -63 a 63 | -163 a 113 | 2 | 12 | 578 mm |
| D500 | 2 | 630 | -393 a 393 | -63 a 63 | -163 a 113 | 2 | 4 | 294 mm |

## Ø100 (sin extensiones, RAIL_EXT_PER_RING = 0)

Largo ensamblado del riel: 230.0 mm (punta a punta, x = ±115.0). Centro de la barra de la linterna (enganche M9) a z = -109.75, fondo del riel z = -69.75.

### Interferencias entre piezas del nodo (nominal)

| Pieza A | Pieza B | mm3 |
|---|---|---|
| M14 pestillo +X | cilindro libre perilla carro +X | 259.20 |
| M14 pestillo -X | cilindro libre perilla carro -X | 259.20 |

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M12 perilla +X | 0.00 | 0.00 | 4126.24 |
| M10 carro +X | M12 perilla -X | 0.00 | 0.00 | 504.99 |
| M10 carro +X | M13 casquillo +X | 0.00 | 247.80 | 0.00 |
| M10 carro +X | M14 pestillo +X | 0.00 | 620.26 | 0.00 |
| M10 carro +X | M3 riel central | 0.00 | 3177.08 | 2640.00 |
| M10 carro +X | M9 gancho +X | 0.00 | 11175.44 | 2695.55 |
| M10 carro +X | M9 gancho -X | 0.00 | 0.00 | 5148.12 |
| M10 carro +X | cilindro libre perilla gancho +X | 0.00 | 0.00 | 7741.20 |
| M10 carro +X | cilindro libre perilla gancho -X | 0.00 | 0.00 | 2007.46 |
| M10 carro +X | lastre pletina_0 | 0.00 | 855.00 | 1140.00 |
| M10 carro +X | lastre pletina_1 | 0.00 | 855.00 | 1140.00 |
| M10 carro +X | lastre pletina_2 | 0.00 | 812.25 | 1083.00 |
| M10 carro +X | lastre pletina_4 | 0.00 | 855.00 | 1140.00 |
| M10 carro +X | lastre pletina_5 | 0.00 | 855.00 | 1140.00 |
| M10 carro +X | lastre pletina_6 | 0.00 | 855.00 | 1140.00 |
| M10 carro +X | lastre pletina_7 | 0.00 | 855.00 | 1140.00 |
| M10 carro +X | tapa_bolsillo_n | 0.00 | 582.00 | 720.00 |
| M10 carro +X | tapa_bolsillo_s | 0.00 | 582.00 | 720.00 |
| M10 carro -X | M12 perilla +X | 0.00 | 0.00 | 504.99 |
| M10 carro -X | M12 perilla -X | 0.00 | 0.00 | 4126.24 |
| M10 carro -X | M13 casquillo -X | 0.00 | 247.80 | 0.00 |
| M10 carro -X | M14 pestillo -X | 0.00 | 620.26 | 0.00 |
| M10 carro -X | M3 riel central | 0.00 | 3177.08 | 2640.00 |
| M10 carro -X | M9 gancho +X | 0.00 | 0.00 | 5148.12 |
| M10 carro -X | M9 gancho -X | 0.00 | 11175.44 | 2695.55 |
| M10 carro -X | cilindro libre perilla gancho +X | 0.00 | 0.00 | 2007.46 |
| M10 carro -X | cilindro libre perilla gancho -X | 0.00 | 0.00 | 7741.20 |
| M10 carro -X | lastre pletina_0 | 0.00 | 855.00 | 1140.00 |
| M10 carro -X | lastre pletina_1 | 0.00 | 855.00 | 1140.00 |
| M10 carro -X | lastre pletina_2 | 0.00 | 855.00 | 1140.00 |
| M10 carro -X | lastre pletina_3 | 0.00 | 855.00 | 1140.00 |
| M10 carro -X | lastre pletina_4 | 0.00 | 855.00 | 1140.00 |
| M10 carro -X | lastre pletina_5 | 0.00 | 855.00 | 1140.00 |
| M10 carro -X | lastre pletina_6 | 0.00 | 812.25 | 1083.00 |
| M10 carro -X | tapa_bolsillo_n | 0.00 | 582.00 | 720.00 |
| M10 carro -X | tapa_bolsillo_s | 0.00 | 582.00 | 720.00 |
| cilindro libre perilla carro +X | M12 perilla +X | 0.00 | 5747.30 | 0.00 |
| cilindro libre perilla carro +X | M12 perilla -X | 0.00 | 0.00 | 4705.81 |
| cilindro libre perilla carro +X | M14 pestillo +X | 259.20 | 0.00 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho +X | 0.00 | 1104.27 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho -X | 0.00 | 0.00 | 1881.61 |
| cilindro libre perilla carro -X | M12 perilla +X | 0.00 | 0.00 | 4705.81 |
| cilindro libre perilla carro -X | M12 perilla -X | 0.00 | 5747.30 | 0.00 |
| cilindro libre perilla carro -X | M14 pestillo -X | 259.20 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho +X | 0.00 | 0.00 | 1881.61 |
| cilindro libre perilla carro -X | M9 gancho -X | 0.00 | 1104.27 | 0.00 |

### Nodo contra la linterna (cuerdas al ojal del asa)

| Pieza | Linterna | mm3 |
|---|---|---|
| M9 gancho -X | red | 96.60 |
| M9 gancho +X | red | 96.60 |
| M13 casquillo -X | red | 55.86 |
| M13 casquillo +X | red | 55.86 |
| M13 casquillo +X | aro | 4.14 |
| M13 casquillo -X | aro | 4.14 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | ninguno | ninguno |
| 50 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 1607.7 mm3 (tilt 90); red 440.6 mm3 (tilt 90); M14 pestillo +X 188.9 mm3 (tilt 90) |
| 100 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 4684.5 mm3 (tilt 0); red 2456.8 mm3 (tilt 90); aro 1828.0 mm3 (tilt 50); M13 casquillo +X 806.7 mm3 (tilt 30); M14 pestillo +X 203.8 mm3 (tilt 30); cilindro libre perilla gancho +X 166.3 mm3 (tilt 0) |

### Cuerdas amarradas al ojal del asa (decision del 29/10)

La linterna cuelga del nodo: las 4 cuerdas suben del aro, rodean el borde de la caja y la tapa, y se amarran al ojal del asa (centro a z = 103). Largo de cada cuerda del aro al ojal: 266, 266, 266, 266 mm. Las interferencias de las cuerdas con el nodo estan en la tabla "Nodo contra la linterna": el modelo deja la cuerda a 0.5 mm del borde, en la realidad apoya. Asa verificada con 150 N + 30 N de la linterna en `reporte_verificacion.md` §6.

## Ø200

Largo ensamblado del riel: 430.0 mm (punta a punta, x = ±215.0). Centro de la barra de la linterna (enganche M9) a z = -109.75, fondo del riel z = -69.75.

### Interferencias entre piezas del nodo (nominal)

Ninguna.

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M13 casquillo +X | 0.00 | 0.00 | 247.80 |
| M10 carro +X | M14 pestillo +X | 0.00 | 0.00 | 620.26 |
| M10 carro +X | M9 gancho +X | 0.00 | 0.00 | 11175.44 |
| M10 carro -X | M13 casquillo -X | 0.00 | 0.00 | 247.80 |
| M10 carro -X | M14 pestillo -X | 0.00 | 0.00 | 620.26 |
| M10 carro -X | M9 gancho -X | 0.00 | 0.00 | 11175.44 |
| cilindro libre perilla carro +X | M12 perilla +X | 0.00 | 0.00 | 5747.30 |
| cilindro libre perilla carro +X | M14 pestillo +X | 0.00 | 259.20 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho +X | 0.00 | 0.00 | 1104.27 |
| cilindro libre perilla carro -X | M12 perilla -X | 0.00 | 0.00 | 5747.30 |
| cilindro libre perilla carro -X | M14 pestillo -X | 0.00 | 259.20 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho -X | 0.00 | 0.00 | 1104.27 |

### Nodo contra la linterna (cuerdas al ojal del asa)

| Pieza | Linterna | mm3 |
|---|---|---|
| M9 gancho -X | red | 96.36 |
| M9 gancho +X | red | 96.36 |
| M13 casquillo -X | red | 55.61 |
| M13 casquillo +X | red | 55.61 |
| M13 casquillo -X | aro | 0.21 |
| M13 casquillo +X | aro | 0.21 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | ninguno | ninguno |
| 50 | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | ninguno | ninguno |
| 100 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 1607.7 mm3 (tilt 90); red 620.1 mm3 (tilt 90); M14 pestillo +X 188.9 mm3 (tilt 90) |

### Cuerdas amarradas al ojal del asa (decision del 29/10)

La linterna cuelga del nodo: las 4 cuerdas suben del aro, rodean el borde de la caja y la tapa, y se amarran al ojal del asa (centro a z = 103). Largo de cada cuerda del aro al ojal: 258, 258, 258, 258 mm. Las interferencias de las cuerdas con el nodo estan en la tabla "Nodo contra la linterna": el modelo deja la cuerda a 0.5 mm del borde, en la realidad apoya. Asa verificada con 150 N + 30 N de la linterna en `reporte_verificacion.md` §6.

## Ø300

Largo ensamblado del riel: 430.0 mm (punta a punta, x = ±215.0). Centro de la barra de la linterna (enganche M9) a z = -109.75, fondo del riel z = -69.75.

### Interferencias entre piezas del nodo (nominal)

| Pieza A | Pieza B | mm3 |
|---|---|---|
| M14 pestillo +X | cilindro libre perilla carro +X | 259.20 |
| M14 pestillo -X | cilindro libre perilla carro -X | 259.20 |

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M12 perilla +X | 0.00 | 0.00 | 4126.24 |
| M10 carro +X | M13 casquillo +X | 0.00 | 247.80 | 0.00 |
| M10 carro +X | M14 pestillo +X | 0.00 | 620.26 | 0.00 |
| M10 carro +X | M9 gancho +X | 0.00 | 11175.44 | 2695.55 |
| M10 carro +X | cilindro libre perilla gancho +X | 0.00 | 0.00 | 7741.20 |
| M10 carro -X | M12 perilla -X | 0.00 | 0.00 | 4126.24 |
| M10 carro -X | M13 casquillo -X | 0.00 | 247.80 | 0.00 |
| M10 carro -X | M14 pestillo -X | 0.00 | 620.26 | 0.00 |
| M10 carro -X | M9 gancho -X | 0.00 | 11175.44 | 2695.55 |
| M10 carro -X | cilindro libre perilla gancho -X | 0.00 | 0.00 | 7741.20 |
| cilindro libre perilla carro +X | M12 perilla +X | 0.00 | 5747.30 | 0.00 |
| cilindro libre perilla carro +X | M14 pestillo +X | 259.20 | 0.00 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho +X | 0.00 | 1104.27 | 0.00 |
| cilindro libre perilla carro -X | M12 perilla -X | 0.00 | 5747.30 | 0.00 |
| cilindro libre perilla carro -X | M14 pestillo -X | 259.20 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho -X | 0.00 | 1104.27 | 0.00 |

### Nodo contra la linterna (apice 400)

| Pieza | Linterna | mm3 |
|---|---|---|
| M9 gancho -X | red | 96.31 |
| M9 gancho +X | red | 96.31 |
| M13 casquillo -X | red | 55.56 |
| M13 casquillo +X | red | 55.56 |
| M2 tapa | cuerda 135 | 32.68 |
| M2 tapa | cuerda 225 | 32.68 |
| M2 tapa | cuerda 315 | 32.68 |
| M2 tapa | cuerda 45 | 32.68 |
| M1 caja | cuerda 45 | 8.20 |
| M1 caja | cuerda 225 | 8.20 |
| M1 caja | cuerda 315 | 8.20 |
| M1 caja | cuerda 135 | 8.20 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | ninguno | ninguno |
| 50 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 1607.7 mm3 (tilt 90); red 674.7 mm3 (tilt 90); M14 pestillo +X 188.9 mm3 (tilt 90) |
| 100 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 4684.5 mm3 (tilt 0); red 2440.1 mm3 (tilt 90); aro 2352.9 mm3 (tilt 50); M13 casquillo +X 806.7 mm3 (tilt 30); M14 pestillo +X 203.8 mm3 (tilt 30); cilindro libre perilla gancho +X 166.3 mm3 (tilt 0) |

### Apice minimo de las cuerdas

Altura minima del apice sobre el aro para 10 mm de aire entre cuerda y cualquier pieza del nodo: **578 mm** (piso: 233 mm = techo del nodo + 10). 

## Ø500

Largo ensamblado del riel: 630.0 mm (punta a punta, x = ±315.0). Centro de la barra de la linterna (enganche M9) a z = -109.75, fondo del riel z = -69.75.

### Interferencias entre piezas del nodo (nominal)

| Pieza A | Pieza B | mm3 |
|---|---|---|
| M14 pestillo +X | cilindro libre perilla carro +X | 259.20 |
| M14 pestillo -X | cilindro libre perilla carro -X | 259.20 |

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M12 perilla +X | 0.00 | 0.00 | 4126.24 |
| M10 carro +X | M13 casquillo +X | 0.00 | 247.80 | 0.00 |
| M10 carro +X | M14 pestillo +X | 0.00 | 620.26 | 0.00 |
| M10 carro +X | M9 gancho +X | 0.00 | 11175.44 | 2695.55 |
| M10 carro +X | cilindro libre perilla gancho +X | 0.00 | 0.00 | 7741.20 |
| M10 carro -X | M12 perilla -X | 0.00 | 0.00 | 4126.24 |
| M10 carro -X | M13 casquillo -X | 0.00 | 247.80 | 0.00 |
| M10 carro -X | M14 pestillo -X | 0.00 | 620.26 | 0.00 |
| M10 carro -X | M9 gancho -X | 0.00 | 11175.44 | 2695.55 |
| M10 carro -X | cilindro libre perilla gancho -X | 0.00 | 0.00 | 7741.20 |
| cilindro libre perilla carro +X | M12 perilla +X | 0.00 | 5747.30 | 0.00 |
| cilindro libre perilla carro +X | M14 pestillo +X | 259.20 | 0.00 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho +X | 0.00 | 1104.27 | 0.00 |
| cilindro libre perilla carro -X | M12 perilla -X | 0.00 | 5747.30 | 0.00 |
| cilindro libre perilla carro -X | M14 pestillo -X | 259.20 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho -X | 0.00 | 1104.27 | 0.00 |

### Nodo contra la linterna (apice 400)

| Pieza | Linterna | mm3 |
|---|---|---|
| M9 gancho +X | red | 96.28 |
| M9 gancho -X | red | 96.28 |
| M13 casquillo -X | red | 55.52 |
| M13 casquillo +X | red | 55.52 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | ninguno | ninguno |
| 50 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 1607.7 mm3 (tilt 90); red 689.4 mm3 (tilt 90); M14 pestillo +X 188.9 mm3 (tilt 90) |
| 100 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 4684.5 mm3 (tilt 0); aro 2443.2 mm3 (tilt 50); red 2415.5 mm3 (tilt 90); M13 casquillo +X 806.7 mm3 (tilt 30); M14 pestillo +X 203.8 mm3 (tilt 30); cilindro libre perilla gancho +X 166.3 mm3 (tilt 0) |

### Apice minimo de las cuerdas

Altura minima del apice sobre el aro para 10 mm de aire entre cuerda y cualquier pieza del nodo: **294 mm** (piso: 233 mm = techo del nodo + 10). 
