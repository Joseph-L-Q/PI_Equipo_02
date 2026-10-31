# Fase G: boya de superficie (B1..B6)

Generado por `cad_final/boya.py`. Todo numero sale de `params.py` o del modelo; lo que no esta medido va marcado como estimado. Esto es una estimacion de geometria, no una certificacion de flotacion ni de estabilidad en mar.

## Geometria derivada del layout

- Cavidad 169 x 89 x 72 mm (referencia del handoff: 220 x 200 x 120 exterior). Casco exterior 177 x 97 x 76; con brida 197 x 117.
- Portabaterias 80 x 70 x 30 centrado en x = y = 0, sobre 4 refuerzos M3 de 6 mm (z = 10..40); bateria baja y asegurada.
- Bandeja B1b (z = 43..46) sobre 4 postes M3, con PCB 70 x 73.5 y, en columna, Waveshare D y RTC. Altura libre sobre la bandeja 25 mm (estimada) + 5 de aire.
- Umbilical: PG7 en el fondo en x = -70.8; codo de R25 (mayor entre el minimo del equipo y 4 x Ø6) que sube a z = 50.0, apenas sobre la bandeja. Cable solar por PG7 en la pared -X (y = 25, z = 55).
- Panel 170 x 170 x 3 a 25 mm sobre la tapa (rango del equipo 20..30); sobresale del casco en Y. Los largueros B3 se apoyan en 4 de los tornillos M3 de la tapa, que se reemplazan por M3 largos: no perfora la tapa. Drenaje: sin bolsillos, patas separadas, el agua de la tapa escurre libre.
- Plataforma: flotadores B5 en dos pontones de 2 modulos (300 mm) a cada lado, plataforma 300 x 329 mm (referencia inicial 320 x 300). Union casco-flotador: orejas del casco + lenguetas del flotador + tornillo M5 inox con tuerca en bolsillo (4 uniones).
- Amarre: ojal B6 atornillado a la oreja del extremo +X del casco con un M5 propio; el umbilical sale por el fondo en el extremo -X y no recibe tension.

## Piezas

| Pieza | Cant. | bbox en impresion (mm) | Cabe en cama | Orientacion | p1 (mm) | min (mm) | Voladizo > 45 (mm²) | Volumen (cm³) | BRep | STL cerrado, cuerpos |
|---|---|---|---|---|---|---|---|---|---|---|
| B1 casco central | 1 | 209.0 x 141.0 x 76.0 | si | sin girar | 2.00 | 2.00 | 765 | 312.7 | ok | si, 1 |
| B1b bandeja | 1 | 124.0 x 85.0 x 3.0 | si | sin girar | 1.31 | 1.30 | 0 | 31.5 | ok | si, 1 |
| B2 tapa | 1 | 197.0 x 117.0 x 5.0 | si | X180 | 2.89 | 2.88 | 0 | 112.5 | ok | si, 1 |
| B3 larguero del panel | 2 | 24.0 x 140.0 x 33.0 | si | X180 | 2.00 | 2.00 | 73 | 33.6 | ok | si, 1 |
| B4 mastil de antena | 1 | 30.0 x 123.0 x 144.0 | si | sin girar | 3.00 | 3.00 | 0 | 29.1 | ok | si, 1 |
| B5 flotador (cuerpo) | 4 | 150.0 x 109.0 x 48.4 | si | sin girar | 1.60 | 1.60 | 1284 | 72.1 | ok | si, 1 |
| B5b tapa del flotador | 4 | 150.0 x 90.0 x 1.6 | si | sin girar | 1.60 | 1.60 | 0 | 21.4 | ok | si, 1 |
| B6 ojal de amarre | 1 | 50.0 x 24.0 x 6.0 | si | sin girar | 3.56 | 3.30 | 0 | 5.8 | ok | si, 1 |

Criterio p1 >= 1.2: todas cumplen.
Piezas con una dimension > 150 (limite de pieza del equipo): B1 casco central, B2 tapa. B1 y B2 son el casco/tapa (excepcion admitida); cabida en la cama real 220 x 220 x 250 (por verificar) se evalua arriba.
Notas de impresion: B1 y B2 y todas las piezas macizas al 100 % de relleno y 5 perimetros; B5 son cuerpo abierto + tapa B5b de 1.6 mm (4 perimetros): se llena de espuma y se cierra pegando la tapa (o con la boca de Ø10 de la tapa, que se sella); la lengüeta de B5 sale en voladizo de 19 mm (puente o soporte local, ver columna de voladizo). B3 se imprime con las patas hacia arriba (girada 180° sobre X).

## Interferencias en el ensamble (volumen comun, mm³)

| Par | Volumen |
|---|---|
| casco-flotadores | 0.000 |
| casco-bandeja | 0.000 |
| casco-tapa | 0.000 |
| casco-bateria | 0.000 |
| casco-pcb zona | 0.000 |
| casco-waveshare | 0.000 |
| casco-rtc | 0.000 |
| bandeja-bateria | 0.000 |
| tapa-pcb zona | 0.000 |
| pcb zona-waveshare | 0.000 |
| waveshare-rtc | 0.000 |
| tapa-largueros | 0.000 |
| tapa-mastil | 0.000 |
| panel-mastil | 0.000 |
| panel-largueros | 0.000 |
| panel-flotadores | 0.000 |
| panel-casco | 0.000 |
| flotadores-largueros | 0.000 |
| ojal-casco | 0.000 |
| ojal-flotadores | 0.000 |
| flotador-flotador | 0.000 |
| flotador-tapa de otro | 0.000 |
| tapa flotador-panel | 0.000 |
| cable-casco | 0.000 |
| cable-bandeja | 0.000 |
| cable-bateria | 0.000 |
| cable-pcb | 0.000 |
| cable-tapa | 0.000 |

Tolerancia 0.01 mm³: sin interferencias.

## Masa total

| Elemento | Masa (g) | Origen | CG z (mm) |
|---|---|---|---|
| B1 casco (100 %) | 397.1 | calculado de la geometria (densidad PETG por verificar) | 37.1 |
| B1b bandeja | 40.0 | calculado de la geometria (densidad PETG por verificar) | 44.5 |
| B2 tapa (100 %) | 142.9 | calculado de la geometria (densidad PETG por verificar) | 78.5 |
| B3 larguero | 85.4 | calculado de la geometria (densidad PETG por verificar) | 106.4 |
| B4 mastil+placa | 37.0 | calculado de la geometria (densidad PETG por verificar) | 118.9 |
| B5 flotador (cuerpo) | 366.2 | calculado de la geometria (densidad PETG por verificar) | 16.4 |
| B5b tapa del flotador | 108.6 | calculado de la geometria (densidad PETG por verificar) | 49.2 |
| B6 ojal | 7.3 | calculado de la geometria (densidad PETG por verificar) | 10.0 |
| 3 x celdas 18650 | 141.0 | estimado | 25.0 |
| portabaterias | 25.0 | estimado | 25.0 |
| PCB + Heltec | 35.0 | estimado | 54.3 |
| Waveshare D | 15.0 | estimado | 51.0 |
| RTC DS3231 | 8.0 | estimado | 53.0 |
| panel solar 5 W | 350.0 | estimado | 115.5 |
| antena LoRa | 20.0 | estimado | 280.0 |
| cables, fusible, conectores | 40.0 | estimado | 54.0 |
| 2 x PG7 | 20.0 | estimado | 30.0 |
| tornilleria e insertos | 60.0 | estimado | 38.0 |
| espuma de celda cerrada (4 flotadores) | 70.4 | estimado | 16.4 |
| pasamuros SMA (desactivado) | 0.0 | opcional | 221.0 |
| **Total** | **1969** | | KG = 56.9 |

Nada de esto esta confirmado por pesaje: las piezas impresas salen del volumen del modelo por la densidad del PETG (1.27 g/cm³, por verificar) con 100 % de relleno (conservador); los componentes son masas tipicas (`boya.masas`, estimadas) y el panel es la mayor incertidumbre (350 g). Con B1b, B3, B4 y B6 al 40 % la masa baja 39 g.

## Hidrostatica (agua de mar 1025 kg/m³)

Metodo: el calado T se resuelve por biseccion sobre el volumen sumergido real (interseccion BRep de los solidos envolventes casco+tapa y 4 flotadores con el semiespacio z <= T) hasta que ρ·V(T) = masa total. Formulas: `KB` = z del centroide del volumen sumergido; `BM = I_wp / V`; `GM = KB + BM − KG`; I_wp del plano de flotacion como suma de rectangulos (casco y 4 flotadores, esquinas redondeadas ignoradas, sobreestima poco); `KG` = suma(m·z)/suma(m) con las posiciones de la tabla.

| Magnitud | Valor |
|---|---|
| Masa total M | 1969 g |
| Desplazamiento necesario V = M / ρ | 1921.0 cm³ |
| Calado T (desde el fondo del casco) | 26.9 mm |
| Francobordo (tapa, T hasta z = 81) | 54.1 mm (minimo 50): **CUMPLE** |
| Francobordo de los flotadores (alto 50) | 23.1 mm |
| Area del plano de flotacion (rectangulos) | 71169 mm² (dV/dT numerico: 70928 mm²) |
| Carga util extra con francobordo >= 50 | 296 g |
| Reserva de flotacion (V sellado total − V sumergido) / V sumergido | 118 % |
| KB | 13.4 mm |
| KG | 56.9 mm |
| I_wp alrededor del eje X (balanceo) / Y (cabeceo) | 8.210e+08 / 4.498e+08 mm⁴ |
| BM balanceo / cabeceo | 427 / 234 mm |
| **GM balanceo / cabeceo** | **384 / 191 mm** |
| Calado con rellenos al 40 % en piezas no selladas | 26.4 mm |
| Calado perdiendo un flotador completo (3 modulos, masa 1833 g, sin escora) | 30.9 mm |

**Lectura.** El francobordo cumple con 4.1 mm de margen. GM positivo y grande en los dos ejes indica estabilidad inicial alta para esta geometria de plataforma ancha; no dice nada del comportamiento con oleaje.

**Supuestos y limites.**
- Si un flotador filtra, la espuma de celda cerrada mantiene la flotabilidad; se supone cero absorcion de agua de la espuma. La espuma no se modela como solido: su masa se suma como estimada y su cavidad es la de la cascara.
- Incertidumbres que solo una prueba real resuelve: oleaje y rolido dinamico, torsion que introduce el amarre en la oreja del extremo, tension y peso del umbilical (3 m, Ø6) sobre el fondo del casco, viento sobre el panel y el mastil, masa real del panel y de las celdas, y estanqueidad de las juntas de la tapa y de los PG7 (el del umbilical queda sumergido).
- Retencion de los largueros B3 y del mastil B4: dependen de tornillos M3 largos en los insertos de la brida (5.7 de rosca, sin perforar la tapa); la carga de viento no se calculo.
- La lengüeta del flotador y la oreja del casco trabajan a cortante de un M5 y a aplastamiento del PETG; no se calculo resistencia. El ojal de amarre transmite la tension al casco por la oreja del extremo.

## Cadena de potencia (solo texto)

Panel solar -> Waveshare Solar Power Manager D (carga las celdas 18650 y entrega 5 V regulados) -> 5 V al sistema (PCB / Heltec / RTC). Sin segunda regulacion: la PCB de la boya debe tomar los 5 V de la salida del Waveshare directamente, sin otro conversor intermedio ni regulador en serie sobre el mismo bus. Comprobarlo contra el esquematico fisico (los agujeros y el conexionado de la PCB fabricada estan por verificar); el panel de 5 W nominales no garantiza potencia para todas las cargas, sobre todo con la radio transmitiendo.

## Parametros agregados a params.py (bloque `# boya (Fase G)`)

| Clave | Valor | Origen | Estado |
|---|---|---|---|
| boya.masas | {'celda_18650': 47.0, 'portabaterias': 25.0, 'pcb_heltec': 35.0, 'waveshare': 15.0, 'rtc': 8.0, 'panel': 350.0, 'antena': 20.0, 'cables_fusible': 40.0, 'prensaestopas': 20.0, 'tornilleria': 60.0} | estimado | por_verificar |
| boya.celdas | 3 | equipo | confirmado |
| boya.sma_pasamuros_g | 5.0 | estimado | por_verificar |
| boya.antena_largo | 110.0 | estimado | por_verificar |
| boya.sma_pasamuros | False | equipo | confirmado |
| boya.sma_agujero | 6.5 | estimado | por_verificar |
| boya.holgura_modulos | 5.0 | estimado | por_verificar |
| boya.alto_pcb_conectores | 25.0 | estimado | por_verificar |
| boya.apoyo_bateria | 6.0 | estimado | por_verificar |
| boya.aire_bateria_bandeja | 3.0 | estimado | por_verificar |
| boya.portabaterias_agujeros | (66.0, 56.0) | estimado | por_verificar |
| boya.bandeja_borde | 2.0 | estimado | por_verificar |
| boya.poste_D | 8.0 | estimado | por_verificar |
| boya.poste_aire_pared | 1.0 | estimado | por_verificar |
| boya.umbilical_margen | 3.0 | estimado | por_verificar |
| boya.cable_aire | 1.0 | estimado | por_verificar |
| boya.pg7_solar | (25.0, 55.0) | estimado | por_verificar |
| boya.panel_elevacion_usada | 25.0 | estimado | por_verificar |
| boya.riel_panel | (24.0, 140.0, 8.0) | estimado | por_verificar |
| boya.pata_D | 14.0 | estimado | por_verificar |
| boya.avellanado | (6.5, 3.0) | estimado | por_verificar |
| boya.panel_agujeros_y | 20.0 | estimado | por_verificar |
| boya.mastil | (14.0, 8.0, 140.0) | estimado | por_verificar |
| boya.mastil_placa | (30.0, 4.0) | estimado | por_verificar |
| boya.mastil_desfase | 11.0 | estimado | por_verificar |
| boya.flotador | (150.0, 90.0, 50.0) | estimado | por_verificar |
| boya.flotador_pared | 1.6 | estimado | por_verificar |
| boya.flotador_pared_interior | 3.0 | estimado | por_verificar |
| boya.flotador_separacion | 26.0 | estimado | por_verificar |
| boya.flotador_boca | 10.0 | estimado | por_verificar |
| boya.espuma_densidad | 0.03 | estimado | por_verificar |
| boya.oreja | (22.0, 12.0, 7.0) | estimado | por_verificar |
| boya.oreja_x | 55.0 | estimado | por_verificar |
| boya.lengueta | (19.0, 70.0, 5.0) | estimado | por_verificar |
| boya.lengueta_agujeros | (55.0, 95.0) | estimado | por_verificar |
| boya.m5 | (5.4, 8.0, 4.2) | estimado | por_verificar |
| boya.ojal | (24.0, 12.0, 6.0, 32.0) | estimado | por_verificar |
| boya.ojal_oreja_ancho | 24.0 | estimado | por_verificar |
| boya.oreja_agujero_punta | 7.5 | estimado | por_verificar |
| boya.flotador_radio | 8.0 | estimado | por_verificar |

## Renders

- `salida/boya/boya_iso.png`: ensamble.
- `salida/boya/boya_corte.png`: corte en y = 0.
- `salida/boya/boya_planta.png`: planta sin tapa.

STL y STEP por pieza en `salida/boya/stl` y `salida/boya/step`.
