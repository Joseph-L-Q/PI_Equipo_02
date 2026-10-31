# Ficha P3_monocasco

Generada por `cad_final/prototipos.py` desde `resultados.json`, `slicer.json` y `fem/fem.json` de esta carpeta. No editar a mano.

## Que es

Nodo del aro de prueba Ø200 (version simple V2 como base) con estas diferencias: riel **celosia**, pared del conducto **4 mm**, gancho **abrazadera**, caja y riel en una sola pieza (monocasco), sin acabado estetico, caja **v2**, capsula **v2**. Caja exterior 127 x 126 x 77 mm. Ventanas de celosia: {'stub': 2, 'end': 1}. Redondeos aplicados (radio mm, 0 = fallo): ninguno.

## Piezas impresas

| Pieza | Cant. | g c/u (slicer) | h c/u | Orientacion | Soportes | Relleno |
|---|---|---|---|---|---|---|
| M1m caja con tramos de riel | 1 | 661.5 | 23.05 | X180 | si | 1.0 |
| M2 caja, tapa con asa | 1 | 181.2 | 5.11 | Y+90 | si | 1.0 |
| M3t tapa del bolsillo | 2 | 13.3 | 0.38 | X180 | no | 1.0 |
| M5m extremo de riel con pie y tapa | 2 | 131.5 | 4.36 | X180 | si | 1.0 |
| M4 capsula, cuerpo | 2 | 59.6 | 2.05 | Y-90 | si | 1.0 |
| M6 bisel | 2 | 2.0 | 0.20 | Y+90 | no | 0.4 |
| M7 ventana (acrilico) | 2 | comprada | - | - | - | acrilico |
| M11 bandeja (M11_bandeja) | 1 | 38.3 | 1.73 | sin girar | no | 0.4 |
| M11 bandeja (M11_bandeja_sup) | 1 | 34.1 | 1.13 | sin girar | no | 0.4 |
| M9c abrazadera (media luna del gancho) | 2 | 3.3 | 0.34 | X+90 | no | 1.0 |

Piezas impresas por nodo: **14** de 9 tipos, mas 2 ventanas de acrilico.

Masa impresa del nodo (slicer, sin pletinas ni tornilleria): **1335 g**; tiempo **45.7 h**; filamento **S/ 120.12** (a S/ 90 el kg, estimado).

## Sellos y juntas

- Sellos estancos: **9** (tapa_caja 1, tapa_capsula 2, ventana 2, pg7_caja 2, pg7_capsula 2).
- Juntas atornilladas no estancas (conducto inundado): **4** (riel_caja 0, union_extremo 2, pie_m4 0, abrazadera_m4 2); ademas de las tapas del bolsillo del lastre (2 M3t) y los tornillos de las tapas.

## Peso

- En aire: **2475 g** (bandeja al 40 %), con 5 pletinas por bolsillo.
- Aparente en agua de mar: **+238 g** (40 %) / +247 g (100 %); ventana exigida 200 a 500 g.

## Factores de seguridad (150 N de manipulacion en una capsula)

FEM local (Gmsh + CalculiX, PETG isotropico estimado, esfuerzo = percentil 99.5 de von Mises; FS a lo largo de las capas / entre capas):

| Caso | Desplazamiento mm | Esfuerzo MPa | FS | FS entre capas |
|---|---|---|---|---|
| riel_agua | 1.91 | 9.5 | 4.8 | 2.3 |
| riel_izado | 0.60 | 7.2 | 6.2 | 3.0 |
| pie | 0.40 | 8.2 | 5.5 | 2.7 |

Calculo a mano (simple.py, conservador, no es FEM): riel 15.7 / 7.7, pie 4.5 / 2.2, gancho 5.8 / 2.9 (a lo largo / entre capas). En P3/P4 el pie va fundido a la tapa: el calculo a mano del pie (aplastamiento de los M4) no aplica; vale el FEM.

## Archivos

- `ensamble_simple_D200.step` (nodo + linterna de prueba), `stl/` y `step/` por pieza, `ensamble_simple_iso.png` y `ensamble_simple_lado.png` (vista frontal), `nodo_simple_iso.png`, `nodo_simple_corte.png`, `REPORTE.md` (chequeos), `slicer.json`, `fem/fem.json` y sus PNG.

## Pendiente

- Todo lo estimado de `params.py` sigue por verificar (diametro real de la varilla del aro, cargas, PETG real); ver `docs/PROTOTIPOS.md`.
- Ninguna cifra de este prototipo esta probada en agua: el FEM es de un material isotropico estimado y no dice nada de estanqueidad.
- Abrazadera: la red de la linterna de prueba pasa por la media luna M9c; no se verifico contra la red real.
