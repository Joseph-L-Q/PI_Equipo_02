# Taller 3: Introducción a la IA — Predicción del índice de calidad del aire

---

## 1. Introducción y planteamiento del problema

En este trabajo se aplicaron dos modelos de aprendizaje automático supervisado para predecir el valor diario del índice de calidad del aire (**AQI**) a partir de mediciones de monóxido de carbono y otros datos de la estación de monitoreo.

El archivo `ad_viz_plotval_data 2023.csv` contiene registros diarios correspondientes al año 2023. Los datos provienen del sistema **AQS** y pertenecen al sitio de monitoreo **GARDEN/TRINITY CHRISTIAN CHURCH**, ubicado en Anchorage, Alaska.

- **Cantidad de registros:** 358.
- **Cantidad de columnas:** 21.
- **Periodo registrado:** del 1 de enero al 31 de diciembre de 2023.
- **Contaminante evaluado:** monóxido de carbono (CO).
- **Variable objetivo:** `Daily AQI Value`.
- **Modelos utilizados:** Regresión Lineal Múltiple y Árbol de Decisión para Regresión.

El objetivo fue analizar qué variables se relacionan con el AQI diario y comparar el rendimiento de ambos modelos mediante las métricas $MSE$, $MAE$ y $R^2$.

---

## 2. Análisis exploratorio de los datos

### 2.1 Carga y revisión del conjunto de datos

Primero se cargó el archivo CSV mediante la biblioteca `pandas`. Después se revisaron las primeras filas, las dimensiones y los tipos de datos. El conjunto contiene **358 observaciones y 21 columnas**, sin valores nulos ni filas duplicadas.

Entre las columnas disponibles se encuentran la fecha, la concentración máxima diaria de CO durante ocho horas, el valor AQI, la cantidad de observaciones, el porcentaje de datos completos, el nombre del sitio y sus coordenadas geográficas.

Las variables numéricas seleccionadas para construir los modelos fueron:

| Variable | Función dentro del modelo |
|---|---|
| `Daily Max 8-hour CO Concentration` | Concentración máxima diaria de CO en un periodo de ocho horas, medida en ppm. |
| `Site Latitude` | Latitud de la estación de monitoreo. |
| `Site Longitude` | Longitud de la estación de monitoreo. |
| `Daily Obs Count` | Cantidad de observaciones realizadas durante el día. |
| `Daily AQI Value` | Variable objetivo que se desea predecir. |

### 2.2 Estadísticas principales

| Variable | Media | Mínimo | Mediana | Máximo |
|---|---:|---:|---:|---:|
| Concentración máxima de CO (ppm) | 0.5444 | 0.20 | 0.40 | 2.60 |
| AQI diario | 6.1229 | 2 | 5 | 30 |
| Observaciones diarias | 22.9302 | 2 | 24 | 24 |
| Porcentaje completo | 95.5587 % | 8 % | 100 % | 100 % |

La mayor parte de los días presenta concentraciones bajas de CO y valores AQI reducidos. Sin embargo, también existen algunos días con concentraciones más elevadas que alcanzan hasta **2.6 ppm** y un AQI máximo de **30**.

### 2.3 Distribución de las variables

La matriz de dispersión permitió observar las relaciones entre las principales variables numéricas. La relación más clara aparece entre la concentración máxima de CO y el AQI diario.

![Matriz de dispersión de las variables](./imagenes_tarea_PI_3_1/01_matriz_dispersion.png)

*Figura 1. Matriz de dispersión de las variables numéricas seleccionadas.*

El histograma muestra que la mayoría de los valores AQI se concentra en la parte baja de la distribución. Esto indica que durante gran parte del año la calidad del aire presentó niveles bajos de contaminación por monóxido de carbono.

![Histograma del AQI diario](./imagenes_tarea_PI_3_1/02_histograma_aqi.png)

*Figura 2. Distribución del valor AQI diario mediante 25 intervalos.*

El gráfico de densidad confirma que la mayor concentración de datos se encuentra alrededor de los valores AQI más bajos y que la distribución se extiende hacia la derecha por la presencia de algunos registros mayores.

![Densidad del AQI diario](./imagenes_tarea_PI_3_1/03_densidad_aqi.png)

*Figura 3. Curva de densidad del AQI diario.*

### 2.4 Correlación entre variables

El mapa de calor permitió medir la relación lineal entre las variables numéricas.

![Mapa de calor de correlaciones](./imagenes_tarea_PI_3_1/04_mapa_correlacion.png)

*Figura 4. Mapa de calor con los coeficientes de correlación.*

Los resultados más importantes fueron los siguientes:

- La concentración máxima de CO tiene una correlación de **0.9980** con el AQI diario. Esta relación positiva es casi perfecta, por lo que constituye la principal variable predictora.
- `Daily Obs Count` presenta una correlación de solo **0.0785** con el AQI, lo cual indica una relación lineal muy débil.
- La latitud y la longitud permanecen constantes porque todos los registros pertenecen al mismo sitio. Por este motivo, su correlación no se puede calcular y aparecen valores `NaN`.

Los gráficos individuales también muestran que el AQI aumenta casi de forma lineal cuando se incrementa la concentración de CO. En cambio, las otras variables no presentan una tendencia clara.

![Relación entre las variables y el AQI](./imagenes_tarea_PI_3_1/05_relacion_variables_aqi.png)

*Figura 5. Relación de cada variable predictora con el AQI diario.*

---

## 3. Preparación de los datos

Para entrenar los modelos se definió la matriz de entrada $X$ con cuatro variables predictoras y el vector $Y$ con el AQI diario:

$$
X = \{\text{CO},\text{Latitud},\text{Longitud},\text{Cantidad de observaciones}\}
$$

$$
Y = \text{AQI diario}
$$

Los datos se dividieron de la siguiente manera:

- **70 % para entrenamiento:** 250 registros.
- **30 % para prueba:** 108 registros.
- **Semilla utilizada:** `random_state=123`.

Esta división permite entrenar los modelos con una parte de los datos y después evaluar su comportamiento con observaciones que no fueron utilizadas durante el aprendizaje.

---

## 4. Regresión Lineal Múltiple

### 4.1 Construcción del modelo

La Regresión Lineal Múltiple busca representar el AQI mediante una combinación lineal de las variables predictoras:

$$
\widehat{AQI}=\beta_0+\beta_1(\text{CO})+\beta_2(\text{Latitud})+\beta_3(\text{Longitud})+\beta_4(\text{Observaciones})
$$

Los coeficientes obtenidos durante el entrenamiento fueron:

| Parámetro | Coeficiente aproximado |
|---|---:|
| Intersección | -0.2969 |
| Concentración máxima de CO | 11.6190 |
| Latitud | 0.0000 |
| Longitud | ≈ 0.0000 |
| Cantidad de observaciones | 0.0035 |

La ecuación aproximada del modelo puede escribirse como:

$$
\widehat{AQI}=-0.2969+11.6190(\text{CO})+0.0035(\text{Observaciones})
$$

La latitud y la longitud no aparecen de manera útil en la ecuación porque no cambian entre los registros.

### 4.2 Interpretación de los coeficientes

- **Concentración máxima de CO:** Si las demás variables permanecen constantes, un aumento de 1 ppm se relaciona con un incremento aproximado de **11.62 unidades de AQI**.
- **Cantidad de observaciones:** Su coeficiente es pequeño y su estadístico t es aproximadamente **0.63**, por lo que su aporte al modelo es reducido.
- **Latitud y longitud:** No ofrecen información para comparar registros debido a que todos provienen de la misma estación.

El análisis OLS obtuvo un $R^2=0.996$, pero también generó una advertencia de matriz singular. Esta advertencia se debe a la inclusión de la latitud y longitud constantes. Por ello, esos coeficientes no deben interpretarse como efectos geográficos reales.

### 4.3 Predicciones y métricas

![Valores reales y predichos con regresión lineal](./imagenes_tarea_PI_3_1/06_aqi_real_predicho_lineal.png)

*Figura 6. Comparación del AQI real y el AQI estimado mediante Regresión Lineal.*

Los puntos se encuentran muy cerca de la línea de referencia, lo que indica que el modelo reproduce correctamente la mayoría de los valores reales.

| Métrica | Resultado |
|---|---:|
| $MSE$ | 0.1036 |
| $MAE$ | 0.2747 |
| $R^2$ | 0.9964 |

El valor $R^2=0.9964$ significa que el modelo explica aproximadamente el **99.64 % de la variación del AQI** en el conjunto de prueba.

### 4.4 Análisis de residuos

Los residuos representan la diferencia entre el valor real y el valor estimado:

$$
e_i=Y_i-\widehat{Y}_i
$$

![Histograma de los residuos](./imagenes_tarea_PI_3_1/07_histograma_residuos.png)

*Figura 7. Histograma de residuos con curva de densidad.*

El histograma permite revisar si los errores se concentran cerca de cero. No obstante, el resumen OLS reportó asimetría positiva y una prueba de Jarque-Bera con $p<0.05$, por lo que la normalidad de los residuos no se cumple de manera perfecta.

![Residuos frente a valores predichos](./imagenes_tarea_PI_3_1/08_homocedasticidad.png)

*Figura 8. Residuos frente a las predicciones para revisar la homocedasticidad.*

El gráfico permite verificar si la dispersión de los errores se mantiene estable. La mayoría de los residuos se encuentra cerca de cero, aunque la distribución discreta del AQI produce agrupaciones visibles.

---

## 5. Árbol de Decisión para Regresión

### 5.1 Construcción del modelo

El segundo modelo utilizado fue un Árbol de Decisión para Regresión con los siguientes parámetros:

```python
tree.DecisionTreeRegressor(max_depth=5, random_state=10)
```

La profundidad máxima se limitó a cinco niveles para reducir el riesgo de sobreajuste. El árbol divide los datos en grupos y asigna una predicción de acuerdo con las condiciones aprendidas.

![Valores reales y predichos con el árbol](./imagenes_tarea_PI_3_1/09_aqi_real_predicho_arbol.png)

*Figura 9. Comparación entre el AQI real y el estimado por el Árbol de Decisión.*

### 5.2 Métricas del árbol

| Métrica | Resultado |
|---|---:|
| $MSE$ | 0.6019 |
| $MAE$ | 0.1019 |
| $R^2$ | 0.9792 |

El árbol presenta un $R^2$ elevado y predice exactamente muchos registros. Su $MAE$ es menor que el de la regresión, pero su $MSE$ es mayor. Esto indica que normalmente comete errores muy pequeños, aunque en unos pocos casos genera errores más grandes que son penalizados por el $MSE$.

### 5.3 Importancia de las variables

![Importancia de las variables](./imagenes_tarea_PI_3_1/10_importancia_variables.png)

*Figura 10. Importancia relativa de las características empleadas por el árbol.*

El resultado de importancia fue:

| Variable | Importancia |
|---|---:|
| Concentración máxima de CO | 1.0000 |
| Latitud | 0.0000 |
| Longitud | 0.0000 |
| Cantidad de observaciones | 0.0000 |

El árbol tomó todas sus decisiones a partir de la concentración de CO. Esto coincide con el análisis de correlación y confirma que las demás variables no aportan información adicional relevante en este conjunto de datos.

---

## 6. Comparación de los modelos

| Modelo | $MSE$ | $MAE$ | $R^2$ | Interpretación |
|---|---:|---:|---:|---|
| **Regresión Lineal** | **0.1036** | 0.2747 | **0.9964** | Logra el mejor ajuste general y presenta menos errores grandes. |
| **Árbol de Decisión** | 0.6019 | **0.1019** | 0.9792 | Tiene el menor error absoluto promedio, pero comete algunos errores más grandes. |

La Regresión Lineal alcanza un $R^2$ mayor y un $MSE$ menor, por lo que representa mejor la relación general entre la concentración de CO y el AQI. El Árbol de Decisión obtiene un $MAE$ menor porque acierta exactamente en muchos valores discretos del AQI, aunque falla con mayor intensidad en algunos casos.

En este conjunto de datos, la **Regresión Lineal es la opción más equilibrada** debido a su precisión global, su facilidad de interpretación y su menor sensibilidad a errores grandes. Sin embargo, el árbol también presenta un desempeño alto y puede ser útil si se desea trabajar con reglas y rangos de decisión.

---

## 7. Aspectos importantes y aprendizajes

Uno de los aspectos que me pareció más interesante fue observar que una sola variable puede explicar casi todo el comportamiento del resultado. En este caso, la concentración máxima de monóxido de carbono presentó una relación muy fuerte con el AQI diario, mientras que las demás variables aportaron muy poca información.

También aprendí que no todas las columnas numéricas deben incluirse automáticamente en un modelo. Aunque la latitud y longitud son números, permanecen constantes porque las mediciones se realizaron en un solo lugar. Esto ocasionó divisiones entre cero en el cálculo manual del error estándar y una advertencia de matriz singular en el modelo OLS.

La comparación de métricas permitió comprender que no siempre un modelo gana en todos los indicadores. La regresión obtuvo mejores resultados en $MSE$ y $R^2$, mientras que el árbol consiguió un $MAE$ menor. Por eso es necesario analizar varias métricas antes de elegir un modelo.

---

## 8. Conclusiones

El análisis mostró que la concentración máxima diaria de CO durante ocho horas es la variable que determina principalmente el valor AQI en este conjunto de datos. Su correlación de **0.9980** y su importancia de **100 %** dentro del árbol confirman esta relación.

La Regresión Lineal obtuvo un $R^2$ de **0.9964**, mientras que el Árbol de Decisión alcanzó **0.9792**. Ambos modelos presentan un buen rendimiento, pero la regresión ofrece un ajuste general más preciso y una ecuación fácil de interpretar.

Como mejora futura, sería recomendable retirar la latitud y longitud del modelo mientras se trabaje con una sola estación. Si posteriormente se incorporan datos de distintos lugares, estas variables sí podrían ser útiles para estudiar diferencias geográficas en la calidad del aire.

---

## 9. Archivos utilizados

- [`tarea_PI_3_1_JL.ipynb`](./tarea_PI_3_1_JL.ipynb)
- [`ad_viz_plotval_data 2023.csv`](./ad_viz_plotval_data%202023.csv)

El notebook contiene el análisis exploratorio, los gráficos, la preparación de los datos, el entrenamiento de los modelos y la evaluación de los resultados.
