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

La investigación se enmarca en el enfoque cuantitativo y posee un alcance correlacional-predictivo. El diseño metodológico es no experimental y longitudinal retrospectivo, dado que las variables no fueron manipuladas deliberadamente en un entorno controlado. En su lugar, se analizaron las series temporales históricas de monitoreo continuo generadas por la red oficial de vigilancia ambiental de la Agencia de Protección Ambiental de Estados Unidos (U.S. EPA), con el propósito de examinar las relaciones de asociación lineal y evaluar la capacidad predictiva de los modelos econométricos y de aprendizaje automático supervisado.

### 2.2 Fuente y obtención de los datos

Los datos primarios se obtuvieron a través del sistema *Air Quality System* (AQS), la plataforma oficial de datos públicos de calidad del aire exterior de la U.S. EPA [3]. Esta base de datos reúne las mediciones recopiladas por las estaciones de control ambiental estatales y locales, permitiendo filtrar la información por contaminante, área geográfica y rango temporal.

El procedimiento de descarga y preparación de la información siguió estos pasos:

1. Ingreso al portal de datos de calidad del aire exterior de la U.S. EPA (`Download Daily Data`).
2. Selección del Dióxido de Azufre ($SO_2$, Código de Parámetro AQS: 42401) como contaminante de interés.
3. Delimitación geográfica al estado de Alabama, enfocando la selección en la estación de monitoreo industrial de *North Birmingham* (Condado de Jefferson, Site ID: 10730023).
4. Configuración del rango temporal continuo entre el 1 de enero de 2022 y el 31 de diciembre de 2023.
5. Descarga del archivo final en formato delimitado por comas (CSV) denominado `SO2_daily_aqs_data_downloaded_2026-09-19 23_09_37.csv`.

<img width="1102" height="615" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/1.png" />

**Figura 1.** Interfaz de filtrado y descarga de datos de calidad del aire ($SO_2$) en el portal AQS de la EPA.

El archivo consolidado comprende un total de **3,581 registros diarios**, cubriendo los 730 días lectivos del período 2022–2023 repartidos entre los distintos monitores operativos de la zona. Cada observación representa una jornada completa de monitoreo, y la variable respuesta fundamental es la concentración máxima horaria diaria de $SO_2$, medida en partes por billón (ppb).

### 2.3 Herramientas computacionales

El procesamiento, modelado predictivo y diagnóstico estadístico se desarrollaron íntegramente en un entorno interactivo Jupyter Notebook utilizando el lenguaje de programación Python 3. Este entorno permite mantener la reproducibilidad total del flujo de trabajo sin requerir compiladores externos.

Las bibliotecas científicas especializadas empleadas en el proyecto se detallan en la siguiente tabla:

| Biblioteca | Alias | Sentencia de importación | Propósito y aplicaciones en el estudio | Ref. |
|---|---|---|---|---|
| `numpy` | `np` | `import numpy as np` | Operaciones matriciales y cálculo vectorial para la determinación de los errores estándar | [4] |
| `pandas` | `pd` | `import pandas as pd` | Carga, estructuración, limpieza e ingeniería de características sobre la estructura de `DataFrame` | [5] |
| `matplotlib.pyplot` | `plt` | `import matplotlib.pyplot as plt` | Construcción de la infraestructura gráfica base: histogramas, dispersiones y gráficos de barras | [6] |
| `seaborn` | `sns` | `import seaborn as sns` | Visualización estadística avanzada: matrices de correlación, mapas de calor y curvas KDE | [7] |
| `scikit-learn` | — | `from sklearn... import ...` | Partición de datos, ajuste de Regresión Lineal, Árboles de Decisión y métricas de error ($MSE$, $MAE$) | [8] |
| `statsmodels.api` | `sm` | `import statsmodels.api as sm` | Validación inferencial formal por Mínimos Cuadrados Ordinarios (OLS) y pruebas de hipótesis | [9] |

Es relevante señalar que la instrucción `%matplotlib inline` corresponde a un comando mágico (*magic command*) propio de los entornos Jupyter/Colab. Su función es renderizar las figuras de manera estática dentro de las salidas del notebook, evitando la apertura de ventanas flotantes independientes.

---

### 2.4 Funciones y métodos empleados

#### Tabla resumen de comandos

La siguiente tabla resume la totalidad de las funciones ejecutadas en el código, organizadas cronológicamente según la etapa metodológica correspondiente:

| # | Comando o función | Biblioteca | Etapa | Qué hace | Resultado obtenido |
|---|---|---|---|---|---|
| 1 | `pd.read_csv()` | pandas | Carga | Lee el archivo CSV y lo transforma en tabla estructurada | `DataFrame` de 3,581 × 28 |
| 2 | `df.head()` | pandas | Inspección | Despliega las primeras 5 observaciones de la tabla | Inspección visual de carga |
| 3 | `df.info(verbose=True)` | pandas | Inspección | Reporta tipos de dato, conteo y detección de vacíos | Verificación de integridad |
| 4 | `df.describe().round(2)` | pandas | Descriptiva | Computa medidas de tendencia central, dispersión y rango | Media, desviación, min, max |
| 5 | `df.columns` | pandas | Inspección | Devuelve el listado completo de variables del dataset | Lista de 28 atributos |
| 6 | `pd.to_datetime()` | pandas | Limpieza | Convierte la columna de texto `Date` a tipo fecha | Atributo en formato `datetime64` |
| 7 | `.dt.year`, `.dt.month`, `.dt.day`, `.dt.dayofweek` | pandas | Transformación | Extrae las componentes del calendario de cada registro | 4 nuevas variables temporales |
| 8 | `df[[...]]` | pandas | Seleccion | Filtra únicamente las columnas de interés analítico | Reducción a 7 columnas útiles |
| 9 | `df.rename(columns={})` | pandas | Limpieza | Estandariza los nombres de las variables | `Obs_Count`, `Percent_Complete`, `SO2_Max` |
| 10 | `sns.pairplot()` | seaborn | Exploración | Genera una matriz gráfica cruzada entre variables | Figura 4 |
| 11 | `.plot.hist(bins=25)` | pandas | Exploración | Dibuja la distribución de frecuencias de $SO_2$ | Figura 5 |
| 12 | `.plot.density()` | pandas | Exploración | Dibuja la estimación de densidad por núcleo (KDE) | Figura 6 |
| 13 | `df.select_dtypes()` | pandas | Correlación | Aísla únicamente las variables de naturaleza numérica | Subconjunto cuantitativo |
| 14 | `.corr()` | pandas | Correlación | Computa la matriz de correlación lineal de Pearson | Matriz de 7 × 7 |
| 15 | `sns.heatmap(annot=True)` | seaborn | Correlación | Proyecta la matriz de correlación como mapa de calor | Figura 8 |
| 16 | `train_test_split()` | scikit-learn | Partición | Divide el dataset de forma aleatoria (70% / 30%) | 2,506 entrenamiento y 1,075 prueba |
| 17 | `LinearRegression()` | scikit-learn | Modelado | Instancia el estimador de regresión lineal múltiple | Objeto estimador `lm` |
| 18 | `lm.fit()` | scikit-learn | Entrenamiento | Modela los coeficientes por Mínimos Cuadrados | Modelo entrenado |
| 19 | `lm.intercept_` | scikit-learn | Resultados | Devuelve la constante o término independiente $\beta_0$ | $\beta_0 = -1991.79$ |
| 20 | `lm.coef_` | scikit-learn | Resultados | Devuelve el vector de coeficientes de las pendientes $\beta_j$ | Arreglo de 6 betas |
| 21 | `lm.predict()` | scikit-learn | Predicción | Aplica la ecuación estimada sobre datos no vistos | 1,075 predicciones de prueba |
| 22 | `np.square()`, `np.sum()`, `np.sqrt()` | numpy | Inferencia | Realiza la formulación vectorial de errores estándar | Errores estándar y estadísticos $t$ |
| 23 | `gridspec.GridSpec(2, 3)` | matplotlib | Visualización | Distribuye 6 subgráficos de dispersión en cuadrícula | Figura 12 |
| 24 | `sns.histplot(kde=True)` | seaborn | Diagnóstico | Grafica el histograma de residuos con densidad KDE | Figura 14 |
| 25 | `plt.scatter()` | matplotlib | Diagnóstico | Dispersión de valores reales vs. predichos y residuos | Figuras 13, 15 y 17 |
| 26 | `tree.DecisionTreeRegressor()` | scikit-learn | Contraste | Ajusta un Árbol de Decisión (`max_depth=5`) | Modelo no paramétrico |
| 27 | `tree_model.feature_importances_` | scikit-learn | Interpretación | Mide la reducción de impureza/varianza por predictor | Figura 18 |
| 28 | `metrics.mean_squared_error()` | scikit-learn | Evaluación | Computa el Error Cuadrático Medio sobre la prueba | $MSE = 25.105$ |
| 29 | `plt.barh()` | matplotlib | Visualización | Genera un gráfico de barras horizontales de importancia | Figura 18 |
| 30 | `sm.add_constant()` | statsmodels | Inferencia | Añade una columna unitaria para la estimación de $\beta_0$ | Matriz de diseño $X_s$ |
| 31 | `sm.OLS().fit()` | statsmodels | Inferencia | Ajusta el modelo OLS paramétrico completo | Reporte de resultados OLS |
| 32 | `.summary()` | statsmodels | Inferencia | Despliega la tabla formal de métricas e inferencia | Figura 16 |

#### 2.4.1 Carga e inspección

El flujo de trabajo inicia con **`pd.read_csv(ruta)`**, comando encargado de cargar el archivo delimitado por comas desde la memoria local y estructurarlo como un `DataFrame` de pandas.

Una vez cargada la estructura, se ejecuta **`df.head()`** para visualizar las primeras cinco filas. Este paso permite validar que los encabezados coincidan con el estándar AQS de la EPA y que la separación de columnas se haya efectuado adecuadamente.

El siguiente comando es **`df.info(verbose=True)`**, que reporta la cantidad total de filas (3,581), el catálogo de columnas, los tipos de datos asignados (`int64`, `float64`, `object`) y el recuento de valores no nulos. Esta inspección es fundamental para detectar la presencia de datos faltantes antes de iniciar la fase de modelado.

Posteriormente, con **`df.describe().round(2)`** se genera un cuadro sintético de métricas descriptivas cuantitativas para las variables numéricas (conteo, media, desviación estándar, mínimo, percentiles 25%, 50%, 75% y máximo). El método `.round(2)` garantiza la legibilidad al acotar los resultados a dos decimales.

Finalmente, **`df.columns`** extrae la lista completa de identificadores de columna, facilitando su selección e invocación precisa en el código.

#### 2.4.2 Limpieza y transformación

La columna cronológica original fue importada como tipo texto (`object`). Por ello, se aplicó la transformación **`pd.to_datetime(df['Date'])`**, convirtiéndola a una estructura de fecha nativa `datetime64`. Sin esta conversión, resulta imposible aplicar operaciones matemáticas o extracciones temporales.

A partir de la columna estandarizada, los métodos **`.dt.year`, `.dt.month`, `.dt.day` y `.dt.dayofweek`** permitieron descomponer la fecha en sus elementos constitutivos. Este procedimiento de ingeniería de características genera cuatro predictores temporales clave. El accesorio `dayofweek` codifica los días de la semana de forma numérica continua del 0 al 6 (donde 0 representa al lunes y 6 al domingo).

Seguidamente, se filtraron únicamente 7 columnas de las 28 originales. Se descartaron atributos constantes en la estación de *North Birmingham* (como identificadores geográficos, coordenadas e información de la agencia de monitoreo) y variables completamente vacías. La razón teórica de este descarte radica en que una variable sin varianza ($Var(X) = 0$) es incapaz de explicar la variabilidad de una respuesta.

Por último, **`df.rename(columns={...})`** se utilizó para acortar los nombres de los atributos clave, eliminando espacios para agilizar su sintaxis en las fórmulas: `Obs_Count`, `Percent_Complete` y `SO2_Max`.

#### 2.4.3 Análisis exploratorio y visualización

La evaluación exploratoria multivariada comienza con **`sns.pairplot(df)`**, que construye una matriz cuadrada de gráficos donde cada variable se cruza individualmente con todas las demás. La diagonal principal presenta los histogramas univariados, mientras que las celdas fuera de la diagonal despliegan diagramas de dispersión para detectar visualmente no linealidades, agrupamientos o correlaciones aparentes.

Para estudiar la variable objetivo por separado se usaron dos gráficos complementarios:
1. **`.plot.hist(bins=25)`**: Agrupa el rango de concentraciones de $SO_2$ en 25 intervalos contiguos, mostrando la frecuencia absoluta de días en cada tramo.
2. **`.plot.density()`**: Evalúa la Estimación de Densidad por Núcleo (KDE), la cual proporciona una representación suave y continua de la distribución de probabilidad subyacente de la masa de contaminantes.

Antes de determinar las asociaciones pareadas, se utilizó **`df.select_dtypes(include=[np.number])`** para aislar únicamente el subconjunto de variables cuantitativas. Sobre este subconjunto se aplicó **`.corr()`**, obteniendo la matriz de correlación de Pearson.

Esa matriz se representó mediante el mapa de calor **`sns.heatmap(matriz, annot=True, linewidths=2)`**. El argumento `annot=True` escribe el valor numérico exacto de cada coeficiente dentro de su celda, mientras que `linewidths=2` añade líneas de separación gráfica.

#### 2.4.4 Separación de variables y partición de datos

La separación de características sigue el esquema clásico del aprendizaje supervisado:

```python
X = df[l_column[0:len_feature-1]]   # Matriz de predictores (6 columnas explicativas)
Y = df[l_column[len_feature-1]]     # Vector objetivo (SO2_Max)
```

La función **`train_test_split(X, Y, test_size=0.3, random_state=123)`** divide el conjunto en cuatro partes de forma aleatoria. Sus parámetros funcionan de la siguiente manera:

| Parámetro | Valor usado | Qué significa | Efecto en este trabajo |
|---|---|---|---|
| `X` | Tabla de 3581 × 6 | Matriz de predictores | Las seis variables explicativas |
| `Y` | Serie de 3581 valores | Vector objetivo | La variable `SO2_Max` |
| `test_size` | `0.3` | Proporción destinada a prueba | 1075 registros |
| `train_size` | `0.7` (implícito) | Proporción destinada a entrenamiento | 2506 registros |
| `random_state` | `123` | Semilla del generador aleatorio | Garantiza la reproducibilidad |
| `shuffle` | `True` (por defecto) | Mezcla los datos antes de dividir | Evita el sesgo por orden cronológico |

Los cuatro objetos que devuelve la función son los siguientes:

| Objeto | Contenido | Tamaño |
|---|---|---|
| `X_train` | Predictores de entrenamiento | 2506 × 6 |
| `X_test` | Predictores de prueba | 1075 × 6 |
| `Y_train` | Valores reales de entrenamiento | 2506 |
| `Y_test` | Valores reales de prueba | 1075 |

El propósito fundamental de esta partición es mitigar el riesgo de sobreajuste (*overfitting*) durante la evaluación del modelo [10], [11]. Evaluar el rendimiento de un algoritmo utilizando el mismo conjunto de datos con el que fue ajustado genera métricas de precisión infladas o artificialmente optimistas, ya que la función ajustada tiende a memorizar el ruido inherente a la muestra de entrenamiento. Al reservar un subconjunto de prueba independiente que no interviene en el ajuste, se logra medir con rigor la capacidad real de generalización del estimador ante observaciones completamente nuevas [8], [10].

El parámetro `random_state=123` merece una mención aparte. Al fijar la semilla del generador de números pseudoaleatorios, se asegura que cualquier persona que ejecute el notebook obtenga exactamente la misma partición, y por lo tanto los mismos resultados. Sin esta semilla, cada ejecución arrojaría números ligeramente distintos.

#### 2.4.5 Modelo de regresión lineal

El estimador se crea con **`LinearRegression()`**, que ajusta un modelo de la forma:

$$\hat{Y} = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_6 X_6$$

El ajuste se realiza por el método de mínimos cuadrados ordinarios, que busca los coeficientes capaces de minimizar la suma de los cuadrados de los residuos:

$$\min \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

Los métodos y atributos del modelo son los siguientes:

| Elemento | Tipo | Sintaxis | Qué devuelve |
|---|---|---|---|
| `LinearRegression()` | Constructor | `lm = LinearRegression()` | El objeto del modelo, aún sin entrenar |
| `.fit(X, Y)` | Método | `lm.fit(X_train, Y_train)` | El mismo objeto, ya ajustado |
| `.intercept_` | Atributo | `lm.intercept_` | El término independiente $\beta_0$ |
| `.coef_` | Atributo | `lm.coef_` | Los seis coeficientes $\beta_1$ a $\beta_6$ |
| `.predict(X)` | Método | `lm.predict(X_test)` | Un arreglo con 1,075 predicciones |

La diferencia entre método y atributo vale la pena señalarla. Los métodos llevan paréntesis porque ejecutan una acción, mientras que los atributos terminan en guion bajo. Esa convención de scikit-learn indica que el valor se aprendió durante el entrenamiento, de modo que no existe hasta que se llama a `.fit()` [8].

En cuanto a la interpretación, cada coeficiente representa el cambio esperado en la concentración de $SO_2$ cuando la variable correspondiente aumenta en una unidad y todas las demás se mantienen constantes. El desarrollo formal del estimador y de sus propiedades puede consultarse en [12].

#### 2.4.6 Inferencia sobre los coeficientes

Para saber si un coeficiente es distinto de cero por una razón real o simplemente por azar muestral, se calcularon manualmente el error estándar y el estadístico t de cada uno.

Primero se determinaron los grados de libertad como `dfN = n − k`, donde n son las 2,506 observaciones de entrenamiento y k los 6 predictores. Luego se obtuvo la suma de cuadrados del error mediante `np.sum(np.square(train_pred − Y_train))`. A partir de ahí se calculó el error estándar, que mide la incertidumbre asociada a cada estimación, y finalmente el estadístico t, que resulta de dividir el coeficiente entre su error estándar.

Ese estadístico indica a cuántos errores estándar de distancia del cero se encuentra el coeficiente estimado. Como regla práctica, un valor absoluto mayor que 1.96 sugiere significancia al nivel del 5 %.

#### 2.4.7 Verificación de supuestos

La regresión lineal descansa sobre cuatro supuestos que conviene comprobar antes de dar por válidos sus resultados:

| Supuesto | Qué exige | Cómo se verificó | Figura |
|---|---|---|---|
| Linealidad | La relación entre predictores y respuesta debe ser recta | Diagramas de dispersión individuales | Figura 12 |
| Normalidad de residuos | Los errores deben distribuirse normalmente en torno a cero | Histograma de residuos con curva de densidad | Figura 14 |
| Homocedasticidad | La varianza del error debe ser constante | Residuos frente a valores predichos | Figura 15 |
| Independencia | Las observaciones no deben estar correlacionadas entre sí | Estadístico de Durbin-Watson (no aplicado) | — |

El tratamiento formal de estos supuestos y de las consecuencias que acarrea su incumplimiento puede consultarse en [12] y [13].

#### 2.4.8 Modelo de contraste: árbol de decisión

Para tener un punto de comparación se ajustó un segundo modelo con **`tree.DecisionTreeRegressor(max_depth=5, random_state=10)`**. Se trata de un modelo no paramétrico que va partiendo el espacio de los predictores mediante reglas de decisión sucesivas. A diferencia de la regresión lineal, puede capturar relaciones curvas e interacciones entre variables sin que haya que especificarlas de antemano [11].

| Parámetro | Valor | Qué controla |
|---|---|---|
| `max_depth` | `5` | El número máximo de niveles de división, y con ello la complejidad del modelo |
| `random_state` | `10` | La semilla que desempata divisiones equivalentes |
| `criterion` | `squared_error` (por defecto) | La medida que se minimiza en cada partición |

El atributo **`tree_model.feature_importances_`** devuelve la importancia relativa de cada predictor, calculada como la reducción total de varianza que aporta esa variable a lo largo de todas las divisiones del árbol. Los valores están normalizados y suman uno.

Para evaluar el desempeño se empleó **`metrics.mean_squared_error(Y_test, tree_pred)`**, que promedia los cuadrados de las diferencias entre los valores reales y los predichos.

#### 2.4.9 Validación estadística formal

El último paso consistió en repetir el ajuste con `statsmodels`, que ofrece un reporte estadístico mucho más completo que scikit-learn.

La función **`sm.add_constant(X)`** agrega una columna de unos a la matriz de predictores, paso necesario para que la biblioteca estime el término independiente. Luego **`sm.OLS(Y, Xs).fit()`** ajusta el modelo por mínimos cuadrados ordinarios sobre el conjunto completo, y **`.summary()`** genera el reporte.

Ese reporte contiene los siguientes indicadores:

| Indicador | Qué mide | Cómo se lee |
|---|---|---|
| `R-squared` | La proporción de varianza explicada | Va de 0 a 1, y cuanto más alto, mejor |
| `Adj. R-squared` | El $R^2$ penalizado por la cantidad de predictores | Si resulta negativo, el modelo es peor que predecir la media |
| `F-statistic` | La significancia conjunta de todos los coeficientes | Un valor alto indica un modelo más significativo |
| `Prob (F-statistic)` | El p-valor de la prueba F global | Si es menor que 0.05, se rechaza $H_0$ |
| `coef` | El valor estimado de cada coeficiente | Indica el cambio en Y por unidad de X |
| `std err` | La incertidumbre de cada estimación | Cuanto mayor, menos precisa es la estimación |
| `t` | El coeficiente dividido entre su error estándar | Un valor absoluto mayor que 1.96 sugiere significancia |
| `P>\|t\|` | El p-valor individual de cada coeficiente | Si es menor que 0.05, la variable es significativa |
| `[0.025, 0.975]` | El intervalo de confianza al 95 % | Si contiene el cero, el efecto no es concluyente |
| `AIC` y `BIC` | Criterios de información | Cuanto menores, mejor el equilibrio entre ajuste y simplicidad |
| `No. Observations` | El tamaño de la muestra | 3,581 |
| `Df Residuals` | Los grados de libertad residuales | 3,574 |
| `Df Model` | La cantidad de predictores | 6 |

El marco teórico de estos indicadores se desarrolla en [15].

---

## 3. Resultados

### 3.1 Estructura del conjunto de datos

La inspección inicial confirmó que el archivo descargado contiene **3,581 registros diarios** y 28 columnas originales. Tras el proceso de limpieza y selección de características, la matriz de trabajo quedó conformada por 7 variables procesadas sin ningún valor faltante, lo que permitió desarrollar el modelado sobre el 100% de la muestra.

<img width="1102" height="615" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/2.png" />

**Figura 2.** Salida del comando `df.info(verbose=True)` para la estructura depurada.

### 3.2 Estadística descriptiva

El análisis estadístico de la serie histórica arrojó los siguientes parámetros descriptivos cuantitativos:

<img width="1102" height="392" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/3.png" />

**Figura 3.** Resumen estadístico obtenido con `df.describe().round(2)`.

**Interpretación de la variable objetivo (`SO2_Max`):** La concentración diaria de $SO_2$ presenta una media de 2.50 ppb y una mediana de 1.20 ppb. Que la media supere sustancialmente a la mediana evidencia un **sesgo positivo (hacia la derecha)**, impulsado por días con eventos esporádicos de contaminación industrial. La desviación estándar alcanza los 5.54 ppb, reflejando un coeficiente de variación del 221.6%, representativo de una volatilidad diaria elevada. El 75% de los datos se ubica por debajo de 2.10 ppb, con un pico máximo de 72.70 ppb, situándose todos los registros dentro del estándar primario nacional de la EPA (75 ppb como promedio horario diario) [16].

**Interpretación de las variables de cobertura:** `Obs_Count` y `Percent_Complete` presentan medianas de 23 observaciones y 96% de completitud respectivamente, con máximos de 24 y 100%. Los valores mínimos (2 observaciones y 8% de completitud) corresponden a interrupciones técnicas del equipo de medición.

### 3.3 Análisis exploratorio visual

#### 3.3.1 Matriz de dispersión general

![Matriz de dispersión entre todas las variables](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/4.png)

**Figura 4.** Matriz de dispersión multivariada generada mediante `sns.pairplot()`.

**Interpretación:** Las intersecciones entre `SO2_Max` y los predictores temporales muestran franjas de dispersión verticales sin inclinación lineal evidente, sugiriendo ausencia de relación lineal directa. La única estructura con pendiente definida se presenta entre `Obs_Count` y `Percent_Complete`, cuya alineación casi perfecta anticipa la multicolinealidad.

#### 3.3.2 Distribución de la variable objetivo

![Histograma de la concentración máxima diaria de SO2](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/5.png)

**Figura 5.** Histograma de frecuencias de `SO2_Max` en 25 intervalos.

**Interpretación:** La distribución exhibe una forma unimodal fuertemente sesgada a la derecha. La enorme mayoría de los días se concentra en el intervalo inferior de 0 a 2.5 ppb, con una caída exponencial de frecuencia a medida que aumentan los niveles de concentración.

![Curva de densidad de la concentración de SO2](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/6.png)

**Figura 6.** Curva de estimación de densidad de probabilidad por núcleo (KDE).

**Interpretación:** La función de densidad confirma que la mayor masa de probabilidad se sitúa alrededor de 1.2 ppb, decayendo progresivamente con una cola extendida hacia los 72.7 ppb.

### 3.4 Matriz de correlación

<img width="1106" height="440" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/7.png" />

**Figura 7.** Comando `.corr()` y su salida, con la matriz de correlaciones de Pearson entre las siete variables.

![Mapa de calor de la matriz de correlación](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/8.png)

**Figura 8.** Mapa de calor de la matriz de correlación de Pearson (`sns.heatmap`).

**Interpretación:** Se observan dos hallazgos clave:
1. Ninguna variable predictora alcanza un coeficiente de correlación absoluto de 0.08 frente a `SO2_Max`. Las asociaciones más altas corresponden a `Year` ($r = 0.0699$) y `Month` ($r = 0.0602$), valores considerados nulos o triviales [14].
2. La correlación entre `Obs_Count` y `Percent_Complete` es de $r = 0.9999$, reflejando una dependencia funcional lineal directa que introduce multicolinealidad severa.

| Rango de \|r\| | Interpretación | Aplicación en predictores |
|---|---|---|
| 0.00 – 0.09 | Nula o trivial | Aplica a los 6 predictores frente a `SO2_Max` |
| 0.10 – 0.29 | Baja | No aplica |
| 0.30 – 0.49 | Moderada | No aplica |
| 0.50 – 0.69 | Alta | No aplica |
| 0.70 – 1.00 | Muy alta | Únicamente entre `Obs_Count` y `Percent_Complete` ($0.9999$) |

### 3.5 Construcción y entrenamiento del modelo lineal

La partición $70/30$ destinó 2,506 registros para entrenamiento y 1,075 para evaluación de prueba.

<img width="1098" height="235" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/9.png" />

**Figura 9.** Verificación de dimensiones mediante `train_test_split()`.

<img width="1103" height="572" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/10.png" />

**Figura 10.** Intercepto ($\beta_0 = -1991.79$) y coeficientes del modelo de regresión lineal.

<img width="1117" height="685" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/11.png" />

**Figura 11.** Tabla de coeficientes, errores estándar y estadísticos $t$ calculados sobre entrenamiento.

**Interpretación:** El intercepto ($\beta_0 = -1991.79$) actúa como constante de ajuste de escala para compensar la variable `Year`. Por su parte, los coeficientes `Obs_Count` ($\beta = -22.9801$) y `Percent_Complete` ($\beta = +5.5247$) muestran signos opuestos atípicos inducidos por la multicolinealidad casi perfecta existente entre ambas variables.

### 3.6 Relación individual entre predictores y variable objetivo

![Diagramas de dispersión de cada predictor frente al SO2](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/12.png)

**Figura 12.** Diagramas de dispersión individuales de las 6 variables predictoras frente a `SO2_Max`.

**Interpretación panel por panel:** Las columnas de `Year`, `Day` y `DayOfWeek` no exhiben patrones ni tendencias. La variable `Month` refleja elevaciones leves en los meses de invierno por estabilidad atmosférica, pero con una relación no monótona. Las variables `Obs_Count` y `Percent_Complete` concentran casi la totalidad de sus observaciones en el límite superior derecho.

### 3.7 Evaluación del modelo y verificación de supuestos

#### 3.7.1 Valores reales frente a predichos

![Dispersión de SO2 real frente a SO2 predicho](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/13.png)

**Figura 13.** Dispersión de valores reales de $SO_2$ frente a los predichos sobre la muestra de prueba (1,075 registros).

**Interpretación:** En lugar de seguir la diagonal de $45^\circ$, los puntos forman una banda horizontal compacta alrededor de 2.5 ppb. Al carecer de capacidad explicativa, el estimador por Mínimos Cuadrados convergió hacia la media muestral para minimizar la suma de errores cuadráticos.

#### 3.7.2 Normalidad de los residuos

![Histograma de residuos con curva de densidad](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/14.png)

**Figura 14.** Distribución empírica de los residuos del modelo ($y_i - \hat{y}_i$).

**Interpretación:** Los errores se centran en cero, pero exhiben una cola hacia la derecha generada por los picos de contaminación, cumpliendo el supuesto de normalidad solo de forma aproximada.

#### 3.7.3 Homocedasticidad

![Residuos frente a valores predichos](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/15.png)

**Figura 15.** Diagrama de dispersión de residuos frente a valores predichos.

**Interpretación:** Muestra una franja vertical concentrada debido a la reducida dispersión de las predicciones, evidenciando que la varianza residual abarca casi la totalidad de la varianza original de los datos.

### 3.8 Modelo de contraste: árbol de decisión

![Dispersión real frente a predicho del árbol de decisión](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/16.png)

**Figura 16.** Valores reales frente a predichos por el Árbol de Decisión (`max_depth=5`).

**Interpretación:** El Árbol de Decisión obtuvo un Error Cuadrático Medio ($MSE$) de $25.105$ en la fase de prueba ($MAE = 2.397 \text{ ppb}$, $R^2 = 0.0288$), superando ligeramente el desempeño de la regresión lineal ($MSE = 25.355$).

<img width="1118" height="217" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/17.png" />

**Figura 17.** Importancia relativa de las características obtenida con `tree_model.feature_importances_`.

![Importancia relativa de las características](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/18.png)

**Figura 18.** Gráfico de barras de importancia de variables del Árbol de Decisión.

| Variable | Importancia | Porcentaje |
|---|---|---|
| `Percent_Complete` | 0.2718 | 27.18 % |
| `Month` | 0.2381 | 23.81 % |
| `Day` | 0.2207 | 22.07 % |
| `Year` | 0.1467 | 14.67 % |
| `Obs_Count` | 0.0638 | 6.38 % |
| `DayOfWeek` | 0.0589 | 5.89 % |

**Interpretación:** El algoritmo no paramétrico distribuyó su poder predictivo principalmente entre `Percent_Complete` ($27.18\%$), `Month` ($23.81\%$) y `Day` ($22.07\%$), capturando reglas de división no lineales que la regresión lineal ordinaria no pudo procesar.

---

### 3.9 Validación estadística formal

<img width="1116" height="723" alt="image" src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/19.png" />

**Figura 19.** Reporte estadístico formal de OLS generado mediante `statsmodels`.

**Interpretación:**
* **$R^2$:** El coeficiente de determinación es de $0.024$, indicando que el modelo lineal solo explica el $2.4\%$ de la variabilidad del $SO_2$.
* **$R^2$ Ajustado:** Su valor de $0.023$ confirma la escasa capacidad predictiva general del modelo.
* **Prueba F:** El estadístico $F = 14.78$ ($p = 9.31 \times 10^{-17}$) rechaza formalmente la hipótesis nula conjunta debido al gran tamaño muestral ($N=3,581$), aunque el efecto práctico sigue siendo marginal.
* **Multicolinealidad:** La nota `[2]` señala un número de condición elevado ($8.24 \times 10^6$), confirmando inestabilidad numérica provocada por la colinealidad.

---

## 4. Discusión

### 4.1 Sobre la efectividad del modelo de regresión lineal

El análisis empírico demuestra que el modelo de regresión lineal múltiple no resulta efectivo para predecir las concentraciones diarias de $SO_2$ a partir de variables temporales y de cobertura en North Birmingham, Alabama. El coeficiente $R^2 = 0.024$ indica que más del $97.6\%$ de la varianza del contaminante permanece sin explicar por la ecuación lineal.

Determinar la falta de capacidad predictiva de un conjunto de variables constituye un hallazgo científico totalmente válido y riguroso. El estudio identificó con precisión las limitaciones de utilizar variables puramente del calendario para modelar dinámicas atmosféricas complejas.

### 4.2 Causas del bajo poder predictivo

1. **Omisión de variables meteorológicas y operativas:** Las concentraciones de $SO_2$ dependen directamente de la velocidad y dirección del viento, la temperatura, la humedad, la altura de la capa de mezcla y las tasas de emisión de las plantas industriales locales. Al no contar con estos predictores en el dataset, el modelo carece de los determinantes físicos del fenómeno.
2. **Multicolinealidad funcional:** La correlación de $0.9999$ entre `Obs_Count` y `Percent_Complete` distorsionó la estimación de sus coeficientes individuales, generando variaciones inestables en los parámetros.
3. **Comportamiento no lineal de la estacionalidad:** La variación estacional de los contaminantes atmosféricos sigue patrones cíclicos no lineales que una pendiente lineal simple no puede capturar adecuadamente.

### 4.3 Recomendaciones para trabajos futuros

1. **Incorporar datos meteorológicos locales** (temperatura, velocidad/dirección del viento, radiación solar y precipitación) provenientes de la NOAA.
2. **Incluir inventarios de emisiones industriales** de las fuentes puntuales del condado de Jefferson.
3. **Eliminar variables redundantes de cobertura** manteniendo únicamente `Percent_Complete`.
4. **Explorar algoritmos avanzados no paramétricos** como Random Forest, XGBoost o modelos de series temporales (SARIMAX).

---

## 5. Conclusiones

- Se analizaron exitosamente 3,581 registros diarios de concentración máxima de $SO_2$ en la estación de North Birmingham, Alabama (2022–2023), sobre un dataset completo sin valores nulos.
- La concentración de $SO_2$ presentó una media de $2.50 \text{ ppb}$ ($1.20 \text{ ppb}$ de mediana) y una desviación estándar de $5.54 \text{ ppb}$, reflejando niveles de fondo bajos con picos industriales esporádicos dentro del estándar ambiental nacional de la EPA ($75 \text{ ppb}$).
- El modelo de regresión lineal múltiple exhibió un poder predictivo muy bajo ($R^2 = 0.024$), demostrando que las variables temporales y de cobertura por sí solas no explican la variabilidad diaria del contaminante.
- Se detectó multicolinealidad casi perfecta ($r = 0.9999$) entre `Obs_Count` y `Percent_Complete`, distorsionando los coeficientes de regresión individuales.
- El Árbol de Decisión superó ligeramente al modelo lineal ($MSE = 25.105$ frente a $25.355$), identificando a `Percent_Complete` ($27.18\%$) y `Month` ($23.81\%$) como los predictores no lineales más relevantes.

---

## 6. Archivos principales del proyecto

El archivo de datos original utilizado en el desarrollo de este estudio se encuentra publicado en la siguiente ruta del repositorio:

* [`SO2_daily_aqs_data_downloaded_2026-09-19 23_09_37.csv`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Proyecto_Integrador/Talleres/Taller%2003/Taller%203.1/Antezana_Mar%C3%ADa/SO2_daily_aqs_data_downloaded_2026-09-19%2023_09_37.csv)

Por otro lado, la ejecución completa del código de análisis, entrenamiento de modelos, diagnósticos estadísticos y visualizaciones se encuentra disponible en el notebook de Jupyter:

* [`Regresi%C3%B3n_Lineal_Antezana.ipynb`](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Proyecto_Integrador/Talleres/Taller%2003/Taller%203.1/Antezana_Mar%C3%ADa/Regresi%C3%B3n_Lineal_Antezana.ipynb)

---

## 7. Referencias bibliográficas

[1] World Health Organization, *WHO Global Air Quality Guidelines: Particulate Matter (PM2.5 and PM10), Ozone, Nitrogen Dioxide, Sulfur Dioxide and Carbon Monoxide*. Geneva, Switzerland: WHO, 2021. [Online]. Available: https://www.who.int/publications/i/item/9789240034228

[2] J. H. Seinfeld and S. N. Pandis, *Atmospheric Chemistry and Physics: From Air Pollution to Climate Change*, 3rd ed. Hoboken, NJ, USA: John Wiley & Sons, 2016.

[3] U.S. Environmental Protection Agency, "Air Quality System (AQS) Data Mart," EPA, 2023. [Online]. Available: https://www.epa.gov/outdoor-air-quality-data. [Accessed: Sep. 17, 2026].

[4] C. R. Harris *et al.*, "Array programming with NumPy," *Nature*, vol. 585, no. 7825, pp. 357–362, Sep. 2020, doi: 10.1038/s41586-020-2649-2.

[5] The pandas development team, "pandas-dev/pandas: Pandas," Zenodo, 2020, doi: 10.5281/zenodo.3509134.

[6] J. D. Hunter, "Matplotlib: A 2D graphics environment," *Computing in Science & Engineering*, vol. 9, no. 3, pp. 90–95, May 2007, doi: 10.1109/MCSE.2007.55.

[7] M. L. Waskom, "seaborn: statistical data visualization," *Journal of Open Source Software*, vol. 6, no. 60, p. 3021, Apr. 2021, doi: 10.21105/joss.03021.

[8] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, Nov. 2011.

[9] S. Seabold and J. Perktold, "statsmodels: Econometric and statistical modeling with Python," in *Proc. 9th Python in Science Conf. (SciPy 2010)*, Austin, TX, USA, 2010, pp. 92–96.

[10] G. James, D. Witten, T. Hastie, and R. Tibshirani, *An Introduction to Statistical Learning: With Applications in R*. New York, NY, USA: Springer, 2013.

[11] T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd ed. New York, NY, USA: Springer, 2009.

[12] D. C. Montgomery, E. A. Peck, and G. G. Vining, *Introduction to Linear Regression Analysis*, 5th ed. Hoboken, NJ, USA: John Wiley & Sons, 2012.

[13] N. R. Draper and H. Smith, *Applied Regression Analysis*, 3rd ed. New York, NY, USA: John Wiley & Sons, 1998.

[14] J. Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. Hillsdale, NJ, USA: Lawrence Erlbaum Associates, 1988.

[15] D. N. Gujarati and D. C. Porter, *Econometría*, 5th ed. Ciudad de México, México: McGraw-Hill, 2010.

[16] U.S. Environmental Protection Agency, "NAAQS Table: National Ambient Air Quality Standards," EPA, 2024. [Online]. Available: https://www.epa.gov/criteria-air-pollutants/naaqs-table. [Accessed: Sep. 17, 2026].

---

## Anexo A. Resultados numéricos consolidados

| Indicador | Valor | Fuente en el código |
|---|---|---|
| Registros totales procesados | 3,581 | `df.shape[0]` |
| Registros de entrenamiento | 2,506 | `X_train.shape[0]` (70%) |
| Registros de prueba | 1,075 | `X_test.shape[0]` (30%) |
| Predictores incluidos | 6 | `X.shape[1]` |
| Grados de libertad residuales | 3,574 | `OLS summary()` |
| Media de $SO_2$ | 2.50 ppb | `df.describe()` |
| Mediana de $SO_2$ | 1.20 ppb | `df.describe()` |
| Desviación estándar de $SO_2$ | 5.54 ppb | `df.describe()` |
| Mínimo y máximo de $SO_2$ | −0.60 y 72.70 ppb | `df.describe()` |
| Correlación entre `Obs_Count` y `Percent_Complete` | 0.9999 | `df.corr()` |
| Intercepto del modelo lineal | −1991.79 | `lm.intercept_` |
| $R^2$ (Regresión lineal) | 0.024 | `OLS summary()` |
| $R^2$ Ajustado | 0.023 | `OLS summary()` |
| Estadístico F | 14.78 | `OLS summary()` |
| MSE Regresión lineal (Prueba) | 25.355 | `mean_squared_error()` |
| MSE Árbol de decisión (Prueba) | 25.105 | `mean_squared_error()` |
| Variable más importante en el Árbol | `Percent_Complete` (27.18%) | `feature_importances_` |

## Anexo B. Contraste entre los dos modelos

| Criterio | Regresión Lineal Múltiple | Árbol de Decisión (`max_depth=5`) |
|---|---|---|
| Tipo de modelo | Paramétrico | No paramétrico |
| Estructura de relaciones | Exclusivamente lineales | Relaciones no lineales y por tramos |
| Variable más relevante | `Obs_Count` (distorsionada por colinealidad) | `Percent_Complete` (27.18%) y `Month` (23.81%) |
| Desempeño en prueba (MSE) | 25.355 | 25.105 |
| Coeficiente $R^2$ | 0.024 | 0.0288 |
| Sensibilidad a multicolinealidad | Alta | Baja |
| Conclusión de efectividad | No efectivo | Ligeramente superior |
