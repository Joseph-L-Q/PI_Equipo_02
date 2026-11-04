# MÁRGENES DE SEGURIDAD (04/11/2026)

Reglas: ninguna pieza pasa de **230 × 230 mm** en X o Y en su orientación de impresión (`impresora.cama_util`; `build.py` falla si alguna se pasa, con `cama.py`). Pared mínima **2.4 mm** en lo no estructural. **4 mm** mínimo en todo elemento vertical esbelto (alto/espesor > 8) o cargado, con chaflán en la base. FS objetivo **≥ 3 entre capas** en lo estructural.

Pared medida en el STL: percentil 1 del espesor local, con 3000 rayos hacia adentro. El mínimo absoluto lo dan las puntas de chaflán y los bordes de agujero, que no son paredes. Antes = commit `1fc425c` (antes de los cambios del 04/11).

## Boya PET 4 × 1 L

| Pieza | Caja X × Y (mm) | Cabe en 230 | Pared p1 antes → después | Elemento más esbelto: antes → después (alto/espesor) | Nota |
|---|---|---|---|---|---|
| B1_casco | 254 × 226 → 132 × 226 | sí | 2.00 → 2.40 | varilla de costilla intermedia 2.4 x 3 mm (lado canal) (17.3) → poste M3 Ø10 libre sobre la silla, con collar (6.8) | 2.4 = paredes laterales con ventanas (no estructurales). Costillas 3 → 4 mm; varillas de 2.4 × 3 mm eliminadas (topes bajos). |
| B2_cubierta_lisa | 254 × 226 → 127 × 226 | sí | 3.00 → 3.99 | columna del panel Ø12 (9.1) → columna del panel Ø12, con chaflán (9.1) | Barras de 4 mm. |
| B2_cubierta_mastil | 254 × 226 → 127 × 226 | sí | 3.00 → 2.99 | columna del panel Ø12 (9.1) → columna del panel Ø12, con chaflán (9.1) | 3.0 = pared del mástil (Ø14 / Ø8). |
| B3_caja | 167 × 117 → 167 × 117 | sí | 2.00 → 2.18 | — | Postes de la bandeja Ø8 → Ø9: el anillo alrededor del inserto Ø4 pasa de 2.0 a 2.5 (la malla facetada lo mide 2.2). Paredes de 2.4 = placas apoyadas en sus 4 bordes. |
| B4_tapa | 167 × 109 → 167 × 109 | sí | 2.50 → 2.50 | — | 2.5 bajo la ranura de la junta. |
| B5_cuna_base | 254 × 115 → 127 × 118 | sí | 2.00 → 2.40 | varilla de costilla intermedia 2.4 x 3 mm (17.3) → poste de correa Ø10 (libre sobre la pared) (3.2) | 2.4 = paredes laterales (no estructurales). Postes de correa Ø8 → Ø10. |
| B5_cuna_cuello | 254 × 115 → 127 × 118 | sí | 2.00 → 2.40 | varilla de costilla intermedia 2.4 x 3 mm (17.3) → poste de correa Ø10 (libre sobre la pared) (3.2) | Igual que el lado base. |
| B6_correa | 14 × 104 → 14 × 106 | sí | 4.00 → 4.00 | — |  |

## Nodo P2 robusto (riel cerrado, 04/11)

| Pieza | Caja X × Y (mm) | Cabe en 230 | Pared p1 | Nota |
|---|---|---|---|---|
| M1s_caja_cuerpo | 147 × 146 | sí | 2.25 | 2.0 en los techos de los bolsillos de lastre (fuera del volumen seco, no estructural). Ventana 24 × 18 al canal del riel en cada extremo (sin PG7). |
| M2_caja_tapa | 63 × 146 | sí | 3.50 |  |
| M3s_riel_gancho | 142 × 79 | sí | 1.90 | Riel cerrado 36 × 30, paredes 6, sin ventanas. FS entre capas 2.72 → 3.18 (alma del gancho 20 → 26). El 1.9 medido es el labio de 1.5 entre la ranura de la junta y el canal (1.6 de alto), no una pared. |
| M3t_tapa_bolsillo | 117 × 57 | sí | 3.00 |  |
| M5s_capsula_tapa_pie | 51 × 64 | sí | 1.50 | Silla de 10 con 4 insertos M3 y junta; tapa 5 → 6. FS entre capas 2.47 → 3.80. El 1.5 medido es el labio entre la ranura de la junta y el pase del cable (1.6 de alto), no una pared. |
| M11_bandeja | 115 × 114 | sí | 2.29 | 2.3 en la bandeja (no estructural, dentro de la caja). Postes pasantes para el M3 × 38; sin la ventana en ocho. |
| M11_bandeja_sup | 115 × 114 | sí | 3.00 |  |
| M4_capsula_cuerpo | 45 × 64 | sí | 1.20 | 1.2 = tubo separador de luz del aro LED (óptico, no estructural). No se puede engrosar sin cambiar el aro: el agujero Ø19 del aro limita el diámetro exterior del tubo. Se ajusta cuando se mida el aro comprado (`aro_led.agujero`). |
| M6_capsula_bisel | 42 × 42 | sí | 2.25 | 2.25 en el borde del bisel (no estructural). |
| M7_capsula_ventana | 30 × 30 | sí | 3.00 |  |

## Fuera de la cama útil

- `M1m_caja_riel` de P3 y P4 (monocasco: caja y riel en una pieza) mide 250 mm. No se imprime ahora (la piscina usa P2). P3/P4 siguen con el riel anterior: si P4 se presenta impreso, hay que llevarle el riel cerrado y partirlo.

## FS entre capas (FEM local, CalculiX)

| Pieza | FS a lo largo | FS entre capas | Objetivo ≥ 3 |
|---|---|---|---|
| M3s riel cerrado (agua 150 N) | 6.50 | 3.18 | **sí** (antes, en celosía: 5.56 / 2.72) |
| M3s riel cerrado (izado 150 N) | 11.19 | 5.47 | **sí** |
| M5s pie de la tapa de cápsula | 7.77 | 3.80 | **sí** (antes 5.04 / 2.47) |
| Boya (B1 a B6) | — | — | sin FEM local: cargas bajas (flotación); el análisis de SimScale de B2 y B3 va en el bloque 3 |

El 04/11 se aplicó la corrección de concepto: riel cerrado y un solo volumen seco. Todo lo estructural del nodo P2 cumple FS ≥ 3 entre capas (FEM local con CalculiX, `salida/prototipos/P2_robusto/fem/fem.json`).
