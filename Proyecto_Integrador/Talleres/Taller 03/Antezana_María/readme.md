# Taller 3: Introducción a la IA - Regresión Lineal y Árboles de Decisión

---

## 1. Introducción y Planteamiento del Problema

En este taller se hará el análisis e implementación de modelos de aprendizaje automático supervisado para la estimación y optimización del consumo de energía en entornos industriales u operativos. 

* **Contextualización del Dataset:** El conjunto de datos (`Data_PI_regresion.csv`) está conformado por **5,000 observaciones numéricas** recopiladas de sensores operacionales y ambientales. Contiene cuatro variables independientes o características (*features*): **Temperatura** (°C), **Horas de Operación** ($h$), **Carga** (%) y **Humedad** (%), orientadas a estimar la variable objetivo (*target*) continua: **Consumo de Energía** ($kWh$).
* **Definición del Problema:** En sistemas de monitoreo y control operacional, la fluctuación ineficiente del consumo eléctrico representa costos elevados y desgaste acelerado de equipos. La falta de un modelo predictivo preciso impide anticipar picos de consumo o proyectar la demanda energética en función de la carga operacional y el clima circundante.
* **Objetivo del Análisis:** Desarrollar, evaluar y comparar modelos predictivos mediante **Regresión Lineal Múltiple** y **Árboles de Decisión para Regresión**, determinando cuál ofrece la mayor precisión en métricas de evaluación ($R^2$, $MSE$, $MAE$) para la toma de decisiones automatizada.

La implementación de modelos de regresión permite convertir las lecturas simples de los sensores en predicciones útiles. De esta forma, se pasa de solo observar datos pasados a anticiparse a los picos de consumo y tomar decisiones inteligentes en tiempo real dentro del proyecto.

---

## 2. Análisis Exploratorio de Datos

### 2.1 Carga e Inspección Estructural

Antes de entrenar cualquier modelo predictivo, primero se verificó la calidad e integridad del conjunto de datos. Este proceso de limpieza e inspección estructural asegura que las variables no presenten sesgos por valores nulos, registros duplicados o tipos de datos inconsistentes que afecten el rendimiento de los algoritmos.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Inspecci%C3%B3n%20de%20tipos%20de%20datos.jpg" alt="Carga e Inspección Estructural" width="100%"/>
  <br>
  <em>Figura 1. Carga del archivo CSV, inspección de tipos de datos (`info()`) y resumen estadístico general (`describe()`).</em>
</p>

**Análisis Crítico de la Estructura y Estadísticas:**

A través del método `df.info()`, se confirmó que el dataset cuenta con **5,000 registros completos** distribuidos en 5 columnas, sin ningún valor nulo (`5000 non-null`). Todos los campos están correctamente tipificados como punto flotante (`float64`), lo que evita transformaciones complejas de tipo de datos.

* **Evaluación de Dispersión y Valores Atípicos:** 
  * **Temperatura (°C):** Presenta una media de $26.5 \text{ °C}$ con un rango contenido entre $18.0 \text{ °C}$ y $35.0 \text{ °C}$, lo cual refleja un comportamiento operativo dentro de parámetros normales.
  * **Horas de Operación ($h$):** Los equipos operan en un rango de $2.0$ a $12.0 \text{ horas}$, con una media y mediana idénticas ($7.0 \text{ h}$), mostrando una distribución uniforme y simétrica.
  * **Carga (%) y Humedad (%):** La carga oscila entre $30.0\%$ y $100.0\%$, mientras que la humedad varía entre $40.0\%$ y $90.0\%$. Las diferencias entre la media y la mediana ($50\%$) en ambas variables son mínimas, descarta la presencia de sesgos extremos en la distribución inicial.
  * **Consumo de Energía ($kWh$):** La variable objetivo registra un promedio de $26.05 \text{ kWh}$ con una desviación estándar baja ($\sigma = 5.62$), variando desde un mínimo de $9.12 \text{ kWh}$ hasta un máximo de $42.63 \text{ kWh}$.


### 2.2 Análisis de Relaciones y Correlación

Para justificar la selección de características y evaluar la independencia entre las variables, se analizaron tanto las distribuciones de dispersión multivariadas como los coeficientes de correlación de Pearson.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Matriz%20de%20dispersi%C3%B3n%20y%20correlaci%C3%B3n.jpg" alt="Matriz de dispersión y mapa de calor de correlaciones" width="100%"/>
  <br>
  <em>Figura 2. Matriz de dispersión (`pairplot`) y mapa de calor de correlación de Pearson (`heatmap`) entre variables numéricas.</em>
</p>

**Análisis Estadístico y Selección de Características:**

* **Identificación de la Variable Clave:** La variable `Horas_Operacion` presenta una fuerte relación lineal positiva con la variable objetivo `Consumo_Energia`, alcanzando un coeficiente de correlación de **$r = 0.8434$**. En la matriz de dispersión se observa una tendencia ascendente clara y uniforme, consolidándola como el predictor de mayor relevancia para los modelos.
* **Aporte de Variables Secundarias:** La variable `Carga` muestra una correlación moderada de **$r = 0.3366$** con el consumo de energía. Aunque su impacto es menor que el de las horas operativas, aporta varianza explicativa útil para afinar la precisión en estados de alta exigencia del equipo.
* **Evaluación de Multicolinealidad e Independencia:** Los coeficientes entre las variables independientes son extremadamente cercanos a cero (por ejemplo, `Horas_Operacion` vs. `Temperatura` da **$-0.0260$**, y `Carga` vs. `Humedad` registra **$0.0060$**). Esto confirma la ausencia total de multicolinealidad entre los predictores, asegurando que cada característica aporta información independiente sin saturar ni distorsionar los estimadores de la Regresión Lineal.

---

## 3. Desarrollo y Evaluación de Modelos

### 3.1 Regresión Lineal Multi-variable

La Regresión Lineal Múltiple permite modelar la variable objetivo $y$ (**Consumo_Energia**) a partir de una combinación lineal de los cuatro predictores ambientales y operacionales, expresándose según la ecuación:

$$Y = \beta_0 + \beta_1 X_{\text{Temp}} + \beta_2 X_{\text{Horas}} + \beta_3 X_{\text{Carga}} + \beta_4 X_{\text{Humedad}} + \epsilon$$

Para validar formalmente el modelo, se evaluaron los supuestos estadísticos clave de **homocedasticidad** y **normalidad de residuos**, siguiendo el marco metodológico de diagnóstico de regresión [1]. Específicamente, se analizó el comportamiento de los residuos definidos por la ecuación:

$$e_i = Y_i - \hat{Y}_i$$

Según la teoría de estimación por Mínimos Cuadrados Ordinarios (MCO) [1], el cumplimiento de estos supuestos asegura que los estimadores $\beta_j$ obtenidos sean los **mejores estimadores lineales e insesgados (BLUE)** por el Teorema de Gauss-Márkov:

* **Homocedasticidad:** Verificación de varianza constante ($\text{Var}(e_i) = \sigma^2$), garantizando que la incertidumbre de predicción no aumente con la magnitud del consumo [1].
* **Normalidad:** Verificación de que $e_i \sim \mathcal{N}(0, \sigma^2)$, lo cual valida la significancia estadística de la prueba $t$ calculada para cada variable en la tabla `cdf` [1].

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Regresi%C3%B3n%20Lineal%20Multi-variable.jpg" alt="Regresión Lineal: entrenamiento, coeficientes y análisis de residuos" width="100%"/>
  <br>
  <em>Figura 3. Entrenamiento del modelo lineal, tabla de coeficientes con prueba t (`cdf`), histograma de normalidad de residuos y diagrama de dispersión para verificación de homocedasticidad.</em>
</p>

**Análisis Crítico de Coeficientes y Supuestos del Modelo:**

* **Ecuación del Modelo y Significancia Estadística:**
  * **Intersección ($\beta_0 = 2.7411$):** Representa el consumo base del sistema en condiciones nulas.
  * **Horas de Operación ($\beta_2 = 1.6688$, $t = 127.02$):** Es la variable con mayor impacto directo. Por cada hora adicional de operación, el consumo energético se incrementa en promedio $1.67 \text{ kWh}$. Su elevado valor en la estadística $t$ ($127.02$) ratifica su extrema significancia estadística.
  * **Efecto de Carga y Clima:** Las variables `Carga` ($\beta_3 = 0.0963$, $t = 51.83$) y `Temperatura` ($\beta_1 = 0.1371$, $t = 18.15$) muestran un efecto positivo moderado, mientras que `Humedad` ($\beta_4 = 0.0268$, $t = 10.26$) aporta un ajuste marginal pero estadísticamente válido.
* **Evaluación de Normalidad de Residuos:** El histograma de residuos ($Y_{test} - \hat{Y}$) refleja una distribución simétrica con forma de campana acampanada (Gaussiana) centrada en $0$, cumpliendo con el supuesto de normalidad en las perturbaciones aleatorias [1].
* **Verificación de Homocedasticidad:** En el diagrama de dispersión de *Valores residuales vs. predichos*, los errores se distribuyen aleatoriamente en una banda horizontal homogénea entre $-6$ y $+6 \text{ kWh}$ sin formar patrones cónicos ni tendencias cuadráticas. Esto confirma una varianza de error constante a lo largo de toda la escala de consumo predicho.

### 3.2 Árboles de Decisión para Regresión

El algoritmo de Árboles de Decisión para Regresión se basa en la partición recursiva del espacio de características. En cada nodo, el modelo selecciona la variable $X_j$ y el umbral de corte $s$ que minimizan la impureza del sistema, medida a través de la Reducción de la Varianza (o Suma de Errores Cuadráticos, $SSE$):

$$\text{Impureza (SSE)} = \sum_{i \in R_1} (y_i - \hat{y}_{R_1})^2 + \sum_{i \in R_2} (y_i - \hat{y}_{R_2})^2$$

Donde $\hat{y}_{R_1}$ y $\hat{y}_{R_2}$ son las medias de la variable respuesta en cada región subdividida. Para mitigar el **sobreajuste** (*overfitting*) y mantener un equilibrio óptimo entre **sesgo y varianza**, se aplicó una poda previa restringiendo la profundidad máxima a `max_depth = 5` [2].

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Arbol_de_Decision_Regresion.png" alt="Estructura, importancia de características y predicción del Árbol de Decisión" width="100%"/>
  <br>
  <em>Figura 4. Entrenamiento del Árbol de Decisión (`max_depth=5`), gráfico de importancia relativa de características y evaluación de predicciones reales vs. predichas.</em>
</p>

**Importancia de Variables y Equilibrio Sesgo-Varianza:**

* **Jerarquía de Importancia de Características (*Feature Importance*):**
  * **Variable Dominante:** Al igual que en la regresión lineal, la variable de **Horas de Operación** concentra la mayor ganancia de información e importancia relativa ($\approx 53.7\%$), siendo el nodo raíz primario de división.
  * **Aporte Secundario:** La variable **Temperatura** representa aproximadamente el $26.9\%$ de la importancia, seguida de la **Carga** ($11.1\%$). Las demás variables aportan un porcentaje marginal en la reducción total de la varianza.
* **Evaluación del Control de Profundidad (`max_depth=5`):**
  * **Control de Varianza:** Al limitar la profundidad del árbol a 5 niveles, se impide que el algoritmo memorice el ruido del conjunto de entrenamiento, evitando la creación de hojas terminales con muy pocos datos.
  * **Sesgo Acotado:** El modelo logra capturar la no-linealidad de los datos sin perder generalización, manteniendo un error medio cuadrático ($MSE$) estable sobre el conjunto de prueba (`X_test`).

---

## 4. Comparativa de Resultados, Discusión y conclusión

Para determinar cuál modelo ofrece el mejor rendimiento sobre datos no vistos, se evaluaron cuantitativamente las predicciones sobre el conjunto de prueba ($30\%$ de los datos, $1,500$ registros) mediante el Error Cuadrático Medio ($MSE$), Error Absoluto Medio ($MAE$) y el Coeficiente de Determinación ($R^2$).

| Modelo | MSE ($kWh^2$) | MAE ($kWh$) | $R^2$ Score | Fortalezas | Limitaciones |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Regresión Lineal** | **4.6124** | **1.7448** | **0.8512** | • **Alta interpretabilidad:** Muestra con claridad matemática exacta cuánto cambia el consumo según cada variable.<br>• **Bajo costo computacional:** Consume muy poca memoria y recursos del sistema.<br>• **Rápida inferencia:** Calcula predicciones de forma instantánea.<br>• **Variables significativas:** Confirma que los datos usados afectan realmente el resultado. | • **Asume linealidad:** Asume que los datos crecen o decrecen siempre a ritmo constante.<br>• **Sensible a datos raros:** Se distorsiona fácilmente si existen lecturas erróneas o picos extremos (*outliers*). |
| **Árbol de Decisión** | **5.7499** | **1.9239** | **0.8145** | • **Capta patrones complejos:** Detecta relaciones no lineales entre las variables.<br>• **Sin supuestos rígidos:** No exige que los datos sigan una distribución normal.<br>• **Lógica intuitiva:** Genera reglas de decisión fáciles de entender. | • **Sensible a variaciones:** Pequeños cambios en los datos de entrenamiento pueden alterar la estructura del árbol.<br>• **Riesgo de sobreajuste:** Requiere limitar su profundidad para no memorizar el ruido. |

---

### Discusión

1. **Rendimiento Predictivo Global:**
   * La **Regresión Lineal Múltiple** obtuvo un rendimiento superior en todas las métricas de prueba, alcanzando un $R^2 = 0.8512$ ($85.12\%$ de varianza explicada) en comparación con el $R^2 = 0.8145$ ($81.45\%$) del Árbol de Decisión.
   * El Error Absoluto Medio de la Regresión Lineal ($MAE = 1.7448 \text{ kWh}$) demuestra que sus estimaciones se desvían, en promedio, menos de $1.75 \text{ kWh}$ respecto al consumo real observado, ofreciendo mayor precisión global para la planificación de carga energética.

2. **Acerca de la Estructura de los Datos:**
   * Dado que las variables clave (`Horas_Operacion` y `Carga`) presentan un comportamiento fuertemente lineal respecto a la variable objetivo `Consumo_Energia`, las funciones continuas de la Regresión Lineal se adaptan con mayor fluidez al dominio del problema que las aproximaciones escalonadas por regiones cuadradas de los Árboles de Decisión.

### Conclusión

A partir del análisis cuantitativo y la naturaleza del dataset, la **Regresión Lineal Múltiple** se consolida como la solución superior para este proyecto. Al presentar una relación fuertemente lineal entre las horas de operación y el consumo energético, la regresión logra un mejor ajuste global ($R^2 = 0.8512$), reduciendo el error medio a solo $1.74 \text{ kWh}$. Además, su fórmula matemática directa facilita una integración ligera y de respuesta inmediata en sistemas de monitoreo en tiempo real o dispositivos IoT con capacidad de procesamiento limitada.

Por otro lado, aunque el **Árbol de Decisión** registra un margen de error ligeramente mayor ($MAE = 1.92 \text{ kWh}$), su valor principal radica en escenarios de auditoría, análisis de negocio o generación de tableros ejecutivos (*dashboards*). Resulta la alternativa ideal si el problema requiere clasificar el consumo en reglas de decisión simples y visuales (como umbrales de alerta según temperatura y carga) o si en el futuro se trabaja con variables con comportamientos no lineales complejos sin necesidad de validar supuestos estadísticos de normalidad.

---

## Referencias

* [1] D. C. Montgomery, E. A. Peck, y G. G. Vining, Introduction to Linear Regression Analysis, 5ta ed. Hoboken, NJ: John Wiley & Sons, 2012.
