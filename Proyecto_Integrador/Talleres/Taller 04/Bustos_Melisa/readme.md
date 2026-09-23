# Taller 04: Redes Neuronales - CNN, Keras y Perceptrón

## Introducción

Una red neuronal artificial es, en el fondo, un intento de replicar computacionalmente cómo un conjunto de unidades simples puede aprender patrones a partir de ejemplos. La idea nace de un modelo matemático de neurona propuesto por McCulloch y Pitts en 1943, donde una neurona artificial simplemente suma señales de entrada y decide si "se activa" o no [1]. Con el tiempo esa idea fue creciendo: de una sola neurona se pasó a conectar muchas en capas, y de ahí a arquitecturas mucho más profundas, capaces de aprender directamente de imágenes, texto o cualquier otro tipo de dato, sin que alguien tenga que programar a mano las reglas de decisión [2].

Hoy estas redes están detrás de la mayoría de los sistemas que reconocen imágenes, entienden texto o toman decisiones automáticas, justamente porque aprenden los patrones a partir de los datos en vez de depender de reglas fijas escritas por una persona. Por ello, en este trabajo exploramos tres formas distintas de construir y entrenar este tipo de redes: una CNN para clasificar imágenes, un modelo armado con Keras para clasificar texto y un perceptrón construido desde cero para entender la lógica que hay detrás de todo lo demás. Por cada una explicamos qué es, qué funciones usamos, qué resultados dio y por qué es importante. Al final mostramos cómo aplicaríamos estas herramientas en nuestro proyecto LanterGuard de monitoreo de conchas de abanico.

---

## 1. CNN (Red Neuronal Convolucional)

### ¿Qué es y para qué sirve?

Una CNN es una red pensada para trabajar con imágenes. En lugar de mirar cada pixel por separado, recorre la imagen con pequeños filtros (kernels) que van detectando patrones: bordes, texturas, formas. Con varias capas apiladas, las primeras detectan cosas simples (líneas, bordes) y las últimas detectan formas más completas (un objeto entero). Por eso es la herramienta estándar cuando el problema depende de reconocer algo visualmente, como diferenciar dos tipos de residuos en una foto, algo que fue justamente nuestro ejercicio: separar vidrio de plástico usando el dataset TrashNet.

Esta idea de usar filtros que se deslizan sobre la imagen para reconocer patrones visuales fue formalizada por LeCun et al. en 1998, cuando mostraron que las CNN superaban a otras técnicas en el reconocimiento de dígitos escritos a mano [3].

### Piezas clave que usamos

- **Conv2D**: aplica los filtros y genera "mapas de características". Cada filtro aprende a detectar algo distinto.
- **ReLU**: es la función de activación. Su regla es simple: si el valor es negativo lo convierte en 0, si es positivo lo deja igual. Esto le da a la red la capacidad de aprender relaciones que no son lineales.
- **MaxPool2D**: reduce el tamaño de la imagen quedándose con lo más relevante de cada zona, lo que ayuda a que el modelo generalice y no se sature de cálculos.
- **AdaptiveAvgPool2D**: al final de los bloques convolucionales, resume cada mapa de características en un solo valor promedio, sin importar el tamaño original de la imagen.
- **Flatten + Linear (capa densa)**: "aplana" lo que queda de la parte convolucional y lo conecta con una capa totalmente conectada, que es la que finalmente decide entre vidrio y plástico.

Todas estas piezas conectadas, en el orden en que las usamos, se ven en la Figura 1:

<p align="center">
  <img width="857" height="717" alt="image" src="https://github.com/user-attachments/assets/4ad68d8d-feea-43b7-998a-64e1d04f7fbc" />
</p>
<p align="center"><em>Figura 1. Código de la arquitectura de la CNN entrenada desde cero (bloques Conv2D, ReLU, MaxPool2D, AdaptiveAvgPool2D y la capa densa final).</em></p>

Como se aprecia en la Figura 1, el modelo combina tres bloques convolucionales (cada uno con su ReLU y su MaxPool2D) antes de llegar al AdaptiveAvgPool2D y a la capa densa final, que es la que entrega la predicción entre vidrio y plástico.

### Lo que hicimos paso a paso

1. Cargamos el dataset TrashNet, con fotos en escala de grises de vidrio (0) y plástico (1).
2. Miramos ejemplos del dataset para asegurarnos de que las etiquetas tenían sentido.

<p align="center">
  <img width="787" height="736" alt="image" src="https://github.com/user-attachments/assets/f409f8f8-edfe-47d2-84ab-c41c9d86cc24" />
</p>
<p align="center"><em>Figura 2. Código usado para mostrar ejemplos del dataset TrashNet.</em></p>

<p align="center">
  <img width="989" height="661" alt="figura03_dataset_ejemplos" src="https://github.com/user-attachments/assets/446940b0-6873-4d96-b39b-918bc4ff7c1f" />
</p>
<p align="center"><em>Figura 3. Ejemplos del dataset TrashNet (vidrio y plástico).</em></p>

En la Figura 2 se muestra el código usado para desplegar los ejemplos, y en la Figura 3 se observa el resultado: las fotos de vidrio son botellas y frascos, y las de plástico son botellas y envases transparentes. Visualmente se parecen bastante entre sí, lo que ya nos avisa que el problema no iba a ser trivial para el modelo.

3. Entrenamos una CNN simple desde cero durante 8 épocas.

<p align="center">
  <img width="1066" height="370" alt="image" src="https://github.com/user-attachments/assets/2f5db870-0ac7-4ad8-a85a-8a3930ad22c3" />
</p>
<p align="center"><em>Figura 4. Código usado para graficar la pérdida y las métricas de validación durante el entrenamiento.</em></p>

<p align="center">
  <img width="864" height="395" alt="figura05_perdida_entrenamiento" src="https://github.com/user-attachments/assets/7560c4dd-ca4c-49e6-b330-146af6781427" />
</p>
<p align="center"><em>Figura 5. Pérdida de entrenamiento (CNN desde cero).</em></p>

<p align="center">
  <img width="855" height="395" alt="figura06_metricas_validacion" src="https://github.com/user-attachments/assets/9b9437ff-a449-49da-8bb5-28421c127441" />
</p>
<p align="center"><em>Figura 6. Métricas de validación (CNN desde cero).</em></p>

En la Figura 4 se muestra el código que grafica ambas curvas. El resultado se observa en las Figuras 5 y 6: la pérdida (Figura 5) baja, pero muy poco, mientras que en las métricas de validación (Figura 6) el ROC-AUC sí mejora, llegando cerca de 0.70, lo que indica que el modelo va encontrando alguna diferencia entre las clases. Sin embargo, el accuracy se queda pegado alrededor del 50%, y hacia el final incluso baja. Esto se confirma con la matriz de confusión en el set de prueba:

<p align="center">
  <img width="1093" height="302" alt="image" src="https://github.com/user-attachments/assets/c0de8cef-5858-42b5-83bb-594d99e4c652" />
</p>
<p align="center"><em>Figura 7. Código usado para graficar la matriz de confusión.</em></p>

<p align="center">
  <img width="364" height="341" alt="figura08_matriz_confusion" src="https://github.com/user-attachments/assets/bbceb026-6120-469a-bd46-58e97c2ce8ac" />
</p>
<p align="center"><em>Figura 8. Matriz de confusión CNN desde cero.</em></p>

En la Figura 7 se muestra el código usado para generarla, y en la Figura 8 se observa el resultado: el modelo predijo casi siempre la clase 0 (vidrio), acertando por pura casualidad en la mitad de los casos. En la práctica, esto significa que la red desde cero, con solo 8 épocas y pocos datos, no alcanzó a aprender rasgos realmente útiles: aprendió un atajo (predecir siempre lo mismo) en vez de aprender a distinguir.

4. Probamos con **data augmentation** (rotaciones y traslaciones pequeñas) para darle más variedad de ejemplos al modelo sin necesidad de más fotos reales.
5. Probamos **transfer learning**: en vez de entrenar una red desde cero, usamos ResNet18, un modelo ya entrenado en millones de imágenes (ImageNet), y solo ajustamos su última capa a nuestro problema. Esta idea de reutilizar redes profundas ya entrenadas, en vez de partir de cero, viene de arquitecturas como ResNet, que introdujeron las conexiones residuales para poder entrenar redes mucho más profundas sin que se degrade el aprendizaje [4].

<p align="center">
  <img width="1287" height="375" alt="image" src="https://github.com/user-attachments/assets/02b20f4e-6662-44da-8b2c-6f91ee2b61dc" />
</p>
<p align="center"><em>Figura 9. Código para construir el modelo con transfer learning a partir de ResNet18.</em></p>

En la Figura 9 se muestra cómo se reemplaza la última capa de ResNet18 (fc) por una nueva capa lineal adaptada a nuestras dos clases, dejando el resto de la red tal como venía entrenada, para aprovechar lo que ya aprendió con ImageNet. Con este cambio, el aprendizaje mejoró notoriamente: el modelo empezó a distinguir mejor entre vidrio y plástico, algo que no lográbamos entrenando desde cero. Luego hicimos **fine-tuning**, descongelando las últimas capas de ResNet18 para que se ajustaran mejor a nuestras imágenes específicas.

6. Por último, usamos **Grad-CAM** para entender en qué parte de la imagen se fijaba el modelo al momento de predecir. Esta técnica genera un mapa de calor sobre la imagen original, señalando las zonas que más influyeron en la decisión [5].

<p align="center">
  <img width="963" height="667" alt="image" src="https://github.com/user-attachments/assets/060faa07-1b4b-4b29-9e1f-4b00fe49a11e" />
</p>
<p align="center"><em>Figura 10. Código usado para generar el mapa de calor de Grad-CAM sobre una imagen de prueba.</em></p>

<p align="center">
  <img width="990" height="356" alt="figura11_gradcam" src="https://github.com/user-attachments/assets/7fbf0201-9af3-437d-986e-c15593bc0cc8" />
</p>
<p align="center"><em>Figura 11. Grad-CAM sobre una imagen del set de prueba.</em></p>

En la Figura 10 se muestra el código que genera el mapa de calor, y en la Figura 11 se observa el resultado sobre una imagen de prueba: las zonas amarillas son las que más pesaron en la predicción, y las moradas las que casi no importaron. En este caso, el modelo se fijó en el centro de la botella, que tiene sentido porque ahí está la textura y forma del vidrio.

### Lo que aprendimos

- Entrenar una CNN desde cero con pocos datos y pocas épocas no siempre funciona: el modelo puede "hacer trampa" prediciendo siempre la misma clase.
- El transfer learning es una herramienta poderosa cuando no tenemos muchos datos propios, porque aprovechamos todo lo que un modelo grande ya aprendió antes.
- Grad-CAM nos ayuda a confiar (o desconfiar) de un modelo, porque muestra si realmente está mirando lo que debería mirar y no algo irrelevante del fondo de la imagen.

### Por qué es importante

Las CNN son la base de casi todo lo que hoy funciona con imágenes: cámaras de seguridad, diagnóstico médico por imágenes, autos autónomos, control de calidad en fábricas, etc. Entender cómo se arma una y por qué a veces falla (como nos pasó con el modelo desde cero) es tan importante como saber usarla cuando funciona bien.

---

## 2. Clasificación binaria con Keras

### ¿Qué es y para qué sirve?

Keras es una librería que permite armar y entrenar redes neuronales sin tener que programar cada operación matemática a mano. Uno arma la red por capas, como si fuera un molde, y Keras se encarga de todo el cálculo de gradientes y ajustes de pesos por detrás. Es ideal para ir directo al diseño del modelo sin perder tiempo en detalles de bajo nivel.

En nuestro ejercicio usamos Keras para un problema de texto: clasificar reseñas de películas del dataset IMDB como positivas o negativas.

### Funciones clave que usamos

- **Sequential**: es el "molde" donde vamos apilando las capas de la red, una tras otra, en orden.
- **Dense**: una capa donde cada neurona está conectada con todas las de la capa anterior. Es la capa más básica de una red.
- **activation='relu'**: la misma función de activación que vimos en la CNN, para las capas ocultas.
- **activation='sigmoid'**: convierte la salida en un número entre 0 y 1, perfecto para decir "probabilidad de que sea positiva".
- **compile**: define cómo se va a entrenar el modelo (optimizador, función de pérdida, métrica).
- **fit**: entrena el modelo con los datos.
- **Dropout** y **regularizers.l2**: técnicas para evitar que el modelo memorice de más los datos de entrenamiento.

<p align="center">
  <img width="1305" height="376" alt="image" src="https://github.com/user-attachments/assets/54d95d69-34cb-4ae3-bfff-5424edfd83d9" />
</p>
<p align="center"><em>Figura 12. Código para crear y compilar el modelo base (capas Dense + compile).</em></p>

En la Figura 12 se observa cómo se apilan dos capas ocultas de 16 neuronas con activación ReLU, seguidas de una capa de salida de una sola neurona con activación sigmoid, y cómo se compila el modelo con el optimizador rmsprop y la función de pérdida binary_crossentropy, que es la adecuada cuando solo hay dos clases posibles (positiva o negativa).

### Lo que hicimos paso a paso

1. Descargamos el dataset de IMDB, que ya viene con las reseñas convertidas en secuencias de números (cada número representa una palabra).
2. Usamos el diccionario de palabras de Keras para poder leer una reseña real y entender qué estábamos clasificando.
3. Convertimos cada reseña en un vector de ceros y unos (one-hot encoding): un 1 si la palabra aparece en la reseña, un 0 si no.

<p align="center">
  <img width="1195" height="252" alt="image" src="https://github.com/user-attachments/assets/52e022cd-67f3-4001-8d67-44d7010650c8" />
</p>
<p align="center"><em>Figura 13. Código de la función de one-hot encoding usada para vectorizar las reseñas.</em></p>

En la Figura 13 se muestra la función que convierte cada reseña en un vector de 10 000 posiciones, donde cada posición representa una palabra del diccionario y su valor pasa a 1 si esa palabra aparece en la reseña.

4. Armamos el modelo base (2 capas ocultas de 16 neuronas) y lo entrenamos 20 épocas.

<p align="center">
  <img width="1211" height="380" alt="image" src="https://github.com/user-attachments/assets/635b9f5f-b186-472c-887f-70c44ac3717b" />
</p>
<p align="center"><em>Figura 14. Código para graficar la pérdida del modelo base.</em></p>

<p align="center">
  <img width="826" height="813" alt="figura15_perdida_base" src="https://github.com/user-attachments/assets/2d494a05-1336-4032-a96f-094eeefcc291" />
</p>
<p align="center"><em>Figura 15. Pérdida del modelo base.</em></p>

En la Figura 14 se muestra el código usado para graficar la pérdida, y en la Figura 15 se observa el resultado: la curva azul (entrenamiento) baja todo el tiempo, pero la naranja (validación) baja al principio y después empieza a subir. Esto es sobreajuste: el modelo está memorizando las reseñas de entrenamiento en vez de aprender patrones generales, y por eso funciona cada vez peor con datos que no ha visto. Al evaluarlo en el set de prueba, dio un 86.1% de exactitud, con un nivel de error de 0.6.

5. Probamos un modelo más chico (4 neuronas en vez de 16) para ver si el sobreajuste cambiaba.

<p align="center">
  <img width="1296" height="403" alt="image" src="https://github.com/user-attachments/assets/622eecc2-e5b1-4933-9efb-7c66d1084737" />
</p>
<p align="center"><em>Figura 16. Código para comparar la validación del modelo original contra el modelo más pequeño.</em></p>

<p align="center">
  <img width="835" height="813" alt="figura17_comparacion_modelo_pequeno" src="https://github.com/user-attachments/assets/97d3b892-cad3-4347-a2ab-57015f39e21c" />
</p>
<p align="center"><em>Figura 17. Comparación con modelo más pequeño.</em></p>

En la Figura 16 se muestra el código de esta comparación, y en la Figura 17 se observa el resultado: con menos neuronas, el modelo tiene menos "capacidad" para memorizar, así que el sobreajuste llega más tarde y es menos pronunciado. Esto confirma que el tamaño del modelo influye directamente en qué tan fácil se sobreajusta.

6. Probamos regularización L2, que penaliza los pesos muy grandes para que el modelo no dependa demasiado de unas pocas conexiones.

<p align="center">
  <img width="1502" height="407" alt="image" src="https://github.com/user-attachments/assets/7334f2fd-4898-4f87-bdc2-81389fc6e12b" />
</p>
<p align="center"><em>Figura 18. Código del modelo con regularización L2 (kernel_regularizer).</em></p>

<p align="center">
  <img width="1312" height="436" alt="image" src="https://github.com/user-attachments/assets/43b45f02-d2da-48b0-9dbb-93d42a07556d" />
</p>
<p align="center"><em>Figura 19. Código para graficar la comparación con regularización.</em></p>

<p align="center">
  <img width="826" height="813" alt="figura20_regularizacion" src="https://github.com/user-attachments/assets/bb559097-4019-47d1-8a3f-9be09a9d96a1" />
</p>
<p align="center"><em>Figura 20. Regularización L2.</em></p>

En la Figura 18 se muestra el modelo con regularización L2 aplicada a las capas ocultas, penalizando los pesos grandes durante el entrenamiento. La Figura 19 contiene el código que grafica la comparación contra el modelo base, y el resultado se observa en la Figura 20: la curva de validación con regularización se mantiene más estable y tarda más en subir que la del modelo original, lo que confirma que penalizar los pesos grandes ayuda a retrasar el sobreajuste.

7. Probamos Dropout, que apaga aleatoriamente la mitad de las neuronas en cada paso de entrenamiento. Esto obliga a la red a no depender de neuronas específicas y a aprender de formas distintas de combinarlas [6].

<p align="center">
  <img width="1352" height="435" alt="image" src="https://github.com/user-attachments/assets/c47794ea-de53-4133-8fbf-af416f6f9638" />
</p>
<p align="center"><em>Figura 21. Código del modelo con capas de Dropout.</em></p>

<p align="center">
  <img width="1330" height="401" alt="image" src="https://github.com/user-attachments/assets/4aebafa4-bb1c-4678-a2f5-7bf5682fe62e" />
</p>
<p align="center"><em>Figura 22. Código para graficar la comparación con Dropout.</em></p>

<p align="center">
  <img width="835" height="813" alt="figura23_dropout" src="https://github.com/user-attachments/assets/255e396d-6303-42d5-afb5-f26318a64842" />
</p>
<p align="center"><em>Figura 23. Dropout.</em></p>

En la Figura 21 se muestra el modelo con capas de Dropout intercaladas entre las capas densas. La Figura 22 contiene el código que grafica la comparación, y en la Figura 23 se observa el resultado: la curva de validación con dropout se mantiene más pareja y baja durante más épocas que la del modelo original, mostrando que esta técnica también retrasa el sobreajuste, de forma parecida a la regularización L2.

8. Finalmente, usamos el modelo para predecir reseñas nuevas. Por ejemplo, la reseña número 10 dio un valor de 99.4%, es decir, el modelo está casi seguro de que es una reseña positiva.

### Lo que aprendimos

- El sobreajuste es uno de los problemas más comunes al entrenar redes, y se nota claramente cuando la curva de validación empieza a subir mientras la de entrenamiento sigue bajando.
- Hay varias formas de pelear contra el sobreajuste: achicar el modelo, regularizar los pesos, o usar dropout. Ninguna es mágica, pero todas ayudan.
- Keras permite iterar rápido: armar, entrenar y comparar varios modelos en poco tiempo, lo que es clave para poder probar estas soluciones una por una.

### Por qué es importante

Keras (parte de TensorFlow) es una de las herramientas más usadas en la industria porque baja la barrera de entrada: no hace falta ser experto en el detalle matemático para construir modelos funcionales. Además, entender el sobreajuste es fundamental en cualquier proyecto real, porque un modelo que funciona perfecto en los datos de entrenamiento pero falla con datos nuevos, en la práctica, no sirve de nada.

---

## 3. Perceptrón

### ¿Qué es y para qué sirve?

El perceptrón es el modelo más simple de red neuronal: una sola neurona que recibe varias entradas, las multiplica por unos pesos, suma todo (más un sesgo o "bias"), y aplica una función de activación para decidir una salida. Fue propuesto por Frank Rosenblatt en 1958 como un modelo simplificado de cómo el cerebro podría almacenar y organizar información [7]. Es la base conceptual de todo lo que vimos antes: una CNN o un modelo de Keras, en el fondo, son muchos perceptrones conectados entre sí en capas.

### Funciones clave que usamos

- **Suma ponderada + bias**: multiplica cada entrada por su peso, suma todo y le agrega el sesgo. Es el cálculo central del perceptrón.
- **Función escalón**: devuelve 1 si la suma ponderada es mayor o igual a 0, y 0 si es negativa. Es una decisión binaria, tipo "sí o no".
- **Función tanh**: transforma cualquier valor en un número entre -1 y 1, dando una salida más suave y gradual en vez de una decisión tajante.

<p align="center">
  <img width="1178" height="575" alt="image" src="https://github.com/user-attachments/assets/8cc4c612-2393-49e1-a321-dc1d2ff047ac" />
</p>
<p align="center"><em>Figura 24. Código de la función escalón, la función tanh y la función del perceptrón.</em></p>

En la Figura 24 se muestran las tres funciones juntas: la suma ponderada dentro de perceptron, la función escalón que convierte esa suma en una salida binaria, y la función tanh que la convierte en una salida suave entre -1 y 1.

### Lo que hicimos paso a paso

1. Simulamos un caso de sobrecalentamiento de un equipo industrial usando temperatura y vibración como entradas, con pesos y bias definidos a mano.
2. Comparamos la salida usando la función escalón contra la función tanh: la escalón dio una alerta clara (0 o 1), mientras que tanh dio un valor intermedio que también se puede interpretar como nivel de riesgo.
3. Armamos compuertas lógicas (AND, OR) ajustando los pesos y el bias del perceptrón, y probamos qué pasa con XOR.

<p align="center">
  <img width="991" height="677" alt="image" src="https://github.com/user-attachments/assets/90fd7de5-c41d-4c01-873e-e0e2473f50e2" />
</p>
<p align="center"><em>Figura 25. Código para graficar las fronteras de decisión de AND y OR.</em></p>

<p align="center">
  <img width="503" height="505" alt="figura26_and_or" src="https://github.com/user-attachments/assets/44dffb89-6b1b-46cd-98ae-fc90f091b3b0" />
</p>
<p align="center"><em>Figura 26. Fronteras de decisión AND y OR.</em></p>

En la Figura 25 se muestra el código usado para graficar estas fronteras, y en la Figura 26 se observa el resultado. Cada línea es la "frontera de decisión" de un perceptrón: todo lo que queda de un lado se clasifica como 1, y del otro lado como 0. Con AND, la línea separa el punto (1,1) del resto. Con OR, la línea separa el punto (0,0) del resto.

4. Con XOR (que da 1 solo cuando las entradas son distintas) nos encontramos con el límite real del perceptrón simple:

<p align="center">
  <img width="956" height="742" alt="image" src="https://github.com/user-attachments/assets/c0f855cd-c4ca-49e4-90d8-83797d3752df" />
</p>
<p align="center"><em>Figura 27. Código para graficar el intento de resolver XOR con un solo perceptrón.</em></p>

<p align="center">
  <img width="503" height="505" alt="figura28_xor" src="https://github.com/user-attachments/assets/902fea8a-c60a-4ce1-b49e-dbf9c898cf42" />
</p>
<p align="center"><em>Figura 28. Intento de XOR.</em></p>

En la Figura 27 se muestra el código usado, y en la Figura 28 se observa por qué falla: no existe una sola línea recta que logre separar los círculos blancos (XOR = 0) de los puntos azules (XOR = 1). Un perceptrón solo no puede resolver XOR, porque XOR no es "separable linealmente". Este fue justamente uno de los límites que señalaron Minsky y Papert en 1969, y lo que frenó por años el desarrollo de las redes neuronales, hasta que se demostró que apilando varios perceptrones en capas (justo lo que hace una red neuronal moderna) sí se puede resolver [8].

### Lo que aprendimos

- Un perceptrón es una suma ponderada más una función de activación. Todo lo demás (CNN, Keras) es una versión más grande y sofisticada de esta misma idea.
- Los pesos y el bias son los que definen el comportamiento del perceptrón: cambiándolos, la misma estructura puede comportarse como AND, como OR, o como cualquier otra regla lineal.
- Un solo perceptrón tiene límites claros: no puede resolver problemas que no se pueden separar con una línea recta, como XOR. Para eso se necesitan varias capas.

### Por qué es importante

Entender el perceptrón es entender la base de todo. Antes de usar una librería como Keras o PyTorch, conviene saber qué está pasando en el fondo: una suma ponderada, un umbral, una decisión. Además, ver con nuestros propios ojos por qué falla en XOR ayuda a entender por qué las redes reales necesitan varias capas para resolver problemas más complejos.

---

## 4. Cómo aplicaríamos esto en nuestro proyecto

Nuestro proyecto se trata de un dispositivo que monitorea el biofouling (la capa de algas y organismos que se pega en las linternas donde crecen las conchas de abanico). El dispositivo usa un sensor de proximidad para calcular el volumen de biofouling pegado a las linternas y dos cámaras ubicadas en los extremos de las linternas para monitorear también, con fotos, la cantidad de biofouling. Es importante señalar que nuestro prototipo solo mide y toma las fotos, lo que es el cálculo del volumen y el procesamiento de imágenes se harían en la nube y los resultados llegan a un aplicativo que muestra el volumen de biofouling, el porcentaje de batería y las fotos tomadas.

El problema de fondo es que el biofouling compite con las conchas de abanico por los nutrientes: mientras más biofouling se pega a las linternas, menos nutrientes y oxígeno les quedan a las conchas, y su crecimiento se vuelve más lento. Además, sin un monitoreo constante, las empresas acuícolas gastan de más en mantenimiento, mandando gente a limpiar las linternas incluso cuando todavía no es necesario. Nuestro dispositivo resuelve esto avisando solo cuándo hace falta limpiar.

Como todavía no contamos con un dataset propio de fotos submarinas de biofouling, no podemos mostrar resultados de entrenamiento como hicimos en las tres secciones anteriores. Lo que sí podemos hacer, y es lo que desarrollamos a continuación, es identificar con detalle qué función cumpliría cada pieza de la CNN, de Keras y del perceptrón dentro de nuestro sistema, de modo que este diseño quede listo para entrenarse en cuanto empecemos a recolectar fotos reales de las linternas.

### 4.1. CNN: leer las fotos de las cámaras

Las dos cámaras ubicadas en los extremos de las linternas tomarían fotos periódicas de la malla. Una CNN sería la encargada de convertir cada foto en un nivel de suciedad (por ejemplo: bajo, medio o alto), exactamente como en nuestro ejercicio separamos vidrio de plástico por su forma y textura, solo que aquí el patrón a reconocer sería la cantidad de algas y organismos adheridos a la malla.

- **Conv2D**, **ReLU** y **MaxPool2D** funcionarían igual que en nuestro ejercicio: los primeros filtros aprenderían a detectar texturas simples (la malla limpia versus la malla con algas), y los filtros de capas más profundas irían reconociendo parches de biofouling más completos, con su forma y densidad.
- **AdaptiveAvgPool2D** y la capa **Linear** final resumirían toda esa información en una sola predicción. A diferencia de nuestro ejercicio (donde la salida era binaria: vidrio o plástico), aquí la capa final probablemente tendría tres salidas con activación **softmax**, una por cada nivel de biofouling, en vez de una sola neurona.
- **Transfer learning** sería casi obligatorio en nuestro caso: como no vamos a tener miles de fotos submarinas propias, partiríamos de un modelo ya entrenado en clasificación de imágenes (como ResNet18, que usamos en el ejercicio, o una versión más liviana como MobileNet, pensando en que el procesamiento correría en la nube y conviene que sea económico) y solo reentrenaríamos la última capa con nuestras propias fotos.
- **Data augmentation** también sería clave aquí, quizás más que en el ejercicio: con pocas fotos reales, generar variaciones (rotaciones, cambios de brillo que simulen distinta turbidez del agua o distinta iluminación según la profundidad) ayudaría a que el modelo no memorice las pocas fotos que sí tenemos.
- **Grad-CAM** tendría un rol importante de confianza: nos permitiría comprobar que el modelo realmente se está fijando en la malla y el biofouling, y no en elementos irrelevantes de la foto, como peces o partículas flotando en el agua, algo especialmente importante porque de esta predicción depende avisar (o no) a un acuicultor para que vaya a limpiar.

### 4.2. Keras: armar y entrenar el modelo rápido

En el ejercicio usamos Keras para un problema de texto, pero la misma lógica de "armar la red por capas y dejar que Keras haga los cálculos" aplicaría igual de bien para entrenar la CNN de la sección anterior, ya que Keras también permite construir capas convolucionales.

- **Sequential** (o el equivalente para modelos más complejos) seguiría siendo el molde donde apilaríamos las capas Conv2D, ReLU, MaxPool2D y la capa final.
- **compile** definiría cómo se entrena el modelo: en vez del `binary_crossentropy` que usamos con IMDB, aquí usaríamos `categorical_crossentropy`, ya que tendríamos varias clases (niveles de biofouling) en vez de dos.
- **fit**, junto con un `validation_split`, entrenaría el modelo y nos permitiría ver si aparece sobreajuste, igual que vimos con las reseñas de IMDB.
- **Dropout** y **regularizers.l2** serían casi indispensables desde el principio: con pocas fotos reales de campo, el riesgo de sobreajuste sería alto, muy similar a lo que vimos con el modelo de IMDB cuando la curva de validación empezaba a subir.
- Además de lo que ya probamos, agregaríamos **EarlyStopping**, una función de Keras que detiene el entrenamiento automáticamente cuando la pérdida de validación deja de mejorar. Con un dataset chico, esto evitaría seguir entrenando de más y ayudaría a quedarnos con la versión del modelo que mejor generaliza.

### 4.3. Perceptrón: la lógica final de alerta

Una vez que el sistema tiene el volumen de biofouling que mide el sensor de proximidad y el nivel de suciedad que predice la CNN en las fotos, necesita tomar una decisión simple: ¿aviso o no aviso al acuicultor? Esa decisión final sería un perceptrón, con entradas muy concretas:

- **x₁**: el volumen de biofouling medido por el sensor de proximidad (normalizado a un rango, por ejemplo de 0 a 1).
- **x₂**: el nivel de suciedad que predice la CNN a partir de las fotos (convertido a número, por ejemplo 0 = bajo, 1 = medio, 2 = alto).
- **x₃**: el tiempo transcurrido desde la última limpieza registrada.

Con esto, la **suma ponderada** sería w₁x₁ + w₂x₂ + w₃x₃ + b, y la **función escalón** decidiría el resultado final: si la suma supera cierto umbral, el sistema genera la alerta de "linterna sucia, hay que limpiar"; si no, devuelve "todo bien, no hace falta ir". Es la misma lógica que usamos para detectar sobrecalentamiento en el ejemplo del equipo industrial, solo que aplicada a las conchas de abanico. Al principio, los pesos w₁, w₂ y w₃ probablemente los fijaríamos a mano, en conversación con los propios acuicultores (por ejemplo, dándole más peso al volumen medido por el sensor que al tiempo transcurrido). Más adelante, cuando tengamos suficientes casos reales de "aquí sí hacía falta limpiar" y "aquí no", esos pesos se podrían ajustar entrenando el perceptrón con esos datos, en vez de definirlos manualmente.

### 4.4. Por qué todo esto correría en la nube

Como el dispositivo solo se encarga de medir (con el sensor de proximidad) y tomar fotos (con las cámaras), tiene sentido que todo el procesamiento pesado —correr la CNN sobre las fotos y calcular el volumen— se haga en la nube y no dentro del dispositivo. Esto evita que el equipo gaste batería procesando imágenes bajo el agua, algo importante porque solo cuenta con pilas y un panel solar. El dispositivo enviaría los datos crudos (la lectura del sensor y las fotos) a través de sus antenas de radio, la nube correría los modelos entrenados con Keras y devolvería tanto el nivel de biofouling como la decisión final del perceptrón, ya lista para mostrarse en el aplicativo. El entrenamiento de los modelos (la parte que sí exige mucho cálculo) se haría aparte, de forma periódica, cada vez que se junte suficiente información nueva; en la nube, durante el uso normal, solo correría la inferencia, que es mucho más liviana.

---

## 5. Conclusiones

Este taller nos permitió ver el mismo tipo de problema resuelto de tres formas distintas, y eso ayudó a entender cómo se relacionan entre sí. El perceptrón nos mostró la base matemática de todo (una suma ponderada más una función de activación) y también sus límites, como la imposibilidad de resolver XOR con una sola neurona. La CNN nos mostró cómo esa misma idea, apilada en muchas capas y adaptada a filtros que recorren la imagen, permite reconocer patrones visuales, aunque también nos mostró que entrenar desde cero con pocos datos puede fallar por completo si no se usan herramientas como transfer learning. Y Keras nos permitió ver, de forma muy clara, el problema del sobreajuste y las distintas maneras de combatirlo: achicar el modelo, regularizar los pesos o usar dropout.

Más allá del ejercicio, esta actividad nos deja herramientas concretas para nuestro proyecto. Ya sabemos qué pieza de cada técnica usaríamos y para qué: la CNN para leer las fotos del biofouling, Keras para armar y entrenar ese modelo evitando el sobreajuste que ya vimos que puede aparecer con pocos datos, y un perceptrón para tomar la decisión final de alerta combinando el sensor de proximidad con lo que detecten las cámaras. También sabemos, de antemano, con qué problemas nos vamos a topar cuando tengamos fotos reales: pocos datos (por lo que transfer learning y data augmentation no serán opcionales, sino necesarios) y el riesgo de que el modelo memorice en vez de aprender (por lo que dropout y regularización deben estar presentes desde el primer entrenamiento). Contar con esto de antemano nos ahorra tener que descubrirlo por prueba y error una vez que el dispositivo esté funcionando en el mar.

---

## Referencias

[1] W. S. McCulloch and W. Pitts, "A logical calculus of the ideas immanent in nervous activity," *Bull. Math. Biophys.*, vol. 5, pp. 115–133, 1943.

[2] I. Goodfellow, Y. Bengio, and A. Courville, *Deep Learning*. Cambridge, MA, USA: MIT Press, 2016.

[3] Y. LeCun, L. Bottou, Y. Bengio, and P. Haffner, "Gradient-based learning applied to document recognition," *Proc. IEEE*, vol. 86, no. 11, pp. 2278–2324, Nov. 1998.

[4] K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2016, pp. 770–778.

[5] R. R. Selvaraju, M. Cogswell, A. Das, R. Vedantam, D. Parikh, and D. Batra, "Grad-CAM: Visual explanations from deep networks via gradient-based localization," in *Proc. IEEE Int. Conf. Comput. Vis. (ICCV)*, 2017, pp. 618–626.

[6] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, and R. Salakhutdinov, "Dropout: A simple way to prevent neural networks from overfitting," *J. Mach. Learn. Res.*, vol. 15, no. 56, pp. 1929–1958, 2014.

[7] F. Rosenblatt, "The perceptron: A probabilistic model for information storage and organization in the brain," *Psychol. Rev.*, vol. 65, no. 6, pp. 386–408, 1958.

[8] M. Minsky and S. Papert, *Perceptrons: An Introduction to Computational Geometry*. Cambridge, MA, USA: MIT Press, 1969.
