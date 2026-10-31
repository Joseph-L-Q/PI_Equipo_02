# Pendientes y bloqueos (sesión del 30/10/2026)

Cada línea: qué falta, por qué y qué hace falta para destrabarlo.

## Medidas físicas (no se pueden resolver desde la PC)
- `aro.seccion`: hoy 8 mm estimado. Calibrador sobre la varilla del aro Ø200 real (MEDIDAS.md, fila 1).
- KIT A real, PG7, peso del panel: sin medir (MEDIDAS.md).

## Decisiones abiertas del equipo
- Ángulo de la cápsula: 30° (actual, M5s) o 70° (REPORTE_CAD §10.3).
- Límite de peso: 3 kg no cierra con la boya; propuesta: nodo ≤ 3 kg y boya aparte.

## Herramientas
- rclone usa el `client_id` compartido de rclone, que Google retira durante 2026. Crear uno propio en Google Cloud Console.

## Sesión de la noche (30/10, cierre)
- `cad_final/variantes.py` quedó roto: llama a las firmas viejas de `plates`, `assemble` y `lantern` de `simple.py`. No se usa en el flujo de hoy; arreglarlo antes de volver a correrlo.
- Onshape: `M1m_caja_riel` (P3, P4) y el umbilical del sistema solo entran con `allowFaultyParts` (pestaña `ENSAMBLE_v2_completo`), marcados como "faulty". En el CAD son sólidos válidos. Para imprimir se usan los STL/3MF.
- Onshape, a mano (la API no lo permite): mover los 2 documentos viejos a `LanternGuard/_historico` y arrastrar la pestaña de ensamble al primer lugar en cada `LG_*`.
- Estimados que hay que medir: densidad a granel del lastre (tuercas M8 4.5 g/cm³, perdigón 6.5) y llenado de la espuma PU (50 %), del que depende que la boya aguante perder una botella.
- Decisión del equipo: cuerda a 2.9 mm de la brida de la tapa en P2 (6.8 en P4); opciones (a), (b) y (c) en `docs/PROTOTIPOS.md`.
