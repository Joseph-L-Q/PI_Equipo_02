# Análisis de Regresión Lineal entre la Concentración de Ozono y el Índice de Calidad del Aire (AQI)

---

# Carátula

**Universidad:** Universidad Peruana Cayetano Heredia

**Curso:** Proyecto Integrador 

**Taller:** Taller 03.1 - Regresión Lineal

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
# 3. Resultados

En esta sección se presentan los resultados obtenidos durante el análisis exploratorio de datos, construcción del modelo de regresión lineal y evaluación del desempeño predictivo.

Las visualizaciones permiten comprender el comportamiento de las variables analizadas, identificar relaciones entre ellas y evaluar la capacidad del modelo para estimar el Índice de Calidad del Aire (AQI) a partir de la concentración de ozono.

---

# 3.1 Inspección inicial del conjunto de datos

<img width="572" height="542" alt="image" src="https://github.com/user-attachments/assets/1b6a2f65-a0b0-473b-bed9-056eb26e296a" />

<img width="1775" height="362" alt="image" src="https://github.com/user-attachments/assets/1358d295-a78e-4048-bc54-85b19f57495e" />


**Fig. 2.** Inspección de la estructura del conjunto de datos mediante información general y estadísticas descriptivas.


La exploración inicial permitió conocer la estructura del conjunto de datos antes de realizar el modelamiento predictivo.

Mediante la función `df.info()` se identificaron las variables disponibles, sus respectivos tipos de datos y la estructura general del dataset. Asimismo, la función `df.describe()` permitió obtener información estadística de las variables numéricas, como valores mínimos, máximos, promedio y dispersión.

Esta etapa fue fundamental debido a que permitió determinar cuáles variables contenían información útil para el análisis y seleccionar aquellas relacionadas directamente con el objetivo del proyecto.

A partir de esta revisión se seleccionaron como variables principales:

- **Daily Max 8-hour Ozone Concentration:** variable predictora.
- **Daily AQI Value:** variable objetivo.

Las demás variables fueron consideradas principalmente como información descriptiva de la estación de monitoreo y no fueron utilizadas dentro del modelo debido a que no aportaban variabilidad al análisis.

---

# 3.2 Análisis de relación entre la concentración de ozono y AQI


<img width="701" height="575" alt="image" src="https://github.com/user-attachments/assets/2edc981c-8df2-4136-807a-7be046b30b4e" />


**Fig. 3.** Relación entre la concentración de ozono y el AQI diario mediante un análisis gráfico de dispersión.


El análisis gráfico permitió observar la relación existente entre la concentración de ozono y el Índice de Calidad del Aire.

En la figura se observa una tendencia creciente entre ambas variables, indicando que cuando aumenta la concentración de ozono también tiende a aumentar el valor del AQI.

La distribución de los puntos presenta un comportamiento aproximadamente lineal, lo cual representa una condición favorable para aplicar un modelo de regresión lineal simple.

Sin embargo, también se observa que algunos valores presentan agrupaciones específicas. Esto ocurre debido a que las mediciones de concentración de ozono presentan valores repetidos durante diferentes días del periodo analizado, generando concentraciones de puntos en determinadas zonas del gráfico.

---

# 3.3 Distribución del Índice de Calidad del Aire (AQI)


<img width="817" height="551" alt="image" src="https://github.com/user-attachments/assets/b1799cba-07e1-43d2-b0ff-bbfc8eeff47d" />



**Fig. 4.** Distribución de frecuencia del Índice de Calidad del Aire (AQI).


El histograma permite analizar la frecuencia con la que aparecen los diferentes valores de AQI registrados durante el periodo de estudio.

La distribución muestra que los datos no se encuentran repartidos uniformemente, sino que existe una concentración de observaciones dentro de determinados rangos de AQI.

Este comportamiento puede explicarse debido a que las condiciones ambientales no presentan cambios completamente aleatorios durante el periodo analizado, generando días con niveles similares de contaminación.

Asimismo, la presencia de valores alejados del grupo principal puede representar eventos particulares con condiciones de contaminación diferentes al comportamiento habitual.

Estos valores extremos son importantes debido a que pueden influir posteriormente en el ajuste del modelo y en la magnitud de los errores de predicción.

---

# 3.4 Análisis de densidad del AQI


<img width="687" height="547" alt="image" src="https://github.com/user-attachments/assets/9a18355a-2b69-48d4-a7ec-d2b29150d2d3" />


**Fig. 5.** Distribución de densidad del AQI diario.


La curva de densidad permite observar de manera continua la distribución de los valores del AQI y complementar la información obtenida mediante el histograma.

El punto máximo de la curva representa la zona donde se concentra la mayor cantidad de observaciones, correspondiente aproximadamente al rango de AQI más frecuente durante el periodo analizado.

La forma de la curva permite identificar la tendencia general de los datos y observar si existen concentraciones principales o desviaciones hacia valores extremos.

---

# 3.5 Matriz de correlación entre variables


<img width="737" height="672" alt="image" src="https://github.com/user-attachments/assets/23a831a1-c386-42f5-a8b5-f0f18d373874" />


**Fig. 6.** Matriz de correlación entre la concentración de ozono y el AQI diario.


La matriz de correlación permitió cuantificar la relación lineal existente entre las variables utilizadas en el análisis.

El resultado obtenido muestra una correlación positiva extremadamente alta entre la concentración de ozono y el AQI, con valores cercanos a 1.

Este resultado indica que ambas variables presentan un comportamiento altamente relacionado, donde incrementos en la concentración de ozono están asociados con aumentos en el valor del AQI.

Esta relación es coherente debido a que el AQI correspondiente al contaminante ozono se encuentra directamente relacionado con la concentración medida del mismo.

La alta correlación obtenida justifica la utilización de un modelo de regresión lineal para representar matemáticamente dicha relación.

---

# 3.6 Construcción del modelo de regresión lineal


<img width="760" height="692" alt="image" src="https://github.com/user-attachments/assets/1d851cf6-4465-47db-9adb-c5d33a833134" />


**Fig. 7.** Relación ajustada mediante el modelo de regresión lineal entre la concentración de ozono y el AQI diario.


El modelo de regresión lineal permitió representar matemáticamente la relación existente entre la concentración de ozono y el Índice de Calidad del Aire (AQI).

La distribución de los puntos evidencia una tendencia creciente entre ambas variables, indicando que incrementos en la concentración de ozono están asociados con valores mayores de AQI.

El ajuste obtenido confirma que la variable concentración de ozono presenta capacidad explicativa sobre el comportamiento del AQI dentro del conjunto de datos analizado.

El coeficiente obtenido representa la variación esperada del AQI ante incrementos en la concentración de ozono, mientras que el intercepto corresponde al valor estimado del AQI cuando la concentración del contaminante tiende a cero.

---

# 3.7 Comparación entre valores reales y valores predichos


<img width="571" height="612" alt="image" src="https://github.com/user-attachments/assets/34dea91d-d278-4475-a72f-2e42c3295049" />


**Fig. 8.** Comparación entre valores reales y valores predichos generados por el modelo de regresión lineal.


La comparación entre los valores reales y predichos permitió evaluar visualmente el desempeño del modelo sobre datos que no fueron utilizados durante el entrenamiento.

La cercanía entre ambos valores representa una menor diferencia de predicción y, por lo tanto, un mejor ajuste del modelo.

Los puntos alejados respecto a la tendencia principal representan observaciones donde el modelo presenta mayores errores de estimación.

Esta evaluación permitió verificar que el modelo logra seguir adecuadamente el comportamiento general del AQI, aunque existen algunos registros donde la predicción presenta mayor desviación respecto al valor real.

---

# 3.8 Análisis de residuos del modelo


<img width="842" height="670" alt="image" src="https://github.com/user-attachments/assets/9bb0cfd2-22b1-4e8d-a763-7bd828f621c0" />



**Fig. 9.** Distribución de los residuos obtenidos del modelo de regresión lineal.


Los residuos representan la diferencia entre los valores reales del AQI y los valores estimados por el modelo.

La distribución obtenida muestra que la mayoría de los errores se concentran alrededor del valor cero, indicando que gran parte de las predicciones presentan diferencias pequeñas respecto a los valores observados.

Sin embargo, se identifica la presencia de una observación alejada del comportamiento principal de los residuos. Este valor representa un caso donde el modelo presentó una mayor diferencia entre el AQI real y el AQI estimado.

La presencia de este valor atípico puede estar asociada a condiciones particulares del día analizado, donde la relación entre concentración de ozono y AQI presentó un comportamiento diferente al patrón general aprendido por el modelo.

---

# 3.9 Evaluación de homocedasticidad mediante residuos


<img width="592" height="597" alt="image" src="https://github.com/user-attachments/assets/6c29ae1d-d166-4717-8418-6b0444590e55" />


**Fig. 10.** Dispersión de residuos frente a valores predichos para evaluar el comportamiento del error.


El gráfico de residuos frente a valores predichos permite analizar si los errores presentan una distribución aleatoria o si existe algún patrón asociado a los valores estimados por el modelo.

Se observa que los residuos presentan agrupaciones asociadas a determinados valores predichos, comportamiento relacionado con la repetición de ciertos valores de concentración de ozono dentro del periodo analizado.

Asimismo, se identifica nuevamente la presencia del valor atípico observado en el histograma de residuos.

Aunque el modelo presenta un comportamiento adecuado en términos generales, la distribución de los residuos sugiere que sería conveniente complementar el análisis mediante pruebas estadísticas adicionales para evaluar con mayor precisión el supuesto de homocedasticidad.

---
## 3.10 Modelo de árbol de decisión

Como segundo enfoque predictivo se implementó un modelo basado en árboles de decisión con la finalidad de comparar su comportamiento frente al modelo de regresión lineal.

A diferencia de la regresión lineal, que busca representar una relación matemática entre variables mediante una ecuación, los árboles de decisión generan reglas de decisión mediante divisiones sucesivas del conjunto de datos.

Este modelo permite identificar patrones dentro de la información y realizar predicciones a partir de las condiciones establecidas durante el proceso de entrenamiento.


### Construcción del modelo de árbol de decisión


<img width="636" height="692" alt="image" src="https://github.com/user-attachments/assets/32c21201-b653-4a06-834e-27c3c39270d6" />



**Fig. 11.** Modelo basado en árbol de decisión para la predicción del Índice de Calidad del Aire (AQI).


La construcción del árbol permitió desarrollar un segundo modelo predictivo utilizando una metodología diferente a la regresión lineal.

El algoritmo divide progresivamente los datos en diferentes nodos con el objetivo de encontrar reglas que reduzcan el error de predicción.

La representación gráfica del árbol permite visualizar la estructura de decisiones generada por el modelo y comprender cómo se realizan las predicciones a partir de las variables utilizadas.

Este enfoque resulta útil debido a que permite capturar relaciones que pueden presentar comportamientos no necesariamente lineales.


---

### Importancia de variables del árbol


<img width="970" height="701" alt="image" src="https://github.com/user-attachments/assets/f4e65502-2f4f-4814-85f5-e39546864963" />


**Fig. 12.** Importancia relativa de las variables utilizadas en el modelo de árbol de decisión.


El análisis de importancia de variables permitió identificar cuáles características tuvieron mayor influencia durante el proceso de predicción del modelo.

Esta evaluación se basa en la contribución de cada variable durante las divisiones realizadas por el árbol, considerando aquellas que generan una mayor reducción del error dentro del modelo.

A diferencia de la regresión lineal, donde la influencia de las variables se interpreta mediante coeficientes, el árbol de decisión permite analizar la relevancia de cada característica según su participación en las reglas generadas.

Este resultado facilita la interpretación del modelo y permite reconocer cuáles variables aportan mayor información para estimar el comportamiento del AQI.


---
## 3.11 Validación estadística mediante OLS


<img width="775" height="637" alt="image" src="https://github.com/user-attachments/assets/28299285-e398-4c2a-8103-de86c1b289d0" />


**Fig. 13.** Resumen estadístico del modelo de regresión lineal mediante Ordinary Least Squares (OLS).


Con la finalidad de complementar la evaluación del modelo de regresión lineal, se realizó una validación estadística mediante el método de Mínimos Cuadrados Ordinarios (OLS, por sus siglas en inglés).

Este análisis permitió evaluar la significancia estadística de la relación existente entre la concentración de ozono y el Índice de Calidad del Aire mediante indicadores como:

- Coeficiente estimado.
- Error estándar.
- Estadístico t.
- Valor p (*p-value*).


El coeficiente estimado representa la relación entre la variable independiente y la variable objetivo, mientras que el error estándar permite evaluar la variabilidad asociada a dicha estimación.

Asimismo, el estadístico t y el valor p permiten determinar si la variable predictora presenta una relación estadísticamente significativa dentro del modelo.

Esta validación complementa los resultados obtenidos mediante las métricas predictivas, debido a que permite evaluar no solamente la capacidad del modelo para realizar predicciones, sino también la relevancia estadística de la relación encontrada entre las variables analizadas.

---
# 4. Discusión

Los resultados obtenidos permitieron analizar la relación entre la concentración de ozono y el Índice de Calidad del Aire (AQI) mediante diferentes enfoques de modelamiento predictivo.

El análisis exploratorio evidenció una relación positiva entre ambas variables, observándose que incrementos en la concentración de ozono se asociaron con aumentos en los valores del AQI. Esta relación fue confirmada mediante el análisis de correlación, donde se obtuvo una asociación lineal elevada entre las variables analizadas.

El modelo de regresión lineal permitió representar matemáticamente esta relación y generar predicciones del AQI a partir de la concentración de ozono. La comparación entre valores reales y predichos mostró que el modelo logra seguir la tendencia general de los datos; sin embargo, algunas observaciones presentaron mayores diferencias, reflejadas posteriormente en el análisis de residuos.

El análisis de residuos permitió evaluar el comportamiento de los errores del modelo. La concentración de la mayoría de residuos alrededor del valor cero indica que el modelo presenta un comportamiento adecuado para gran parte de las observaciones. No obstante, la presencia de valores alejados evidencia casos particulares donde la relación entre las variables no siguió completamente la tendencia aprendida por el modelo.

Por otro lado, la implementación del modelo basado en árbol de decisión permitió evaluar un enfoque alternativo al modelo lineal. Mientras la regresión lineal busca establecer una relación continua entre las variables mediante una ecuación matemática, el árbol de decisión genera reglas de predicción mediante divisiones sucesivas del conjunto de datos.

El análisis de importancia de variables del árbol permitió identificar aquellas características con mayor contribución dentro del proceso predictivo. Este enfoque facilita la interpretación del modelo al mostrar qué variables influyen en mayor medida durante la generación de las predicciones.

La validación estadística mediante OLS complementó el análisis del modelo de regresión lineal al evaluar la significancia de la relación encontrada entre la concentración de ozono y el AQI. Esto permitió analizar no solamente el desempeño predictivo del modelo, sino también la relevancia estadística de la variable utilizada como predictor.

Sin embargo, es importante considerar algunas limitaciones del análisis. El modelo desarrollado utiliza principalmente la concentración de ozono como variable explicativa, por lo que no incorpora otros factores ambientales que pueden influir en la calidad del aire, como temperatura, humedad, velocidad del viento u otros contaminantes atmosféricos.

Por ello, futuras mejoras podrían considerar la incorporación de nuevas variables predictoras y la evaluación de modelos más complejos que permitan capturar relaciones no lineales y mejorar la capacidad de predicción.

---
# 5. Archivo principal del proyecto

El desarrollo completo del análisis se encuentra implementado en el siguiente notebook:

- [Regresion_lineal_Santamaria_ad_viz_plotval_data.ipynb](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Proyecto_Integrador/Talleres/Taller%2003/Taller%203.1/Santamaria_Gabriela/Regresion_lineal_Santamaria_ad_viz_plotval_data.ipynb)


El notebook contiene el desarrollo completo del proyecto, incluyendo:

- Carga y exploración inicial del conjunto de datos.
- Análisis descriptivo de las variables.
- Preparación y selección de datos para el modelamiento.
- Visualización de relaciones y distribuciones mediante gráficos exploratorios.
- Construcción del modelo de regresión lineal.
- Evaluación del modelo mediante valores reales y predichos.
- Análisis de residuos para evaluar el comportamiento de los errores.
- Implementación del modelo basado en árbol de decisión.
- Análisis de importancia de variables.
- Validación estadística mediante el modelo OLS.

Este archivo permite reproducir el flujo completo del análisis y verificar los resultados presentados en el presente informe.

---

# 6. Conclusiones

A partir del análisis realizado sobre la relación entre la concentración de ozono y el Índice de Calidad del Aire (AQI), se obtuvieron las siguientes conclusiones:

- El análisis exploratorio permitió identificar una relación positiva entre la concentración máxima diaria de ozono y el AQI, evidenciando que incrementos en la concentración del contaminante están asociados con aumentos en el índice de calidad del aire.

- El modelo de regresión lineal permitió representar adecuadamente la relación entre ambas variables, mostrando capacidad para estimar el comportamiento general del AQI a partir de la concentración de ozono.

- La evaluación mediante comparación entre valores reales y predichos permitió verificar el desempeño del modelo; sin embargo, el análisis de residuos evidenció la presencia de algunas observaciones con mayores errores de estimación.

- El análisis de residuos permitió evaluar el comportamiento del modelo e identificar posibles valores atípicos que pueden influir en la precisión de las predicciones.

- La implementación del modelo basado en árbol de decisión permitió analizar un enfoque alternativo al modelo lineal, facilitando la identificación de patrones mediante reglas de decisión e importancia relativa de variables.

- La validación estadística mediante OLS permitió complementar el análisis predictivo mediante la evaluación de la significancia estadística de la relación entre la concentración de ozono y el AQI.

- Como mejora futura, se recomienda incorporar variables ambientales adicionales como temperatura, humedad, velocidad del viento u otros contaminantes, con la finalidad de desarrollar modelos más completos y mejorar la capacidad predictiva.

  ---

# 7.Referencias

<a id="ref1"></a>

[1] U.S. Environmental Protection Agency, "AirData: Air Quality Data Collected at Outdoor Monitors Across the US," EPA. [Online]. Available: https://www.epa.gov/outdoor-air-quality-data.


<a id="ref2"></a>

[2] F. Pedregosa et al., "Scikit-learn: Machine Learning in Python," Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.


<a id="ref3"></a>

[3] W. McKinney, "Data Structures for Statistical Computing in Python," in Proceedings of the 9th Python in Science Conference, pp. 56–61, 2010.


<a id="ref4"></a>

[4] M. L. Waskom, "seaborn: Statistical Data Visualization," Journal of Open Source Software, vol. 6, no. 60, p. 3021, 2021.


<a id="ref5"></a>

[5] J. D. Hunter, "Matplotlib: A 2D Graphics Environment," Computing in Science & Engineering, vol. 9, no. 3, pp. 90–95, 2007.
