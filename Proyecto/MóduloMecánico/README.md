# Módulo mecánico: LanternGuard (prototipo a escala de laboratorio)

Carcasa estanca y soporte para las dos cámaras y la electrónica sumergida del concepto elegido (**Solución 1**): una barra prismática que se apoya sobre el aro superior de la linterna, con una caja central y una cápsula de cámara en cada extremo. La bisagra dentada fija el ángulo de cada cápsula.

El diseño es **CAD paramétrico en código** (CadQuery, Python). Todas las medidas están en un solo archivo, [`cad/params.py`](cad/params.py), en mm. Cada pieza se exporta a **STEP** (para Onshape) y **STL** (para imprimir).

![Ensamble](../../Recursos/Imágenes/LG_mec_ensamble_iso.png)

## Piezas

| Pieza | Archivo (`step/`, `stl/`) | Cant. | Material | Qué hace |
|---|---|---|---|---|
| P1 | `P1_caja_central_cuerpo` | 1 | PETG | Caja estanca: ESP32-WROOM-32U, microSD, MAX485, placa del JSN-SR04T. Sensor ultrasónico pasante por el fondo. Almohadillas en los extremos para atornillar los brazos |
| P2 | `P2_caja_central_tapa` | 1 | PETG | Tapa con ranura de junta tórica, prensaestopas PG9 del umbilical, **asa para guantes y ojo de anclaje** |
| P3 | `P3_brazo` | 2 | PETG | Brazo hueco 30 × 25 (conducto inundado del cable), horquilla dentada al final, apoyo con ranura para el aro de la linterna y ranura para correa |
| P4 rev. B | `P4revB_capsula_cuerpo` | 2 | PETG | Cápsula de cámara con asiento exterior para la ventana y prensaestopas PG7 en la pared inferior |
| P5 | `P5_capsula_tapa` | 2 | PETG | Tapa trasera con ranura de junta y **lengüeta dentada de la bisagra (fuera del sello)** |
| P6 | `P6_bisel_ventana` | 2 | PETG | Aro que retiene la ventana (3 tornillos M2 autorroscantes) |
| P7 | `P7_ventana` | 2 | Acrílico 3 mm | Disco Ø30 (comprado y cortado, no impreso) |
| P8 | `P8_marco_malla_prueba` | 1 | PETG | Marco 200 × 200 con malla de referencia de 20 mm para el banco de prueba |
| - | `ENSAMBLE_modulo` | - | - | Conjunto montado, cámaras a 40° |
| - | `ENSAMBLE_banco_prueba` | - | - | Conjunto + marco de malla a 150 mm frente a la cámara derecha |

Compras (no se modelan): cordón de junta tórica Ø2 mm (Buna-N o EPDM), 3 prensaestopas (2 PG7 y 1 PG9) con contratuerca, tornillería M3 × 12 con tuerca, 8 insertos térmicos M3, 2 pernos M4 × 20 con tuerca mariposa (bisagra, se ajusta con guantes) y una correa de velcro o abrazadera.

## Medidas principales

| Conjunto | Medida |
|---|---|
| Conjunto montado, cámaras a 40° (largo × ancho × alto) | 658 × 94 × 152 mm (horquilla a horquilla: 546 mm) |
| Caja central (exterior, sin brazos ni pestaña) | 142 × 76 × 60 mm + tapa de 6 y asa de 42 mm (pestaña 160 × 94) |
| Cavidad de la caja | 132 × 66 × 54 mm |
| Cápsula (exterior / cavidad) | 46 × 46 × 48 mm con pestaña de 64 × 64 / 38 × 38 × 42 mm |
| Bisagra | Disco Ø24, 36 dientes (paso 10°), horquilla 5 + 8.4 + 5, perno M4. Rango 0 a 90° |
| Masa estimada en aire | ≈ 0.97 kg (exigencia ≤ 3 kg) |

Los números verificados están en [`cad/reporte_verificacion.md`](cad/reporte_verificacion.md). El script los regenera cada vez.

## Decisiones de diseño (opción elegida y alternativa)

Cada alternativa se puede activar desde `params.py` o es un cambio pequeño en `parts.py`.

1. **Dónde va la bisagra.**
   - **Elegida: lengüeta en la tapa trasera, a la altura del eje óptico.** Con el eje sobre el techo de la cápsula, al inclinarla 90° el cuerpo gira hacia atrás y choca con el brazo (comprobado en el CAD). Con el eje detrás, la cápsula baja sin tocar nada en todo el rango de 0 a 90°: la holgura mínima medida es 8.5 mm. El eje queda **fuera del sello**, como pedía la documentación.
   - Alternativa: orejas sobre la cápsula (como la P4 original). Exige horquillas de unos 90 mm, demasiado largas y flexibles. Se descartó.
2. **Ventana.**
   - **Elegida: disco plano de acrílico de 3 mm en un asiento exterior.** La presión del agua la empuja contra el hombro, que tiene 2.8 mm. Va sellada con silicona neutra o RTV marino y retenida por el bisel P6. Es barata, fácil de cortar y de reemplazar.
   - Alternativa: domo (la lista de exigencias rev. 3 pide "ventana hemisférica truncada, R 25 a 150 mm" para corregir la refracción). Cuesta más (domo comprado o termoformado) y complica el sello. **Contradicción a resolver con el grupo.**
3. **Cierre de las tapas.**
   - **Elegida: sello de cara con cordón tórico de Ø2 mm.** La ranura de 2.6 × 1.5 mm da 25 % de compresión. El cierre es con tornillos M3 pasantes y tuerca: 4 en la cápsula y 6 en la caja.
   - Alternativa: insertos térmicos en la pestaña. Se ve más limpio, pero un inserto mal puesto agrieta la pestaña justo donde está el sello.
4. **Cómo se fija a la linterna.**
   - **Elegida: dos apoyos con ranura semicircular sobre el aro (Ø12, supuesto) y una correa de velcro o abrazadera.** No necesita herramientas y se pone con guantes en menos de 5 min (exigencia de Montaje).
   - Alternativa: abrazadera impresa con perilla. Es más rígida, pero agrega piezas y tiempo.
5. **Brazos.**
   - **Elegida: conductos inundados.** El cable pasa por dentro del brazo (como pide la rev. 3), pero el sello está en los prensaestopas de la caja y de la cápsula, no en el brazo.
   - Alternativa: brazo sellado. Duplica las superficies que hay que sellar.
6. **Escala.**
   - **Elegida: brazos de 140 mm para que cada pieza entre en una impresora de 220 × 220 mm.** Para campo, la rev. 3 pide más de 0.5 m: basta subir `ARM_LEN` en `params.py` o usar un tubo comercial.

## Supuestos (confirmar con el grupo)

- **Componentes:** el repo no tiene nuestro esquema electrónico. El PDF de `MóduloElectrónico/` es una plantilla de otro proyecto. Las medidas de los componentes son de datasheet y están marcadas en `params.py` con su grado de confianza. **Hay que medir las placas reales**, sobre todo la Arducam Mega con su lente y el ESP32 DevKit (los clones varían ±3 mm).
- **Electrónica de la caja:** se sigue el boceto de la Solución 1 (ESP32-WROOM-32U, JSN-SR04T, microSD y MAX485 en la caja; baterías en la boya). La rev. 3 pone las baterías en el módulo y dice "sin sensores".
- **Ventana:** se usa Ø30 en vez de Ø25.4 para dar margen al campo de visión del lente gran angular.
- **Bisagra:** ángulo de trabajo de 40° (debe ser múltiplo de 10°, el paso del dentado).
- **Varios:** diámetro del aro de la linterna Ø12 mm, cama de impresión 220 × 220 × 250 y distancia de prueba de 150 mm.
- **P4 rev. B:** la cavidad de la P4 original (46 × 34 × 22) no aloja la placa de 33 × 33 con su lente. Se agrandó a 38 × 38 × 42. **La simulación SimScale del Taller 01 ya no corresponde a esta geometría.**

## Verificación hecha (resumen de `cad/reporte_verificacion.md`)

- **Sólidos e impresión:** las 8 piezas son sólidos válidos y su STL es cerrado, de un solo cuerpo. Todas caben en la cama en la orientación de impresión indicada.
  - Lo que queda como voladizo son puentes cortos: el techo de la cavidad de la cápsula (38 mm), los agujeros de los prensaestopas, el aro del ojo del asa y los flancos de los dientes.
  - Las pestañas y las almohadillas tienen chaflanes a 45° para imprimir sin soporte.
- **Espesores:** todos los que quedan bajo un corte (asiento de ventana, ranuras de junta, insertos, pilotos) miden ≥ 1.2 mm. El más justo está entre la ranura y el tornillo de la cápsula: 1.25 mm.
- **Encaje:** las placas no tocan las paredes (holgura ≥ 1.59 mm) y las contratuercas de los PG7 no tocan las placas. La cámara cabe con 1 mm frente a la ventana.
- **Bisagra:** sin choque de 0 a 90° y los dientes engranan sin solaparse a 40°.
- **Presión a 15 m (0.15 MPa):** el cálculo de placa plana de Roark da un factor de seguridad entre 3.9 y 18 en todos los paneles (flecha máxima de 0.86 mm en la tapa de la caja). **Es una estimación, no un ensayo.**
- **Flotabilidad:** con 592 cm³ de aire sellado, el conjunto **flota** (≈ −0.3 kgf de peso aparente). Para cumplir 0.2 a 0.5 kgf hace falta un **lastre de unos 0.5 a 0.8 kg**, por ejemplo una placa de acero inoxidable bajo la caja. Hay que medirlo en un balde.

## Qué falta validar (no está probado)

- **Estanqueidad real.** El PETG impreso por FDM es poroso entre capas. Recomendado:
  - 100 % de relleno o al menos 5 perímetros en las paredes del sello;
  - capa de sellado (resina epoxi o barniz) por dentro;
  - prueba en balde 30 min con papel indicador dentro, y luego a la profundidad del tanque.
- **Resistencia a 0.15 MPa:** con anisotropía entre capas. Falta un ensayo (cámara de presión o inmersión progresiva). Las simulaciones del equipo usaron 50 kPa (≈ 5 m).
- **Tolerancias de impresión:** ajuste de la ventana en su asiento, prensaestopas en agujeros impresos (quizá roscar o usar contratuerca) y engrane de los dientes impresos.
- **Compresión de la junta:** está calculada (25 %), no medida. La planitud de la tapa impresa puede dejar fugas.
- **Lastre y equilibrio:** el centro de masa respecto al centro de empuje, para que la barra no gire.
- **Sensor ultrasónico:** el sellado del JSN-SR04T en el fondo de la caja (supuesto: junta con silicona o tuerca propia del sensor).
- **Planos:** los planos con cajetín UPCH se hacen en Onshape (pasos abajo); no se generan aquí.

## Cómo regenerar

```bash
pip install cadquery trimesh
cd Proyecto/MóduloMecánico/cad
python build.py        # ~1 min: STEP, STL y reporte_verificacion.md
```

Para cambiar una medida, edita `cad/params.py` y vuelve a correr `build.py`. El reporte dice si algo dejó de caber o de cumplir.

## Importar en Onshape (sin probar esta noche: verifica los nombres de los menús)

1. En Onshape, **Create → Document** (nombre: *LanternGuard módulo mecánico*).
2. Pestaña inferior **+ → Import** y elige los `step/P*.step`, o `step/ENSAMBLE_modulo.step` para traer todo junto. Unidades: **milímetros**.
3. Si importas el ensamble, Onshape crea un **Assembly** con cada pieza como sólido editable. Si importas pieza por pieza, crea un Assembly nuevo e **Insert** cada pieza.
4. Uniones (*mates*):
   - **Fastened** entre la caja (P1) y la tapa (P2), y entre cada brazo (P3) y su almohadilla.
   - **Revolute** en el eje M4 de cada bisagra (P5 ↔ P3), con límite de 0 a 90°.
5. Planos: **+ → Create Drawing** desde el Assembly.
   - Elige el formato con cajetín UPCH (o crea uno: universidad, curso, título, escala, lámina, autor, revisó, fecha, material, unidades mm, proyección del primer diedro).
   - Prioridad: plano de conjunto con globos y lista de piezas, y plano de la cápsula con un corte por la junta tórica.
6. Las piezas importadas no traen el historial paramétrico, pero se editan con *Move face* y *Offset face*. Para cambios grandes conviene editar `params.py` y reimportar.

## Imágenes

Renders hechos en Blender 5.2 (Mac mini), en `Recursos/Imágenes/`:
- `LG_mec_ensamble_iso.png` (proporción 2.6 : 1, para el hueco del ensamble en el PPT);
- `LG_mec_banco_prueba.png` (1.55 : 1, para la diapo de interacción);
- `LG_mec_P*.png`, uno por pieza.

## Plantilla anterior

Los dos STL de la estación meteorológica que había en esta carpeta eran de una plantilla, no de nuestro diseño. Se movieron a [`_plantilla/`](_plantilla/) sin borrarlos.
