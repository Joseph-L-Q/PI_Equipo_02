# Taller 3: Regresión Lineal y Árboles de Decisión

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
*Principios matemáticos del modelo de Regresión Lineal, supuestos de homocedasticidad y normalidad de residuos [1].*

![Fig. 3. Código de entrenamiento y gráfica de residuos del modelo de Regresión Lineal](ruta/a/tu/imagen3.png)  
* **Fig. 3.** Código de entrenamiento y gráfica de residuos del modelo de Regresión Lineal.

*Análisis del desempeño del modelo basado en los coeficientes obtenidos y el comportamiento de las predicciones frente a los valores reales.*

### 3.2 Árboles de Decisión para Regresión
*Fundamentos del algoritmo de partición recursiva, criterios de impureza y control de profundidad para evitar sobreajuste [2].*

![Fig. 4. Visualización de la estructura y divisiones del Árbol de Decisión](ruta/a/tu/imagen4.png)  
* **Fig. 4.** Visualización de la estructura y divisiones del Árbol de Decisión.

*Evaluación de la importancia de variables en el árbol y diagnóstico del equilibrio entre sesgo y varianza.*

---

## 4. Comparativa de Resultados y Discusión

*Evaluación cuantitativa comparativa de las métricas clave obtenidas en la fase de prueba:*

| Modelo | MSE | MAE | $R^2$ Score | Fortalezas | Limitaciones |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Regresión Lineal** | *[Valor]* | *[Valor]* | *[Valor]* | Alta interpretabilidad, bajo costo computacional | Sensible a *outliers* y asume linealidad |
| **Árbol de Decisión** | *[Valor]* | *[Valor]* | *[Valor]* | Captura relaciones no lineales complejas | Propenso a *overfitting* sin poda |

*Discusión sobre qué modelo ofrece el mejor rendimiento en función de las necesidades operativas del problema.*

---

## 5. Propuesta de Integración en Arquitectura de Datos
*Estrategia para empaquetar el modelo entrenado (`joblib`/`pickle`), automatizar la ingesta de datos y desplegarlo como servicio consumible.*

*Descripción del flujo de inferencia en tiempo real o por lotes para el proyecto.*

---

## Referencias

* [1] F. Pedregosa *et al.*, "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, 2011.
* [2] L. Breiman, *Classification and Regression Trees*, Routledge, 2017.
* [3] IEEE, "IEEE Editorial Style Manual," IEEE Periodicals, Piscataway, NJ, USA, 2021.
