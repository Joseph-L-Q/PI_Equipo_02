# Resumen del proyecto LanternGuard (Equipo 02, Proyecto Integrador, UPCH)

Examen escrito: mar 6/10/2026, 07:00-09:00 (sílabo, p. 12). Alcance: Unidades 1 y 2 hasta la semana 7 (sílabo, p. 2). Peso del examen: 20 % de la nota final (sílabo, p. 3).

Convención: **[V]** = dato dado por el equipo con fuente; **[S]** = supuesto o propuesta de estudio, no verificado en un documento oficial del equipo.

## 1. Problema (solo cifras verificadas)

En el cultivo de concha de abanico en linternas, el biofouling (organismos incrustados en la malla) reduce el flujo de agua y obliga a limpiar o recambiar las linternas.

| Dato | Fuente |
|---|---|
| 68 a 73 kg de biofouling por linterna en 2 a 3 meses (bahía Samanco) | Loayza y Tresierra 2014 (UNT) [V] |
| Recambio a los 30 días: -64.6 % de biofouling y +10.8 % de supervivencia | Loayza-Aguilar et al. 2025, J. World Aquac. Soc., e70054 [V] |
| Exportaciones peruanas de concha de abanico 2025: más de US$ 188 millones FOB | Gestión 2026, citando a Sanipes [V] |
| Evaluación manual: unos 30 min por 100 puntos; clasificación automática instantánea (piloto) | First et al. 2021 [V] |
| Faster R-CNN mejorado: mAP 93.14 % en moluscos incrustantes sobre jaulas marinas | Zhu et al. 2025 [V] |

**Errores que evitar:**
- La cifra "132 kg" del README del equipo y del Entregable 1 rev. 3 no está en ninguna fuente. No usarla.
- Las referencias [3] Lodeiros y García 2004 y [4] Samanco Marine Research Group 2025 del README no existen. No citarlas.
- Revista de Loayza y Tresierra 2014 verificada en el PDF del artículo: *Ciencia y Tecnología* (UNT), año 10, n.º 2, pp. 19-34. Otros documentos la citan como SCIÉNDO: es un error.

## 2. Objetivos [S]

Redacción de estudio a partir de la lista de exigencias rev. 3. Alinear con el texto oficial del entregable.
- **General:** diseñar un sistema que estime de forma remota el nivel de biofouling de una linterna de cultivo, para apoyar la decisión de limpieza o recambio.
- **Específicos:**
  - Estimar el % de área libre de malla frente a una imagen de referencia de malla limpia.
  - Clasificar el nivel de intervención.
  - Enviar una alerta remota.
  - Cumplir las exigencias mecánicas, eléctricas y de costo de la lista.
- **ODS:** 14 (meta 14.b, pescadores artesanales: acceso a recursos y mercados), 12 (meta 12.2, uso eficiente de recursos), 9 (meta 9.5, capacidad tecnológica) [V].

## 3. VDI 2206 aplicada fase por fase

La guía de 2004 usa el V-model como macrociclo (VDI 2206, p. 29-30). La versión de 2020 renombra las fases (Graessler y Hentze 2020, p. 318-320). Se indican ambos nombres.

| Fase 2004 / nombre 2020 | Qué se hizo en LanternGuard |
|---|---|
| **Requisitos** / requirements elicitation | Lista de exigencias rev. 3 [V]: profundidad 0 a 15 m (≈ 0.15 MPa), salinidad 35 g/L, tracción > 150 N, peso aparente en agua de mar 0.2 a 0.5 kgf, ≤ 3 kg en aire, carcasa PETG impresa con ventanas de acrílico o policarbonato, juntas tóricas y prensaestopas, montaje ≤ 5 min con guantes, costo de materiales ≤ S/ 1200, potencia activa 2 a 5 W, reposo < 0.15 W, MAE deseado < 15 % frente a un especialista. |
| **Diseño del sistema** / system architecture and design | Caja negra y estructura de funciones. Función global: estimar el % de malla libre, clasificar el nivel de intervención y alertar. Matriz morfológica con tres soluciones. Control en lazo abierto con decisión asistida; procesamiento fuera de la placa, en Python/OpenCV [V]. |
| **Diseño específico por dominio** / implementation of system elements | **Mecánico:** barra prismática sobre el aro superior, caja central estanca, dos cápsulas de cámara con bisagra dentada (0 a 90°, 36 dientes), PETG, simulación SimScale. **Electrónico:** ESP32, SPI, RS-485, reguladores. **Software:** adquisición, Python/OpenCV, alerta en app. |
| **Integración** / system integration and verification | Unir los tres módulos: caja central, umbilical RS-485 y caja en boya. |
| **Aseguramiento de propiedades** / verification y validation | Verificación: cada exigencia con una medida (análisis, inspección, demostración o prueba). Validación: que el sistema sirva al productor. |
| **Producto** / validation and transition | Madurez prevista [S]: modelo de laboratorio primero, luego modelo funcional. Un banco de pruebas con malla se prepara en el CAD. |

**Modelado y análisis** acompaña todas las fases (CAD, simulación, regresión). En el esquema 2020 es la franja exterior.

**Verificación y validación del proyecto [S]:**

| Exigencia | Medida de verificación propuesta |
|---|---|
| Tracción > 150 N | Prueba y análisis |
| ≤ 3 kg en aire | Inspección (balanza) |
| ≤ 5 min de montaje | Demostración |
| MAE < 15 % | Prueba con imágenes etiquetadas por un especialista |
| Costo ≤ S/ 1200 | Inspección de la lista de materiales |

La validación se hace contra la necesidad del productor.

## 4. Arquitectura: Solución 1 (concepto elegido)

Barra prismática apoyada en el aro superior de la linterna.

| Módulo | Contenido |
|---|---|
| **Mecánico** | Barra, caja central sellada, dos cápsulas de cámara en los extremos con bisagra dentada. Cables por el interior. Un cuerpo PETG impreso con ventanas de acrílico o policarbonato. |
| **Electrónico** | **Caja central:** ESP32-WROOM-32U, sensor ultrasónico de distancia JSN-SR04T, microSD, MAX485. **Cápsulas:** Arducam Mega 5 MP por SPI. **Umbilical:** RS-485. **Caja en boya:** ESP32-S3, LoRa SX1276, celdas 18650, regulador LM2596, panel solar. |
| **Software** | Captura de imagen, envío por LoRa, procesamiento fuera de la placa en Python/OpenCV, cálculo del % de malla libre, clasificación del nivel de intervención, alerta en la app. |

Flujo: cámara (SPI) -> ESP32 central -> RS-485 -> ESP32-S3 en boya -> LoRa -> procesamiento -> alerta en app.

**Por qué la Solución 1:** no hay radio bajo el agua, así que se usa cable hasta la boya. LoRa da largo alcance con bajo consumo. Es la opción más barata y liviana.

**Alternativas:**

| Solución | Núcleo | Enlace |
|---|---|---|
| 2 | Portenta H7 | Ethernet hasta la orilla |
| 3 | Raspberry Pi Zero 2 W | Wi-Fi y WhatsApp |

## 5. Inconsistencias que hay que saber explicar

| Tema | Qué pasa | Cómo explicarlo |
|---|---|---|
| Comunicaciones | Wi-Fi/WhatsApp en el Entregable 1 viejo, acústica en rev. 3, RS-485 + LoRa en el concepto elegido | Son iteraciones del diseño. La definitiva es RS-485 + LoRa; falta actualizar los documentos. |
| Presión de simulación | SimScale usó 50 kPa (≈ 5 m); la exigencia es 15 m (≈ 150 kPa) | La simulación actual no cubre el caso exigido. Hay que repetirla con ≈ 150 kPa. |
| Geometría heredada | El Entregable 1 en `main` conserva el cilindro de 220 × 130 | Es la versión vieja. La rev. 3 está en otra rama. |
| Biomasa | "132 kg" no existe en la fuente | Usar 68 a 73 kg. |

Además, el módulo mecánico tiene en preparación un CAD paramétrico (CadQuery, exportable a STEP/STL).
