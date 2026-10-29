# Verificación a mano (generado por `verificacion.py`)

Carga de manipulación: 150 N en una cápsula; gancho: 75 N. PETG: E 1700 MPa, ν 0.38, σy 45 MPa macizo (a lo largo de las capas) y 22 MPa entre capas. Todos estimados. FS = σ admisible / σ calculada; se dan las dos columnas y se dice cuál aplica según la orientación de impresión.

## 1. Secciones del riel (cortes del CAD)

Corte de 0.05 mm del sólido real; I respecto del eje horizontal que pasa por el centroide; Z = I / c.

| Sección | A mm² | I mm⁴ | c mm | Z mm³ |
|---|---|---|---|---|
| ext_medio | 412 | 46051 | 15.3 | 3018 |
| ext_ranura_salida | 412 | 46051 | 15.3 | 3018 |
| union_hembra | 361 | 80087 | 24.5 | 3267 |
| union_macho | 229 | 6716 | 9.6 | 697 |

## 2. Riel con 150 N en la cápsula

Carga en el eje de la bisagra con el carro a ras de la punta (palanca máxima). La caída del eje bajo el riel no suma momento con carga vertical. El tramo se imprime acostado: la flexión va a lo largo de las capas (aplica 45).

**Caso A, nodo colgado del asa:** voladizo desde la caja. Momento en la unión central/extensión (|x| = 70) M = F·(x_carga − 70); en la sección llena σ = M/Z; en la media madera σ = M/Z_mitad. Flecha de la punta δ = F·L³/(3·E·I) con la sección llena (las uniones la aumentan).

**Caso B, nodo apoyado en los ganchos:** voladizo más allá del gancho, M = F·(x_carga − D/2).

| Aro | Ext. | Punta mm | x carga mm | A: M N·mm | A: σ llena MPa | A: σ media madera MPa | A: FS 45 / 22 (media madera) | A: flecha mm | B: M N·mm | B: σ MPa | B: FS 45 / 22 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Ø100 | 0 | 115 | 127.5 | 8625 | 2.9 | 12.4 | 3.6 / 1.8 | 0.1 | 11625 | 3.9 | 11.7 / 5.7 |
| Ø200 | 1 | 215 | 227.5 | 23625 | 7.8 | 33.9 | 1.3 / 0.6 | 2.5 | 19125 | 6.3 | 7.1 / 3.5 |
| Ø300 | 1 | 215 | 227.5 | 23625 | 7.8 | 33.9 | 1.3 / 0.6 | 2.5 | 11625 | 3.9 | 11.7 / 5.7 |
| Ø500 | 2 | 315 | 327.5 | 38625 | 12.8 | 55.4 | 0.8 / 0.4 | 10.9 | 11625 | 3.9 | 11.7 / 5.7 |

Con la punta (C18) el carro entra a ras de la punta en todos los aros; la fila usa esa posición (palanca máxima).

## 3. Unión de tramos (media madera + llave en cola de milano + 2 M4 verticales)

Momento más cargado: caso A, M = 38625 N·mm. Par de fuerzas con brazo igual a la media altura de la media madera (z = 15): la mitad de arriba se apoya en el hombro y abajo aparece una tracción T = M / 15 = **2575 N** que tiende a separar las mitades a lo largo del riel. La toman los 2 M4 en corte simple y la llave en aplastamiento; se dan los dos por separado (ambos son conservadores porque comparten).

- M4 solos, corte: τ = T / (2·12.6 mm²) = **102 MPa** en el acero (A2-70: fluencia del orden de 450 MPa, corte del orden de 0.6 de eso, dato de catálogo por confirmar).
- M4 solos, aplastamiento del PETG: σ = T / (2·d·h) con d = 4.0 y h = 15 (media altura) = **21.5 MPa** → FS 2.1 (45, carga en el plano de las capas, tramo acostado) / 1.0 (22).
- Llave sola (8 × 11 × 4), aplastamiento en su cara de 8 × 4: σ = 80.5 MPa → FS 0.6 / 0.3; corte en su base 11 × 8: τ = 29.3 MPa.
- Flexión en la media madera: σ = M / Z_mitad = 55.4 MPa → FS 0.8 / 0.4.

### 3b. La unión según el largo del riel

Mismo caso A con la punta del riel en cada configuración: la decidida el 29/10 (C18), la mínima que deja armar gancho + carro (R + 64) y la anterior.

| Aro | Configuración | Punta mm | M en la unión N·mm | σ media madera MPa | FS 45 / 22 |
|---|---|---|---|---|---|
| Ø100 | decisión 29/10 (paso 100 + punta) | 115 | 8625 | 12.4 | 3.6 / 1.8 |
| Ø100 | mínima para armar | 114 | 8475 | 12.2 | 3.7 / 1.8 |
| Ø100 | anterior (extensiones solapadas, sin punta) | 70 | 1875 | 2.7 | 16.7 / 8.2 |
| Ø200 | decisión 29/10 (paso 100 + punta) | 215 | 23625 | 33.9 | 1.3 / 0.6 |
| Ø200 | mínima para armar | 164 | 15975 | 22.9 | 2.0 / 1.0 |
| Ø200 | anterior (extensiones solapadas, sin punta) | 155 | 14625 | 21.0 | 2.1 / 1.0 |
| Ø300 | decisión 29/10 (paso 100 + punta) | 215 | 23625 | 33.9 | 1.3 / 0.6 |
| Ø300 | mínima para armar | 214 | 23475 | 33.7 | 1.3 / 0.7 |
| Ø300 | anterior (extensiones solapadas, sin punta) | 155 | 14625 | 21.0 | 2.1 / 1.0 |
| Ø500 | decisión 29/10 (paso 100 + punta) | 315 | 38625 | 55.4 | 0.8 / 0.4 |
| Ø500 | mínima para armar | 314 | 38475 | 55.2 | 0.8 / 0.4 |
| Ø500 | anterior (extensiones solapadas, sin punta) | 240 | 27375 | 39.2 | 1.1 / 0.6 |

Refuerzo opcional `riel.varilla_M8` (equipo) en el peor caso, M = 38625 N·mm, sección compuesta con la media madera macho (n = E_acero/E_PETG = 118, núcleo Ø6.47 en el centro del conducto, z = 15): I transformada 139394 mm⁴ contra 6716 sin varilla. PETG σ ≈ M·c/I = 4.2 MPa; acero σ ≈ n·M·y/I = 289 MPa. Sólo vale si la varilla pasa ajustada por la unión (agujeros o bujes) para que se curve junto con el riel; suelta en el conducto no ayuda. Estimación gruesa.

## 4. Insertos M4 del fondo de la caja (caso A)

El momento del riel entra a la caja por los 4 M4 de la brida de la cámara en (±40, ±20). Pivote en la línea de tornillos del lado opuesto (conservador): T_par = F·(x_carga + 40) / 80, la mitad por inserto.

| Aro | x carga mm | Tracción por inserto N |
|---|---|---|
| Ø100 | 127.5 | **157** |
| Ø200 | 227.5 | **251** |
| Ø300 | 227.5 | **251** |
| Ø500 | 327.5 | **345** |

**Exigencia:** cada inserto térmico M4 del fondo debe aguantar al menos 345 N de arranque en PETG (más el factor de seguridad que el equipo quiera). No hay dato de capacidad del inserto: hay que probarlo o tomarlo del fabricante.

## 5. Gancho con 75 N

Varilla en x = 0; alma de 12 × 12 de x = −12 a 0 (excentricidad e = 6); M4 de la perilla en x = -30.0; extremo de la brida en x = -47.0. La brida sólo puede empujar contra el fondo del riel, así que el apoyo está en el extremo del lado de la perilla y el perno toma la suma.

- Alma: σ = F/A + F·e/Z = 75/144 + 75·6/288 = **2.1 MPa** → FS 21.6 (45: el gancho se imprime de costado y la carga va en el plano de las capas).
- Reacción en el extremo de la brida R = F·24.0/17.0 = 106 N; perno M4 = F + R = **181 N**.
- Brida en el perno: M = 1800 N·mm, Z = (30 − 4.2)·6²/6 = 155 mm³, σ = **11.6 MPa** → FS 3.9 / 1.9.
- Tuerca M4 contra los labios de la ranura T (apoyo de 1.2 por lado × 7): σ = 10.8 MPa → FS 4.2 / 2.0 (tramo acostado: el labio trabaja en el plano de las capas, aplica 45).
- Asiento recto: flecha de la curva del aro sobre 12 de contacto, f = c²/(8R): Ø100 0.36 mm, Ø200 0.18 mm, Ø300 0.12 mm, Ø500 0.07 mm. El prompt pedía este cálculo: el asiento recto sirve.

## 6. Asa y tapa con 150 N de izado

- Barra del asa como viga simplemente apoyada de 90 (conservador), sección 12 × 10: M = F·L/4 = 3375 N·mm, σ = **16.9 MPa** → FS 2.7 (la tapa se imprime con el asa arriba: la barra flexa en el plano de las capas).
- Patas del asa: tracción a través de las capas, F/2 sobre 12 × 12: 0.52 MPa → FS 42 (22).
- 10 tornillos M3 con inserto en la brida: si sólo los tornillos llevan el izado, **15.0 N por inserto**, más la reacción de la junta tórica comprimida (sin dato: depende de la dureza del cordón).

## 7. Bisagra dentada

- Peso de la cápsula con contenido en aire: 128 g, centro a 43 del eje → par T = 54 N·mm (en el agua casi neutra: desplaza 128 cm³).
- Dientes: 36, alto 1.2, radio medio 9.5, semipaso 0.83 → flanco α = 55.4°. Par para saltar un diente con precarga axial N, dos caras: T = 2·N·r_m·tan(α + φ), con μ = 0.3 (estimado, φ = 16.7°): T = 58.7·N.
- Contra el peso propio: N ≥ 0.9 N. Contra 150 N en el frente (palanca 65): N ≥ **166 N**, que un M4 da con un par de apriete de unos 0.13 N·m (T = 0.2·d·N, coeficiente típico).
- Aplastamiento del M4 con 150 N: en las orejas 2 × 4 × 5 → 3.8 MPa; en la lengua 4 × 6.0 → 6.2 MPa. FS > 4 aun entre capas.

## 8. Presión a 1 m (0.0101 MPa), placas de Roark

σ = β·q·b²/t², y = α·q·b⁴/(E·t³) (Roark, 7.ª ed., tabla 11.4 caso 1a, bordes simplemente apoyados; coeficientes copiados de `cad/build.py`). La presión empuja hacia adentro: la tapa se apoya en la brida y la junta; los tornillos no la cargan.

| Placa | a × b mm | t mm | β | σ MPa | FS 45 / 22 | flecha mm |
|---|---|---|---|---|---|---|
| Tapa de la caja (campo de 5; bajo la ranura quedan 3.5) | 132 × 98 | 5 | 0.431 | 1.67 | 27 / 13 | 0.317 |
| Fondo de la caja | 132 × 98 | 4 | 0.431 | 2.60 | 17 / 8 | 0.619 |
| Pared larga | 132 × 46 | 4 | 0.699 | 0.93 | 48 / 24 | 0.054 |
| Pared corta | 98 × 46 | 4 | 0.624 | 0.83 | 54 / 27 | 0.047 |
| Pared de la cápsula | 38 × 38 | 4 | 0.287 | 0.26 | 173 / 84 | 0.009 |

Ventana de acrílico, placa circular simplemente apoyada en el hombro (radio libre 13, t 3, ν 0.37 típico): σ = 3(3+ν)·q·a²/(8t²) = **0.24 MPa**, frente a un acrílico típico de decenas de MPa (dato de material estimado, no medido).

## 9. Flotabilidad y estabilidad

Los números de flotabilidad son los de `fase_a.py`. En esta fase se corrigió su cálculo de estabilidad: el acero de las pletinas no sumaba a la masa total y las cápsulas iban a la altura del riel (ahora van con el eje bajo el riel, a 0 y a 90°).

Exigencias: peso aparente de +0.2 a +0.5 kgf, total en aire ≤ 3 kg.

| Relleno bandeja | Aro | Nodo sin acero g | Desplaza cm³ | Aparente sin acero g | Pletinas por lado | Aparente final g | En ventana | Total en aire g | ≤ 3 kg |
|---|---|---|---|---|---|---|---|---|---|
| 40 % | Ø100 | 1321 | 1578 | -296 | 3 | **+219** | sí | 1913 | sí |
| 40 % | Ø200 | 1432 | 1665 | -275 | 3 | **+241** | sí | 2024 | sí |
| 40 % | Ø300 | 1432 | 1665 | -275 | 3 | **+241** | sí | 2024 | sí |
| 40 % | Ø500 | 1543 | 1752 | -254 | 3 | **+262** | sí | 2135 | sí |
| 100 % | Ø100 | 1325 | 1578 | -292 | 3 | **+223** | sí | 1917 | sí |
| 100 % | Ø200 | 1436 | 1665 | -271 | 3 | **+245** | sí | 2028 | sí |
| 100 % | Ø300 | 1436 | 1665 | -271 | 3 | **+245** | sí | 2028 | sí |
| 100 % | Ø500 | 1547 | 1752 | -250 | 3 | **+266** | sí | 2139 | sí |

Totalmente sumergido no hay plano de flotación ni metacentro: el par adrizante al inclinarse un ángulo θ es B·BG·sen θ, con B el empuje y BG la distancia vertical del centro de masa (G) bajo el centro de empuje (B). BG > 0 quiere decir que no se voltea; el número que importa es BG. Las placas de acero ya están en G y en B.

| Aro | Inclinación de las cápsulas | z G mm | z B mm | BG mm | B N | Par adrizante a 10° N·mm |
|---|---|---|---|---|---|---|
| Ø100 | 0° | -25.7 | -7.1 | **18.6** | 16.6 | 54 |
| Ø100 | 90° | -31.5 | -13.8 | **17.7** | 16.6 | 51 |
| Ø200 | 0° | -26.6 | -8.9 | **17.7** | 17.5 | 54 |
| Ø200 | 90° | -32.1 | -15.2 | **16.9** | 17.5 | 51 |
| Ø300 | 0° | -26.6 | -8.9 | **17.7** | 17.5 | 54 |
| Ø300 | 90° | -32.1 | -15.2 | **16.9** | 17.5 | 51 |
| Ø500 | 0° | -27.4 | -10.5 | **16.9** | 18.4 | 54 |
| Ø500 | 90° | -32.6 | -16.5 | **16.1** | 18.4 | 51 |

Las cápsulas son casi neutras (128 g contra 128 cm³), así que bajarlas mueve G y B casi igual. El margen lo dan las pletinas bajo el riel contra el aire de la caja arriba.
