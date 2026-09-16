# Taller 3: Introducción a la IA — Regresión lineal y árboles de decisión

---

## 1. Introducción y planteamiento del problema

En este taller se implementaron y analizaron dos modelos de aprendizaje supervisado con el propósito de estimar el consumo de energía en un entorno industrial u operativo.

- **Descripción del conjunto de datos:** El archivo `Data_PI_regresion.csv` contiene **5,000 registros numéricos** obtenidos a partir de sensores ambientales y operativos. Se trabajó con cuatro variables de entrada: **Temperatura** (°C), **Horas de Operación** (h), **Carga** (%) y **Humedad** (%). A partir de ellas se busca predecir el **Consumo de Energía** (kWh), que corresponde a la variable objetivo.
- **Problema identificado:** Un consumo eléctrico ineficiente puede incrementar los costos de operación y acelerar el desgaste de los equipos. Sin una herramienta predictiva resulta difícil anticipar aumentos de consumo o estimar la demanda de acuerdo con la carga de trabajo y las condiciones ambientales.
- **Propósito del análisis:** Construir y comparar un modelo de **Regresión Lineal Múltiple** y un **Árbol de Decisión para Regresión**, utilizando las métricas $R^2$, $MSE$ y $MAE$ para determinar cuál realiza predicciones más precisas.

El uso de estos modelos permite aprovechar las mediciones de los sensores para obtener información útil. Así, no solo se observan los registros anteriores, sino que también se pueden anticipar posibles picos de consumo y apoyar la toma de decisiones dentro del proyecto.

---

## 2. Análisis exploratorio de datos

### 2.1 Carga y revisión de la estructura

Antes de entrenar los modelos se revisó el estado general del conjunto de datos. Esta etapa permitió comprobar si existían datos faltantes, registros repetidos o tipos de variables incorrectos que pudieran perjudicar los resultados.

https://github.com/Joseph-L-Q/PI_Equipo_02/blob/0c097c3afedb0f7793e3182da5661214b79f0a3a/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-16%20011416.png

*Figura 1. Lectura del archivo CSV, revisión con `info()` y resumen estadístico mediante `describe()`.*

### Interpretación de la estructura y de las estadísticas

Con `df.info()` se comprobó que el conjunto posee **5,000 observaciones completas y 5 columnas**, sin valores nulos. Todas las variables tienen el tipo `float64`, por lo que se pueden usar directamente en los cálculos numéricos.

- **Temperatura (°C):** Tiene una media de $26.5\,°C$ y sus valores se encuentran entre $18.0\,°C$ y $35.0\,°C$. Este intervalo representa condiciones operativas razonables.
- **Horas de Operación (h):** Varía entre 2 y 12 horas. La media y la mediana son de 7 horas, lo que indica una distribución bastante equilibrada.
- **Carga (%) y Humedad (%):** La carga se encuentra entre 30 % y 100 %, mientras que la humedad está entre 40 % y 90 %. La cercanía entre sus medias y medianas indica que, inicialmente, no se observan sesgos demasiado marcados.
- **Consumo de Energía (kWh):** Presenta un promedio de $26.05\,kWh$ y una desviación estándar de $5.62$. Sus valores van desde $9.12\,kWh$ hasta $42.63\,kWh$.

### 2.2 Relación y correlación entre variables

Después se estudiaron las relaciones entre las variables mediante gráficos de dispersión y la correlación de Pearson. Esto permitió identificar cuáles características se relacionan más con el consumo y verificar si las variables de entrada entregan información diferente entre sí.

https://github.com/Joseph-L-Q/PI_Equipo_02/blob/0c097c3afedb0f7793e3182da5661214b79f0a3a/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-16%20011513.png
https://github.com/Joseph-L-Q/PI_Equipo_02/blob/0c097c3afedb0f7793e3182da5661214b79f0a3a/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-16%20011533.png

*Figura 2. Matriz de dispersión (`pairplot`) y mapa de calor (`heatmap`) con las correlaciones de Pearson.*

### Interpretación y elección de características

- **Variable con mayor relación:** `Horas_Operacion` alcanza una correlación positiva de **$r=0.8434$** con `Consumo_Energia`. En los gráficos también se aprecia una tendencia ascendente definida, por lo que se considera el predictor más importante.
- **Contribución de otras variables:** `Carga` obtiene una correlación moderada de **$r=0.3366$**. Aunque su efecto es menor, sigue aportando información útil, especialmente cuando el equipo trabaja con una carga elevada.
- **Independencia entre predictores:** Las correlaciones entre las variables de entrada son muy cercanas a cero. Por ejemplo, la correlación entre `Horas_Operacion` y `Temperatura` es **$-0.0260$**, y entre `Carga` y `Humedad` es **$0.0060$**. Esto sugiere que no existe un problema importante de multicolinealidad y que cada predictor aporta información distinta.

---

## 3. Construcción y evaluación de los modelos

### 3.1 Regresión lineal múltiple

La Regresión Lineal Múltiple estima el **Consumo de Energía** a partir de una combinación de las cuatro variables ambientales y operativas. Su ecuación general es:

$$Y=\beta_0+\beta_1X_{\text{Temp}}+\beta_2X_{\text{Horas}}+\beta_3X_{\text{Carga}}+\beta_4X_{\text{Humedad}}+\epsilon$$

Para comprobar que el modelo fuese estadísticamente adecuado se revisaron dos supuestos: la **homocedasticidad** y la **normalidad de los residuos** [1]. Los residuos se calcularon como la diferencia entre el valor real y el valor estimado:

$$e_i=Y_i-\hat{Y}_i$$

De acuerdo con el método de Mínimos Cuadrados Ordinarios [1], el cumplimiento de estos supuestos permite considerar a los coeficientes $\beta_j$ como buenos estimadores lineales e insesgados, según el teorema de Gauss-Márkov.

- **Homocedasticidad:** Significa que la varianza de los residuos se mantiene aproximadamente constante, es decir, $\text{Var}(e_i)=\sigma^2$.
- **Normalidad:** Se espera que los residuos sigan aproximadamente una distribución normal, $e_i\sim\mathcal{N}(0,\sigma^2)$. Esto respalda la interpretación de la prueba $t$ aplicada a los coeficientes.

https://github.com/Joseph-L-Q/PI_Equipo_02/blob/0c097c3afedb0f7793e3182da5661214b79f0a3a/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-16%20011640.png
https://github.com/Joseph-L-Q/PI_Equipo_02/blob/0c097c3afedb0f7793e3182da5661214b79f0a3a/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-16%20011702.png
https://github.com/Joseph-L-Q/PI_Equipo_02/blob/0c097c3afedb0f7793e3182da5661214b79f0a3a/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-16%20011731.png
https://github.com/Joseph-L-Q/PI_Equipo_02/blob/0c097c3afedb0f7793e3182da5661214b79f0a3a/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-16%20011745.png

*Figura 3. Entrenamiento de la regresión, coeficientes, estadísticos t, histograma de residuos y gráfico de residuos frente a predicciones.*

### Interpretación de los coeficientes y los supuestos

- **Intercepto ($\beta_0=2.7411$):** Representa el consumo inicial estimado cuando las variables de entrada toman el valor cero. Su interpretación práctica debe realizarse con cuidado, ya que esas condiciones podrían encontrarse fuera del rango observado.
- **Horas de Operación ($\beta_2=1.6688$, $t=127.02$):** Es el predictor con mayor influencia. Manteniendo constantes las demás variables, una hora adicional de funcionamiento incrementaría el consumo en aproximadamente $1.67\,kWh$. El valor t elevado muestra que su coeficiente está claramente alejado de cero respecto a su error estándar.
- **Carga y variables ambientales:** `Carga` ($\beta_3=0.0963$, $t=51.83$) y `Temperatura` ($\beta_1=0.1371$, $t=18.15$) presentan efectos positivos. `Humedad` ($\beta_4=0.0268$, $t=10.26$) tiene una influencia menor, aunque su coeficiente también resulta relevante dentro del modelo.
- **Normalidad de los residuos:** El histograma tiene una forma aproximadamente simétrica y se concentra alrededor de cero. Esto indica que los errores se aproximan a una distribución normal.
- **Homocedasticidad:** En el gráfico de residuos frente a valores predichos, los puntos aparecen repartidos sin un patrón definido y dentro de una franja aproximada de $-6$ a $+6\,kWh$. Al no observarse una forma de cono o una curva marcada, la varianza del error parece mantenerse estable.

### 3.2 Árbol de decisión para regresión

El Árbol de Decisión divide repetidamente el espacio de las variables de entrada. En cada nodo selecciona una variable $X_j$ y un punto de corte $s$ que reduzcan el error dentro de las regiones resultantes. La impureza puede expresarse mediante la suma de errores cuadrados:

$$\text{Impureza (SSE)}=\sum_{i\in R_1}(y_i-\hat{y}_{R_1})^2+\sum_{i\in R_2}(y_i-\hat{y}_{R_2})^2$$

En esta fórmula, $\hat{y}_{R_1}$ y $\hat{y}_{R_2}$ representan el promedio de la variable objetivo en cada región. Para disminuir el riesgo de **sobreajuste**, se limitó la profundidad a `max_depth=5` [2].

https://github.com/Joseph-L-Q/PI_Equipo_02/blob/0c097c3afedb0f7793e3182da5661214b79f0a3a/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-16%20011825.png

*Figura 4. Entrenamiento del árbol con `max_depth=5`, importancia de las características y comparación entre valores reales y predichos.*

### Importancia de las variables y control del modelo

- **Variable principal:** `Horas_Operacion` reúne cerca del **53.7 %** de la importancia total. Al igual que en la regresión, es la variable que más ayuda a explicar el consumo.
- **Variables secundarias:** `Temperatura` representa aproximadamente el **26.9 %** y `Carga` alrededor del **11.1 %**. Las demás características contribuyen en menor proporción a reducir la varianza.
- **Profundidad máxima:** La restricción de cinco niveles evita que el árbol cree demasiadas divisiones para memorizar casos particulares del entrenamiento.
- **Equilibrio entre sesgo y varianza:** Con este límite, el árbol puede representar relaciones no lineales sin volverse excesivamente complejo y conserva un desempeño razonable sobre `X_test`.

---

## 4. Comparación de resultados y discusión

Los modelos se probaron con el 30 % del conjunto de datos, equivalente a **1,500 registros no utilizados durante el entrenamiento**. Para compararlos se emplearon el Error Cuadrático Medio ($MSE$), el Error Absoluto Medio ($MAE$) y el Coeficiente de Determinación ($R^2$).

| Modelo | MSE ($kWh^2$) | MAE ($kWh$) | $R^2$ | Ventajas | Desventajas |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Regresión Lineal** | **4.6124** | **1.7448** | **0.8512** | Permite interpretar directamente el efecto de cada variable; requiere pocos recursos; genera predicciones rápidamente; facilita estudiar la relevancia de los coeficientes. | Supone relaciones lineales y puede verse afectada por valores atípicos o mediciones erróneas. |
| **Árbol de Decisión** | **5.7499** | **1.9239** | **0.8145** | Reconoce relaciones no lineales; no necesita normalidad en los datos; sus divisiones pueden expresarse como reglas sencillas. | Puede cambiar ante pequeñas variaciones de los datos y corre el riesgo de sobreajustarse si no se controla su profundidad. |

### Discusión

1. **Desempeño de las predicciones:**
   - La Regresión Lineal Múltiple alcanzó los mejores resultados en las tres métricas. Su $R^2=0.8512$ indica que explica aproximadamente el **85.12 %** de la variabilidad del consumo, mientras que el árbol explica el **81.45 %**.
   - Su $MAE=1.7448\,kWh$ significa que las predicciones se alejan, en promedio, cerca de $1.74\,kWh$ de los valores reales. Este error es menor que el obtenido con el árbol.

2. **Comportamiento de los datos:**
   - Variables como `Horas_Operacion` y `Carga` mantienen relaciones principalmente lineales con `Consumo_Energia`. Por ello, una función continua de regresión representa estos datos mejor que las predicciones escalonadas que produce un árbol al dividir el espacio en regiones.

### Conclusión de la comparación

Los resultados muestran que la **Regresión Lineal Múltiple** es la alternativa más conveniente para este conjunto de datos. La marcada relación lineal entre las horas de operación y el consumo permite alcanzar un $R^2$ de 0.8512 y un error absoluto medio cercano a $1.74\,kWh$. Además, al tratarse de una ecuación sencilla, puede integrarse en sistemas de monitoreo en tiempo real o dispositivos IoT con recursos limitados.

El **Árbol de Decisión** obtuvo un error ligeramente mayor, con un $MAE$ aproximado de $1.92\,kWh$. Sin embargo, sigue siendo útil cuando se necesitan reglas fáciles de visualizar, como generar alertas según determinados niveles de temperatura y carga. También podría resultar más apropiado si posteriormente aparecen relaciones no lineales más complejas.

---

## 5. Aprendizajes principales del desarrollo

Uno de los aprendizajes más importantes del taller fue entender que desarrollar un modelo de inteligencia artificial no consiste únicamente en ejecutar un algoritmo. Primero es necesario revisar los datos, conocer el significado de las variables, preparar la información y después evaluar si el resultado realmente es confiable.

El análisis exploratorio ayudó a conocer cómo estaban distribuidos los datos y qué variables tenían una mayor relación con el consumo. Luego, las métricas y los gráficos de residuos permitieron comprobar el comportamiento de las predicciones. La comparación entre ambos modelos también permitió comprender que no existe un algoritmo ideal para todos los casos, ya que su utilidad depende de las características del problema y de los datos disponibles.

---

## 6. Archivo principal del proyecto

El procedimiento completo se encuentra en el siguiente notebook:

- [https://github.com/Joseph-L-Q/PI_Equipo_02/blob/883baf2025cea2ac40ce47bfb3caa032e26716e4/Proyecto_Integrador/Talleres/Taller%2003/Lombardi_Joseph/readme.md`Regresion_Lineal_Joseph_Lombardi.ipynb`]

En este archivo se incluye la exploración inicial, la preparación del conjunto de datos, el entrenamiento de la regresión lineal, la evaluación de las predicciones y los residuos, así como la implementación y revisión del árbol de decisión.

---

## 7. Conclusiones finales

La realización del taller permitió reconocer las etapas fundamentales de un proyecto de ciencia de datos, desde la inspección de la información hasta la construcción y comparación de modelos predictivos. La regresión lineal ayudó a medir de forma directa cómo cambia el consumo energético según cada variable. Por su parte, el árbol de decisión ofreció otra manera de analizar los datos mediante divisiones y permitió observar la importancia relativa de las características.

Este aprendizaje también puede relacionarse con nuestro proyecto de cultivo de conchas de abanico. Las técnicas de regresión y análisis exploratorio podrían aplicarse para estimar el crecimiento, la supervivencia o la biomasa a partir de parámetros del agua como temperatura, salinidad, pH y oxígeno disuelto. Por ello, lo más importante no fue solamente obtener buenas métricas, sino aprender a interpretar los datos, comprobar los supuestos y utilizar las predicciones para apoyar decisiones reales.

---

## 8. Referencias

- [1] D. C. Montgomery, E. A. Peck y G. G. Vining, *Introduction to Linear Regression Analysis*, 5.ª ed. Hoboken, NJ: John Wiley & Sons, 2012.
- [2] Referencia utilizada para el control de profundidad y sobreajuste en árboles de decisión.
