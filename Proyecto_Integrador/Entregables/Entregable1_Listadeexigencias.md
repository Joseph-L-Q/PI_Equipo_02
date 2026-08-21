# Lista de Exigencias

| | |
|---|---|
| **Proyecto** | Sistema inteligente de inspección y determinación del nivel de bioincrustación en linternas de cultivo de concha de abanico (*Argopecten purpuratus*) |
| **Cliente** | Productores de cultivo suspendido de concha de abanico (bahías de Sechura, Samanco y afines) |
| **Metodología** | VDI 2206 — modelo en V (rama de requisitos) |
| **Edición** | Revisión 1 |
| **Fecha** | 20/08/2026 |
| **Elaborado por** | `[iniciales del equipo]` |
| **Revisado por** | `[   ]` |

**E** = Exigencia (de cumplimiento obligatorio)  ·  **D** = Deseo (mejora no obligatoria)

---

## Índice de requisitos

| # | Apartado | Tipo | Responsable |
|:--:|---|:--:|---|
| 1 | [Función principal](#1-funcion-principal) | E | `[   ]` |
| 2 | [Geometría](#2-geometria) | E | `[   ]` |
| 3 | [Cinemática](#3-cinematica) | E | `[   ]` |
| 4 | [Fuerzas](#4-fuerzas) | E | `[   ]` |
| 5 | [Energía](#5-energia) | E | `[   ]` |
| 6 | [Señales](#6-señales) | E | `[   ]` |
| 7 | [Control](#7-control) | E | `[   ]` |
| 8 | [Electrónica](#8-electronica) | E | `[   ]` |
| 9 | [Software](#9-software) | E | `[   ]` |
| 10 | [Software — desempeño objetivo](#10-software--desempeño-objetivo) | D | `[   ]` |
| 11 | [Comunicaciones](#11-comunicaciones) | E | `[   ]` |
| 12 | [Seguridad y marco legal](#12-seguridad-y-marco-legal) | E | `[   ]` |
| 13 | [Ergonomía](#13-ergonomia) | E | `[   ]` |
| 14 | [Fabricación](#14-fabricacion) | E | `[   ]` |
| 15 | [Montaje](#15-montaje) | E | `[   ]` |
| 16 | [Transporte](#16-transporte) | E | `[   ]` |
| 17 | [Uso](#17-uso) | E | `[   ]` |
| 18 | [Mantenimiento](#18-mantenimiento) | E | `[   ]` |
| 19 | [Mantenimiento — mejora deseable](#19-mantenimiento--mejora-deseable) | D | `[   ]` |
| 20 | [Costos](#20-costos) | E | `[   ]` |
| 21 | [Plazos](#21-plazos) | E | `[   ]` |

---

## 1. Función principal

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

Detectar y estimar el porcentaje de superficie cubierta por organismos de bioincrustación sobre las linternas de cultivo suspendido de *A. purpuratus*, mediante la adquisición y el procesamiento de imágenes submarinas, clasificar el resultado en un nivel de intervención y emitir una alerta que permita al productor decidir cuándo la linterna requiere recambio o limpieza.

El sistema **no** limpia la linterna ni identifica especies: entrega un indicador cuantitativo de cobertura para apoyar la decisión de mantenimiento.

> **Fuente.** Loayza y Tresierra (2014): el biofouling cubre el 100 % de las linternas evaluadas. Loayza-Aguilar et al. (2025): el recambio de linternas redujo el peso del biofouling en 64,6 % y mejoró la supervivencia en 10,8 %, con un ingreso neto adicional de 6 582,58 US$/ha.

## 2. Geometría

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El módulo debe alojarse junto a una linterna de cultivo estándar de 2 m de altura, 0,50 m de diámetro y 10 pisos, sin obstruir el flujo de agua ni las labores de faena.

- Envolvente cilíndrica de dimensiones máximas **220 mm (largo) × 130 mm (diámetro)**.
- Ventana de captura hemisférica truncada, radio de curvatura entre **25 y 150 mm**, para reducir la distorsión y conservar el campo angular de la cámara bajo el agua.
- Segunda ventana plana para la iluminación artificial.
- Distancia de trabajo cámara-linterna: **250 a 400 mm**.

> **Fuente.** Dimensiones de la linterna: Loayza y Tresierra (2014). Geometría óptica de la envolvente: Patente US 7,801,425 B2 (Fantone et al., 2010), que describe la ventana hemisférica truncada y la ventana plana de iluminación con difusor.

## 3. Cinemática

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El módulo debe poder recorrer verticalmente el eje de la linterna (2 m) para inspeccionar los 10 pisos, o bien reposicionarse manualmente por tramos.

- Velocidad relativa cámara-superficie durante la captura: **≤ 0,10 m/s**, para evitar arrastre de imagen.
- Ciclo completo de inspección de una linterna: **≤ 5 minutos**.

> **Fuente.** Captura de imágenes in situ sobre estructuras de cultivo: First et al. (2021); Zhu et al. (2025). Los valores de velocidad y tiempo de ciclo son decisión de diseño del equipo, a validar en el prototipo.

## 4. Fuerzas

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El módulo se fijará a la línea o al cabo de suspensión, **no a la linterna**, para no añadir carga a una estructura que ya soporta entre 68 y 132 kg de biofouling por linterna.

- Resistencia a fuerza manual de izado: **> 150 N**.
- Debe resistir el arrastre hidrodinámico de la corriente en condiciones normales de faena.
- Flotabilidad ligeramente negativa: peso aparente en agua entre **0,2 y 0,5 kgf**, para mantener posición estable sin tensar la línea.

> **Fuente.** Peso del biofouling por linterna: 68,04–73,42 kg (Loayza y Tresierra, 2014) y hasta 131,87 kg en el tratamiento sin recambio (Loayza-Aguilar et al., 2025). Condiciones de mar registradas durante la faena (escalas Beaufort y Douglas): Loayza-Aguilar et al. (2025), Tabla 5.

## 5. Energía

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

Alimentación autónoma mediante batería recargable de iones de litio con regulador de voltaje.

- Consumo en captura (cámara + iluminación LED + procesamiento): **2,0 a 5,0 W**.
- Consumo en reposo: **< 0,15 W**.
- Autonomía mínima: una jornada de faena (**8 h**) o **40 ciclos** de inspección, lo que ocurra primero.
- La recarga se realiza en superficie, sin abrir la envolvente estanca.

> **Fuente.** Rangos de consumo derivados de las hojas de datos de los componentes seleccionados (ESP32-CAM / Raspberry Pi Zero 2 W + módulo de iluminación) — a verificar con mediciones propias en el prototipo. Necesidad de iluminación artificial en inspección submarina: Zhu et al. (2025).

## 6. Señales

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

**Señales de entrada**

1. Señal de encendido, que activa la comprobación de cámara, iluminación y almacenamiento.
2. Imágenes RGB de la superficie de la linterna, capturadas de forma periódica o a demanda del operador.
3. Señal auxiliar de profundidad y temperatura del agua, para registrar las condiciones de la captura.

**Señales de salida**

4. Porcentaje estimado de superficie cubierta por bioincrustación.
5. Nivel de intervención asignado.
6. Señal de alerta cuando se supere el umbral configurado, con la imagen de evidencia asociada.

> **Fuente.** Adquisición y procesamiento de imágenes submarinas para cuantificar fouling: First et al. (2021); Zhu et al. (2025). Generación de información de abundancia por clase a partir de imágenes in situ: artículo de *Aquacultural Engineering* (art. 102682).

## 7. Control

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El sistema opera como **lazo abierto de medición con decisión asistida**: no existe actuador que modifique el estado de la linterna, por lo que el ciclo se cierra con la intervención del operador.

Secuencia: captura → mejora de la imagen → segmentación de las regiones incrustadas → cálculo del porcentaje de cobertura → comparación contra umbrales configurables → emisión de alerta.

Los umbrales deben ser **parámetros ajustables por el usuario** y no valores fijos: la propuesta inicial (bajo, medio, alto, crítico) es orientativa y deberá calibrarse contra observaciones de campo antes de proponerse como criterio operativo.

> **Fuente.** Arquitectura de detección y cuantificación: Zhu et al. (2025); artículo de *Aquacultural Engineering* (art. 102682). La decisión de mantenimiento como variable de manejo: Loayza-Aguilar et al. (2025).

## 8. Electrónica

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

- Unidad central de procesamiento basada en microcontrolador con módulo de cámara integrado (ESP32-CAM) o computadora de placa única (Raspberry Pi Zero 2 W), según la carga de cómputo que exija el algoritmo.
- Módulo de cámara RGB con resolución mínima de **1600 × 1200 px**.
- Iluminación LED blanca difusa, **obligatoria** por la atenuación de la luz en agua de mar.
- Almacenamiento local en microSD para conservar las imágenes de evidencia.
- Batería Li-ion con regulador y protección contra sobredescarga.
- Todos los pasamuros deben conservar la estanqueidad de la envolvente.

> **Fuente.** Necesidad de iluminación y mejora de imagen en captura submarina: Zhu et al. (2025). Viabilidad con cámara de bajo costo: First et al. (2021). Preservación de la estanqueidad en los elementos que atraviesan la envolvente: Patente US 7,801,425 B2 (Fantone et al., 2010).

## 9. Software

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

Desarrollo por etapas.

**Etapa 1 — obligatoria para el prototipo.** Preprocesamiento de la imagen para compensar la dominante de color del agua, seguido de segmentación de la superficie incrustada por características de color y textura, y cálculo del porcentaje de área cubierta.

**Etapa 2 — deseable.** Sustitución de la segmentación clásica por un modelo de aprendizaje profundo entrenado con un conjunto de imágenes propio.

Lenguaje Python con bibliotecas de visión por computadora. Interfaz de visualización en aplicación web o de escritorio que muestre la imagen, el porcentaje y el nivel asignado.

> **Fuente.** Enfoque por clustering y clasificación supervisada sobre imágenes de cámara económica: First et al. (2021). Mejora de imagen submarina previa a la detección (supuesto de mundo gris y MSRCR): Zhu et al. (2025). Segmentación multiclase y cuantificación por píxel: artículo de *Aquacultural Engineering* (art. 102682).

## 10. Software — desempeño objetivo

`D` · Deseo · Responsable: `[   ]` · Fecha: 20/08/2026

Se desea que la estimación de cobertura presente un **error absoluto medio inferior al 15 %** respecto de la evaluación visual de referencia realizada sobre las mismas imágenes.

> Se declara explícitamente que las métricas publicadas para sistemas industriales (precisión promedio de 94,27 % en jaulas de acuicultura; exactitud global de 86,7 % en infraestructura de salmón) corresponden a modelos entrenados con conjuntos de datos extensos y **no** constituyen una meta alcanzable para este prototipo académico.

> **Fuente.** Zhu et al. (2025); artículo de *Aquacultural Engineering* (art. 102682). El umbral del 15 % es una meta propia del equipo, no un valor tomado de la literatura.

## 11. Comunicaciones

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

La transmisión inalámbrica por radiofrecuencia **no es viable** a través del agua de mar.

Arquitectura: módulo sumergido conectado por cable estanco a una unidad de superficie, y desde ésta transmisión inalámbrica (Wi-Fi) al dispositivo del usuario. El enlace debe garantizar la integridad de las imágenes transmitidas.

La comunicación totalmente inalámbrica bajo el agua queda declarada como mejora de una eventual versión industrial, fuera del alcance de este prototipo.

> **Fuente.** Limitaciones físicas de la propagación de radiofrecuencia en medio marino y alternativas acústicas o cableadas: Akyildiz et al. (2005). Arquitectura de inspección con vehículo y enlace a superficie: Zhu et al. (2025).

## 12. Seguridad y marco legal

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

La actividad en la que se inserta el producto está regulada por el **Decreto Legislativo N.º 1195**, Ley General de Acuicultura, y su Reglamento (**D.S. N.º 003-2016-PRODUCE**, modificado por el **D.S. N.º 002-2020-PRODUCE**), que declaran la acuicultura actividad de interés nacional en armonía con la preservación del ambiente. La **Ley N.º 31666** promueve la tecnificación del sector. En materia sanitaria, el **D.S. N.º 07-2004-PRODUCE** (Norma Sanitaria de Moluscos Bivalvos Vivos), fiscalizado por SANIPES, condiciona la habilitación de las áreas de producción y, con ello, la exportación.

En consecuencia, el dispositivo:

1. No empleará biocidas, recubrimientos antiincrustantes tóxicos ni sustancias que puedan afectar la inocuidad del molusco.
2. No interferirá con la estructura de cultivo ni con las labores de faena.
3. Sus materiales serán inertes en agua de mar.
4. El operador conservará el registro de las inspecciones como evidencia de buenas prácticas de manejo.

> **Fuente.** D.L. N.º 1195; D.S. N.º 003-2016-PRODUCE; D.S. N.º 002-2020-PRODUCE; Ley N.º 31666; D.S. N.º 07-2004-PRODUCE; D.S. N.º 040-2001-PE.

## 13. Ergonomía

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

- Peso en aire **≤ 3,0 kg**, con centro de masa centrado respecto del eje longitudinal para evitar cabeceo durante la manipulación.
- Asa integrada y punto de anclaje para cabo de seguridad, de modo que pueda manipularse desde la embarcación con una sola mano y sin riesgo de pérdida.
- La instalación y el retiro deben ser posibles usando guantes de faena.

> **Fuente.** Asa integrada y anclaje para cabo de seguridad en envolventes submarinas: Patente US 7,801,425 B2 (Fantone et al., 2010). Condiciones de manipulación en faena de cultivo suspendido: FONDEPES, *Manual de cultivo de concha de abanico*.

## 14. Fabricación

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

La envolvente se fabricará con materiales disponibles en el mercado nacional:

- Cuerpo en tubo comercial de acrílico o PVC.
- Tapas y soportes impresos en 3D en **PETG** (preferido por su resistencia a la humedad frente al PLA).
- Sellado mediante juntas tóricas normalizadas.
- Grado de protección mínimo equivalente a **IP68** según la norma IEC 60529.
- Todos los componentes electrónicos serán de adquisición local o de importación regular.

> **Fuente.** Grado de protección de envolventes: IEC 60529 (Código IP). Construcción de envolvente estanca en dos secciones con junta tórica y cierre por palanca: Patente US 7,801,425 B2 (Fantone et al., 2010).

## 15. Montaje

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El módulo se instalará sobre la línea de cultivo o el cabo de suspensión mediante abrazaderas de apriete manual, sin herramientas especiales y en un tiempo **≤ 5 minutos** por unidad.

El sistema de sujeción debe admitir cabos de diámetro variable y permitir orientar la cámara hacia la superficie de la linterna. No debe requerir la extracción de la linterna del agua para su instalación.

> **Fuente.** Estructura del cultivo suspendido (líneas, boyas, linternas): FONDEPES, *Manual de cultivo de concha de abanico*; Avendaño et al. (2001). Configuración de alojamiento sumergible con sensores y controlador integrados: Patente US 8,272,262 B2, *Underwater sensor apparatus*.

## 16. Transporte

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El equipo debe transportarse en caja rígida con alojamiento acolchado, con peso total **< 5 kg**, resistiendo la manipulación manual y el traslado terrestre y en embarcación menor.

La ventana óptica debe protegerse con tapa o cubierta durante el traslado para evitar rayaduras que degraden la calidad de imagen.

> **Fuente.** Protección de la ventana óptica y de la envolvente durante el traslado: Patente US 7,801,425 B2 (Fantone et al., 2010). Los valores de peso y las condiciones de embalaje son decisión del equipo.

## 17. Uso

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El dispositivo operará sumergido en agua de mar, en concesiones de cultivo suspendido:

- Profundidad de trabajo: **0 a 15 m**.
- Salinidad del orden de **35 g/L**.
- Debe mantener su desempeño ante la variabilidad de temperatura, oxígeno disuelto y sólidos suspendidos propia de las bahías de cultivo, y ante la turbidez, que es la principal limitante de la calidad de imagen.
- Se establecerá una **condición mínima de visibilidad** por debajo de la cual el sistema debe declarar la medición como no válida, en lugar de entregar un valor poco confiable.

> **Fuente.** Parámetros oceanográficos registrados en el cultivo (temperatura, oxígeno disuelto y sólidos totales en suspensión): Loayza-Aguilar et al. (2025), Figura 6; Tapia-Ugaz et al. (2022). Presencia permanente de fouling sobre las estructuras: Loayza y Tresierra (2014).

## 18. Mantenimiento

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

La ventana óptica del propio módulo sufrirá bioincrustación, igual que cualquier superficie sumergida.

- Acceso directo para su limpieza manual **sin desarmar la envolvente**.
- Rutina de limpieza previa a cada jornada de inspección.
- Las juntas tóricas se inspeccionarán y lubricarán antes de cada inmersión, y se sustituirán ante cualquier signo de deterioro.
- La batería y el almacenamiento serán accesibles mediante una única tapa desmontable.

> **Fuente.** El biofouling afecta a toda superficie artificial sumergida y condiciona el intervalo de mantenimiento de los sensores: Fitridge et al. (2012); Patente US 5,889,209 A (Piedrahita y Wong, 1999), que documenta la incrustación de superficies ópticas sumergidas —incluidas ventanas de observación y de cámaras— y su eliminación por ultrasonido.

## 19. Mantenimiento — mejora deseable

`D` · Deseo · Responsable: `[   ]` · Fecha: 20/08/2026

Se desea incorporar un mecanismo de **limpieza automática de la ventana óptica** que evite la intervención manual entre inspecciones.

La alternativa documentada consiste en un transductor ultrasónico adyacente a la superficie óptica, activado por intervalos, con frecuencias del orden de **10 a 100 kHz** y pulsos de algunas decenas de segundos separados por intervalos de minutos a un par de horas.

> **Fuente.** Patente US 5,889,209 A, *Method and apparatus for preventing biofouling of aquatic sensors* (Piedrahita y Wong, 1999): reivindica la activación del transductor durante 5 a 90 segundos, a intervalos de 5 a 120 minutos, en el rango de 10 a 100 kHz.

## 20. Costos

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El costo objetivo del prototipo, considerando unidad de procesamiento, módulo de cámara, iluminación, batería y regulador, envolvente y elementos de sellado, se sitúa entre **S/ 450 y S/ 900** por unidad, a los que se suman insumos de impresión 3D y pruebas.

> Este rango es una **estimación preliminar del equipo** y deberá sustituirse por cotizaciones reales del mercado local antes de la revisión final del documento.

> **Fuente.** Estimación propia del equipo (pendiente de cotización). Justificación económica del producto: el manejo del biofouling representó un ingreso neto adicional de 6 582,58 US$/ha en el estudio de Loayza-Aguilar et al. (2025).

## 21. Plazos

`E` · Exigencia · Responsable: `[   ]` · Fecha: 20/08/2026

El proyecto se desarrollará según el cronograma del curso, con hitos alineados a la rama del modelo en V: definición de requisitos, diseño del sistema, diseño de dominios específicos, integración, verificación y validación en tanque.

Fechas y horas de dedicación: `[completar por el equipo]`.

> **Fuente.** Decisión propia del equipo; no requiere fuente externa.

---

## Nota metodológica (VDI 2206)

La Lista de Exigencias constituye la entrada de la rama izquierda del modelo en V: los requisitos aquí definidos gobiernan el diseño del sistema, se descomponen en los dominios mecánico, electrónico y de software, y se convierten en los criterios de verificación al cerrar la V. Por ello cada exigencia se ha redactado de forma verificable y trazable a una fuente.

Se distinguen exigencias (E) de deseos (D), conforme a la práctica del diseño sistemático: una exigencia debe cumplirse para que la solución sea aceptable; un deseo mejora la solución pero no la condiciona.

## Diferencias respecto de la lista de exigencias anterior

1. **El sistema de control ya no es de lazo cerrado.** En el proyecto de la refrigeradora existía una lógica de umbral sobre una variable continua; aquí no hay actuador que modifique el estado de la linterna, de modo que el lazo se cierra con la decisión del operador. Declararlo como lazo cerrado sería incorrecto.
2. **El marco legal cambia por completo:** la Ley N.º 29571 y la Ley N.º 30988 no aplican a este proyecto. El marco pertinente es el acuícola-sanitario.
3. **Aparece una exigencia que el proyecto anterior no tenía:** el propio dispositivo sufre bioincrustación. Es el riesgo técnico más específico de este producto.
4. **Se declara explícitamente el límite de alcance:** el sistema estima cobertura, no identifica especies.

---

## Bibliografía

### Patentes (formato Vancouver, el mismo de la lista anterior)

- **GEOMETRÍA, ERGONOMÍA, FABRICACIÓN, TRANSPORTE:** Fantone SJ, Fantone SD, Nielsen PM. Underwater adaptive camera housing [Internet]. Patente US 7,801,425 B2. Estados Unidos: Optikos Corporation; 21 de septiembre de 2010 [citado 20 de agosto de 2026]. Disponible en: <https://patents.google.com/patent/US7801425B2/en>
- **MONTAJE:** Underwater sensor apparatus [Internet]. Patente US 8,272,262 B2 [citado 20 de agosto de 2026]. Disponible en: <https://patents.google.com/patent/US8272262B2/en>
- **MANTENIMIENTO:** Piedrahita RH, Wong KBH. Method and apparatus for preventing biofouling of aquatic sensors [Internet]. Patente US 5,889,209 A. Estados Unidos: Regents of the University of California; 30 de marzo de 1999 [citado 20 de agosto de 2026]. Disponible en: <https://patents.google.com/patent/US5889209A/en>
- **USO:** Sistema submarino para labores de acuicultura [Internet]. Patente ES 2729816 B2. España [citado 20 de agosto de 2026]. Disponible en: <https://patents.google.com/patent/ES2729816B2/en>

### Referencias científicas y técnicas (APA 7)

- Avendaño, M., Cantillánez, M., Le Pennec, M., Lodeiros, C., & Freites, L. (2001). Cultivo de pectínidos iberoamericanos en suspensión. En A. N. Maeda-Martínez (Ed.), *Los moluscos pectínidos de Iberoamérica: Ciencia y acuicultura* (pp. 193–211). Limusa.
- Akyildiz, I. F., Pompili, D., & Melodia, T. (2005). Underwater acoustic sensor networks: Research challenges. *Ad Hoc Networks, 3*(3), 257–279. https://doi.org/10.1016/j.adhoc.2005.01.004 `[confirmar ficha en el DOI]`
- First, M. R., Riley, S. C., Islam, K. A., Hill, V., Li, J., Zimmerman, R. C., & Drake, L. A. (2021). Rapid quantification of biofouling with an inexpensive, underwater camera and image analysis. *Management of Biological Invasions, 12*(3), 599–617. https://doi.org/10.3391/mbi.2021.12.3.06
- Fitridge, I., Dempster, T., Guenther, J., & de Nys, R. (2012). The impact and control of biofouling in marine aquaculture: A review. *Biofouling, 28*(7), 649–669. https://doi.org/10.1080/08927014.2012.700478
- Fondo Nacional de Desarrollo Pesquero. *Manual de cultivo de concha de abanico*. FONDEPES. `[completar año y enlace oficial]`
- Loayza, R., & Tresierra, Á. (2014). Variación del "biofouling" en linternas de cultivo de "concha de abanico" *Argopecten purpuratus* en bahía Samanco, Ancash, Perú. *SCIÉNDO INGENIUM, 10*(2), 19–34. https://revistas.unitru.edu.pe/index.php/PGM/article/view/567
- Loayza-Aguilar, R. E., Carhuapoma-Garay, J., Ramos-Falla, K., Saldaña-Rojas, G. B., Huamancondor-Paz, Y. P., Campoverde-Vigo, L., & Olivos-Ramirez, G. E. (2024). Epibionts affect the growth and survival of *Argopecten purpuratus* (Lamarck, 1819) cultivated in Samanco Bay, Peru. *Aquaculture, 578*, 740042. https://doi.org/10.1016/j.aquaculture.2023.740042
- Loayza-Aguilar, R. E., Saldaña-Rojas, G. B., Merino, F., & Olivos-Ramirez, G. E. (2025). Biofouling reduction by lantern nets exchange and its relationship with production and survival of *Argopecten purpuratus* in Samanco Bay, Peru. *Journal of the World Aquaculture Society, 56*(5), e70054. https://doi.org/10.1111/jwas.70054
- Tapia-Ugaz, L. `[completar autores]`. (2022). Caracterización biológica de los organismos incrustantes en sistemas de cultivo suspendido de *Argopecten purpuratus* en bahía Samanco (Ancash, Perú). *Caldasia*. https://revistas.unal.edu.co/index.php/cal/article/view/91786
- Zhu, P., Li, H., Chen, J., & Guo, C. (2025). Research on fouling shellfish on marine aquaculture cages detection technology based on an improved symmetric Faster R-CNN detection algorithm. *Symmetry, 17*(12), 2107. https://doi.org/10.3390/sym17122107
- `[Completar autores]`. (2025). Pixel-level quantification of biofouling taxa associated with salmon aquaculture infrastructure using deep learning. *Aquacultural Engineering, 113*, 102682. https://doi.org/10.1016/j.aquaeng.2025.102682

### Normas

- Comisión Electrotécnica Internacional. (2013). *IEC 60529: Grados de protección proporcionados por las envolventes (Código IP)*.
- Verein Deutscher Ingenieure. (2021). *VDI 2206: Development of mechatronic and cyber-physical systems*. VDI.

---

## Pendientes antes de la entrega

- [ ] Completar las fichas marcadas `[completar]` o `[confirmar]`: autores del artículo de *Aquacultural Engineering*, autores de Tapia-Ugaz et al., ficha del manual de FONDEPES, ficha de Akyildiz et al. y datos de la patente ES 2729816 B2.
- [ ] Sustituir el rango de costos por cotizaciones reales del mercado local.
- [ ] Consultar la Figura 6 de Loayza-Aguilar et al. (2025) y sustituir la descripción cualitativa de las condiciones oceanográficas por los rangos numéricos publicados.
- [ ] Asignar responsables por apartado y fijar las fechas del cronograma.
- [ ] Unificar el estilo de citación: la lista anterior mezcla Vancouver para patentes con autor-año para artículos. Declarar qué estilo rige cada bloque, o unificar todo en APA 7.
