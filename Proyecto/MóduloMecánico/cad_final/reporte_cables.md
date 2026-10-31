# Recorrido del Cat5e por cámara (generado por `cables.py`)

Por cámara: 60 de holgura en la caja + 25 de prensaestopas + tramo por el riel + bucle hasta el PG7 de la cápsula + 30 dentro de la cápsula + 30 de holgura. El bucle es el mayor entre 40 y la distancia en línea recta de la salida al PG7 de la cápsula, en el peor caso del recorrido del carro (±50) y de la inclinación (0 a 90°): es un mínimo, el cable además se curva. Tramo por el riel: curva de 90° con R25 en la cámara (39.3) + recto hasta la punta del tramo central (33.8) + extensiones hasta la ranura de salida (a 20 de la punta). Sin extensiones sale por la punta abierta del tramo central.

| Aro | Extensiones por lado | Tramo por el riel mm | Bucle mm | Total por cámara mm | Cable de fábrica (300) alcanza | Nota |
|---|---|---|---|---|---|---|
| Ø100 | 0 | 98 | 127 | 370 | no | requiere prueba en banco SPI a 8 y 4 MHz |
| Ø200 | 1 | 198 | 127 | 470 | no | requiere prueba en banco SPI a 8 y 4 MHz |
| Ø300 | 1 | 198 | 127 | 470 | no | requiere prueba en banco SPI a 8 y 4 MHz |
| Ø500 | 2 | 298 | 127 | 570 | no | requiere prueba en banco SPI a 8 y 4 MHz |

Medidas estimadas: diámetro del Cat5e, radio de curvatura (se usa el mayor entre 4 × D y 25) y largo del domo del PG7, que fija dónde empieza la curva.
