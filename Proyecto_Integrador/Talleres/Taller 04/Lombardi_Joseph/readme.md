# Lo que aprendí sobre las CNN

En la primera parte del notebook aprendí qué es una **CNN** o red neuronal convolucional. Este tipo de red se usa para analizar imágenes. Sus filtros recorren los píxeles y van detectando características como bordes, formas y texturas. También vimos que **ReLU** ayuda a la red a aprender relaciones más complejas y que **MaxPool** reduce el tamaño de la información que se está procesando.

![Esquema de la CNN que aparece al inicio del notebook](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20161807.png)

Para ponerlo en práctica usamos imágenes de **vidrio y plástico** del conjunto de datos TrashNet. Primero se cargaron las imágenes en escala de grises y se dividieron en tres grupos: **entrenamiento**, para que la red aprenda; **validación**, para revisar cómo va aprendiendo; y **prueba**, para evaluar el resultado final con imágenes que no usó durante el entrenamiento.

![Ejemplos de imágenes de vidrio y plástico mostradas en el notebook](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162024.png)

Después construimos una CNN desde cero y la entrenamos durante ocho épocas. Una época significa que el modelo pasó una vez por los datos de entrenamiento. Revisamos la **pérdida**, que indica el error del modelo, y la **exactitud**, que indica cuántas imágenes clasificó correctamente. La pérdida de entrenamiento fue bajando y la exactitud de validación llegó a **63,27 %**, pero en el conjunto de prueba obtuvo **55,03 %**. Entendí que mejorar durante el entrenamiento no siempre significa que el modelo vaya a funcionar igual de bien con imágenes nuevas.

![Gráfica de pérdida de entrenamiento de la CNN](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162411.png)

![Gráfica de exactitud y ROC-AUC de validación](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162417.png)

También revisamos una **matriz de confusión**. Esta nos deja ver los aciertos y errores por separado: cuántas imágenes de vidrio se clasificaron como vidrio, cuántas se confundieron con plástico y lo mismo para las imágenes de plástico. Así entendí mejor los resultados, porque una sola cifra de exactitud no muestra en qué clase se equivoca el modelo.

![Matriz de confusión de la CNN entrenada desde cero](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/1a9c0e53495ca54dbad3161197d47b2c07016004/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162426.png)

Luego probamos el **aumento de datos** (*data augmentation*). Consistió en aplicar pequeñas rotaciones y desplazamientos a las imágenes de entrenamiento para que la red viera más variaciones. La exactitud en prueba subió un poco, de **55,03 % a 56,38 %**. En este caso ayudó, aunque la mejora fue pequeña.

La mejora más grande llegó cuando usamos **ResNet18**. Esta red ya había sido entrenada con muchas imágenes, así que aprovechamos lo que había aprendido y adaptamos sus últimas capas para distinguir vidrio de plástico. Primero entrenamos la capa final y después ajustamos también una de sus últimas partes. Con este modelo obtuvimos **86,58 % de exactitud** en prueba. Aprendí que usar una red preentrenada puede dar mejores resultados cuando tenemos una cantidad limitada de imágenes.

Por último, usamos **Grad-CAM** para generar un mapa de calor sobre una imagen. Las zonas más resaltadas muestran qué partes influyeron más en la predicción de ResNet18. Esto sirve para observar en qué se fijó el modelo, aunque el mapa por sí solo no asegura que haya clasificado bien. Al final también guardamos los modelos para poder recuperarlos sin entrenarlos otra vez.

![Imagen original, mapa Grad-CAM y superposición](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/ce2cf0d0b135a149e0c698f04cf2ff8137af02b1/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20162820.png)

# Lo que aprendí sobre la clasificación binaria con Keras

En esta parte usamos **Keras** para crear una red neuronal que clasifica reseñas de películas de IMDB como **negativas (0)** o **positivas (1)**. Aprendí que Keras permite construir y entrenar el modelo sin tener que programar cada paso de la red desde cero.

Las reseñas primero se cargaron como secuencias de números, donde cada número representa una palabra. Después las convertimos en vectores de **0 y 1**: el 1 indica que una palabra aparece en la reseña y el 0 que no aparece. Así la red puede trabajar con el texto.

El modelo tenía **dos capas ocultas de 16 neuronas** y una capa final que daba un valor entre 0 y 1. Se entrenó durante **20 épocas**. También se separaron datos de validación para revisar cómo respondía a reseñas que no estaba usando para aprender.

Al observar la gráfica, vimos que el error en entrenamiento seguía bajando, pero el error de validación empezó a subir. Entendí que eso se llama **sobreajuste**: el modelo aprende muy bien las reseñas de entrenamiento, pero le cuesta más generalizar a otras. Al evaluarlo con los datos de prueba obtuvo **86,11 % de exactitud**.

![Gráfica de pérdida de entrenamiento y validación del modelo original — celda 87](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/5a4fb13d34ac5dbbbb6ac189aba1339bd776f650/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20203519.png)

Luego probamos un **modelo más pequeño**, con una sola capa oculta de 4 neuronas. Al comparar las gráficas, vimos que el aumento del error de validación era menos pronunciado. Aprendí que reducir el tamaño de una red puede ayudar a controlar el sobreajuste.

![Comparación de la pérdida de validación del modelo pequeño y el original — celda 94](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/5a4fb13d34ac5dbbbb6ac189aba1339bd776f650/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20203534.png)

También vimos la **regularización L2**, que penaliza los pesos muy grandes, y **dropout**, que durante el entrenamiento desactiva aleatoriamente algunas neuronas. Las dos técnicas buscan que el modelo no dependa demasiado de los ejemplos que ya conoce.

![Comparación del modelo con regularización y el original — celda 98](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/5a4fb13d34ac5dbbbb6ac189aba1339bd776f650/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20203550.png)

![Comparación del modelo con dropout y el original — celda 102](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/5a4fb13d34ac5dbbbb6ac189aba1339bd776f650/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20203603.png)

Por último, el modelo original hizo predicciones sobre las reseñas de prueba. Para una de ellas dio **0,9937**, un valor muy cercano a 1, así que la clasificó como **positiva**. Con esta práctica entendí que no basta con mirar qué tan bien aprende una red durante el entrenamiento: también hay que revisar cómo funciona con datos nuevos.

# Lo que aprendí sobre el perceptrón

En esta parte aprendí que un **perceptrón** es una neurona artificial sencilla. Recibe datos de entrada, multiplica cada uno por un **peso**, suma un **sesgo** (*bias*) y aplica una **función de activación** para obtener una salida. Los pesos indican cuánto influye cada dato en la decisión.

Primero vimos un ejemplo sobre una alerta de sobrecalentamiento. Las entradas fueron la **temperatura** y la **vibración** de un equipo industrial. Con los pesos y el sesgo elegidos en el código, la suma dio **−5**. Como el resultado fue negativo, la función escalón devolvió **0**, es decir, **sin alerta**. También probamos la función **tanh**: esta dio un valor cercano a **−1** y llegó a la misma decisión. Así entendí que distintas funciones de activación pueden dar salidas diferentes a partir de la misma suma.

Después probamos el perceptrón con entradas de **0 y 1**. Al cambiar los pesos y el sesgo, conseguimos que se comportara como una compuerta **AND**, que da 1 solo cuando las dos entradas son 1, y como una compuerta **OR**, que da 1 cuando al menos una entrada es 1. También vimos que elegir otros pesos cambia la decisión: una de las configuraciones que probamos ya no se comportaba como AND.

![Gráfico con los puntos y las fronteras de decisión de AND y OR — celda 128](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/5a4fb13d34ac5dbbbb6ac189aba1339bd776f650/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20203621.png)

Por último, revisamos **XOR**, que da 1 cuando las dos entradas son diferentes. En el gráfico vimos que sus resultados no se pueden separar con una sola línea. Por eso, **un solo perceptrón no puede resolver XOR**, pero una red con varias neuronas y una capa de salida sí puede hacerlo. Esa fue la idea que más me ayudó a entender por qué las redes neuronales usan varias capas.

![Gráfico que muestra por qué XOR necesita más de una frontera de decisión — celda 130](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/5a4fb13d34ac5dbbbb6ac189aba1339bd776f650/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-09-22%20203629.png)
