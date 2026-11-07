# Encargo SimScale por módulo ensamblado (07/11/2026)

Escrito desde el chat de Claude para la sesión de Claude Code de la PC de casa. Ejecutar completo, sin preguntar salvo bloqueo real. Commit y push al final.

## 0. Verificar que se trabaja con LO ÚLTIMO (obligatorio antes de simular)

La simulación tiene que ser de exactamente lo que se entregó para imprimir. Melissa pudo haber borrado o cambiado cosas en Onshape después.

1. `git pull` en `cad/version-final` (origin y personal). Anota el commit.
2. Fuente de verdad de la geometría: el CAD del repo (params.py + scripts), en el commit que generó el documento limpio (7ef7793 o posterior). Confirma que M3s tiene asiento Ø17,1, LR2_aro Ø16,5 con 13 perímetros, riel cerrado, B1/B2/B5 en mitades, caja M1s y tapa M2 con chaflán de 6 mm, cubiertas B2 con barras 26 x 20, T1/T2 de tierra.
3. Comparar con el documento entregado "LanternGuard - PIEZAS PARA IMPRIMIR":
   https://cad.onshape.com/documents/76e36e0130a8d259842ecee7/w/fdd58e8bdf77f39a1781a12d
   Es de Melissa (no usar la API de la cuenta personal: cuota agotada). Ábrelo con Playwright por el link público (si Melissa ya activó link sharing) y lista sus pestañas: nombres, cantidad de piezas, ensambles 00_ENSAMBLE_nodo / _boya / _tierra. Si el link no abre sin login, compara contra la lista registrada en cad_final/onshape_docs.json y anótalo.
4. Comparar con Drive (rclone `lgdrive:`): 04_Planos (PLANOS_A4 más reciente, STL_por_pieza + LEEME), 02_Imprimir (imprimir_hoy_2026-11-05), 08_PARA_IMPRIMIR si existe.
5. Escribe `docs/VERIFICACION_2026-11-07.md` con una tabla pieza por pieza: repo / Onshape entregado / Drive, y cualquier diferencia. Si hay una diferencia de GEOMETRÍA (no solo de nombres o pestañas borradas), DETENTE y repórtala antes de simular. Si solo faltan archivos en Drive, súbelos y sigue.

## 1. SimScale por módulo ENSAMBLADO (no pieza por pieza)

Como lo hizo María: subió el ensamble completo como un solo modelo y corrió un estático lineal. Referencias (versión vieja, solo para copiar la configuración):
- Módulo sumergido (estático, bien hecho): https://www.simscale.com/projects/antena/prueba_-_m-dulo_sumergido_pi__104166404 (máx. 19,5 MPa → FS ≈ 2,6 con PETG)
- Boya (es un análisis de FLUJO con dominio cúbico, no estructural): https://www.simscale.com/projects/Maraa/prueba_-_boya_553159539

Ábrelas con Playwright y copia: tipo de análisis, contactos, malla, apoyos y cargas.

Clave en cad_final/.env como SIMSCALE_API_KEY (dotenv, nunca imprimirla). Reusa cad_final/simscale_run.py con un modo --modulo. No borres proyectos anteriores.

1. "LanternGuard 1 - Nodo sumergido": STEP del ensamble actual completo (un solo upload). Estático lineal, PETG (E 2,1 GPa, ν 0,38, ρ 1270 kg/m³, σ_adm 50 MPa), contactos bonded automáticos. Apoyo en el asiento del gancho sobre el aro. Cargas: peso + lastre como masa (990 g), 150 N sobre una cápsula, corriente 1,5 m/s como presión.
2. "LanternGuard 2 - Boya":
   (a) Estático lineal del ensamble completo: peso + panel + electrónica, ola 200 N sobre la cubierta, golpe lateral 200 N sobre el panel, tiro del cabo 300 N en la pata de gallo; apoyo en el amarre (documentar supuesto).
   (b) Si quedan horas de cómputo: flujo incompresible con dominio cúbico como el de María, corriente 1,5 m/s, para la fuerza de arrastre.
3. "LanternGuard 3 - Estación de tierra": T1 + T2, PLA (E 3,5 GPa, ν 0,36, ρ 1240, σ_adm 40 MPa). Estático: 50 N sobre la tapa, 30 N lateral sobre la antena SMA; fijo en las pestañas.

Si el plan gratuito rechaza la malla, simplifica (quitar roscas, texto, chaflanes < 2 mm) y anótalo; no pases a pieza por pieza sin avisar.

## 2. Capturas

Los proyectos del plan gratuito son públicos: captura con Playwright desde la página pública y el post-procesador, sin depender de descargas por API. Por módulo: von Mises con leyenda, desplazamiento, malla y condiciones de borde, vista ISO, 1920 x 1080. Si alguna vista exige login, anótalo en GUIA_CAPTURAS_SIMSCALE.md con qué abrir y qué capturar.

## 3. Entrega

- Por módulo: σmax, FS = σ_adm/σmax, pieza donde ocurre, desplazamiento máximo, comparación con el resultado viejo de María (19,5 MPa) y con el FEM local.
- REPORTE_SIMSCALE_MODULOS.pdf con capturas y los 3 links públicos → Drive 06_SimScale/.
- Subir a Drive lo pendiente del SIS: STL y planos A4 de M3s, LR2_aro, T1, T2.
- docs/ESTADO.md y HANDOFF_siguiente.md actualizados. Commit y push.
- Resumen corto: commit, resultado de la verificación, 3 links, FS de cada módulo.
