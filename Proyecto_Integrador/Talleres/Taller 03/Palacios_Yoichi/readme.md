# Taller 3: Introducción a la IA - Regresión Lineal y Árboles de Decisión

**Autor:** Yoichi Palacios Tanaka
**Proyecto:** LanternGuard, monitoreo de biofouling en linternas de cultivo de concha de abanico

---

## 1. Introducción y Planteamiento del Problema

El objetivo de este taller es ajustar un modelo de **regresión lineal multivariable** que
prediga el consumo de energía de un equipo a partir de cuatro variables de operación, y
luego contrastarlo contra un **árbol de decisión** para comprobar si la suposición de
linealidad es razonable.

La pregunta que importa para el proyecto no es solo cuánto acierta el modelo, sino **qué
variable manda**. El nodo sumergido de LanternGuard funciona con una batería que se recarga
mediante el panel solar de la boya de superficie, así que el margen energético es una
restricción de diseño real. Saber qué factor domina el consumo decide cómo se programa el
ciclo de trabajo del nodo.

## 2. Análisis Exploratorio de Datos

### 2.1 Carga e Inspección Estructural

El conjunto de datos es `Data_PI_regresion.csv`, el mismo utilizado en clase. Contiene
**5000 registros y 5 columnas**, todas de tipo `float64` y **sin valores nulos**, por lo que
no fue necesario limpiar ni convertir tipos antes de modelar.

| Columna | Rol |
|---|---|
| `Temperatura` | Variable independiente |
| `Horas_Operacion` | Variable independiente |
| `Carga` | Variable independiente |
| `Humedad` | Variable independiente |
| `Consumo_Energia` | **Variable objetivo** |

### 2.2 Análisis de Relaciones y Correlación

Se graficó cada variable independiente contra el consumo de energía. Solo
`Horas_Operacion` dibuja una banda claramente inclinada; `Carga` insinúa una pendiente
suave, y `Temperatura` y `Humedad` son nubes sin dirección.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller3_Palacios_Dispersion.png" alt="Diagramas de dispersión de cada variable contra el consumo de energía" width="100%"/>
  <br>
  <em>Figura 1. Dispersión de cada variable independiente frente a Consumo_Energia.</em>
</p>

El mapa de calor confirma numéricamente lo que se ve en los gráficos.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller3_Palacios_Heatmap.png" alt="Matriz de correlación en mapa de calor" width="100%"/>
  <br>
  <em>Figura 2. Matriz de correlación de las cinco variables del conjunto de datos.</em>
</p>

Correlación de cada variable con `Consumo_Energia`:

| Variable | Correlación | Lectura |
|---|:---:|---|
| `Horas_Operacion` | **0.8434** | Relación lineal positiva fuerte |
| `Carga` | 0.3366 | Relación positiva moderada/baja |
| `Temperatura` | 0.0978 | Relación muy débil |
| `Humedad` | 0.0627 | Prácticamente nula |

Un detalle que resulta clave más adelante: **entre las variables independientes las
correlaciones son casi nulas** (todas por debajo de 0.03 en valor absoluto). No hay
multicolinealidad.

## 3. Desarrollo y Evaluación de Modelos

Los datos se dividieron en 70% entrenamiento y 30% prueba con
`train_test_split(..., test_size=0.3, random_state=123)`, lo que da **3500 registros de
entrenamiento y 1500 de prueba**.

> **Nota sobre `random_state`:** se usó `123`, el mismo valor del notebook de clase. Con ese
> valor el modelo reproduce exactamente el término de intersección mostrado por el profesor
> ($2.741067446117448$) y sus cuatro coeficientes.

### 3.1 Regresión Lineal Multi-variable

Término de intersección: $2.7411$

| Variable | Coeficiente | Error estándar | Estadístico t |
|---|---:|---:|---:|
| `Temperatura` | 0.137137 | 0.007557 | 18.15 |
| `Horas_Operacion` | **1.668778** | 0.013138 | **127.02** |
| `Carga` | 0.096348 | 0.001859 | 51.83 |
| `Humedad` | 0.026791 | 0.002611 | 10.26 |

Las cuatro variables son estadísticamente significativas ($|t| > 2$), pero la magnitud del
efecto es muy distinta: una hora más de operación suma $1.67$ kWh, mientras que un grado
más de temperatura suma apenas $0.14$ kWh.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Taller3_Palacios_Real_vs_Predicho.png" alt="Consumo de energía real frente al predicho" width="100%"/>
  <br>
  <em>Figura 3. Consumo de energía real vs. el predicho, con la línea de 45° de referencia.</em>
</p>

**Sobre el cálculo de los errores estándar.** La fórmula usada en clase,

$$SE(\hat{\beta}_i) = \sqrt{\frac{SSE / (n-k)}{\sum_j (x_{ij} - \bar{x}_i)^2}}$$

es la del error estándar de una regresión **simple**, aplicada variable por variable. En una
regresión múltiple lo correcto en general es usar la diagonal de $\sigma^2 (X^{T}X)^{-1}$.
Ambas coinciden únicamente cuando las variables independientes no están correlacionadas
entre sí, que es exactamente el caso de este conjunto de datos. El notebook incluye una
celda de verificación con `statsmodels.api.OLS` cuyos estadísticos t confirman el resultado.

### 3.2 Árboles de Decisión para Regresión

Se ajustó un `DecisionTreeRegressor(max_depth=4, random_state=42)` como contraste. A
diferencia de la regresión lineal, el árbol no supone que la relación sea una recta: parte
los datos en grupos mediante cortes sucesivos y predice el promedio de cada grupo.

## 4. Comparativa de Resultados, Discusión y conclusión

| Modelo | MAE ($kWh$) | MSE ($kWh^2$) | RMSE ($kWh$) | $R^2$ Score |
| :--- | ---: | ---: | ---: | ---: |
| **Regresión Lineal** | **1.7448** | **4.6124** | **2.1476** | **0.8512** |
| **Árbol de Decisión** | 1.9712 | 6.0879 | 2.4674 | 0.8036 |

### Discusión

La regresión lineal supera al árbol de decisión en las cuatro métricas. Esto no es un
detalle menor: significa que la relación entre las variables de operación y el consumo es
**efectivamente lineal**, sin quiebres ni umbrales que la recta esté dejando pasar. Si
existiera un punto de inflexión, el árbol lo habría capturado y habría ganado.

El modelo lineal explica alrededor del **85%** de la variación del consumo y se equivoca, en
promedio, en menos de **2 kWh**. El 15% restante corresponde al ruido propio del proceso,
que ninguna de las cuatro variables disponibles alcanza a explicar.

### Conclusión

`Horas_Operacion` domina el modelo por tres vías independientes que apuntan a lo mismo: es
la correlación más alta (0.84), el coeficiente más grande (1.67) y, por lejos, el mayor
estadístico t (127). `Temperatura` y `Humedad` son significativas en el sentido estadístico,
pero su efecto práctico sobre el consumo es marginal.

## 5. Aspectos más importantes del desarrollo

- **Significancia estadística no es lo mismo que relevancia práctica.** Con 5000 registros,
  hasta un efecto diminuto sale significativo. `Humedad` tiene $t = 10.26$ y aun así aporta
  $0.027$ kWh por unidad. Hay que mirar el coeficiente, no solo el estadístico t.
- **La ausencia de multicolinealidad es lo que valida el método de la clase.** Fue necesario
  comprobarlo en la matriz de correlación antes de dar por bueno el cálculo de los errores
  estándar, y verificarlo después con `statsmodels`.
- **Que un modelo más flexible pierda es información útil.** El árbol de decisión no perdió
  por estar mal configurado, sino porque no había no-linealidad que explotar.

## 6. Archivo principal del proyecto

- Notebook: [`Regresión_Lineal_Palacios.ipynb`](./Regresión_Lineal_Palacios.ipynb)
- Conjunto de datos: [`Data_PI_regresion.csv`](./Data_PI_regresion.csv)
- Enlace a Google Colab: `[ENLACE COLAB]`

## 7. Conclusiones finales

Para LanternGuard el resultado respalda una decisión concreta de diseño: **el consumo del
nodo sumergido se controla recortando el tiempo encendido, no optimizando las condiciones
ambientales**, que además no podemos controlar bajo el agua. El nodo debe capturar en ciclos
cortos y dormir el resto del tiempo.

Esto se alinea con la fila *Energía* de la Lista de Exigencias, que fija un consumo activo
de 2.0 W a 5.0 W y un consumo en reposo menor a 0.15 W: la diferencia entre ambos estados es
de más de un orden de magnitud, así que cada minuto que el nodo pasa despierto sin capturar
es margen energético desperdiciado.

En lo personal, el aprendizaje más útil del taller fue que las métricas no se leen solas.
Un $R^2$ de 0.85 no dice nada por sí mismo hasta que se compara contra un modelo alternativo
y se revisa qué variable está haciendo el trabajo.

## 8. Referencias

[1] F. Pedregosa *et al.*, "Scikit-learn: Machine learning in Python", *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, 2011. https://jmlr.org/papers/v12/pedregosa11a.html

[2] S. Seabold y J. Perktold, "Statsmodels: Econometric and statistical modeling with Python", en *Proceedings of the 9th Python in Science Conference*, 2010, pp. 92-96. https://doi.org/10.25080/Majora-92bf1922-011

[3] G. James, D. Witten, T. Hastie y R. Tibshirani, *An Introduction to Statistical Learning with Applications in Python*. Cham, Suiza: Springer, 2023. https://www.statlearning.com/
