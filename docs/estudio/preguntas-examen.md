# 30 preguntas probables de examen (Proyecto Integrador, Equipo 02, LanternGuard)

Examen: mar 6/10/2026. Unidades 1 y 2 hasta la semana 7.

**Convención de citas**
- PDF: página del PDF. Para `VDI 2206.pdf` coincide con la página impresa.
- Artículo del V-model 2020 (`The new V-Model of VDI 2206 and its validation.pdf`): página impresa, con la página del PDF entre paréntesis. Se escribe "Graessler 2020, p. 319 (PDF 8)".
- PPTX: posición de la diapositiva en el archivo. `Intro a IA.pptx` imprime números unos 2 más altos que la posición (la posición 60 muestra "62").
- Clase 2.pdf trata del perceptrón multicapa y backpropagation. Clase4.pdf trata de innovación, TRL y VDI.
- **(conocimiento general)** = no está en los archivos del curso.
- **[S]** = supuesto o propuesta de estudio sobre el proyecto, no verificado en un documento del equipo.

---

## A. VDI 2206

**1. ¿Qué es la mecatrónica y cuál es la estructura básica de un sistema mecatrónico?**
Integración sinérgica de ingeniería mecánica, eléctrica/electrónica y tecnología de la información. Un sistema mecatrónico tiene sistema base, sensores, actores y procesamiento de información, más el entorno. Entre ellos fluyen material, energía e información. El término lo acuñó Ko Kikuchi (Yaskawa) en 1969.
*Fuente: VDI 2206.pdf, p. 9-10, 14-16.*
*En LanternGuard [S]: sistema base = barra y linterna; sensores = cámaras y sensor de distancia; procesamiento = ESP32 y Python. El control es de lazo abierto con decisión asistida, así que no hay actor mecánico: la salida es información (la alerta).*

**2. ¿Qué es el micro-ciclo de VDI 2206 y cuáles son sus pasos?**
Ciclo general de resolución de problemas, de nivel micro, que se encadena y anida para planificar cualquier tarea. Pasos: (1) análisis de la situación o adopción de una meta; (2) análisis y síntesis, alternando para generar variantes; (3) análisis y evaluación de las variantes con criterios definidos; (4) decisión; (5) planificación del procedimiento siguiente o aprendizaje.
*Fuente: VDI 2206.pdf, p. 26-29.*

**3. Describe el V-model de VDI 2206:2004 como macrociclo.**
Describe la secuencia lógica de la entrega: requisitos, diseño del sistema (concepto interdisciplinario, función global dividida en subfunciones), diseño específico por dominio, integración del sistema y aseguramiento de propiedades. El modelado y análisis acompaña todo. El resultado es el producto, entendido como madurez creciente: modelo de laboratorio, modelo funcional, producto de preserie. Un producto complejo requiere varios macrociclos.
*Fuente: VDI 2206.pdf, p. 29-31. Origen en software: Graessler 2020, p. 315 (PDF 4).*

**4. ¿Qué cambia en el nuevo V-model (2020)?**
Tiene tres franjas: el núcleo (actividades centrales), los requisitos (elicitación y gestión continuas, no una caja de entrada) y el modelado y análisis (envuelve todo el V). Añade puntos de control. Representa la secuencia lógica de tareas, no una secuencia temporal, así que sirve para proyectos clásicos y ágiles. Los requisitos se escriben primero como necesidades de los interesados y luego como requisitos del sistema.
*Fuente: Graessler 2020, p. 317-319 (PDF 6-8); Clase4.pdf, p. 22-23.*

**5. Diferencia entre verificación y validación.**
Verificación: ¿se construye correctamente el producto? Comprueba que lo realizado coincide con la especificación, en el mismo nivel de sistema. Validación: ¿se construye el producto correcto? Comprueba que sirve al uso previsto y a las expectativas del usuario. En el V-model 2020, la verificación es una flecha horizontal y la validación sube al nivel de las necesidades de los interesados.
*Fuente: VDI 2206.pdf, p. 38-39; Graessler 2020, p. 317 (PDF 6) y p. 320 (PDF 9).*
*Ejemplo [S]: verificar que la carcasa soporta > 150 N; validar que el productor puede decidir cuándo limpiar con la alerta.*

**6. ¿Qué métodos de aseguramiento de propiedades existen?**
Cuatro: análisis teórico (cálculo, modelado, simulación), inspección (propiedades visibles o medibles), demostración (prueba cualitativa con poca instrumentación) y ensayo (prueba cuantitativa en entorno definido). También hay experimentos virtuales, reales o híbridos (hardware-in-the-loop). La integración al nivel superior no debe empezar hasta verificar el nivel inicial.
*Fuente: Graessler 2020, p. 320 (PDF 9); VDI 2206.pdf, p. 39-40.*
*Ejemplo [S]: peso ≤ 3 kg = inspección; montaje ≤ 5 min con guantes = demostración; MAE < 15 % = ensayo.*

**7. ¿Qué tipos de integración distingue VDI 2206? Ubica LanternGuard.**
(a) De componentes distribuidos: sensores y actuadores unidos por señales y energía con cables y conectores; permite componentes en serie, pero riesgo de contactos, roturas y cortocircuitos en ambientes duros. (b) Modular: módulos con interfaces unificadas. (c) Espacial: todo en una sola carcasa; menor volumen y menos interfaces, pero calor, vibraciones y ruido interfieren.
*Fuente: VDI 2206.pdf, p. 35-36.*
*En LanternGuard [S]: la caja central es integración espacial; el umbilical RS-485 hasta la boya es integración distribuida, y por eso sus conectores y prensaestopas son un punto de riesgo.*

## B. Herramientas de diseño del sistema

**8. ¿Qué es una lista de exigencias y qué significan E y D?**
Documento que traduce el encargo en requisitos verificables y es la medida contra la que se juzga el producto. E = exigencia (obligatoria); D = deseo (deseable, se valora pero no se exige) (conocimiento general). Se organiza por categorías: función principal, geometría, cinemática, fuerzas, energía, materia, señales, control. La guía pide reducirla a enunciados esenciales y formularlos sin imponer solución. Calidad: completitud, claridad, consistencia y corrección.
*Fuente: INFORME TÉCNICO Lista de exigencias y plan de trabajo.docx (tabla, columna "Deseo o Exigencia"); VDI 2206.pdf, p. 32; Graessler 2020, p. 319 (PDF 8).*
*LanternGuard (rev. 3): 0 a 15 m, > 150 N, ≤ 3 kg en aire, ≤ 5 min de montaje, costo ≤ S/ 1200, MAE deseado < 15 %. Nótese que "deseado" es un deseo (D), no una exigencia.*

**9. ¿Qué es la caja negra y la estructura de funciones?**
La caja negra expresa la función global solo con entradas y salidas (flujos de energía, señales y materia), sin decir cómo. Luego se abre en subfunciones unidas por flujos de material, energía e información, y se refina hasta poder asignar principios de solución.
*Fuente: Dialnet-AnalisisDeFuncionYMatrizMorfologica...pdf, p. 3-4 (figs. 1 y 2); VDI 2206.pdf, p. 32-33.*
*LanternGuard [S]:*
- *Entradas: linterna con biofouling (materia), energía, comando de captura (señal).*
- *Salidas: % de malla libre, nivel de intervención, alerta.*
- *Subfunciones: capturar imagen, medir distancia, almacenar, transmitir, alimentar, procesar, alertar.*

**10. ¿Qué es la matriz morfológica y cuántas variantes globales genera?**
Matriz con las subfunciones en filas y las alternativas de solución en columnas. Se elige una solución por subfunción y se combinan. Con m_i soluciones para la subfunción i hay N = m1 × m2 × ... × mn variantes teóricas, que las incompatibilidades reducen mucho. Se supone que un problema complejo se divide en subproblemas y la solución global es combinación de soluciones parciales.
*Fuente: VDI 2206.pdf, p. 37; Dialnet-AnalisisDeFuncion...pdf, p. 5-6 (tabla 1); Evaluacion_Matriz_Morfologica_VDI2206_Ejemplo.xlsx, hoja "Matriz".*
*Ejemplo del curso: 6 subfunciones con 3 a 4 alternativas cada una, sobre dosificación de fluido. No es nuestro proyecto.*

**11. ¿Cómo se elige entre conceptos? Pugh y evaluación ponderada.**
Ponderada: criterios con pesos que suman 1.0, puntajes de 1 a 5 por concepto, total = suma(peso × puntaje). Pugh: se compara cada concepto con uno base usando +, 0 o -, y se suman. Luego se elige el concepto líder.
*Fuente: Evaluacion_Matriz_Morfologica_VDI2206_Ejemplo.xlsx, hojas "Criterios", "Puntajes", "Pugh", "Ponderado".*
*LanternGuard [S]: criterios naturales son costo, peso, consumo, robustez bajo agua y complejidad. Eligió la Solución 1 sobre la 2 (Portenta H7 + Ethernet) y la 3 (Raspberry Pi Zero 2 W + Wi-Fi + WhatsApp).*

**12. ¿Qué son principio de funcionamiento, estructura de funcionamiento y estructura constructiva? ¿Qué es la partición por dominios?**
Principio de funcionamiento: relación entre efecto físico y rasgos geométricos y de material que cumple una subfunción. Estructura de funcionamiento: principios unidos por flujos. Estructura constructiva: añade las relaciones espaciales, de fabricación y montaje. La partición reparte la función entre los dominios mecánico, electrónico y de software, cada uno con su metodología. Una carcasa cumple varias subfunciones a la vez (sujetar, sellar, soportar).
*Fuente: VDI 2206.pdf, p. 30, 33-35.*

## C. Módulo mecánico

**13. ¿Por qué PETG impreso para la carcasa? ¿Qué dice el curso de los materiales y de FDM?**
El laboratorio ofrece impresoras Ender 3-S1 y Bambu P1S y materiales PLA, ABS, PETG y TPU. La elección de PETG para el proyecto es una exigencia de la lista rev. 3. Su justificación típica (conocimiento general): resiste mejor el agua y es más tenaz que el PLA, que es más frágil y sensible a humedad y calor; el ABS exige cámara cerrada y deforma más. El sellado depende de juntas tóricas y prensaestopas, no del plástico solo. FDM deja capas porosas y anisótropas: la orientación de impresión y el relleno cambian la resistencia.
*Fuente: Mecánica.pptx, diap. 15 (orientación y relleno), 17 (equipamiento y materiales).*

**14. ¿Qué pautas de diseño 3D se usan para piezas impresas?**
Nervaduras (rib), chaflanes (chamfer, 45° típico), escuadras (gusset), espesor constante, redondeos (fillet) y esquinas redondeadas. Todas reducen concentraciones de esfuerzo, deformación o contracción.
*Fuente: Mecánica.pptx, diap. 6-7.*

**15. ¿Qué tipos de esfuerzo y modos de falla existen? ¿Qué es el factor de seguridad?**
Esfuerzos: tracción, compresión, flexión, torsión y cortante. Modos de falla: fractura por esfuerzo mayor a la resistencia, fatiga por cargas fluctuantes, fractura frágil, y deformación por temperatura alta. Factor de seguridad = resistencia del material / esfuerzo máximo calculado (conocimiento general); debe ser mayor que 1 con margen. Simulación por elementos finitos (SimScale): importar la geometría, simulación estática, contactos, malla refinada en zonas críticas, material, apoyos y cargas, y revisión de esfuerzos.
*Fuente: Mecánica.pptx, diap. 9 (esfuerzos y fallas), 10-12 (procedimiento de elementos finitos).*
*Proyecto: la exigencia de tracción es > 150 N. El equipo corrió simulaciones a 50 kPa, no a la presión de la exigencia (ver pregunta 29).*

**16. ¿Qué presión soporta el equipo a 15 m? Calcula.**
Presión hidrostática p = ρ·g·h (conocimiento general).
- Con ρ ≈ 1025 kg/m³ de agua de mar, g = 9.81 m/s² y h = 15 m: p ≈ 1025 × 9.81 × 15 ≈ 150 800 Pa ≈ 151 kPa ≈ 0.15 MPa (presión manométrica).
- La presión absoluta suma la atmosférica (≈ 101 kPa), unos 252 kPa.
- A 5 m: p ≈ 50 kPa, que es el valor usado en SimScale.
- Nota: la salinidad exigida es 35 g/L; la densidad de 1025 kg/m³ es un valor típico, no un dato del proyecto.

## D. Módulo electrónico

**17. ¿Qué es un ESP32 y qué papel cumple? ¿Qué hace el ADC?**
Microcontrolador con Wi-Fi y Bluetooth, usado en el taller (ESP32 Dev Kit 1). El microcontrolador procesa la señal del sensor; el ADC convierte la señal analógica en digital. Programación con `analogRead` y salida serie a 115200.
*Fuente: Taller Internet of Things (IoT).pdf, p. 3-7.*
Con 12 bits y 3.3 V (conocimiento general): V = ADC × 3.3 / 4095.
*Proyecto: ESP32-WROOM-32U (caja central) y ESP32-S3 (boya).*

**18. Compara SPI, I2C, UART y RS-485.**
- Los cuatro aparecen como interfaces y medios en la arquitectura de referencia.
  *Fuente: Teoría IoT.pdf, p. 9-10.*
- Detalle (conocimiento general):

| Bus | Hilos | Características |
|---|---|---|
| SPI | MOSI, MISO, SCK y CS por dispositivo | Rápido, full-duplex, maestro-esclavo |
| I2C | SDA y SCL | Direcciones de 7 bits, varios dispositivos en 2 hilos, más lento |
| UART | TX y RX | Asíncrono, punto a punto |
| RS-485 | Par diferencial A/B | Half-duplex, largo alcance, inmune a ruido; el MAX485 convierte UART a señal diferencial |

*Proyecto: cámaras Arducam Mega y microSD por SPI; umbilical hasta la boya por RS-485 con MAX485. El RS-485 se eligió por la distancia y el ruido en el cable [S].*

**19. ¿Para qué sirven los reguladores y cuál usa el proyecto?**
Convierten la tensión de la batería en la tensión estable que piden los circuitos. Lineal: simple, ruidoso, disipa la diferencia en calor. Conmutado (buck): eficiente, más ruido de conmutación (conocimiento general). El LM2596 es un regulador reductor conmutado (conocimiento general). Con celdas 18650 (nominal 3.7 V) y panel solar, la eficiencia pesa porque el reposo exige < 0.15 W y la potencia activa es de 2 a 5 W (requisitos del proyecto).

## E. Módulo de software y calidad

**20. ¿Qué es la calidad de software y qué factores propone el modelo de McCall?**
Capacidad del software de satisfacer necesidades y expectativas del usuario; se mide, y lo que se certifica son los procedimientos (ISO 9000, CMMI), no el software. McCall (1977) agrupa factores en tres capacidades:
- Operación: corrección, confiabilidad, usabilidad, integridad, eficiencia.
- Transición: portabilidad, reusabilidad, interoperabilidad.
- Revisión: mantenimiento, flexibilidad, facilidad de prueba.

*Fuente: Clase 4 - Sofware.pptx, diap. 2, 4, 9-13.*

**21. ¿Qué son ISO/IEC 12207, SPICE, CMMI y Agile? ¿Qué es TRL?**
- ISO/IEC 12207: ciclo de vida del software.
- SPICE (ISO/IEC 15504): evaluación de la capacidad de los procesos.
- CMMI: cinco niveles de madurez (1 Inicial, 2 Gestionado, 3 Definido, 4 Gestionado cuantitativamente, 5 Optimización).
- Agile: entrega iterativa e incremental.

*Fuente: Clase 4 - Sofware.pptx, diap. 17-20.*
TRL = nivel de madurez tecnológica, de 1 a 9 (Clase4.pdf, p. 18); es el tema de la Unidad 3, fuera de este examen.

## F. IoT

**22. ¿Qué es MQTT y por qué se usa en IoT?**
Protocolo máquina a máquina de publicación/suscripción extremadamente ligero. Útil donde el ancho de banda o la huella de código importan. Ventajas: paquetes mínimos, orientado a eventos, bajo consumo, un cliente a muchos, seguridad y escalabilidad a cientos de miles de clientes. Puertos habituales: 1883 (sin cifrar) y 8883 (TLS).
*Fuente: Teoría IoT.pdf, p. 18, 20, 27.*

**23. Explica broker, topic, publish, subscribe y QoS.**
- **Topic:** ruta jerárquica que direcciona una publicación o suscripción. Ejemplo del curso: `edificio1/planta3/sala1/raspberry0/temperatura`; `#` es comodín de varios niveles (comodín: conocimiento general).
- **Publish:** enviar un mensaje a un topic. **Subscribe:** recibir los mensajes de un topic.
- **Broker:** recibe mensajes, los filtra por topic, los distribuye a los suscriptores, gestiona conexiones, seguridad y QoS.
- **QoS:** como máximo una vez, al menos una vez, exactamente una vez. Equivalen a QoS 0, 1 y 2 (numeración: conocimiento general).
- **Brokers:** EMQX, Mosquitto, HiveMQ, AWS IoT Core, Azure IoT Hub. **Node-RED** conecta flujos con un broker.

*Fuente: Teoría IoT.pdf, p. 19, 21, 24-26, 29-32.*

**24. Describe la arquitectura IoT y las plataformas en la nube del curso.**
- **Referencia de 7 capas:**
  1. física (sensores y actuadores)
  2. adquisición (acondicionamiento, ADC, interfaz GPIO/UART/I2C/SPI/1-Wire)
  3. edge (microcontrolador)
  4. comunicación (Wi-Fi, 4G/5G, LoRa, Ethernet, RS-485; MQTT, HTTP, CoAP, AMQP)
  5. plataforma
  6. datos
  7. aplicación
- **Versión simplificada:** adquisición, procesamiento, comunicación, visualización.
- **Tres pilares:** recopilación, comunicación, inteligencia.
- **Plataformas:** son middleware entre el borde y la aplicación. Se vieron Arduino Cloud, Ubidots (conexión por MQTT) y ThingSpeak (compatible con Matlab).

*Fuente: Teoría IoT.pdf, p. 7, 9-14; Taller Internet of Things (IoT).pdf, p. 17-19.*
*Proyecto [S]: el enlace de campo es LoRa. Cómo llega el dato a la nube y a la app (por ejemplo con MQTT) no está documentado en los documentos del equipo.*

## G. Inteligencia artificial y redes neuronales

**25. ¿Qué es la regresión lineal y qué métricas se usan?**
Aprendizaje supervisado que predice un valor continuo: ŷ = b0 + b1·x (simple) o con varias variables (múltiple). Los parámetros se estiman por mínimos cuadrados, minimizando la suma de residuos al cuadrado. Ejemplo del curso: sueldo según horas por semana, ŷ = -2461 + 297x con R² = 0.311. La regresión lineal no basta si la relación es en U.
*Fuente: Intro a IA.pptx, diap. 66-75; MSE en Clase 2.pdf, p. 37.*
Métricas (conocimiento general):
- MAE = (1/n)·Σ|y - ŷ|.
- RMSE = √MSE = √[(1/n)·Σ(y - ŷ)²].
- R² = 1 - SS_res / SS_tot.

*Proyecto: el requisito de MAE < 15 % frente a un especialista no dice cómo se normaliza el error. Definirlo es un [S] pendiente. Los datos de regresión del curso son `Data_PI_regresion.csv` (consumo de energía según temperatura, horas, carga y humedad).*

**26. ¿Qué es un perceptrón y qué funciones de activación vimos?**
Modelo matemático de neurona (Rosenblatt, 1958): salida = f(Σ wᵢ·xᵢ + b). Una sola neurona solo separa linealmente: resuelve AND y OR, no XOR; XOR necesita dos neuronas o capas.
- Sigmoide: σ(z) = 1/(1 + e⁻ᶻ), salida en (0, 1); satura y su derivada σ(1 - σ) se vuelve casi cero.
- tanh: salida en (-1, 1).
- ReLU: max(0, x).
- Softmax: yⱼ = e^zⱼ / Σ e^zₖ, para clasificación multiclase.

*Fuente: Clase 2.pdf, p. 14-15, 29-34; Perceptrón.ipynb, celdas 7-16; Red_neuronal_con_Keras.ipynb, celdas 10-11.*

**27. ¿Cómo aprende una red neuronal?**
1. Propaga los datos y obtiene la predicción (forward).
2. Mide el error con la función de pérdida: MSE para regresión, entropía cruzada para clasificación.
3. El gradiente descendente actualiza los pesos en sentido contrario al gradiente: x_nuevo = x_viejo - α·f'(x_viejo), con α = tasa de aprendizaje.
4. La retropropagación (backpropagation) calcula los gradientes capa por capa de atrás hacia adelante.
5. Optimizadores y momentum mejoran el descenso.

*Fuente: Clase 2.pdf, p. 17, 22-25, 32, 36-38, 40-48.*
Ejemplo de Keras: Dense(512, ReLU) y Dense(10, softmax), pérdida `categorical_crossentropy`, 5 épocas (Red_neuronal_con_Keras.ipynb).

**28. ¿Qué es una CNN, qué es el transfer learning y cómo se detecta el overfitting?**
- **CNN:** red para imágenes. La convolución desliza un filtro (kernel) sobre la imagen y suma los productos término a término. Capas típicas: Conv2D, ReLU, MaxPool y capas densas. Necesita muchos datos y mucho tiempo de entrenamiento.
- **Transfer learning:** reutilizar una red preentrenada (por ejemplo ResNet18 con ImageNet), congelar el extractor, entrenar la última capa y luego hacer ajuste fino (fine-tuning). Converge más rápido y rinde mejor con pocos datos.
- **Overfitting:** el modelo memoriza el entrenamiento y falla con datos nuevos. Se detecta porque el error de entrenamiento baja y el de validación sube. Se combate con más datos, regularización (por ejemplo dropout), menos capas o aumento de datos. Siempre se evalúa en un conjunto de prueba no visto.
- **Métricas de clasificación:** exactitud, precisión = VP/(VP+FP), recall = VP/(VP+FN), medida F y matriz de confusión.

*Fuente: Clase 2.pdf, p. 8-9, 74-78; CNN_TransferLearning.ipynb, celdas 1, 23, 28-31; Keras_Clasificacion_binaria.ipynb, celdas 32-38; Intro a IA.pptx, diap. 53-54.*
*Proyecto [S]: el procesamiento en Python/OpenCV podría usar visión clásica o una CNN. El estado del arte citado usa Faster R-CNN (Zhu 2025, mAP 93.14 %).*

## H. Preguntas aplicadas al proyecto

**29. Explica las inconsistencias entre los documentos del proyecto.**
- **Comunicaciones:** el Entregable 1 viejo dice Wi-Fi/WhatsApp, la rev. 3 dice acústica, el concepto elegido usa RS-485 + LoRa. Son iteraciones; la definitiva es RS-485 + LoRa.
- **Presión de simulación:** SimScale usó 50 kPa (≈ 5 m), pero la exigencia es 15 m (≈ 150 kPa). Hay que repetirla con 150 kPa.
- **Geometría heredada:** el cilindro de 220 × 130 sigue en el Entregable 1 de `main`.
- **Biomasa:** "132 kg" no está en ninguna fuente. El dato correcto es 68 a 73 kg (Loayza y Tresierra 2014).

**30. ¿Por qué se eligió la Solución 1 y cómo es el flujo de datos completo?**
- **Motivo:** no hay radio bajo el agua, así que se usa cable hasta una boya. LoRa da largo alcance con bajo consumo. Es la opción más barata y liviana.
- **Alternativas:** Solución 2 (Portenta H7 + Ethernet hasta la orilla) y Solución 3 (Raspberry Pi Zero 2 W + Wi-Fi + WhatsApp).
- **Flujo:** cámaras Arducam (SPI) -> ESP32 central (con JSN-SR04T y microSD) -> RS-485 (MAX485) -> ESP32-S3 en boya (LoRa SX1276, 18650, LM2596, panel solar) -> procesamiento fuera de la placa en Python/OpenCV -> % de malla libre frente a la imagen de referencia -> nivel de intervención -> alerta en app.
- **Control:** lazo abierto con decisión asistida: el sistema informa y la persona decide.
- **Contexto del problema:** 68 a 73 kg de biofouling por linterna en 2 a 3 meses; el recambio a 30 días redujo el biofouling 64.6 %.
- **ODS:** 14 (meta 14.b), 12 (meta 12.2) y 9 (meta 9.5).
