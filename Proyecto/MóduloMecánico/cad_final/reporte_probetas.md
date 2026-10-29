# Probetas de la Fase B

Generado por `cad_final/probetas.py`. STL en `../salida/probetas/`; render `probetas_iso.png`. Todas las cotas salen de `params.py`.

| pieza | STL | BRep/BOP | estanco | volumen cm3 | bbox en orientacion (mm) | voladizo mm2 | que medir/probar |
|---|---|---|---|---|---|---|---|
| PB1_garra | PB1_garra.stl | ok | si | 10.49 | 33.0 x 55.2 x 12.0 (X 90) | 185 | Orientacion: eje del asiento vertical (X 90). Medir con dinamometro de equipaje la fuerza de entrada y salida de cada varilla real por casquillo; probar la correa en la ranura 25 x 3; comprobar que el casquillo entra a presion en el asiento de 16. |
| M13_casquillo_D6 | M13_casquillo_D6.stl | ok | si | 2.01 | 19.5 x 20.0 x 13.5 (X -90) | 0 | Fuerza de entrada/salida de la varilla D6 (dinamometro); apriete del ajuste a presion en el asiento. |
| M13_casquillo_D8 | M13_casquillo_D8.stl | ok | si | 1.66 | 19.1 x 20.0 x 13.5 (X -90) | 0 | Fuerza de entrada/salida de la varilla D8 (dinamometro); apriete del ajuste a presion en el asiento. |
| M13_casquillo_D10 | M13_casquillo_D10.stl | ok | si | 1.27 | 18.5 x 20.0 x 13.5 (X -90) | 0 | Fuerza de entrada/salida de la varilla D10 (dinamometro); apriete del ajuste a presion en el asiento. |
| M13_casquillo_D12 | M13_casquillo_D12.stl | ok | si | 0.87 | 17.8 x 20.0 x 13.5 (X -90) | 0 | Fuerza de entrada/salida de la varilla D12 (dinamometro); apriete del ajuste a presion en el asiento. |
| PB2_ranura_T | PB2_ranura_T.stl | ok | si | 16.48 | 40.0 x 30.0 x 30.0 (X 90) | 1328 | Que la tuerca M4 AF7 entre por la punta y deslice sin holgura excesiva; que el perno pase por la abertura de 4.6; fuerza de extraccion. Calibra RAIL_TSLOT (abertura, ancho, alto). |
| PB3_macho | PB3_macho.stl | ok | si | 15.26 | 40.0 x 30.0 x 30.0 (X 90) | 1226 | Imprimir macho y hembra, deslizar la llave de costado (eje Y); holgura de la cola de milano; ajuste de los 2 M4 y de la tuerca en la bolsa; ranura T continua en el macho. |
| PB3_hembra | PB3_hembra.stl | ok | si | 13.98 | 40.0 x 30.0 x 30.0 (X 90) | 1044 | Par del macho; revisar el avellanado de la cabeza M4 y la piel de la bolsa de tuerca. |
| M14_pestillo | M14_pestillo.stl | ok | si | 0.91 | 12.0 x 35.2 x 3.6 (X 90) | 0 | Montar sobre PB1 con un M3: el resalte de 0.6 debe dar un clic sin trabarse ni soltarse solo; calibra LATCH_BUMP; probar con guante. |
| M12_perilla | M12_perilla.stl | ok | si | 6.71 | 30.0 x 30.0 x 12.0 (plano) | 45 | PAUSAR la impresion al llegar a la altura del bolsillo hexagonal, colocar la cabeza del perno M4, reanudar para cerrar la tapa de 1.2. Verificar torque con guante y que no gire la cabeza. |
| PB6_base | PB6_base.stl | ok | si | 31.07 | 60.0 x 60.0 x 20.0 (plano) | 0 | Insertos termicos M3 en las 4 esquinas; prueba de estanqueidad con la tapa y el o-ring de 2 mm a 1 m. |
| PB6_tapa | PB6_tapa.stl | ok | si | 17.04 | 60.0 x 60.0 x 5.0 (plano) | 511 | Ranura 2.6 x 1.5: comprobar compresion del o-ring (25 %) y que el cordon no se salga; sumergir. |
| PB7_peine | PB7_peine.stl | ok | si | 10.52 | 76.0 x 26.0 x 6.0 (plano) | 0 | Probar que pin entra en cada agujero: la holgura que ajusta sin juego fija FIT_CLEAR y HOLE_COMP (sin texto: de izquierda a derecha 0.2, 0.3, 0.4, 0.5). |
| PB7_pines | PB7_pines.stl | ok | si | 1.76 | 62.0 x 8.0 x 8.0 (plano) | 0 | Cortar los pines del sprue; se prueban en los 4 agujeros del peine. |

## Como alimentan los parametros

- Peine de holguras (PB7): el resultado fija `FIT_CLEAR` y `HOLE_COMP`.
- Ranura T con tuerca (PB2): fija `RAIL_TSLOT` (abertura, ancho, alto) y `RAIL_TSLOT_RIB`.
- Pestillo (PB4) sobre la garra (PB1): fija el resalte `LATCH_BUMP` de 0.6.
- Garra y casquillos (PB1, M13): el usuario mide con dinamometro de equipaje la fuerza de entrada y salida por casquillo (varillas reales de 6, 8, 10 y 12).

## Decisiones de diseno

- PB1: la garra mide 12 en Y (contacto). La ranura de correa 25 x 3 atraviesa en Y la parte baja, bajo el asiento. El pestillo gira en un M3 en el labio superior y se aloja en una ranura central de 4.2; la cresta de enganche (0.6) esta en el labio inferior. El pie lleva un vastago con M4 para atornillarla a PB2.
- Casquillo: pestana en +Y, abertura igual al diametro interior orientada a +X (boca de la J).
- PB2: la ranura T no lleva techo sobre el canal de la tuerca; la tuerca entra por la punta.
- PB3: los dos M4 atraviesan la llave de cola de milano (la llave queda con 1.9 mm por lado alrededor del agujero a la altura de la base).
- PB5: bolsillo hexagonal cerrado por una tapa de 1.2: pausar la impresion, colocar el perno y seguir.
- PB6: el hueco de la base tiene esquinas interiores grandes para que el sello siga la ruta de la ranura y los insertos queden en las esquinas macizas.
- PB7: los 4 pines van unidos por un sprue fino en un solo STL (se cortan antes de probar).
- Orientacion de impresion: carril acostado sobre una cara lateral (X 90); garra y pestillo con el eje de pivote vertical (X 90); casquillos con la pestana sobre la cama (X -90); el resto plano.

## Avisos

- PB7: el texto grabado rompio las booleanas; se omite el texto

## Chequeos que fallaron

- ninguno

## Params que faltan (constantes de modulo en probetas.py)

- `COUPON_L` = 40.0
- `JAW_WALL` = 4.0
- `JAW_LIP_H` = 10.0
- `STRAP_SLOT_T` = 3.0
- `STEM_H` = 20.0
- `LATCH_T` = 3.6
- `LATCH_ARM_W` = 5.0
- `LATCH_RIDGE_W` = 1.2
- `LATCH_TIP_GAP` = 0.2
- `LATCH_SWING` = 4.5
- `KNOB_LOBE_R` = 3.5
- `KNOB_CAP` = 1.2
- `SEAL_CAV_CORNER` = 14.0
- `SEAL_FILLET` = 2.0
- `COMB_PITCH` = 18.0
- `COMB_T` = 6.0
- `COMB_W` = 26.0
- `COMB_TEXT_H` = 4.5
- `COMB_TEXT_DEPTH` = 0.6
- `PIN_L` = 8.0
