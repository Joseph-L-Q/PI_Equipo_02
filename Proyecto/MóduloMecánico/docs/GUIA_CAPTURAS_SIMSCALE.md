# Guía de capturas de SimScale (07/11/2026)

Esta guía explica qué capturas se pueden sacar sin iniciar sesión y cuáles piden abrir el workbench con tu cuenta.

## Qué se puede sacar sin sesión (lo hace `cad_final/capturas_simscale.py`)

Los proyectos del plan gratuito son públicos. Su página está en `https://www.simscale.com/projects/yoichi_palacio/<nombre>/`. El nombre lo da `https://www.simscale.com/api/v3/projects/<pid>/`, sin clave. En esa página:

- **Von Mises con leyenda, en vista ISO:** cada resultado se publica como un modelo 3D (CUG) que muestra el campo de von Mises. El script lo abre a pantalla completa en 1920 × 1080.
- **σ máx. exacto:** sale del `modelInfo` del mismo modelo (`resultInfoArr[0].maximumValue`, en Pa) y se guarda en `vistas.json`. No depende de leer la leyenda.

Uso: `python capturas_simscale.py <pid> ../salida/simscale_modulos/capturas/<módulo>` (Playwright con Chromium).

## Qué pide iniciar sesión

La API no entrega estos datos: devuelve 403 «export-source-locked» al exportar y «result is locked» al pedir un informe de capturas. La página pública tampoco los muestra. En Chrome, sin sesión, el workbench redirige a `/signin`.

| Captura | Dónde |
|---|---|
| Desplazamiento (magnitud) con leyenda | Workbench → proyecto → *Simulation Runs* → *Run* → *Solution Fields* → Post-procesador. Campo **Displacement**, componente **Magnitude**. Vista ISO (cubo de vistas, esquina +X −Y +Z) y leyenda visible. *Screenshot* a 1920 × 1080 |
| Malla | Workbench → *Meshes* → la malla del módulo. Vista ISO con aristas visibles (*Show edges*). Anotar el número de celdas que da el panel |
| Condiciones de borde | Workbench → *Simulations* → la simulación → *Boundary conditions*. Seleccionar cada apoyo y cada carga y capturar con las caras resaltadas |
| Configuración del modelo de María | `https://www.simscale.com/workbench/?pid=5976336888024613560` (nodo) y `?pid=5793875753508499519` (boya). Anotar tipo de análisis, contactos, malla, apoyos y cargas |

Mientras no estén esas capturas, el informe usa:
- un **render local** de las condiciones de borde, hecho con las mismas caras que se mandaron a SimScale (`simscale_modulos.py --bc <módulo>`), y marcado así;
- el **número de celdas** estimado por la API para la malla.

## Proyectos

| Módulo | pid | Página pública |
|---|---|---|
| LanternGuard 1 - Nodo sumergido | 4039119794151323480 | https://www.simscale.com/projects/yoichi_palacio/lanternguard_1_-_nodo_sumergido_1336844629/ |
| LanternGuard 2 - Boya | 133929070339263934 | https://www.simscale.com/projects/yoichi_palacio/lanternguard_2_-_boya_661668473/ |
| LanternGuard 3 - Estación de tierra | 120690419689208349 | https://www.simscale.com/projects/yoichi_palacio/lanternguard_3_-_estacion_de_tierra_418577745/ |

## Trampa del script de capturas

El `cug` que `vistas.json` asocia a cada captura no es fiable: a veces es el del modelo anterior. Cada captura se identifica por el título y el máximo de su leyenda. En tierra, la tarjeta 3 era la corrida descartada (0,92 MPa) y quedó en `capturas/tierra/_descartadas/`.
