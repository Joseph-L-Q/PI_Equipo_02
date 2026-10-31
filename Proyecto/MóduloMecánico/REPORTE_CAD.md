# Reporte CAD, versión final del nodo LanternGuard

Rama `cad/version-final`. Fuente única de medidas: `cad_final/params.py` (324 parámetros, cada uno con origen y
estado). Todo se regenera con `python cad_final/build.py` (ver `README.md`). Medidas por pieza para el equipo en
`MEDIDAS.md`; planos por pieza en `planos/cad_final/`. Detalle por fase en `FASE_A.md` a `FASE_G.md`.

> **Desde el 29/10 hay dos versiones** (`version` en `params.py`): **simple** (por defecto, el prototipo real en el aro
> Ø200, sección 9 y `cad_final/reporte_simple.md`) y **modular** (el riel por tramos de Ø100 a Ø500, secciones 1 a 8).
> `build.py --rapido` regenera la que esté elegida; la otra queda como está.

## 1. Estado en una línea por cosa

| Qué | Estado | Dónde |
|---|---|---|
| Probetas (gancho, ranura T, unión, pestillo, perilla, junta, peine, inserto M4 en PETG) | **Listas para imprimir.** Son lo primero: sirven para medir holguras | `salida/probetas/` |
| Caja, tapa y bandeja del nodo | Preliminar: falta medir la electrónica y los PG7 | `salida/preliminar/` |
| Riel, gancho, casquillos, pestillo, perilla | Preliminar; largo del riel decidido (C18) y varilla M8 tensada (C19) | `salida/preliminar/` |
| Cápsula y carro | Preliminar; el carro depende del largo del riel | `salida/preliminar/` |
| Boya | Preliminar: masas de componentes estimadas, francobordo con 4 mm de margen | `salida/boya/` |
| Ensambles por aro | Rehechos con el riel nuevo; el pestillo contra la perilla del carro (C20) se prueba con guante | `salida/ensambles/` (renders; STEP se regeneran) |
| SimScale | 4 STEP simplificados y la guía con el resultado a mano esperado; las simulaciones las corre el equipo | `SIMSCALE.md`, `salida/simscale/` |
| `salida/final/` | **Vacía a propósito**: ningún parámetro está medido todavía (0 de 294 con origen "medido") | `salida/final/LEEME.md` |

## 2. Inventario de piezas

| Pieza | Script | Cant. por nodo | Relleno | Orientación de impresión | Soportes |
|---|---|---|---|---|---|
| M1 caja, cuerpo | `fase_c_caja.py` | 1 | 100 %, 5 perímetros (sellada) | boca arriba, fondo en la cama | no; falda de la brida a 45° |
| M2 caja, tapa | `fase_c_caja.py` | 1 | 100 %, 5 perímetros | cara de la ranura en la cama, asa arriba | no |
| M11 bandeja | `fase_c_caja.py` | 1 | 40 % | plana | no |
| M3 tramo central (cámara de cables) | `riel.py` | 1 | 100 %, 5 perímetros | brida abajo | **sí** (8958 mm² de voladizo) |
| M3 extensión (115, paso 100) | `riel.py` | 0 a 2 por lado | 100 %, 5 perímetros | acostada (capas a lo largo) | casi nada |
| M3 punta (60) | `riel.py` | 2 | 100 %, 5 perímetros | acostada | casi nada |
| M3 tapa del bolsillo | `riel.py` | 2 | 100 % | plana | no |
| Varilla roscada M8, 2 tuercas, 2 arandelas DIN 9021 | `riel.py` | 1 juego | acero 8.8 (o 4.6) | | |
| M9 gancho | `gancho.py` | 2 | 40 % | de costado (capas en planos XZ) | bajo el escalón brida/alma |
| M13 casquillo Ø6/8/10/12 | `gancho.py` | 2 del Ø de la varilla | 100 % | de pie | no |
| M14 pestillo | `gancho.py` | 2 | 100 % | plano | no |
| M12 perilla | `gancho.py`, `capsula.py` | 4 (2 ganchos + 2 carros) | 40 % | plana | no |
| M10 carro | `capsula.py` | 2 | 40 % | de costado | 899 mm² de voladizo |
| M4 cápsula, cuerpo | `capsula.py` | 2 | 100 %, 5 perímetros | eje óptico vertical | 1054 mm² |
| M5 cápsula, tapa | `capsula.py` | 2 | 100 %, 5 perímetros | de canto | 499 mm² |
| M6 bisel | `capsula.py` | 2 | 40 % | plano | no |
| M7 ventana | `capsula.py` | 2 | acrílico de 3, no se imprime | | |
| Pletina de inox 25 × 5 × 100 | `camara.py` | 2 o 3 por lado (ver `MEDIDAS.md` §2) | acero | | |
| PB8 probeta de inserto M4 | `probetas.py` | 1 | 100 %, igual que el fondo de la caja | plana | no |
| B1 a B6 boya | `boya.py` | ver `FASE_G.md` | 100 % casco y tapa | ver `reporte_boya.md` | lengüeta de B5 y casco |

**Cama (actualizado 29/10, impresora real Bambu Lab P1P, boquilla 0.4, 256 × 256 × 256):** las 53 piezas de
`salida/` (simple, modular, boya, probetas y LR1) caben, cada una en al menos una orientación de impresión. Las más
largas: M3s mitad del riel 215 (simple, con la brida abajo), LR1 separador 211.9, casco de la boya B1 209, tapa B2 197,
caja y tapa 159.6. Todas cabían también en la cama supuesta de 220 × 220 × 250; con la P1P queda un margen de 41 mm
en la pieza más larga. Ninguna pieza de la modular pasa de 150 salvo la caja y la boya (regla `pieza.largo_max`).

## 3. Qué cambió respecto del diseño anterior

La tabla completa anterior → nuevo → origen → razón la genera `cad_final/reporte_parametros.py` en
`cad_final/reporte_parametros.md` (§1). Lo grande:

- La caja se dimensionó desde la bandeja: 159.6 × 126 × 55 con brida, un piso, 484 cm³ de aire (antes 797).
- El brazo M3 pasó a un riel modular: tramo central que es una cámara de cables bajo la caja + 2 puntas + 0, 1 o 2
  extensiones por lado (230 / 430 / 630), atravesado por una varilla M8 tensada.
- La horquilla de la cápsula pasó a un carro deslizante con la bisagra bajo el riel.
- Ganchos al aro con casquillo intercambiable, pestillo y correa.
- Lastre en pletinas de inox bajo el tramo central, fuera del sello.
- Cápsula achicada a 38 × 38 × 38 de cavidad (93 g, 128 cm³), con anillo LED y separador.
- Boya nueva (B1 a B6).

## 4. Conflictos

| # | Estado |
|---|---|
| C1 (largo del conjunto) | Sigue: con un aro de Ø500 el nodo mide más de 600 de largo |
| C2 (diseño a 15 m) | Cerrado: se diseña a 1 m; manda la manipulación (150 N) |
| C3, C7, C9 (boya, RTC, placa) | Atendidos en la Fase G: placa de 70 × 73.5, lugar para el DS3231, cadena panel → Waveshare → 5 V sin doble regulación (texto, sin esquema de la placa) |
| C4 (KIT A) | Queda como alternativa desactivada |
| C5 (ultrasónico) | Cerrado: descartado |
| C6 (cable) | **Sigue, peor:** con el carro deslizante ningún recorrido baja de 300; todos requieren prueba en banco SPI a 8 y 4 MHz |
| C8 (estanqueidad) | Sigue: solo se valida con prueba de 24 h, 72 h y 7 días |
| C10 (brazo impreso de pie) | Cerrado: el riel se imprime acostado |
| C11 (rojo de M3 en Onshape) | Cerrado por reemplazo: **hay que volver a importar el ensamble en Onshape**, las referencias al M3 viejo se rompen |
| C12, C13, C14 | Cerrados en la revisión de la Fase A |
| C15 (cuerdas en Ø100) | Cerrado en Ø100 y Ø200: las cuerdas se amarran al ojal del asa (la linterna cuelga del nodo). En Ø300 y Ø500 siguen al ápice: con la cámara 12.4 más honda, Ø300 pide ápice ≥ 578 y Ø500 ≥ 294 |
| C16 (domo del PG7) | Sigue: medir el prensaestopas; fija el alto de la cámara |
| C17 (riel 57 bajo la caja) | Revisado: los ganchos no tocan la caja |
| C18 (largo del riel) | **Cerrado (decisión del 29/10):** pieza de punta de 45 + 15 de unión y extensiones a paso 100. Riel de 230 / 430 / 630; la punta queda a 1 mm de R + 64 en Ø100, Ø300 y Ø500, y a 51 en Ø200 |
| C19 (unión de tramos) | **Cerrado (decisión del 29/10):** varilla M8 obligatoria, tensada con tuerca y arandela en las dos puntas. Ø500 con 150 N en la punta: pared de PETG a FS 1.4 en fluencia y 2.0 a rotura (sin varilla 0.8); varilla FS 7.3 en 8.8 y 2.7 en 4.6. Para alojarla la cámara de cables crece 12.4 mm (fondo del riel a −69.75) y la rampa pasa a 60°. Detalle en `cad_final/reporte_verificacion.md` §3c |
| C20 (pestillo y perilla del carro) | **Se deja así (decisión del 29/10)**: se prueba con guante en la probeta del pestillo. El pestillo M14 entra 259 mm³ en el espacio de la mano de la perilla del carro con s = 0 (Ø100, Ø300, Ø500; en Ø200 con s = 50); las piezas no chocan. En Ø100, Ø300 y Ø500 el carro solo va a ras de la punta. **Si molesta:** `gancho.boca = "adentro"` gira 180 grados el juego del gancho sobre la varilla del aro (mismas piezas impresas) y el pestillo abre hacia el otro lado; hoy solo cabe en Ø200, porque en Ø100, Ø300 y Ø500 la brida y la perilla del gancho chocan con el carro (5148 y 505 mm³; el largo del riel supone la brida hacia adentro). Espejar solo el pestillo dentro de la garra no sirve: al abrir, su brazo entra en la varilla del aro a partir de 38 a 50 grados. Lo que sí achica el choque es acortar la lengüeta (`pestillo.lengueta`) |
| C21 (ojal y tapa del bolsillo) | **Cerrado (decisión del 29/10):** grillete o argolla de inox M6 en el ojal Ø10 (ver Compras); las cuerdas se amarran al grillete. La tapa del bolsillo se fija con 2 M3 × 8 avellanados por tapa a insertos M3, en bosses que salen 6 mm de la pared exterior del bolsillo; la cabeza queda al ras del fondo del riel. El tramo central pasa de 88 a 100 de ancho en los bolsillos |

## 5. Verificación

- **Piezas:** todas pasan BRep, BOP, STL estanco de un cuerpo, cama y espesor ≥ 1.2; las excepciones son los dientes de
  la bisagra (1.2 por diseño) y la pared exacta de 1.2 del tubo separador del LED.
- **Colisiones y encajes:** uniones del riel, gancho con pestillo y perilla, carro con cápsula en todo el recorrido e
  inclinación, maquetas de cámara, LED y ventana: sin interferencias. En los ensambles por aro, las interferencias
  vienen del largo del riel (C18).
- **Cables:** `cad_final/reporte_cables.md`.
- **Cálculo a mano:** `cad_final/reporte_verificacion.md` (`FASE_E.md` tiene el resumen). Método de flotabilidad: volúmenes
  de los sólidos reales, relleno como parámetro (40 % y 100 %), empuje con agua de mar de 1025 kg/m³; estabilidad con G
  y B del nodo completo (sumergido no hay metacentro, el número es BG).
- **Peso:** nodo de 2.04 a 2.22 kg con la varilla (≤ 3), peso aparente de +224 a +318 g (ventana de +200 a +500).

## 5b. Compras (no se imprimen)

| Qué | Cantidad por nodo | Nota |
|---|---|---|
| Varilla roscada M8 (8.8; si no hay, 4.6) | 1 tramo de 251 / 451 / 651 mm según el aro | Largo en `MEDIDAS.md` §2 |
| Tuerca M8 y arandela ancha M8 DIN 9021 (Ø24) | 2 y 2 | |
| Pletina de inox 25 × 5, trozos de 100 | 4 a 6 | `MEDIDAS.md` §2 |
| Grillete o argolla de inox M6 | 1 | En el ojal Ø10 del asa (Ø100 y Ø200); las cuerdas se amarran ahí |
| Tornillo M3 × 8 avellanado (ISO 10642) | 4 | 2 por tapa del bolsillo |
| Inserto térmico M3 | 4 para las tapas, más los de la caja y la bandeja | |
| Inserto térmico M4 | 4 (riel a la caja) | Probar antes con PB8 |
| Tornillos M4, tuercas M4 de la ranura T, perno M4 de las perillas | ver `MEDIDAS.md` §4 | |
| Prensaestopas PG7 | ver `MEDIDAS.md` | Medir antes de imprimir la caja |
| Cordón de junta tórica Ø2 | | Caja y cápsulas |
| Cable Cat5e | según el aro | `cad_final/reporte_cables.md` |
| Correa de 25 × 3 | 2 | Ganchos |

## 6. Pruebas físicas recomendadas, en orden

1. Imprimir las probetas: peine de holguras, encaje de los casquillos en varilla real (fuerza de entrada y salida),
   tuerca M4 en la ranura T, unión de tramos, pestillo con guante, perilla y junta.
2. Arranque de los insertos M4 en PETG con la probeta PB8 (el fondo de la caja pide 274 N cada uno).
3. Unión de tramos a flexión hasta la falla, con y sin varilla M8.
4. Estanqueidad de la caja y de la cápsula: 24 h, 72 h y 7 días a 1 m.
5. Cable Cat5e de la longitud real con la cámara a 8 y 4 MHz.
6. Pesar el panel solar y la batería, y flotar la boya en un balde antes del mar.

## 7. Resumen simple

- **Listo para imprimir:** las probetas de `salida/probetas/` (PB1 a PB8). Nada más todavía.
- **Preliminar:** el resto de las piezas del nodo, la cápsula y la boya. Están completas y chequeadas, pero las medidas
  de la electrónica, los prensaestopas, el domo del PG7, el anillo LED y las masas son estimadas.
- **Qué hay que medir:** la lista ordenada por importancia está arriba de `MEDIDAS.md`; la completa, en
  `cad_final/reporte_parametros.md` §2. Lo crítico: DevKit y módulos de
  la bandeja, prensaestopas PG7 (contratuerca y domo), varilla del aro, agujero del anillo LED, cámara, panel solar,
  baterías y la densidad del PETG del slicer.
- **Siguiente paso:** imprimir las probetas (PB1 a PB8), medir lo de la tabla de `MEDIDAS.md`, cargar los valores en
  `params.py` y regenerar. Después, probar el pestillo con guante (C20) y comprar el grillete del ojal (C21).

## 8. Decisiones tomadas sin el equipo en la ronda C18/C19 (29/10)

| Tarea | Qué se eligió | Por qué | Qué se descartó | Cómo revertir |
|---|---|---|---|---|
| Varilla M8 | La varilla pasa **bajo** el cable (eje a 14.05 del fondo del riel) y la cámara crece 12.4 mm; rampa de 45 a 60 grados | Un Cat5e que baja del domo del PG7 con R ≥ 25 no pasa por encima de una varilla alta | Varilla sobre el cable; cámara del mismo alto | `ROD_CHANNEL_GAP`, `ROD_BOSS_WALL`, `CHAMBER_RAMP_DEG` en `params.py` |
| Varilla M8 | Arandela ancha DIN 9021 (24 × 2), precarga de 500 N, 2 mm de sobrante | Reparte la carga en 2.7 veces más área que la arandela común de Ø16 (9.1 MPa en el PETG con la carga de diseño) | Arandela DIN 125 | `ROD_WASHER`, `ROD_PRELOAD_N`, `ROD_PROTRUSION` |
| Conducto | En la unión de tramos (10 de ancho) pasa un solo Cat5e por lado | Cada lado lleva el cable de una sola cámara; dos Cat5e no entran ni lado a lado (11 > 10) ni uno sobre otro (7.9 de alto sobre la varilla) | Agrandar la sección del riel | `RAIL_SECTION` y volver a correr `--todo` |
| Cuerdas al asa | Recorrido de la cuerda: aro, bajo el borde de la caja, sobre el borde de la tapa, al ojal | Es el camino más corto sin atravesar la caja | Cuerda recta al ojal (atraviesa la caja) | `cords_to_eye()` en `ensambles.py` |
| Ojal del asa | Se deja Ø10 y se recomienda grillete o argolla | La pieza aguanta 180 N; lo que no entra son los nudos | Agrandar el ojal (cambia el asa y la tapa) | `HANDLE_EYE` |
| PB8 | Placa de 40 × 40 con el espesor del fondo de la caja, inserto desde abajo y 4 agujeros M4 para apoyarla | Reproduce el fondo de la caja tal como se imprime | Probeta de pared vertical | `INSERT_COUPON`, `pb8()` en `probetas.py` |
| Ensambles | Se quitó el caso `100e1` (Ø100 con una extensión) | Con la regla del equipo Ø100 no lleva extensiones | Mantenerlo | Agregarlo a `CASES` en `ensambles.py` |
| Planos por pieza | Script propio `planos_piezas.py` (misma técnica que `cad/planos.py`) | `cad/planos.py` lee los parámetros viejos de `cad/` al importarse y tiene cambios sin commitear del autor | Modificar `cad/planos.py` | Borrar `planos/cad_final/` |
| Instalación | `requirements.txt` con las dependencias directas fijadas, no un `pip freeze` completo | El Python de esta máquina tiene muchos paquetes que el CAD no usa | `pip freeze` | Agregar líneas a `requirements.txt` |
| Fijación de la tapa del bolsillo (C21) | 2 M3 avellanados a insertos en bosses hacia afuera, a x = ±30 | La pared de 3 no aguanta un inserto de 4; hacia los extremos el boss chocaría con el carro en Ø100 y adentro están las pletinas. A x = ±40 las cuerdas de Ø100 que suben al asa rozaban la orejeta (0.6 mm³); a ±30 quedan a 9 mm | Pegarla; correa alrededor del tramo; tapa deslizante con 1 tornillo (más simple, ver abajo) | `lastre.tapa_tornillo_x`, `lastre.tapa_boss` en `params.py` |
| Pestillo hacia el otro lado (C20) | Parámetro de ensamble `gancho.boca` (gira el juego del gancho), por defecto "afuera" | Espejar solo el pestillo lo deja sin poder abrir | Rediseñar la garra | Volver a "afuera" |
| STEP deterministas | La fecha del encabezado de cada STEP queda fija (2026-01-01) | Mismo modelo, mismos bytes: git solo muestra lo que cambió de verdad | Fijarla desde OCP al escribir | `STEP_STAMP` en `cad_final/checks.py` |

**Alternativa más simple para la tapa (propuesta, no hecha):** una tapa que entra deslizando por dos ranuras en las paredes del bolsillo y se traba con un solo tornillo M3 en un extremo. Ahorra 2 insertos y 2 tornillos por nodo, pero pide ranuras de 1 mm en paredes de 3, que conviene probar en una probeta antes. Con 2 o 3 pletinas por lado la tapa carga de 1.7 a 2.5 N dentro del agua, así que cualquiera de las dos alcanza.

## 9. Versión simple para el prototipo en el aro Ø200 y suspensión propia de la linterna (29/10)

> **Esta sección describe la V1.** La versión vigente es la V2 (caja baja, KIT A, cámaras hacia la malla): ver la sección 10.

Generada por `cad_final/simple.py` (`build.py --rapido` con `version = "simple"`, unos 40 a 65 s). Números completos y
verificación en `cad_final/reporte_simple.md`; piezas en `salida/simple/` (STL y STEP por pieza, ensamble con la
linterna `ensamble_simple_D200.step`, riel fusionado para SimScale en `simscale/`), separador en `salida/linterna_prueba/`.

**Piezas (9 tipos impresos + ventana, 15 piezas impresas por nodo; la modular tenía 16 tipos y 28 piezas en Ø200):**
M1, M2, M11, M4, M6 y M7 iguales; **M3s** mitad del riel (2, la misma pieza girada; media cámara de cables, bolsillo
del lastre, unión plana en x = 0 bajo la caja con 4 M3 en orejas, sin varilla M8); M3t tapa del bolsillo (2, igual);
**M9s** gancho en C fijo con ranura de correa de 25 (2; reemplaza a M9, M12, M13 y M14); **M5s** tapa de la cápsula con
pie en silla a ángulo fijo (2; `capsula.angulo` = 30; reemplaza a M5 y M10, sin bisagra dentada).

**Suspensión nueva:** la linterna cuelga de su brida: 4 cuerdas a 60/120/240/300 (`linterna.cuerda_azimut`) suben
verticales del aro al separador LR1 (`separador.tipo` aro, a 250 sobre el aro) y de ahí al ápice (`apice.altura` 150
sobre el separador = **400 sobre el aro**), y un cabo vertical va al punto fijo (`linterna.punto_fijo` = estructura).
El nodo no carga la linterna: va enganchado al aro con los ganchos y la correa; el ojal del asa queda solo para izar.
El umbilical baja de la boya con comba. A 45 grados (el azimut de la modular) no había ápice posible en Ø200: la brida
de la caja llega a r = 103, fuera del aro.

| Resultado (bandeja al 40 %) | Valor |
|---|---|
| Peso en aire | **2079 g** (≤ 3 kg) |
| Peso aparente | **+265 g** con 3 pletinas por bolsillo (`lastre.pletinas`; 3 o 4 entran en la ventana de +200 a +500) |
| Sin pletinas | −251 g: el nodo flota; sin la varilla M8 hace falta 1 pletina más por bolsillo que en la modular Ø200 |
| Estabilidad | BG = 17.4 mm con las cápsulas a 30 grados (la modular Ø200: 20.2 a 0 grados) |
| Aire mínimo cuerdas/separador contra el nodo | **21.6 mm** (cuerdas verticales; exigido 10), con cápsulas y ganchos puestos |
| Separador | 250 sobre el aro; el mínimo calculado es 165 (aro); con cruceta sube porque pasa sobre el asa |
| Cable por cámara | 420 mm: requiere la prueba SPI (C6 sigue) |

**¿Cambia el peso aparente por la suspensión?** No: el peso aparente es masa del nodo menos agua desplazada y no
depende de quién cargue la linterna. Lo que cambió (de +225 a −251 sin pletinas) es por el modo simple: sin la varilla
M8 (unos 167 g de acero) ni las piezas chicas. Se corrige con las pletinas.

**Chequeos de este reporte que cambian en la versión simple:**

| Chequeo | Modular | Simple |
|---|---|---|
| §2 de `reporte_verificacion.md`, riel con 150 N | Caso A (colgado del asa) mandaba | En el agua manda el caso B (apoyado en los ganchos): σ 6.5 MPa, FS 6.9 / 3.4 |
| §3, §3b, §3c, unión de tramos y varilla M8 (C19) | FS 1.3 / 0.6 sin varilla en Ø200, varilla obligatoria | **No aplican**: una sola unión, bajo la caja (que la puentea con 4 M4); sin contar la caja, 61 N por M3 |
| §4, insertos M4 del fondo | 251 N por inserto (Ø200) | 254 N, solo al izar por el asa fuera del agua; se prueba con PB8 |
| §5, gancho con 75 N | J con casquillo, pestillo y perilla | C fija: σ 7.5 MPa, FS 6.0 |
| §6b, linterna colgada del ojal (C15) | 180 N en el asa | **Desaparece**: el asa solo iza el nodo (§6, 150 N, sigue) |
| §7, bisagra dentada | Precarga del M4 contra el salto de dientes | **Desaparece**. Nuevo: pie de la cápsula, 602 N por M4 y 17.9 MPa en las paredes del riel, **FS 1.2 a través de las capas**: es el punto débil, probar con la mano antes del agua |
| §9, flotabilidad y estabilidad | +225 g con 2 pletinas por lado | +265 g con 3 por lado, BG 17.4 mm |
| C6, cable | 300 o más, prueba SPI | 420, prueba SPI |
| C15, C20, C21 | Cuerdas al asa; pestillo contra perilla; grillete para las cuerdas | C15 se revierte (cuerdas a la brida propia); C20 no existe; C21 queda solo para izar |

**Por verificar en la versión simple:** `aro.seccion` (8, la varilla del aro real), el alma del pie de la cápsula
(sin cálculo: SimScale o prueba a mano), el apriete de los M4 del pie en el PETG impreso a través de las capas, y que
el umbilical salga entre las cuerdas del ápice sin rozarlas (en el render pasa por dentro de la brida).

## 10. Observaciones y medidas del equipo (29/10) y versión simple V2

Fuente: decisiones del chat de Melissa del 29/10. `chatgpt_boya_medidas.md` no existía en Downloads, así que no hay
más medidas que esas. Todas entraron en `params.py` como origen **equipo**, estado **por_verificar**, solo para la
versión simple (la modular no cambia).

### 10.1 Equipo contra CAD

| Parámetro | Valor del equipo | Valor que tenía el CAD | Diferencia | Qué se hizo / estado |
|---|---|---|---|---|
| `material` | PETG opaco, no ASA | PETG (`petg.*`) | ninguna | Registrado. **Aplicado** |
| `simple.esp32_base` | ESP32-S3 N16R8 sobre KIT A + módulos sueltos | sin_base (DevKit suelto) | caja más grande: 127 × 126 × 77 (antes 139.6 × 106 × 50) | **Aplicado** en 2 pisos: con 1 piso la brida (170) quedaba a 1.6 mm de las cuerdas a 60°. `esp32.base` sigue en sin_base para la modular |
| `camara.envolvente` | Arducam Mega 5MP 33 × 33 × 17, fabricante | 33 × 33 × 17, fabricante, confirmado | ninguna | Sin cambio |
| `capsula.acimut` | cámaras inclinadas hacia la malla | hacia afuera (V1) | 180° | **Aplicado** (adentro, 30°). Ver 10.3: en Ø200 la red queda a 38 mm del lente |
| `ventana.antibiofouling` | spray en las ventanas | no estaba | ninguna en la geometría | Registrado |
| `enlace.nodo_boya` | RS-485 dentro del umbilical | XY-017 RS-485 ya estaba en la caja | ninguna | Registrado |
| `boya.caja_exterior` / `boya.caja_interior` | ~220 × 200 × 120 / 210 × 190 | casco 177 × 97 × 76 (derivado del layout) | +43 / +103 / +44 mm | **Aplicado** en la boya propia (cuerpo; la brida de la tapa da 240 × 220). Hace que nodo + boya pase de 3 kg (10.4) |
| `boya.panel` | 170 × 170 encima | 170 × 170 × 3 | ninguna | Sin cambio (corrido a −X para dejar libre la antena) |
| `boya.flotadores_esquinas` | 4 flotadores modulares en las esquinas | 2 pontones de 2 módulos a los lados | forma | **Aplicado**: 4 flotadores huecos de 100 × 100 × 60 atornillados con M5 a cojines |
| `boya.antena_interior` | antena LoRa pequeña dentro, despejada de metal y del panel | mástil B4 exterior | sin mástil | **Aplicado**: antena dentro en el extremo +X, fuera de la proyección del panel |
| `boya.sma_ciego` | agujero ciego para SMA de panel, lejos de los cables | pasamuros desactivado | nuevo | **Aplicado** en la pared +X (los PG7 están en −X) |
| PG7 del umbilical abajo, ojal independiente | | ya era así | ninguna | Mantenido |

**No apliqué:** nada quedó afuera, pero dos decisiones del equipo chocan con exigencias: la caja de la boya de
220 × 200 × 120 con el KIT A en el nodo lleva el total a **5168 g contra 3 kg** (10.4), y las cámaras hacia la malla
quedan **más cerca de la red que el enfoque mínimo estimado** en Ø200 (10.3). Hay que decidirlas con el equipo.

### 10.2 Nodo: antes (V1) y después (V2)

Alturas sobre el centro de la varilla del aro. V2 = KIT A en 2 pisos + caja baja + cámaras hacia la malla.

| Concepto | V1 | V2 |
|---|---|---|
| Nodo de / a | −40 / +210 mm | −40 / +181 mm |
| Altura total | 250 mm | **221 mm** |
| Centro de masa | +66.5 mm | **+45.9 mm** |
| BG (estabilidad) | 17.4 mm | 18.2 mm |
| Separador / ápice sobre el aro | 250 / 400 mm | 140 (mínimo 136) / **290 mm** |
| Peso en aire | 2079 g | 2462 g (caja con KIT A y 5 pletinas por bolsillo) |
| Peso aparente | +265 g | +205 g (ventana +200 a +500) |
| Aire mínimo suspensión-nodo | 21.6 mm | 11.6 mm (exigido 10) |
| Piezas impresas por nodo | 15 (9 tipos) | 14 (9 tipos, con 2 bandejas) |
| FS del pie entre capas | 1.2 | 2.2 a mano, 2.5 FEM |
| Cable por cámara | 420 mm | 379 mm (sigue la prueba SPI) |

Cambios de V2: los PG7 de las cámaras pasan por las paredes extremas de M1 y el domo entra en el conducto del riel
(no hay cámara de cables ni bloque bajo la caja); el riel son 2 mitades M3s atornilladas a cojines de la caja con el
gancho en C **fusionado** (alma de 20 y pared de la C de 6, por el FEM); los bolsillos del lastre van moldeados bajo
M1; el pie de la cápsula cumple FS ≥ 2 entre capas sin inserto ni pared de 6 porque con la cápsula mirando adentro la
palanca es corta. Tapas, cápsulas y bandejas siguen desmontables.

### 10.3 Cámaras hacia la malla

FOV 70° diagonal y enfoque desde 8 cm (los dos estimados, sin ficha). En Ø200 el eje óptico corta la red a **38 mm**
del lente (campo diagonal 53 mm): **fuera del enfoque estimado**. Opciones: alargar el riel unos 50 mm por lado (la
cápsula queda más afuera), inclinar a 70° o más, o confirmar con la ficha que enfoca a 4 cm. En Ø500 (mismo nodo) el
eje no corta la red dentro de su alto. El aro LED ilumina el encuadre si su haz es al menos igual al FOV (dato por
confirmar).

### 10.4 Boya propia y peso del sistema

Boya B1s..B6s (`cad_final/reporte_boya_simple.md`): **2705 g**, calado 31.6 mm, francobordo **88.4 mm** (≥ 50),
reserva 194 %, GM 92 / 467 mm. **Nodo + boya = 5168 g: 2168 g sobre los 3 kg.** Lo que más pesa: el casco al 100 %
(957 g), la tapa (331 g), el panel (350 g, estimado) y los 4 flotadores (464 g). Para bajar: casco y tapa a 5
perímetros con 40 % de relleno (la boya está seca), flotadores de espuma con cáscara fina, y pesar el panel real.

### 10.5 Sistema, FEM y slicer

- `ENSAMBLE_sistema_simple.step`: nodo + LR1 + cuerdas + linterna a 1 m + boya, piezas nombradas. U1 (manguera Ø10
  de referencia) mide 950 mm: con el umbilical de 3 m sobran 2050; radio mínimo 61 (exigido 60), 7.5 mm de la
  suspensión. C1 del ápice al ojal de la boya (648 mm) carga la linterna; el cable no.
- FEM local (Gmsh + CalculiX 2.22, `salida/simple/fem/`), 150 N en una cápsula, PETG estimado e isótropo:
  riel en el agua 8.4 MPa (FS 5.4 / 2.6 entre capas), riel al izar 4.2 MPa (FS 10.9 / 5.3), pie 8.9 MPa (FS 5.0 / 2.5).
  El FEM mostró que en el agua un solo gancho lleva los 150 N (el cálculo a mano suponía 75): de ahí el alma de 20.
  SimScale: pasos manuales en `salida/simscale/SIMSCALE.md`. No se afirma estanqueidad por simulación.
- Slicer (OrcaSlicer, P1P 0.4, 0.20 mm, 3 paredes, giroide con el relleno de cada pieza; corrido en otra sesión):
  nodo 1307 g / 47.1 h / S/ 117.59, LR1 37 g / 1.6 h, boya 2179 g / 72.5 h / S/ 196.10. Las piezas impresas pesan
  más que lo que supone la flotación (nodo +79 g, boya +236 g): el peso aparente real será algo mayor.

### 10.6 Chequeos de este reporte

Ninguno se rompió: insertos M4 de las bridas 339 N al izar (§4 exige 345 N: probar con PB8), peso aparente en la
ventana, BG positivo, aire ≥ 10, FS ≥ 2 entre capas en riel, gancho y pie. Cambian de forma: §3 (uniones) y §6b
(linterna en el asa) no aplican en la simple; el gancho se verifica con 150 N.

## 11. Prototipos, boya PET y entrega (30/10, noche, sin el equipo)

Plan: `HANDOFF_2026-10-30_v2.md` §4 y `docs/HANDOFF_noche.md`. Decisiones con su forma de revertir: `docs/DECISIONES.md`
(raíz del repo). Documento para el equipo: `docs/LANTERNGUARD_ENTREGA.pdf`.

### 11.1 Qué se hizo
- **Prototipos del nodo** (`docs/PROTOTIPOS.md`, `salida/prototipos/`): P0 original (simple V1 y modular, geometría sin
  tocar), P1 mínimo, P2 robusto, P3 monocasco y P4 estético, todos desde `simple.py` con banderas de `params.proto`.
  Recomendación: **P2 para la piscina** (1400 g, 46.7 h, S/ 126.0, FS riel 5.6 / 2.7, pie 5.0 / 2.5) y **P4 para
  presentar** (1352 g, 46.0 h, S/ 121.7, FS 4.7 / 2.3). P1 descartado (FS 2.0 entre capas).
- **Correcciones de Yoichi** (tanda 3, `683ade1`): linterna sin separador ni ápice (aro + 4 cuerdas a un nudo a 400 mm +
  cabo), nodo girado con los brazos a 45° entre cuerdas (aire ≥ 10 mm a brazo y cápsula); lastre a granel en un bolsillo
  por lado (`lastre_izq`/`lastre_der`, 1020 a 1150 g para 0.35 kgf); cajas de P1, P3 y P4 más chicas (menos aire).
- **Boya PET** (`docs/BOYA.md`): tres vueltas; queda **4 × 1 L en cruz** (casco + 2 cunas + 4 correas): 863 g, 32.0 h,
  S/ 77.7, calado 39.5 mm, francobordo a la abertura 82 mm, GM 112 / 762 mm, reserva 136 %. Con una botella perdida
  vuelca sin espuma y queda estable con la espuma estimada (6 a 12°). No cumple 700 g ni 25 h.
- **Onshape**: carpeta LanternGuard con `LG_00_LEER_PRIMERO` (el PDF), `LG_P0` a `LG_P4`, `LG_boya_PET` y `_v2`,
  `LG_sistema`, `LG_probetas`. Pestañas de ensamble con nombres (código para lo impreso, `REF_` para lo demás),
  verificadas contra el STEP (`onshape_push.py --verificar`). `M1m_caja_riel` y el umbilical solo entran con
  `allowFaultyParts` (pestaña `ENSAMBLE_v2_completo`).
- **Planos**: `planos/PLANOS_LanternGuard.pdf`, 27 láminas (P2, P4, boya).
- **Impresión**: 17 placas sin fallas, 2469 g y 84.7 h (`salida/imprimir_hoy/`, 3MF en Drive), capturas del slicer en
  `salida/capturas_slicer/`.
- **Bitácora**: BITACORA.xlsx y BOM.md con P2, P4 y la boya PET.

### 11.2 Lo que no salió como se pedía
- Boya: 4 × 500 ml (lo pedido) vuelca si pierde una botella y no llega a GM ≥ 40 en un solo casco; se recomendó 1 L.
- Boya: masa y horas por encima del objetivo (863 g contra 700; 32 h contra 25).
- Cuerda a brida de la tapa: 2.9 mm en P2 (6.8 en P4). Aviso, no falla; tres opciones en `docs/PROTOTIPOS.md`.
- Onshape no cura `M1m_caja_riel` ni el umbilical al importar (en OCCT son válidos): entran marcados como "faulty".
- `cad_final/variantes.py` quedó roto (usa las firmas viejas de `plates`, `assemble` y `lantern`).
- Densidad a granel del lastre (4.5 g/cm³ tuercas, 6.5 perdigón) y espuma PU (50 % de llenado): estimadas.

### 11.3 Chequeos
Builds de V2, P1 a P4, sistema y boya: "FALLAS: ninguna". Slicer: 17 de 17 placas. Onshape: partes = sólidos en todas
las pestañas de ensamble indicadas en `docs/LINKS.md`. Nada de esto reemplaza las probetas: nada se declara listo para
imprimir sin PB6 a PB10.
