# Reporte de verificación (generado por `build.py`)

No editar a mano: se regenera. Valores en mm, cm³, g y MPa.

## 1. Piezas: sólido cerrado e imprimible

Cama supuesta 220 × 220 × 250 mm. Voladizo = caras con normal hacia abajo a más de 45° de la vertical, fuera de la cama, en la orientación de impresión indicada.

| Pieza | Archivo | Material | Cant. | Sólido válido | Estanco (STL) | Cuerpos | Volumen cm³ | Masa g (100 % relleno) | Caja en orientación de impresión | Cabe en la cama | Voladizo mm² |
|---|---|---|---|---|---|---|---|---|---|---|---|
| M1 | `M1_caja_central_cuerpo` | PETG | 1 | sí | sí | 1 | 238.3 | 303 | 162 × 94 × 60 | sí | 570 |
| M2 | `M2_caja_central_tapa` | PETG | 1 | sí | sí | 1 | 118.9 | 151 | 160 × 94 × 64 | sí | 1847 |
| M3 | `M3_brazo` | PETG | 2 | sí | sí | 1 | 78.2 | 99 | 42 × 34 × 242 | sí | 902 |
| M4 | `M4_capsula_cuerpo_P4revB` | PETG | 2 | sí | sí | 1 | 53.7 | 68 | 64 × 64 × 56 | sí | 1101 |
| M5 | `M5_capsula_tapa` | PETG | 2 | sí | sí | 1 | 23.5 | 30 | 64 × 64 × 33 | sí | 701 |
| M6 | `M6_bisel_ventana` | PETG | 2 | sí | sí | 1 | 2.3 | 3 | 42 × 42 × 2 | sí | 0 |
| M7 | `M7_ventana` | acrílico 3 mm (comprado, cortado) | 2 | sí | sí | 1 | 2.1 | 3 | 3 × 30 × 30 | sí | 54 |
| M8 | `M8_marco_malla_prueba` | PETG | 1 | sí | sí | 1 | 71.4 | 91 | 200 × 200 × 6 | sí | 0 |

Antes de exportar, cada pieza pasa por `clean()`, `ShapeFix_Shape` y `UnifySameDomain` (OCP), y luego por `BRepCheck_Analyzer`, `BOPAlgo_ArgumentAnalyzer` y un barrido de astillas (arista ≥ 0.05 mm, cara ≥ 0.01 mm²). Si algo falla, el build se detiene. El STEP escrito se vuelve a leer y se compara.

| Pieza | BRepCheck | BOPAlgo | Sólidos | Arista mínima mm | Cara mínima mm² |
|---|---|---|---|---|---|
| M1 | ok | ok | 1 | 3.00 | 5.37 |
| M2 | ok | ok | 1 | 1.50 | 8.25 |
| M3 | ok | ok | 1 | 0.39 | 0.73 |
| M4 | ok | ok | 1 | 2.80 | 2.54 |
| M5 | ok | ok | 1 | 1.05 | 0.73 |
| M6 | ok | ok | 1 | 2.50 | 18.85 |
| M7 | ok | ok | 1 | 3.00 | 282.74 |
| M8 | ok | ok | 1 | 2.00 | 38.00 |


## 2. Espesores mínimos que quedan bajo cada corte

Mínimo aceptado: 1.2 mm (3 perímetros de boquilla 0.4).

| Zona | Espesor mm | ¿≥ mínimo? |
|---|---|---|
| Hombro de la ventana (pared frontal − asiento) | 2.80 | sí |
| Tapa cápsula bajo la ranura del O-ring | 3.50 | sí |
| Tapa caja bajo la ranura del O-ring | 4.50 | sí |
| Ranura ↔ agujero de tornillo (cápsula) | 1.25 | sí |
| Ranura ↔ cavidad (cápsula) | 2.95 | sí |
| Ranura ↔ agujero de tornillo (caja, lado corto) | 1.75 | sí |
| Ranura ↔ cavidad (caja, lado corto) | 3.45 | sí |
| Fondo del inserto M3 ↔ cavidad (almohadilla del brazo) | 9.00 | sí |
| Agujero piloto M2 del bisel ↔ cavidad | 2.00 | sí |
| Pared de brazo | 3.00 | sí |
| Barra de malla de prueba | 2.00 | sí |

## 3. Encaje de componentes e interferencias

`ENSAMBLE_modulo.step` releído: 12 sólidos, todos válidos según BRepCheck.

| Par | Volumen de interferencia mm³ | Holgura mínima mm | Resultado |
|---|---|---|---|
| esp32_devkit_wroom32u ↔ caja (cuerpo) | 0.00 | 1.59 | OK |
| esp32_devkit_wroom32u ↔ caja (tapa) | 0.00 | 36.00 | OK |
| microsd_module ↔ caja (cuerpo) | 0.00 | 1.59 | OK |
| microsd_module ↔ caja (tapa) | 0.00 | 37.00 | OK |
| max485_module ↔ caja (cuerpo) | 0.00 | 1.59 | OK |
| max485_module ↔ caja (tapa) | 0.00 | 37.00 | OK |
| jsn_sr04t_board ↔ caja (cuerpo) | 0.00 | 1.59 | OK |
| jsn_sr04t_board ↔ caja (tapa) | 0.00 | 39.00 | OK |
| jsn_sr04t_probe ↔ caja (cuerpo) | 0.00 | 0.20 | OK |
| jsn_sr04t_probe ↔ caja (tapa) | 0.00 | 38.00 | OK |
| contratuerca PG7 (+X) ↔ esp32_devkit_wroom32u | 0.00 | 72.04 | OK |
| contratuerca PG7 (+X) ↔ microsd_module | 0.00 | 82.12 | OK |
| contratuerca PG7 (+X) ↔ max485_module | 0.00 | 12.72 | OK |
| contratuerca PG7 (+X) ↔ jsn_sr04t_board | 0.00 | 5.50 | OK |
| contratuerca PG7 (+X) ↔ jsn_sr04t_probe | 0.00 | 48.46 | OK |
| contratuerca PG7 (−X) ↔ esp32_devkit_wroom32u | 0.00 | 2.50 | OK |
| contratuerca PG7 (−X) ↔ microsd_module | 0.00 | 4.40 | OK |
| contratuerca PG7 (−X) ↔ max485_module | 0.00 | 81.01 | OK |
| contratuerca PG7 (−X) ↔ jsn_sr04t_board | 0.00 | 83.18 | OK |
| contratuerca PG7 (−X) ↔ jsn_sr04t_probe | 0.00 | 48.46 | OK |
| contratuerca PG9 (tapa) ↔ caja (cuerpo) | 0.00 | 5.00 | OK |
| contratuerca PG9 (tapa) ↔ esp32_devkit_wroom32u | 0.00 | 33.48 | OK |
| contratuerca PG9 (tapa) ↔ microsd_module | 0.00 | 33.66 | OK |
| contratuerca PG9 (tapa) ↔ max485_module | 0.00 | 43.03 | OK |
| contratuerca PG9 (tapa) ↔ jsn_sr04t_board | 0.00 | 35.88 | OK |
| contratuerca PG9 (tapa) ↔ jsn_sr04t_probe | 0.00 | 33.00 | OK |
| contratuerca PG7 (cápsula) ↔ cámara | 0.00 | 5.34 | OK |
| contratuerca PG7 (cápsula) ↔ cápsula (cuerpo) | 0.00 | 0.00 | OK |
| contratuerca PG7 (cápsula) ↔ cápsula (tapa) | 0.00 | 1.34 | OK |
| cámara ↔ cápsula (cuerpo) | 0.00 | 1.00 | OK |
| cámara ↔ cápsula (tapa) | 0.00 | 24.00 | OK |
| ventana ↔ cápsula (cuerpo) | 0.00 | 0.00 | OK |

Bisagra: la lengüeta de la tapa engrana con las orejas del brazo. Se comprueba el cuerpo de la cápsula contra el brazo en todo el rango; los dientes de la tapa contra los del brazo se reportan aparte porque se tocan por diseño (flanco con flanco).

| Ángulo | Cuerpo cápsula ↔ brazo mm³ | Holgura mm | Tapa (sin dientes) ↔ brazo mm³ |
|---|---|---|---|
| 0° | 0.00 | 12.97 | 0.00 |
| 10° | 0.00 | 12.97 | 0.00 |
| 20° | 0.00 | 12.97 | 0.00 |
| 30° | 0.00 | 12.97 | 0.00 |
| 40° | 0.00 | 12.97 | 0.00 |
| 50° | 0.00 | 12.97 | 0.00 |
| 60° | 0.00 | 12.97 | 0.00 |
| 70° | 0.00 | 12.97 | 0.00 |
| 80° | 0.00 | 11.48 | 0.00 |
| 90° | 0.00 | 8.50 | 0.00 |

Dientes engranados a 40° (ángulo de trabajo): solape 0.00 mm³ (≈ 0 = flancos en contacto, sin juego ni choque).

## 4. Peso y flotabilidad (exigencia: peso aparente de 0.2 a 0.5 kgf; ≤ 3 kg en aire)

| Concepto | Valor |
|---|---|
| PETG impreso (sin el marco de prueba), 100 % relleno | 854 g |
| Ventanas de acrílico | 5 g |
| Electrónica (datasheets, ver params.py) | 63 g |
| Cables y prensaestopas (supuesto) | 40 g |
| Tornillería (supuesto) | 60 g |
| **Masa total en aire** | **1022 g** (cumple ≤ 3 kg) |
| Aire sellado (caja 470 + 2 cápsulas × 72) | 615 cm³ |
| Volumen desplazado | 1299 cm³ |
| Empuje en agua de mar (1.025 g/cm³) | 1332 g |
| **Peso aparente** | **-310 g** (flota) |
| Lastre para entrar en 0.2 a 0.5 kgf | 510 a 810 g de peso aparente (acero inoxidable: ×1.15 en aire, ≈ 586 a 931 g) |

El relleno real < 100 % baja la masa y deja aire atrapado en las paredes: el peso aparente real será más negativo. Medir en balde y ajustar el lastre.

## 5. Presión a 15 m (0.15 MPa): placa plana, estimación de Roark

Fórmula: σ = β·q·b²/t², y = α·q·b⁴/(E·t³). Roark, *Formulas for Stress and Strain*, 7.ª ed., tabla 11.4 caso 1a (bordes simplemente apoyados, más conservador que empotrado). σy PETG = 45.0 MPa, E = 1700 MPa (valores tentativos del T01).

| Panel | a × b mm | t mm | β | σ MPa | FS = σy/σ | Flecha mm |
|---|---|---|---|---|---|---|
| Tapa de la caja | 132 × 66 | 6 | 0.610 | 11.1 | 4.1 | 0.86 |
| Fondo de la caja | 132 × 66 | 6 | 0.610 | 11.1 | 4.1 | 0.86 |
| Pared lateral de la caja | 132 × 54 | 5 | 0.656 | 11.5 | 3.9 | 0.73 |
| Pared extrema de la caja | 66 × 54 | 5 | 0.385 | 6.7 | 6.7 | 0.38 |
| Pared de la cápsula | 50 × 38 | 4 | 0.421 | 5.7 | 7.9 | 0.20 |
| Tapa de la cápsula | 38 × 38 | 5 | 0.287 | 2.5 | 18.1 | 0.07 |

**Límites de esta estimación.** (1) Roark supone placa sin agujeros: el agujero del sensor JSN-SR04T está en el centro del fondo, donde el momento es máximo, con un factor de concentración Kt ≈ 2. (2) En las paredes laterales la flexión cruza las capas de impresión, la dirección débil del FDM (resistencia entre capas del orden de la mitad). Con ambos efectos, el factor de seguridad efectivo del fondo y de las paredes laterales baja a **≈ 2**, no a los valores de la tabla. **No está probado**: falta el ensayo en cámara de presión o a profundidad. Las simulaciones SimScale del equipo usaron 50 kPa (≈ 5 m), un tercio de esta carga.

## 6. Junta tórica (sello de cara, estático)

Cordón Ø2.0 mm en ranura de 2.6 × 1.5 mm: compresión 25 % (rango habitual 15 a 30 % para sello estático), llenado de ranura 81 % (< 90 %). Calculado, **no probado**.
