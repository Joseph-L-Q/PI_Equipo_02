# Ficha P1_minimo

Generada por `cad_final/prototipos.py` desde `resultados.json`, `slicer.json` y `fem/fem.json` de esta carpeta. No editar a mano.

## Que es

Nodo del aro de prueba Ø200 (version simple V2 como base) con estas diferencias: riel **celosia**, pared del conducto **3.5 mm**, gancho **snap**, caja y rieles separados, sin acabado estetico, caja **minima**, capsula **minima**. Caja exterior 119 x 128 x 77 mm. Ventanas de celosia: {'half': 6}. Redondeos aplicados (radio mm, 0 = fallo): ninguno.

## Piezas impresas

| Pieza | Cant. | g c/u (slicer) | h c/u | Orientacion | Soportes | Relleno |
|---|---|---|---|---|---|---|
| M1 caja baja con bolsillos | 1 | 484.1 | 16.15 | X180 | si | 1.0 |
| M2 caja, tapa con asa | 1 | 175.3 | 4.93 | Y+90 | si | 1.0 |
| M3t tapa del bolsillo | 2 | 13.3 | 0.38 | X180 | no | 1.0 |
| M5s tapa con pie | 2 | 100.7 | 3.39 | sin girar | si | 1.0 |
| M4 capsula, cuerpo | 2 | 53.5 | 1.88 | Y-90 | si | 1.0 |
| M6 bisel | 2 | 2.0 | 0.20 | Y+90 | no | 0.4 |
| M7 ventana (acrilico) | 2 | comprada | - | - | - | acrilico |
| M11 bandeja (M11_bandeja) | 1 | 35.4 | 1.64 | sin girar | no | 0.4 |
| M11 bandeja (M11_bandeja_sup) | 1 | 31.2 | 1.05 | sin girar | no | 0.4 |
| M3s riel con gancho, mitad | 2 | 118.5 | 4.87 | X+90 | si | riel 40 %, gancho 100 % |

Piezas impresas por nodo: **14** de 9 tipos, mas 2 ventanas de acrilico.

Masa impresa del nodo (slicer, sin pletinas ni tornilleria): **1302 g**; tiempo **45.2 h**; filamento **S/ 117.17** (a S/ 90 el kg, estimado).

## Sellos y juntas

- Sellos estancos: **9** (tapa_caja 1, tapa_capsula 2, ventana 2, pg7_caja 2, pg7_capsula 2).
- Juntas atornilladas no estancas (conducto inundado): **4** (riel_caja 2, union_extremo 0, pie_m4 2, abrazadera_m4 0); ademas de las tapas del bolsillo del lastre (2 M3t) y los tornillos de las tapas.

## Peso

- En aire: **2415 g** (bandeja al 40 %), con 5 pletinas por bolsillo.
- Aparente en agua de mar: **+277 g** (40 %) / +285 g (100 %); ventana exigida 200 a 500 g.

## Factores de seguridad (150 N de manipulacion en una capsula)

FEM local (Gmsh + CalculiX, PETG isotropico estimado, esfuerzo = percentil 99.5 de von Mises; FS a lo largo de las capas / entre capas):

| Caso | Desplazamiento mm | Esfuerzo MPa | FS | FS entre capas |
|---|---|---|---|---|
| riel_agua | 2.88 | 11.5 | 3.9 | 1.9 |
| riel_izado | 0.68 | 8.8 | 5.1 | 2.5 |
| pie | 0.45 | 8.4 | 5.4 | 2.6 |

Calculo a mano (simple.py, conservador, no es FEM): riel 14.7 / 7.2, pie 3.9 / 1.9, gancho 5.8 / 2.9 (a lo largo / entre capas).

## Archivos

- `ensamble_simple_D200.step` (nodo + linterna de prueba), `stl/` y `step/` por pieza, `ensamble_simple_iso.png` y `ensamble_simple_lado.png` (vista frontal), `nodo_simple_iso.png`, `nodo_simple_corte.png`, `REPORTE.md` (chequeos), `slicer.json`, `fem/fem.json` y sus PNG.

## Pendiente

- Todo lo estimado de `params.py` sigue por verificar (diametro real de la varilla del aro, cargas, PETG real); ver `docs/PROTOTIPOS.md`.
- Ninguna cifra de este prototipo esta probada en agua: el FEM es de un material isotropico estimado y no dice nada de estanqueidad.
- Gancho snap-fit: la fuerza de insercion y la fatiga del brazo no estan calculadas; imprimir una probeta del gancho sobre la varilla real antes del nodo.
