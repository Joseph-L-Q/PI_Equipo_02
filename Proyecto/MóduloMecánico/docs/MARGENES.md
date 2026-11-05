# MÁRGENES DE SEGURIDAD (04/11/2026)

Reglas: ninguna pieza pasa de **230 × 230 mm** en X o Y en su orientación de impresión (`impresora.cama_util`; `build.py` falla si alguna se pasa, con `cama.py`). Pared mínima **2.4 mm** en lo no estructural. **5 mm** mínimo en todo elemento vertical esbelto (alto/espesor > 8) o cargado, con chaflán en la base. FS objetivo **≥ 3 entre capas** en lo estructural.

Pared medida en el STL: percentil 1 del espesor local, con 3000 rayos hacia adentro. El mínimo absoluto lo dan las puntas de chaflán y los bordes de agujero, que no son paredes. Antes = commit `1fc425c` (antes de los cambios del 04/11).

## Boya PET 4 × 1 L

| Pieza | Caja X × Y (mm) | Cabe en 230 | Pared p1 antes → después | Elemento más esbelto: antes → después (alto/espesor) | Nota |
|---|---|---|---|---|---|
| B1_casco | 254 × 226 → 133 × 226 | sí | 2.00 → 2.40 | varilla de costilla intermedia 2.4 x 3 mm (lado canal) (17.3) → poste M3 Ø10 libre sobre la silla, con collar (6.8) | 2.4 = paredes laterales con ventanas y patín (no estructurales; excepción declarada). Costillas 3 → 4 → 5 mm; varillas de 2.4 × 3 mm eliminadas (topes bajos); brida de unión 5 + 5, columnas de 16, pin Ø5, lengüeta y ranura en las columnas; chaflán de 45° × 3 en la base de postes y costillas. |
| B2_cubierta_lisa | 254 × 226 → 131 × 226 | sí | 3.00 → 3.99 | columna del panel Ø12 (9.3) → columna del panel Ø12, con chaflán (9.3) | Barras de 14 × 8 mm; 4 lengüetas verticales en la barra de la costura; orejas de la caja de 5; pilares Ø10. |
| B2_cubierta_mastil | 254 × 226 → 131 × 226 | sí | 3.00 → 4.00 | columna del panel Ø12 (9.3) → columna del panel Ø12, con chaflán (9.3) | Pared del mástil 3 → 5 (Ø18 / Ø8); mismas barras, pilares y columnas que el lado liso. |
| B3_caja | 167 × 117 → 167 × 117 | sí | 2.00 → 2.15 | — | Postes de la bandeja Ø8 → Ø9: el anillo alrededor del inserto Ø4 pasa de 2.0 a 2.5 (la malla facetada lo mide 2.2). Paredes de 2.4 = placas apoyadas en sus 4 bordes. |
| B4_tapa | 167 × 109 → 167 × 109 | sí | 2.50 → 5.00 | — | Tapa de 6.5 mm: quedan 5 bajo la ranura de la junta (antes 2.5). |
| B5_cuna_base | 254 × 115 → 131 × 119 | sí | 2.00 → 2.40 | varilla de costilla intermedia 2.4 x 3 mm (17.3) → poste de correa Ø10 (libre sobre la pared) (3.2) | 2.4 = paredes laterales (no estructurales). Postes de correa Ø8 → Ø10; lengüeta vertical en vez de pin; lengüetas de 12 × 14. |
| B5_cuna_cuello | 254 × 115 → 131 × 119 | sí | 2.00 → 2.40 | varilla de costilla intermedia 2.4 x 3 mm (17.3) → poste de correa Ø10 (libre sobre la pared) (3.2) | Igual que el lado base. |
| B6_correa | 14 × 104 → 14 × 106 | sí | 4.00 → 5.00 | — | Correa de 14 × 5 (antes 14 × 4). |

## Nodo P2 robusto (riel cerrado, 04/11)

| Pieza | Caja X × Y (mm) | Cabe en 230 | Pared p1 | Nota |
|---|---|---|---|---|
| M1s_caja_cuerpo | 149 × 156 | sí | 2.59 | Paredes y fondo de 5. Sin soportes: el piso es plano porque los bolsillos de lastre pasaron al marco M3f (4 orejas M3 de 20 × 14 × 12); ventana con techo a 45°. Ventana 24 × 18 al canal del riel en cada extremo (sin PG7). |
| M2_caja_tapa | 149 × 148 | sí | 3.50 | Tapa sin girar y sin soportes; asa de 60 con ventana de techo a 45° y ojo en gota. |
| M3s_riel_gancho | 140 × 79 | sí | 2.92 | Riel cerrado 36 × 30, paredes 6, sin ventanas; pared del gancho 5; 2 costillas de apoyo de 6 bajo el riel y techo del canal a 45° (sin soportes casi todo: 12.2 % aceptado). FS entre capas 2.72 → 3.18 (alma del gancho 20 → 26). El 1.9 medido es el labio de 1.5 entre la ranura de la junta y el canal (1.6 de alto), no una pared. |
| M3t_tapa_bolsillo | 117 × 61 | sí | 5.00 | Placa de 5 que cierra el marco M3f (fuera del sello). |
| M5s_capsula_tapa_pie | 52 × 66 | sí | 1.50 | Silla de 10 con 4 insertos M3 y junta; tapa 5 → 6. FS entre capas 2.47 → 3.80. El 1.5 medido es el labio entre la ranura de la junta y el pase del cable (1.6 de alto), no una pared. |
| M3f_marco_bolsillo | 117 × 77 | sí | 5.00 | Marco del bolsillo de lastre (×2), fuera del sello, atornillado a las 4 orejas de M1s; paredes de 5. |
| M11_bandeja | 115 × 114 | sí | 2.29 | 2.3 en la bandeja (no estructural, dentro de la caja). Postes pasantes para el M3 × 38; sin la ventana en ocho. |
| M11_bandeja_sup | 115 × 114 | sí | 3.00 | Bandeja de 3 sin postes propios. |
| M4_capsula_cuerpo | 66 × 66 | sí | 1.20 | Pared de 5, brida de 6, falda a 45° bajo la brida. 1.2 = tubo separador de luz del aro LED (óptico, no estructural). No se puede engrosar sin cambiar el aro: el agujero Ø19 del aro limita el diámetro exterior del tubo. Se ajusta cuando se mida el aro comprado (`aro_led.agujero`). |
| M6_capsula_bisel | 42 × 42 | sí | 2.25 | 2.25 en el borde del bisel (no estructural). |
| M7_capsula_ventana | 30 × 30 | sí | 3.00 |  |

## Elementos esbeltos por pieza (registro con control, `esbelto.py` + `esbelto_nodo.py`)

Cada elemento declarado debe medir al menos **5 mm**; si no, `esbelto.py` sale con error y `build.py` / `boya_pet.py` no construyen. Espesor = lado fino (pared, costilla, oreja, barra) o diámetro (poste, columna).

| Pieza | Elemento | Espesor (mm) | ¿Cumple? |
|---|---|---|---|
| B1_casco | B1/B5 costillas y topes bajos (boya_pet.costilla) | 5.0 | sí |
| B1_casco | B1/B5 brida de union por mitad (boya_pet.union[0]) | 5.0 | sí |
| B1_casco | B1/B5 ancho de columna y almohadilla de union (boya_pet.union[1]) | 16.0 | sí |
| B1_casco | B1/B2 pin de alineacion (boya_pet.union[2]) | 5.0 | sí |
| B1_casco | B1/B2/B5 lengueta de union, seccion (boya_pet.llave[1]) | 6.0 | sí |
| B1_casco | B1/B5 pared de fondo de la ranura de la lengueta (2 brida - salida - holgura) | 5.5 | sí |
| B1_casco | B1 postes M3 de la cubierta (boya_pet.poste_D) | 10.0 | sí |
| B1_casco | B1 parche de amarre (boya_pet.ojal[1]) | 8.0 | sí |
| B2_cubierta_lisa | B1/B2 pin de alineacion (boya_pet.union[2]) | 5.0 | sí |
| B2_cubierta_lisa | B1/B2/B5 lengueta de union, seccion (boya_pet.llave[1]) | 6.0 | sí |
| B2_cubierta_lisa | B2 barras de la cubierta, espesor (boya_pet.cubierta_espesor) | 8.0 | sí |
| B2_cubierta_lisa | B2 barras de la cubierta, ancho (boya_pet.barra_ancho) | 14.0 | sí |
| B2_cubierta_lisa | B2 pilares bajo la caja (boya_pet.pilar[0]) | 10.0 | sí |
| B2_cubierta_lisa | B2 columnas del panel (boya_pet.columna_D) | 12.0 | sí |
| B2_cubierta_lisa | B2 mastil, pared ((D - d) / 2) (boya_pet.mastil) | 5.0 | sí |
| B2_cubierta_mastil | B1/B2 pin de alineacion (boya_pet.union[2]) | 5.0 | sí |
| B2_cubierta_mastil | B1/B2/B5 lengueta de union, seccion (boya_pet.llave[1]) | 6.0 | sí |
| B2_cubierta_mastil | B2 barras de la cubierta, espesor (boya_pet.cubierta_espesor) | 8.0 | sí |
| B2_cubierta_mastil | B2 barras de la cubierta, ancho (boya_pet.barra_ancho) | 14.0 | sí |
| B2_cubierta_mastil | B2 pilares bajo la caja (boya_pet.pilar[0]) | 10.0 | sí |
| B2_cubierta_mastil | B2 columnas del panel (boya_pet.columna_D) | 12.0 | sí |
| B2_cubierta_mastil | B2 mastil, pared ((D - d) / 2) (boya_pet.mastil) | 5.0 | sí |
| B3_caja | B3 orejas de la caja (boya_pet.oreja[2]) | 5.0 | sí |
| B3_caja | B3 brida de la caja (boya_pet.brida[1]) | 7.0 | sí |
| B3_caja | B3 postes de la bandeja (boya.poste_D) | 9.0 | sí |
| B3_caja | B3 refuerzos del portabaterias (boya.apoyo_bateria_D) | 9.0 | sí |
| B4_tapa | B4 tapa bajo la ranura de la junta (tapa_espesor - ranura_prof) | 5.0 | sí |
| B5_cuna_base | B1/B5 costillas y topes bajos (boya_pet.costilla) | 5.0 | sí |
| B5_cuna_base | B1/B5 brida de union por mitad (boya_pet.union[0]) | 5.0 | sí |
| B5_cuna_base | B1/B5 ancho de columna y almohadilla de union (boya_pet.union[1]) | 16.0 | sí |
| B5_cuna_base | B1/B2/B5 lengueta de union, seccion (boya_pet.llave[1]) | 6.0 | sí |
| B5_cuna_base | B1/B5 pared de fondo de la ranura de la lengueta (2 brida - salida - holgura) | 5.5 | sí |
| B5_cuna_base | B5 lengueta de la cuna, ancho (boya_pet.lengueta[0]) | 12.0 | sí |
| B5_cuna_base | B5 lengueta de la cuna, alto (boya_pet.lengueta[1]) | 14.0 | sí |
| B5_cuna_cuello | B1/B5 costillas y topes bajos (boya_pet.costilla) | 5.0 | sí |
| B5_cuna_cuello | B1/B5 brida de union por mitad (boya_pet.union[0]) | 5.0 | sí |
| B5_cuna_cuello | B1/B5 ancho de columna y almohadilla de union (boya_pet.union[1]) | 16.0 | sí |
| B5_cuna_cuello | B1/B2/B5 lengueta de union, seccion (boya_pet.llave[1]) | 6.0 | sí |
| B5_cuna_cuello | B1/B5 pared de fondo de la ranura de la lengueta (2 brida - salida - holgura) | 5.5 | sí |
| B5_cuna_cuello | B5 lengueta de la cuna, ancho (boya_pet.lengueta[0]) | 12.0 | sí |
| B5_cuna_cuello | B5 lengueta de la cuna, alto (boya_pet.lengueta[1]) | 14.0 | sí |
| B6_correa | B6 correa, espesor (boya_pet.correa[1]) | 5.0 | sí |
| B6_correa | B6 correa, ancho (boya_pet.correa[0]) | 14.0 | sí |
| M1s_caja_cuerpo | M1s pared de la caja | 5.0 | sí |
| M1s_caja_cuerpo | M1s fondo de la caja | 5.0 | sí |
| M2_caja_tapa | M2 barra del asa sobre la ventana | 12.0 | sí |
| M2_caja_tapa | M2 anillo del ojo en la punta de la gota | 5.4 | sí |
| M3s_riel_gancho | M3s costilla de apoyo en la cama | 6.0 | sí |
| M3s_riel_gancho | M3s pared del gancho | 5.0 | sí |
| M3t_tapa_bolsillo | — (sin elementos esbeltos declarados) | — | — |
| M5s_capsula_tapa_pie | — (sin elementos esbeltos declarados) | — | — |
| M3f_marco_bolsillo | M3f pared del bolsillo de lastre | 5.0 | sí |
| M3f_marco_bolsillo | M3f oreja de M1s (ancho) | 20.0 | sí |
| M11_bandeja | M11 repisa de la cuna | 5.0 | sí |
| M11_bandeja_sup | M11 repisa de la cuna | 5.0 | sí |
| M4_capsula_cuerpo | M4 pared de la capsula | 5.0 | sí |
| M6_capsula_bisel | — (sin elementos esbeltos declarados) | — | — |
| M7_capsula_ventana | — (sin elementos esbeltos declarados) | — | — |

Excepciones declaradas (más finas que el mínimo, con su motivo):

- B1/B5 paredes laterales del casco y la cuna (boya_pet.pared): **2.4 mm**. piel de cierre de 6 perimetros (margen.pared_min), sostenida por 5 costillas de 5 mm cada <= 64 mm y con ventanas; no recibe carga. Subirla a 5 cambia el ancho del canal y la altura del casco (decision abierta, ver DECISIONES.md)
- B3 paredes y piso de la caja seca (boya_pet.caja_pared): **2.4 mm**. placas apoyadas en sus 4 bordes y en la brida de 7 mm; la caja es el volumen seco (margen.pared_min)
- B1/B5 patin bajo la botella (boya_pet.pared): **2.4 mm**. placa horizontal de 24 mm de ancho sobre la cama; no es un elemento vertical
- B1/B2/B5 salida de la lengueta (boya_pet.llave[0]): **4 mm**. es un taco de 4 mm de salida y 6 x 16 de base (relacion 0.7): no es esbelto; su espesor es la seccion, registrada arriba

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
