# Taller 3: Regresión Lineal y Árboles de Decisión aplicado a la predicción del consumo energético

---

# 1. Introducción y planteamiento del problema

En el presente taller se aplicaron técnicas de aprendizaje automático con el objetivo de desarrollar modelos predictivos capaces de estimar el consumo energético a partir de diferentes variables relacionadas con las condiciones de operación de un sistema.

El análisis se realizó utilizando un conjunto de datos compuesto por variables como temperatura, horas de operación, carga y humedad, las cuales pueden influir en el comportamiento del consumo energético.

El objetivo principal fue comprender el proceso completo de construcción de un modelo predictivo, iniciando desde la exploración y preparación de los datos, continuando con el entrenamiento de modelos y finalmente evaluando la capacidad de predicción obtenida.

Para ello, se implementó inicialmente un modelo de regresión lineal, una técnica de aprendizaje supervisado que permite establecer una relación matemática entre variables predictoras y una variable objetivo [1]. Posteriormente, se desarrolló un modelo basado en árboles de decisión con la finalidad de comparar diferentes enfoques de aprendizaje automático y analizar la importancia de las variables dentro del proceso predictivo [2].

---

# 2. Análisis Exploratorio de Datos (EDA)

Antes de realizar el entrenamiento de los modelos, se efectuó un análisis exploratorio del conjunto de datos con la finalidad de comprender su estructura, distribución y comportamiento.

Esta etapa es fundamental dentro de un proyecto de ciencia de datos, debido a que permite identificar características importantes del dataset y tomar mejores decisiones antes de aplicar algoritmos de aprendizaje automático.

---

## 2.1 Inspección inicial del conjunto de datos

Se realizó una revisión inicial mediante herramientas estadísticas y descriptivas para conocer la estructura del dataset, la cantidad de registros disponibles, los tipos de variables y los valores principales de cada característica.

Este análisis permitió verificar la organización de la información y comprender la naturaleza de los datos antes de iniciar la construcción de los modelos.

<img width="646" height="628" alt="Captura de pantalla 2026-09-15 222700" src="https://github.com/user-attachments/assets/11bf8f53-083e-4a77-95d2-9ddf9b7eb3c0" />


**Fig. 1.** Inspección de la estructura del conjunto de datos mediante información general y estadísticas descriptivas.

---

## 2.2 Análisis visual y distribución de variables

Se utilizaron diferentes representaciones gráficas para analizar el comportamiento de las variables involucradas en el problema.

Mediante gráficos de dispersión, histogramas y gráficos de densidad fue posible observar tendencias, patrones y la distribución del consumo energético.

El análisis visual permitió identificar relaciones iniciales entre variables y comprender mejor el comportamiento de los datos antes del entrenamiento del modelo.

![Fig. 2. Relación gráfica entre variables del dataset](ruta_de_la_imagen)

**Fig. 2.** Matriz de dispersión utilizada para analizar relaciones visuales entre las variables del conjunto de datos.

![Fig. 3. Distribución del consumo energético](ruta_de_la_imagen)

**Fig. 3.** Distribución del consumo energético mediante histogramas y gráficos de densidad.

---

## 2.3 Análisis de correlación entre variables

Para identificar la relación existente entre las variables numéricas se construyó una matriz de correlación representada mediante un mapa de calor (*heatmap*).

Este análisis permitió conocer qué variables presentan mayor relación con el consumo energético y comprender la influencia potencial de cada característica dentro del modelo predictivo.

![Fig. 4. Matriz de correlación entre variables](ruta_de_la_imagen)

**Fig. 4.** Mapa de calor de correlación utilizado para identificar relaciones entre las variables del dataset.

---

# 3. Desarrollo del modelo de regresión lineal

La regresión lineal fue utilizada como primer modelo predictivo debido a su capacidad para representar la relación entre una variable objetivo y diferentes variables explicativas mediante una ecuación matemática [1].

Para desarrollar el modelo se realizó la separación de los datos en conjuntos de entrenamiento y prueba. Esta división permitió que el algoritmo aprendiera utilizando una parte de la información y posteriormente fuera evaluado con datos que no habían sido utilizados durante el entrenamiento.

Durante esta etapa se obtuvieron los coeficientes del modelo, los cuales permiten interpretar la influencia de cada variable sobre el consumo energético.

![Fig. 5. Entrenamiento del modelo de regresión lineal](ruta_de_la_imagen)

**Fig. 5.** Entrenamiento del modelo de regresión lineal y obtención de coeficientes asociados a las variables predictoras.

---

# 4. Evaluación del modelo de regresión lineal

La evaluación del modelo fue una etapa fundamental para determinar si las predicciones obtenidas representaban adecuadamente el comportamiento de los datos.

Para ello, se realizó una comparación entre los valores reales y los valores predichos por el modelo, permitiendo analizar qué tan cercanas eran las estimaciones generadas.

Además, se efectuó un análisis de residuos para estudiar la diferencia entre los valores reales y las predicciones, permitiendo comprender el comportamiento de los errores generados por el modelo.

También se realizó una evaluación estadística mediante el cálculo del error estándar y el estadístico T, con la finalidad de analizar la relevancia de los coeficientes obtenidos.

![Fig. 6. Comparación entre valores reales y predichos](ruta_de_la_imagen)

**Fig. 6.** Comparación gráfica entre los valores reales del consumo energético y las predicciones generadas por el modelo.

![Fig. 7. Análisis de residuos del modelo](ruta_de_la_imagen)

**Fig. 7.** Análisis del comportamiento de los residuos para evaluar los errores del modelo de regresión lineal.

---

# 5. Modelo basado en árboles de decisión

Como segundo enfoque de aprendizaje automático se implementó un modelo basado en árboles de decisión utilizando datos simulados.

Este algoritmo utiliza reglas de decisión generadas mediante divisiones sucesivas de las variables para realizar predicciones y determinar la importancia relativa de las características utilizadas [2].

El desarrollo de este modelo permitió comparar una metodología basada en relaciones matemáticas lineales frente a un modelo capaz de identificar patrones mediante reglas de decisión.

![Fig. 8. Implementación del árbol de decisión](ruta_de_la_imagen)

**Fig. 8.** Entrenamiento y evaluación del modelo basado en árbol de decisión utilizando datos simulados.

![Fig. 9. Importancia de variables del árbol de decisión](ruta_de_la_imagen)

**Fig. 9.** Importancia relativa de las características identificadas por el modelo de árbol de decisión.

---

# 6. Comparación y discusión de resultados

El desarrollo de ambos modelos permitió comprender que cada algoritmo posee características diferentes y que su elección depende del tipo de problema que se desea resolver.

| Modelo | Característica principal | Ventaja | Limitación |
|---|---|---|---|
| Regresión Lineal | Establece relaciones matemáticas entre variables | Alta interpretación de los coeficientes obtenidos | Requiere relaciones aproximadamente lineales |
| Árbol de Decisión | Genera reglas mediante divisiones de variables | Permite identificar patrones y variables importantes | Puede presentar sobreajuste |

La comparación permitió reconocer que un modelo predictivo no debe evaluarse únicamente por generar resultados, sino también por la capacidad de interpretar la información y validar que sus predicciones sean coherentes.

---

# 7. Aspectos más importantes del desarrollo

Uno de los principales aprendizajes obtenidos durante el taller fue comprender que la construcción de un modelo de inteligencia artificial requiere varias etapas y no solamente el entrenamiento de un algoritmo.

La exploración inicial de los datos permitió comprender la información disponible, mientras que la evaluación del modelo permitió analizar si las predicciones obtenidas eran confiables.

La parte más importante del desarrollo fue comprender la relación entre los datos, el modelo y los resultados obtenidos. La comparación entre regresión lineal y árbol de decisión permitió reconocer que existen diferentes formas de aprendizaje y que cada una presenta ventajas dependiendo del problema analizado.

---

# 8. Archivo principal del proyecto

El desarrollo completo del taller se encuentra implementado en el siguiente notebook:

- `Regresion_lineal_Santamaria.ipynb`

Este archivo contiene el análisis exploratorio de datos, preparación del dataset, entrenamiento del modelo de regresión lineal, evaluación mediante predicciones y residuos, además de la implementación y análisis del modelo basado en árbol de decisión.

---

# 9. Conclusión

El desarrollo de este taller permitió comprender las principales etapas involucradas en un proyecto de ciencia de datos, desde la exploración inicial de información hasta la construcción y evaluación de modelos predictivos.

La regresión lineal permitió analizar cómo diferentes variables pueden relacionarse con el consumo energético y generar predicciones mediante un modelo matemático. Por otro lado, el árbol de decisión permitió observar una alternativa diferente para identificar patrones y variables relevantes.

En conclusión, el aprendizaje más importante fue comprender que un modelo predictivo no debe evaluarse únicamente por sus resultados numéricos, sino también por la capacidad de analizar los datos, interpretar sus resultados y validar que sus predicciones sean adecuadas para el problema planteado.

---

# Referencias

[1] Pedregosa F, Varoquaux G, Gramfort A, Michel V, Thirion B, Grisel O, et al. Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research*. 2011;12:2825-2830.

[2] Scikit-learn Developers. Decision Trees. *Scikit-learn Documentation*. Disponible en: https://scikit-learn.org/stable/modules/tree.html
