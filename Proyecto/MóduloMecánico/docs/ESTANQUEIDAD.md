# Estanqueidad: sellos del concepto vigente

> **Concepto vigente antes de la corrección 3a; se actualiza cuando llegue.**

Lista de lo que mantiene seco cada volumen. Los números de la última columna son los de `GUIA_PIEZAS_LanternGuard.pdf` / `GUIA_PIEZAS.md`. Se genera con `cad_final/guia_piezas.py`; datos en `salida/guia_piezas/sellos.json`.

| N° | Sello | Piezas | Tipo | Qué protege | Dónde lo ves en la guía |
|---|---|---|---|---|---|
| 1 | Tapa B4 sobre la caja seca B3 | B3, B4 | cordón O-ring Ø2 en ranura | La electrónica de la boya: PCB, Waveshare, portabaterías 3×18650 y RTC. | B4 N° 2; B4 N° 1; B3 N° 8 |
| 2 | PG7 del umbilical en B3 (pared −X) | B3 | prensaestopas PG7 (Ø12.6) con contratuerca | El paso del cable umbilical (boya ↔ nodo) hacia la caja seca. | B3 N° 5 |
| 3 | PG7 del cable solar en B3 (pared +X) | B3 | prensaestopas PG7 (Ø12.6) con contratuerca | El paso del cable del panel solar hacia la caja seca. | B3 N° 6 |
| 4 | PG7 del pigtail de antena en B3 (pared +X) | B3, B2 mástil | prensaestopas PG7 (Ø12.6) con contratuerca | El paso del pigtail de la antena hacia la caja seca. El mástil de B2 solo guía el cable: no sella. | B3 N° 7; B2 mástil N° 5 |
| 5 | Insertos M3 de la brida de B3 | B3 | inserto térmico ciego (no atraviesa la brida) | La brida no queda perforada y los tornillos quedan fuera del cordón: el agua no tiene camino por los tornillos. | B3 N° 2 |
| 6 | Botellas PET selladas (flotación) | B1, B5 base, B5 cuello | tapón de rosca de fábrica (botella comprada) | El aire que flota la boya. El casco impreso NO es estanco: solo sostiene las botellas. | B1 N° 9; B1 N° 10; B5 cuello N° 5 |
| 7 | Tapa M2 sobre la caja M1s | M1s, M2 | cordón O-ring Ø2 en ranura | La electrónica del nodo (bandejas M11) en la caja seca. | M2 N° 2; M2 N° 1; M1s N° 6 |
| 8 | PG7 de cada cámara en las paredes de extremo de M1s (×2) | M1s, M3s | prensaestopas PG7 (Ø12.6) con contratuerca | El paso del Cat5e de cada cámara a la caja seca. El conducto del riel va inundado: el sello es el PG7, no el riel. | M1s N° 4; M3s N° 2 |
| 9 | PG7 del umbilical en la tapa M2 | M2 | prensaestopas PG7 (Ø12.6) con contratuerca | El paso del umbilical hacia la caja seca del nodo. | M2 N° 3 |
| 10 | Insertos M3 de la brida de M1s y M4 del cojín | M1s | inserto térmico ciego | No perforan la caja: los 12 M3 de la tapa quedan fuera del cordón y los 8 M4 del cojín no pasan la pared. | M1s N° 5; M1s N° 3 |
| 11 | Tapa M5s sobre la cápsula M4 (×2 cápsulas) | M4, M5s | cordón O-ring Ø2 en ranura | La cámara Arducam y el anillo LED dentro de cada cápsula. | M5s N° 2; M5s N° 1; M4 N° 1 |
| 12 | PG7 de cada cápsula en M4 (×2) | M4 | prensaestopas PG7 (Ø12.6) con contratuerca | El paso del Cat5e hacia el interior de la cápsula (cámara y LED). | M4 N° 2 |
| 13 | Ventana de acrílico M7 en el frente de M4 (×2) | M4, M6 | asiento Ø30.4 con sellador (a definir) | El frente de la cápsula: la ventana deja pasar la luz y no el agua. A confirmar: el CAD solo define el asiento y el bisel M6 con 3 M2; no hay sellador especificado. | M4 N° 3; M6 N° 2; M6 N° 1 |

## Lo que NO es estanco a propósito

- Conducto del riel M3s: va inundado a propósito (el Cat5e tiene chaqueta exterior y entra por PG7 a la caja y a la cápsula).
- Unión riel ↔ caja (4 M4) y pie M5s ↔ riel (2 M4): atornilladas, no estancas.
- Bolsillos de lastre de M1s y sus tapas M3t: fuera del sello, entra agua.
- Casco B1, cunas B5, correas B6 y cubierta B2 de la boya: estructura abierta; flotan las botellas.

## Pendiente

- Sellador o junta de la ventana M7: no está especificado en el CAD.
- Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): el conducto del riel y los PG7 de M1s/M3s se rehacen.
