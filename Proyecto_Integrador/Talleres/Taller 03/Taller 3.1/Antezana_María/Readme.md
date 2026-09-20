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
