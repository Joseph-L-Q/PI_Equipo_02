# HANDOFF siguiente | LanternGuard CAD | 04/11/2026 (sesión de día, Yoichi ausente hasta la noche)

La rama es `cad/version-final`. Cada paso tiene commit y push a `origin` (equipo) y a `personal` (respaldo privado `IchiSieben/LanternGuard-CAD-backup`).
Leer primero `docs/ESTADO.md` (sección 04/11), `docs/PENDIENTES.md` (bloqueos del 04/11) y `docs/DECISIONES.md` (raíz del repo).

## Hecho hoy
- **Paso 0:** respaldo privado con todas las ramas. Hay una write key de ThingSpeak de un taller en el historial; ya era pública. `docs/RETOMAR_EN_OTRA_PC.md`.
- **`cad/celosia-v2`:** congela el concepto anterior (riel en celosía y caja con PG7), commit 7a2bc7c.
- **Convención de nombres (bloque 2, casi completo):**
  - lo vigente va sin sufijo;
  - LG_HISTORICO creado, con 4 STEP "OLD 2026-11-01 <pieza> (sin chaflan)";
  - en LG_IMPRIMIR_P2 lo vigente quedó sin `_v1` ni `_v2`;
  - pestaña CAMBIOS en LG_00_LEER_PRIMERO;
  - herramienta: `cad_final/onshape_historico.py`;
  - la API **no puede borrar** (403): las 4 "OLD …" de LG_IMPRIMIR_P2 se borran a mano;
  - no había ninguna `zz_*`, porque Melissa las borró el 02/11 y rehizo los planos a mano como "Drawing 1 … 16". **Sus planos no se tocan.**
- **Boya (pasos 2 y 3):** B1, B2 y B5 quedan en mitades ≤ 230.
  - B1 son 2 mitades iguales con brida de 4 + 4 mm, 6 M3 inox y 2 pines;
  - B2 se divide en lado liso y lado mástil;
  - B5 se divide en lado base y lado cuello;
  - 2 ojales de amarre en x = ±21;
  - las costillas intermedias quedan como topes bajos de 4 mm (se eliminaron las varillas de 2,4 × 3 mm), y los postes pasan a Ø10 con collar;
  - resultado: 958 g, 39,6 h, calado 40,8 mm, francobordo 80,7 mm, GM 107 / 733 mm;
  - detalle en `docs/BOYA.md` §04/11; interruptores `boya_pet.partir` y `boya_pet.topes_bajos`.
- **Márgenes (paso 1):**
  - `impresora.cama_util = 230` y `cama.py`: `build.py` falla si una pieza se pasa;
  - `docs/MARGENES.md` mide la pared con rayos;
  - postes de la bandeja de B3 a Ø9;
  - fuera de 230 solo queda M1m de P3/P4.
- **Placas:** 19 placas sin fallas, **2567 g y 92,3 h** (nodo P2 previo a 3a, boya y probetas). En Drive `02_Imprimir_primero_probetas/imprimir_hoy_04nov/`.
- **SimScale:**
  - la clave de `cad_final/.env` (`SIMSCALE_API_KEY`) **responde**: se listaron 2 proyectos;
  - el SDK se instaló desde `git+https://github.com/SimScaleGmbH/simscale-python-sdk.git` (en PyPI no está);
  - **`docs/PENDIENTES.md` dice todavía que no hay clave: corregir esa línea.**

## Bloqueado
**Corrección de concepto 3a** (riel cerrado estanco, un solo volumen seco, cable plano por dentro, sin prensaestopas intermedio, "pasos A a E"). El prompt nunca llegó: el mensaje traía el marcador "[pega aquí el prompt de corrección de concepto completo]". De ella dependen:
- el riel M3s (FS entre capas 2,72) y el pie M5s (2,47);
- el lastre nuevo y la lista de sellos definitiva;
- M1m de P3/P4.

## Lo que quedaba del BLOQUE 1 al cortar
- **Guía de piezas (paso 4): HECHA** (18 páginas, `docs/GUIA_PIEZAS_LanternGuard.pdf`, en Drive 07_Documentos). Dudas abiertas: M11 (pasos M3 tapados por los postes, ventana Ø27), sellador de la ventana M7 "a definir". Sin revisar a ojo: B2 lisa, B5 cuello, B6, M3t, M6, M11 sup.
  - `salida/guia_piezas/*.png|pdf`;
  - `docs/GUIA_PIEZAS_LanternGuard.pdf` y `docs/GUIA_PIEZAS.md`;
  - `docs/ESTANQUEIDAD.md`;
  - `salida/guia_piezas/{sellos,rasgos}.json`.

  Revisa si esos archivos existen; si no, rehazlo. Después: commit y subir el PDF a Drive `07_Documentos/`.
- **Planos A4 en Onshape** de las piezas nuevas o cambiadas: B1_casco (mitad), B2_cubierta_lisa, B2_cubierta_mastil, B3_caja, B5_cuna_base, B5_cuna_cuello y B6_correa.
  - Se suben a LG_IMPRIMIR_P2 con la convención nueva (`PLANO_A4_<pieza>`, sin sufijo), con `planos_onshape.py --formato equipo`. Hay que adaptarlo: `V2_PIECES`, `A4_ORDER`, `PIECES` y `piece_v2` escriben `_v2`, y hay que quitarlo.
  - Lo reemplazado se retira con `python cad_final/onshape_historico.py --doc LG_IMPRIMIR_P2 --tab <tab> --fecha 2026-11-04 --motivo "partida en mitades"` (B1_casco, B2_cubierta, B5_cuna y sus STEP). **No tocar los "Drawing N …" de Melissa.**
  - Cupo de la API: 1549 llamadas usadas de ~2200 (`LIMIT_A4`); mira `onshape_calls.log`.
- **PDF de planos unido v4** a Drive `04_Planos/PLANOS_A4_LanternGuard_v4.pdf`. En Drive solo se usa `rclone copy`; no se renombra nada.
- **ESTADO.md** a Drive `07_Documentos/ESTADO.md` (`rclone copyto docs/ESTADO.md lgdrive:07_Documentos/ESTADO.md`).

## COLA DE TRABAJO (texto íntegro del usuario, bloques 2 a 5)
Después de CADA bloque: commit, push, actualiza docs/ESTADO.md (hora, qué terminó, qué falta, links, problemas) y súbelo a Drive LanternGuard_CAD/07_Documentos/ESTADO.md. Si algo bloquea, anótalo en docs/PENDIENTES.md y sigue con el siguiente bloque.

BLOQUE 2. CONVENCIÓN DE NOMBRES. Lo vigente sin sufijo ni versión (B1_casco, PLANO_A4_B1_casco). Lo reemplazado se copia al documento LG_HISTORICO (créalo en la carpeta LanternGuard de Onshape) con nombre "OLD <fecha> <pieza> (<motivo>)" y se elimina de LG_IMPRIMIR_P2; si la API no permite copiar pestañas entre documentos, renómbralas con ese formato dentro de LG_IMPRIMIR_P2 y anótalo para moverlas a mano. Renombra también las zz_* que existan. En LG_00_LEER_PRIMERO, pestaña CAMBIOS con una línea por fecha.
*(Estado: hecho, salvo el borrado a mano y actualizar CAMBIOS con lo del 04/11 cuando se suban las mitades.)*

BLOQUE 3. SIMSCALE con la API oficial (pip install simscale-sdk). Clave en cad_final/.env como SIMSCALE_API_KEY: nunca la imprimas ni la subas a git. Script reutilizable cad_final/simscale_run.py (--pieza X). Proyecto "LanternGuard FEM 2026-11". Dos grupos:
 A) NODO SUMERGIDO: M3s_riel (cerrado), M5s_capsula_tapa_pie, M1s_caja_cuerpo. Estático lineal, PETG (E 2,1 GPa, ν 0,38, ρ 1270 kg/m³, σ_adm 50 MPa). Apoyos y cargas iguales a cad_final/fem.py (150 N en el gancho; corriente 1,5 m/s como presión sobre la cápsula). Caras elegidas por posición y normal. Malla estándar 2.º orden.
 B) BOYA: B3_caja y B2_cubierta (mitades) con peso de panel y electrónica + golpe de ola 200 N sobre la cubierta. Aclarar que flotación y estabilidad son analíticas (docs/BOYA.md).
 Por pieza: subir STEP limpio, configurar, correr, esperar, descargar resultados y capturar von Mises (MPa), desplazamiento (mm), malla y condiciones de borde. Tabla: σmax, FS = 50/σmax, desplazamiento máx., comparación con el FEM local. PDF REPORTE_SIMSCALE_LanternGuard.pdf a Drive 06_SimScale/ con el link público de cada simulación.
 Si la cuenta gratuita limita horas o malla, usa malla más gruesa y anótalo. Si un paso de la API no existe en el plan gratuito o no hay clave, deja el proyecto con geometría, material y condiciones cargadas y escribe en GUIA_SIMSCALE.md qué falta apretar a mano, con capturas de las caras a seleccionar (PyVista, caras resaltadas).
*(Corrección del usuario: la clave SÍ existe en cad_final/.env línea 3. Cárgala desde .env como onshape_sync.py, sin imprimirla. Plan A, simulación real por API. Solo si una verificación falla, pega SOLO el código de error en PENDIENTES.md y cae al plan B. Verificada el 04/11: responde. El riel "cerrado" no existe hasta 3a: simular el M3s vigente y anotarlo.)*

BLOQUE 4. VISOR 3D INTERACTIVO. Página HTML de un solo archivo con three.js (versión fija desde cdnjs), en docs/visor/index.html y subida a Drive 07_Documentos/visor/:
 - Ensamble nodo + boya exportado a GLB, una malla por pieza con su código.
 - Clic en una pieza: se resalta y muestra panel con nombre, función, material, gramos, horas, con qué se une, tornillos, y cada agujero explicado (reusa GUIA_PIEZAS).
 - Botón "explotar" que separa las piezas; pasos de ensamble numerados que animan la colocación; sellos marcados en rojo (reusa ESTANQUEIDAD.md).
 - Lista lateral, buscador, modo claro/oscuro, funciona en celular.

BLOQUE 5. CIERRE. docs/ENTREGA_2026-11-04.md + PDF para el equipo (qué cambió y por qué, gramos y horas totales, lastre, lista de sellos, links a todo), a Drive 07_Documentos. docs/HANDOFF_siguiente.md actualizado. ESTADO.md final con "TERMINADO" y la hora. Resumen de 15 líneas con links.

**Reporte final pedido antes (paso 4 del mensaje de las 07:40):**
- gramos totales de nodo + boya + probetas, horas, lastre nuevo y lista de sellos;
- si el total impreso pasa de 2,7 kg, avisarlo al inicio del resumen;
- una respuesta de 3 líneas para la profesora sobre los soportes delgados (ver `docs/DECISIONES.md`, 04/11, "Soportes delgados del casco").
