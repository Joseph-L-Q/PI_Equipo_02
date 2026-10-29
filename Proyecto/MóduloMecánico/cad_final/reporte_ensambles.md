# Ensambles (Fase D)

Nodo completo sobre la linterna de referencia (esquematica: aro Ø8 en el plano horizontal a la altura del centro de la varilla, 4 cuerdas Ø4 a 45/135/225/315 grados, red cilindro de 1 mm de espesor y alto D). Todos los valores de la linterna son `estimado / por_verificar` (ver `params.py`, bloque `# ensambles (Fase D)`). Umbral de interferencia: volumen comun > 0.01 mm3.
Posicion nominal: carro con s = 50 (punta del riel 50 mm pasada la manga), capsula a 40 grados. El lado -X es la misma pieza girada 180 grados sobre Z (como `riel.py`). El barrido de bisagra se calcula en el lado +X.

## Resumen

| Caso | Ext/lado | Largo del riel | Bbox X | Bbox Y | Bbox Z | Pares con interferencia | Nodo vs linterna | Apice minimo (10 mm) |
|---|---|---|---|---|---|---|---|---|
| D100 | 0 | 140 | -98 a 98 | -63 a 63 | -151 a 113 | 46 | 46 | no existe |
| D100e1 | 1 | 310 | -183 a 183 | -63 a 63 | -151 a 113 | 26 | 42 | no existe |
| D200 | 1 | 310 | -183 a 183 | -63 a 63 | -151 a 113 | 40 | 14 | no existe |
| D300 | 1 | 310 | -183 a 183 | -63 a 63 | -151 a 113 | 34 | 8 | 535 mm |
| D500 | 2 | 480 | -272 a 272 | -63 a 63 | -151 a 113 | 8 | 8 | 273 mm |

## Ø100 (sin extensiones, RAIL_EXT_PER_RING = 0)

Largo ensamblado del riel: 140.0 mm (punta a punta, x = ±70.0). Centro de la varilla a z = -97.35, fondo del riel z = -57.35.

### Interferencias entre piezas del nodo (nominal)

| Pieza A | Pieza B | mm3 |
|---|---|---|
| cilindro libre perilla gancho +X | M10 carro +X | 9329.79 |
| cilindro libre perilla gancho -X | M10 carro -X | 9329.79 |
| cilindro libre perilla carro +X | M12 perilla -X | 5697.02 |
| M12 perilla +X | cilindro libre perilla carro -X | 5697.02 |
| cilindro libre perilla carro +X | M10 carro -X | 5658.94 |
| M10 carro +X | cilindro libre perilla carro -X | 5658.94 |
| M12 perilla -X | M10 carro -X | 5035.17 |
| M12 perilla +X | M10 carro +X | 5035.17 |
| M10 carro +X | M9 gancho -X | 4401.44 |
| M9 gancho +X | M10 carro -X | 4401.44 |
| M9 gancho -X | M10 carro -X | 3819.96 |
| M9 gancho +X | M10 carro +X | 3819.96 |
| M3 riel central | M10 carro -X | 3360.00 |
| M3 riel central | M10 carro +X | 3360.00 |
| M9 gancho -X | capsula M4-M7 -X | 2613.29 |
| M9 gancho +X | capsula M4-M7 +X | 2613.29 |
| M9 gancho +X | cilindro libre perilla carro -X | 1233.61 |
| cilindro libre perilla carro +X | M9 gancho -X | 1233.61 |
| lastre pletina_3 | M10 carro +X | 1140.00 |
| lastre pletina_0 | M10 carro -X | 1140.00 |
| lastre pletina_1 | M10 carro -X | 1140.00 |
| lastre pletina_2 | M10 carro -X | 1140.00 |
| lastre pletina_3 | M10 carro -X | 1140.00 |
| lastre pletina_7 | M10 carro +X | 1140.00 |
| lastre pletina_7 | M10 carro -X | 1140.00 |
| lastre pletina_4 | M10 carro +X | 1140.00 |
| lastre pletina_5 | M10 carro +X | 1140.00 |
| lastre pletina_6 | M10 carro +X | 1140.00 |
| M13 casquillo -X | capsula M4-M7 -X | 733.16 |
| M13 casquillo +X | capsula M4-M7 +X | 733.16 |
| tapa_bolsillo_n | M10 carro -X | 720.00 |
| tapa_bolsillo_n | M10 carro +X | 720.00 |
| tapa_bolsillo_s | M10 carro +X | 720.00 |
| tapa_bolsillo_s | M10 carro -X | 720.00 |
| lastre pletina_2 | M10 carro +X | 604.20 |
| lastre pletina_6 | M10 carro -X | 604.20 |
| lastre pletina_0 | M10 carro +X | 535.80 |
| lastre pletina_4 | M10 carro -X | 535.80 |
| M10 carro +X | cilindro libre perilla gancho -X | 384.44 |
| cilindro libre perilla gancho +X | M10 carro -X | 384.44 |
| M14 pestillo -X | capsula M4-M7 -X | 267.13 |
| M14 pestillo +X | capsula M4-M7 +X | 267.13 |
| M13 casquillo +X | M10 carro +X | 105.95 |
| M13 casquillo -X | M10 carro -X | 105.95 |
| cilindro libre perilla gancho -X | capsula M4-M7 -X | 103.70 |
| cilindro libre perilla gancho +X | capsula M4-M7 +X | 103.70 |

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M12 perilla +X | 0.00 | 5035.17 | 0.00 |
| M10 carro +X | M12 perilla -X | 0.00 | 0.00 | 3036.51 |
| M10 carro +X | M13 casquillo +X | 240.10 | 105.95 | 0.00 |
| M10 carro +X | M13 casquillo -X | 0.00 | 0.00 | 244.30 |
| M10 carro +X | M14 pestillo +X | 701.06 | 0.00 | 0.00 |
| M10 carro +X | M3 riel central | 3410.40 | 3360.00 | 2302.40 |
| M10 carro +X | M9 gancho +X | 8829.07 | 3819.96 | 0.00 |
| M10 carro +X | M9 gancho -X | 0.00 | 4401.44 | 8749.20 |
| M10 carro +X | cilindro libre perilla gancho +X | 0.00 | 9329.79 | 0.00 |
| M10 carro +X | cilindro libre perilla gancho -X | 0.00 | 384.44 | 6103.63 |
| M10 carro +X | lastre pletina_0 | 357.20 | 535.80 | 178.60 |
| M10 carro +X | lastre pletina_2 | 402.80 | 604.20 | 201.40 |
| M10 carro +X | lastre pletina_3 | 760.00 | 1140.00 | 380.00 |
| M10 carro +X | lastre pletina_4 | 760.00 | 1140.00 | 380.00 |
| M10 carro +X | lastre pletina_5 | 760.00 | 1140.00 | 380.00 |
| M10 carro +X | lastre pletina_6 | 760.00 | 1140.00 | 380.00 |
| M10 carro +X | lastre pletina_7 | 760.00 | 1140.00 | 380.00 |
| M10 carro +X | tapa_bolsillo_n | 522.00 | 720.00 | 282.00 |
| M10 carro +X | tapa_bolsillo_s | 522.00 | 720.00 | 282.00 |
| M10 carro -X | M12 perilla +X | 0.00 | 0.00 | 3036.51 |
| M10 carro -X | M12 perilla -X | 0.00 | 5035.17 | 0.00 |
| M10 carro -X | M13 casquillo +X | 0.00 | 0.00 | 244.30 |
| M10 carro -X | M13 casquillo -X | 240.10 | 105.95 | 0.00 |
| M10 carro -X | M14 pestillo -X | 701.06 | 0.00 | 0.00 |
| M10 carro -X | M3 riel central | 3422.40 | 3360.00 | 2290.40 |
| M10 carro -X | M9 gancho +X | 0.00 | 4401.44 | 8749.20 |
| M10 carro -X | M9 gancho -X | 8829.07 | 3819.96 | 0.00 |
| M10 carro -X | cilindro libre perilla gancho +X | 0.00 | 384.44 | 6103.63 |
| M10 carro -X | cilindro libre perilla gancho -X | 0.00 | 9329.79 | 0.00 |
| M10 carro -X | lastre pletina_0 | 760.00 | 1140.00 | 380.00 |
| M10 carro -X | lastre pletina_1 | 760.00 | 1140.00 | 380.00 |
| M10 carro -X | lastre pletina_2 | 760.00 | 1140.00 | 380.00 |
| M10 carro -X | lastre pletina_3 | 760.00 | 1140.00 | 380.00 |
| M10 carro -X | lastre pletina_4 | 357.20 | 535.80 | 178.60 |
| M10 carro -X | lastre pletina_6 | 402.80 | 604.20 | 201.40 |
| M10 carro -X | lastre pletina_7 | 760.00 | 1140.00 | 380.00 |
| M10 carro -X | tapa_bolsillo_n | 522.00 | 720.00 | 282.00 |
| M10 carro -X | tapa_bolsillo_s | 522.00 | 720.00 | 282.00 |
| cilindro libre perilla carro +X | M12 perilla +X | 4954.22 | 0.00 | 0.00 |
| cilindro libre perilla carro +X | M12 perilla -X | 0.00 | 5697.02 | 0.00 |
| cilindro libre perilla carro +X | M14 pestillo -X | 0.00 | 0.00 | 259.20 |
| cilindro libre perilla carro +X | M9 gancho +X | 1752.01 | 0.00 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho -X | 0.00 | 1233.61 | 0.00 |
| cilindro libre perilla carro -X | M12 perilla +X | 0.00 | 5697.02 | 0.00 |
| cilindro libre perilla carro -X | M12 perilla -X | 4954.22 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M14 pestillo +X | 0.00 | 0.00 | 259.20 |
| cilindro libre perilla carro -X | M9 gancho +X | 0.00 | 1233.61 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho -X | 1752.01 | 0.00 | 0.00 |

### Nodo contra la linterna (apice 400)

| Pieza | Linterna | mm3 |
|---|---|---|
| capsula M4-M7 -X | aro | 1252.43 |
| capsula M4-M7 +X | aro | 1251.65 |
| capsula M4-M7 +X | red | 1108.48 |
| capsula M4-M7 -X | red | 1108.48 |
| M9 gancho -X | red | 96.60 |
| M9 gancho +X | red | 96.60 |
| M3 riel central | cuerda 315 | 79.66 |
| M3 riel central | cuerda 45 | 79.66 |
| M3 riel central | cuerda 135 | 79.66 |
| M3 riel central | cuerda 225 | 79.66 |
| lastre pletina_0 | cuerda 45 | 63.32 |
| lastre pletina_5 | cuerda 225 | 63.32 |
| lastre pletina_5 | cuerda 315 | 63.32 |
| lastre pletina_1 | cuerda 135 | 63.32 |
| M2 tapa | cuerda 315 | 63.32 |
| M2 tapa | cuerda 225 | 63.32 |
| lastre pletina_1 | cuerda 45 | 63.32 |
| M2 tapa | cuerda 135 | 63.32 |
| M2 tapa | cuerda 45 | 63.32 |
| lastre pletina_0 | cuerda 135 | 63.32 |
| lastre pletina_4 | cuerda 225 | 63.32 |
| lastre pletina_4 | cuerda 315 | 63.32 |
| lastre pletina_7 | cuerda 225 | 63.32 |
| lastre pletina_7 | cuerda 315 | 63.32 |
| lastre pletina_3 | cuerda 135 | 63.32 |
| lastre pletina_6 | cuerda 225 | 63.32 |
| lastre pletina_6 | cuerda 315 | 63.32 |
| lastre pletina_2 | cuerda 135 | 63.32 |
| lastre pletina_2 | cuerda 45 | 63.32 |
| lastre pletina_3 | cuerda 45 | 63.32 |
| M13 casquillo -X | red | 55.86 |
| M13 casquillo +X | red | 55.86 |
| M1 caja | cuerda 135 | 50.66 |
| M1 caja | cuerda 45 | 50.66 |
| M1 caja | cuerda 225 | 50.66 |
| M1 caja | cuerda 315 | 50.66 |
| M11 bandeja_M11_bandeja | cuerda 135 | 37.99 |
| M11 bandeja_M11_bandeja | cuerda 45 | 37.99 |
| tapa_bolsillo_s | cuerda 225 | 37.99 |
| tapa_bolsillo_s | cuerda 315 | 37.99 |
| M11 bandeja_M11_bandeja | cuerda 315 | 37.99 |
| M11 bandeja_M11_bandeja | cuerda 225 | 37.99 |
| tapa_bolsillo_n | cuerda 45 | 37.99 |
| tapa_bolsillo_n | cuerda 135 | 37.99 |
| M13 casquillo +X | aro | 4.14 |
| M13 casquillo -X | aro | 4.14 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 1271.4 mm3 (tilt 90) |
| 50 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 3358.5 mm3 (tilt 0); aro 1430.2 mm3 (tilt 20); red 1308.9 mm3 (tilt 60); M13 casquillo +X 892.1 mm3 (tilt 10); M14 pestillo +X 369.8 mm3 (tilt 30); cilindro libre perilla gancho +X 111.0 mm3 (tilt 0) |
| 100 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | cilindro libre perilla gancho +X 6057.4 mm3 (tilt 10); M9 gancho +X 3322.5 mm3 (tilt 0); M12 perilla +X 2397.3 mm3 (tilt 0); aro 1967.8 mm3 (tilt 20); M9 gancho -X 902.7 mm3 (tilt 90); red 713.7 mm3 (tilt 90); M13 casquillo +X 713.4 mm3 (tilt 20); cilindro libre perilla gancho -X 220.3 mm3 (tilt 0) |

### Apice minimo de las cuerdas

No existe: ninguna altura entre el techo del nodo y 3000 mm deja 10 mm de aire. Aire con las cuerdas casi verticales (apice a 3000 mm, caso mas favorable): -1.9 mm entre la superficie de la cuerda y el nodo (piso de altura 220 mm).

## Ø100 con 1 extension por lado (variante)

Largo ensamblado del riel: 310.0 mm (punta a punta, x = ±155.0). Centro de la varilla a z = -97.35, fondo del riel z = -57.35.

### Interferencias entre piezas del nodo (nominal)

| Pieza A | Pieza B | mm3 |
|---|---|---|
| M3 riel central | M10 carro -X | 1462.40 |
| M3 riel central | M10 carro +X | 1450.40 |
| M9 gancho +X | M10 carro +X | 960.00 |
| M9 gancho -X | M10 carro -X | 960.00 |
| M9 gancho -X | cilindro libre perilla carro -X | 796.87 |
| M9 gancho +X | cilindro libre perilla carro +X | 796.87 |
| M14 pestillo +X | cilindro libre perilla carro +X | 259.20 |
| M14 pestillo -X | cilindro libre perilla carro -X | 259.20 |
| tapa_bolsillo_n | M10 carro -X | 102.00 |
| tapa_bolsillo_n | M10 carro +X | 102.00 |
| tapa_bolsillo_s | M10 carro +X | 102.00 |
| tapa_bolsillo_s | M10 carro -X | 102.00 |
| lastre pletina_0 | M10 carro -X | 95.00 |
| lastre pletina_1 | M10 carro -X | 95.00 |
| lastre pletina_2 | M10 carro -X | 95.00 |
| lastre pletina_3 | M10 carro -X | 95.00 |
| lastre pletina_3 | M10 carro +X | 95.00 |
| lastre pletina_4 | M10 carro +X | 95.00 |
| lastre pletina_5 | M10 carro +X | 95.00 |
| lastre pletina_6 | M10 carro +X | 95.00 |
| lastre pletina_7 | M10 carro +X | 95.00 |
| lastre pletina_7 | M10 carro -X | 95.00 |
| lastre pletina_2 | M10 carro +X | 50.35 |
| lastre pletina_6 | M10 carro -X | 50.35 |
| lastre pletina_0 | M10 carro +X | 44.65 |
| lastre pletina_4 | M10 carro -X | 44.65 |

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M12 perilla +X | 0.00 | 0.00 | 504.99 |
| M10 carro +X | M13 casquillo +X | 0.00 | 0.00 | 251.47 |
| M10 carro +X | M14 pestillo +X | 0.00 | 0.00 | 295.07 |
| M10 carro +X | M3 riel central | 0.00 | 1450.40 | 4250.40 |
| M10 carro +X | M9 gancho +X | 0.00 | 960.00 | 11778.54 |
| M10 carro +X | M9 gancho -X | 0.00 | 0.00 | 240.00 |
| M10 carro +X | cilindro libre perilla gancho +X | 0.00 | 0.00 | 2007.46 |
| M10 carro +X | lastre pletina_0 | 0.00 | 44.65 | 491.15 |
| M10 carro +X | lastre pletina_2 | 0.00 | 50.35 | 553.85 |
| M10 carro +X | lastre pletina_3 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_4 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_5 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_6 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_7 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | tapa_bolsillo_n | 0.00 | 102.00 | 702.00 |
| M10 carro +X | tapa_bolsillo_s | 0.00 | 102.00 | 702.00 |
| M10 carro -X | M12 perilla -X | 0.00 | 0.00 | 504.99 |
| M10 carro -X | M13 casquillo -X | 0.00 | 0.00 | 251.47 |
| M10 carro -X | M14 pestillo -X | 0.00 | 0.00 | 295.07 |
| M10 carro -X | M3 riel central | 0.00 | 1462.40 | 4250.40 |
| M10 carro -X | M9 gancho +X | 0.00 | 0.00 | 240.00 |
| M10 carro -X | M9 gancho -X | 0.00 | 960.00 | 11778.54 |
| M10 carro -X | cilindro libre perilla gancho -X | 0.00 | 0.00 | 2007.46 |
| M10 carro -X | lastre pletina_0 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_1 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_2 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_3 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_4 | 0.00 | 44.65 | 491.15 |
| M10 carro -X | lastre pletina_6 | 0.00 | 50.35 | 553.85 |
| M10 carro -X | lastre pletina_7 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | tapa_bolsillo_n | 0.00 | 102.00 | 702.00 |
| M10 carro -X | tapa_bolsillo_s | 0.00 | 102.00 | 702.00 |
| cilindro libre perilla carro +X | M12 perilla +X | 0.00 | 0.00 | 4705.81 |
| cilindro libre perilla carro +X | M14 pestillo +X | 0.00 | 259.20 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho +X | 0.00 | 796.87 | 825.53 |
| cilindro libre perilla carro +X | M9 gancho -X | 0.00 | 0.00 | 25.92 |
| cilindro libre perilla carro -X | M12 perilla -X | 0.00 | 0.00 | 4705.81 |
| cilindro libre perilla carro -X | M14 pestillo -X | 0.00 | 259.20 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho +X | 0.00 | 0.00 | 25.92 |
| cilindro libre perilla carro -X | M9 gancho -X | 0.00 | 796.87 | 825.53 |

### Nodo contra la linterna (apice 400)

| Pieza | Linterna | mm3 |
|---|---|---|
| M9 gancho -X | red | 96.60 |
| M9 gancho +X | red | 96.60 |
| M3 riel central | cuerda 315 | 79.66 |
| M3 riel central | cuerda 45 | 79.66 |
| M3 riel central | cuerda 135 | 79.66 |
| M3 riel central | cuerda 225 | 79.66 |
| lastre pletina_0 | cuerda 45 | 63.32 |
| lastre pletina_5 | cuerda 225 | 63.32 |
| lastre pletina_5 | cuerda 315 | 63.32 |
| lastre pletina_1 | cuerda 135 | 63.32 |
| M2 tapa | cuerda 315 | 63.32 |
| M2 tapa | cuerda 225 | 63.32 |
| lastre pletina_1 | cuerda 45 | 63.32 |
| M2 tapa | cuerda 135 | 63.32 |
| M2 tapa | cuerda 45 | 63.32 |
| lastre pletina_0 | cuerda 135 | 63.32 |
| lastre pletina_4 | cuerda 225 | 63.32 |
| lastre pletina_4 | cuerda 315 | 63.32 |
| lastre pletina_7 | cuerda 225 | 63.32 |
| lastre pletina_7 | cuerda 315 | 63.32 |
| lastre pletina_3 | cuerda 135 | 63.32 |
| lastre pletina_6 | cuerda 225 | 63.32 |
| lastre pletina_6 | cuerda 315 | 63.32 |
| lastre pletina_2 | cuerda 135 | 63.32 |
| lastre pletina_2 | cuerda 45 | 63.32 |
| lastre pletina_3 | cuerda 45 | 63.32 |
| M13 casquillo -X | red | 55.86 |
| M13 casquillo +X | red | 55.86 |
| M1 caja | cuerda 135 | 50.66 |
| M1 caja | cuerda 45 | 50.66 |
| M1 caja | cuerda 225 | 50.66 |
| M1 caja | cuerda 315 | 50.66 |
| M11 bandeja_M11_bandeja | cuerda 135 | 37.99 |
| M11 bandeja_M11_bandeja | cuerda 45 | 37.99 |
| tapa_bolsillo_s | cuerda 225 | 37.99 |
| tapa_bolsillo_s | cuerda 315 | 37.99 |
| M11 bandeja_M11_bandeja | cuerda 315 | 37.99 |
| M11 bandeja_M11_bandeja | cuerda 225 | 37.99 |
| tapa_bolsillo_n | cuerda 45 | 37.99 |
| tapa_bolsillo_n | cuerda 135 | 37.99 |
| M13 casquillo +X | aro | 4.14 |
| M13 casquillo -X | aro | 4.14 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | ninguno | ninguno |
| 50 | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | ninguno | ninguno |
| 100 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 2403.0 mm3 (tilt 90); red 1643.2 mm3 (tilt 90); M14 pestillo +X 379.4 mm3 (tilt 0); M13 casquillo +X 4.5 mm3 (tilt 90) |

### Apice minimo de las cuerdas

No existe: ninguna altura entre el techo del nodo y 3000 mm deja 10 mm de aire. Aire con las cuerdas casi verticales (apice a 3000 mm, caso mas favorable): -1.9 mm entre la superficie de la cuerda y el nodo (piso de altura 220 mm).

## Ø200

Largo ensamblado del riel: 310.0 mm (punta a punta, x = ±155.0). Centro de la varilla a z = -97.35, fondo del riel z = -57.35.

### Interferencias entre piezas del nodo (nominal)

| Pieza A | Pieza B | mm3 |
|---|---|---|
| M9 gancho -X | M10 carro -X | 11778.54 |
| M9 gancho +X | M10 carro +X | 11778.54 |
| M12 perilla -X | cilindro libre perilla carro -X | 4705.81 |
| M12 perilla +X | cilindro libre perilla carro +X | 4705.81 |
| cilindro libre perilla gancho +X | M10 carro +X | 2007.46 |
| cilindro libre perilla gancho -X | M10 carro -X | 2007.46 |
| M3 riel central | M10 carro -X | 1462.40 |
| M3 riel central | M10 carro +X | 1450.40 |
| M9 gancho -X | cilindro libre perilla carro -X | 825.53 |
| M9 gancho +X | cilindro libre perilla carro +X | 825.53 |
| M9 gancho +X | capsula M4-M7 +X | 707.51 |
| M9 gancho -X | capsula M4-M7 -X | 707.51 |
| M12 perilla -X | M10 carro -X | 504.99 |
| M12 perilla +X | M10 carro +X | 504.99 |
| M14 pestillo +X | capsula M4-M7 +X | 378.01 |
| M14 pestillo -X | capsula M4-M7 -X | 378.01 |
| M14 pestillo -X | M10 carro -X | 295.07 |
| M14 pestillo +X | M10 carro +X | 295.07 |
| M13 casquillo +X | M10 carro +X | 251.47 |
| M13 casquillo -X | M10 carro -X | 251.47 |
| tapa_bolsillo_n | M10 carro -X | 102.00 |
| tapa_bolsillo_n | M10 carro +X | 102.00 |
| tapa_bolsillo_s | M10 carro +X | 102.00 |
| tapa_bolsillo_s | M10 carro -X | 102.00 |
| lastre pletina_0 | M10 carro -X | 95.00 |
| lastre pletina_1 | M10 carro -X | 95.00 |
| lastre pletina_2 | M10 carro -X | 95.00 |
| lastre pletina_3 | M10 carro -X | 95.00 |
| lastre pletina_3 | M10 carro +X | 95.00 |
| lastre pletina_4 | M10 carro +X | 95.00 |
| lastre pletina_5 | M10 carro +X | 95.00 |
| lastre pletina_6 | M10 carro +X | 95.00 |
| lastre pletina_7 | M10 carro +X | 95.00 |
| lastre pletina_7 | M10 carro -X | 95.00 |
| lastre pletina_2 | M10 carro +X | 50.35 |
| lastre pletina_6 | M10 carro -X | 50.35 |
| lastre pletina_0 | M10 carro +X | 44.65 |
| lastre pletina_4 | M10 carro -X | 44.65 |
| M13 casquillo -X | capsula M4-M7 -X | 1.88 |
| M13 casquillo +X | capsula M4-M7 +X | 1.88 |

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M12 perilla +X | 0.00 | 504.99 | 2146.72 |
| M10 carro +X | M13 casquillo +X | 0.00 | 251.47 | 0.00 |
| M10 carro +X | M14 pestillo +X | 0.00 | 295.07 | 0.00 |
| M10 carro +X | M3 riel central | 0.00 | 1450.40 | 4250.40 |
| M10 carro +X | M9 gancho +X | 960.00 | 11778.54 | 1153.56 |
| M10 carro +X | cilindro libre perilla gancho +X | 0.00 | 2007.46 | 4466.03 |
| M10 carro +X | lastre pletina_0 | 0.00 | 44.65 | 491.15 |
| M10 carro +X | lastre pletina_2 | 0.00 | 50.35 | 553.85 |
| M10 carro +X | lastre pletina_3 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_4 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_5 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_6 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_7 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | tapa_bolsillo_n | 0.00 | 102.00 | 702.00 |
| M10 carro +X | tapa_bolsillo_s | 0.00 | 102.00 | 702.00 |
| M10 carro -X | M12 perilla -X | 0.00 | 504.99 | 2146.72 |
| M10 carro -X | M13 casquillo -X | 0.00 | 251.47 | 0.00 |
| M10 carro -X | M14 pestillo -X | 0.00 | 295.07 | 0.00 |
| M10 carro -X | M3 riel central | 0.00 | 1462.40 | 4250.40 |
| M10 carro -X | M9 gancho -X | 960.00 | 11778.54 | 1153.56 |
| M10 carro -X | cilindro libre perilla gancho -X | 0.00 | 2007.46 | 4466.03 |
| M10 carro -X | lastre pletina_0 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_1 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_2 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_3 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_4 | 0.00 | 44.65 | 491.15 |
| M10 carro -X | lastre pletina_6 | 0.00 | 50.35 | 553.85 |
| M10 carro -X | lastre pletina_7 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | tapa_bolsillo_n | 0.00 | 102.00 | 702.00 |
| M10 carro -X | tapa_bolsillo_s | 0.00 | 102.00 | 702.00 |
| cilindro libre perilla carro +X | M12 perilla +X | 0.00 | 4705.81 | 0.00 |
| cilindro libre perilla carro +X | M14 pestillo +X | 259.20 | 0.00 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho +X | 796.87 | 825.53 | 0.00 |
| cilindro libre perilla carro -X | M12 perilla -X | 0.00 | 4705.81 | 0.00 |
| cilindro libre perilla carro -X | M14 pestillo -X | 259.20 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho -X | 796.87 | 825.53 | 0.00 |

### Nodo contra la linterna (apice 400)

| Pieza | Linterna | mm3 |
|---|---|---|
| M1 caja | cuerda 225 | 277.01 |
| M1 caja | cuerda 135 | 277.01 |
| M1 caja | cuerda 45 | 277.01 |
| M1 caja | cuerda 315 | 277.01 |
| M9 gancho -X | red | 96.36 |
| M9 gancho +X | red | 96.36 |
| M2 tapa | cuerda 225 | 64.77 |
| M2 tapa | cuerda 315 | 64.77 |
| M2 tapa | cuerda 135 | 64.77 |
| M2 tapa | cuerda 45 | 64.77 |
| M13 casquillo -X | red | 55.61 |
| M13 casquillo +X | red | 55.61 |
| M13 casquillo -X | aro | 0.21 |
| M13 casquillo +X | aro | 0.21 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | ninguno | ninguno |
| 50 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 2403.0 mm3 (tilt 90); red 1454.0 mm3 (tilt 90); M14 pestillo +X 379.4 mm3 (tilt 0); M13 casquillo +X 4.5 mm3 (tilt 90) |
| 100 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 3365.4 mm3 (tilt 0); aro 3038.7 mm3 (tilt 60); red 1771.1 mm3 (tilt 70); cilindro libre perilla gancho +X 1115.1 mm3 (tilt 0); M13 casquillo +X 954.3 mm3 (tilt 60); M14 pestillo +X 172.8 mm3 (tilt 0); M12 perilla +X 72.6 mm3 (tilt 0) |

### Apice minimo de las cuerdas

No existe: ninguna altura entre el techo del nodo y 3000 mm deja 10 mm de aire. Aire con las cuerdas casi verticales (apice a 3000 mm, caso mas favorable): 2.1 mm entre la superficie de la cuerda y el nodo (piso de altura 220 mm).

## Ø300

Largo ensamblado del riel: 310.0 mm (punta a punta, x = ±155.0). Centro de la varilla a z = -97.35, fondo del riel z = -57.35.

### Interferencias entre piezas del nodo (nominal)

| Pieza A | Pieza B | mm3 |
|---|---|---|
| cilindro libre perilla gancho +X | M10 carro +X | 4466.03 |
| cilindro libre perilla gancho -X | M10 carro -X | 4466.03 |
| M9 gancho +X | capsula M4-M7 +X | 2235.33 |
| M9 gancho -X | capsula M4-M7 -X | 2235.33 |
| M12 perilla -X | M10 carro -X | 2146.72 |
| M12 perilla +X | M10 carro +X | 2146.72 |
| M3 riel central | M10 carro -X | 1462.40 |
| M3 riel central | M10 carro +X | 1450.40 |
| M9 gancho +X | M10 carro +X | 1153.56 |
| M9 gancho -X | M10 carro -X | 1153.56 |
| M13 casquillo -X | capsula M4-M7 -X | 384.23 |
| M13 casquillo +X | capsula M4-M7 +X | 384.23 |
| cilindro libre perilla gancho +X | capsula M4-M7 +X | 110.94 |
| cilindro libre perilla gancho -X | capsula M4-M7 -X | 110.94 |
| tapa_bolsillo_n | M10 carro -X | 102.00 |
| tapa_bolsillo_n | M10 carro +X | 102.00 |
| tapa_bolsillo_s | M10 carro +X | 102.00 |
| tapa_bolsillo_s | M10 carro -X | 102.00 |
| lastre pletina_0 | M10 carro -X | 95.00 |
| lastre pletina_1 | M10 carro -X | 95.00 |
| lastre pletina_2 | M10 carro -X | 95.00 |
| lastre pletina_3 | M10 carro -X | 95.00 |
| lastre pletina_3 | M10 carro +X | 95.00 |
| lastre pletina_4 | M10 carro +X | 95.00 |
| lastre pletina_5 | M10 carro +X | 95.00 |
| lastre pletina_6 | M10 carro +X | 95.00 |
| lastre pletina_7 | M10 carro +X | 95.00 |
| lastre pletina_7 | M10 carro -X | 95.00 |
| lastre pletina_2 | M10 carro +X | 50.35 |
| lastre pletina_6 | M10 carro -X | 50.35 |
| lastre pletina_0 | M10 carro +X | 44.65 |
| lastre pletina_4 | M10 carro -X | 44.65 |
| M14 pestillo +X | capsula M4-M7 +X | 25.18 |
| M14 pestillo -X | capsula M4-M7 -X | 25.18 |

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M12 perilla +X | 504.99 | 2146.72 | 0.00 |
| M10 carro +X | M13 casquillo +X | 251.47 | 0.00 | 0.00 |
| M10 carro +X | M14 pestillo +X | 295.07 | 0.00 | 0.00 |
| M10 carro +X | M3 riel central | 0.00 | 1450.40 | 4250.40 |
| M10 carro +X | M9 gancho +X | 11778.54 | 1153.56 | 0.00 |
| M10 carro +X | cilindro libre perilla gancho +X | 2007.46 | 4466.03 | 0.00 |
| M10 carro +X | lastre pletina_0 | 0.00 | 44.65 | 491.15 |
| M10 carro +X | lastre pletina_2 | 0.00 | 50.35 | 553.85 |
| M10 carro +X | lastre pletina_3 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_4 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_5 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_6 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | lastre pletina_7 | 0.00 | 95.00 | 1045.00 |
| M10 carro +X | tapa_bolsillo_n | 0.00 | 102.00 | 702.00 |
| M10 carro +X | tapa_bolsillo_s | 0.00 | 102.00 | 702.00 |
| M10 carro -X | M12 perilla -X | 504.99 | 2146.72 | 0.00 |
| M10 carro -X | M13 casquillo -X | 251.47 | 0.00 | 0.00 |
| M10 carro -X | M14 pestillo -X | 295.07 | 0.00 | 0.00 |
| M10 carro -X | M3 riel central | 0.00 | 1462.40 | 4250.40 |
| M10 carro -X | M9 gancho -X | 11778.54 | 1153.56 | 0.00 |
| M10 carro -X | cilindro libre perilla gancho -X | 2007.46 | 4466.03 | 0.00 |
| M10 carro -X | lastre pletina_0 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_1 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_2 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_3 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | lastre pletina_4 | 0.00 | 44.65 | 491.15 |
| M10 carro -X | lastre pletina_6 | 0.00 | 50.35 | 553.85 |
| M10 carro -X | lastre pletina_7 | 0.00 | 95.00 | 1045.00 |
| M10 carro -X | tapa_bolsillo_n | 0.00 | 102.00 | 702.00 |
| M10 carro -X | tapa_bolsillo_s | 0.00 | 102.00 | 702.00 |
| cilindro libre perilla carro +X | M12 perilla +X | 4705.81 | 0.00 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho +X | 825.53 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M12 perilla -X | 4705.81 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho -X | 825.53 | 0.00 | 0.00 |

### Nodo contra la linterna (apice 400)

| Pieza | Linterna | mm3 |
|---|---|---|
| capsula M4-M7 +X | aro | 1054.65 |
| capsula M4-M7 -X | aro | 1054.65 |
| capsula M4-M7 -X | red | 614.66 |
| capsula M4-M7 +X | red | 614.66 |
| M9 gancho -X | red | 96.31 |
| M9 gancho +X | red | 96.31 |
| M13 casquillo -X | red | 55.56 |
| M13 casquillo +X | red | 55.56 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 2403.0 mm3 (tilt 90); red 1263.7 mm3 (tilt 90); M14 pestillo +X 379.4 mm3 (tilt 0); M13 casquillo +X 4.5 mm3 (tilt 90) |
| 50 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 3365.4 mm3 (tilt 0); aro 3023.3 mm3 (tilt 60); red 1761.0 mm3 (tilt 70); cilindro libre perilla gancho +X 1115.1 mm3 (tilt 0); M13 casquillo +X 954.3 mm3 (tilt 60); M14 pestillo +X 172.8 mm3 (tilt 0); M12 perilla +X 72.6 mm3 (tilt 0) |
| 100 | [50, 60, 70, 80, 90] | [0, 10, 20, 30, 40] | cilindro libre perilla gancho +X 5056.9 mm3 (tilt 0); M12 perilla +X 2634.2 mm3 (tilt 0); M9 gancho +X 0.1 mm3 (tilt 20) |

### Apice minimo de las cuerdas

Altura minima del apice sobre el aro para 10 mm de aire entre cuerda y cualquier pieza del nodo: **535 mm** (piso: 220 mm = techo del nodo + 10). 

## Ø500

Largo ensamblado del riel: 480.0 mm (punta a punta, x = ±240.0). Centro de la varilla a z = -97.35, fondo del riel z = -57.35.

### Interferencias entre piezas del nodo (nominal)

| Pieza A | Pieza B | mm3 |
|---|---|---|
| M9 gancho -X | capsula M4-M7 -X | 1305.77 |
| M9 gancho +X | capsula M4-M7 +X | 1305.77 |
| M13 casquillo -X | capsula M4-M7 -X | 628.99 |
| M13 casquillo +X | capsula M4-M7 +X | 628.99 |
| cilindro libre perilla gancho +X | capsula M4-M7 +X | 230.42 |
| cilindro libre perilla gancho -X | capsula M4-M7 -X | 230.42 |
| cilindro libre perilla gancho -X | M10 carro -X | 76.82 |
| cilindro libre perilla gancho +X | M10 carro +X | 76.82 |

### Carro y cilindro libre de su perilla contra el resto, segun s

| Par | s=0 | s=50 | s=100 |
|---|---|---|---|
| M10 carro +X | M12 perilla +X | 3574.24 | 0.00 | 0.00 |
| M10 carro +X | M13 casquillo +X | 496.24 | 0.00 | 0.00 |
| M10 carro +X | M9 gancho +X | 9839.49 | 0.00 | 0.00 |
| M10 carro +X | cilindro libre perilla gancho +X | 6920.26 | 76.82 | 0.00 |
| M10 carro -X | M12 perilla -X | 3574.24 | 0.00 | 0.00 |
| M10 carro -X | M13 casquillo -X | 496.24 | 0.00 | 0.00 |
| M10 carro -X | M9 gancho -X | 9839.49 | 0.00 | 0.00 |
| M10 carro -X | cilindro libre perilla gancho -X | 6920.26 | 76.82 | 0.00 |
| cilindro libre perilla carro +X | M12 perilla +X | 1086.36 | 0.00 | 0.00 |
| cilindro libre perilla carro +X | M9 gancho +X | 302.83 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M12 perilla -X | 1086.36 | 0.00 | 0.00 |
| cilindro libre perilla carro -X | M9 gancho -X | 302.83 | 0.00 | 0.00 |

### Nodo contra la linterna (apice 400)

| Pieza | Linterna | mm3 |
|---|---|---|
| capsula M4-M7 +X | red | 837.78 |
| capsula M4-M7 -X | red | 837.78 |
| capsula M4-M7 -X | aro | 224.70 |
| capsula M4-M7 +X | aro | 224.70 |
| M9 gancho +X | red | 96.28 |
| M9 gancho -X | red | 96.28 |
| M13 casquillo -X | red | 55.52 |
| M13 casquillo +X | red | 55.52 |

### Barrido de bisagra (capsula +X, tilt 0 a 90, paso 10)

| s | Tilts libres | Tilts con choque | Choques (peor tilt) |
|---|---|---|---|
| 0 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | M9 gancho +X 3115.4 mm3 (tilt 80); red 1229.4 mm3 (tilt 70); M13 casquillo +X 643.1 mm3 (tilt 90); M14 pestillo +X 576.5 mm3 (tilt 0); aro 330.8 mm3 (tilt 40) |
| 50 | ninguno | [0, 10, 20, 30, 40, 50, 60, 70, 80, 90] | cilindro libre perilla gancho +X 5331.6 mm3 (tilt 0); M9 gancho +X 3532.5 mm3 (tilt 0); M12 perilla +X 2790.2 mm3 (tilt 0); aro 1197.8 mm3 (tilt 30); red 837.8 mm3 (tilt 40); M13 casquillo +X 629.0 mm3 (tilt 40); M14 pestillo +X 522.4 mm3 (tilt 0) |
| 100 | [20, 30, 40, 50, 60, 70, 80, 90] | [0, 10] | cilindro libre perilla gancho +X 3604.2 mm3 (tilt 0); M12 perilla +X 1527.9 mm3 (tilt 0) |

### Apice minimo de las cuerdas

Altura minima del apice sobre el aro para 10 mm de aire entre cuerda y cualquier pieza del nodo: **273 mm** (piso: 220 mm = techo del nodo + 10). 
