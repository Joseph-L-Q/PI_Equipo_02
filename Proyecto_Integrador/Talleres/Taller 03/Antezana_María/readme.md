# Taller 3: Regresión Lineal y Árboles de Decisión

---

## 1. Introducción y Planteamiento del Problema
*Breve contextualización del dataset, definición del problema a resolver, objetivo del análisis y su justificación dentro del marco de la ciencia de datos.*

---

## 2. Análisis Exploratorio de Datos (EDA)

### 2.1 Carga e Inspección Estructural
*Fundamento teórico sobre la verificación de la integridad del dataset, limpieza de datos y manejo de valores nulos.*

![Fig. 1. Inspección de tipos de datos y resumen estadístico inicial](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Inspecci%C3%B3n%20de%20tipos%20de%20datos.jpg)  
* **Fig. 1.** Inspección de tipos de datos y resumen estadístico inicial.

*Interpretación crítica de la distribución de las variables, presencia de valores atípicos (outliers) y escala de los datos.*

### 2.2 Análisis de Relaciones y Correlación
*Justificación técnica de la selección de características (feature selection) mediante evaluación de independencia entre variables.*

![Fig. 2. Matriz de dispersión y correlación entre variables numéricas](ruta/a/tu/imagen2.png)  
* **Fig. 2.** Matriz de dispersión y correlación entre variables numéricas.

*Análisis estadístico de los patrones visuales observados, identificando colinealidad y variables clave para el modelado.*

---

## 3. Desarrollo y Evaluación de Modelos

### 3.1 Regresión Lineal Multi-variable
*Principios matemáticos del modelo de Regresión Lineal, supuestos de homocedasticidad y normalidad de residuos [1].*

![Fig. 3. Código de entrenamiento y gráfica de residuos del modelo de Regresión Lineal](ruta/a/tu/imagen3.png)  
* **Fig. 3.** Código de entrenamiento y gráfica de residuos del modelo de Regresión Lineal.

*Análisis del desempeño del modelo basado en los coeficientes obtenidos y el comportamiento de las predicciones frente a los valores reales.*

### 3.2 Árboles de Decisión para Regresión
*Fundamentos del algoritmo de partición recursiva, criterios de impureza y control de profundidad para evitar sobreajuste [2].*

![Fig. 4. Visualización de la estructura y divisiones del Árbol de Decisión](ruta/a/tu/imagen4.png)  
* **Fig. 4.** Visualización de la estructura y divisiones del Árbol de Decisión.

*Evaluación de la importancia de variables en el árbol y diagnóstico del equilibrio entre sesgo y varianza.*

---

## 4. Comparativa de Resultados y Discusión

*Evaluación cuantitativa comparativa de las métricas clave obtenidas en la fase de prueba:*

| Modelo | MSE | MAE | $R^2$ Score | Fortalezas | Limitaciones |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Regresión Lineal** | *[Valor]* | *[Valor]* | *[Valor]* | Alta interpretabilidad, bajo costo computacional | Sensible a *outliers* y asume linealidad |
| **Árbol de Decisión** | *[Valor]* | *[Valor]* | *[Valor]* | Captura relaciones no lineales complejas | Propenso a *overfitting* sin poda |

*Discusión sobre qué modelo ofrece el mejor rendimiento en función de las necesidades operativas del problema.*

---

## 5. Propuesta de Integración en Arquitectura de Datos
*Estrategia para empaquetar el modelo entrenado (`joblib`/`pickle`), automatizar la ingesta de datos y desplegarlo como servicio consumible.*

*Descripción del flujo de inferencia en tiempo real o por lotes para el proyecto.*

---

## Referencias

* [1] F. Pedregosa *et al.*, "Scikit-learn: Machine Learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825-2830, 2011.
* [2] L. Breiman, *Classification and Regression Trees*, Routledge, 2017.
* [3] IEEE, "IEEE Editorial Style Manual," IEEE Periodicals, Piscataway, NJ, USA, 2021.
