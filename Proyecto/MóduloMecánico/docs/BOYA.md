# Boya con botellas PET (bloque C)

Rediseño de la boya del nodo LanternGuard: la flotación la dan **botellas PET selladas** (más espuma PU como reserva) y el PETG impreso solo hace de estructura. Reemplaza a la boya de plataforma `boya_simple.py` (B1s..B6s). Todo sale de `cad_final/boya_pet.py` y de los parámetros `flotacion.*` y `boya_pet.*` de `cad_final/params.py`; los resultados están en `salida/boya_pet/` (`resultados.json`, `slicer.json`, `step/`, `stl/`, `boya_pet_iso.png`, `boya_pet_corte.png`, `ENSAMBLE_boya_pet.step`).

Regenerar: `python boya_pet.py` desde `cad_final/` (CAD, chequeos, OrcaSlicer y flotación). Cambiar de botella es un solo parámetro: `flotacion.botella = "500ml" | "1L" | "2L"` (o `--botella`).

## Qué es

Un casco abierto (no estanco) con dos bahías en las que se acuestan dos botellas de 1 L. Entre las botellas queda un canal de 50 mm por donde baja el umbilical. Sobre las botellas va una cubierta atornillada que impide que se salgan, y sobre la cubierta una caja seca (la única parte estanca de PETG) con la electrónica, a 6 mm de la cubierta. El panel solar de 170 x 170 va sobre 4 columnas, 25 mm por encima de la tapa de la caja. El mástil de la antena de la Heltec sale del extremo +X de la cubierta. El punto de amarre es un parche en el fondo del casco, en el eje, y no tiene nada que ver con el umbilical (que sale por el canal abierto del extremo -X, a través de un PG7 bajo en la pared -X de la caja).

Las botellas se sujetan con costillas: la del extremo de la base es cerrada (la base de la botella apoya y queda un anillo), la del extremo del cuello es una ranura en U sobre el hombro/cuello, y tres costillas intermedias llevan ranuras en U con 1.5 mm de holgura. Entre ranura y botella quedan huecos para inyectar la espuma PU por las ventanas de la cubierta (`flotacion.relleno = "espuma_PU" | "vacio"`). Paredes de 2.4 mm. Ninguna pieza de la boya necesita soportes.

## Piezas impresas

PETG, capas de 0.2 mm, 3 paredes, giroide al 40 %, sin soportes (voladizo medido bajo el umbral de 300 mm²). Masa y horas salen del G-code de OrcaSlicer (P1P, boquilla 0.4); costo con PETG a 90 soles/kg (`costo.filamento_soles_kg`).

| Pieza | STL | Cant. | Orientación | Soportes | Relleno | g | h | Costo (S/) |
|---|---|---|---|---|---|---|---|---|
| B1 casco (costillas, paredes con ventanas, parche de amarre, bosses M3) | `B1_casco.stl` | 1 | sin girar (abierto hacia arriba) | no | 40 % | 277.4 | 7.49 | 24.97 |
| B2 cubierta (barras, 4 pilares, 4 columnas del panel, mástil) | `B2_cubierta.stl` | 1 | sin girar | no | 40 % | 118.8 | 5.79 | 10.69 |
| B3 caja seca (con orejas, brida con chaflán, postes, 3 PG7) | `B3_caja.stl` | 1 | sin girar (piso en la cama) | no | 40 % | 171.0 | 5.49 | 15.39 |
| B4 tapa (ranura de junta) | `B4_tapa.stl` | 1 | `X180` (ranura hacia arriba) | no | 40 % | 57.2 | 2.10 | 5.15 |
| **Total** | | 4 | | | | **624.4** | **20.87** | **56.20** |

Objetivos: 700 g y 25 h, ambos cumplidos. Todas las piezas caben en la cama de 256 x 256 x 250 (el casco y la cubierta miden 254 x 225.6; **hay que correrlas fuera de la esquina excluida de 18 x 28 mm** de la P1P, el script lo hace al laminar: con ellas centradas, Orca se niega a laminar). El slicer es la fuente de las masas; las del CAD (`mass_g`) salieron 9 a 26 % más altas.

La caja se fija a los 4 pilares con M3 (orejas), la tapa con 14 M3 a insertos de la brida y una cuerda de junta de 2.6 mm en la ranura de 1.5 mm de profundidad, y la cubierta al casco con 8 M3 a insertos. El interior de la caja mide 142 x 84 x 72: componentes más 5 mm (PCB 70 x 73.5, Waveshare 45 x 40 x 10, portabaterías 3 x 18650 de 80 x 70 x 30, RTC reservado 40 x 25 x 15).

## Flotación (agua de mar 1025 kg/m³)

Botellas modeladas como cilindros con el **volumen nominal** (conservador): empuje = volumen nominal x cantidad. La espuma no entra en el cálculo base.

| Magnitud | Valor |
|---|---|
| Masa total de la boya (impreso 624 g + componentes + 2 botellas vacías 50 g + espuma 14 g) | 1412 g |
| Empuje máximo de las botellas (2 x 1 L) | 2050 g |
| **Calado** | **55.1 mm** |
| **Francobordo** a la abertura más baja de la caja (borde del PG7 del umbilical) | **51.4 mm** (mínimo 50: cumple) |
| Francobordo al plano de la junta de la tapa / a la cara inferior de la caja | 114.7 mm / 40.3 mm (la caja es estanca: su base no importa) |
| **Reserva de flotación** (empuje de botellas contra masa) | **638 g, 45 %** |
| Reserva extra por espuma (estimada: 462 cm³ de vacío, 50 % de llenado) | unos 460 g (estimado) |
| KB / KG | 34.0 / 125.7 mm |
| **GM balanceo / cabeceo** | **30.6 / 15.5 mm** (estimado) |
| Diferencia centro de empuje y de gravedad en x | 0.9 mm (trimado despreciable) |

El GM es positivo pero **corto**, sobre todo en cabeceo: lo limita el KG alto (el panel de 350 g está a 200 mm y la caja con la electrónica entre 100 y 175 mm). Lo que lo mejora, en orden: pesar el panel real, bajar la caja (apilar menos: poner la PCB junto a la batería en vez de encima baja unos 30 mm el KG, pero ensancha la caja y sube unos 110 g de PETG), y un canal más ancho (ayuda solo al balanceo; el casco ya está en 225.6 de los 228 que dejan la esquina excluida).

### Si se pierde una botella

Sin una botella el empuje de la otra (1025 g) no alcanza los 1412 g. La boya queda a flote solo por la caja estanca, con calado 124.5 mm (107.3 con la espuma estimada) y el centro de empuje 68.9 mm fuera del eje, con **GM negativo en ambos ejes (-57 / -47 mm)**: **no tolera perder una botella, vuelca**. La espuma estimada no lo arregla. Si se quiere redundancia hace falta más volumen (más botellas o botellas mayores), no solo espuma. Es un resultado del modelo de formas simples, no una prueba.

### Las tres botellas

Mismo script, `flotacion.botella` cambiado; las masas de las alternativas usan la masa del CAD (estimada, sin slicer).

| Botella | Cant. | Masa boya | Calado | Francobordo (abertura) | Reserva | GM bal. / cab. | Cabe en cama | Veredicto |
|---|---|---|---|---|---|---|---|---|
| 500 ml (Ø65 x 210) | 2 | 1381 g (est.) | 107 mm | -16 mm | -26 % (1025 g de empuje) | -60 / -49 mm | si | No cumple: las botellas no sostienen la boya, flota solo por la caja |
| **1 L (Ø80 x 270)** | **2** | **1412 g** | **55.1 mm** | **51.4 mm** | **45 %** | **31 / 16 mm** | **si** | **Elegida** |
| 2 L (Ø105 x 330) | 2 | 1614 g (est.) | 48.5 mm | 83.0 mm | 154 % | 143 / 189 mm | **no** (casco 254 x 275.6; botella de 330 mm mayor que el casco; la cubierta interfiere con la caja y la tapa) | No se puede imprimir en este diseño; sería la mejor flotación |

Tres botellas de 500 ml en fila (1537 g de empuje máximo) dejarían una reserva de solo unos 9 % y no se modelaron (el CAD solo cubre una fila de 2); cuatro no caben en la cama.

## Comparación con la boya de plataforma anterior

| | Plataforma (`boya_simple.py`) | PET (`boya_pet.py`) |
|---|---|---|
| Masa total de la boya | 2705 g | 1412 g |
| Impreso (slicer) | 2179 g, 72.5 h | 624 g, 20.9 h |
| Piezas impresas | casco, tapa, bandeja, 2 largueros, 4 flotadores, ojal | casco, cubierta, caja, tapa |
| Calado / francobordo | 31.6 mm / 88.4 mm (a la tapa) | 55.1 mm / 114.7 mm a la junta, 51.4 a la abertura |
| Reserva | 194 % | 45 % |
| GM | 92 / 467 mm | 31 / 16 mm |

Con el nodo de `REPORTE_CAD.md` 10.4 (2463 g) el sistema pasa de 5168 g a **unos 3875 g, todavía 875 g sobre los 3 kg** (cuenta aproximada: el nodo no se recalculó). Se ganó mucho peso y tiempo de impresión; se perdió estabilidad y reserva, que son las cifras a vigilar.

## Material

PETG alcanza para una piscina; si la boya va a estar semanas al sol, imprimir en ASA (el PETG se ablanda y se amarillea). Hay que confirmar con la boleta el precio de 90 soles/kg.

## Pendiente de medir o confirmar

- Dimensiones reales de las botellas (diámetro del cuerpo, largo total, diámetro y largo del cuello, forma del hombro) y su volumen real: están como "estimado" en `flotacion.botellas`. La costilla del cuello supone una ranura de Ø32 sobre un cuello de Ø30; con otra marca cambia.
- Masa real de todos los componentes, en especial el panel (350 g estimado) y las botellas vacías (25 g estimado). Es lo que más mueve el KG.
- Agujeros del panel real (las columnas llevan un inserto M3 arriba, la posición es provisoria) y si se pega con cinta VHB.
- Cuánto de verdad llena la espuma PU (`flotacion.espuma_llenado = 0.5` es un supuesto) y que su celda sea cerrada.
- Resistencia del parche de amarre y de los bosses (no se hizo FEM; la tracción real del cabo es dato por definir).
- PG7, cuerda de junta y el RTC reales; el interior de la caja es de 142 x 84 x 72 con 5 mm de holgura sobre las maquetas.
- Hidrostática de formas simples: sin oleaje, viento ni tensión del umbilical; la altura metacéntrica es una estimación, no una certificación.
