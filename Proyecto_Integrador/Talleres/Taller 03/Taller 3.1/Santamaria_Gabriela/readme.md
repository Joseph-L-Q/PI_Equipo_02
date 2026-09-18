# Análisis de Regresión Lineal entre la Concentración de Ozono y el Índice de Calidad del Aire (AQI)

---

# Carátula

**Universidad:** Universidad Peruana Cayetano Heredia
**Curso:** Proyecto Integrador
**Taller:** Taller 03 - Regresión Lineal

**Título del proyecto:**Análisis de Regresión Lineal entre la Concentración de Ozono y el Índice de Calidad del Aire (AQI)

**Autor:** Gabriela Santamaria Huaytan 
**Docente:** Maria Angelica Rejas Nuñez 
**Año:** 2026

---

# 1. Introducción

La calidad del aire representa un factor importante para el análisis ambiental debido a su relación con la salud pública y las condiciones de vida de la población. Dentro de los contaminantes atmosféricos monitoreados con mayor frecuencia se encuentra el ozono troposférico (O₃), debido a su influencia en los indicadores utilizados para evaluar los niveles de contaminación ambiental.

El Índice de Calidad del Aire (AQI, por sus siglas en inglés) es un indicador que permite representar mediante una escala numérica el nivel de contaminación registrado en una determinada zona, facilitando la interpretación del estado de la calidad del aire.

El presente informe desarrolla un modelo de regresión lineal simple con el objetivo de analizar la relación existente entre la concentración máxima diaria de ozono durante un periodo de 8 horas y el valor diario del AQI registrado en una estación de monitoreo ubicada en San Francisco, California.

El propósito principal del análisis es determinar si la concentración de ozono permite explicar el comportamiento del AQI y evaluar la capacidad predictiva del modelo mediante la comparación entre valores reales y valores estimados.

Para lograr este objetivo se desarrolló un flujo completo de análisis de datos que comprende:

* Exploración inicial del conjunto de datos.
* Análisis estadístico de las variables.
* Visualización gráfica de patrones y relaciones.
* Evaluación de correlación.
* Construcción del modelo de regresión lineal.
* Validación mediante análisis de residuos.

Los datos utilizados fueron obtenidos del portal **AirData de la Environmental Protection Agency (EPA)**, plataforma que proporciona registros históricos de calidad del aire obtenidos mediante estaciones de monitoreo ambiental distribuidas en Estados Unidos <a href="#ref1">[1]</a>.

---

# 2. Metodología

## 2.1 Fuente y descripción de los datos

El conjunto de datos utilizado corresponde al archivo:

`ad_viz_plotval_data.csv`

Este dataset contiene mediciones diarias de ozono correspondientes a la estación de monitoreo con **Site ID 60750005**, ubicada en San Francisco, California.

El conjunto original contiene diferentes variables relacionadas con:

* Fecha de medición.
* Concentración máxima diaria de ozono durante 8 horas.
* Valor diario del AQI.
* Información descriptiva de la estación.
* Datos administrativos del monitoreo.

Luego de realizar la exploración inicial, se identificó que muchas variables correspondían a información constante de la estación de monitoreo, por lo que no aportaban variabilidad para el modelo predictivo.

Por esta razón, se seleccionaron las siguientes variables principales:

| Variable                             | Tipo                   | Descripción                                          |
| ------------------------------------ | ---------------------- | ---------------------------------------------------- |
| Daily Max 8-hour Ozone Concentration | Variable independiente | Concentración máxima diaria de ozono durante 8 horas |
| Daily AQI Value                      | Variable dependiente   | Valor diario del Índice de Calidad del Aire          |

La selección de estas variables permitió analizar la relación entre la concentración del contaminante y el indicador utilizado para representar la calidad del aire.

---

## 2.2 Herramientas utilizadas

El desarrollo del análisis fue realizado mediante el entorno **Google Colab**, utilizando el lenguaje de programación Python.

Las principales herramientas utilizadas fueron:

| Herramienta  | Aplicación                                               |
| ------------ | -------------------------------------------------------- |
| Pandas       | Lectura, organización y manipulación del dataset         |
| NumPy        | Operaciones numéricas                                    |
| Matplotlib   | Generación de gráficos                                   |
| Seaborn      | Visualización estadística                                |
| Scikit-learn | Construcción y evaluación del modelo de regresión lineal |

La manipulación de datos se realizó mediante estructuras de datos proporcionadas por Pandas, herramienta ampliamente utilizada para análisis de información estructurada en Python <a href="#ref3">[3]</a>.

Asimismo, la construcción del modelo predictivo fue desarrollada mediante Scikit-learn, librería que proporciona algoritmos de aprendizaje supervisado y herramientas para evaluación de modelos <a href="#ref2">[2]</a>.

---

## 2.3 Exploración inicial del conjunto de datos

Antes de desarrollar el modelo predictivo se realizó una exploración inicial del dataset con la finalidad de comprender su estructura y características principales.

Para ello se utilizaron funciones descriptivas como:

* `df.info()`
* `df.describe()`

Estas herramientas permitieron identificar:

* Número de registros disponibles.
* Tipo de datos de cada variable.
* Existencia de valores nulos.
* Distribución estadística de las variables numéricas.

Esta etapa fue fundamental debido a que permitió determinar qué variables eran adecuadas para el análisis y evitar incluir información que no aportara al modelo.

---

## 2.4 Análisis exploratorio mediante visualizaciones

Posteriormente se desarrolló un análisis gráfico para comprender el comportamiento de las variables.

Se utilizaron diferentes representaciones:

* Diagramas de dispersión.
* Histogramas.
* Gráficos de densidad.
* Matriz de correlación.

Las visualizaciones permitieron identificar tendencias, distribución de datos y posibles patrones antes del entrenamiento del modelo.

Los gráficos fueron desarrollados utilizando Matplotlib y Seaborn, herramientas ampliamente empleadas para análisis exploratorio y representación visual de datos científicos <a href="#ref4">[4]</a>, <a href="#ref5">[5]</a>.

---

## 2.5 Construcción del modelo de regresión lineal

Para construir el modelo predictivo se aplicó una regresión lineal simple utilizando:

* Variable independiente:

  * Concentración máxima diaria de ozono.

* Variable dependiente:

  * AQI diario.

El conjunto de datos fue dividido en:

* 70% para entrenamiento.
* 30% para prueba.

Se utilizó una semilla fija (`random_state = 123`) con la finalidad de garantizar la reproducibilidad de los resultados.

El modelo fue entrenado mediante el algoritmo `LinearRegression` de Scikit-learn, obteniendo los coeficientes necesarios para representar matemáticamente la relación entre ambas variables.

---

## 2.6 Evaluación del modelo

La evaluación del modelo se realizó mediante:

* Comparación entre valores reales y predichos.
* Cálculo del error generado.
* Análisis de residuos.

Los residuos fueron evaluados mediante:

* Histograma de errores.
* Gráfico de residuos frente a valores predichos.

Este análisis permitió verificar si los errores presentaban un comportamiento adecuado y detectar posibles valores atípicos dentro del conjunto evaluado.

---

