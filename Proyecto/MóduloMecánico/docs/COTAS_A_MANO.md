# Cotas que hay que poner a mano en los planos de Onshape

Versión del 2026-11-04 (noche). Es la lista única: junta lo que el script de planos no pudo acotar (`salida/planos_onshape/COTAS_A_MANO_A4_v4.md`) y la sección "Cotas que hay que agregar a mano" de `PENDIENTES.md`, y la pone al día con los cambios de hoy (mínimo de 5 mm en lo esbelto, nodo sin soportes, marco de lastre M3f).

## Cómo leerla

- **Cambió hoy**: la geometría de la pieza se modificó el 04/11. Los planos A4 anteriores (v4) y sus notas **pueden estar viejos**: no copie cotas del v4 sin comprobarlas contra el modelo. Las separaciones entre nervios, los espesores y las posiciones de los agujeros cambiaron.
- **Sin cambios**: el plano del 31/10 sigue valiendo.
- **Chaflán**: el script de planos no pone la cota de chaflán. En cada pieza se da el texto para escribir a mano, en la vista donde se vea la arista (normalmente la frontal o la lateral), con la herramienta de cota de chaflán de Onshape: `45° × valor`. El valor sale de `params.py` (`chaflan.base_boya` para la boya, `chaflan.base_soportes` para el nodo); si el chaflán chocó con otra cosa, el programa lo bajó, y entonces vale lo que mida el modelo.
- Todas las medidas de abajo están en mm.

## Boya

### B1_casco: cambió hoy
- Ancho total **132** y ancho **131** de la vista superior (bordes curvos: el script no los acota).
- Brida de unión: **5 + 5**; columnas del canal y almohadillas: **16** de ancho.
- Pin de alineación **Ø5** y su alojamiento **Ø5.4**; lengüeta de **6 × 6 × 4** y su ranura (hoy son la misma pieza girada 180°: acote la lengüeta de un lado y la ranura del otro).
- 4x Ø10 (postes), 6x Ø3.4 de la unión, 2x **Ø83** (sillas) en la lateral, ranura del cuello (Ø35.3, sale del cálculo: léala del modelo), espesor de pared (2.4).
- Costillas de **5**. El v4 traía "separación 5 / 49.5 / 58.5" entre nervios: rehágalas.
- Chaflán: **45° × 4** en postes; **45° × 1** en las costillas sobre el patín; collar de los postes **45° × 3**.

### B2_cubierta_lisa y B2_cubierta_mastil: cambió hoy
- Alto total (117.4 la lisa, 140.4 la del mástil: bordes curvos).
- Barras de **14 × 8**; las separaciones entre barras del v4 (14, 42.5, 56.5, 6, 7) ya no valen.
- 4x Ø4 y 4x Ø3.4 (posiciones al borde), 2x Ø12 (columnas), 2x Ø10 (pilares).
- Solo mástil: **Ø18** exterior, **Ø8** interior, Ø7 del pigtail a 20 del borde.
- Chaflán: **45° × 4** en pilares, columnas y mástil.

### B3_caja: cambió hoy
- Orejas de **14 × 14 × 5**; 4x Ø3.4 arriba; 18x Ø4 (insertos de la brida y postes); postes de la bandeja y del portabaterías **Ø9** (la nota de chaflanes del plano viejo dice Ø8: corregir).
- 4x Ø12.6 (PG7) y Ø12.6 en la lateral.
- Chaflán: **45° × 3** en el piso de la caja y en las orejas; chaflán de la brida (45°, abajo).

### B4_tapa: cambió hoy (antes figuraba "sin cambios")
- Espesor total **6.5**; bajo la ranura quedan **5**; ranura de 2.6 × 1.5; 10x Ø3.4. El plano del 31/10 ya **no vale**.
- Chaflán: no lleva.

### B5_cuna_base y B5_cuna_cuello: cambió hoy
- Alto total (114.6 el v4: revisar), 2x Ø83 en la frontal, 4x Ø4 en frontal y superior, 2x Ø10 (postes de correa).
- Espesor de costillas **5** (el v4 decía 4); lengüeta de la cuna **12 × 14**; brida **5 + 5**; lengüeta vertical de unión (en B5 no hay pin).
- Solo cuello: ranura del cuello (Ø35.3, léala del modelo).
- Chaflán: **45° × 4** en postes y lengüetas; **45° × 1** en costillas sobre el patín. (B2 y B5 en mitades: nunca se acotó el chaflán.)

### B6_correa: cambió hoy
- Espesor **5** y ancho **14** (antes 14 × 4); 2x Ø3.4 a 7 del borde (centros a 91.8).
- Chaflán: no lleva (pieza plana).

## Nodo

### M1s_caja_cuerpo: cambió hoy
- 4x Ø5.6 (insertos M4 del cojín) y **Ø30** en la lateral; paredes y fondo de **5**; caja de 129 × 128 × 78.
- **Nuevas**: 4 orejas del marco de lastre de **20 × 14 × 12** con inserto Ø4 ciego (posiciones x = ±45, y = ±71); ventana de 24 × 18 con techo a 45° (**7**).
- La nota de chaflanes del plano viene de los datos del 01/11 (riel viejo): reescribirla.
- Chaflán: bosses de la bandeja **45° × 1.5**; falda bajo la brida **45°** (el paso a la brida); techo de la ventana **45° × 7**.

### M2_caja_tapa: cambió hoy (antes "sin cambios")
- Alto total **85.5** (la tapa más el asa, que ahora mide **60**); ojo Ø10 en gota; PG7 Ø12.6; 12x Ø3.4; ranura del cordón 2.6 × 1.5.
- Chaflán: planos a 45° del techo de la ventana del asa (apertura de 90, plano de 10).

### M3s_riel_gancho: cambió hoy
- Alto **79.4** en la frontal; 4x Ø4.2 y **Ø8** en la lateral; 4x Ø3.4 y 4x Ø6.5 de la almohadilla; asiento del gancho Ø8.8.
- **Nuevas**: 2 costillas de apoyo de **6** bajo el riel; pared del gancho **5**; techo del canal con chaflán de **8**.
- Chaflán: **45° × 8** en las dos esquinas de arriba del canal.

### M3f_marco_bolsillo: pieza nueva (sin plano)
- Hay que hacer el plano completo. Caja de 117 × 77 × 30; paredes de **5**; 2x Ø3.4 en las orejas y 2x Ø4.0 de los insertos de la placa.
- Chaflán: **45°** en la base de las orejas y de las paredes; valor entre 1.5 y 2 (`chaflan.base_soportes`): medirlo en el modelo.

### M3t_tapa_bolsillo: cambió hoy (antes "sin cambios")
- Placa de **117 × 61 × 5** (antes 107 × 35 × 3); 2x Ø3.4 avellanados. El plano del 31/10 ya **no vale**.
- Chaflán: no lleva (plana).

### M4_capsula_cuerpo: cambió hoy
- Casi todo es curvo, así que casi todo va a mano: Ø12.6 arriba; 3x Ø1.8, Ø16.4 y Ø30.4 en la lateral; Ø26 del anillo LED; espesor de pared **5**; brida de **6**.
- Chaflán: falda **45°** bajo la brida (valor: medirlo en el modelo).

### M5s_capsula_tapa_pie: cambió hoy
- Ancho total y alto total (bordes curvos); 2x Ø4.2; 4x Ø4 y 4x Ø3.4; tapa de **6**; placa de silla de 10.
- Chaflán: **45°** en el pie y el alma; valor entre 1.5 y 2 (`chaflan.base_soportes`): medirlo en el modelo.

### M6_capsula_bisel y M7_capsula_ventana: sin cambios
- M6 faltan Ø exterior **42** y espesor **2.5**. Plano del 31/10.

### M11_bandeja: posible cambio hoy (repisa de la cuna de 5)
- Alto **30** en frontal y lateral; 4x Ø3.4; 4x Ø8.
- Chaflán: bosses **45° × 1.5**.

### M11_bandeja_sup: sin cambios
- Plano completo; solo el espesor 3 si se pide.

### SKIN_concha: sin cambios
- Alto general **5.5** en frontal y lateral (el tope de la costilla es inclinado y el script no lo acota).

## Revisar a ojo en todos los planos nuevos
- Textos de diámetro encima de una línea de cota vecina (en M1s y B1 pasa).
- Casilla SHEET: la API no la llena; corregir "11" por "1 of 1".
- Borrar a mano los estudios y dibujos "OLD" (la API no borra). Ver `PENDIENTES.md`.
