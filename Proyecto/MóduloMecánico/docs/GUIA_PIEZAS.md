# Guía de piezas LanternGuard

> Texto de `GUIA_PIEZAS_LanternGuard.pdf`. Los números coinciden con los de los PNG de `salida/guia_piezas/`.
> Concepto vigente antes de la corrección 3a (lo del riel y del cable en M1s y M3s cambia con ella).

Colores en los PNG: azul = tornillo / unión · naranja = cable · rojo = sello · verde = forma / ahorro de material · morado = alineación · gris = montaje interno.
Medidas: M3 de paso Ø3.4 · inserto M3 Ø4.0 · M4 de paso Ø4.2 · inserto M4 Ø5.6 · piloto M2 Ø1.8 · PG7 Ø12.6 · cordón O-ring Ø2 en ranura de 2.6 × 1.5.
Regenerar: `cd cad_final && ..\.venv\Scripts\python.exe guia_piezas.py`.

# Boya con botellas PET

## B1 · Casco (una mitad)

Estructura que sostiene las botellas PET. Se imprime 2 veces: la segunda mitad es esta misma pieza girada 180° (x = 0 es la unión). Ejes: x a lo largo de las botellas, z arriba.

![B1_casco](../salida/guia_piezas/B1_casco.png)

1. **Tornillos de unión de las mitades** Ø3.4 ×6 _(tornillo / unión)_. Paso M3 (Ø3.4) en x = 0. Seis M3×20 inox con tuerca cruzan las dos bridas de 4 + 4 mm: 4 en las columnas del canal (y = ±19) y 2 en las almohadillas bajas de las paredes (y = ±107).
2. **Pin Ø4 de alineación** Ø4.0 _(alineación / ajuste)_. Pin impreso Ø4 en x = 0 (y = +19, z = 28) que entra en el alojamiento de la otra mitad. Garantiza que las dos mitades coinciden antes de apretar los M3.
3. **Alojamiento del pin** Ø4.4 _(alineación / ajuste)_. Agujero Ø4.4 (pin 4 + holgura 0.2) en y = −19: recibe el pin de la otra mitad.
4. **Pasos M3 hacia las cunas** Ø3.4 ×4 _(tornillo / unión)_. Cuatro pasos M3 (Ø3.4) en la costilla del extremo. Los tornillos vienen de las bahías del casco y se enroscan en los insertos de las lengüetas de las cunas B5.
5. **Insertos M3 de los postes** Ø4.0 ×4 _(tornillo / unión)_. Inserto térmico M3 (Ø4.0 × 6) en la punta de cada poste: reciben los 4 tornillos M3 con que se atornilla la cubierta B2 (cada mitad de B2 va a sus propios 4 postes).
6. **Poste Ø10** Ø10 ×4 _(forma / ahorro de material)_. Cuatro postes Ø10 que nacen del piso y suben hasta el inserto. Pasaron de Ø8 a Ø10 el 04/11; los del medio llevan un collar a 45° donde salen de la silla baja.
7. **Ojal de amarre** Ø10.5 _(cable)_. Agujero Ø10.5 en el parche de la quilla. Hay uno por mitad (x = ±21): el cabo de amarre va en pata de gallo, con dos ramales a un nudo. Es independiente del umbilical.
8. **Canal central** ×2 _(cable)_. Hueco de 50 mm entre las dos bahías (y = ±25), sin costillas. Por aquí baja el cable umbilical y caben el domo del PG7 y la contratuerca de la caja B3.
9. **Silla baja de la botella** Ø83 ×4 _(forma / ahorro de material)_. Ranura en U Ø83 (botella Ø80 + 1.5 de holgura). Desde el 04/11 las costillas intermedias son sillas bajas (≤ 15 mm sobre el patín) y no varillas de 2.4×3. Lo que sujeta la botella hacia arriba son las barras de B2 y las correas.
10. **Ranura del cuello** Ø32 _(forma / ahorro de material)_. Ranura Ø32 en la costilla del extremo (bahía y = −69): por ella asoma el cuello de la botella, unos 21 mm fuera del casco.
11. **Rombo de aligeramiento** _(forma / ahorro de material)_. Ventana en rombo en la costilla del extremo de la base de la botella (bahía y = +69). Ahorra material y, con caras a 45°, se imprime sin puentes.
12. **Ventanas hexagonales** ×4 _(forma / ahorro de material)_. Cuatro ventanas hexagonales en la pared exterior (2 por bahía visible). Aligeran la pared y sirven para inyectar la espuma de poliuretano que da reserva de flotación.
13. **Patín bajo la botella** ×2 _(forma / ahorro de material)_. Piso de 2.4 mm y 24 mm de ancho bajo cada botella: es lo único que toca la botella por abajo. El resto del fondo queda abierto para que escurra el agua.
14. **Chaflán 45° en la base de los soportes** ×4 _(forma / ahorro de material)_. Chaflanes de 45° donde costillas y postes nacen del patín: evitan voladizos y soportes de impresión (corrección de la jefa de práctica).

## B2 · Cubierta, lado liso

Marco de barras que cierra el casco por arriba y sostiene la caja B3 y el panel solar. Cada mitad es un marco cerrado atornillado a sus propios 4 postes. Esta es la que no lleva mástil.

![B2_cubierta_lisa](../salida/guia_piezas/B2_cubierta_lisa.png)

1. **Pasos M3 al casco** Ø3.4 ×4 _(tornillo / unión)_. Cuatro pasos M3 (Ø3.4) en las barras: los tornillos entran a los insertos de los postes de B1 (N° 5 de B1).
2. **Pilares con inserto M3** Ø4.0 ×2 _(tornillo / unión)_. Dos pilares Ø10 × 6 bajo las orejas de la caja. Inserto M3 (Ø4.0): recibe el tornillo que atraviesa la oreja de B3.
3. **Columnas del panel con inserto M3** Ø4.0 ×2 _(tornillo / unión)_. Dos columnas Ø12 que suben 107 mm. Inserto M3 (Ø4.0) en la punta: el panel solar de 170×170 se atornilla a las cuatro columnas (2 por mitad), 25 mm sobre la tapa.
4. **Barras de 14 × 4 mm** ×3 _(forma / ahorro de material)_. Barras que cruzan sobre las botellas: no las dejan salir hacia arriba. Los huecos entre barras son por donde se inyecta la espuma. La barra de x = 0 es nueva: cierra el marco de cada mitad.
5. **Pie a 45° de pilares y columnas** ×4 _(forma / ahorro de material)_. Chaflán de 45° en la base de pilares y columnas sobre las barras (chaflán de la base de soportes): imprime sin soporte.

## B2 · Cubierta, lado mástil

La otra mitad de la cubierta, con el mástil de la antena. Mismos pilares y columnas que el lado liso; la caja y el panel atornillados encima amarran las dos mitades.

![B2_cubierta_mastil](../salida/guia_piezas/B2_cubierta_mastil.png)

1. **Pasos M3 al casco** Ø3.4 ×4 _(tornillo / unión)_. Cuatro pasos M3 (Ø3.4): tornillos hacia los insertos de los postes de B1.
2. **Pilares con inserto M3** Ø4.0 ×2 _(tornillo / unión)_. Dos pilares Ø10 bajo las orejas de la caja: inserto M3 (Ø4.0) para el tornillo de la oreja de B3.
3. **Columnas del panel con inserto M3** Ø4.0 ×2 _(tornillo / unión)_. Dos columnas Ø12 con inserto M3 (Ø4.0) en la punta para el panel solar.
4. **Hueco del mástil Ø8** Ø8.0 _(cable)_. Mástil Ø14 con hueco interior Ø8 desde z = 95 hasta la punta. Por dentro sube el pigtail de la antena (un cable corto con el conector de antena).
5. **Puerto del pigtail Ø7** Ø7.0 _(cable)_. Agujero Ø7 en el mástil hacia la caja: por aquí sale el pigtail y va a un PG7 de la cara +X de B3 (N° 7 de B3).
6. **Barras y barra de costura** ×3 _(forma / ahorro de material)_. Marco de barras de 14 × 4 mm; la barra en x = 0 cierra este marco. Igual que en el lado liso: retiene las botellas y deja huecos para la espuma.
7. **Pie a 45° de pilares y columnas** ×4 _(forma / ahorro de material)_. Chaflán de 45° en la base de pilares, columnas y mástil (chaflán de la base de soportes).

## B3 · Caja seca

Caja hermética de la electrónica de la boya (PCB, Waveshare, portabaterías 3×18650, RTC). Paredes de 2.4 mm con brida de 10 × 7 mm. Se cierra con la tapa B4.

![B3_caja](../salida/guia_piezas/B3_caja.png)

1. **Pasos M3 de las orejas** Ø3.4 ×4 _(tornillo / unión)_. Cuatro orejas de 14×14×4 mm en las esquinas. Un M3 por oreja entra al inserto del pilar de B2 (N° 2 de B2 lisa): así la caja queda fija a la cubierta.
2. **Insertos M3 de la brida** Ø4.0 ×10 _(sello / agua)_. Diez insertos térmicos M3 (Ø4.0 × 6) en la brida de 7 mm. Los tornillos de la tapa B4 los aprietan. Son ciegos (no atraviesan) y quedan afuera del cordón.
3. **Standoffs del portabaterías** Ø4.0 ×4 _(montaje de piezas internas)_. Cuatro standoffs Ø9 con inserto M3: sostienen el portabaterías 3×18650 separado del piso.
4. **Postes de la bandeja** Ø4.0 ×4 _(montaje de piezas internas)_. Cuatro postes Ø9 con inserto M3 en la punta: sostienen la bandeja donde van la PCB y el Waveshare.
5. **PG7 del umbilical** Ø12.6 _(cable)_. Agujero Ø12.6 en la pared −X (z = 30 mm sobre el piso interior). Entra el cable umbilical que baja al nodo; la contratuerca va por dentro y el prensaestopas aprieta el cable. Sella el paso.
6. **PG7 del cable solar** Ø12.6 _(cable)_. Agujero Ø12.6 en la pared +X (y = −25): entra el cable del panel solar.
7. **PG7 del pigtail de antena** Ø12.6 _(cable)_. Agujero Ø12.6 en la pared +X (y = +25): entra el pigtail que viene del mástil de B2 (N° 5 de B2 mástil).
8. **Brida plana con chaflán 45°** ×2 _(sello / agua)_. Brida de 10 mm de ancho y 7 de espesor. Su cara superior, plana, es donde aprieta el cordón de la tapa (ver N° 2 de B4). Abajo lleva un chaflán de 45° para imprimir sin soportes.

## B4 · Tapa de la caja seca

Tapa plana de 4 mm de B3. Se imprime con la ranura hacia arriba (girada 180°). Aquí está el sello que mantiene seca la electrónica.

![B4_tapa](../salida/guia_piezas/B4_tapa.png)

1. **Pasos M3 de la tapa** Ø3.4 ×10 _(tornillo / unión)_. Diez pasos M3 (Ø3.4): los tornillos entran a los diez insertos de la brida de B3 (N° 2 de B3) y comprimen el cordón.
2. **Ranura del cordón O-ring** ×4 _(sello / agua)_. Ranura rectangular de 2.6 mm de ancho × 1.5 de hondo en la cara inferior, 2.8 mm afuera de la pared. Lleva un cordón de goma Ø2 mm (25 % de compresión) que aprieta contra la brida plana de B3.

## B5 · Cuna, lado base

Cuna que sostiene una botella a lo largo de Y en cada extremo del casco. Mitad del lado de la base de la botella; se imprime 2 veces (una por cuna). Aquí x = 0 es la unión con el lado cuello.

![B5_cuna_base](../salida/guia_piezas/B5_cuna_base.png)

1. **Pasos M3 de unión de las mitades** Ø3.4 ×2 _(tornillo / unión)_. Dos pasos M3 (Ø3.4) en almohadillas bajas en x = 0: un M3 por lado une esta mitad con la del cuello (brida 4 + 4 mm).
2. **Insertos M3 de las lengüetas** Ø4.0 ×2 _(tornillo / unión)_. Inserto M3 (Ø4.0 × 6, eje en Y) en cada lengüeta de 12 × 14 mm que sale hacia el casco. El tornillo entra desde la bahía de B1, cruza la costilla del extremo (N° 4 de B1) y rosca aquí.
3. **Insertos M3 de los postes de correa** Ø4.0 ×2 _(tornillo / unión)_. Dos postes Ø10 (corridos 1 mm afuera para no tocar la botella) con inserto M3: reciben los tornillos de la correa B6.
4. **Silla baja de la botella** Ø83 ×2 _(forma / ahorro de material)_. Ranuras en U Ø83 en la costilla del medio y en la de la unión: guían la botella; las correas B6 la sujetan hacia arriba.
5. **Rombo de aligeramiento** _(forma / ahorro de material)_. Ventana en rombo en la costilla del extremo de la base de la botella (cerrada: la base de la botella la toca). Ahorra material y se imprime sin puentes.
6. **Ventanas hexagonales** ×4 _(forma / ahorro de material)_. Cuatro ventanas hexagonales (2 por pared): aligeran y dejan inyectar espuma de poliuretano.
7. **Chaflán 45° en la base de los soportes** ×3 _(forma / ahorro de material)_. Chaflanes de 45° en la unión de costillas, lengüetas y postes con el patín: sin voladizos ni soportes.

## B5 · Cuna, lado cuello

La otra mitad de la cuna, la que recibe el cuello de la botella. Se imprime 2 veces. Mismas uniones que el lado base.

![B5_cuna_cuello](../salida/guia_piezas/B5_cuna_cuello.png)

1. **Pasos M3 de unión de las mitades** Ø3.4 ×2 _(tornillo / unión)_. Dos pasos M3 (Ø3.4) en x = 0: unen esta mitad con la del lado base.
2. **Insertos M3 de las lengüetas** Ø4.0 ×2 _(tornillo / unión)_. Inserto M3 (Ø4.0, eje en Y) en cada lengüeta: reciben los tornillos que vienen del casco B1.
3. **Insertos M3 de los postes de correa** Ø4.0 ×2 _(tornillo / unión)_. Dos postes Ø10 con inserto M3 (Ø4.0) para la correa B6.
4. **Silla baja de la botella** Ø83 ×2 _(forma / ahorro de material)_. Ranuras en U Ø83 que guían la botella.
5. **Ranura del cuello** Ø32 _(forma / ahorro de material)_. Ranura Ø32 en la costilla del extremo: por aquí asoma el cuello de la botella.
6. **Ventanas hexagonales** ×4 _(forma / ahorro de material)_. Cuatro ventanas hexagonales (2 por pared): aligeran y dejan inyectar espuma.
7. **Chaflán 45° en la base de los soportes** ×3 _(forma / ahorro de material)_. Chaflanes de 45° en la unión de costillas, lengüetas y postes con el patín.

## B6 · Correa

Cierra cada cuna sobre la botella. Se imprimen 4 (2 por cuna). Va plana sobre la cama.

![B6_correa](../salida/guia_piezas/B6_correa.png)

1. **Pasos M3 en los extremos** Ø3.4 ×2 _(tornillo / unión)_. Dos agujeros M3 (Ø3.4) a 92 mm entre centros: se atornillan a los insertos de los postes de la cuna (N° 3 de B5 base).
2. **Banda plana de 14 × 4 mm** _(forma / ahorro de material)_. Banda que pasa por encima de la botella y la sujeta hacia arriba contra la silla baja de la cuna.

# Nodo de cámaras P2_robusto

## M1s · Caja del nodo (cuerpo)

Caja seca del nodo (127 × 126 × 77 mm exteriores). En los dos extremos lleva el cojín donde se atornilla cada riel; abajo, los bolsillos de lastre. Se cierra con la tapa M2. x a lo largo de los rieles, z arriba.

![M1s_caja_cuerpo](../salida/guia_piezas/M1s_caja_cuerpo.png)

1. **Cojín cuadrado de la pared (el "agujero cuadrado" del costado)** ×2 _(forma / ahorro de material)_. En cada pared de extremo hay un cojín rectangular (casi cuadrado) de 10 mm de espesor y 50 mm de ancho. No es un agujero cuadrado: es una placa en relieve con un agujero redondo (N° 2) y 4 tornillos (N° 3). Da un asiento plano a la brida del riel y refuerza la pared donde se rosca. Hay uno por extremo (×2). Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente.
2. **Agujero redondo Ø30 del cojín** Ø30 ×2 _(cable)_. Ventana de acceso de 30 mm en el cojín. Deja entrar el domo del PG7 (que asoma hacia afuera) y una llave para apretar la contratuerca. Por aquí el cable sale de la caja hacia el conducto del riel (N° 2 de M3s). Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente.
3. **Insertos M4 del cojín** Ø5.6 ×8 _(tornillo / unión)_. Cuatro insertos térmicos M4 (Ø5.6 × 8.5) por cojín, en cuadro de 40 × 20 mm. Son los 4 tornillos que se ven al costado: los M4 de la brida del riel (N° 1 de M3s) entran aquí. Ciegos: no perforan la pared de la caja. Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente.
4. **PG7 de la pared (cámara)** Ø12.6 ×2 _(cable)_. Agujero Ø12.6 para el prensaestopas PG7 en el fondo del Ø30. Por él pasa el cable Cat5e de la cámara (un cable por cápsula: imagen SPI y anillo LED) hacia el interior seco. La contratuerca va dentro (9 mm). Es el sello del cable. Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente.
5. **Insertos M3 de la brida** Ø4.0 ×12 _(sello / agua)_. Doce insertos térmicos M3 (Ø4.0 × 6) en la brida: los 12 tornillos de la tapa M2 los aprietan y comprimen el cordón O-ring. Ciegos y fuera del cordón.
6. **Brida plana: asiento del cordón** ×2 _(sello / agua)_. La cara superior de la brida es plana: contra ella aprieta el cordón de goma Ø2 que va en la ranura de la tapa M2 (ver N° 2 de M2).
7. **Falda a 45° bajo la brida** ×2 _(forma / ahorro de material)_. El paso del cuerpo a la brida es un chaflán a 45°: se imprime sin soportes.
8. **Insertos M3 de los bosses de la bandeja** Ø4.0 ×4 _(montaje de piezas internas)_. Cuatro bosses Ø8 sobre el piso con inserto M3: atornillan la bandeja M11 (en el interior seco). Cada boss, igual que las paredes interiores, nace del piso con un chaflán de 45° (chaflán de la base de soportes).
9. **Insertos M3 de los bolsillos** Ø4.0 ×4 _(tornillo / unión)_. Cuatro insertos M3 (Ø4.0) en el fondo de los bolsillos (2 por bolsillo): ahí se atornillan los M3 avellanados de la tapa M3t.
10. **Bolsillos de lastre** ×2 _(forma / ahorro de material)_. Dos cajones de 100 × 50 × 30 mm bajo el piso (uno por lado), abiertos por abajo y fuera del sello. Llevan las tuercas y arandelas M8 a granel (575 g por bolsillo, 1150 g en total) y se cierran con M3t. Entra agua: es lo normal.

## M2 · Tapa de la caja con asa

Cierra la caja M1s. Lleva el asa para cargar con guante, el ojo de anclaje del cabo y el PG7 del umbilical. Se imprime girada (Y+90). Aquí z crece hacia arriba (asa arriba).

![M2_caja_tapa](../salida/guia_piezas/M2_caja_tapa.png)

1. **Pasos M3 de la tapa** Ø3.4 ×12 _(tornillo / unión)_. Doce pasos M3 (Ø3.4): los tornillos entran a los doce insertos de la brida de M1s (N° 5 de M1s) y aprietan el cordón.
2. **Ranura del cordón O-ring (4 esquinas)** Ø12 ×4 _(sello / agua)_. Ranura rectangular de 2.6 × 1.5 mm en la cara inferior, a mitad de camino entre la cavidad y la línea de tornillos. Cordón de goma Ø2. Se marcan las 4 esquinas redondeadas (R6); la ranura sigue el contorno.
3. **PG7 del umbilical** Ø12.6 _(cable)_. Agujero Ø12.6 en la tapa: entra el cable umbilical que sube a la boya (cable flojo, con curva). Prensaestopas con contratuerca por dentro; es un sello del nodo.
4. **Ojo de anclaje Ø10** Ø10 _(tornillo / unión)_. Ojo Ø10 en lo alto del asa, con eje en Y: aquí se amarra el cabo que sube a la linterna / línea larga.
5. **Asa en arco** ×2 _(forma / ahorro de material)_. Asa de 12 mm de grosor con apertura para guante. El techo de la ventana va a 45° para imprimir sin soportes.

## M3s · Riel con gancho (una mitad)

Riel hueco de 30 × 30 mm (celosía) que sale de la caja y lleva la cápsula de cámara. Una mitad por lado; la otra es la misma pieza girada 180° sobre z. El gancho en C cuelga el nodo del aro de la linterna.

![M3s_riel_gancho](../salida/guia_piezas/M3s_riel_gancho.png)

1. **Pasos M4 de la brida** Ø4.2 ×4 _(tornillo / unión)_. Cuatro pasos M4 (Ø4.2) en la brida de 25 mm de ancho: los 4 tornillos M4 que atan el riel al cojín de la caja (N° 3 de M1s). Unión no estanca. Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente.
2. **Ventana Ø21 de la brida** Ø21 _(cable)_. Ventana de 21 mm. Mirando el riel desde el lado de la caja es el agujero redondo grande que se ve en la brida, junto a la celosía. Deja pasar el domo del PG7 de la caja (que asoma por el Ø30 del cojín). De aquí el Cat5e sale del PG7 hacia el interior del conducto. Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente.
3. **Conducto hueco por dentro** _(cable)_. El riel es un tubo hueco: 10 mm libres entre paredes de 5 mm. Por dentro corre el Cat5e de la cámara (varilla M8 de lastre aparte). Va inundado: no sella; el sello son los PG7. Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente.
4. **Celosía de triángulos (ahorro de material)** ×6 _(forma / ahorro de material)_. Ventanas triangulares (celosía Warren de 65°, barras de 3 mm) en las dos paredes. Quitan material y peso. No son pasos de cable: el cable va por dentro y se ve a través de ellas.
5. **Agujero redondo Ø8 de la punta** Ø8.0 _(cable)_. Es el agujero redondo que se ve en el extremo del riel (pared de 5 mm). Es la entrada del cable de la cámara al riel: el Cat5e sale del PG7 de la cápsula (N° 2 de M4), hace un bucle y entra por aquí, corre por el conducto (N° 3, se ve por la celosía), pasa la ventana Ø21 (N° 2) y llega al PG7 del cojín de la caja (N° 4 de M1s). Cambia con la corrección de concepto (riel cerrado estanco, cable por dentro): pendiente.
6. **M4 de la silla de la cápsula** Ø4.2 ×4 _(tornillo / unión)_. Dos tornillos M4 (a x = 170 y 200) cruzan el riel de lado a lado: se ven 4 pasos Ø4.2, uno por pared. Aprietan las mejillas de la silla de M5s contra el riel. NO son pasos de cable.
7. **Asiento en C del gancho** Ø8.8 _(tornillo / unión)_. C abierta de Ø8.8 (varilla del aro Ø8 + 0.4 de holgura): el nodo cae sobre la varilla del aro de la linterna. Una correa de 25 × 3 pasa por la ranura del alma.

## M3t · Tapa del bolsillo de lastre

Placa de 3 mm que cierra por abajo cada bolsillo de lastre de la caja. Se imprimen 2 (una por bolsillo). Plana en la cama.

![M3t_tapa_bolsillo](../salida/guia_piezas/M3t_tapa_bolsillo.png)

1. **Pasos M3 avellanados** Ø3.4 ×2 _(tornillo / unión)_. Dos pasos M3 (Ø3.4) con avellanado: la cabeza queda al ras del fondo. Los M3 de 8 mm entran a los insertos del fondo del bolsillo (N° 9 de M1s).
2. **Placa de cierre** _(forma / ahorro de material)_. Placa de 107 × 35 × 3 mm que retiene el lastre a granel. No es estanca: el bolsillo está fuera del sello.

## M4 · Cápsula de cámara (cuerpo)

Caja estanca de la cámara Arducam Mega 5 MP, con anillo LED y ventana de acrílico. Brida de 4 mm que se cierra con la tapa M5s. Hay una por lado (×2). x es el eje óptico (adelante = +x).

![M4_capsula_cuerpo](../salida/guia_piezas/M4_capsula_cuerpo.png)

1. **Pasos M3 de la brida** Ø3.4 ×4 _(tornillo / unión)_. Cuatro pasos M3 (Ø3.4) en las esquinas de la brida: M3 con tuerca unen la tapa M5s y aprietan el cordón O-ring Ø2 (N° 2 de M5s).
2. **PG7 de la cápsula** Ø12.6 _(cable)_. Agujero Ø12.6 en la pared inferior, a 10 mm de la apertura trasera. Entra el Cat5e de esta cámara (imagen SPI y anillo LED); este es el otro extremo del cable del riel (N° 5 de M3s). Sello del cable; hay 23 mm atrás para el bucle y la contratuerca.
3. **Asiento de la ventana Ø30.4** Ø30.4 _(sello / agua)_. Rebaje frontal para el disco de acrílico M7 (Ø30 × 3). El bisel M6 lo mantiene en su lugar. A confirmar: el CAD solo define el asiento; el sellador o junta de la ventana no está especificado.
4. **Apertura anular del LED con 3 radios** _(forma / ahorro de material)_. Anillo de luz Ø26 alrededor del lente: deja salir la luz del anillo LED (Ø30 × 3, pegado a la cara interior). Tres radios de 2 mm sujetan el tubo opaco que impide que el LED ilumine el lente por dentro.
5. **Orificio del lente Ø16.4** Ø16.4 _(forma / ahorro de material)_. Agujero central: por aquí mira el porta-lente Ø16 de la cámara. Lo rodea un tubo separador opaco (pared 1.2).
6. **Pilotos M2 del bisel** Ø1.8 ×3 _(tornillo / unión)_. Tres agujeros ciegos Ø1.8 × 4 mm: tornillos M2 autorroscantes del bisel M6.
7. **Cavidad 38 × 38 × 38** _(montaje de piezas internas)_. Aloja la cámara (33 × 33 × 17), el anillo LED y, detrás, 23 mm de zona libre para el bucle del cable y la contratuerca del PG7.

## M5s · Tapa de la cápsula con pie

Cierra la cápsula M4 y la fija al riel: placa de tapa inclinada 30°, alma y silla en U que abraza el riel. Se imprime ×2. El STEP está en la pose del ensamble (x a lo largo del riel).

![M5s_capsula_tapa_pie](../salida/guia_piezas/M5s_capsula_tapa_pie.png)

1. **Pasos M3 de la tapa** Ø3.4 ×4 _(tornillo / unión)_. Cuatro pasos M3 (Ø3.4) en las esquinas de la placa: M3 con tuerca contra M4 (N° 1 de M4). Apretados, comprimen el cordón.
2. **Ranura del cordón O-ring (4 esquinas)** Ø10.6 ×4 _(sello / agua)_. Ranura rectangular de 2.6 × 1.5 mm en la cara interior de la placa, entre la cavidad y los M3. Cordón de goma Ø2. Se marcan sus 4 esquinas (R4).
3. **M4 de la silla** Ø4.2 ×4 _(tornillo / unión)_. Dos M4 (a x = 170 y 200) cruzan las dos mejillas (4 pasos Ø4.2) y el riel por dentro (N° 6 de M3s). Sujetan la cápsula al riel.
4. **Silla en U sobre el riel** ×2 _(forma / ahorro de material)_. Dos mejillas y una placa bajo el riel: abrazan el conducto (holgura 0.3 por lado).
5. **Alma triangular** _(forma / ahorro de material)_. Alma en V que lleva el peso de la cápsula al riel; se imprime sin soportes locales. FEM local: factor de seguridad 5.0 (150 N).

## M6 · Bisel de la cápsula

Anillo de 2.5 mm que sostiene la ventana de acrílico contra el frente de M4. Pequeño: se imprime ×2 al 40 %.

![M6_capsula_bisel](../salida/guia_piezas/M6_capsula_bisel.png)

1. **Pasos de los M2** Ø2.4 ×3 _(tornillo / unión)_. Tres agujeros Ø2.4 a 120°: pasan los M2 autorroscantes que se enroscan en los pilotos Ø1.8 de M4 (N° 6 de M4).
2. **Abertura Ø28** Ø28 _(sello / agua)_. Abertura de 28 mm: deja ver el lente y el LED a través del acrílico (Ø30). La corona de 1 mm que queda sobre el borde de la ventana la retiene.

## M11 · Bandeja inferior

Bandeja de 3 mm dentro de la caja seca: sostiene los módulos electrónicos. Se atornilla a los 4 bosses de M1s y lleva 4 postes que reciben la bandeja superior.

![M11_bandeja](../salida/guia_piezas/M11_bandeja.png)

1. **Pasos M3 sobre los bosses** Ø3.4 ×4 _(tornillo / unión)_. Cuatro pasos M3 (Ø3.4) en las esquinas de la placa, justo bajo los postes: deberían recibir los M3 hacia los insertos de los bosses de M1s (N° 8 de M1s). A confirmar: en el STEP el poste es sólido de z = 16 a 36, así que el paso queda tapado y el tornillo no tiene por dónde entrar. Revisar en el CAD.
2. **Postes de la bandeja superior** Ø3.4 ×4 _(montaje de piezas internas)_. Cuatro postes con paso M3 (Ø3.4): la bandeja superior M11_sup se atornilla encima.
3. **Ventana doble Ø27 (en ocho)** Ø27.32 ×2 _(cable)_. Dos círculos de 27 mm que se juntan. Herencia de la caja anterior con PG7 en el piso (radio de acceso para la llave); hoy solo deja pasar cables hacia el fondo. A confirmar: no tiene función estructural.
4. **Muescas de los extremos** ×2 _(forma / ahorro de material)_. Muescas en los bordes de la bandeja sobre las contratuercas de los PG7 de las paredes de extremo (+2 mm alrededor de sus esquinas).

## M11 · Bandeja superior

Segundo piso de la caja seca. Placa de 3 mm que se apoya en los 4 postes de la bandeja inferior.

![M11_bandeja_sup](../salida/guia_piezas/M11_bandeja_sup.png)

1. **Pasos M3 de los postes** Ø3.4 ×4 _(tornillo / unión)_. Cuatro pasos M3 (Ø3.4): los M3 bajan a los postes de la bandeja inferior (N° 2 de M11 inferior).
