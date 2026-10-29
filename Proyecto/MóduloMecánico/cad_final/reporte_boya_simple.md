# Boya de la version simple, B1s..B6s (generado por `boya_simple.py`)

Decisiones del equipo del 29/10 (chat de Melissa, `params.py` boya.*): caja hermetica de 220 × 200 × 120 exterior (cuerpo; la brida de la tapa sale 10 por lado: 240 × 220), 210 × 190 interior, pared 5; panel 170 × 170 a 25 sobre la tapa, corrido a -X para que la antena LoRa (dentro, en el extremo +X) no quede bajo el panel; 4 flotadores huecos de 100 × 100 × 60 en las esquinas, atornillados con 2 M5 largos cada uno a insertos en cojines de las paredes extremas (la caja no se perfora); PG7 del umbilical en el piso (-X), PG7 del panel en la pared -X, agujero ciego Ø6.5 para un SMA futuro en la pared +X (lejos de los cables), ojal de amarre bajo el extremo +X.

## Piezas

| Pieza | Cant. | Bbox en impresion | Orientacion | Volumen cm³ | Relleno | Masa g | BRep | Estanco |
|---|---|---|---|---|---|---|---|---|
| B1s casco | 1 | 240.0 x 220.0 x 125.0 | X180 | 753.5 | 100 % | 957 | ok | si |
| B2s tapa | 1 | 9.0 x 220.0 x 240.0 | Y+90 | 260.5 | 100 % | 331 | ok | si |
| B1bs bandeja | 1 | 206.0 x 186.0 x 3.0 | sin girar | 113.0 | 40 % | 129 | ok | si |
| B3s larguero del panel | 2 | 24.0 x 170.0 x 21.0 | X180 | 28.4 | 40 % | 26 | ok | si |
| B5s flotador de esquina | 4 | 60.0 x 100.0 x 100.0 | Y+90 | 91.5 | 100 % | 116 | ok | si |
| B6s ojal de amarre | 1 | 30.0 x 24.0 x 26.0 | X180 | 8.3 | 100 % | 11 | ok | si |

Interferencias (piezas y maquetas de bateria, PCB, Waveshare, RTC, antena y panel): ninguna.

## Masa

| Elemento | g | z mm |
|---|---|---|
| B1s casco | 957 | 47 |
| B2s tapa | 331 | 118 |
| B1bs bandeja | 129 | 46 |
| B6s ojal | 11 | -19 |
| B3s larguero 1 | 26 | 140 |
| B3s larguero 2 | 26 | 140 |
| B5s flotador 1 | 116 | 30 |
| B5s flotador 2 | 116 | 30 |
| B5s flotador 3 | 116 | 30 |
| B5s flotador 4 | 116 | 30 |
| 3 x celdas 18650 | 141 | 26 |
| portabaterias | 25 | 26 |
| PCB + Heltec | 35 | 60 |
| Waveshare D | 15 | 52 |
| RTC | 8 | 54 |
| panel solar | 350 | 146 |
| antena LoRa (dentro) | 20 | 82 |
| cables y fusible | 40 | 50 |
| 2 PG7 | 20 | 30 |
| tornilleria (M3, 8 M5 largos, insertos) | 108 | 50 |
| **Total boya** | **2705** | KG = 66.2 |

## Hidrostatica (agua de mar 1025 kg/m³)

| Magnitud | Valor |
|---|---|
| Calado | 31.6 mm |
| Francobordo (hasta la tapa) | **88.4 mm** (minimo 50: CUMPLE) |
| Volumen sumergido / sellado | 2639 / 7763 cm³ |
| Reserva de flotacion | 194 % |
| KB / KG | 15.8 / 66.2 mm |
| BM balanceo / cabeceo | 142 / 518 mm |
| **GM balanceo / cabeceo** | **92 / 467 mm** |

**Peso total nodo + boya: 5168 g** (nodo 2462 g, boya 2705 g) contra 3 kg: **se pasa por 2168 g**.

Estimacion de geometria, no certificacion: masas de componentes estimadas (`boya.masas`, el panel es la mayor incertidumbre), sin oleaje, viento ni tension del umbilical.

## Chequeos que fallaron

- ninguno
