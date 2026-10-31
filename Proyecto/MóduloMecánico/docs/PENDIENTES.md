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

## Skin decorativo "concha" — P2 terminado (31/10), P4 sin rehacer
- **P2 (`python skin.py P2_robusto`)**: 1 sólido, `brep_ok` true, pared p1 2.0 mm y mínima 1.8 mm (0 de 13 158 rayos bajo 1.6), dentro de la tapa con 0.5 mm, sin interferencias (asa, umbilical, cuerdas en (±75, ±75)), 12 agujeros Ø3.4. 146 × 145 × 5.5 mm, 29.1 cm³.
- Slicer (P1P, PETG gris, 100 %, sin soportes): **34.9 g, 1.11 h, S/ 2.09** a S/ 60/kg → `salida/skin/P2_robusto/concha/3mf/SKIN_concha_P2.3mf`.
- Lastre: +5.1 g aparentes (352.5 → 357.6 gf con 40 % de relleno), dentro de 200–500. **El lastre no cambia.** Para volver exactamente al centro (350) habría que sacar ~10 g de tuercas: opcional.
- Onshape: pestaña `SKIN_concha_v1` y `PLANO_SKIN_concha_v1` en LG_IMPRIMIR_P2 (6 cotas). **A mano:** alto general 5.5 mm en frontal y lateral (el tope de la costilla es inclinado y el script no lo acota).
- Montaje: los 12 tornillos M3 de la tapa deben ser **2 mm más largos** con el skin puesto (placa de 2 mm). Añadir al BOM.
- Con el asa centrada en P2, "LanternGuard" queda detrás del asa: en la vista de frente el asa tapa parte del texto. Se ve completo en ISO y desde atrás.
- Pendiente: P4 con la misma receta (labio sobre contorno real + texto poligonal), y el óvalo del logo de P4. Tema "manta" sin empezar. `assets/logo_upch.svg` no existe: "UPCH" va como texto.

## Planos Onshape de P2 + boya (LG_IMPRIMIR_P2, 30/10)
- Link sharing del documento: la API devuelve 403 (la llave no tiene permiso de compartir). A mano: Share > Link > ver + exportar.
- Cotas que hay que agregar a mano (la API solo acota entre aristas rectas; las que chocaban se omitieron):
  - M1s_caja_cuerpo: 4x Ø5.6 y Ø30 en la lateral.
  - M2_caja_tapa: alto en la frontal (el alto total 63 ya está en la lateral).
  - M3s_riel_gancho: alto 79.4 en la frontal; 4x Ø4.2 y Ø8 en la lateral.
  - M4_capsula_cuerpo: casi todo (Ø12.6 arriba; 3x Ø1.8, Ø16.4 y Ø30.4 en la lateral; espesor): es un cilindro y sus contornos son curvos.
  - M5s_capsula_tapa_pie: ancho 55.2 y alto 95.9 en la frontal, 2x Ø4.2.
  - M6_capsula_bisel: anillo, solo salieron 3 cotas; faltan Ø exterior 42 y espesor 2.5.
  - M11_bandeja: alto 30 en frontal y lateral.
  - B1_casco: 2x Ø83 (cunas) en la lateral; espesor de pared.
  - B2_cubierta: alto 136.4.
  - B3_caja: 4x Ø3.4 arriba.
  - B5_cuna: 4x Ø4 en frontal y superior, alto 114.6, Ø83.
  - Completas: M3t, M11_bandeja_sup, B4, B6.
- Revisar a ojo: en M1s y B1 algunos textos de diámetro quedan encima de una línea de cota vecina (el control de choques mira los textos, no las líneas).
