# Fase C: piezas

Todas las piezas salen de `cad_final/` y escriben STL y STEP en `salida/preliminar/` (NO LISTO PARA IMPRIMIR: faltan
las medidas reales de la electrónica, los prensaestopas y el domo del PG7). Cada pieza pasó BRepCheck, BOPAlgo,
astillas, STL estanco de un solo cuerpo, cama, voladizo y espesor mínimo (percentil 1 de 1500 rayos ≥ 1.2 mm).

| Script | Piezas | Reporte |
|---|---|---|
| `fase_c_caja.py` | M1 cuerpo de la caja, M2 tapa, M11 bandeja | `cad_final/reporte_caja.md` |
| `riel.py` | M3 tramo central (cámara de cables), M3 extensión de 100 | `cad_final/reporte_riel.md` |
| `gancho.py` | M9 gancho, M13 casquillos Ø6/8/10/12, M14 pestillo, M12 perilla | `cad_final/reporte_gancho.md` |
| `capsula.py` | M4 a M7 cápsula, M10 carro | `cad_final/reporte_capsula.md` |
| `cables.py` | recorrido del Cat5e por aro | `cad_final/reporte_cables.md` |

## Resultados

| Pieza | bbox mm | Espesor p1 mm | Masa g (relleno) | Voladizo / soportes |
|---|---|---|---|---|
| M1 caja | 159.6 × 126 × 50 | 1.50 | 273 (100 %) | 120 mm², sin soportes |
| M2 tapa | 159.6 × 126 × 63 | 2.90 | 164 (100 %) | ventana del asa a 45° |
| M11 bandeja | 127.6 × 94 × 18 | 3.00 | 41 (40 %) | ninguno |
| M3 tramo central | 140 × 88 × 57.3 | 1.37 | 184 (100 %) | 8958 mm², brida abajo, lleva soportes |
| M3 extensión | 100 × 30 × 30 | 1.40 | 47 (100 %) | 2814 mm², acostada |
| M9 gancho | 68 × 59 × 30 | 3.31 | 18 (40 %) | 1017 mm², soporte bajo el escalón brida/alma |
| M13 casquillos | 12 a 17 × 20 × 13.5 | 1.51 | 1 a 2 | ninguno |
| M14 pestillo | 12 × 35.2 × 3.6 | 1.50 | 1 | ninguno |
| M12 perilla | 30 × 30 × 12 | 6.99 | 6 (40 %) | 45 mm² |
| M4 cápsula cuerpo | 64 × 64 × 44 | 1.19 (pared de 1.2 exacta del tubo separador) | 59 (100 %) | 1054 mm² |
| M5 cápsula tapa | 33 × 64 × 64 | 0.62 (dientes de la bisagra, excepción D25) | 30 (100 %) | 499 mm² |
| M6 bisel | 42 × 42 × 2.5 | 1.79 | 2 | ninguno |
| M7 ventana (acrílico) | 30 × 30 × 3 | 3.00 | 3 | no se imprime |
| M10 carro | 80.8 × 38.6 × 85 | 0.62 (dientes de la bisagra, excepción D25) | 49 (40 %) | 899 mm² |

Cápsula por unidad: 71.5 cm³ de PETG + 54.2 de aire + 2.1 de ventana = **127.8 cm³ desplazados** (antes 154) y
**93.3 g** (antes 104). La cavidad bajó a 38 × 38 × 38 con la cámara de 33 × 33 × 17.

Interferencias revisadas con volumen común = 0: tramo central con extensión a ambos lados, extensión con extensión,
deslizamiento lateral del macho cada 10 mm, perilla y su cilindro libre Ø34 contra el gancho, pestillo cerrado
contra la mandíbula y contra el casquillo Ø10. Carro con cápsula: 0 de 0 a 90° en pasos de 10, contra el carro, contra la
perilla y contra el riel en 5 posiciones (punta del riel de 0 a 100 más allá de la manga); carro contra riel 0 en las 5.

## Decisiones tomadas sin consulta

| # | Qué | Por qué | Descartado | Cómo revertir |
|---|---|---|---|---|
| D16 | Falda de la brida de M1 hecha con loft entre rectángulos redondeados (r5 abajo, r6 arriba) | El loft de esquinas vivas sobresalía del redondeo de la brida y del cuerpo y dejaba un filo de 0.01 mm en las 4 esquinas (p1 1.04) | Quitar el redondeo de la brida | `caja_central.box_body`, volver a `.rect().loft()` |
| D17 | Buje alrededor del pivote del pestillo, Ø3.4 + 2 × 1.5 | El brazo de 5 dejaba 0.8 mm al costado del agujero M3 (venía así desde PB4). El buje está centrado en el pivote, así que al girar solo barre su propio círculo | Ensanchar todo el brazo | `gancho.latch`, quitar el `union` del buje |
| D18 | Extremos del tramo central con la hembra de PB3 en ambos lados; la extensión lleva macho y hembra | Así se encadenan extensiones sin piezas distintas por lado | Central macho/macho | `riel.py` |
| D19 | Ventana de acceso a los M4 de la unión en el tramo central (\|x\| 55 a 70, \|y\| ≤ 15, sin tocar la brida) | Sin ella no se llega a los M4 verticales de la media madera con la caja puesta | Atornillar antes de montar la caja | `riel.py`, constante de la ventana |
| D20 | La ranura T queda abierta por las puntas del tramo central y por el macho de la extensión | Las tuercas M4 entran por ahí; hay que cargarlas antes de unir los tramos | Ranura cerrada con boca lateral | `riel.py` |
| D21 | La ranura de salida del cable solo se usa en la extensión más externa | Si se encadena otra, su macho la tapa | Ranura en cada tramo | `RAIL_EXIT_SLOT` |
| D22 | Gancho impreso de costado (capas en planos XZ) | Los 75 N del asiento y del alma van a lo largo de las capas, no las abren | Boca arriba, más lindo y más débil | orientación en `gancho.py` |
| D23 | Carro M10 rediseñado (`CARRIAGE_MODE = "deslizante"`): manga abierta en los dos extremos, fondo cerrado con el M4 de la perilla abajo (como el gancho), quilla con las orejas delante de la perilla y eje de la bisagra 34 bajo el fondo del riel; largo 60 (antes 40) | La primera versión tenía una placa de tope sobre el eje del riel: el carro solo podía ir a ras de la punta (no ±50), la perilla iba arriba sin forma de llegar a la T inferior y el cable no tenía paso. Con el eje bajo el riel, todo punto de la cápsula sobre el eje queda a más de 16 de él, así que el riel puede pasar por encima | Orejas de 80 o más con el eje en la línea del riel | `CARRIAGE_MODE = "tope"` en `params.py` |
| D24 | Rendija lateral de 10 en +Y a todo lo largo de la manga, a la altura de la ranura de salida del riel | La ranura de salida queda bajo la manga en las posiciones exteriores; con la rendija el cable sale en cualquier posición | Ventana del largo del recorrido | `CARRIAGE_SLIT_CLR`, quitar el corte |
| D25 | Los dientes de la bisagra (alto 1.2, dato del equipo) quedan como excepción al espesor mínimo | El criterio de 1.2 es para paredes; los dientes son de 1.2 por diseño y la Fase F los quita del modelo de SimScale | Agrandar los dientes | no aplica |
| D26 | Tubo separador del LED con pared de 1.2 (sin cambio) | Con 1.5 el tubo chocaba con el agujero supuesto del anillo LED (36 mm³); el p1 de 1.19 es teselado | Pared 1.5 | `LED_SEPARATOR` |
| D27 | Bucle del cable = mayor entre 40 y la distancia recta de la salida al PG7 de la cápsula en el peor caso de recorrido e inclinación | Con el eje bajo el riel y ±50 de recorrido, 40 no alcanza | Mantener 40 | `cables.py` |
| D28 | Constantes sueltas de `riel.py` y `gancho.py` pasadas a `params.py` (`XFER_STEP`, `KNOB_FREE_EXTRA`, `KNOB_WEB_GAP`, `KNOB_FLANGE_GAP`, `BUSHING_TIP_MARGIN`, `WEB_OVERLAP`); `EXIT_SLOT_ZC` queda en `riel.py` porque es derivada | Regla de fuente única | | |

## Pendiente

- **Cable:** con el carro deslizante el bucle hasta la cápsula pasa de 40 a 119 (134 en Ø100, que sale por la punta).
  El cable de fábrica de 300 ya no alcanza en ningún aro: todos requieren prueba en banco SPI a 8 y 4 MHz
  (`reporte_cables.md`). Si se fija el carro en la mitad interior del recorrido, el bucle baja.
- **Ø100 sin extensiones:** el tramo central sobresale solo 15 de la brida de la caja y el carro mide 60; dónde va la
  cápsula en Ø100 se resuelve en la Fase D (sigue abierto C15).
- El tramo central es la pieza con más soporte (8958 mm² de voladizo): conviene una prueba de impresión antes del lote.
- `PB4` y `M14` en `salida/probetas/` se regeneraron con el buje del pivote (D17).

## Balance con la cápsula real

`fase_a.py` corrido de nuevo con `CAPSULE_SET_G` 93.1 y `CAPSULE_SET_DISP_CM3` 127.8 (bandeja al 40 %):

| Aro | Pletinas por lado | Peso aparente final g | Total en aire g |
|---|---|---|---|
| Ø100 | 3 | +208 | 1855 |
| Ø200 y Ø300 | 3 | +228 | 1961 |
| Ø500 | 3 | +249 | 2067 |

Todos dentro de 0.2 a 0.5 kgf. Estabilidad: en la Fase E se corrigió el cálculo (el acero de las pletinas no sumaba a la masa y las cápsulas iban a
la altura del riel). Con eso el centro de masa queda 19.1 mm (Ø100) y 17.4 mm (Ø500) bajo el de empuje; ver
`FASE_E.md`.

## Cierre

- **Qué cambió:** 17 piezas finales en `salida/preliminar/` (caja, tapa, bandeja, dos tramos de riel, gancho, cuatro
  casquillos, pestillo, perilla, cápsula de cuatro piezas y carro). El carro pasó a deslizante con la bisagra bajo el
  riel, la cápsula bajó a 93 g, el lastre a 3 pletinas por lado y el cable ya no alcanza con el de fábrica.
- **Qué chequeos pasaron:** BRep, BOP, STL estanco de un cuerpo, cama y voladizo en todas; espesor ≥ 1.2 en todas salvo
  los dientes de la bisagra (excepción D25) y la pared de 1.2 exacta del tubo separador (1.19 de teselado);
  interferencia 0 en uniones del riel, gancho, pestillo, perilla y en el barrido carro × inclinación.
- **Qué quedó pendiente:** prueba SPI del cable en todos los aros, dónde va la cápsula en Ø100 (C15, Fase D), medir el
  agujero del anillo LED y el domo del PG7, prueba de impresión del tramo central (el que más soporte lleva).
