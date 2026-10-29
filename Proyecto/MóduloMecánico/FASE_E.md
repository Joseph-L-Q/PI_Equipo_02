# Fase E: cálculo a mano

`cad_final/verificacion.py` → `cad_final/reporte_verificacion.md`, con fórmulas y unidades. Las secciones del riel salen
de cortes del CAD real (cuentan la ranura T, los nervios y las paredes engrosadas de la unión); el resto es aritmética
sobre `params.py`. Si no hay dato de capacidad (insertos, grado de los tornillos, acrílico), se da la exigencia y no un
factor de seguridad inventado. Carga de manipulación: 150 N en una cápsula; gancho: 75 N.

## Resumen

| Elemento | Resultado | FS a 45 / 22 MPa | Nota |
|---|---|---|---|
| Riel, sección llena (extensión) | Z = 2874 a 3018 mm³; σ máx. 9.5 MPa (Ø500, colgado del asa) | 4.7 / 2.3 | flecha de la punta 3.9 mm en Ø500 |
| **Unión, media madera macho** | Z = 698 mm³; σ = 39.2 MPa en Ø500 con el riel actual, 55 MPa con el largo que pide el armado | **1.1 / 0.6** (0.8 / 0.4) | punto débil del nodo |
| Unión, 2 M4 | T = 1825 N; aplastamiento del PETG 15.2 MPa | 3.0 / 1.4 | |
| Unión, llave sola | aplastamiento 57 MPa | 0.8 / 0.4 | conservador: comparte con los M4 |
| Insertos M4 del fondo de la caja | **274 N por inserto** (Ø500) | sin dato | hay que probar el inserto |
| Gancho, alma | 2.1 MPa | 21.6 | |
| Gancho, brida en el perno | 11.6 MPa; el perno lleva 181 N | 3.9 / 1.9 | |
| Asa, barra | 16.9 MPa | 2.7 | |
| Tapa, insertos M3 | 15 N por inserto + la junta | sin dato | |
| Bisagra | precarga del M4 ≥ 166 N para aguantar 150 N en el frente (unos 0.13 N·m de apriete) | aplastamiento > 4 | |
| Presión a 1 m | máx. 2.6 MPa (fondo de la caja) | 17 / 8 | ventana 0.24 MPa |
| Peso aparente | +208 a +253 g, 3 pletinas por lado | en ventana | total 1.86 a 2.07 kg (≤ 3) |
| Estabilidad | G entre 16.6 y 19.1 mm bajo B | no se voltea | |

## Decisiones tomadas sin consulta

| # | Qué | Por qué | Descartado | Cómo revertir |
|---|---|---|---|---|
| D34 | Corregido el cálculo de estabilidad de `fase_a.py`: el acero de las pletinas no sumaba a la masa total, y las cápsulas iban a la altura del riel | Era un error: el acero se restaba del "resto" en vez de sumarse. BG pasó de 8.9 / 9.8 a 19.1 / 17.4 mm (Ø100 / Ø500) | | `fase_a.stability` |
| D35 | Unión de tramos modelada como par con brazo = media altura (15): la tracción abajo la toman los M4 o la llave, se informan por separado | Ninguno de los dos trabaja solo; separarlos es conservador | Reparto por rigideces (sin datos) | `verificacion.py` §3 |
| D36 | Insertos del fondo con pivote en la línea de tornillos opuesta | Conservador; la brida real reparte | | `verificacion.py` §4 |
| D37 | μ = 0.3 PETG contra PETG en la bisagra, coeficiente de apriete 0.2 | Valores típicos, marcados como estimados | | `verificacion.py` §7 |

## Cierre

- **Qué cambió:** hay verificación a mano de todos los puntos del prompt y se corrigió la estabilidad de `fase_a.py`.
- **Qué chequeos pasaron:** el riel con sección llena, el gancho, el asa, la bisagra, la presión a 1 m, el peso aparente y
  el total ≤ 3 kg, todos con FS ≥ 1.9 entre capas donde aplica.
- **Qué quedó pendiente:** **la media madera de la unión**, con FS 1.1 a 45 MPa en Ø500, y bajo 1 si el riel se alarga
  como pide el armado (Fase D). La varilla M8 opcional del equipo la baja a unos 4 MPa si pasa ajustada por la unión
  (estimación gruesa, acero a unos 300 MPa). También falta probar el arranque de los insertos M4 (274 N).
