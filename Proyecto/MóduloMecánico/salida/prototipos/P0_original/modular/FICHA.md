# P0 original: versión modular (riel por tramos, aro Ø200)

**Qué es:** el primer diseño completo, pensado para aros de Ø100 a Ø500 (`version = "modular"`, REPORTE_CAD §1 a §8).
Copiado sin tocar desde `salida/preliminar/` (último cambio de geometría en `68c8aaa`, 29/10) y `salida/ensambles/`
(Ø200). Queda como referencia para comparar; no se imprime (ver `NO_LISTO_PARA_IMPRIMIR.md`).

**Cómo es:** caja sellada con asa; riel modular (tramo central que hace de cámara de cables bajo la caja, extensiones de
100 mm y puntas) con varilla M8 pasante; gancho en J con casquillo para la varilla del aro, pestillo y perilla; carro de
cápsula que desliza sobre el riel con bisagra dentada (0° a 90°).

## Piezas y slicer (OrcaSlicer, P1P, PETG, 0.20 mm, una pieza por placa)

Estimado: se cortó con la orientación del modelo (piezas.py da la orientación en texto) y relleno por regla (cajas,
tapas, gancho, carro y pestillo 100 %; rieles, bandeja, bisel, perilla y casquillo 40 %).

| Pieza | Cant. Ø200 | Relleno | g c/u | h c/u |
|---|---|---|---|---|
| M1 caja, cuerpo | 1 | 100 % | 255.1 | 5.54 |
| M2 caja, tapa con asa | 1 | 100 % | 159.6 | 4.12 |
| M11 bandeja | 1 | 40 % | 34.0 | 1.38 |
| M3 riel, tramo central | 1 | 40 % | 203.1 | 10.60 |
| M3 riel, extensión | 2 | 40 % | 48.7 | 2.52 |
| M3 riel, punta | 2 | 40 % | 26.8 | 1.46 |
| M3 tapa del bolsillo | 2 | 100 % | 11.4 | 0.36 |
| M4 cápsula, cuerpo | 2 | 100 % | 65.2 | 2.84 |
| M5 cápsula, tapa con bisagra | 2 | 100 % | 31.1 | 1.60 |
| M6 bisel | 2 | 40 % | 2.2 | 0.71 |
| M9 gancho | 2 | 100 % | 32.4 | 1.85 |
| M10 carro de la cápsula | 2 | 100 % | 85.3 | 3.74 |
| M12 perilla | 4 | 40 % | 5.2 | 0.39 |
| M13 casquillo Ø8 | 2 | 40 % | 1.7 | 0.40 |
| M14 pestillo | 2 | 100 % | 1.2 | 0.45 |
| M7 ventana | 2 | acrílico, no se imprime | | |

**Total impreso: 1285 g, 55.1 h, 116 soles** (PETG a 90 soles/kg). 28 piezas impresas, 15 tipos (16 con la ventana).

## Resultados (REPORTE_CAD y `cad_final/reporte_verificacion.md`)
- Peso en aire 2048 g, peso aparente **+225 g** con 2 pletinas por lado (relleno 40 %). Sin contar la varilla M8
  (unos 167 g de acero) ni las piezas chicas. BG 20.2 mm.
- FS, **cálculo a mano** (sin FEM): unión de tramos sin varilla 1.3 / 0.6 entre capas en Ø200, por eso la varilla M8
  es obligatoria. Insertos M4 del fondo: 251 N por inserto.
- Sellos: junta de la tapa de la caja, 2 tapas de cápsula y 2 ventanas (5 juntas) más los PG7 del fondo de la caja.

## Archivos
`step/` y `stl/` por pieza, `render_iso.png`, `render_lado.png`, `slicer.json`. El ensamble
`ensamble_modular_D200.step` (9 MB) está en Drive y en disco, no en el repo; se regenera con `cad_final/ensambles.py`.

## Pendiente
Nada: es referencia. Más piezas, más uniones y la varilla M8 obligatoria fueron las razones para pasar a la simple.
