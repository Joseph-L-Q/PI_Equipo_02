# Pendientes y bloqueos (sesión del 30/10/2026)

Cada línea: qué falta, por qué y qué hace falta para destrabarlo.

## Encargo del 05/11/2026 (diseño para mar)
- **Resuelto:** golpe lateral sobre el panel (FS 3,42 entre capas), GM con una botella perdida (88 mm con espuma) y holgura cuerda-caja (3,2 mm). Las líneas de abajo sobre esos temas quedan como historia.
- **Riesgo abierto:** con la espuma al 50 % y una botella de cuna perdida, la boya vuelca. Control: pesar la lata (≥ 55 g de espuma). La escora con una botella perdida es de 11° (criterio propio 10°).
- **Onshape sin API:**
  - importar a mano los 5 STEP y `00_ENSAMBLE.step` de `salida/onshape_importar/2026-11-05/` (Drive `01_Onshape_importar/2026-11-05/`), siguiendo `IMPORTAR.md`;
  - después, borrar las pestañas «OLD 2026-11-04 …» y «OLD 2026-11-05 …».
- **Drive, borrar a mano** (ya están copiados en `OLD/`):
  - `02_Imprimir_primero_probetas/imprimir_hoy_2026-11-04_noche/`;
  - los PDF `PLANOS_A4_LanternGuard_v5.pdf` y anteriores de `04_Planos/`.

## Bloqueos del 04/11/2026
- **SimScale:**
  - El plan gratuito no deja descargar los resultados de las corridas nuevas de B2 (cubierta de 8 mm) ni de la variante lateral (error 403 «export-source-locked»). La verificación de esas corridas se hizo con CalculiX local.
  - Descarga por API (403 «export-source-locked») también en las corridas de B2 con 8 mm; la ruta de captura del visor web no es posible (la clave de la API no inicia sesión y no hay sesión abierta). Mientras tanto el bloque 3 sale con FEM local donde SimScale no exporta (`cad_final/resultados_bloque3.py`).
  - Los enlaces de los proyectos no se pudieron probar sin sesión: abrirlos una vez en una ventana privada.
  - En el proyecto B quedaron simulaciones repetidas, y la API no las puede borrar: se borran a mano.
- **Golpe de ola lateral sobre el panel solar** (200 N con el panel haciendo de vela): las 4 columnas Ø12 no lo resisten (FS 0,15 con la cubierta de 4 mm). Las barras de 8 mm no lo arreglan. Opciones: un panel más bajo, columnas más gruesas o tirantes. Hay que decidir si ese caso es un requisito real. **Medido de nuevo el 04/11 (FEM local, cubierta de 8 mm, `docs/resultados/`): sigue sin cumplir** (σ p99.5 52 MPa, FS 0,96 en el plano y 0,42 entre capas, 47 mm de flecha con los 200 N en una sola mitad; con 100 N por mitad, FS 1,9 y 0,85 entre capas).
- **Onshape:** suman otras 4 pestañas «OLD 2026-11-04 … (barras de 4 mm…)» de B2 para borrar a mano en LG_IMPRIMIR_P2.
- **Corrección de concepto 3a (riel cerrado): HECHA el 04/11 (bloque 1-FINAL).** Ver `docs/DECISIONES.md` (raíz del repo) y `docs/ESTANQUEIDAD.md`. Queda:
  - P3 y P4 (monocasco) siguen con el riel anterior. Si se imprime P4, hay que llevarle el riel cerrado y partir `M1m_caja_riel`, que mide 250 mm (> 230).
  - El cable plano real: medir su ancho y su espesor. El canal deja 22 mm de piso plano y 18 de alto, y el pase a la cápsula mide 8 × 22 mm.
  - Hacer la probeta de la junta plana (`probeta.junta`) con el cordón Ø2 NBR que se compre, y la prueba de estanqueidad de `ESTANQUEIDAD.md`.
- **Onshape:** la API key no puede borrar (403). En LG_IMPRIMIR_P2 hay que borrar a mano las 4 pestañas "OLD 2026-11-01 …",
  que ya están copiadas en LG_HISTORICO.
- **Onshape:** los planos de B1, B2 y B5 que Melissa hizo a mano ("Drawing 1/2/5") muestran las piezas enteras. Las piezas
  nuevas (mitades) se suben aparte; ella decide si rehace sus planos.
- **SimScale:** clave verificada el 04/11 (listar proyectos responde). El plan A va por API; no hace falta la guía manual.

## Medidas físicas (no se pueden resolver desde la PC)
- `aro.seccion`: 16,5 mm, decisión final del 05/11 (aro impreso LR2_aro, asiento Ø16,8). Diseñado para 2 kg por piso + 150 N; con 13 perímetros + 15 % de gyroid, FS pico entre capas 3,01 (150 g por aro). Margen real en el asiento 0,06 mm por lado: probar PB_aro antes de imprimir (`ARO_Y_ESTACION.md`).
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
  - M3s_riel_gancho: 4x Ø4.2 y Ø16.8 en la lateral.
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

## Planos A4 del 04/11/2026 (a mano en Onshape)
- **Borrar a mano** (la API no borra) en LG_IMPRIMIR_P2: las 4 "OLD 2026-11-01 …" y las nuevas "OLD 2026-11-04 …" de B1_casco, B2_cubierta, B3_caja, B5_cuna, B6_correa, M1s_caja_cuerpo, M3s_riel_gancho, M5s_capsula_tapa_pie, M11_bandeja, M11_bandeja_sup y M4_capsula_cuerpo (cada una: estudio y `.step`). El estudio ya está copiado en LG_HISTORICO. Ojo: los Drawing de Melissa 1, 2, 3, 5, 6, 7, 9, 11, 12, 14, 15 apuntan a esos estudios viejos.
- **SHEET**: la API no llena la casilla; los planos nuevos muestran "11" en vez de "1 of 1". Corregir a mano en cada plano.
- Cotas que el script no pudo poner (completar a mano): `salida/planos_onshape/COTAS_A_MANO_A4_v4.md`. En B1 faltan el ancho 132 y el 131 (bordes curvos) y hay textos de cota que se pisan; revisar a ojo.
- B3_caja: la nota de chaflanes del plano dice "postes bandeja Ø8"; son Ø9.
- M1s_caja_cuerpo: la nota de chaflanes viene de los datos del 01/11 y puede no describir el riel cerrado; revisarla.
- B2 y B5 en mitades: sin cota de chaflán (agregar a mano si se pide).
- Los dibujos con script de B4, M2, M3t, M6 y SKIN ya no existen en Onshape; para el PDF v4 se usaron sus PDF del 31/10 (piezas sin cambios).

## Bloque 2.1 de Onshape (04/11, noche): lo que queda a mano
- **Borrar a mano** en LG_IMPRIMIR_P2 las pestañas "OLD 2026-11-04 …": 17 estudios con su `.step` ("geometría anterior"), los dibujos "OLD … PLANO_A4_…" (12 reemplazados por uno nuevo y 5 por plano local) y las de las tandas anteriores (la API no borra, 403). No se copiaron a LG_HISTORICO esta vez; si hace falta el historial, git guarda los STEP.
- **Campo SHEET** del cajetín: los 12 planos de Onshape dicen "11" en vez de "1 of 1" (la API no lo llena); corregirlo a mano.
- **Planos que no entraron en la cuota** (hay plano local en el PDF v5, rotulado así): M5s_capsula_tapa_pie, M11_bandeja, M11_bandeja_sup, M3t_tapa_bolsillo y B6_correa. Si se quiere versión Onshape: `python planos_0511.py --dibujar <pieza>` (unas 20 llamadas cada una) cuando haya cupo. M6_capsula_bisel usa el plano de Onshape del 31/10 (el modelo no cambió).
- **Cotas a mano**: la lista de lo que falta por plano está en `docs/COTAS_A_MANO.md` y en la portada del PDF v5. Los planos locales solo traen cotas generales, lista de agujeros y nota de chaflán.
- **00_ENSAMBLE**: la boya está corrida 700 mm a un lado del nodo (no hay marco de amarre en el modelo); si se quiere en su posición real, hay que definir ese marco.
- **Melissa**: sus "Drawing 1 … 16" no se tocaron; los desactualizados siguen así (ver tabla en `docs/CAMBIOS.md`).
- Quedan sin renombrar los dibujos "PLANO_A4_<pieza>" de pestañas viejas como "Assembly 1", "BOM : Assembly 1" y "Part Studio 1" (del documento original).

## Encargo del 04/11 noche: lo que queda a mano
- **Drive, borrar a mano** (ya están copiados en `OLD/`):
  - `02_Imprimir_primero_probetas/imprimir_hoy_04nov*` y `*_30oct*`;
  - `04_Planos/PLANOS_A4_LanternGuard{,_v2,_v3,_v4}.pdf`, `PLANOS_ONSHAPE_P2.pdf`, `PLANO_*.pdf` y `COTAS_A_MANO_A4.md`;
  - `04_Planos/STL_por_pieza/B2_cubierta.stl` y `B5_cuna.stl`;
  - `07_Documentos/visor/lanternguard.glb`.
- **Boya con una botella perdida:** GM de balanceo 38 mm (objetivo 40). Opciones: botellas un poco más separadas o lastre bajo el casco.
- **Holgura cuerda–caja del nodo:** 1,5 mm (antes 2,9), porque la caja creció 2 mm por la pared de 5. Revisar al armar con la linterna real.
- **Riel M3s:** queda con 12,2 % de soporte (excepción documentada en DECISIONES).
