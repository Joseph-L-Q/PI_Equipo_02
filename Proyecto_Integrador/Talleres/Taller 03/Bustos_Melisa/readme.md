# Taller 3: Introducción a la IA - Regresión Lineal y Árboles de Decisión

---

## 1. Introducción y Planteamiento del Problema

En este taller desarrollamos e implementamos modelos de aprendizaje automático (Machine Learning) para la predicción del **Consumo de Energía** en un entorno operativo. Trabajamos con un conjunto de datos (`Data_PI_regresion.csv`) de 5,000 registros capturados por sensores, que incluyen variables ambientales e industriales: **Temperatura, Horas de Operación, Carga y Humedad**.

El problema central que abordamos es la fluctuación ineficiente del consumo eléctrico. En la industria, no anticipar estos picos genera desgaste de equipos y sobrecostos. Por ello, el objetivo de este análisis no es solo leer datos históricos, sino construir un algoritmo predictivo que tome estas variables independientes y proyecte con alta precisión la demanda energética futura, permitiendo una toma de decisiones automatizada y en tiempo real.

---

## 2. Análisis Exploratorio de Datos

### 2.1 Carga e Inspección Estructural

La primera regla del Machine Learning es que si entrenas un algoritmo con datos deficientes, obtendrás predicciones inútiles. Por ello, la inspección estructural a través de programación fue nuestro primer paso crítico.

Mediante los comandos `df.info()` y `df.describe()`, auditamos el dataset. A nivel de código, esto nos permitió confirmar que los 5,000 registros estaban completos, sin ningún valor nulo (`non-null`) que pudiera generar errores de ejecución. Además, comprobamos que todas las columnas poseían un formato numérico continuo (`float64`), lo cual es un requisito indispensable para los modelos de regresión, evitándonos transformaciones complejas.

Para entender el comportamiento de nuestra variable objetivo, utilizamos la librería Seaborn (`sns.histplot`, `sns.kdeplot`). El gráfico de densidad reveló que el consumo de energía sigue una distribución simétrica (una campana de Gauss) centrada alrededor de los 26 kWh, descartando la presencia de sesgos extremos o valores atípicos que pudieran desviar el aprendizaje del modelo.

<div align="center">

  <img width="1280" height="640" alt="image" src="https://github.com/user-attachments/assets/c4671a91-c815-4f86-b1e9-c6695bf71cc4" />
  <br>
  <em>Figura 1. Inspección Estructural del Código. Se validan los tipos de datos y la ausencia de valores nulos.</em>

  <br><br>

  <img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/81d2ece0-9079-4ed1-81d7-54c3f7f5824e" />
  <br>
  <em>Figura 2. Análisis de distribución del consumo energético. La campana simétrica indica un comportamiento estable de los datos.</em>

</div>

### 2.2 Análisis de Relaciones y Correlación

En lugar de introducir todas las variables a ciegas en el algoritmo, evaluamos estadísticamente su independencia y relevancia. La ejecución del comando `sns.heatmap()` fue el punto de inflexión de esta fase.

* **Identificación del Predictor Principal:** La matriz de correlación nos demostró de forma numérica y visual que las **Horas de Operación** poseen una relación lineal directa y muy fuerte ($r = 0.8434$) con el consumo de energía. 
* **Ausencia de Multicolinealidad:** Observamos que los coeficientes entre las variables independientes (como Temperatura vs. Carga) son cercanos a cero. Esto nos garantiza que los sensores capturan información independiente y no se "estorban" entre sí, un escenario ideal para aplicar modelos lineales aditivos.

<div align="center">

  <img width="910" height="777" alt="image" src="https://github.com/user-attachments/assets/66c7e011-c217-4b9c-8d08-f6b67f84e14c" />
  <br>
  <em>Figura 3. Matriz de correlaciones. Se identifica visualmente a las horas de operación como el predictor principal y se descarta la multicolinealidad.</em>

</div>

---

## 3. Desarrollo y Evaluación de Modelos

### 3.1 Regresión Lineal Multi-variable

Para construir la regresión, primero aplicamos una buena práctica de programación: `train_test_split`. Dividimos el dataset (70% entrenamiento, 30% prueba) para evitar que el algoritmo simplemente "memorice" las respuestas y asegurarnos de que pueda generalizar ante datos nuevos.

Al instanciar y entrenar `LinearRegression()`, el modelo calculó los pesos de cada variable. Descubrimos que, manteniendo las demás condiciones constantes, cada hora extra de operación incrementa el consumo en **1.66 kWh**. 

**Diagnóstico Estadístico (El examen real del modelo):**
Un modelo no es válido solo por lograr un buen porcentaje de acierto. Utilizando la librería `statsmodels` (OLS), realizamos un diagnóstico de los residuos (la diferencia entre la predicción y el valor real):
* **Normalidad:** El histograma de residuos demostró una distribución normal centrada en cero, lo que valida que el modelo no tiene sesgos sistemáticos.
* **Homocedasticidad:** Al observar el diagrama de dispersión de los errores, los puntos formaron una nube aleatoria y constante en forma de banda horizontal. Si hubieran formado un embudo, significaría que nuestro código falla en rangos altos de consumo; afortunadamente, logramos validar su estabilidad geométrica.

<div align="center">

  <img width="1280" height="485" alt="image" src="https://github.com/user-attachments/assets/711925f2-42c9-4a0a-940f-d26cc6c2003d" />
  <br>
  <em>Figura 4. Diagrama de dispersión de residuos y evaluación de normalidad. Se confirma la estabilidad del modelo predictivo y el cumplimiento de la homocedasticidad.</em>

</div>

### 3.2 Árboles de Decisión para Regresión

Como segunda alternativa lógica, implementamos un `DecisionTreeRegressor`. A diferencia de la regresión que traza una línea continua, el árbol fragmenta el conjunto de datos mediante reglas condicionales (ej. divisiones por umbrales de temperatura y tiempo).

* **Prevención de Sobreajuste:** Fue estrictamente necesario configurar el hiperparámetro `max_depth = 5`. Sin esta restricción, el árbol crecería infinitamente hasta memorizar el ruido de los sensores, arruinando su capacidad predictiva en el mundo real.
* **Importancia de Características (Feature Importance):** Extraímos el peso que el algoritmo le dio a cada sensor para minimizar el error. De manera fascinante, la lógica del árbol le otorgó más del **53% de importancia** a las horas operativas. Esto confirmó mediante partición de varianza exactamente lo mismo que nos había dicho el coeficiente de Pearson en el mapa de calor inicial.

<div align="center">

  <img width="1280" height="426" alt="image" src="https://github.com/user-attachments/assets/e158c654-c38a-4231-a317-e42b4beda058" />
  <br>
  <em>Figura 5. Jerarquía de características del Árbol de Decisión. El algoritmo ratifica qué variables reducen mejor el margen de error.</em>

</div>

---

## 4. Comparativa de Resultados, Discusión y Conclusión

Para definir la viabilidad operativa de estos modelos, es necesario contrastar la naturaleza de sus algoritmos y cómo procesan la información del entorno.

| Modelo | Enfoque de Aprendizaje | Fortalezas Principales | Limitaciones y Riesgos |
| :--- | :--- | :--- | :--- |
| **Regresión Lineal** | Ecuación matemática continua basada en estimadores. | • Altamente interpretable gracias a sus coeficientes.<br>• Responde perfectamente a variables con crecimiento proporcional.<br>• Diagnóstico estadístico de errores claro. | • Sensible a datos atípicos extremos.<br>• Asume que la relación entre variables es siempre una línea recta. |
| **Árbol de Decisión** | Partición del espacio mediante reglas condicionales lógicas. | • Excelente para capturar patrones no lineales.<br>• No exige supuestos estrictos de normalidad en los datos.<br>• Genera jerarquías visuales de los parámetros. | • Alto riesgo de sobreajuste (*overfitting*) si no se limita su profundidad.<br>• Pequeños cambios en los datos pueden alterar toda su estructura. |

### Discusión
La estructura de nuestro conjunto de datos favorece enormemente a la Regresión Lineal. Debido a que las Horas de Operación y la Carga tienen un comportamiento sumamente proporcional respecto al consumo eléctrico, la aproximación matemática continua logra capturar la esencia del problema de forma fluida. El Árbol de Decisión, aunque poderoso, se ve obligado a crear "escalones" para intentar seguir una tendencia que es naturalmente recta.

### Conclusión
Para este problema en particular, la **Regresión Lineal Múltiple** se consolida como la herramienta más robusta y confiable. Al haber validado rigurosamente sus supuestos de homocedasticidad y normalidad de residuos, el algoritmo garantiza predicciones estables en cualquier rango operativo. Su bajo costo computacional y su fácil interpretación la hacen ideal para ser integrada en sistemas de control en tiempo real. 

Por otro lado, el **Árbol de Decisión** demostró ser una excelente herramienta analítica complementaria, ideal para generar tableros de control visuales o auditorías, ya que nos permitió confirmar la jerarquía de los sensores sin recurrir a cálculos estadísticos tradicionales.

---

## 5. Aspectos más importantes del desarrollo

El aprendizaje más profundo de este taller es comprender que el Machine Learning aplicado a la ingeniería no es una "caja negra" donde simplemente ingresas datos y aceptas el resultado. 

* **La preparación lo es todo:** Comprendí que la limpieza de datos y el análisis exploratorio (EDA) representan el 80% del éxito. Escribir el código para entrenar un modelo toma un par de líneas, pero asegurar que esa información es válida requiere criterio analítico.
* **Diagnóstico crítico:** Me impactó descubrir cómo un simple gráfico de dispersión de errores (residuos) te revela la "verdad" absoluta sobre tu algoritmo. Un modelo puede mostrar una precisión aceptable, pero si sus residuos tienen un patrón oculto o forma de cono, será inestable y peligroso en la toma de decisiones industriales.
* **Complementariedad algorítmica:** Resultó fascinante observar cómo dos lógicas de programación tan diametralmente opuestas (la estadística paramétrica de la regresión vs. la partición heurística del árbol) llegaron a la misma conclusión irrefutable sobre la importancia de las horas de operación.

---

## 6. Archivo principal del proyecto

El desarrollo codificado, estructurado y documentado de este taller se encuentra en el siguiente notebook:

* [Regresión_Lineal_Bustos.ipynb](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Proyecto_Integrador/Talleres/Taller%2003/Bustos_Melisa/Regresi%C3%B3n_Lineal_Bustos.ipynb)

Este archivo contiene el flujo de trabajo completo: importación de librerías, análisis exploratorio exhaustivo, división de conjuntos de prueba, entrenamiento, extracción de coeficientes OLS y la validación gráfica de ambos modelos.

---

## 7. Conclusiones finales

Este taller evidencia las fases estructuradas de un proyecto de ciencia de datos, transformando la simple lectura de instrumentos en inteligencia operativa. Sin embargo, el valor real de esta experiencia radica en su aplicación directa a los desafíos de hardware e ingeniería que estamos abordando actualmente.

Este flujo de trabajo es el núcleo analítico que necesitamos para nuestro proyecto de monitoreo submarino. Los dispositivos basados en ESP32 que estamos diseñando para el hábitat marino capturarán constantemente variables ambientales complejas (presión, temperatura, tiempo de inmersión). Aplicando las técnicas de regresión lineal, limpieza de datos y diagnóstico de residuos que dominamos aquí, seremos capaces de programar el microcontrolador no solo para leer el entorno, sino para predecir la acumulación de *biofouling* o proyectar las tasas de biomasa de las conchas de abanico. Esta capacidad de anticipación es lo que convierte a un simple sensor en una verdadera herramienta de ingeniería predictiva.

---

## 8. Referencias

* [1] D. C. Montgomery, E. A. Peck, y G. G. Vining, *Introduction to Linear Regression Analysis*, 5ta ed. Hoboken, NJ: John Wiley & Sons, 2012.
* [2] Pedregosa F. et al., *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 2011.
