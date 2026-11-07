# Gancho de la Fase C

Generado por `cad_final/gancho.py`. STL y STEP en `../salida/preliminar/`; render `gancho_iso.png`. Todas las cotas salen de `params.py`.

| pieza | STL | BRep/BOP | estanco | cuerpos | bbox en orientacion (mm) | voladizo mm2 | espesor min p1 (mm) | masa 40 % (g) | masa 100 % (g) | que medir |
|---|---|---|---|---|---|---|---|---|---|---|
| M9_gancho | M9_gancho.stl | ok | si | 1 | 68.0 x 59.0 x 30.0 (X 90) | 1017 | 3.31 (min 1.78) | 18.2 | 24.8 | Cargar la J con el casquillo y la varilla real; tirar 75 N con dinamometro de equipaje y medir la flexion del alma; comprobar HOOK_DROP con el aro real; pasar la correa de 25 x 3. |
| M13_casquillo_D6 | M13_casquillo_D6.stl | ok | si | 1 | 16.6 x 20.0 x 13.5 (X -90) | 0 | 1.51 (min 1.51) | 2.2 | 2.5 | Fuerza de entrada y salida de la varilla D6 (dinamometro); apriete a presion en el asiento. |
| M13_casquillo_D8 | M13_casquillo_D8.stl | ok | si | 1 | 15.7 x 20.0 x 13.5 (X -90) | 0 | 1.51 (min 1.51) | 2.0 | 2.0 | Fuerza de entrada y salida de la varilla D8 (dinamometro); apriete a presion en el asiento. |
| M13_casquillo_D10 | M13_casquillo_D10.stl | ok | si | 1 | 14.5 x 20.0 x 13.5 (X -90) | 0 | 1.51 (min 1.51) | 1.5 | 1.5 | Fuerza de entrada y salida de la varilla D10 (dinamometro); apriete a presion en el asiento. |
| M13_casquillo_D12 | M13_casquillo_D12.stl | ok | si | 1 | 12.4 x 20.0 x 13.5 (X -90) | 0 | 1.51 (min 1.51) | 1.0 | 1.0 | Fuerza de entrada y salida de la varilla D12 (dinamometro); apriete a presion en el asiento. |
| M14_pestillo | M14_pestillo.stl | ok | si | 1 | 12.0 x 35.2 x 3.6 (X 90) | 0 | 1.50 (min 1.27) | 1.2 | 1.2 | Clic de cierre sobre la cresta (LATCH_BUMP) sin trabarse; probar con guante. |
| M12_perilla | M12_perilla.stl | ok | si | 1 | 30.0 x 30.0 x 12.0 (plano) | 45 | 6.99 (min 1.20) | 5.9 | 8.5 | Pausar la impresion en el bolsillo hexagonal, colocar el perno M4 y reanudar; torque con guante. |

## Chequeos

- Holgura de la perilla: cilindro libre de D34 (KNOB_D + 4.0) centrado en x = -30.0, desde la cara inferior de la brida (z = -6.0) hasta la cara superior de la mandibula (z = -23.8): interferencia con el gancho 0.0000 mm3 (assert < 0.001). Perilla montada (invertida, perno hacia arriba) contra el gancho: 0.0000 mm3.
- Pestillo cerrado contra la mandibula: 0.0000 mm3 (esperado 0). Contra el casquillo D10: 0.0000 mm3.
- Brida 50.0 x 30.0 x 6.0, agujero M4 de paso en x = -30.0, fuera del alma (alma en x de -12 a 0). Centro de varilla 40.0 mm bajo la cara superior de la brida.
- Carga 75.0 N en el asiento: orientacion de impresion con el perfil XZ sobre la cama (X 90), capas en planos XZ; la carga vertical sobre el asiento y el alma va a lo largo de las capas, no a traves. Los ejes del asiento, del pivote y de la correa quedan verticales (sin voladizo). El voladizo medido viene del escalon de ancho 30 (brida) a 12 (alma y mandibula): la cara -Y del alma queda en el aire y pide soporte.
- Casquillos: las puntas de la C se recortan con un plano en x para dejar un espesor radial de MIN_WALL + 0.3 (antes eran cuñas de 0.2 mm); la boca sigue siendo varilla + 0.4.
- Perilla: se monta invertida (el perno sale por la cara que mira a la brida); imprimir con esa cara sobre la cama.

## Avisos

- ninguno

## Chequeos que fallaron

- ninguno

## Params que faltan (constantes de modulo en gancho.py)

- `KNOB_FREE_EXTRA` = 4.0
- `KNOB_WEB_GAP` = 1.0
- `KNOB_FLANGE_GAP` = 0.5
- `BUSHING_TIP_MARGIN` = 0.3
- `WEB_OVERLAP` = 0.5
