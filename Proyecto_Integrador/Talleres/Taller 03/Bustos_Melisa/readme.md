# Taller 3: Introducción a la IA - Regresión Lineal y Árboles de Decisión

---

## 1. Introducción y Planteamiento del Problema

En este taller desarrollamos e implementamos modelos de aprendizaje automático (Machine Learning) para la predicción del **Consumo de Energía** ($kWh$) en un entorno operativo. Trabajamos con un conjunto de datos (`Data_PI_regresion.csv`) de 5,000 registros capturados por sensores, que incluyen variables ambientales e industriales: **Temperatura** (°C), **Horas de Operación** ($h$), **Carga** (%) y **Humedad** (%).

El problema central que abordamos es la fluctuación ineficiente del consumo eléctrico. En la industria, no anticipar estos picos genera desgaste de equipos y sobrecostos. Por ello, el objetivo de este análisis no es solo leer datos históricos, sino construir un algoritmo predictivo que tome estas variables independientes y proyecte con alta precisión la demanda energética futura, permitiendo una toma de decisiones automatizada y en tiempo real.

---

## 2. Análisis Exploratorio de Datos (EDA)

Antes de programar cualquier modelo predictivo, es obligatorio realizar una inspección exploratoria. Si un algoritmo se entrena con datos basura, sus predicciones serán inútiles. En esta fase, utilizamos Google Colab para interrogar al dataset y entender su comportamiento real.

*   **Inspección Estructural en Código:** Utilizamos comandos como `df.info()` y `df.describe()` para auditar la calidad de la información. A nivel de programación, esto nos confirmó que no existían celdas vacías (valores nulos) y que todas las columnas tenían un formato numérico continuo (`float64`). Esto es vital, ya que los modelos de regresión no procesan texto ni datos inconsistentes.
*   **Distribución de la Variable Objetivo:** Empleamos matriz de dispersión, histogramas y gráficos de densidad (`sns.pairplot`, `sns.histplot`, `sns.kdeplot`) para visualizar cómo se comporta el consumo de energía. Descubrimos una distribución casi perfectamente simétrica (forma de campana) centrada en los 26 kWh. Saber esto nos da la tranquilidad de que no hay sesgos extremos o valores atípicos severos que puedan "confundir" al algoritmo durante su entrenamiento [1].
*   **El Mapa de Calor y las Correlaciones:** La ejecución de `sns.heatmap()` fue el punto de inflexión del análisis. En lugar de adivinar qué variable importaba más, la matriz de correlación nos demostró matemáticamente que las **Horas de Operación** tienen una relación lineal directa y fortísima ($r = 0.84$) con el consumo energético. Además, el gráfico nos confirmó la ausencia de multicolinealidad (las variables independientes no se estorban entre sí).

<div align="center">

  <img width="1280" height="640" alt="image" src="https://github.com/user-attachments/assets/c4671a91-c815-4f86-b1e9-c6695bf71cc4" />
  <br>
  <em>Figura 1. Inspección Estructural del Código</em>

  <br><br>

  <img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/81d2ece0-9079-4ed1-81d7-54c3f7f5824e" />
  <br>
  <em>Figura 2. Análisis de distribución del consumo energético. La campana simétrica indica un comportamiento estable de los datos.</em>

  <br><br>

  <img width="910" height="777" alt="image" src="https://github.com/user-attachments/assets/66c7e011-c217-4b9c-8d08-f6b67f84e14c" />
  <br>
  <em>Figura 3. Matriz de correlaciones. Se identifica visualmente a las horas de operación como el predictor principal.</em>

</div>

---

## 3. Desarrollo, Evaluación y Diagnóstico de Modelos

Para resolver el problema, decidimos contrastar dos lógicas de programación completamente distintas: una basada en ecuaciones continuas y otra en partición por reglas lógicas.

*   **El Entrenamiento Lineal Múltiple:** Primero, separamos los datos con `train_test_split` (70% para entrenar, 30% para probar). Esto es una buena práctica de programación para evitar que el modelo "memorice" las respuestas. Al entrenar `LinearRegression()`, el código reveló que cada hora extra de operación suma exactamente 1.66 kWh al consumo, manteniendo lo demás constante [2].
*   **Diagnóstico de Residuos (El Verdadero Examen):** Un modelo no es bueno solo por su precisión, sino por cómo se equivoca. Utilizando `statsmodels` (OLS), graficamos la diferencia entre los valores reales y las predicciones (residuos). Al ver el diagrama de dispersión de los errores, comprobamos la **homocedasticidad**: los puntos formaban una nube constante y aleatoria. Si hubieran formado un cono, significaría que nuestro código falla en los consumos altos, pero logramos un modelo estable [1].
*   **Control del Árbol de Decisión:** Como segunda alternativa, implementamos `DecisionTreeRegressor`. A diferencia de la regresión, el árbol crea umbrales lógicos (ej. "Si la temperatura es > 25 y las horas > 5, entonces..."). Aquí fue fundamental configurar el hiperparámetro `max_depth=5` en el código. Sin este límite, el árbol sufriría de "sobreajuste", memorizando el ruido de los sensores en lugar de aprender el patrón real.
*   **Extracción de la Importancia de Variables:** Usando el atributo `feature_importances_` del árbol, generamos un gráfico de barras que evaluó el peso de cada sensor. El algoritmo le otorgó más del 53% de importancia a las horas operativas, confirmando desde la lógica del árbol exactamente lo mismo que nos dijo el mapa de calor estadístico al inicio [2].

<div align="center">

  <img width="1280" height="485" alt="image" src="https://github.com/user-attachments/assets/711925f2-42c9-4a0a-940f-d26cc6c2003d" />
  <br>
  <em>Figura 4. Diagrama de dispersión de residuos y evaluación de normalidad. Se confirma la estabilidad del modelo predictivo.</em>

  <br><br>

  <img width="1280" height="426" alt="image" src="https://github.com/user-attachments/assets/e158c654-c38a-4231-a317-e42b4beda058" />
  <br>
  <em>Figura 5. Jerarquía de características del Árbol de Decisión. El algoritmo ratifica qué variables reducen mejor el margen de error.</em>

</div>

---

## 4. Aprendizajes Clave y Aplicación al Proyecto

La parte más valiosa de este taller fue comprender que la inteligencia artificial aplicada no es una "caja negra" donde metes datos y salen resultados mágicos. Requiere interpretación crítica.

*   **Lo que aprendí:** Entendí que la limpieza de datos y el análisis exploratorio son el 80% del éxito. Escribir el código del modelo toma solo unas líneas, pero diagnosticar si ese modelo es viable (mediante la homocedasticidad y la normalidad de residuos) exige verdadero criterio de ingeniería.
*   **Lo que más me llamó la atención:** Me sorprendió ver cómo un simple gráfico de dispersión de errores te cuenta la "verdad" sobre tu código. Un modelo puede tener un porcentaje de acierto alto, pero si sus residuos tienen un patrón oculto, el algoritmo es inservible en el mundo real. Comparar la transparencia matemática de la regresión frente a la jerarquización del árbol fue muy revelador.
*   **Impacto en el monitoreo marino:** Todo este flujo de trabajo cambia por completo la perspectiva de nuestro diseño de monitoreo de biomasa marina. Las técnicas de correlación y entrenamiento lineal que programamos aquí son exactamente las que necesitamos para procesar los datos continuos de los sensores sumergidos. Cruzando el tiempo de inmersión, la temperatura y la salinidad, podremos predecir con precisión la tasa de incrustación de *biofouling* o proyectar el desarrollo de las conchas de abanico, convirtiendo nuestro dispositivo en una herramienta de analítica predictiva avanzada.

---

## Referencias

[1] D. C. Montgomery, E. A. Peck, y G. G. Vining, *Introduction to Linear Regression Analysis*, 5ta ed. Hoboken, NJ: John Wiley & Sons, 2012.

[2] Pedregosa F. et al., *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research, 2011.
