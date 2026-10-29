# Reporte CAD, versión final del nodo LanternGuard

Rama `cad/version-final`. Fuente única de medidas: `cad_final/params.py` (294 parámetros, cada uno con origen y
estado). Todo se regenera con `python cad_final/build.py` (ver `README.md`). Medidas por pieza para el equipo en
`MEDIDAS.md`; planos por pieza en `planos/cad_final/`. Detalle por fase en `FASE_A.md` a `FASE_G.md`.

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

Ninguna pieza pasa de 150 mm salvo la caja (159.6) y el casco de la boya (209), que caben en la cama de 220 × 220.

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
