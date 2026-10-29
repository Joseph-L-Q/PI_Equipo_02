# Fase C, caja central (generado por `fase_c_caja.py`)

Layout de 1 piso. STL y STEP en `salida/preliminar/`: NO LISTO PARA IMPRIMIR hasta medir la electrónica y los prensaestopas (Fase H).

| Pieza | BRep/BOP | Sólidos | STL estanco | Cuerpos | bbox mm | Cabe | Voladizo mm² | Espesor mín p1 / mín mm | Relleno | Masa g | Orientación | Soportes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| M1_caja_cuerpo | ok | 1 | sí | 1 | 159.6 × 126.0 × 50.0 | sí | 651 | 1.50 / 1.50 | 100 % | 273 | boca arriba, fondo en la cama | sin soportes; la falda de la brida es a 45° |
| M2_caja_tapa | ok | 1 | sí | 1 | 159.6 × 126.0 × 63.0 | sí | 2007 | 2.90 / 2.88 | 100 % | 164 | cara interior (ranura) en la cama, asa arriba | sin soportes; techo de la ventana del asa a 45° |
| M11_bandeja | ok | 1 | sí | 1 | 127.6 × 94.0 × 18.0 | sí | 0 | 3.00 / 2.19 | 40 % | 41 | plana | sin soportes |

El espesor mínimo se mide con rayos hacia adentro desde 1500 caras al azar; el percentil 1 es el criterio (≥ 1.2). El mínimo absoluto suele caer en aristas y redondeos.
