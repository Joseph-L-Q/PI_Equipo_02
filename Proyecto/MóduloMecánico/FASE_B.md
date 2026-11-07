# Fase B | Probetas (28/10/2026)

Son lo primero que se imprime. Correr: `cd cad_final` y `python probetas.py`. Salen 14 STL en `salida/probetas/` y el render `probetas_iso.png`. El detalle por pieza (orientación, voladizo, qué medir) está en `cad_final/reporte_probetas.md`, que se regenera con el script.

| Probeta | Piezas | Qué se prueba | Qué parámetro calibra |
|---|---|---|---|
| PB1 garra + casquillos | `PB1_garra`, `M13_casquillo_D6/D8/D10/D12` | Encaje en tramos de varilla real; fuerza de entrada y salida con un dinamómetro de equipaje; correa de 25 en su ranura | `gancho.alojamiento`, `casquillo.interferencia`, `casquillo.holgura_varilla` |
| PB2 ranura T | `PB2_ranura_T` | Que la tuerca M4 entre por la punta y deslice, y que el perno pase | `riel.ranura_T`, `riel.ranura_T_nervio` |
| PB3 unión de tramos | `PB3_macho`, `PB3_hembra` | La llave en cola de milano entra deslizando de costado; 2 M4 con tuerca dentro de las paredes; ranura T continua | `riel.union_*`, `riel.cola_llave` |
| PB4 pestillo | `M14_pestillo` (sobre PB1, pivote M3) | El resalte de 0.6 da un clic, no se suelta solo y se abre con guante | `pestillo.resalte` |
| PB5 perilla | `M12_perilla` | Perno M4 embebido: **pausar la impresión** al llegar al bolsillo hexagonal, meter la cabeza y seguir | `m4.cabeza_hex`, `perilla.*` |
| PB6 junta | `PB6_base`, `PB6_tapa` | Cuadrado de 60 × 60, junta Ø2 en la ranura de 2.6 × 1.5 y 4 M3 con insertos; sumergir a 1 m | `junta.*`, `m3.inserto_*` |
| PB7 peine | `PB7_peine`, `PB7_pines` | Holguras 0.2, 0.3, 0.4 y 0.5, de izquierda a derecha (el texto grabado rompía las booleanas y se omitió) | `impresion.holgura`, `impresion.comp_agujero` |

Las 14 piezas pasan BRepCheck y BOPAlgo, y cada STL es cerrado, de 1 cuerpo y cabe en la cama. El pestillo cerrado contra la garra y el macho contra la hembra dan 0 mm³ de interferencia.

**Decisiones de forma** (las constantes quedaron en `params.py`, bloque "probetas"): la garra mide 12 de ancho (el contacto) y lleva un vástago con M4 para atornillarla a PB2. El casquillo es una C con la boca hacia la abertura de la J y una pestaña de tope. La unión es una media madera con llave en cola de milano vista de lado; las paredes se engrosan a 10 para que la tuerca M4 tenga 1.4 mm de piel (la primera versión dejaba 0.4). Ver D15 en `FASE_A.md`.

## Cierre de la fase

- **Qué cambió:** `cad_final/probetas.py` genera las 7 probetas (14 STL) desde `params.py`. A `checks.py` se sumaron la exportación STL y los chequeos de malla de `cad/build.py`.
- **Qué chequeos pasaron:** BRepCheck, BOPAlgo, STL cerrado de 1 cuerpo, cama, y 0 mm³ de interferencia en los dos pares que van montados.
- **Qué quedó pendiente:** imprimirlas y medir. Con los resultados se ajustan holgura, ranura T, resalte del pestillo y casquillos antes de la Fase C final.
