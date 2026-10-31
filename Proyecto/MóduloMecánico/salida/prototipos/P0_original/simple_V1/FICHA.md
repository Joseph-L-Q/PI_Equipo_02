# P0 original: simple V1 (aro Ø200)

**Qué es:** el primer diseño simple que le gustó a Yoichi (pestaña `simple_D200_V1` de Onshape). Regenerado sin tocar
la geometría desde el commit `8dda578` (el último antes del nodo V2, `e46a907`), con su propio `simple.py` y su
`params.py`. Queda como referencia para comparar; no se modifica.

**Cómo es:** caja alta 139.6 × 106 × 50 con la electrónica en una bandeja; riel en 2 mitades M3s (cuadrado 30, pared 4)
que pasan bajo la caja; gancho en C atornillado aparte (M9s, pared 4, interior 8.8 para la varilla de 8); cápsula de
cámara con pie fijo a 30° (M5s) atornillada al riel; lastre de pletinas de inox en 2 bolsillos (3 por bolsillo).

## Piezas y slicer (OrcaSlicer, P1P, PETG, 0.20 mm, una pieza por placa)

| Pieza | Cant. | Orientación | Soportes | Relleno | g c/u | h c/u |
|---|---|---|---|---|---|---|
| M1 caja, cuerpo | 1 | sin girar | sí | 100 % | 255.1 | 5.54 |
| M2 caja, tapa con asa | 1 | Y+90 | sí | 100 % | 172.8 | 4.95 |
| M11 bandeja | 1 | sin girar | no | 40 % | 34.0 | 1.38 |
| M3s riel, mitad | 2 | X180 | sí | 40 % | 170.1 | 8.92 |
| M9s gancho en C | 2 | X+90 | no | 100 % | 25.3 | 0.95 |
| M5s tapa con pie | 2 | X180 | sí | 100 % | 124.6 | 4.15 |
| M3t tapa del bolsillo | 2 | X180 | no | 100 % | 11.4 | 0.35 |
| M4 cápsula, cuerpo | 2 | Y-90 | sí | 100 % | 59.6 | 2.05 |
| M6 bisel | 2 | Y+90 | no | 40 % | 2.0 | 0.20 |
| M7 ventana | 2 | | | acrílico, no se imprime | | |

**Total impreso: 1248 g, 45.1 h, 112 soles** (PETG a 90 soles/kg). 17 piezas impresas, 9 tipos.

## Resultados (de su `resultados.json`)
- Peso en aire 2079 g (relleno 40 % en las zonas de relleno), peso aparente en agua de mar **+265 g** con 3 pletinas
  por bolsillo; sin pletinas flota (−251 g). BG 17.4 mm.
- FS, **cálculo a mano** (REPORTE_CAD §9, sin FEM: el FEM local llegó con la V2): riel 6.9 / 3.4 entre capas,
  gancho 6.0, **pie de la cápsula 2.5 / 1.2 entre capas** (el punto débil; la V2 lo corrigió).
- Insertos M4: 254 N por inserto al izar.
- Sellos: junta de la tapa de la caja, 2 tapas de cápsula y 2 ventanas (5 juntas) más 2 PG7 en el fondo de la caja.

## Archivos
`ensamble_simple_V1.step`, `step/` y `stl/` por pieza, `render_iso.png`, `render_lado.png`, `nodo_iso.png`,
`resultados.json`, `slicer.json`.

## Pendiente
Nada: es referencia. Lo que se aprendió de ella (pie débil entre capas, caja alta) está aplicado en la V2 y en P1 a P4.
