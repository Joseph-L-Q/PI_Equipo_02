# Piezas del riel

Generado por `cad_final/riel.py`. STL en `../salida/preliminar/stl/`, STEP en `step/`, render `riel_iso.png`. Todas las cotas salen de `params.py`; la union y la ranura T reproducen las probetas PB2/PB3.

Armado (decision del 29/10, C18): tramo central + 0 / 1 / 2 extensiones de paso 100 (pieza de 115) + una punta de 60 por lado: riel de 230 / 430 / 630 mm.

| pieza | STL | BRep/BOP | estanco | cuerpos | bbox en orientacion (mm) | voladizo mm2 | espesor minimo p1 (mm) | masa al 100 % (g) | volumen cm3 |
|---|---|---|---|---|---|---|---|---|---|
| M3_riel_central | M3_riel_central.stl | ok | si | 1 | 140.0 x 88.0 x 57.3 (X 180) | 8958 | 1.37 (min absoluto 1.30) | 183.5 | 144.48 |
| M3_riel_ext | M3_riel_ext.stl | ok | si | 1 | 115.0 x 30.0 x 30.0 (X 90) | 3432 | 1.40 (min absoluto 1.30) | 55.4 | 43.66 |
| M3_riel_punta | M3_riel_punta.stl | ok | si | 1 | 60.0 x 30.0 x 30.0 (X 90) | 1730 | 2.00 (min absoluto 1.40) | 29.0 | 22.86 |

## Interferencias de ensamble

- central+ext(+X): 0.000 mm3
- central+ext(-X): 0.000 mm3
- ext+ext: 0.000 mm3
- central+punta (0 ext.): 0.000 mm3
- ext+punta: 0.000 mm3
- Bolsillos de lastre: llegan hasta |x| = 53.5, la zona de union empieza en |x| = 55.0; volumen del central dentro de la media madera inferior de la union: 0.000 mm3. El macho entra de costado (eje Y) sin tocar los bolsillos.
- Deslizamiento lateral del macho, barrido cada 10 mm fuera del riel: interferencia maxima 0.000 mm3.

## Orientacion de impresion

- M3_riel_central: brida abajo (X 180). La ventana de acceso sobre la union evita puentes largos; el voladizo de la tabla es el de los techos de la camara y de los bolsillos de lastre, con soportes locales. El central es la pieza que mas soporte necesita.
- M3_riel_ext: acostada sobre una cara lateral (X 90), como las probetas PB2/PB3. La llave de cola de milano y la ranura T quedan de perfil; la ranura de salida del cable (+Y) queda en la cara lateral.

## Orden de montaje

1. Cargar las tuercas M4 en la ranura T por las puntas ANTES de unir una extension: en el central la ranura queda abierta en las caras |x| = 55 (frente a la media madera vacia); en la extension queda abierta por la punta macho.
2. Deslizar el macho de la extension de costado (eje Y) en la media madera inferior de la hembra hasta que la llave entre en el nido de cola de milano.
3. Los 2 M4 verticales de la union (y = +-10) van por las paredes engrosadas: cabeza en el avellanado de la hembra (por la ventana de acceso en el central) y tuerca en la bolsa hexagonal del macho.
4. Un cable Cat5e por lado, en el conducto local de 10 mm. Sale por la ranura lateral (+Y) de la punta, junto al carro.

## Chequeos que fallaron

- ninguno

## Params que faltan (constantes de modulo en riel.py)

- `EXIT_SLOT_ZC` = 10.35: altura del centro de la ranura de salida sobre el fondo del riel (cable sobre las costillas).
- `XFER_STEP` = 10.0: paso del barrido de deslizamiento lateral (solo verificacion).
