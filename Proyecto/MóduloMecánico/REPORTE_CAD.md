# Reporte CAD, versión final del nodo LanternGuard

Rama local `cad/version-final` (sin push). Fuente única de medidas: `cad_final/params.py` (276 parámetros, cada uno
con origen y estado). Todo se regenera con los scripts de `cad_final/`. Detalle por fase en `FASE_A.md` a `FASE_G.md`.

## 1. Estado en una línea por cosa

| Qué | Estado | Dónde |
|---|---|---|
| Probetas (gancho, ranura T, unión, pestillo, perilla, junta, peine) | **Listas para imprimir.** Son lo primero: sirven para medir holguras | `salida/probetas/` |
| Caja, tapa y bandeja del nodo | Preliminar: falta medir la electrónica y los PG7 | `salida/preliminar/` |
| Riel, gancho, casquillos, pestillo, perilla | Preliminar; **el largo del riel tiene una decisión pendiente del equipo** | `salida/preliminar/` |
| Cápsula y carro | Preliminar; el carro depende del largo del riel | `salida/preliminar/` |
| Boya | Preliminar: masas de componentes estimadas, francobordo con 4 mm de margen | `salida/boya/` |
| Ensambles por aro | Hechos, con conflictos de largo de riel | `salida/ensambles/` (renders; STEP se regeneran) |
| SimScale | 4 STEP simplificados y la guía con el resultado a mano esperado; las simulaciones las corre el equipo | `SIMSCALE.md`, `salida/simscale/` |
| `salida/final/` | **Vacía a propósito**: ningún parámetro está medido todavía (0 de 276 con origen "medido") | `salida/final/LEEME.md` |

## 2. Inventario de piezas

| Pieza | Script | Cant. por nodo | Relleno | Orientación de impresión | Soportes |
|---|---|---|---|---|---|
| M1 caja, cuerpo | `fase_c_caja.py` | 1 | 100 %, 5 perímetros (sellada) | boca arriba, fondo en la cama | no; falda de la brida a 45° |
| M2 caja, tapa | `fase_c_caja.py` | 1 | 100 %, 5 perímetros | cara de la ranura en la cama, asa arriba | no |
| M11 bandeja | `fase_c_caja.py` | 1 | 40 % | plana | no |
| M3 tramo central (cámara de cables) | `riel.py` | 1 | 100 %, 5 perímetros | brida abajo | **sí** (8958 mm² de voladizo) |
| M3 extensión | `riel.py` | 0 a 2 por lado | 100 %, 5 perímetros | acostada (capas a lo largo) | casi nada |
| M9 gancho | `gancho.py` | 2 | 40 % | de costado (capas en planos XZ) | bajo el escalón brida/alma |
| M13 casquillo Ø6/8/10/12 | `gancho.py` | 2 del Ø de la varilla | 100 % | de pie | no |
| M14 pestillo | `gancho.py` | 2 | 100 % | plano | no |
| M12 perilla | `gancho.py`, `capsula.py` | 4 (2 ganchos + 2 carros) | 40 % | plana | no |
| M10 carro | `capsula.py` | 2 | 40 % | de costado | 899 mm² de voladizo |
| M4 cápsula, cuerpo | `capsula.py` | 2 | 100 %, 5 perímetros | eje óptico vertical | 1054 mm² |
| M5 cápsula, tapa | `capsula.py` | 2 | 100 %, 5 perímetros | de canto | 499 mm² |
| M6 bisel | `capsula.py` | 2 | 40 % | plano | no |
| M7 ventana | `capsula.py` | 2 | acrílico de 3, no se imprime | | |
| Pletina de inox 25 × 5 × 100 | `camara.py` | 3 por lado | acero | | |
| B1 a B6 boya | `boya.py` | ver `FASE_G.md` | 100 % casco y tapa | ver `reporte_boya.md` | lengüeta de B5 y casco |

Ninguna pieza pasa de 150 mm salvo la caja (159.6) y el casco de la boya (209), que caben en la cama de 220 × 220.

## 3. Qué cambió respecto del diseño anterior

La tabla completa anterior → nuevo → origen → razón la genera `cad_final/reporte_parametros.py` en
`cad_final/reporte_parametros.md` (§1). Lo grande:

- La caja se dimensionó desde la bandeja: 159.6 × 126 × 55 con brida, un piso, 484 cm³ de aire (antes 797).
- El brazo M3 pasó a un riel modular: tramo central que es una cámara de cables bajo la caja + extensiones de 100.
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
| C15 (cuerdas en Ø100) | Sigue y se extiende a Ø200: las cuerdas a 45° atraviesan la caja con cualquier ápice. Ø300 pide ápice ≥ 535, Ø500 ≥ 273 |
| C16 (domo del PG7) | Sigue: medir el prensaestopas; fija el alto de la cámara |
| C17 (riel 57 bajo la caja) | Revisado: los ganchos no tocan la caja |
| **C18 (nuevo, Fase D)** | **El riel no llega**: la punta debe estar en R + 64 y faltan de 9 a 74 mm. La tabla del equipo (230 / 430 / 630) no sale de un central de 140 + extensiones de 100. Decide el equipo; tres salidas en `FASE_D.md` |
| **C19 (nuevo, Fase E)** | La media madera de la unión queda con FS 1.1 (Ø500) y bajo 1 si se alarga el riel. Va junto con C18 |

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
- **Peso:** nodo de 1.86 a 2.07 kg (≤ 3), peso aparente de +208 a +253 g (ventana de +200 a +500).

## 6. Pruebas físicas recomendadas, en orden

1. Imprimir las probetas: peine de holguras, encaje de los casquillos en varilla real (fuerza de entrada y salida),
   tuerca M4 en la ranura T, unión de tramos, pestillo con guante, perilla y junta.
2. Arranque de los insertos M4 en PETG (el fondo de la caja pide 274 N cada uno).
3. Unión de tramos a flexión hasta la falla, con y sin varilla M8.
4. Estanqueidad de la caja y de la cápsula: 24 h, 72 h y 7 días a 1 m.
5. Cable Cat5e de la longitud real con la cámara a 8 y 4 MHz.
6. Pesar el panel solar y la batería, y flotar la boya en un balde antes del mar.

## 7. Resumen simple

- **Listo para imprimir:** las probetas de `salida/probetas/`. Nada más todavía.
- **Preliminar:** el resto de las piezas del nodo, la cápsula y la boya. Están completas y chequeadas, pero las medidas
  de la electrónica, los prensaestopas, el domo del PG7, el anillo LED y las masas son estimadas.
- **Qué hay que medir:** la lista completa está en `cad_final/reporte_parametros.md` §2. Lo crítico: DevKit y módulos de
  la bandeja, prensaestopas PG7 (contratuerca y domo), varilla del aro, agujero del anillo LED, cámara, panel solar,
  baterías y la densidad del PETG del slicer.
- **Siguiente paso:** que el equipo decida el largo del riel (C18). Con eso se rehacen los ensambles y la unión, y se
  imprimen las probetas.
