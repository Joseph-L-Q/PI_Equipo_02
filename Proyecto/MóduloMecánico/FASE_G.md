# Fase G: boya de superficie

`cad_final/boya.py` → `cad_final/reporte_boya.md`, STL y STEP en `salida/boya/`, renders `boya_iso.png`, `boya_corte.png`
y `boya_planta.png`. Todo preliminar: las masas de los componentes son típicas, no pesadas.

## Piezas

| Pieza | Cant. | bbox de impresión mm | Espesor p1 | Masa g (100 %) | Nota |
|---|---|---|---|---|---|
| B1 casco | 1 | 209 × 141 × 76 | 2.00 | 397 | cavidad 169 × 89 × 72 (la referencia era 220 × 200 × 120) |
| B1b bandeja | 1 | 124 × 85 × 3 | 1.31 | 40 | PCB, Waveshare y RTC arriba; batería abajo, centrada |
| B2 tapa | 1 | 197 × 117 × 5 | 2.89 | 143 | junta tórica y M3 con inserto, como la caja del nodo |
| B3 larguero del panel | 2 | 24 × 140 × 33 | 2.00 | 85 c/u | panel elevado sin perforar la tapa (M3 largos de la tapa) |
| B4 mástil de antena | 1 | 30 × 123 × 144 | 3.00 | 37 | vertical, fuera del panel; pasamuros SMA desactivado |
| B5 flotador, cuerpo | 4 | 150 × 109 × 48 | 1.60 | 366 c/u | relleno de espuma de celda cerrada |
| B5b tapa del flotador | 4 | 150 × 90 × 1.6 | 1.60 | 109 c/u | |
| B6 ojal de amarre | 1 | 50 × 24 × 6 | 3.56 | 7 | en el extremo +X, separado del umbilical (−X, por el fondo) |

Todas pasan BRep, STL cerrado de un cuerpo, cama y espesor; cero interferencias en el ensamble. Plataforma de 300 × 329.

## Hidrostática (agua de mar 1025 kg/m³)

| Magnitud | Valor |
|---|---|
| Masa total | 1969 g |
| Calado | 26.9 mm (volumen sumergido resuelto con los sólidos reales) |
| Francobordo | **54.1 mm** contra ≥ 50: cumple con 4.1 de margen |
| Carga extra hasta francobordo 50 | 296 g |
| Reserva de flotación | 118 % |
| GM balanceo / cabeceo | 384 / 191 mm (estimación con plano de flotación rectangular) |
| Con un flotador perdido | francobordo 50.1 mm (la espuma mantiene el empuje) |

Oleaje, torsión del amarre y carga del umbilical no están modelados: hace falta prueba real.

## Decisiones tomadas sin consulta

| # | Qué | Por qué | Descartado | Cómo revertir |
|---|---|---|---|---|
| D38 | Casco chico dimensionado desde el layout (cavidad 169 × 89 × 72) | El handoff pedía quedarse con lo menor entre el layout y la referencia | Casco de 220 × 200 × 120 | `boya.*` en `params.py` |
| D39 | Flotador partido en cuerpo abierto (B5) + tapa (B5b) | Cerrado, el techo hueco de 85 mm solo se imprimía de pie | Flotador cerrado con boca de llenado | `boya.py` |
| D40 | Unión casco-flotadores con orejas, lengüetas y M5 inox | Desmontable, sin pegamento | Pegado | `boya.py` |
| D41 | Largueros del panel y mástil apoyados en los M3 de la tapa (más largos) | No se perfora la tapa | Agujeros nuevos con junta | `boya.py` |
| D42 | Pasamuros SMA desactivado (`boya.sma_pasamuros = False`) | Lo pedía el handoff hasta tener antena de intemperie | | el parámetro |

## Cierre

- **Qué cambió:** se diseñó la boya completa (8 piezas, 13 impresiones), dimensionada desde la electrónica, con el ojal de
  amarre separado del umbilical.
- **Qué chequeos pasaron:** las 8 piezas caben en la cama y pasan BRep, STL y espesor; francobordo de 54.1 contra 50, y GM
  positivo en los dos ejes.
- **Qué quedó pendiente:** pesar el panel (está estimado en 350 g y con unos 40 g más el francobordo baja de 50), los
  soportes de impresión de la lengüeta de B5 y del casco, y la resistencia de la unión con M5, del ojal y del soporte del
  panel contra el viento. El PG7 del umbilical queda bajo el agua: depende de la prueba de estanqueidad.
