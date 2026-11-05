# Ficha P2_robusto

Generada por `cad_final/prototipos.py` desde `resultados.json`, `slicer.json` y `fem/fem.json` de esta carpeta. No editar a mano.

## Que es

Nodo del aro de prueba Ø200 (version simple V2 como base) con estas diferencias: riel **celosia**, pared del conducto **5 mm**, gancho **c**, caja y rieles separados, sin acabado estetico, caja **v2**, capsula **v2**. Caja exterior 129 x 128 x 78 mm. Ventanas de celosia: ninguna. Redondeos aplicados (radio mm, 0 = fallo): ninguno.

## Piezas impresas

| Pieza | Cant. | g c/u (slicer) | h c/u | Orientacion | Soportes | Relleno |
|---|---|---|---|---|---|---|
| M1 caja baja con bolsillos | 1 | 436.8 | 9.27 | sin girar | si | 1.0 |
| M2 caja, tapa con asa | 1 | 194.4 | 4.81 | sin girar | si | 1.0 |
| M3t tapa del bolsillo | 2 | 42.3 | 0.87 | X180 | no | 1.0 |
| M5s tapa con pie | 2 | 97.3 | 2.80 | X180 | si | 1.0 |
| M3f marco del bolsillo de lastre | 2 | 51.8 | 1.95 | X180 | no | 0.4 |
| M4 capsula, cuerpo | 2 | 77.3 | 2.04 | Y+90 | si | 1.0 |
| M6 bisel | 2 | 2.0 | 0.20 | Y+90 | no | 0.4 |
| M7 ventana (acrilico) | 2 | comprada | - | - | - | acrilico |
| M11 bandeja (M11_bandeja) | 1 | 42.1 | 1.79 | sin girar | no | 0.4 |
| M11 bandeja (M11_bandeja_sup) | 1 | 35.0 | 1.15 | sin girar | no | 0.4 |
| M3s riel con gancho, mitad | 2 | 217.1 | 6.14 | X+90 | si | riel 40 %, gancho 100 % |

Piezas impresas por nodo: **16** de 10 tipos, mas 2 ventanas de acrilico.

Masa impresa del nodo (slicer, sin lastre ni tornilleria): **1684 g**; tiempo **45.0 h**; filamento **S/ 151.55** (a S/ 90 el kg, estimado).

## Sellos y juntas

- Sellos estancos: **9** (tapa_caja 1, tapa_capsula 2, ventana 2, junta_riel_caja 2, junta_riel_capsula 2).
- Juntas atornilladas no estancas (conducto inundado): **4** (riel_caja 2, union_extremo 0, pie_m4 2, abrazadera_m4 0); ademas de las tapas del bolsillo del lastre (2 M3t) y los tornillos de las tapas.

## Peso

- En aire: **2988 g** (bandeja al 40 %), con el lastre.
- **Lastre a granel** (tuercas y arandelas M8 de inox, a granel, densidad aparente 4.5 g/cm3, estimada): **980 g** en total (490 g por bolsillo, un bolsillo por lado, 100 x 50 x 30 mm). Llena 21.8 de 30 mm. Rango de lastre que deja el peso aparente en la ventana: 870 a 1204 g. Con perdigon de plomo: 997 g.
- Aparente en agua de mar: **+296 g** (40 %) / +305 g (100 %); ventana exigida 200 a 500 g.

## Factores de seguridad (150 N de manipulacion en una capsula)

FEM local (Gmsh + CalculiX, PETG isotropico estimado, esfuerzo = percentil 99.5 de von Mises; FS a lo largo de las capas / entre capas):

| Caso | Desplazamiento mm | Esfuerzo MPa | FS | FS entre capas |
|---|---|---|---|---|
| riel_agua | 1.81 | 6.5 | 6.9 | 3.4 |
| riel_izado | 0.18 | 3.8 | 11.9 | 5.8 |
| pie | 0.17 | 5.8 | 7.8 | 3.8 |

Calculo a mano (simple.py, conservador, no es FEM): riel 24.6 / 12.0, pie 23.2 / 11.3, gancho 5.8 / 2.9 (a lo largo / entre capas).

## Archivos

- `ensamble_simple_D200.step` (nodo + linterna de prueba, ensamble con nombres: piezas impresas por codigo, el resto `REF_*`, lastre `lastre_izq`/`lastre_der`) y `ensamble_solidos.json` (lista de cuerpos y conteo de solidos), `stl/` y `step/` por pieza, `ensamble_simple_iso.png` y `ensamble_simple_lado.png` (vista frontal), `nodo_simple_iso.png`, `nodo_simple_corte.png`, `REPORTE.md` (chequeos), `slicer.json`, `fem/fem.json` y sus PNG.

## Cambios del 30/10 noche (tanda 3)

- **Sin separador ni apice.** La linterna de prueba es el aro, la malla de referencia, 4 cuerdas que suben rectas del aro (a 45 grados del riel, los brazos quedan entre cuerdas) y van a un solo nudo, y un cabo del nudo a la linea larga.
- **Aire cuerda-brazo 48.0 mm y cuerda-capsula 70.4 mm** (se exigen 10; el build falla si no). Cuerda-caja (brida de la tapa): 1.5 mm, informativo.
- **Lastre a granel** en vez de pletinas: 980 g, un bolsillo por lado cerrado por M3t; peso aparente +296 g (40 %) / +305 g (100 %); caja 129 x 128 x 78 mm (V2: 127 x 126 x 77).
- **Ensamble con nombres** (`REF_*` para lo no impreso, `lastre_izq`/`lastre_der`) y `ensamble_solidos.json` con el conteo de solidos.

## Pendiente

- Todo lo estimado de `params.py` sigue por verificar (diametro real de la varilla del aro, cargas, PETG real); ver `docs/PROTOTIPOS.md`.
- Ninguna cifra de este prototipo esta probada en agua: el FEM es de un material isotropico estimado y no dice nada de estanqueidad.
