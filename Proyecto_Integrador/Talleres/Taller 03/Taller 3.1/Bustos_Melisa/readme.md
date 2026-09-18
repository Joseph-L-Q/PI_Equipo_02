# Análisis de la Calidad del Aire mediante Regresión Lineal: Dióxido de Nitrógeno (NO₂) en Montana, EE. UU. (2022–2023)

---

**Componente analizado:** Dióxido de nitrógeno (NO₂)

**Período de estudio:** 1 de enero de 2022 – 31 de diciembre de 2023

**Fuente de datos:** AQS (Air Quality System), U.S. Environmental Protection Agency

**Unidad de medida:** partes por billón (ppb)

**Registros analizados:** 730 observaciones diarias

### Localización del estudio

El conjunto de datos corresponde a **una única estación de monitoreo**. Su ubicación se describe mediante niveles administrativos anidados, todos referidos al mismo punto geográfico:

| Nivel administrativo | Denominación |
|---|---|
| País | Estados Unidos de América |
| **Estado** | **Montana** |
| Condado (*County*) | Custer |
| Ciudad | Miles City |
| Estación de monitoreo | Pines Hills |
| Identificador (Site ID) | 300170005 |
| Código FIPS de estado | 30 |
| Código FIPS de condado | 17 |
| Latitud | 46.411389° N |
| Longitud | −105.812778° O |

**Nota aclaratoria.** *Montana* es el **estado**, no la ciudad. *Miles City* es la ciudad situada dentro del estado de Montana donde se emplaza físicamente el sensor. No se trata de dos localidades distintas, sino del mismo emplazamiento descrito con distinto grado de detalle administrativo. La unicidad de la estación queda verificada por el hecho de que el conjunto contiene exactamente 730 registros, equivalentes a 365 días × 2 años, es decir, **un registro diario único** sin duplicación por múltiples sitios de muestreo.

**Contexto fisiográfico.** El emplazamiento se sitúa en la porción oriental de Montana, dentro de la provincia fisiográfica de las **Grandes Llanuras** (*Great Plains*), sobre un relieve de llanuras semiáridas desarrolladas en formaciones sedimentarias del Cretácico tardío y el Paleógeno.

---

## Tabla de contenido

1. [Introducción](#1-introducción)
2. [Metodología](#2-metodología)
3. [Resultados](#3-resultados)
4. [Discusión](#4-discusión)
5. [Conclusiones](#5-conclusiones)
6. [Referencias bibliográficas](#6-referencias-bibliográficas)
7. [Anexo A. Tabla consolidada de resultados numéricos](#anexo-a-tabla-consolidada-de-resultados-numéricos)
8. [Anexo B. Contraste entre los dos modelos](#anexo-b-contraste-entre-los-dos-modelos)
9. [Anexo C. Contraste de hipótesis](#anexo-c-contraste-de-hipótesis)

---

## 1. Introducción

### 1.1 Contexto del problema

El dióxido de nitrógeno (NO₂) es un gas de color pardo-rojizo perteneciente a la familia de los óxidos de nitrógeno (NOₓ). Se genera principalmente por procesos de combustión a altas temperaturas: motores de vehículos, plantas de generación eléctrica, calderas industriales y quema de biomasa. Su relevancia ambiental y sanitaria es doble.

En primer lugar, actúa como **contaminante primario** con efectos directos sobre la salud respiratoria. La exposición sostenida se asocia con inflamación de las vías respiratorias, agravamiento del asma y reducción de la función pulmonar, con mayor impacto en poblaciones vulnerables como niños, adultos mayores y personas con enfermedades respiratorias preexistentes [1].

En segundo lugar, funciona como **precursor de contaminantes secundarios**. En presencia de radiación solar y compuestos orgánicos volátiles, el NO₂ participa en las reacciones fotoquímicas que producen ozono troposférico; además contribuye a la formación de material particulado fino (PM₂.₅) por vía de nitratos secundarios y participa en los procesos de deposición ácida [2].

### 1.2 Justificación del área de estudio

El estado de Montana constituye un caso de estudio particular dentro del territorio estadounidense. Es un estado de baja densidad poblacional, con una economía de base agropecuaria y extractiva, y sin grandes conurbaciones industriales. La estación analizada se encuentra en la ciudad de Miles City, condado de Custer, en la porción oriental del estado, en el contexto fisiográfico descrito en el encabezado de este documento.

Este contexto es relevante porque las concentraciones esperadas de NO₂ son comparativamente bajas respecto a áreas metropolitanas, lo que permite evaluar el comportamiento de un modelo predictivo en un régimen de contaminación de fondo (*background*) más que en un régimen de emisión intensiva.

### 1.3 Objetivos

**Objetivo general**

Evaluar si es posible predecir la concentración máxima diaria de NO₂ (media horaria máxima) en la estación Miles City – Pines Hills durante 2022–2023, a partir de variables temporales y de cobertura de muestreo, empleando un modelo de regresión lineal múltiple.

**Objetivos específicos**

- Realizar un análisis exploratorio de datos (EDA) sobre la serie de 730 observaciones diarias.
- Caracterizar estadísticamente la distribución del NO₂ mediante medidas de tendencia central, dispersión y forma.
- Cuantificar la asociación lineal entre las variables predictoras y la variable objetivo mediante la matriz de correlación de Pearson.
- Construir, entrenar y evaluar un modelo de regresión lineal múltiple mediante división entrenamiento/prueba.
- Verificar el cumplimiento de los supuestos del modelo lineal (normalidad de residuos, homocedasticidad).
- Contrastar el desempeño del modelo lineal contra un modelo no lineal de referencia (árbol de decisión).
- Validar la significancia estadística del modelo mediante inferencia formal (OLS con `statsmodels`).

### 1.4 Hipótesis de trabajo

- **H₀ (hipótesis nula):** los coeficientes del modelo son conjuntamente iguales a cero; las variables predictoras no explican la variabilidad del NO₂.
- **H₁ (hipótesis alternativa):** al menos un coeficiente es distinto de cero; existe una relación lineal significativa entre los predictores y la concentración de NO₂.

El criterio de decisión adoptado es un nivel de significancia α = 0.05.

---

## 2. Metodología

### 2.1 Enfoque y diseño

La investigación es de tipo **cuantitativo, correlacional-predictivo**, con diseño **no experimental** y **longitudinal retrospectivo**. No se manipulan variables: se observan registros ya generados por la red de monitoreo oficial y se busca establecer relaciones de asociación y capacidad predictiva.

### 2.2 Descripción del conjunto de datos

Los datos proceden del sistema Air Quality System (AQS) de la Agencia de Protección Ambiental de Estados Unidos [3]. El conjunto original contiene **730 registros y 21 columnas**, correspondientes a los 365 días de 2022 más los 365 días de 2023, sin valores faltantes en las variables de interés. La verificación con `df.info(verbose=True)` confirmó que 19 de las 21 columnas presentan 730 valores no nulos; las columnas `CBSA Code` y `CBSA Name` resultaron completamente vacías (0 valores no nulos), por corresponder a un área estadística metropolitana que no aplica a esta estación rural.

### 2.3 Herramientas computacionales

El análisis se desarrolló en Python 3 sobre entorno Jupyter Notebook. Las bibliotecas empleadas y su función específica fueron:

| Biblioteca | Alias | Sentencia de importación | Función en el proyecto | Ref. |
|---|---|---|---|---|
| `numpy` | `np` | `import numpy as np` | Cálculo numérico vectorizado; operaciones sobre arreglos para el cómputo de errores estándar | [4] |
| `pandas` | `pd` | `import pandas as pd` | Carga, limpieza, transformación y manejo tabular de los datos | [5] |
| `matplotlib.pyplot` | `plt` | `import matplotlib.pyplot as plt` | Generación de gráficos base: histogramas, dispersión, barras | [6] |
| `seaborn` | `sns` | `import seaborn as sns` | Gráficos estadísticos de mayor nivel: pairplot, heatmap, histograma con KDE | [7] |
| `scikit-learn` | — | `from sklearn... import ...` | Modelado predictivo: partición de datos, regresión lineal, árbol de decisión, métricas | [8] |
| `statsmodels.api` | `sm` | `import statsmodels.api as sm` | Inferencia estadística formal mediante mínimos cuadrados ordinarios (OLS) | [9] |

La directiva `%matplotlib inline` no es una función de Python sino un **comando mágico** (*magic command*) propio de IPython/Jupyter. Su efecto es incrustar las figuras generadas directamente en la salida de la celda, en lugar de abrirlas en una ventana emergente externa.

### 2.4 Funciones y métodos empleados

#### Tabla resumen de comandos

La siguiente tabla consolida la totalidad de comandos, funciones, métodos y atributos empleados en el notebook, ordenados según la etapa del flujo de trabajo. Cada uno se desarrolla en detalle en los apartados posteriores.

| # | Comando / función | Biblioteca | Etapa | Qué hace | Resultado obtenido |
|---|---|---|---|---|---|
| 1 | `pd.read_csv()` | pandas | Carga | Lee un archivo CSV y lo convierte en `DataFrame` | Tabla de 730 × 21 |
| 2 | `df.head()` | pandas | Inspección | Muestra las primeras 5 filas | Verificación visual de la carga |
| 3 | `df.info(verbose=True)` | pandas | Inspección | Reporta filas, tipos de dato y valores no nulos | 19 columnas completas, 2 vacías |
| 4 | `df.describe().round(2)` | pandas | Descriptiva | Resumen estadístico de variables numéricas | Media, desv. est., cuartiles |
| 5 | `df.columns` | pandas | Inspección | Devuelve los nombres de las columnas | Lista de 7 variables |
| 6 | `pd.to_datetime()` | pandas | Limpieza | Convierte texto a tipo fecha | Columna `Date` como `datetime64` |
| 7 | `.dt.year` / `.dt.month` / `.dt.day` / `.dt.dayofweek` | pandas | Ing. de características | Extrae componentes de una fecha | 4 variables temporales nuevas |
| 8 | Selección por lista `df[[...]]` | pandas | Limpieza | Conserva solo columnas relevantes | Reducción de 21 a 7 columnas |
| 9 | `df.rename(columns={})` | pandas | Limpieza | Renombra columnas | Nombres cortos sin espacios |
| 10 | `sns.pairplot()` | seaborn | Exploración | Matriz de dispersión de todas las variables | Figura 1 |
| 11 | `.plot.hist(bins=25)` | pandas/matplotlib | Exploración | Histograma de frecuencias | Figura 2 |
| 12 | `.plot.density()` | pandas | Exploración | Curva de densidad por núcleo (KDE) | Figura 3 |
| 13 | `df.select_dtypes()` | pandas | Correlación | Filtra solo columnas numéricas | Subconjunto numérico |
| 14 | `.corr()` | pandas | Correlación | Matriz de correlación de Pearson | Matriz 7 × 7 |
| 15 | `sns.heatmap(annot=True)` | seaborn | Correlación | Mapa de calor de la matriz | Figura 4 |
| 16 | `train_test_split()` | scikit-learn | Partición | Divide en entrenamiento y prueba | 511 / 219 registros |
| 17 | `LinearRegression()` | scikit-learn | Modelado | Instancia el modelo lineal | Objeto `lm` |
| 18 | `lm.fit()` | scikit-learn | Entrenamiento | Estima los coeficientes por mínimos cuadrados | Modelo ajustado |
| 19 | `lm.intercept_` | scikit-learn | Resultados | Devuelve el término independiente β₀ | 1566.83 |
| 20 | `lm.coef_` | scikit-learn | Resultados | Devuelve el vector de coeficientes β₁…β₆ | 6 valores |
| 21 | `lm.predict()` | scikit-learn | Predicción | Aplica el modelo a datos nuevos | Arreglo de 219 predicciones |
| 22 | `np.square()` / `np.sum()` / `np.sqrt()` | numpy | Inferencia | Operaciones para el error estándar manual | Columna SE |
| 23 | `gridspec.GridSpec(2, 3)` | matplotlib | Visualización | Organiza subgráficos en una cuadrícula | Figura 5 |
| 24 | `sns.histplot(kde=True)` | seaborn | Diagnóstico | Histograma de residuos con densidad | Figura 7 |
| 25 | `plt.scatter()` | matplotlib | Diagnóstico | Diagramas de dispersión | Figuras 6, 8, 9 |
| 26 | `tree.DecisionTreeRegressor()` | scikit-learn | Modelo de contraste | Árbol de decisión para regresión | Modelo no lineal |
| 27 | `tree_model.feature_importances_` | scikit-learn | Interpretación | Importancia relativa de cada predictor | Figura 10 |
| 28 | `metrics.mean_squared_error()` | scikit-learn | Evaluación | Error cuadrático medio | MSE = 31.474 |
| 29 | `plt.barh()` | matplotlib | Visualización | Gráfico de barras horizontales | Figura 10 |
| 30 | `sm.add_constant()` | statsmodels | Inferencia | Añade columna de unos para el intercepto | Matriz de diseño |
| 31 | `sm.OLS().fit()` | statsmodels | Inferencia | Ajusta mínimos cuadrados ordinarios | Objeto de resultados |
| 32 | `.summary()` | statsmodels | Inferencia | Reporte econométrico completo | R², F, p-valores, IC |

A continuación se detalla cada función utilizada, su propósito y su fundamento.

#### 2.4.1 Carga e inspección

- **`pd.read_csv(ruta)`** — Lee el archivo de valores separados por comas y lo convierte en un objeto `DataFrame`, la estructura tabular bidimensional de pandas.
- **`df.head()`** — Devuelve las primeras cinco filas. Sirve para verificar que la lectura fue correcta y que las columnas se interpretaron con el tipo de dato adecuado.
- **`df.info(verbose=True)`** — Reporta el número de registros, el nombre de cada columna, la cantidad de valores no nulos y el tipo de dato (`int64`, `float64`, `object`). Es la herramienta primaria para detectar valores faltantes.
- **`df.describe().round(2)`** — Calcula el resumen estadístico de las variables numéricas: conteo, media, desviación estándar, mínimo, cuartiles (25 %, 50 %, 75 %) y máximo. El método `.round(2)` limita la salida a dos decimales.
- **`df.columns`** — Devuelve el índice con los nombres de las columnas.

#### 2.4.2 Limpieza y transformación

- **`pd.to_datetime(df['Date'], format='%m/%d/%Y')`** — Convierte la columna de fechas, originalmente de tipo texto (`object`), a tipo `datetime64`. Sin esta conversión no es posible extraer componentes temporales.
- **`.dt.year`, `.dt.month`, `.dt.day`, `.dt.dayofweek`** — Accesorios del tipo datetime que permiten la **ingeniería de características** (*feature engineering*): a partir de una sola columna de fecha se derivaron cuatro variables predictoras nuevas. `dayofweek` codifica el día de la semana de 0 (lunes) a 6 (domingo).
- **Selección de columnas por lista** — Se conservaron únicamente siete columnas, descartando aquellas constantes para esta estación (`Site ID`, `State`, `County`, `Units`, coordenadas) o vacías (`CBSA`). Una variable constante no aporta información porque su varianza es cero y por tanto no puede explicar variabilidad alguna.
- **`df.rename(columns={...})`** — Renombra las columnas a identificadores cortos y sin espacios (`Obs_Count`, `Percent_Complete`, `NO2_Max`), facilitando su referencia en el código.

#### 2.4.3 Análisis exploratorio y visualización

- **`sns.pairplot(df)`** — Genera una matriz de gráficos que cruza todas las variables entre sí: dispersión en las celdas fuera de la diagonal e histogramas en la diagonal. Permite detectar visualmente relaciones lineales, no lineales, agrupamientos y valores atípicos.
- **`.plot.hist(bins=25)`** — Histograma con 25 intervalos. Responde a la pregunta de cómo se reparten las observaciones a lo largo del rango de valores.
- **`.plot.density()`** — Estimación de densidad por núcleo (*Kernel Density Estimate*, KDE). Es la versión suavizada y continua del histograma; muestra dónde se concentra la masa de probabilidad.
- **`df.select_dtypes(include=[np.number])`** — Filtra el DataFrame conservando solo columnas numéricas, requisito previo para calcular correlaciones.
- **`.corr()`** — Calcula la matriz de coeficientes de correlación de Pearson entre todos los pares de variables numéricas.
- **`sns.heatmap(matriz, annot=True, linewidths=2)`** — Representa la matriz de correlación como mapa de calor; `annot=True` sobreimprime el valor numérico en cada celda.

#### 2.4.4 Separación de variables y partición de datos

La separación siguió la convención estándar del aprendizaje supervisado:

```python
X = df[l_column[0:len_feature-1]]   # matriz de predictores (6 columnas)
Y = df[l_column[len_feature-1]]     # vector objetivo (NO2_Max)
```

- **`train_test_split(X, Y, test_size=0.3, random_state=123)`** — Divide aleatoriamente el conjunto en cuatro subconjuntos: `X_train`, `X_test`, `Y_train`, `Y_test`.
  - `test_size=0.3` reserva el 30 % de los datos (219 registros) para prueba y destina el 70 % (511 registros) al entrenamiento.
  - `random_state=123` fija la semilla del generador pseudoaleatorio. Esto garantiza la **reproducibilidad**: cualquier persona que ejecute el código obtendrá exactamente la misma partición.

**Tabla de parámetros de `train_test_split()`**

| Parámetro | Valor usado | Significado | Efecto en este proyecto |
|---|---|---|---|
| `X` | DataFrame 730 × 6 | Matriz de predictores | Variables explicativas |
| `Y` | Serie de 730 valores | Vector objetivo | `NO2_Max` |
| `test_size` | `0.3` | Proporción reservada a prueba | 219 registros de prueba |
| *(implícito)* `train_size` | `0.7` | Proporción de entrenamiento | 511 registros de entrenamiento |
| `random_state` | `123` | Semilla del generador pseudoaleatorio | Garantiza reproducibilidad exacta |
| *(por defecto)* `shuffle` | `True` | Mezcla los datos antes de dividir | Evita sesgo por orden cronológico |

**Objetos devueltos**

| Objeto | Contenido | Dimensión |
|---|---|---|
| `X_train` | Predictores de entrenamiento | 511 × 6 |
| `X_test` | Predictores de prueba | 219 × 6 |
| `Y_train` | Valores reales de entrenamiento | 511 |
| `Y_test` | Valores reales de prueba | 219 |

El fundamento de esta división es evitar el **sobreajuste** (*overfitting*) [10]. Evaluar un modelo sobre los mismos datos con los que fue entrenado produce una estimación optimista y engañosa de su desempeño; la partición permite medir la capacidad de **generalización** sobre datos que el modelo nunca vio.

#### 2.4.5 Modelo de regresión lineal

- **`LinearRegression()`** — Instancia el estimador. Ajusta un modelo de la forma:

$$\hat{Y} = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \dots + \beta_6 X_6$$

  El ajuste se realiza por el método de **mínimos cuadrados ordinarios**, que busca los coeficientes que minimizan la suma de los cuadrados de los residuos:

$$\min \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$

- **`lm.fit(X_train, Y_train)`** — Ejecuta el entrenamiento, estimando los valores de los coeficientes a partir de los datos de entrenamiento.
- **`lm.intercept_`** — Atributo que almacena β₀, el valor esperado de Y cuando todos los predictores valen cero.
- **`lm.coef_`** — Arreglo con los coeficientes β₁ … β₆. Cada coeficiente representa el cambio esperado en NO₂ (ppb) ante un incremento unitario de esa variable, manteniendo las demás constantes (*ceteris paribus*).
- **`lm.predict(X_test)`** — Aplica la ecuación ajustada a los datos de prueba y devuelve las predicciones.

**Tabla de métodos y atributos de `LinearRegression`**

| Elemento | Tipo | Sintaxis | Devuelve |
|---|---|---|---|
| `LinearRegression()` | Constructor | `lm = LinearRegression()` | Objeto estimador sin entrenar |
| `.fit(X, Y)` | Método | `lm.fit(X_train, Y_train)` | El propio objeto, ya ajustado |
| `.intercept_` | Atributo | `lm.intercept_` | Escalar: término independiente β₀ |
| `.coef_` | Atributo | `lm.coef_` | Arreglo de 6 coeficientes β₁…β₆ |
| `.predict(X)` | Método | `lm.predict(X_test)` | `ndarray` de 219 predicciones |

La distinción entre método y atributo es relevante: los **métodos** llevan paréntesis porque ejecutan una acción; los **atributos** terminan en guion bajo (`_`), convención de scikit-learn que indica que el valor fue *aprendido durante el entrenamiento* y no existe antes de llamar a `.fit()` [8].

La fundamentación teórica del estimador de mínimos cuadrados y de sus propiedades de insesgadez y varianza mínima se encuentra en [11].

#### 2.4.6 Inferencia sobre los coeficientes

Se calcularon manualmente el error estándar y el estadístico t de cada coeficiente:

- **Grados de libertad:** `dfN = n − k`, donde n = 511 observaciones de entrenamiento y k = 6 predictores.
- **Suma de cuadrados del error:** `np.sum(np.square(train_pred − Y_train))`.
- **Error estándar (SE):** mide la incertidumbre asociada a la estimación de cada coeficiente.
- **Estadístico t:** `t = Coeficiente / Error estándar`. Cuantifica a cuántos errores estándar de distancia del cero se encuentra el coeficiente estimado. Valores absolutos mayores a aproximadamente 1.96 sugieren significancia al 5 %.

#### 2.4.7 Verificación de supuestos

El modelo de regresión lineal descansa sobre cuatro supuestos fundamentales, verificados gráficamente:

1. **Linealidad** — la relación entre predictores y respuesta es lineal (evaluada con los diagramas de dispersión individuales).
2. **Normalidad de los residuos** — los errores se distribuyen normalmente con media cero (evaluada con `sns.histplot(Y_test − predictions, kde=True)`).
3. **Homocedasticidad** — la varianza de los errores es constante a lo largo del rango de predicciones (evaluada con el gráfico de residuos frente a valores predichos).
4. **Independencia** — las observaciones no están correlacionadas entre sí.

**Tabla de verificación de supuestos**

| Supuesto | Herramienta de diagnóstico | Criterio de cumplimiento | Figura |
|---|---|---|---|
| Linealidad | Diagramas de dispersión predictor–respuesta | Tendencia recta visible | Figura 5 |
| Normalidad de residuos | Histograma con KDE de `Y_test − predictions` | Forma acampanada centrada en 0 | Figura 7 |
| Homocedasticidad | Residuos frente a valores predichos | Dispersión constante, sin embudo | Figura 8 |
| Independencia | Durbin-Watson *(no aplicado)* | Estadístico próximo a 2 | — |
| Ajuste global | Real frente a predicho | Puntos sobre la diagonal de 45° | Figura 6 |

El desarrollo formal de estos supuestos y de las consecuencias de su incumplimiento se expone en [11] y [16].

#### 2.4.8 Modelo de contraste: árbol de decisión

- **`tree.DecisionTreeRegressor(max_depth=5, random_state=10)`** — Modelo no paramétrico que particiona recursivamente el espacio de predictores mediante reglas de decisión binarias. A diferencia de la regresión lineal, puede capturar relaciones no lineales e interacciones entre variables sin especificarlas previamente. El parámetro `max_depth=5` limita la profundidad del árbol para controlar el sobreajuste. El fundamento teórico de los árboles de regresión y del criterio de partición por reducción de impureza se desarrolla en [12].

**Tabla de parámetros del árbol de decisión**

| Parámetro | Valor | Significado |
|---|---|---|
| `max_depth` | `5` | Número máximo de niveles de división; controla la complejidad |
| `random_state` | `10` | Semilla para el desempate de divisiones equivalentes |
| *(por defecto)* `criterion` | `squared_error` | Minimiza el error cuadrático en cada partición |
- **`tree_model.feature_importances_`** — Devuelve la importancia relativa normalizada de cada predictor, calculada como la reducción total de impureza (varianza) que aporta cada variable en las divisiones del árbol. Los valores suman 1.
- **`metrics.mean_squared_error(Y_test, tree_pred)`** — Error cuadrático medio, promedio de los cuadrados de las diferencias entre valores reales y predichos.

#### 2.4.9 Validación estadística formal

- **`sm.add_constant(X)`** — Añade una columna de unos a la matriz de predictores, necesaria para que `statsmodels` estime el término independiente.
- **`sm.OLS(Y, Xs).fit()`** — Ajusta el modelo de mínimos cuadrados ordinarios sobre el conjunto completo.
- **`.summary()`** — Genera el reporte econométrico completo.

**Tabla de indicadores del reporte `summary()`**

| Indicador | Qué mide | Cómo se interpreta |
|---|---|---|
| `R-squared` | Proporción de varianza explicada | Entre 0 y 1; mayor es mejor |
| `Adj. R-squared` | R² penalizado por número de predictores | Puede ser negativo si el modelo es peor que la media |
| `F-statistic` | Significancia conjunta de todos los coeficientes | Mayor valor indica modelo más significativo |
| `Prob (F-statistic)` | p-valor de la prueba F global | Si < 0.05, se rechaza H₀ |
| `coef` | Valor estimado de cada β | Cambio en Y por unidad de X |
| `std err` | Incertidumbre de la estimación | Mayor valor, estimación menos precisa |
| `t` | Coeficiente dividido entre su error estándar | \|t\| > 1.96 sugiere significancia al 5 % |
| `P>\|t\|` | p-valor individual de cada coeficiente | Si < 0.05, la variable es significativa |
| `[0.025, 0.975]` | Intervalo de confianza al 95 % | Si contiene el 0, el efecto no es concluyente |
| `AIC` / `BIC` | Criterios de información | Menor valor indica mejor equilibrio ajuste-parsimonia |
| `No. Observations` | Tamaño muestral | 730 |
| `Df Residuals` | Grados de libertad residuales | n − k − 1 = 723 |
| `Df Model` | Número de predictores | 6 |

El marco econométrico de estos indicadores se desarrolla en [15].

---

## 3. Resultados

### 3.1 Estadística descriptiva

La aplicación de `df.describe()` sobre las variables transformadas arrojó los siguientes valores:

| Estadístico | Year | Month | Day | DayOfWeek | Obs_Count | Percent_Complete | **NO2_Max** |
|---|---|---|---|---|---|---|---|
| count | 730.0 | 730.00 | 730.00 | 730.00 | 730.00 | 730.00 | **730.00** |
| mean | 2022.5 | 6.53 | 15.72 | 3.01 | 23.53 | 98.06 | **10.47** |
| std | 0.5 | 3.45 | 8.80 | 2.00 | 1.54 | 6.37 | **6.37** |
| min | 2022.0 | 1.00 | 1.00 | 0.00 | 10.00 | 42.00 | **0.00** |
| 25 % | 2022.0 | 4.00 | 8.00 | 1.00 | 24.00 | 100.00 | **6.00** |
| 50 % | 2022.5 | 7.00 | 16.00 | 3.00 | 24.00 | 100.00 | **9.00** |
| 75 % | 2023.0 | 10.00 | 23.00 | 5.00 | 24.00 | 100.00 | **14.00** |
| max | 2023.0 | 12.00 | 31.00 | 6.00 | 24.00 | 100.00 | **35.00** |

**Interpretación de la variable objetivo (NO2_Max):**

- La **media** es de 10.47 ppb y la **mediana** de 9.00 ppb. Que la media supere a la mediana indica una distribución con **asimetría positiva** (sesgo a la derecha): existe una cola de valores altos que arrastra el promedio hacia arriba.
- La **desviación estándar** de 6.37 ppb frente a una media de 10.47 ppb produce un **coeficiente de variación** de aproximadamente 61 %, lo que evidencia una dispersión considerable en términos relativos.
- El **rango** abarca de 0 a 35 ppb y el **rango intercuartílico** (RIC) es de 14 − 6 = 8 ppb, es decir, el 50 % central de los días registró entre 6 y 14 ppb.
- Todos los valores se encuentran muy por debajo del estándar nacional de calidad del aire de EE. UU. para NO₂, fijado en 100 ppb como promedio horario máximo diario en su percentil 98 anual [13], lo que confirma el carácter de **aire limpio** del área estudiada.

**Interpretación de las variables de cobertura:**

`Obs_Count` (número de observaciones horarias diarias) tiene mediana 24, el máximo teórico posible en un día. `Percent_Complete` tiene mediana 100 %. Ambas variables describen la **completitud del muestreo**, no un fenómeno atmosférico. El mínimo de 10 observaciones (42 % de completitud) corresponde a días con interrupciones del equipo de monitoreo.

---

### 3.2 Análisis exploratorio visual

#### 3.2.1 Matriz de dispersión general

![Matriz de dispersión entre todas las variables](imagenes/01_pairplot.png)

*Figura 1. Matriz de dispersión (pairplot) de todas las variables del conjunto depurado.*

**Interpretación:** Las celdas que cruzan `NO2_Max` con las variables temporales (`Year`, `Month`, `Day`, `DayOfWeek`) muestran nubes de puntos distribuidas en bandas verticales sin pendiente apreciable. Esta configuración es la firma visual de la **ausencia de relación lineal**: para cualquier valor del predictor, el NO₂ toma prácticamente todo su rango de valores. La única estructura visible es la fuerte alineación entre `Obs_Count` y `Percent_Complete`, que forman una recta casi perfecta, anticipando el problema de colinealidad que se documenta en la sección 3.3.

#### 3.2.2 Distribución de la variable objetivo

![Histograma de la concentración máxima diaria de NO2](imagenes/02_histograma_no2.png)

*Figura 2. Histograma de NO2_Max con 25 intervalos.*

**Interpretación:** La distribución es **unimodal y asimétrica positiva**. La mayor frecuencia se concentra en el intervalo de 5 a 10 ppb, y la frecuencia decae progresivamente hacia la derecha, con muy pocos días superando los 25 ppb. Esta forma es característica de los contaminantes atmosféricos, que suelen ajustarse mejor a distribuciones log-normales o gamma que a la normal: no pueden tomar valores negativos, se acumulan cerca del límite inferior y presentan episodios extremos esporádicos.

![Curva de densidad de la concentración de NO2](imagenes/03_densidad_no2.png)

*Figura 3. Estimación de densidad por núcleo (KDE) de NO2_Max.*

**Interpretación:** La curva suavizada confirma la asimetría observada en el histograma. El pico de densidad se ubica alrededor de los 7–9 ppb, ligeramente por debajo de la media aritmética, lo que es consistente con el orden moda < mediana < media propio de las distribuciones sesgadas a la derecha. La cola derecha se extiende sin interrupciones hasta los 35 ppb.

---

### 3.3 Matriz de correlación

| | Year | Month | Day | DayOfWeek | Obs_Count | Percent_Complete | **NO2_Max** |
|---|---|---|---|---|---|---|---|
| **Year** | 1.0000 | 0.0000 | 0.0000 | 0.0007 | 0.0259 | 0.0265 | **−0.0241** |
| **Month** | 0.0000 | 1.0000 | 0.0119 | 0.0068 | −0.0408 | −0.0417 | **0.0047** |
| **Day** | 0.0000 | 0.0119 | 1.0000 | −0.0108 | −0.0545 | −0.0541 | **−0.0063** |
| **DayOfWeek** | 0.0007 | 0.0068 | −0.0108 | 1.0000 | 0.1416 | 0.1396 | **0.0311** |
| **Obs_Count** | 0.0259 | −0.0408 | −0.0545 | 0.1416 | 1.0000 | 0.9998 | **0.0439** |
| **Percent_Complete** | 0.0265 | −0.0417 | −0.0541 | 0.1396 | 0.9998 | 1.0000 | **0.0432** |
| **NO2_Max** | −0.0241 | 0.0047 | −0.0063 | 0.0311 | 0.0439 | 0.0432 | **1.0000** |

![Mapa de calor de la matriz de correlación](imagenes/04_heatmap_correlacion.png)

*Figura 4. Mapa de calor de correlaciones de Pearson.*

**Interpretación:** Dos hallazgos dominan esta matriz.

**Primero**, ninguna variable predictora alcanza siquiera |r| = 0.05 con NO2_Max. La correlación más alta es 0.0439 con `Obs_Count`, un valor que bajo los criterios convencionales de clasificación de la magnitud del efecto [14] corresponde a una correlación **nula o trivial**. Elevando al cuadrado, el coeficiente de determinación individual sería r² = 0.0019, es decir, apenas el 0.19 % de varianza compartida. Esto anticipa desde la etapa exploratoria que el modelo lineal tendrá un poder predictivo muy limitado.

**Tabla de referencia para la interpretación del coeficiente r** [14]

| Rango de \|r\| | Interpretación | ¿Aplica a algún predictor de NO2_Max? |
|---|---|---|
| 0.00 – 0.09 | Nula o trivial | **Sí — los seis predictores** |
| 0.10 – 0.29 | Baja | No |
| 0.30 – 0.49 | Moderada | No |
| 0.50 – 0.69 | Alta | No |
| 0.70 – 1.00 | Muy alta | Solo entre `Obs_Count` y `Percent_Complete` |

**Segundo**, la correlación entre `Obs_Count` y `Percent_Complete` es de **0.9998**, prácticamente perfecta. Esto no es coincidencia: `Percent_Complete` se calcula como el cociente entre observaciones registradas y observaciones esperadas, multiplicado por cien. Es decir, **una variable es una transformación determinista de la otra**. Incluir ambas en un mismo modelo introduce **multicolinealidad severa**, un problema cuyas consecuencias se detallan en la discusión.

---

### 3.4 Construcción y entrenamiento del modelo lineal

La partición produjo 511 registros de entrenamiento y **219 registros de prueba**, verificados mediante `predictions.shape`, que devolvió `(219,)`.

**Parámetros estimados:**

- **Intercepto (β₀):** 1566.830328071976
- **Coeficientes:**

| Variable | Coeficiente | Error estándar | Estadístico t |
|---|---|---|---|
| Year | −0.772701 | 0.589794 | −1.310119 |
| Month | 0.014875 | 0.083655 | 0.177816 |
| Day | −0.015843 | 0.033847 | −0.468086 |
| DayOfWeek | 0.033458 | 0.147875 | 0.226259 |
| Obs_Count | 3.535945 | 0.203842 | 17.346512 |
| Percent_Complete | −0.778825 | 0.049028 | −15.885331 |

**Interpretación de los parámetros:**

El **intercepto de 1566.83 ppb** carece de sentido físico directo. Representa el valor predicho cuando todos los predictores valen cero, incluida `Year = 0`, una condición inexistente. Su magnitud desproporcionada es un efecto de escala: dado que `Year` toma valores cercanos a 2022 y su coeficiente es −0.7727, el producto −0.7727 × 2022 ≈ −1562 debe ser compensado por el intercepto para que la predicción resultante caiga en el rango observado de 0 a 35 ppb.

Los coeficientes de las variables estrictamente temporales son todos de magnitud despreciable: un cambio de un mes altera la predicción en apenas 0.0149 ppb, y un cambio de día de la semana en 0.0335 ppb. Frente a una desviación estándar de 6.37 ppb en la variable objetivo, estos efectos son irrelevantes.

Los coeficientes de `Obs_Count` (+3.54) y `Percent_Complete` (−0.78) aparecen como los de mayor magnitud, pero **tienen signos opuestos pese a que ambas variables están correlacionadas al 0.9998**. Esta inversión de signos es un síntoma clásico de multicolinealidad: los coeficientes se compensan mutuamente y pierden toda interpretabilidad individual.

**Advertencia metodológica sobre los estadísticos t:** los errores estándar calculados manualmente en el notebook emplean una fórmula que considera la variabilidad de cada predictor de forma aislada, sin incorporar la matriz de covarianzas completa (X'X)⁻¹. En presencia de la colinealidad detectada, este procedimiento **subestima gravemente los errores estándar** y produce estadísticos t artificialmente inflados. Los valores de 17.35 y −15.89 son, por tanto, espurios. La sección 3.7 presenta el cálculo correcto mediante `statsmodels`, donde estos mismos coeficientes resultan **no significativos** (t = 0.86 y t = −0.84).

---

### 3.5 Relación individual entre predictores y variable objetivo

![Diagramas de dispersión de cada predictor frente al NO2](imagenes/05_dispersion_predictores.png)

*Figura 5. Diagramas de dispersión de los seis predictores frente a NO2_Max.*

**Interpretación panel por panel:**

- **Year vs. NO2_Max:** dos columnas verticales (2022 y 2023) de altura prácticamente idéntica. No hay evidencia de tendencia interanual.
- **Month vs. NO2_Max:** doce columnas verticales. Se aprecia una ligera reducción de los valores máximos en los meses centrales del año (5–8, verano boreal) y mayor dispersión hacia arriba en los meses fríos, lo que sugiere una **estacionalidad débil pero existente**, atribuible a inversiones térmicas invernales y mayor demanda de calefacción. Sin embargo, esta relación es **no monótona** (baja en verano, alta en ambos extremos del año) y por ello un término lineal simple no puede capturarla.
- **Day vs. NO2_Max:** treinta y una columnas homogéneas. El día del mes es, como cabía esperar, completamente irrelevante.
- **DayOfWeek vs. NO2_Max:** siete columnas. No se observa el descenso de fin de semana típico de zonas con tráfico vehicular intenso, coherente con el carácter rural de la estación.
- **Obs_Count vs. NO2_Max** y **Percent_Complete vs. NO2_Max:** la enorme mayoría de puntos se agolpa en el extremo derecho (24 observaciones, 100 % de completitud), con unos pocos puntos aislados a la izquierda. Esta distribución extremadamente desbalanceada hace que la pendiente estimada sea muy sensible a un número reducido de observaciones.

---

### 3.6 Evaluación del modelo y verificación de supuestos

#### 3.6.1 Valores reales frente a predichos

![Dispersión de NO2 real frente a NO2 predicho](imagenes/06_real_vs_predicho.png)

*Figura 6. NO₂ real frente a NO₂ predicho en el conjunto de prueba (n = 219).*

**Interpretación:** El criterio de calidad para este gráfico es que los puntos se alineen sobre la diagonal de 45°, donde valor predicho = valor real. Lo que se observa es lo contrario: una **nube horizontal**. Mientras los valores reales se extienden de 0 a 35 ppb, las predicciones se comprimen en un rango estrecho en torno a los 10 ppb, muy cercano a la media de la variable.

Este comportamiento tiene una explicación estadística precisa. Cuando los predictores no aportan información útil, la solución de mínimos cuadrados converge hacia la **predicción de la media incondicional**, puesto que la media es el estimador que minimiza el error cuadrático en ausencia de información adicional. En términos prácticos, el modelo no está prediciendo: está devolviendo el promedio.

#### 3.6.2 Normalidad de los residuos

![Histograma de residuos con curva de densidad](imagenes/07_histograma_residuos.png)

*Figura 7. Distribución de los residuos (Y_test − predictions).*

**Interpretación:** Los residuos se centran aproximadamente en cero, lo cual es correcto y esperado (la suma de residuos en mínimos cuadrados es cero por construcción). La forma general es unimodal, pero presenta **asimetría positiva** con una cola derecha más extendida, heredada de la asimetría de la variable original. Esto implica que el supuesto de normalidad se cumple solo de forma **aproximada**.

Conviene señalar que, para muestras grandes como esta (n = 219 en prueba), el teorema del límite central atenúa el impacto de las desviaciones moderadas de normalidad sobre la validez de las pruebas de hipótesis. La normalidad afecta principalmente a los intervalos de confianza, no a la insesgadez de los estimadores.

#### 3.6.3 Homocedasticidad

![Residuos frente a valores predichos](imagenes/08_residuos_vs_predichos.png)

*Figura 8. Residuos frente a valores predichos.*

**Interpretación:** El patrón deseable es una nube de puntos sin estructura, distribuida con amplitud constante alrededor de la línea horizontal en cero. Lo observado es una **franja vertical estrecha**: los valores predichos ocupan un intervalo muy reducido en el eje horizontal, mientras que los residuos se dispersan ampliamente en el eje vertical.

Esta configuración no indica heterocedasticidad en sentido estricto —la varianza del error no crece sistemáticamente con la predicción—, sino algo más fundamental: **la varianza de los residuos es prácticamente igual a la varianza total de la variable objetivo**. El modelo no ha logrado descomponer la variabilidad total en una parte explicada y una parte residual; toda la variabilidad permanece en los residuos.

---

### 3.7 Validación estadística formal mediante OLS

```
                            OLS Regression Results
==============================================================================
Dep. Variable:                NO2_Max   R-squared:                       0.004
Model:                            OLS   Adj. R-squared:                 -0.004
Method:                 Least Squares   F-statistic:                    0.5100
No. Observations:                 730   Prob (F-statistic):              0.801
Df Residuals:                     723   Log-Likelihood:                -2385.6
Df Model:                           6   AIC:                             4785.
Covariance Type:            nonrobust   BIC:                             4817.
====================================================================================
                       coef    std err          t      P>|t|      [0.025      0.975]
------------------------------------------------------------------------------------
const              631.5659    956.472      0.660      0.509   -1246.228    2509.360
Year                -0.3089      0.473     -0.653      0.514      -1.237       0.620
Month                0.0089      0.069      0.130      0.897      -0.126       0.144
Day                 -0.0023      0.027     -0.086      0.931      -0.055       0.051
DayOfWeek            0.0701      0.120      0.585      0.559      -0.165       0.305
Obs_Count            7.0483      8.197      0.860      0.390      -9.044      23.141
Percent_Complete    -1.6562      1.973     -0.839      0.402      -5.531       2.218
====================================================================================
```

**Interpretación detallada de cada indicador:**

**R² = 0.004.** El coeficiente de determinación indica la proporción de la varianza de NO2_Max explicada por el conjunto de predictores. Un valor de 0.004 significa que el modelo explica el **0.4 %** de la variabilidad observada. El 99.6 % restante queda sin explicar. Este es el indicador más contundente del fracaso predictivo del modelo.

**R² ajustado = −0.004.** Esta versión penaliza la inclusión de predictores que no aportan capacidad explicativa. Que resulte **negativo** tiene un significado muy concreto: el modelo con seis predictores ajusta **peor** que un modelo trivial que se limitara a predecir siempre la media de NO₂. En otras palabras, las seis variables no solo son inútiles, sino que añaden ruido.

**Estadístico F = 0.5100 con Prob (F-statistic) = 0.801.** La prueba F contrasta la hipótesis nula de que todos los coeficientes (excepto el intercepto) son simultáneamente cero. El p-valor de 0.801 es muy superior al nivel de significancia α = 0.05. Por tanto, **no se rechaza la hipótesis nula**. En términos probabilísticos: si en la población no existiera ninguna relación entre estos predictores y el NO₂, habría un 80.1 % de probabilidad de observar un ajuste igual o mejor que el obtenido, por puro azar muestral.

**P-valores individuales.** Los seis predictores presentan p-valores entre 0.390 y 0.931, todos muy por encima de 0.05. **Ninguna variable resulta estadísticamente significativa** de forma individual.

**Intervalos de confianza al 95 %.** Todos los intervalos **contienen el valor cero**. Por ejemplo, el de `Obs_Count` va de −9.044 a 23.141: el rango de valores plausibles para el efecto real de esta variable incluye tanto efectos negativos como positivos considerables. Esta amplitud es reflejo directo de la multicolinealidad, que infla los errores estándar (8.197 para `Obs_Count`, frente a un coeficiente de 7.048).

**Criterios de información:** AIC = 4785 y BIC = 4817. Son útiles como referencia comparativa para futuros modelos alternativos sobre el mismo conjunto de datos: valores menores indican mejor equilibrio entre ajuste y parsimonia.

---

### 3.8 Modelo de contraste: árbol de decisión

![Dispersión real frente a predicho del árbol de decisión](imagenes/09_arbol_real_vs_predicho.png)

*Figura 9. NO₂ real frente a NO₂ predicho por el árbol de decisión (max_depth = 5).*

**Error cuadrático medio (MSE) = 31.474**

**Interpretación:** La raíz del error cuadrático medio (RMSE) es √31.474 ≈ **5.61 ppb**. Este valor debe compararse con la desviación estándar de la variable objetivo, 6.37 ppb, que representa el error que cometería un modelo nulo que siempre predijera la media. La mejora es de apenas un 12 %, modesta pero superior a la del modelo lineal.

Visualmente, la dispersión muestra mayor variabilidad en el eje vertical que la Figura 6: el árbol sí produce predicciones diferenciadas en lugar de concentrarlas en torno a la media. No obstante, la alineación con la diagonal sigue siendo pobre.

![Importancia relativa de las características](imagenes/10_importancia_caracteristicas.png)

*Figura 10. Importancia relativa normalizada de los predictores según el árbol de decisión.*

**Importancias obtenidas:** `[0.0345, 0.6827, 0.2035, 0.0506, 0.0101, 0.0186]`

| Variable | Importancia | Porcentaje |
|---|---|---|
| Year | 0.0345 | 3.45 % |
| **Month** | **0.6827** | **68.27 %** |
| **Day** | **0.2035** | **20.35 %** |
| DayOfWeek | 0.0506 | 5.06 % |
| Obs_Count | 0.0101 | 1.01 % |
| Percent_Complete | 0.0186 | 1.86 % |

**Interpretación:** Este resultado constituye el hallazgo más informativo del trabajo. El árbol asigna casi el 70 % de la importancia a **`Month`**, precisamente la variable que en el modelo lineal tenía el coeficiente más insignificante (0.0149, p = 0.897).

La contradicción es solo aparente y revela algo sustantivo: **la relación entre el mes y la concentración de NO₂ existe, pero es no lineal**. El ciclo estacional del NO₂ es aproximadamente sinusoidal —valores elevados en invierno, bajos en verano, elevados nuevamente al final del año—. Un coeficiente lineal único no puede representar esta forma: al promediar una pendiente ascendente en la primera mitad del año con una descendente en la segunda, el resultado neto tiende a cero. El árbol de decisión, en cambio, puede segmentar el año en tramos y asignar predicciones distintas a cada uno, capturando así el patrón.

La correspondiente baja importancia de `Obs_Count` (1.01 %) y `Percent_Complete` (1.86 %) confirma que su aparente relevancia en el modelo lineal era un artefacto de la colinealidad.

---

## 4. Discusión

### 4.1 Sobre la efectividad del modelo de regresión lineal

La evidencia acumulada permite una conclusión inequívoca: **el modelo de regresión lineal múltiple no fue efectivo** para predecir la concentración máxima diaria de NO₂ en Miles City durante 2022–2023. Esta afirmación se sostiene en cinco pruebas convergentes:

1. Las correlaciones de Pearson entre todos los predictores y la variable objetivo son inferiores a |0.05|.
2. El R² de 0.004 indica que se explica menos del medio por ciento de la variabilidad.
3. El R² ajustado negativo señala que el modelo es inferior a la predicción por la media.
4. La prueba F global no es significativa (p = 0.801), por lo que no se rechaza H₀.
5. Ningún coeficiente individual alcanza significancia estadística; todos los intervalos de confianza contienen el cero.

Es importante enmarcar correctamente este resultado. Un modelo que no logra predecir **no equivale a un análisis fallido**. La conclusión de que un conjunto de variables no explica un fenómeno es un resultado científico legítimo, y en este caso está respaldado por un procedimiento metodológicamente correcto: los datos se limpiaron adecuadamente, la partición fue apropiada, los supuestos se verificaron y la validación se realizó mediante inferencia formal. El valor del trabajo reside precisamente en haber podido demostrar la ausencia de relación con rigor, y en haber identificado las razones de ello.

### 4.2 Causas identificadas del bajo poder predictivo

**Ausencia de variables explicativas físicamente relevantes.** El determinante principal. Las concentraciones de NO₂ dependen de dos familias de factores: las **emisiones** (densidad de tráfico, actividad industrial, consumo de combustibles) y la **dispersión atmosférica** (velocidad y dirección del viento, temperatura, altura de la capa de mezcla, estabilidad atmosférica, radiación solar, precipitación). El conjunto de datos no contiene ninguna de estas variables. Los predictores utilizados son etiquetas temporales y metadatos de calidad del muestreo, que solo podrían funcionar como aproximaciones (*proxies*) muy indirectas de los procesos reales.

**Multicolinealidad severa.** La correlación de 0.9998 entre `Obs_Count` y `Percent_Complete` refleja una dependencia funcional. Cuando dos columnas de la matriz de diseño son casi linealmente dependientes, la matriz (X'X) se aproxima a la singularidad y su inversa presenta valores muy grandes, lo que infla los errores estándar de los coeficientes [15], [16]. Las consecuencias observadas en este trabajo fueron: coeficientes de signos opuestos para variables positivamente correlacionadas, errores estándar desmesurados (8.197 para `Obs_Count`) e intervalos de confianza inutilizables.

**No linealidad de la única relación existente.** Como estableció el análisis de importancias del árbol, `Month` sí contiene información predictiva —cerca del 70 % de la que el árbol logra aprovechar—, pero en forma cíclica. La regresión lineal, por su especificación funcional, es estructuralmente incapaz de capturar patrones periódicos sin una transformación previa de la variable.

**Variables de calidad del muestreo como predictores.** Incluir `Obs_Count` y `Percent_Complete` es cuestionable desde el punto de vista conceptual: describen el funcionamiento del instrumento de medición, no el fenómeno atmosférico. Cualquier asociación que presenten con el NO₂ sería, en el mejor de los casos, espuria.

**Naturaleza estocástica del fenómeno.** Incluso con un conjunto completo de variables meteorológicas, la concentración diaria de contaminantes conserva un componente aleatorio sustancial. Ningún modelo determinista puede aspirar a explicar la totalidad de la varianza.

### 4.3 Sobre los supuestos del modelo

El examen de los supuestos arrojó resultados mixtos. La **linealidad** no se cumple para `Month`, la variable con mayor contenido informativo. La **normalidad de los residuos** se satisface de manera aproximada, con una asimetría positiva heredada de la distribución original de la variable. La **homocedasticidad** no presenta violaciones claras, aunque el diagnóstico está limitado por el estrecho rango de valores predichos. La **independencia** no fue verificada formalmente, y constituye una limitación relevante: al tratarse de una serie temporal diaria, es plausible la presencia de **autocorrelación** en los residuos, que podría evaluarse mediante el estadístico de Durbin-Watson.

### 4.4 Interpretación estadística y probabilística

Desde la óptica de la inferencia estadística, el resultado central es la **no rechazo de la hipótesis nula**. El p-valor de 0.801 asociado al estadístico F debe leerse como una probabilidad condicional: bajo el supuesto de que H₀ es verdadera (ausencia total de relación lineal en la población), la probabilidad de obtener por azar muestral un ajuste igual o superior al observado es del 80.1 %. Con una probabilidad tan alta de que el resultado sea producto del azar, no existe base para afirmar la existencia de relación alguna.

Conviene precisar una distinción metodológica: no rechazar H₀ **no demuestra** que H₀ sea verdadera. La conclusión correcta es que los datos disponibles no proporcionan evidencia suficiente para rechazarla. Con variables diferentes o con una especificación funcional distinta, el resultado podría ser otro.

Desde la perspectiva de la teoría de la probabilidad, la distribución empírica del NO₂ —unimodal, asimétrica positiva, acotada inferiormente en cero— sugiere que un modelo **log-normal** o **gamma** describiría mejor el proceso generador de datos que la distribución normal implícita en la regresión lineal ordinaria. Esto abre la vía a los modelos lineales generalizados (GLM) como alternativa metodológica.

### 4.5 Interpretación ambiental de los resultados

Más allá del desempeño del modelo, los datos ofrecen información ambiental de valor. La concentración media de 10.47 ppb y el máximo de 35 ppb se sitúan muy por debajo del estándar nacional de calidad del aire de la EPA para NO₂ (100 ppb en promedio horario). La estación de Miles City registra, por tanto, condiciones de **calidad del aire buena** durante la totalidad del período analizado.

La ausencia de diferencia apreciable entre 2022 y 2023 (coeficiente de −0.31 ppb por año, p = 0.514) indica **estabilidad interanual**, sin tendencias de deterioro ni de mejora detectables en esta ventana temporal de dos años. La ausencia de un efecto de día de la semana, contrastante con lo que suele observarse en entornos urbanos, es coherente con el carácter rural del emplazamiento y con la baja incidencia del tráfico vehicular de tipo laboral.

### 4.6 Limitaciones del estudio

- Los datos provienen de una **única estación de monitoreo**, por lo que los resultados no son generalizables al conjunto del estado de Montana.
- El horizonte temporal de **dos años** es insuficiente para el análisis de tendencias de largo plazo.
- No se dispuso de **variables meteorológicas**, principal deficiencia del conjunto de datos.
- No se evaluó la **autocorrelación temporal** de los residuos.
- No se aplicaron transformaciones a la variable objetivo (logarítmica o raíz cuadrada) que pudieran mitigar la asimetría.
- No se calcularon explícitamente las métricas MAE, MSE y RMSE sobre el conjunto de prueba para el modelo lineal, lo que habría permitido una comparación numérica directa con el árbol de decisión.

### 4.7 Recomendaciones para trabajos futuros

1. **Incorporar variables meteorológicas** (temperatura, velocidad y dirección del viento, humedad relativa, presión, precipitación) a partir de bases como NOAA o Meteostat. Es la mejora de mayor impacto potencial.
2. **Codificar la estacionalidad de forma adecuada** mediante transformaciones trigonométricas: `sin(2π · mes/12)` y `cos(2π · mes/12)`, que preservan la naturaleza cíclica del calendario, o mediante variables dicotómicas por estación del año.
3. **Eliminar la redundancia** conservando solo una de las variables `Obs_Count` / `Percent_Complete`, o excluyendo ambas por no ser predictores del fenómeno.
4. **Aplicar transformación logarítmica** a la variable objetivo para aproximar su distribución a la normal.
5. **Explorar modelos alternativos**: Random Forest, Gradient Boosting o modelos de series temporales (SARIMA, Prophet) que modelen explícitamente la estacionalidad y la autocorrelación.
6. **Incorporar rezagos temporales** (*lags*) de la propia variable, dado que la concentración de un día está correlacionada con la del día anterior.
7. **Ampliar el análisis a múltiples estaciones** de Montana para obtener variabilidad espacial.
8. **Utilizar validación cruzada** (*k-fold cross-validation*) en lugar de una única partición, para obtener estimaciones más estables del error.

---

## 5. Conclusiones

**Primera.** Se analizaron 730 registros diarios de concentración máxima horaria de NO₂ correspondientes a la estación Miles City – Pines Hills, condado de Custer, Montana, durante los años 2022 y 2023. El conjunto resultó completo, sin valores faltantes en las variables de interés.

**Segunda.** La concentración de NO₂ presentó una media de 10.47 ppb, mediana de 9.00 ppb, desviación estándar de 6.37 ppb y un rango de 0 a 35 ppb. La distribución es unimodal con asimetría positiva, comportamiento característico de los contaminantes atmosféricos.

**Tercera.** Todos los valores registrados se mantuvieron muy por debajo del estándar nacional de calidad del aire de la EPA (100 ppb), lo que permite caracterizar el área como de calidad del aire buena durante todo el período.

**Cuarta.** El modelo de regresión lineal múltiple **no resultó efectivo**. El coeficiente de determinación de 0.004 indica que explica únicamente el 0.4 % de la variabilidad del NO₂, y el R² ajustado negativo (−0.004) revela que su desempeño es inferior al de una predicción basada en la media.

**Quinta.** La prueba F global no fue estadísticamente significativa (F = 0.51; p = 0.801), por lo que **no se rechaza la hipótesis nula** de ausencia de relación lineal. Ningún coeficiente individual alcanzó significancia al nivel α = 0.05, y todos los intervalos de confianza al 95 % incluyeron el valor cero.

**Sexta.** Se identificó **multicolinealidad severa** entre las variables `Obs_Count` y `Percent_Complete` (r = 0.9998), producto de una dependencia funcional entre ambas. Este problema explica la inestabilidad de los coeficientes, la inversión de signos y la magnitud desproporcionada de los errores estándar.

**Séptima.** El árbol de decisión, con un RMSE de 5.61 ppb frente a una desviación estándar de 6.37 ppb, superó marginalmente al modelo lineal y atribuyó el 68.3 % de la importancia predictiva a la variable `Month`. Esto demuestra que **sí existe una señal estacional en los datos, pero de naturaleza no lineal**, inaccesible para una especificación lineal simple.

**Octava.** La causa fundamental del bajo poder predictivo es la ausencia, en el conjunto de datos, de las variables meteorológicas y de emisión que gobiernan físicamente la concentración de NO₂ en la atmósfera.

**Novena.** El resultado negativo constituye un hallazgo válido y metodológicamente sólido. La verificación de supuestos, la validación mediante inferencia formal y la comparación con un modelo de contraste permitieron no solo constatar la ausencia de relación lineal, sino explicar sus causas y delinear una ruta concreta de mejora para trabajos posteriores.

---

## 6. Referencias bibliográficas

*Formato de citación: IEEE (Institute of Electrical and Electronics Engineers). Las referencias se numeran según su orden de primera aparición en el texto y se citan mediante corchetes.*

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

[11] D. C. Montgomery, E. A. Peck, and G. G. Vining, *Introduction to Linear Regression Analysis*, 5th ed. Hoboken, NJ, USA: John Wiley & Sons, 2012.

[12] T. Hastie, R. Tibshirani, and J. Friedman, *The Elements of Statistical Learning: Data Mining, Inference, and Prediction*, 2nd ed. New York, NY, USA: Springer, 2009.

[13] U.S. Environmental Protection Agency, "NAAQS Table: National Ambient Air Quality Standards," EPA, 2024. [Online]. Available: https://www.epa.gov/criteria-air-pollutants/naaqs-table. [Accessed: Sep. 17, 2026].

[14] J. Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. Hillsdale, NJ, USA: Lawrence Erlbaum Associates, 1988.

[15] D. N. Gujarati and D. C. Porter, *Econometría*, 5th ed. Ciudad de México, México: McGraw-Hill, 2010.

[16] N. R. Draper and H. Smith, *Applied Regression Analysis*, 3rd ed. New York, NY, USA: John Wiley & Sons, 1998.

---

## Anexo A. Tabla consolidada de resultados numéricos

| Indicador | Valor | Fuente en el notebook |
|---|---|---|
| Registros totales | 730 | `df.info()` |
| Registros de entrenamiento | 511 | 70 % de la partición |
| Registros de prueba | 219 | `predictions.shape` |
| Predictores | 6 | `X.shape[1]` |
| Grados de libertad residuales (OLS) | 723 | `summary()` |
| Media de NO₂ | 10.47 ppb | `df.describe()` |
| Mediana de NO₂ | 9.00 ppb | `df.describe()` |
| Desviación estándar de NO₂ | 6.37 ppb | `df.describe()` |
| Mínimo / Máximo de NO₂ | 0.00 / 35.00 ppb | `df.describe()` |
| Rango intercuartílico | 8.00 ppb | 14.00 − 6.00 |
| Coeficiente de variación | ≈ 61 % | 6.37 / 10.47 |
| Correlación máxima con NO₂ | 0.0439 (`Obs_Count`) | `.corr()` |
| Correlación `Obs_Count`–`Percent_Complete` | 0.9998 | `.corr()` |
| Intercepto del modelo lineal | 1566.83 | `lm.intercept_` |
| R² (OLS) | 0.004 | `summary()` |
| R² ajustado (OLS) | −0.004 | `summary()` |
| Estadístico F | 0.5100 | `summary()` |
| p-valor de la prueba F | 0.801 | `summary()` |
| AIC / BIC | 4785 / 4817 | `summary()` |
| MSE del árbol de decisión | 31.474 | `mean_squared_error()` |
| RMSE del árbol de decisión | ≈ 5.61 ppb | √31.474 |
| Importancia de `Month` (árbol) | 68.27 % | `feature_importances_` |

## Anexo B. Contraste entre los dos modelos

| Criterio | Regresión lineal múltiple | Árbol de decisión |
|---|---|---|
| Tipo de modelo | Paramétrico | No paramétrico |
| Relaciones que captura | Solo lineales | Lineales y no lineales |
| Variable más influyente | `Obs_Count` *(artefacto de colinealidad)* | `Month` (68.27 %) |
| Capacidad explicativa | R² = 0.004 | RMSE ≈ 5.61 ppb |
| Comparación con el modelo nulo | Inferior (R² ajustado negativo) | Superior en ≈ 12 % |
| Significancia estadística | No significativo (p = 0.801) | No aplica |
| Interpretabilidad de coeficientes | Nula por multicolinealidad | Importancias interpretables |
| Sensible a multicolinealidad | Sí, severamente | No |
| Conclusión | **No efectivo** | Marginalmente superior |

## Anexo C. Contraste de hipótesis

| Elemento | Formulación |
|---|---|
| Hipótesis nula (H₀) | β₁ = β₂ = β₃ = β₄ = β₅ = β₆ = 0 |
| Hipótesis alternativa (H₁) | Al menos un βᵢ ≠ 0 |
| Estadístico de prueba | F de Fisher-Snedecor |
| Valor calculado | F = 0.5100 |
| p-valor | 0.801 |
| Nivel de significancia | α = 0.05 |
| Regla de decisión | Rechazar H₀ si p < α |
| **Decisión** | **0.801 > 0.05 → No se rechaza H₀** |
| Conclusión | No hay evidencia estadística de relación lineal entre los predictores y el NO₂ |

---
