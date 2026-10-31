# Ficha P2_robusto

Generada por `cad_final/prototipos.py` desde `resultados.json`, `slicer.json` y `fem/fem.json` de esta carpeta. No editar a mano.

## Que es

Nodo del aro de prueba Ø200 (version simple V2 como base) con estas diferencias: riel **celosia**, pared del conducto **5 mm**, gancho **c**, caja y rieles separados, sin acabado estetico, caja **v2**, capsula **v2**. Caja exterior 127 x 126 x 77 mm. Ventanas de celosia: {'half': 6}. Redondeos aplicados (radio mm, 0 = fallo): ninguno.

## Piezas impresas

| Pieza | Cant. | g c/u (slicer) | h c/u | Orientacion | Soportes | Relleno |
|---|---|---|---|---|---|---|
| M1 caja baja con bolsillos | 1 | 509.2 | 16.13 | sin girar | si | 1.0 |
| M2 caja, tapa con asa | 1 | 181.2 | 5.11 | Y+90 | si | 1.0 |
| M3t tapa del bolsillo | 2 | 23.7 | 0.55 | X180 | no | 1.0 |
| M5s tapa con pie | 2 | 96.2 | 3.19 | sin girar | si | 1.0 |
| M4 capsula, cuerpo | 2 | 59.6 | 2.05 | Y-90 | si | 1.0 |
| M6 bisel | 2 | 2.0 | 0.20 | Y+90 | no | 0.4 |
| M7 ventana (acrilico) | 2 | comprada | - | - | - | acrilico |
| M11 bandeja (M11_bandeja) | 1 | 38.3 | 1.73 | sin girar | no | 0.4 |
| M11 bandeja (M11_bandeja_sup) | 1 | 34.1 | 1.13 | sin girar | no | 0.4 |
| M3s riel con gancho, mitad | 2 | 137.1 | 5.31 | X+90 | si | riel 40 %, gancho 100 % |

Piezas impresas por nodo: **14** de 9 tipos, mas 2 ventanas de acrilico.

Masa impresa del nodo (slicer, sin lastre ni tornilleria): **1400 g**; tiempo **46.7 h**; filamento **S/ 126.02** (a S/ 90 el kg, estimado).

## Sellos y juntas

- Sellos estancos: **9** (tapa_caja 1, tapa_capsula 2, ventana 2, pg7_caja 2, pg7_capsula 2).
- Juntas atornilladas no estancas (conducto inundado): **4** (riel_caja 2, union_extremo 0, pie_m4 2, abrazadera_m4 0); ademas de las tapas del bolsillo del lastre (2 M3t) y los tornillos de las tapas.

## Peso

- En aire: **2694 g** (bandeja al 40 %), con el lastre.
- **Lastre a granel** (tuercas y arandelas M8 de inox, a granel, densidad aparente 4.5 g/cm3, estimada): **1150 g** en total (575 g por bolsillo, un bolsillo por lado, 100 x 50 x 30 mm). Llena 25.6 de 30 mm. Rango de lastre que deja el peso aparente en la ventana: 975 a 1309 g. Con perdigon de plomo: 1098 g.
- Aparente en agua de mar: **+352 g** (40 %) / +361 g (100 %); ventana exigida 200 a 500 g.

## Factores de seguridad (150 N de manipulacion en una capsula)

FEM local (Gmsh + CalculiX, PETG isotropico estimado, esfuerzo = percentil 99.5 de von Mises; FS a lo largo de las capas / entre capas):

| Caso | Desplazamiento mm | Esfuerzo MPa | FS | FS entre capas |
|---|---|---|---|---|
| riel_agua | 2.63 | 8.1 | 5.6 | 2.7 |
| riel_izado | 0.36 | 5.3 | 8.5 | 4.1 |
| pie | 0.48 | 8.9 | 5.0 | 2.5 |

Calculo a mano (simple.py, conservador, no es FEM): riel 18.2 / 8.9, pie 5.6 / 2.7, gancho 5.8 / 2.9 (a lo largo / entre capas).

## Archivos

- `ensamble_simple_D200.step` (nodo + linterna de prueba, ensamble con nombres: piezas impresas por codigo, el resto `REF_*`, lastre `lastre_izq`/`lastre_der`) y `ensamble_solidos.json` (lista de cuerpos y conteo de solidos), `stl/` y `step/` por pieza, `ensamble_simple_iso.png` y `ensamble_simple_lado.png` (vista frontal), `nodo_simple_iso.png`, `nodo_simple_corte.png`, `REPORTE.md` (chequeos), `slicer.json`, `fem/fem.json` y sus PNG.

## Cambios del 30/10 noche (tanda 3)

- **Sin separador ni apice.** La linterna de prueba es el aro, la malla de referencia, 4 cuerdas que suben rectas del aro (a 45 grados del riel, los brazos quedan entre cuerdas) y van a un solo nudo, y un cabo del nudo a la linea larga.
- **Aire cuerda-brazo 48.0 mm y cuerda-capsula 68.3 mm** (se exigen 10; el build falla si no). Cuerda-caja (brida de la tapa): 2.9 mm, informativo.
- **Lastre a granel** en vez de pletinas: 1150 g, un bolsillo por lado cerrado por M3t; peso aparente +352 g (40 %) / +361 g (100 %); caja 127 x 126 x 77 mm (V2: 127 x 126 x 77).
- **Ensamble con nombres** (`REF_*` para lo no impreso, `lastre_izq`/`lastre_der`) y `ensamble_solidos.json` con el conteo de solidos.

## Pendiente

- Todo lo estimado de `params.py` sigue por verificar (diametro real de la varilla del aro, cargas, PETG real); ver `docs/PROTOTIPOS.md`.
- Ninguna cifra de este prototipo esta probada en agua: el FEM es de un material isotropico estimado y no dice nada de estanqueidad.
