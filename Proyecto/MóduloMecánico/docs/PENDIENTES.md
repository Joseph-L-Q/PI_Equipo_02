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

## Skin decorativo "concha" (30/10, detenido por prioridad de planos)
- Código en la rama `cad/skin-wip` (`cad_final/skin.py` y el bloque `skin.*` de `params.py`); no está en `cad/version-final`.
- Dónde quedó (P4): un solo sólido de ~24 cm³ (~31 g en PETG, muy bajo el tope de 200 g), dentro del contorno de la tapa con 0.5 mm de margen, sin interferencias con la tapa, el asa ni el umbilical, 10 agujeros M3 en los tornillos de la tapa.
- Falla 1, pared: el percentil 1 del espesor da 0.22 mm. La causa es la costilla exterior (344° y 196°), que pasa casi tangente al óvalo que deja ver el logo de P4 y queda una astilla. Arreglo a medio hacer: 9 costillas en lugar de 11 y agrandar el óvalo hasta que ninguna costilla lo roce (función `graze`, no aplicada).
- Falla 2, `brep_ok` false: `CurveOnSurfaceMode` del analizador booleano. El texto de la fuente de CadQuery ya trae autointersecciones (`SelfInterMode` true en "LanternGuard" solo). Los trazos más finos de "LanternGuard" a 16 mm miden ~1.3 mm, bajo la pared mínima de 1.6.
- Falta: P2, cálculo del lastre con el skin, 3MF con pausa `M400 U1` en z 2.0, render, pestaña `SKIN_concha_v1` en LG_P4_estetico, STL a Drive. El tema "manta" no se empezó.

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
