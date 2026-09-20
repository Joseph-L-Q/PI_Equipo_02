# Análisis de la Calidad del Aire mediante Regresión Lineal: Dióxido de Azufre ($SO_2$) en Alabama, EE. UU. (2022 – 2023)

---

**Componente analizado:** Dióxido de azufre ($SO_2$)

**Período de estudio:** 1 de enero de 2022 – 31 de diciembre de 2023

**Área geográfica:** Alabama, Estados Unidos

**Fuente de datos:** Air Quality System (AQS), U.S. Environmental Protection Agency (EPA)

**Unidad de medida:** Partes por billón (ppb)

**Registros analizados:** 3,581 observaciones diarias

### Localización del estudio

Los datos provienen de la red de monitoreo ambiental del estado de Alabama, enfocándose en la estación principal de control industrial y urbano:

| Dato | Valor |
|---|---|
| Estado | Alabama |
| Condado | Jefferson |
| Ciudad / Área | Birmingham (North Birmingham) |
| Estación de monitoreo | North Birmingham |
| Identificador (Site ID) | 10730023 |
| Latitud | 33.553056° N |
| Longitud | −86.815000° O |

El condado de Jefferson, donde se ubica la estación de North Birmingham, alberga un núcleo histórico de actividad industrial pesada, manufactura metalúrgica y fundición de hierro en el sureste de Estados Unidos. A diferencia de zonas puramente rurales, esta localización presenta focos puntuales de emisión industrial combinados con tráfico urbano denso. Este contexto resulta de gran valor analítico para evaluar el comportamiento del $SO_2$, ya que permite determinar si los modelos estadísticos tradicionales de regresión lineal pueden predecir las concentraciones diarias de dióxido de azufre en presencia de variaciones industriales y dinámicas atmosféricas locales.

---

## 1. Introducción

### 1.1 Contexto del problema

El dióxido de azufre ($SO_2$) es un gas incoloro, reactivo y de olor penetrante que pertenece a la familia de los óxidos de azufre ($SO_x$). Se genera principalmente durante la combustión de fósiles que contienen azufre (como el carbón y el petróleo) en plantas generadoras de energía eléctrica, refinerías, fundiciones e instalaciones industriales, así como por la combustión de diésel en equipos pesados [1]. Su estudio e integración en sistemas de vigilancia ambiental responde a dos factores fundamentales.

En primer lugar, el $SO_2$ es un contaminante primario con un impacto severo sobre el sistema respiratorio humano. Exposiciones incluso de corta duración (desde 10 minutos) pueden desencadenar broncocontricción, crisis de asma y reducción de la función pulmonar, afectando de manera desproporcionada a niños, adultos mayores y personas con enfermedades pulmonares crónicas preexistentes [1].

En segundo lugar, el dióxido de azufre actúa como un precursor crítico en la química atmosférica. Al reaccionar con el vapor de agua y otros compuestos en la atmósfera, se transforma en ácido sulfúrico ($H_2SO_4$), el principal componente de la lluvia ácida, y contribuye sustancialmente a la formación de sulfatos secundarios que integran el material particulado fino ($PM_{2.5}$), deteriorando la visibilidad y alterando la acidez de suelos y ecosistemas acuáticos [2].

### 1.2 Justificación del área de estudio

El estado de Alabama, y en particular la zona industrial de North Birmingham, ofrece un escenario idóneo para la evaluación de modelos predictivos de calidad del aire. Al albergar complejos industriales y plantas térmicas operativas durante los años 2022 y 2023, la serie temporal presenta variabilidad en los picos de concentración de $SO_2$. Evaluar un modelo predictivo supervisado sobre esta serie permite determinar el alcance y las limitaciones de los métodos econométricos lineales frente a fenómenos regulados por variables meteorológicas y operativas no observadas.

### 1.3 Objetivos

**Objetivo general**

Evaluar la capacidad predictiva de un modelo de regresión lineal múltiple para estimar la concentración máxima diaria de $SO_2$ registrada en la estación de North Birmingham, Alabama, durante los años 2022 y 2023, a partir de variables temporales y métricas de cobertura de muestreo.

**Objetivos específicos**

- Realizar un análisis exploratorio de datos sobre los 3,581 registros diarios que componen la base histórica descargada.
- Caracterizar estadísticamente la distribución del $SO_2$ mediante medidas de tendencia central, dispersión, sesgo y valores extremos.
- Evaluar la asociación lineal entre las variables independientes y la variable respuesta a través de la matriz de correlación de Pearson.
- Construir, entrenar y validar un modelo de regresión lineal múltiple aplicando una partición aleatoria de datos de entrenamiento ($70\%$) y prueba ($30\%$).
- Diagnosticar el cumplimiento de los supuestos estadísticos de la regresión lineal (linealidad, normalidad de residuos y homocedasticidad).
- Comparar el desempeño predictivo del modelo lineal con un algoritmo no paramétrico de Árbol de Decisión para Regresión.
- Validar formalmente la significancia estadística global e individual mediante pruebas de hipótesis F y t de Student con mínimos cuadrados ordinarios (OLS).

### 1.4 Hipótesis de trabajo

El análisis inferencial del modelo de regresión se plantea bajo el siguiente contraste de hipótesis:

- **Hipótesis nula ($H_0$):** Los coeficientes de regresión son conjuntamente iguales a cero ($\beta_1 = \beta_2 = \dots = \beta_k = 0$), lo que indica que las variables predictoras no explican la variabilidad observada en la concentración de $SO_2$.
- **Hipótesis alternativa ($H_1$):** Al menos uno de los coeficientes de regresión es diferente de cero ($\beta_j \neq 0$), confirmando una relación lineal significativa entre los predictores y la concentración máxima diaria de $SO_2$.

Para la toma de decisiones estadísticas se fija un nivel de significancia estandarizado de $\alpha = 0.05$ ($95\%$ de confianza).

---

## 2. Metodología

### 2.1 Enfoque y diseño

La investigación sigue un enfoque cuantitativo con alcance correlacional y predictivo. El diseño es de tipo no experimental y longitudinal retrospectivo, puesto que no se manipularon variables ambientales de forma directa; el análisis se ejecutó a partir de las series históricas de monitoreo continuo generadas por la red oficial de calidad del aire para evaluar la capacidad predictiva de los modelos ajustados.

### 2.2 Fuente y obtención de los datos

Los datos primarios se obtuvieron a través del sistema Air Quality System (AQS), la plataforma oficial de datos públicos de calidad del aire de la Agencia de Protección Ambiental de los Estados Unidos (U.S. EPA) [3]. Esta plataforma almacena los registros recopilados por las estaciones estatales de control ambiental.

El flujo de obtención de la información constó de las siguientes fases:

1. Acceso al portal público de datos de aire exterior de la U.S. EPA (`Download Daily Data`).
2. Selección del contaminante de estudio: Dióxido de Azufre ($SO_2$, Código AQS: 42401).
3. Filtrado por período temporal completo: del 1 de enero de 2022 al 31 de diciembre de 2023.
4. Selección del nivel de agregación diario (`Daily Data`).
5. Descarga del archivo final en formato CSV (`SO2_daily_aqs_data_downloaded_2026-09-19 23_09_37.csv`).

<p align="center">
  <img src="URL_IMAGEN_BUSQUEDA_EPA" alt="Descarga de datos de SO2 en la plataforma AQS de la EPA" width="90%"/>
  <br>
  <em>Figura 1. Interfaz de filtrado y descarga de datos de $SO_2$ en el sistema AQS de la EPA.</em>
</p>

El archivo descargado comprende un total de **3,581 observaciones diarias**, donde cada registro incluye la concentración máxima diaria de $SO_2$ expresada en partes por billón (ppb), junto con parámetros de ubicación, metadatos de muestreo y fechas de medición.

### 2.3 Herramientas computacionales

El procesamiento, modelado y validación de los datos se realizó en un entorno interactivo Jupyter Notebook respaldado por Python 3. Se emplearon las librerías especializadas en ciencia de datos y aprendizaje automático descritas a continuación:

| Biblioteca | Alias | Sentencia de importación | Función en el estudio | Ref. |
|---|---|---|---|---|
| `numpy` | `np` | `import numpy as np` | Operaciones matriciales, vectores numéricos y cálculo de errores estándar | [4] |
| `pandas` | `pd` | `import pandas as pd` | Carga, limpieza, estructuración y agregación de tablas de datos (`DataFrame`) | [5] |
| `matplotlib.pyplot` | `plt` | `import matplotlib.pyplot as plt` | Creación de gráficos estadísticos base (histogramas, dispersión y barras) | [6] |
| `seaborn` | `sns` | `import seaborn as sns` | Visualización avanzada: matrices de correlación, mapas de calor y estimaciones de densidad | [7] |
| `scikit-learn` | — | `from sklearn... import ...` | Partición de datos (`train_test_split`), regresión lineal, árbol de decisión y métricas | [8] |
| `statsmodels.api` | `sm` | `import statsmodels.api as sm` | Análisis estadístico inferencial formal por Mínimos Cuadrados Ordinarios (OLS) | [9] |

### 2.4 Funciones y métodos empleados

#### Tabla resumen de comandos

La siguiente tabla compila las funciones de Python ejecutadas secuencialmente en el notebook de trabajo:

| # | Comando o función | Biblioteca | Etapa | Propósito | Resultado |
|---|---|---|---|---|---|
| 1 | `pd.read_csv()` | pandas | Carga | Carga el dataset en memoria como `DataFrame` | Tabla de 3,581 × 28 |
| 2 | `df.head()` | pandas | Inspección | Muestra los primeros 5 registros de la tabla | Validación de estructura |
| 3 | `df.info(verbose=True)` | pandas | Inspección | Reporta columnas, no nulos y tipos de dato | Identificación de metadatos |
| 4 | `df.describe().round(2)` | pandas | Descriptiva | Calcula medidas estadísticas multivariadas | Media, std, min, max, cuartiles |
| 5 | `df.columns` | pandas | Inspección | Lista el catálogo de nombres de variables | Identificación de columnas |
| 6 | `pd.to_datetime()` | pandas | Limpieza | Convierte texto de fechas a tipo `datetime64` | Estandarización de fechas |
| 7 | `.dt.year`, `.dt.month`, `.dt.day`, `.dt.dayofweek` | pandas | Nuevas variables | Extrae componentes temporales individuales | 4 predictores temporales |
| 8 | `df[[...]]` | pandas | Limpieza | Selecciona columnas de interés operativo | Reducción de 28 a 7 columnas |
| 9 | `df.rename(columns={})` | pandas | Limpieza | Renombra columnas a nombres cortos | Normalización de nombres |
| 10 | `sns.pairplot()` | seaborn | Exploración | Grafica dispersiones cruzadas entre variables | Matriz de dispersión general |
| 11 | `.plot.hist(bins=25)` | pandas | Exploración | Genera el histograma de frecuencias | Distribución empírica del $SO_2$ |
| 12 | `.plot.density()` | pandas | Exploración | Estima la curva de densidad de probabilidad | Estimación Kernel de densidad |
| 13 | `df.select_dtypes()` | pandas | Correlación | Filtra únicamente las columnas numéricas | Subconjunto numérico |
| 14 | `.corr()` | pandas | Correlación | Calcula la matriz de correlación de Pearson | Matriz de 7 × 7 |
| 15 | `sns.heatmap(annot=True)` | seaborn | Correlación | Grafica la matriz mediante mapa de calor | Representación de colinealidad |
| 16 | `train_test_split()` | scikit-learn | Partición | Divide los datos en entrenamiento y prueba | 2,506 entrenamiento / 1,075 prueba |
| 17 | `LinearRegression()` | scikit-learn | Modelado | Instancia el estimador de regresión lineal | Objeto `lm` |
| 18 | `lm.fit()` | scikit-learn | Entrenamiento | Entrena el modelo ajustando mínimos cuadrados | Coeficientes $\beta_0$ y $\beta_j$ |
| 19 | `lm.intercept_` | scikit-learn | Resultados | Devuelve el término independiente ($\beta_0$) | Intercepto del modelo |
| 20 | `lm.coef_` | scikit-learn | Resultados | Devuelve los coeficientes de las variables ($\beta_j$) | Vector de coeficientes |
| 21 | `lm.predict()` | scikit-learn | Predicción | Genera predicciones sobre $X_{\text{test}}$ | Vector de 1,075 predicciones |
| 22 | `np.square()`, `np.sum()`, `np.sqrt()` | numpy | Inferencia | Calcula el error estándar manual de $\beta$ | Errores estándar y estadístico $t$ |
| 23 | `gridspec.GridSpec(2, 3)` | matplotlib | Visualización | Organiza submódulos de gráficos en rejilla | Dispersiones individuales |
| 24 | `sns.histplot(kde=True)` | seaborn | Diagnóstico | Grafica el histograma de residuos con densidad | Verificación de normalidad |
| 25 | `plt.scatter()` | matplotlib | Diagnóstico | Dispersión de reales vs. predichos y residuos | Evaluación de homocedasticidad |
| 26 | `tree.DecisionTreeRegressor()` | scikit-learn | Contraste | Instancia el árbol de decisión (`max_depth=5`) | Modelo no lineal |
| 27 | `tree_model.feature_importances_` | scikit-learn | Interpretación | Mide la importancia de las características | Vector de importancias |
| 28 | `metrics.mean_squared_error()` | scikit-learn | Evaluación | Calcula el Error Cuadrático Medio ($MSE$) | Métrica de evaluación $MSE$ |
| 29 | `plt.barh()` | matplotlib | Visualización | Grafica barras horizontales de importancias | Gráfico de importancia |
| 30 | `sm.add_constant()` | statsmodels | Inferencia | Agrega la columna de unos para la constante | Matriz de diseño $X_s$ |
| 31 | `sm.OLS().fit()` | statsmodels | Inferencia | Ajusta el modelo OLS formal | Objeto de resultados estadísticos |
| 32 | `.summary()` | statsmodels | Inferencia | Despliega la tabla completa de inferencia OLS | Reporte estadístico formal |

#### 2.4.1 Carga e inspección

El flujo inicia cargando el archivo descargado mediante **`pd.read_csv()`**. Posteriormente, **`df.head()`** permite revisar los primeros cinco registros para validar la codificación y estructura del archivo. Mediante **`df.info(verbose=True)`** se verifica el número total de observaciones (3,581), el catálogo de 28 columnas iniciales y la presencia de valores nulos. Con **`df.describe().round(2)`** se obtiene un resumen inicial de métricas cuantitativas clave, y **`df.columns`** extrae los nombres exactos de los campos disponibles.

#### 2.4.2 Limpieza y transformación de datos

La variable `Date` fue convertida de cadena de texto a tipo `datetime64` mediante **`pd.to_datetime()`**. A partir de esta transformación, se aplicó ingeniería de características utilizando los métodos **`.dt.year`**, **`.dt.month`**, **`.dt.day`** y **`.dt.dayofweek`** para extraer cuatro componentes temporales explicativos.

Posteriormente, se redujo la dimensionalidad del conjunto filtrando siete variables de interés y descartando metadatos constantes o repetitivos. Finalmente, mediante **`df.rename(columns={...})`** se renombraron los campos para estandarizar el código: `Obs_Count` (conteo de observaciones), `Percent_Complete` (porcentaje de completitud) y `SO2_Max` (concentración máxima diaria de $SO_2$).

#### 2.4.3 Análisis exploratorio y visualización

Se utilizó **`sns.pairplot()`** para generar una matriz gráfica multivariada de dispersión. La distribución univariada de la variable objetivo `SO2_Max` se analizó combinando un histograma con 25 intervalos (**`.plot.hist(bins=25)`**) y una función de estimación de densidad por núcleo (**`.plot.density()`**).

Para evaluar las relaciones lineales pareadas, se filtraron las variables numéricas con **`df.select_dtypes()`**, calculando la matriz de correlación de Pearson con **`.corr()`** y proyectándola mediante un mapa de calor con **`sns.heatmap(annot=True)`**.

#### 2.4.4 Separación de variables y partición de datos

Se estructuraron la matriz de variables independientes ($X$, 6 predictores) y el vector dependiente ($Y$, `SO2_Max`):

```python
X = df[l_column[0:len_feature-1]]   # Matriz de predictores (6 columnas)
Y = df[l_column[len_feature-1]]     # Vector objetivo (SO2_Max)
