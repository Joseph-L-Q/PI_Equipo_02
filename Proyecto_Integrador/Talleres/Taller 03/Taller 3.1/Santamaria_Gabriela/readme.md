# Análisis de Regresión Lineal entre la Concentración de Ozono y el Índice de Calidad del Aire (AQI)

---

# Carátula

**Universidad:** Universidad Peruana Cayetano Heredia

**Curso:** Proyecto Integrador 

**Taller:** Taller 03 - Regresión Lineal

**Título del proyecto:**

**Análisis de Regresión Lineal entre la Concentración de Ozono y el Índice de Calidad del Aire (AQI)**

**Autor:** Gabriela Santamaria Huaytan 

**Docente:** Maria Angelica Rejas Nuñez 

**Año:** 2026

---

# 1. Introducción

La calidad del aire representa un aspecto fundamental dentro del análisis ambiental debido a su relación con las condiciones de vida y los posibles efectos sobre la salud pública. Entre los contaminantes atmosféricos monitoreados con mayor frecuencia se encuentra el ozono troposférico (O₃), debido a su importancia dentro de los indicadores utilizados para evaluar los niveles de contaminación ambiental.

El Índice de Calidad del Aire (AQI, por sus siglas en inglés) es un indicador utilizado para representar la calidad del aire mediante una escala numérica, permitiendo interpretar de manera sencilla los niveles de contaminación registrados en una determinada zona.

El presente proyecto tiene como finalidad aplicar un modelo de regresión lineal simple para analizar la relación existente entre la concentración máxima diaria de ozono durante un periodo de 8 horas y el valor diario del Índice de Calidad del Aire registrado en una estación de monitoreo ubicada en San Francisco, California.

El objetivo principal es determinar si la concentración de ozono permite explicar el comportamiento del AQI y evaluar la capacidad predictiva del modelo mediante la comparación entre valores reales y valores estimados.

Para ello, se desarrolló un flujo completo de análisis de datos que comprende:

- Obtención y selección del conjunto de datos.
- Exploración inicial de la información.
- Análisis estadístico y visualización de variables.
- Evaluación de la relación entre concentración de ozono y AQI.
- Construcción del modelo de regresión lineal.
- Evaluación del desempeño mediante predicciones.
- Análisis de residuos para validar el comportamiento de los errores.

Los datos utilizados fueron obtenidos mediante la plataforma **AirData de la Environmental Protection Agency (EPA)**, herramienta que permite acceder a registros históricos de calidad del aire recopilados mediante estaciones de monitoreo ambiental en Estados Unidos <a href="#ref1">[1]</a>.


---

# 2. Metodología


## 2.1 Fuente y obtención de datos

El conjunto de datos utilizado corresponde a mediciones diarias de ozono obtenidas desde la plataforma **AirData de la Environmental Protection Agency (EPA)**.

Para la descarga de información se configuraron los siguientes parámetros:

- **Contaminante seleccionado:** Ozone.
- **Año de análisis:** 2022.
- **Área geográfica:** San Francisco, California.
- **Estación de monitoreo:** Site ID 060750005.

La selección de estos parámetros permitió obtener registros diarios correspondientes a la concentración de ozono medida en una estación específica de monitoreo ambiental.


<img width="716" height="969" alt="imagen" src="https://github.com/user-attachments/assets/101c7724-c30c-4e98-b035-601cc8637c94" />

**Fig. 1.** Configuración de parámetros para la descarga del conjunto de datos desde la plataforma AirData de la Environmental Protection Agency (EPA).


La figura evidencia el origen de los datos utilizados en el proyecto y permite garantizar la trazabilidad de la información analizada.

Posteriormente, el archivo descargado fue importado en Google Colab para realizar el procesamiento, exploración y construcción del modelo predictivo.


---

## 2.2 Descripción del conjunto de datos

El dataset utilizado contiene registros diarios relacionados con la medición del ozono y variables asociadas al monitoreo ambiental.

Entre las variables disponibles se encuentran:

- Información temporal de la medición.
- Concentración máxima diaria de ozono durante 8 horas.
- Valor diario del AQI.
- Datos descriptivos de la estación de monitoreo.

Luego de realizar la exploración inicial, se seleccionaron las variables principales utilizadas en el modelo:

| Variable | Tipo | Descripción |
|---|---|---|
| Daily Max 8-hour Ozone Concentration | Independiente | Concentración máxima diaria de ozono durante 8 horas |
| Daily AQI Value | Dependiente | Índice diario de calidad del aire |

La variable concentración de ozono fue seleccionada como variable predictora debido a que representa el nivel del contaminante analizado, mientras que el AQI fue considerado como variable objetivo debido a que representa la condición de calidad del aire asociada.


---

## 2.3 Herramientas utilizadas

El análisis fue desarrollado utilizando el entorno **Google Colab** mediante el lenguaje de programación Python.

Las principales herramientas utilizadas fueron:

| Herramienta | Aplicación |
|---|---|
| Pandas | Lectura y manipulación del conjunto de datos |
| NumPy | Procesamiento numérico |
| Matplotlib | Construcción de gráficos |
| Seaborn | Visualización estadística |
| Scikit-learn | Construcción y evaluación del modelo predictivo |


La manipulación y organización de los datos fue realizada mediante Pandas, biblioteca ampliamente utilizada para análisis de datos estructurados en Python <a href="#ref3">[3]</a>.

Para la construcción del modelo de regresión lineal se utilizó Scikit-learn, biblioteca que proporciona algoritmos de aprendizaje supervisado y herramientas para evaluación de modelos predictivos <a href="#ref2">[2]</a>.

Las representaciones gráficas fueron desarrolladas mediante Matplotlib y Seaborn, herramientas utilizadas para analizar distribuciones, relaciones entre variables y patrones presentes en los datos <a href="#ref4">[4]</a>, <a href="#ref5">[5]</a>.


---

## 2.4 Exploración inicial de datos

Antes de realizar el entrenamiento del modelo se efectuó una exploración inicial del conjunto de datos.

Esta etapa permitió conocer:

- La estructura general del dataset.
- El número de registros disponibles.
- Los tipos de variables.
- La existencia de valores nulos.
- El comportamiento estadístico de las variables numéricas.

Para ello se utilizaron las funciones:

- `df.info()`
- `df.describe()`

Esta revisión permitió identificar las variables relevantes para el análisis y descartar aquellas que correspondían únicamente a información descriptiva de la estación de monitoreo.


---

## 2.5 Análisis exploratorio mediante visualizaciones

Posteriormente se desarrolló un análisis exploratorio utilizando diferentes representaciones gráficas:

- Diagramas de dispersión.
- Histogramas.
- Gráficos de densidad.
- Matriz de correlación.

Estas visualizaciones permitieron identificar patrones iniciales, evaluar la distribución de los datos y determinar si existía una relación lineal entre la concentración de ozono y el AQI.


---

## 2.6 Construcción del modelo de regresión lineal

Para desarrollar el modelo predictivo se aplicó una regresión lineal simple considerando:

**Variable independiente:**

- Daily Max 8-hour Ozone Concentration

**Variable dependiente:**

- Daily AQI Value


El conjunto de datos fue dividido utilizando:

- 70% de datos para entrenamiento.
- 30% de datos para prueba.

Además, se estableció una semilla fija mediante `random_state = 123`, permitiendo que los resultados obtenidos puedan ser reproducidos.

El modelo fue entrenado utilizando el algoritmo `LinearRegression` de Scikit-learn, obteniendo los coeficientes necesarios para representar matemáticamente la relación entre ambas variables.


---

## 2.7 Evaluación del modelo

La evaluación del modelo se realizó mediante:

- Comparación entre valores reales y valores predichos.
- Evaluación del error generado.
- Análisis de residuos.


El análisis de residuos permitió evaluar el comportamiento de los errores del modelo y determinar si las diferencias entre valores observados y estimados presentaban patrones específicos.

Para ello se utilizaron:

- Histograma de residuos.
- Gráfico de residuos frente a valores predichos.


---


