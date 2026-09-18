# Análisis de la Calidad del Aire mediante Regresión Lineal: Dióxido de Nitrógeno (NO₂) en Montana, EE. UU. (2022 – 2023)

---

**Componente analizado:** Dióxido de nitrógeno (NO₂)

**Período de estudio:** 1 de enero de 2022 – 31 de diciembre de 2023

**Área geográfica:** Montana, Estados Unidos

**Fuente de datos:** Air Quality System (AQS), U.S. Environmental Protection Agency

**Unidad de medida:** partes por billón (ppb)

**Registros analizados:** 730 observaciones diarias

### Localización del estudio

Los datos provienen de una estación de monitoreo ubicada en el estado de Montana, cuyos datos de identificación son los siguientes:

| Dato | Valor |
|---|---|
| Estado | Montana |
| Condado | Custer |
| Ciudad | Miles City |
| Estación de monitoreo | Pines Hills |
| Identificador (Site ID) | 300170005 |
| Latitud | 46.411389° N |
| Longitud | −105.812778° O |

Montana es un estado de baja densidad poblacional situado en el noroeste de Estados Unidos, con una economía apoyada en la agricultura, la ganadería y la actividad extractiva. Carece de grandes conurbaciones industriales, y la estación analizada se encuentra en un entorno de llanuras semiáridas pertenecientes a las Grandes Llanuras (*Great Plains*). Este contexto resulta relevante para el estudio porque permite observar el comportamiento del NO₂ en condiciones de contaminación de fondo, lejos de los focos de emisión intensiva que caracterizan a las zonas metropolitanas.

---

## Tabla de contenido

1. [Introducción](#1-introducción)
2. [Metodología](#2-metodología)
3. [Resultados](#3-resultados)
4. [Discusión](#4-discusión)
5. [Conclusiones](#5-conclusiones)
6. [Referencias bibliográficas](#6-referencias-bibliográficas)
7. [Anexo A. Resultados numéricos consolidados](#anexo-a-resultados-numéricos-consolidados)
8. [Anexo B. Contraste entre los dos modelos](#anexo-b-contraste-entre-los-dos-modelos)
9. [Anexo C. Contraste de hipótesis](#anexo-c-contraste-de-hipótesis)

---

## 1. Introducción

### 1.1 Contexto del problema

El dióxido de nitrógeno (NO₂) es un gas de color pardo-rojizo que pertenece a la familia de los óxidos de nitrógeno (NOₓ). Se origina sobre todo en los procesos de combustión a alta temperatura, como los que ocurren en los motores de los vehículos, en las plantas de generación eléctrica, en las calderas industriales y en la quema de biomasa. Su importancia para la calidad del aire se explica por dos razones distintas.

La primera es que se trata de un contaminante primario con efectos directos sobre la salud respiratoria. Cuando la exposición se prolonga en el tiempo, aparecen cuadros de inflamación de las vías respiratorias, se agravan los síntomas del asma y se reduce la función pulmonar. Estos efectos golpean con más fuerza a los grupos vulnerables, entre ellos los niños, los adultos mayores y quienes ya padecen alguna enfermedad respiratoria [1].

La segunda razón es que el NO₂ funciona como precursor de otros contaminantes. Al reaccionar con compuestos orgánicos volátiles bajo la acción de la radiación solar, interviene en la formación de ozono troposférico. Además contribuye a generar material particulado fino (PM₂.₅) a través de la formación de nitratos secundarios, y participa en los procesos de deposición ácida que afectan a suelos y cuerpos de agua [2].

### 1.2 Justificación del área de estudio

Montana ofrece un caso de estudio poco habitual dentro del territorio estadounidense. Al no contar con grandes centros industriales ni con un parque automotor concentrado, las concentraciones esperadas de NO₂ son bajas si se las compara con las de una ciudad grande. Esto convierte al estado en un buen escenario para evaluar cómo se comporta un modelo predictivo cuando trabaja sobre niveles de contaminación de fondo y no sobre episodios de contaminación aguda, que son los que la mayoría de los estudios suele abordar.

### 1.3 Objetivos

**Objetivo general**

Evaluar si resulta posible predecir la concentración máxima diaria de NO₂ registrada en Montana durante los años 2022 y 2023, a partir de variables temporales y de cobertura de muestreo, mediante un modelo de regresión lineal múltiple.

**Objetivos específicos**

- Realizar un análisis exploratorio sobre los 730 registros diarios que componen la serie.
- Caracterizar estadísticamente la distribución del NO₂ mediante medidas de tendencia central, dispersión y forma.
- Medir la asociación lineal entre las variables predictoras y la variable objetivo a través de la matriz de correlación de Pearson.
- Construir, entrenar y evaluar un modelo de regresión lineal múltiple utilizando una partición de entrenamiento y prueba.
- Comprobar si el modelo cumple con los supuestos que exige la regresión lineal.
- Contrastar el desempeño del modelo lineal con el de un modelo no lineal de referencia.
- Validar la significancia estadística de los resultados mediante inferencia formal.

### 1.4 Hipótesis de trabajo

El estudio se plantea sobre dos hipótesis enfrentadas:

- **Hipótesis nula (H₀):** los coeficientes del modelo son conjuntamente iguales a cero, de modo que las variables predictoras no explican la variabilidad del NO₂.
- **Hipótesis alternativa (H₁):** al menos uno de los coeficientes es distinto de cero, lo que indicaría una relación lineal significativa entre los predictores y la concentración de NO₂.

Para decidir entre ambas se adopta un nivel de significancia de α = 0.05, que es el valor convencional en este tipo de análisis.

---

## 2. Metodología

### 2.1 Enfoque y diseño

La investigación es de tipo cuantitativo y de alcance correlacional-predictivo. El diseño es no experimental y longitudinal retrospectivo, ya que no se manipuló ninguna variable: se trabajó sobre registros que la red oficial de monitoreo ya había generado, con el propósito de establecer relaciones de asociación y evaluar la capacidad predictiva del modelo.

### 2.2 Fuente y obtención de los datos

Los datos se obtuvieron del sistema Air Quality System (AQS), la plataforma pública de datos de calidad del aire de la Agencia de Protección Ambiental de Estados Unidos [3]. Esta base reúne las mediciones de la red nacional de estaciones de monitoreo y permite filtrar la descarga por contaminante, por estado y por período.

El procedimiento de obtención siguió estos pasos:

1. Se ingresó al portal de datos de calidad del aire exterior de la EPA.
2. Se seleccionó el dióxido de nitrógeno (NO₂) como contaminante de interés.
3. Se delimitó la búsqueda al estado de Montana.
4. Se estableció el rango temporal comprendido entre el 1 de enero de 2022 y el 31 de diciembre de 2023.
5. Se descargó el archivo resultante en formato CSV.

<!-- ESPACIO PARA IMAGEN -->

**Figura 1.** Búsqueda y filtrado de datos de NO₂ en el portal AQS de la EPA.

El archivo descargado contiene 730 registros, que corresponden a los 365 días de 2022 más los 365 días de 2023. Cada fila representa un día, y la variable de interés es la concentración máxima horaria registrada en esa jornada, expresada en partes por billón.

### 2.3 Herramientas computacionales

El análisis se desarrolló íntegramente en **Google Colab**, el entorno de notebooks en la nube de Google, que ejecuta Python 3 sin necesidad de instalar nada en el equipo local y mantiene preinstaladas las bibliotecas científicas más usadas. Trabajar en esta plataforma facilita además el trabajo colaborativo, ya que varios integrantes del grupo pueden abrir y ejecutar el mismo notebook.

Las bibliotecas empleadas fueron las siguientes:

| Biblioteca | Alias | Sentencia de importación | Para qué se usó | Ref. |
|---|---|---|---|---|
| `numpy` | `np` | `import numpy as np` | Cálculo numérico sobre arreglos, empleado en el cómputo de los errores estándar | [4] |
| `pandas` | `pd` | `import pandas as pd` | Carga, limpieza y transformación de los datos en formato de tabla | [5] |
| `matplotlib.pyplot` | `plt` | `import matplotlib.pyplot as plt` | Generación de los gráficos base: histogramas, dispersión y barras | [6] |
| `seaborn` | `sns` | `import seaborn as sns` | Gráficos estadísticos de mayor nivel, como el pairplot y el mapa de calor | [7] |
| `scikit-learn` | — | `from sklearn... import ...` | Partición de datos, regresión lineal, árbol de decisión y métricas | [8] |
| `statsmodels.api` | `sm` | `import statsmodels.api as sm` | Inferencia estadística formal mediante mínimos cuadrados ordinarios | [9] |

Conviene aclarar que la instrucción `%matplotlib inline` no es una función de Python, sino un comando mágico propio de los entornos Jupyter y Colab. Lo que hace es incrustar las figuras dentro de la salida de la celda en lugar de abrirlas en una ventana aparte.

### 2.4 Funciones y métodos empleados

#### Tabla resumen de comandos

La siguiente tabla reúne todos los comandos utilizados en el notebook, ordenados según la etapa del trabajo en la que aparecen. Cada uno se explica con más detalle en los apartados que siguen.

| # | Comando o función | Biblioteca | Etapa | Qué hace | Resultado |
|---|---|---|---|---|---|
| 1 | `pd.read_csv()` | pandas | Carga | Lee un archivo CSV y lo convierte en tabla | Tabla de 730 × 21 |
| 2 | `df.head()` | pandas | Inspección | Muestra las primeras cinco filas | Verificación de la carga |
| 3 | `df.info(verbose=True)` | pandas | Inspección | Reporta filas, tipos de dato y valores no nulos | 19 columnas completas |
| 4 | `df.describe().round(2)` | pandas | Descriptiva | Resume estadísticamente las variables numéricas | Media, desviación, cuartiles |
| 5 | `df.columns` | pandas | Inspección | Devuelve los nombres de las columnas | Lista de variables |
| 6 | `pd.to_datetime()` | pandas | Limpieza | Convierte texto a tipo fecha | Columna `Date` como fecha |
| 7 | `.dt.year`, `.dt.month`, `.dt.day`, `.dt.dayofweek` | pandas | Nuevas variables | Extrae componentes de una fecha | Cuatro variables temporales |
| 8 | `df[[...]]` | pandas | Limpieza | Conserva solo las columnas relevantes | De 21 a 7 columnas |
| 9 | `df.rename(columns={})` | pandas | Limpieza | Cambia el nombre de las columnas | Nombres cortos y sin espacios |
| 10 | `sns.pairplot()` | seaborn | Exploración | Cruza todas las variables entre sí | Figura 5 |
| 11 | `.plot.hist(bins=25)` | pandas | Exploración | Dibuja un histograma de frecuencias | Figura 6 |
| 12 | `.plot.density()` | pandas | Exploración | Dibuja la curva de densidad | Figura 7 |
| 13 | `df.select_dtypes()` | pandas | Correlación | Filtra únicamente las columnas numéricas | Subconjunto numérico |
| 14 | `.corr()` | pandas | Correlación | Calcula la matriz de correlación de Pearson | Matriz de 7 × 7 |
| 15 | `sns.heatmap(annot=True)` | seaborn | Correlación | Representa la matriz como mapa de calor | Figura 9 |
| 16 | `train_test_split()` | scikit-learn | Partición | Separa entrenamiento y prueba | 511 y 219 registros |
| 17 | `LinearRegression()` | scikit-learn | Modelado | Crea el modelo lineal | Objeto `lm` |
| 18 | `lm.fit()` | scikit-learn | Entrenamiento | Estima los coeficientes | Modelo ajustado |
| 19 | `lm.intercept_` | scikit-learn | Resultados | Devuelve el término independiente | 1566.83 |
| 20 | `lm.coef_` | scikit-learn | Resultados | Devuelve los seis coeficientes | Arreglo de betas |
| 21 | `lm.predict()` | scikit-learn | Predicción | Aplica el modelo a datos nuevos | 219 predicciones |
| 22 | `np.square()`, `np.sum()`, `np.sqrt()` | numpy | Inferencia | Operaciones del error estándar | Columna de errores |
| 23 | `gridspec.GridSpec(2, 3)` | matplotlib | Visualización | Ordena varios gráficos en cuadrícula | Figura 13 |
| 24 | `sns.histplot(kde=True)` | seaborn | Diagnóstico | Histograma de residuos con curva | Figura 15 |
| 25 | `plt.scatter()` | matplotlib | Diagnóstico | Dibuja diagramas de dispersión | Figuras 14, 16 y 18 |
| 26 | `tree.DecisionTreeRegressor()` | scikit-learn | Contraste | Ajusta un árbol de decisión | Modelo no lineal |
| 27 | `tree_model.feature_importances_` | scikit-learn | Interpretación | Mide la importancia de cada variable | Figura 19 |
| 28 | `metrics.mean_squared_error()` | scikit-learn | Evaluación | Calcula el error cuadrático medio | MSE = 31.474 |
| 29 | `plt.barh()` | matplotlib | Visualización | Dibuja barras horizontales | Figura 19 |
| 30 | `sm.add_constant()` | statsmodels | Inferencia | Agrega la columna del intercepto | Matriz de diseño |
| 31 | `sm.OLS().fit()` | statsmodels | Inferencia | Ajusta mínimos cuadrados ordinarios | Objeto de resultados |
| 32 | `.summary()` | statsmodels | Inferencia | Genera el reporte estadístico completo | Figura 17 |

#### 2.4.1 Carga e inspección

El trabajo comienza con **`pd.read_csv(ruta)`**, que lee el archivo separado por comas y lo convierte en un `DataFrame`, la estructura de tabla con la que trabaja pandas.

Una vez cargado el archivo, **`df.head()`** devuelve las primeras cinco filas. Sirve para confirmar de un vistazo que la lectura funcionó y que cada columna quedó con el tipo de dato correcto.

El paso siguiente es **`df.info(verbose=True)`**, que reporta cuántos registros hay, cómo se llama cada columna, cuántos valores no nulos contiene y de qué tipo son. Esta es la herramienta principal para detectar valores faltantes antes de empezar a analizar.

Con **`df.describe().round(2)`** se obtiene el resumen estadístico de las variables numéricas, que incluye el conteo, la media, la desviación estándar, el mínimo, los tres cuartiles y el máximo. El método `.round(2)` simplemente limita la salida a dos decimales para que la tabla sea legible.

Finalmente, **`df.columns`** devuelve los nombres de todas las columnas, algo útil cuando se necesita referenciarlas en el código.

#### 2.4.2 Limpieza y transformación

La columna de fechas llegó del archivo original como texto, de modo que fue necesario convertirla con **`pd.to_datetime(df['Date'], format='%m/%d/%Y')`**. Sin esta conversión Python no reconoce la columna como una fecha, y por lo tanto no permite extraer de ella ninguna información temporal.

Hecha la conversión, los accesorios **`.dt.year`, `.dt.month`, `.dt.day` y `.dt.dayofweek`** permiten descomponer cada fecha en sus partes. Este proceso se conoce como ingeniería de características, y consiste en crear variables nuevas a partir de las que ya existen. En este caso, de una sola columna de fechas se obtuvieron cuatro variables predictoras. El accesorio `dayofweek` codifica el día de la semana con números del 0 al 6, donde el 0 corresponde al lunes.

A continuación se seleccionaron únicamente siete columnas de las veintiuna originales. Se descartaron aquellas que resultaban constantes para esta estación, como el identificador del sitio, el estado, el condado o las coordenadas, y también las que estaban completamente vacías. El motivo es sencillo: una variable que toma siempre el mismo valor tiene varianza cero, y algo que no varía no puede explicar la variación de otra cosa.

Por último, **`df.rename(columns={...})`** se usó para acortar los nombres de las columnas y quitarles los espacios, de manera que quedaran como `Obs_Count`, `Percent_Complete` y `NO2_Max`, más cómodos de escribir en el código.

#### 2.4.3 Análisis exploratorio y visualización

El primer gráfico del análisis se genera con **`sns.pairplot(df)`**, que arma una matriz donde cada variable se cruza con todas las demás. En las celdas fuera de la diagonal aparecen diagramas de dispersión, y en la diagonal, histogramas. Es una forma rápida de detectar a simple vista relaciones lineales, patrones curvos, agrupamientos o valores atípicos.

Para estudiar la variable objetivo por separado se usaron dos gráficos complementarios. El primero, **`.plot.hist(bins=25)`**, divide el rango de valores en veinticinco intervalos y cuenta cuántas observaciones caen en cada uno. El segundo, **`.plot.density()`**, calcula una estimación de densidad por núcleo, que viene a ser la versión suavizada y continua del histograma y muestra con más claridad dónde se concentra la masa de probabilidad.

Antes de calcular las correlaciones fue necesario aplicar **`df.select_dtypes(include=[np.number])`**, que filtra la tabla y deja solo las columnas numéricas, ya que el coeficiente de Pearson no puede calcularse sobre texto. Sobre ese subconjunto se aplicó **`.corr()`**, que devuelve la matriz de correlaciones entre todos los pares de variables.

Esa matriz se representó gráficamente con **`sns.heatmap(matriz, annot=True, linewidths=2)`**. El parámetro `annot=True` hace que el valor numérico aparezca escrito dentro de cada celda, lo que evita tener que consultar la tabla por separado.

#### 2.4.4 Separación de variables y partición de datos

La separación entre predictores y variable objetivo sigue la convención habitual del aprendizaje supervisado:

```python
X = df[l_column[0:len_feature-1]]   # matriz de predictores (6 columnas)
Y = df[l_column[len_feature-1]]     # vector objetivo (NO2_Max)
```

La función **`train_test_split(X, Y, test_size=0.3, random_state=123)`** divide el conjunto en cuatro partes de forma aleatoria. Sus parámetros funcionan de la siguiente manera:

| Parámetro | Valor usado | Qué significa | Efecto en este trabajo |
|---|---|---|---|
| `X` | Tabla de 730 × 6 | Matriz de predictores | Las seis variables explicativas |
| `Y` | Serie de 730 valores | Vector objetivo | La variable `NO2_Max` |
| `test_size` | `0.3` | Proporción destinada a prueba | 219 registros |
| `train_size` | `0.7` (implícito) | Proporción destinada a entrenamiento | 511 registros |
| `random_state` | `123` | Semilla del generador aleatorio | Garantiza la reproducibilidad |
| `shuffle` | `True` (por defecto) | Mezcla los datos antes de dividir | Evita el sesgo por orden cronológico |

Los cuatro objetos que devuelve la función son los siguientes:

| Objeto | Contenido | Tamaño |
|---|---|---|
| `X_train` | Predictores de entrenamiento | 511 × 6 |
| `X_test` | Predictores de prueba | 219 × 6 |
| `Y_train` | Valores reales de entrenamiento | 511 |
| `Y_test` | Valores reales de prueba | 219 |

La razón de fondo para hacer esta división es evitar el sobreajuste [10]. Si un modelo se evalúa con los mismos datos que se usaron para entrenarlo, el resultado será siempre demasiado optimista, porque el modelo ya conoce esas respuestas. Al reservar una parte de los datos que el modelo nunca ve durante el entrenamiento, se puede medir su verdadera capacidad de generalizar ante información nueva.

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
| `.intercept_` | Atributo | `lm.intercept_` | El término independiente β₀ |
| `.coef_` | Atributo | `lm.coef_` | Los seis coeficientes β₁ a β₆ |
| `.predict(X)` | Método | `lm.predict(X_test)` | Un arreglo con 219 predicciones |

La diferencia entre método y atributo vale la pena señalarla. Los métodos llevan paréntesis porque ejecutan una acción, mientras que los atributos terminan en guion bajo. Esa convención de scikit-learn indica que el valor se aprendió durante el entrenamiento, de modo que no existe hasta que se llama a `.fit()` [8].

En cuanto a la interpretación, cada coeficiente representa el cambio esperado en la concentración de NO₂ cuando la variable correspondiente aumenta en una unidad y todas las demás se mantienen constantes. El desarrollo formal del estimador y de sus propiedades puede consultarse en [11].

#### 2.4.6 Inferencia sobre los coeficientes

Para saber si un coeficiente es distinto de cero por una razón real o simplemente por azar muestral, se calcularon manualmente el error estándar y el estadístico t de cada uno.

Primero se determinaron los grados de libertad como `dfN = n − k`, donde n son las 511 observaciones de entrenamiento y k los 6 predictores. Luego se obtuvo la suma de cuadrados del error mediante `np.sum(np.square(train_pred − Y_train))`. A partir de ahí se calculó el error estándar, que mide la incertidumbre asociada a cada estimación, y finalmente el estadístico t, que resulta de dividir el coeficiente entre su error estándar.

Ese estadístico indica a cuántos errores estándar de distancia del cero se encuentra el coeficiente estimado. Como regla práctica, un valor absoluto mayor que 1.96 sugiere significancia al nivel del 5 %.

#### 2.4.7 Verificación de supuestos

La regresión lineal descansa sobre cuatro supuestos que conviene comprobar antes de dar por válidos sus resultados:

| Supuesto | Qué exige | Cómo se verificó | Figura |
|---|---|---|---|
| Linealidad | La relación entre predictores y respuesta debe ser recta | Diagramas de dispersión individuales | Figura 13 |
| Normalidad de residuos | Los errores deben distribuirse normalmente en torno a cero | Histograma de residuos con curva de densidad | Figura 15 |
| Homocedasticidad | La varianza del error debe ser constante | Residuos frente a valores predichos | Figura 16 |
| Independencia | Las observaciones no deben estar correlacionadas entre sí | Estadístico de Durbin-Watson (no aplicado) | — |

El tratamiento formal de estos supuestos y de las consecuencias que acarrea su incumplimiento puede consultarse en [11] y [16].

#### 2.4.8 Modelo de contraste: árbol de decisión

Para tener un punto de comparación se ajustó un segundo modelo con **`tree.DecisionTreeRegressor(max_depth=5, random_state=10)`**. Se trata de un modelo no paramétrico que va partiendo el espacio de los predictores mediante reglas de decisión sucesivas. A diferencia de la regresión lineal, puede capturar relaciones curvas e interacciones entre variables sin que haya que especificarlas de antemano [12].

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
| `Adj. R-squared` | El R² penalizado por la cantidad de predictores | Si resulta negativo, el modelo es peor que predecir la media |
| `F-statistic` | La significancia conjunta de todos los coeficientes | Un valor alto indica un modelo más significativo |
| `Prob (F-statistic)` | El p-valor de la prueba F global | Si es menor que 0.05, se rechaza H₀ |
| `coef` | El valor estimado de cada coeficiente | Indica el cambio en Y por unidad de X |
| `std err` | La incertidumbre de cada estimación | Cuanto mayor, menos precisa es la estimación |
| `t` | El coeficiente dividido entre su error estándar | Un valor absoluto mayor que 1.96 sugiere significancia |
| `P>\|t\|` | El p-valor individual de cada coeficiente | Si es menor que 0.05, la variable es significativa |
| `[0.025, 0.975]` | El intervalo de confianza al 95 % | Si contiene el cero, el efecto no es concluyente |
| `AIC` y `BIC` | Criterios de información | Cuanto menores, mejor el equilibrio entre ajuste y simplicidad |
| `No. Observations` | El tamaño de la muestra | 730 |
| `Df Residuals` | Los grados de libertad residuales | 723 |
| `Df Model` | La cantidad de predictores | 6 |

El marco teórico de estos indicadores se desarrolla en [15].

---

## 3. Resultados

### 3.1 Estructura del conjunto de datos

La inspección inicial confirmó que el archivo contiene 730 registros y 21 columnas. De ellas, 19 presentan valores completos en las 730 filas, mientras que las columnas `CBSA Code` y `CBSA Name` aparecen totalmente vacías, ya que corresponden a un área estadística metropolitana que no aplica a una estación rural como esta.

<img width="1102" height="615" alt="image" src="https://github.com/user-attachments/assets/220ec30c-c427-49d7-abd7-eb4143e28ce1" />

**Figura 2.** Comando `df.info(verbose=True)` y su salida, con el detalle de columnas, tipos de dato y valores no nulos.

La ausencia de valores faltantes en las variables de interés es un punto favorable, porque permitió avanzar al modelado sin necesidad de aplicar técnicas de imputación, que siempre introducen supuestos adicionales.

### 3.2 Estadística descriptiva

<img width="1102" height="392" alt="image" src="https://github.com/user-attachments/assets/24130358-c206-43bc-82ad-d7fe266af502" />

**Figura 3.** Comando `df.describe().round(2)` y su salida, con el resumen estadístico de las siete variables.

**Interpretación de la variable objetivo.** La concentración de NO₂ tiene una media de 10.47 ppb y una mediana de 9.00 ppb. Que la media supere a la mediana indica que la distribución está sesgada hacia la derecha, es decir, que existe una cola de valores altos que empuja el promedio hacia arriba.

La desviación estándar es de 6.37 ppb, lo que frente a una media de 10.47 ppb da un coeficiente de variación cercano al 61 %. Se trata de una dispersión considerable: los valores diarios se alejan bastante del promedio, lo cual ya anticipa que predecirlos no será sencillo.

Los valores se extienden entre 0 y 35 ppb, y el 50 % central de los días se ubica entre 6 y 14 ppb, de modo que el rango intercuartílico es de 8 ppb. Todos estos valores quedan muy por debajo del estándar nacional de calidad del aire de Estados Unidos, fijado en 100 ppb como promedio horario máximo diario en su percentil 98 anual [13], lo que confirma que el aire de la zona se mantiene limpio a lo largo de todo el período.

**Interpretación de las variables de cobertura.** Las variables `Obs_Count` y `Percent_Complete` tienen una mediana de 24 y de 100 % respectivamente, que son los valores máximos posibles. Esto significa que en la mayoría de los días el equipo registró las veinticuatro mediciones horarias esperadas. El mínimo de 10 observaciones, equivalente al 42 % de completitud, corresponde a jornadas en las que hubo interrupciones del equipo. Conviene tener presente que estas dos variables describen el funcionamiento del instrumento y no un fenómeno atmosférico, un punto que resultará importante en la discusión.

### 3.3 Análisis exploratorio visual

![Matriz de dispersión entre todas las variables](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/01_pairplot_melisa.png)

**Figura 4.** Matriz de dispersión de todas las variables del conjunto depurado, generada con `sns.pairplot()`.

**Interpretación.** Las celdas que cruzan `NO2_Max` con las variables temporales muestran nubes de puntos organizadas en bandas verticales, sin ninguna pendiente apreciable. Esta forma es precisamente la firma visual de la ausencia de relación lineal, porque significa que para cualquier valor del predictor la concentración de NO₂ puede tomar prácticamente todo su rango. La única estructura clara del gráfico aparece entre `Obs_Count` y `Percent_Complete`, cuyos puntos se alinean formando una recta casi perfecta y anticipan el problema que se documenta más adelante.

![Histograma de la concentración máxima diaria de NO2](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/02_histograma_no2_melisa.png)

**Figura 5.** Histograma de `NO2_Max` con veinticinco intervalos.

**Interpretación.** La distribución tiene un solo pico y se inclina hacia la derecha. La mayor cantidad de días se concentra en el intervalo que va de 5 a 10 ppb, y a partir de ahí la frecuencia cae de forma progresiva, hasta el punto de que muy pocas jornadas superan los 25 ppb. Esta forma es característica de los contaminantes atmosféricos, que se ajustan mejor a distribuciones log-normales o gamma que a la normal, porque no pueden tomar valores negativos, se acumulan cerca del límite inferior y presentan episodios extremos de manera esporádica.

![Curva de densidad de la concentración de NO2](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/03_densidad_no2_melisa.png)

**Figura 6.** Curva de densidad de `NO2_Max`, obtenida con `.plot.density()`.

**Interpretación.** La versión suavizada confirma lo que mostraba el histograma. El punto más alto de la curva se sitúa entre los 7 y los 9 ppb, algo por debajo de la media aritmética, lo cual encaja con el orden que caracteriza a las distribuciones sesgadas a la derecha, donde la moda queda por debajo de la mediana y esta por debajo de la media. La cola derecha se extiende sin cortes hasta los 35 ppb.

### 3.4 Matriz de correlación

<img width="1106" height="440" alt="image" src="https://github.com/user-attachments/assets/061f5a9e-637e-4167-9578-7e468c611ed3" />

**Figura 7.** Comando `.corr()` y su salida, con la matriz de correlaciones de Pearson entre las siete variables.

![Mapa de calor de la matriz de correlación](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/04_heatmap_correlacion_melisa.png)

**Figura 8.** Representación de la matriz de correlación como mapa de calor, generada con `sns.heatmap()`.

**Interpretación.** De esta matriz se desprenden dos hallazgos, y ambos resultan decisivos para entender lo que ocurrió después.

El primero es que ninguna variable predictora alcanza siquiera un valor absoluto de 0.05 en su correlación con `NO2_Max`. La más alta es la de `Obs_Count`, con 0.0439, un número que según los criterios convencionales de clasificación [14] corresponde a una correlación nula o trivial. Si se eleva al cuadrado, se obtiene que apenas el 0.19 % de la varianza es compartida. Desde la etapa exploratoria, entonces, ya podía preverse que el modelo lineal tendría un poder predictivo muy limitado.

| Rango de \|r\| | Interpretación | ¿Aplica a algún predictor? |
|---|---|---|
| 0.00 – 0.09 | Nula o trivial | Sí, a los seis predictores |
| 0.10 – 0.29 | Baja | No |
| 0.30 – 0.49 | Moderada | No |
| 0.50 – 0.69 | Alta | No |
| 0.70 – 1.00 | Muy alta | Solo entre `Obs_Count` y `Percent_Complete` |

El segundo hallazgo es que la correlación entre `Obs_Count` y `Percent_Complete` llega a 0.9998, prácticamente perfecta. No se trata de una casualidad, sino de una consecuencia de cómo se construyen ambas variables: el porcentaje de completitud se obtiene dividiendo las observaciones registradas entre las esperadas y multiplicando por cien, de manera que una variable es una transformación directa de la otra. Incluir las dos en un mismo modelo introduce multicolinealidad severa, un problema cuyas consecuencias se detallan en la discusión.

### 3.5 Construcción y entrenamiento del modelo lineal

La partición dejó 511 registros para entrenamiento y 219 para prueba, cifra que se verificó consultando `predictions.shape`.

<img width="1098" height="235" alt="image" src="https://github.com/user-attachments/assets/10779ad9-482b-4f7e-afca-0a67cefa9443" />

**Figura 9.** Comandos de partición con `train_test_split()` y verificación de las dimensiones resultantes.

<img width="1103" height="572" alt="image" src="https://github.com/user-attachments/assets/3542bc15-cccd-4260-b457-473e12cd88bc" />

**Figura 10.** Salida de `lm.intercept_` y `lm.coef_`, con el intercepto y los seis coeficientes estimados.

<img width="1117" height="685" alt="image" src="https://github.com/user-attachments/assets/8c1cd7c4-ec27-4fa9-854c-bb6c1862abed" />

**Figura 11.** Tabla de coeficientes con sus errores estándar y estadísticos t, calculados manualmente.

**Interpretación del intercepto.** El valor obtenido, 1566.83 ppb, no tiene ningún sentido físico. Representa lo que el modelo predeciría si todas las variables valieran cero, incluida la variable `Year`, una condición que nunca podría darse. Su magnitud desproporcionada se explica por una cuestión de escala: como `Year` toma valores cercanos a 2022 y su coeficiente es de −0.7727, el producto de ambos ronda los −1562, y el intercepto debe compensar esa cifra para que la predicción final caiga dentro del rango observado de 0 a 35 ppb.

**Interpretación de los coeficientes temporales.** Todos ellos resultan de una magnitud despreciable. Un cambio de un mes modifica la predicción en apenas 0.0149 ppb, y un cambio de día de la semana en 0.0335 ppb. Frente a una desviación estándar de 6.37 ppb en la variable objetivo, estos efectos son irrelevantes en términos prácticos.

**Interpretación de los coeficientes de cobertura.** Los de `Obs_Count` y `Percent_Complete` aparecen como los de mayor magnitud, pero presentan una anomalía llamativa: tienen signos opuestos, uno positivo y otro negativo, a pesar de que ambas variables están correlacionadas al 0.9998. Esta inversión de signos es un síntoma clásico de multicolinealidad, y ocurre porque los coeficientes terminan compensándose entre sí, lo que hace que pierdan toda interpretación individual.

**Advertencia metodológica.** Los errores estándar que se calcularon manualmente en el notebook emplean una fórmula que considera la variabilidad de cada predictor de forma aislada, sin incorporar la matriz de covarianzas completa. Cuando existe colinealidad como la detectada aquí, ese procedimiento subestima los errores estándar y, en consecuencia, infla artificialmente los estadísticos t. Los valores de 17.35 y −15.89 que aparecen en la tabla son, por lo tanto, espurios. El apartado 3.8 presenta el cálculo correcto realizado con `statsmodels`, donde esos mismos coeficientes resultan no significativos.

### 3.6 Relación individual entre predictores y variable objetivo

![Diagramas de dispersión de cada predictor frente al NO2](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/05_dispersion_predictores_melisa.png)

**Figura 12.** Diagramas de dispersión de los seis predictores frente a `NO2_Max`, organizados con `gridspec.GridSpec()`.

**Interpretación panel por panel.** El gráfico de `Year` muestra dos columnas verticales, una por cada año, de altura prácticamente idéntica, lo que descarta cualquier tendencia entre 2022 y 2023.

El de `Month` presenta doce columnas y aporta el dato más interesante de todo el panel. Se aprecia una ligera reducción de los valores máximos en los meses centrales del año, que corresponden al verano boreal, junto con una mayor dispersión hacia arriba en los meses fríos. Esto sugiere que existe una estacionalidad débil pero real, atribuible a las inversiones térmicas del invierno y a la mayor demanda de calefacción. El problema es que esa relación no es monótona, ya que los valores son altos en ambos extremos del año y bajos en el centro, y un término lineal simple no puede representar esa forma.

El de `Day` muestra treinta y una columnas homogéneas, de manera que el día del mes resulta completamente irrelevante, tal como cabía esperar.

El de `DayOfWeek` presenta siete columnas sin diferencias notables. Llama la atención que no aparezca el descenso de fin de semana que suele observarse en zonas con tráfico vehicular intenso, aunque esto resulta coherente con el carácter rural del emplazamiento.

Los dos últimos paneles, correspondientes a `Obs_Count` y `Percent_Complete`, muestran la enorme mayoría de los puntos agolpados en el extremo derecho, con unos pocos casos aislados a la izquierda. Una distribución tan desbalanceada hace que la pendiente estimada dependa de un número muy reducido de observaciones, lo cual la vuelve inestable.

### 3.7 Evaluación del modelo y verificación de supuestos

![Dispersión de NO2 real frente a NO2 predicho](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/06_real_vs_predicho_melisa.png)

**Figura 13.** Valores reales de NO₂ frente a los valores predichos por el modelo lineal, sobre el conjunto de prueba.

**Interpretación.** El criterio de calidad para este gráfico es que los puntos se alineen sobre una diagonal de 45 grados, que es donde el valor predicho coincide con el real. Lo que se observa, en cambio, es una nube horizontal. Mientras los valores reales se extienden de 0 a 35 ppb, las predicciones se comprimen en una franja estrecha alrededor de los 10 ppb, muy cerca de la media de la variable.

Este comportamiento tiene una explicación estadística precisa. Cuando los predictores no aportan información útil, la solución de mínimos cuadrados tiende a converger hacia la media, porque en ausencia de información adicional la media es el valor que minimiza el error cuadrático. Dicho de otro modo, el modelo no está prediciendo: está devolviendo el promedio disfrazado de predicción.

![Histograma de residuos con curva de densidad](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/07_histograma_residuos_melisa.png)

**Figura 14.** Distribución de los residuos del modelo, calculados como la diferencia entre `Y_test` y las predicciones.

**Interpretación.** Los residuos se centran aproximadamente en cero, tal como debe ocurrir, ya que en mínimos cuadrados la suma de residuos es nula por construcción. La forma general tiene un solo pico, aunque presenta un sesgo hacia la derecha con una cola más extendida, heredado de la asimetría de la variable original. El supuesto de normalidad se cumple, entonces, solo de manera aproximada.

Vale aclarar que en muestras grandes como esta, con 219 observaciones de prueba, el teorema del límite central amortigua el impacto de las desviaciones moderadas de la normalidad sobre la validez de las pruebas. La normalidad afecta sobre todo a los intervalos de confianza, no a la insesgadez de los estimadores.

![Residuos frente a valores predichos](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/08_residuos_vs_predichos_melisa.png)

**Figura 15.** Residuos del modelo frente a los valores predichos.

**Interpretación.** Lo deseable en este gráfico es una nube de puntos sin estructura aparente, repartida con amplitud constante alrededor de la línea horizontal del cero. Lo que aparece, sin embargo, es una franja vertical estrecha: los valores predichos ocupan un intervalo muy reducido sobre el eje horizontal, mientras que los residuos se dispersan ampliamente sobre el vertical.

Esta configuración no indica heterocedasticidad en sentido estricto, porque la varianza del error no crece de forma sistemática a medida que aumenta la predicción. Lo que revela es algo más de fondo, y es que la varianza de los residuos resulta prácticamente igual a la varianza total de la variable objetivo. El modelo no consiguió separar la variabilidad total en una parte explicada y otra residual, de manera que toda ella quedó del lado de los residuos.

### 3.8 Validación estadística formal

<!-- ESPACIO PARA IMAGEN -->

**Figura 16.** Salida completa de `sm.OLS().fit().summary()`, con los indicadores de ajuste, los coeficientes y sus p-valores.

**Interpretación del coeficiente de determinación.** El R² obtenido es de 0.004, lo que significa que el modelo explica el 0.4 % de la variabilidad del NO₂ y deja sin explicar el 99.6 % restante. Este es el indicador más contundente del fracaso predictivo del modelo.

**Interpretación del R² ajustado.** Su valor de −0.004 tiene un significado muy concreto. Esta versión del coeficiente penaliza la inclusión de predictores que no aportan capacidad explicativa, y que resulte negativo indica que el modelo con seis variables ajusta peor que uno trivial que se limitara a predecir siempre la media. Las seis variables no solo son inútiles, sino que además agregan ruido.

**Interpretación de la prueba F.** El estadístico F vale 0.5100 y su p-valor asociado es de 0.801. Esta prueba contrasta la hipótesis de que todos los coeficientes son simultáneamente cero, y como 0.801 supera ampliamente el nivel de significancia de 0.05, no se rechaza la hipótesis nula. Dicho en términos probabilísticos, si en la población no existiera ninguna relación entre estos predictores y el NO₂, habría un 80.1 % de probabilidad de observar por puro azar un ajuste igual o mejor que el obtenido.

**Interpretación de los p-valores individuales.** Los seis predictores presentan p-valores que van de 0.390 a 0.931, todos muy por encima del umbral de 0.05. Ninguna variable resulta estadísticamente significativa por sí sola.

**Interpretación de los intervalos de confianza.** Todos ellos contienen el valor cero. El de `Obs_Count`, por ejemplo, va de −9.044 a 23.141, de modo que el rango de valores plausibles para el efecto real de esa variable incluye tanto efectos negativos como positivos considerables. Esa amplitud es consecuencia directa de la multicolinealidad, que infla los errores estándar hasta valores como el 8.197 de `Obs_Count`, superior al propio coeficiente.

**Criterios de información.** El AIC alcanza 4785 y el BIC 4817. Estos valores no dicen mucho por sí solos, pero sirven como referencia para comparar modelos alternativos que se construyan sobre el mismo conjunto de datos, donde los valores menores indican un mejor equilibrio entre ajuste y simplicidad.

### 3.9 Modelo de contraste: árbol de decisión

![Dispersión real frente a predicho del árbol de decisión](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/09_arbol_real_vs_predicho_melisa.png)

**Figura 17.** Valores reales de NO₂ frente a los predichos por el árbol de decisión con profundidad máxima de cinco niveles.

**Interpretación.** El error cuadrático medio del árbol es de 31.474, cuya raíz cuadrada da un RMSE cercano a los 5.61 ppb. Para valorar esa cifra hay que compararla con la desviación estándar de la variable objetivo, que es de 6.37 ppb y equivale al error que cometería un modelo nulo que siempre predijera la media. La mejora, por lo tanto, ronda el 12 %: es modesta, aunque supera claramente lo logrado por el modelo lineal.

En el plano visual, la dispersión muestra más variabilidad vertical que la Figura 13, lo que significa que el árbol sí produce predicciones diferenciadas en lugar de concentrarlas todas alrededor de la media. Aun así, la alineación con la diagonal sigue siendo pobre.



**Figura 18.** Comando `tree_model.feature_importances_` y su salida, con la importancia relativa de cada predictor.

![Importancia relativa de las características](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/10_importancia_caracteristicas_melisa.png)

**Figura 19.** Representación gráfica de la importancia relativa de los predictores, generada con `plt.barh()`.

| Variable | Importancia | Porcentaje |
|---|---|---|
| `Year` | 0.0345 | 3.45 % |
| `Month` | 0.6827 | 68.27 % |
| `Day` | 0.2035 | 20.35 % |
| `DayOfWeek` | 0.0506 | 5.06 % |
| `Obs_Count` | 0.0101 | 1.01 % |
| `Percent_Complete` | 0.0186 | 1.86 % |

**Interpretación.** Este resultado es, probablemente, el hallazgo más informativo de todo el trabajo. El árbol asigna casi el 70 % de la importancia a la variable `Month`, que es justamente la que en el modelo lineal tenía el coeficiente más insignificante, con un valor de 0.0149 y un p-valor de 0.897.

La contradicción es solo aparente, y al resolverla se entiende el problema de fondo. La relación entre el mes y la concentración de NO₂ sí existe, pero no es lineal. El ciclo estacional del contaminante tiene una forma aproximadamente sinusoidal, con valores altos en invierno, bajos en verano y altos otra vez al cerrar el año. Un coeficiente lineal único no puede representar ese recorrido, porque al promediar una pendiente ascendente en la primera mitad del año con una descendente en la segunda, el resultado neto tiende a cero. El árbol de decisión, en cambio, puede cortar el año en tramos y asignar una predicción distinta a cada uno, y por eso logra capturar el patrón.

De manera complementaria, la escasa importancia que el árbol otorga a `Obs_Count` y `Percent_Complete`, que apenas suman el 2.87 % entre las dos, confirma que la relevancia que parecían tener en el modelo lineal era un artefacto de la colinealidad y no un efecto real.

---

## 4. Discusión

### 4.1 Sobre la efectividad del modelo de regresión lineal

La evidencia reunida conduce a una conclusión inequívoca: el modelo de regresión lineal múltiple no resultó efectivo para predecir la concentración máxima diaria de NO₂ en Montana durante 2022 y 2023. Cinco pruebas independientes apuntan en la misma dirección.

- Las correlaciones de Pearson entre todos los predictores y la variable objetivo quedan por debajo de 0.05 en valor absoluto.
- El R² de 0.004 indica que el modelo explica menos del medio por ciento de la variabilidad.
- El R² ajustado negativo revela que el modelo rinde peor que una predicción basada simplemente en la media.
- La prueba F global no alcanza significancia, con un p-valor de 0.801, de modo que no se rechaza la hipótesis nula.
- Ningún coeficiente individual resulta significativo, y todos los intervalos de confianza incluyen el cero.

Ahora bien, conviene enmarcar correctamente este resultado. Un modelo que no logra predecir no equivale a un análisis fallido. Determinar que un conjunto de variables no explica un fenómeno es un resultado científico legítimo, y en este caso se sostiene sobre un procedimiento metodológicamente correcto: los datos se limpiaron de forma adecuada, la partición fue apropiada, los supuestos se verificaron uno por uno y la validación se realizó mediante inferencia formal. El valor del trabajo reside precisamente en haber demostrado la ausencia de relación con rigor y en haber identificado las razones que la explican.

### 4.2 Causas del bajo poder predictivo

**Faltan las variables que realmente importan.** Esta es la causa principal. Las concentraciones de NO₂ dependen de dos grupos de factores. Por un lado están las emisiones, que responden a la densidad del tráfico, a la actividad industrial y al consumo de combustibles. Por otro lado está la dispersión atmosférica, gobernada por la velocidad y dirección del viento, la temperatura, la altura de la capa de mezcla, la estabilidad atmosférica, la radiación solar y la precipitación. El conjunto de datos no contiene ninguna de estas variables. Lo que se utilizó como predictores fueron etiquetas temporales y metadatos sobre la calidad del muestreo, que en el mejor de los casos solo podrían funcionar como aproximaciones muy indirectas de los procesos reales.

**La multicolinealidad distorsionó los coeficientes.** La correlación de 0.9998 entre `Obs_Count` y `Percent_Complete` refleja una dependencia funcional entre ambas. Cuando dos columnas de la matriz de diseño son casi linealmente dependientes, esa matriz se acerca a la singularidad y su inversa arroja valores muy grandes, lo que infla los errores estándar de los coeficientes [15], [16]. En este trabajo las consecuencias se vieron con claridad: coeficientes de signos opuestos para variables positivamente correlacionadas, errores estándar desmesurados e intervalos de confianza tan amplios que resultan inutilizables.

**La única relación existente no es lineal.** Como mostró el análisis de importancias del árbol, la variable `Month` sí contiene información predictiva, y de hecho concentra cerca del 70 % de la que el modelo no lineal logra aprovechar. El inconveniente es que esa información tiene forma cíclica, y la regresión lineal, por su propia especificación funcional, no puede capturar patrones periódicos a menos que se transforme la variable previamente.

**Se usaron variables que describen el instrumento, no el fenómeno.** Incluir `Obs_Count` y `Percent_Complete` resulta cuestionable desde el punto de vista conceptual, porque ambas informan sobre el funcionamiento del equipo de medición y no sobre la atmósfera. Cualquier asociación que mostraran con el NO₂ sería, en el mejor de los casos, espuria.

**El fenómeno tiene un componente aleatorio irreducible.** Incluso contando con un conjunto completo de variables meteorológicas, la concentración diaria de contaminantes conserva un margen de aleatoriedad considerable. Ningún modelo determinista puede aspirar a explicar la totalidad de la varianza.

### 4.3 Sobre el cumplimiento de los supuestos

El examen de los supuestos arrojó un panorama mixto. La linealidad no se cumple justamente para `Month`, que es la variable con mayor contenido informativo. La normalidad de los residuos se satisface de manera aproximada, con un sesgo hacia la derecha heredado de la distribución original. La homocedasticidad no presenta violaciones claras, aunque el diagnóstico queda limitado por lo estrecho que resultó el rango de valores predichos.

La independencia, en cambio, no llegó a verificarse, y esto constituye una limitación relevante. Al tratarse de una serie temporal diaria, resulta bastante plausible que los residuos presenten autocorrelación, es decir, que el error de un día guarde relación con el del día anterior. Evaluarlo habría requerido calcular el estadístico de Durbin-Watson, algo que queda pendiente para una futura versión del análisis.

### 4.4 Interpretación estadística y probabilística

Desde la perspectiva de la inferencia estadística, el resultado central es que no se rechaza la hipótesis nula. El p-valor de 0.801 asociado al estadístico F debe leerse como una probabilidad condicional: bajo el supuesto de que H₀ sea verdadera, es decir, de que no exista ninguna relación lineal en la población, la probabilidad de obtener por azar muestral un ajuste igual o superior al observado sería del 80.1 %. Con una probabilidad tan alta de que el resultado provenga simplemente del azar, no queda base alguna para afirmar que exista una relación.

Aquí conviene hacer una precisión que suele pasarse por alto. No rechazar H₀ no demuestra que H₀ sea verdadera. Lo correcto es decir que los datos disponibles no ofrecen evidencia suficiente para rechazarla. Con otras variables, o con una especificación funcional distinta, el resultado podría perfectamente ser otro.

Desde la teoría de la probabilidad, por su parte, la distribución empírica del NO₂ resulta reveladora. Que sea unimodal, sesgada a la derecha y acotada inferiormente en cero sugiere que un modelo log-normal o gamma describiría mejor el proceso que genera estos datos que la distribución normal implícita en la regresión lineal ordinaria. Esta observación abre la puerta a los modelos lineales generalizados como alternativa metodológica.

### 4.5 Interpretación ambiental de los resultados

Más allá del desempeño del modelo, los datos ofrecen información ambiental que vale la pena destacar. La concentración media de 10.47 ppb y el máximo de 35 ppb se sitúan muy por debajo del estándar de 100 ppb que fija la EPA, de manera que la zona analizada mantuvo una calidad del aire buena durante la totalidad del período.

Tampoco se aprecia diferencia entre 2022 y 2023, ya que el coeficiente anual es de −0.31 ppb con un p-valor de 0.514. Esto habla de estabilidad interanual, sin tendencias de deterioro ni de mejora detectables en una ventana temporal de dos años.

Resulta llamativa, por último, la ausencia de un efecto de día de la semana. En entornos urbanos suele observarse un descenso durante los fines de semana, asociado a la caída del tráfico laboral, y que aquí no aparezca resulta coherente con el carácter rural del emplazamiento.

### 4.6 Limitaciones del estudio

- Los datos provienen de una sola estación de monitoreo, por lo que los resultados no pueden generalizarse a todo el estado.
- El horizonte de dos años resulta insuficiente para analizar tendencias de largo plazo.
- No se dispuso de variables meteorológicas, que es la principal deficiencia del conjunto de datos.
- No se evaluó la autocorrelación temporal de los residuos.
- No se aplicaron transformaciones a la variable objetivo que pudieran corregir su asimetría.
- No se calcularon las métricas MAE, MSE y RMSE del modelo lineal sobre el conjunto de prueba, lo que habría permitido una comparación numérica directa con el árbol de decisión.

### 4.7 Recomendaciones para trabajos futuros

1. **Incorporar variables meteorológicas** como temperatura, velocidad y dirección del viento, humedad relativa, presión y precipitación, obtenibles de bases como NOAA o Meteostat. Es, con diferencia, la mejora con mayor impacto potencial.
2. **Codificar la estacionalidad de forma adecuada**, mediante transformaciones trigonométricas del tipo seno y coseno del mes, que preservan la naturaleza cíclica del calendario, o bien mediante variables dicotómicas por estación del año.
3. **Eliminar la redundancia** conservando solo una de las dos variables de cobertura, o directamente excluyendo ambas por no ser predictores del fenómeno.
4. **Aplicar una transformación logarítmica** a la variable objetivo para acercar su distribución a la normal.
5. **Explorar modelos alternativos** como Random Forest, Gradient Boosting o modelos de series temporales del tipo SARIMA, que modelan explícitamente la estacionalidad y la autocorrelación.
6. **Incorporar rezagos temporales** de la propia variable, dado que la concentración de un día guarda relación con la del día anterior.
7. **Ampliar el análisis a varias estaciones** de Montana, para incorporar la variabilidad espacial.
8. **Emplear validación cruzada** en lugar de una única partición, de modo que las estimaciones del error resulten más estables.

---

## 5. Conclusiones

- Se analizaron 730 registros diarios de concentración máxima horaria de NO₂ correspondientes a Montana durante los años 2022 y 2023. El conjunto resultó completo, sin valores faltantes en las variables de interés.

- La concentración de NO₂ presentó una media de 10.47 ppb, una mediana de 9.00 ppb, una desviación estándar de 6.37 ppb y un rango que va de 0 a 35 ppb. Su distribución es unimodal y sesgada hacia la derecha, comportamiento habitual en los contaminantes atmosféricos.

- Todos los valores registrados se mantuvieron muy por debajo del estándar nacional de calidad del aire de 100 ppb, de modo que el área puede caracterizarse como de calidad del aire buena durante todo el período.

- El modelo de regresión lineal múltiple no resultó efectivo. Su coeficiente de determinación de 0.004 indica que explica apenas el 0.4 % de la variabilidad del NO₂, y el R² ajustado negativo revela que rinde peor que una predicción basada en la media.

- La prueba F global no alcanzó significancia estadística, con un valor de 0.51 y un p-valor de 0.801, por lo que no se rechaza la hipótesis nula. Ningún coeficiente individual resultó significativo al nivel de 0.05, y todos los intervalos de confianza al 95 % incluyeron el cero.

- Se detectó multicolinealidad severa entre las variables `Obs_Count` y `Percent_Complete`, con una correlación de 0.9998 producto de una dependencia funcional entre ambas. Este problema explica la inestabilidad de los coeficientes, la inversión de sus signos y la magnitud desmesurada de los errores estándar.

- El árbol de decisión, con un RMSE de 5.61 ppb frente a una desviación estándar de 6.37 ppb, superó ligeramente al modelo lineal y atribuyó el 68.3 % de la importancia predictiva a la variable `Month`. Esto demuestra que sí existe una señal estacional en los datos, aunque de naturaleza no lineal y por lo tanto inaccesible para una especificación lineal simple.

- La causa de fondo del bajo poder predictivo es la ausencia, en el conjunto de datos, de las variables meteorológicas y de emisión que gobiernan físicamente la concentración de NO₂ en la atmósfera.

- El resultado negativo constituye un hallazgo válido y metodológicamente sólido. La verificación de supuestos, la validación mediante inferencia formal y la comparación con un modelo de contraste permitieron no solo constatar la ausencia de relación lineal, sino también explicar sus causas y trazar una ruta concreta de mejora para trabajos posteriores.

---

## 6. Referencias bibliográficas

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

## Anexo A. Resultados numéricos consolidados

| Indicador | Valor | De dónde sale |
|---|---|---|
| Registros totales | 730 | `df.info()` |
| Registros de entrenamiento | 511 | 70 % de la partición |
| Registros de prueba | 219 | `predictions.shape` |
| Predictores | 6 | `X.shape[1]` |
| Grados de libertad residuales | 723 | `summary()` |
| Media de NO₂ | 10.47 ppb | `df.describe()` |
| Mediana de NO₂ | 9.00 ppb | `df.describe()` |
| Desviación estándar de NO₂ | 6.37 ppb | `df.describe()` |
| Mínimo y máximo de NO₂ | 0.00 y 35.00 ppb | `df.describe()` |
| Rango intercuartílico | 8.00 ppb | 14.00 − 6.00 |
| Coeficiente de variación | ≈ 61 % | 6.37 / 10.47 |
| Correlación máxima con NO₂ | 0.0439 (`Obs_Count`) | `.corr()` |
| Correlación entre variables de cobertura | 0.9998 | `.corr()` |
| Intercepto del modelo lineal | 1566.83 | `lm.intercept_` |
| R² | 0.004 | `summary()` |
| R² ajustado | −0.004 | `summary()` |
| Estadístico F | 0.5100 | `summary()` |
| p-valor de la prueba F | 0.801 | `summary()` |
| AIC y BIC | 4785 y 4817 | `summary()` |
| MSE del árbol de decisión | 31.474 | `mean_squared_error()` |
| RMSE del árbol de decisión | ≈ 5.61 ppb | √31.474 |
| Importancia de `Month` en el árbol | 68.27 % | `feature_importances_` |

## Anexo B. Contraste entre los dos modelos

| Criterio | Regresión lineal múltiple | Árbol de decisión |
|---|---|---|
| Tipo de modelo | Paramétrico | No paramétrico |
| Relaciones que captura | Solo lineales | Lineales y no lineales |
| Variable más influyente | `Obs_Count`, por artefacto de colinealidad | `Month`, con el 68.27 % |
| Medida de ajuste | R² = 0.004 | RMSE ≈ 5.61 ppb |
| Comparación con el modelo nulo | Inferior, R² ajustado negativo | Superior en torno al 12 % |
| Significancia estadística | No significativo, p = 0.801 | No aplica |
| Interpretabilidad de los coeficientes | Nula por multicolinealidad | Importancias interpretables |
| Sensibilidad a la multicolinealidad | Alta | Baja |
| Conclusión | No efectivo | Marginalmente superior |

## Anexo C. Contraste de hipótesis

| Elemento | Formulación |
|---|---|
| Hipótesis nula (H₀) | β₁ = β₂ = β₃ = β₄ = β₅ = β₆ = 0 |
| Hipótesis alternativa (H₁) | Al menos un βᵢ ≠ 0 |
| Estadístico de prueba | F de Fisher-Snedecor |
| Valor calculado | F = 0.5100 |
| p-valor | 0.801 |
| Nivel de significancia | α = 0.05 |
| Regla de decisión | Rechazar H₀ si el p-valor es menor que α |
| Decisión | 0.801 > 0.05, por lo que no se rechaza H₀ |
| Conclusión | No hay evidencia estadística de relación lineal entre los predictores y el NO₂ |

---
