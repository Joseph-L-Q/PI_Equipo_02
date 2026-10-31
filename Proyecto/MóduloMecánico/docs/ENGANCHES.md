# Enganches al aro: tres mecanismos probados en impresion 3D

Bloque B, 30/10. Investigacion previa a los prototipos P1 a P4. El aro de la linterna de prueba (Ø200) lleva una varilla de `aro.seccion`
(hoy **8 mm, estimado**: medir con el aro real); los numeros de abajo salen de esa cifra y se recalculan con ella
(`gancho.c` = holgura, pared, asiento; `proto.snap`; `proto.abrazadera`). La correa de seguridad es de 25 mm (`correa.ancho`).
Los modelos de las fuentes son de aficionados y sus notas de impresion no son datos de laboratorio: sirven para elegir una
geometria y una orientacion de capas, no para dar un factor de seguridad. El FS sale del FEM de `docs/PROTOTIPOS.md`.

Geometria de referencia (V2, gancho en C): radio interior `ri = 8/2 + 0.4 = 4.4 mm`, pared 6, radio exterior `ro = 10.4 mm`; el gancho
cuelga de la varilla y la carga del nodo (150 N de manipulacion en una capsula, un solo gancho) aprieta la varilla contra la corona de la C.

## 1. Abrazadera de media luna con tornillo

**Fuentes.** Abrazaderas de tubo en dos mitades atornilladas de Printables y MakerWorld:
[pipe clamp 40/45 mm para tornillo M6, PETG/ABS/ASA](https://makerworld.com/models/2007848),
[clamp para tubo de 75 mm con nidos de tuerca impresos para M4](https://makerworld.com/models/2913150),
[QuickLock pipe clamp](https://makerworld.com/es/models/3109003-quicklock-pipeclamp),
[Narrow tube GoPro clamp](https://www.printables.com/model/509740-narrow-tube-gopro-clamp). Un comentario de un modelo de MakerWorld con
tornillos impresos advierte que los tornillos y tuercas impresos fallan a muchos usuarios: la recomendacion repetida es **tornilleria metalica**.

**Por que encaja.** Es el unico de los tres que se abre y se cierra sin deformar el plastico: la varilla entra sin esfuerzo y el cierre lo da el tornillo,
asi que el FS no depende de una flexion repetida. Cada media luna es una pieza pequena y de capas continuas.

**Adaptacion al aro (`proto.abrazadera`, usada en P3 y P4).** La C del gancho pierde su mitad inferior y conserva una oreja de 6 mm de espesor y 8 mm
de salida a cada lado, a la altura del centro de la varilla (z = 0). La media luna **M9c** (anillo `ri`/`ro`, 12 mm de ancho) tiene la oreja gemela debajo.
Un M4 vertical por lado (agujero de paso 4.2) las une; la tuerca hexagonal (AF 7 + 0.4 de holgura) queda en un nido de la oreja del gancho, asi que se aprieta
por debajo con una sola llave. Con `aro.seccion` distinta basta cambiar la holgura y la pared de `gancho.c`: las orejas siguen a `ro`.
La oreja llega a `ro + 8 = 18.4 mm` del eje: queda a 1.6 mm de la capsula (que empieza a 20 mm del eje) y el chequeo de interferencias lo verifica.

**Correa de 25 mm.** No pasa por la abrazadera: el gancho se cierra con el tornillo y la media luna es mas ancha que la varilla en ambos lados, asi que la
correa deja de hacer falta para que el nodo no se levante. La ranura de correa (3 x 25 mm en el alma) existe solo en el gancho C de P2 (`gancho.correa = True`).
La red de la linterna cuelga de la varilla y pasa por la media luna: el chequeo de la red se omite para M9c (es tela, no se verifico con la red real).

**Impresion.** M9c de plano sobre las orejas (las capas quedan en el plano del anillo: la tension del tornillo va a lo largo de la oreja y la carga de la varilla va en el
plano de capas). Orejas de 6 mm = 15 capas de 0.4 en el eje del tornillo; usar 5 perimetros. No imprimir el tornillo.

## 2. Clip snap-fit para tubo

**Fuentes.** Guias de diseno de snap-fits impresos: [Guide to 3D Printed Snap Fits (Unionfab)](https://www.unionfab.com/blog/2025/06/3d-print-snap-fit),
[Snap-fit joints: how to design clips that work (Sovol)](https://www.sovol3d.com/blogs/news/3d-printed-snap-fit-joints-how-to-design-clips-that-work),
[Designing snap-fit parts for FPV drones (UAVmodel)](https://blog.uavmodel.com/?p=4638),
[Snap-fit joint test prints, eight versions (Printables)](https://www.printables.com/model/151102-snap-fit-joint-test-prints-eight-versions),
la guia clasica del MIT citada por ellas (Snap-Fit Joints for Plastics) y [Fictiv](https://fictiv.com/?p=1238) para la ecuacion de deformacion del voladizo.
Puntos que se repiten: el voladizo se imprime **en el plano XY de la cama**, nunca subiendo en Z; chaflan de entrada; radio minimo de 1 mm en la raiz;
brazo de 0.8 a 1.5 veces la pared; PETG tolera una deformacion de borde del orden de 3 a 4 %, por debajo de eso, con probeta propia.
(La cifra de PETG viene de un solo blog: verificar con una probeta.)

**Por que encaja.** Sin tornilleria ni pieza extra: el gancho se hunde sobre la varilla desde arriba y se retiene solo.
Es el que menos material y menos piezas usa (P1).

**Adaptacion al aro (`proto.snap`, usada en P1).** Los dos cuernos de la C (que ya bajaban 9.4 mm bajo el centro de la varilla) pasan a ser dos brazos curvos de
**2.4 mm** de espesor (0.8 a 1.5 veces la pared de 3.5 a 6), libres desde la raiz a z = +5 mm: se quita la pared exterior bajo la raiz. Cada brazo lleva una **pestana**
hacia adentro que deja la boca en **6.8 mm** (85 % del Ø8): cada brazo se abre 0.6 mm para pasar la varilla. Deformacion de borde estimada con la viga en voladizo
(e = 1.5 t d / L^2, t = 2.4, d = 0.6, L ~ 9 mm): **~2.7 %**, dentro del limite citado. Con otra `aro.seccion` la apertura es 0.85 del diametro y la pestana `ri - apertura/2`.
Los brazos no bajan mas de 5 mm bajo el eje: la red de la linterna cuelga de la varilla y mas abajo chocaria.

**Correa de 25 mm.** P1 no la usa; el snap retiene contra el levantado. Si se quiere una correa de refuerzo, pasa por la ranura de 3 x 25 que el gancho C de P2 conserva.

**Impresion.** Gancho **de costado** (eje de la varilla vertical: la C dibujada en el plano de las capas, ya es la orientacion `X+90` del riel). Los brazos
quedan asi en el plano XY y sus capas corren a lo largo del brazo. 5 perimetros. Sin probeta no se debe asumir la fuerza de insercion.

## 3. Mosqueton con puerta y pestillo impresos

**Fuentes.** Mosquetones impresos de MakerWorld y Printables: [Flexi Carabiner, print-in-place, PETG](https://makerworld.com/models/1185113),
[PAX ergonomic print-in-place](https://makerworld.com/models/1905619), [Classic spring carabiner](https://makerworld.com/models/3033772),
[FlexGate, puerta con resorte de lamina](https://makerworld.com/models/3303082), [Click-Lock, sin bisagra](https://makerworld.com/models/1318670),
[Snap Clip Carabiner](https://makerworld.com/models/2632629), [Sleek Carabiner](https://www.printables.com/model/1032039-sleek-carabiner-travel-essential).
Coinciden en: PETG antes que PLA (el PLA se deforma o se agrieta en la bisagra), imprimir **plano con la puerta hacia arriba**, y ajustar la holgura de la puerta
a la impresora. Un comentario del [Asymmetric Carabiner](https://www.myminifactory.com/object/3d-print-18181) cuenta una puerta de PETG que se agrieto en la base: el pestillo
es la pieza que falla.

**Por que encaja.** Cierra la boca del gancho y se abre con una mano sobre el aro, sin herramienta y sin un tornillo que perder.

**Adaptacion (no construida en este bloque).** La boca del gancho es de 8.8 mm y la puerta serviria como lamina de 2 mm de PETG en voladizo de ~25 mm con una espiga
de 3 mm; la boca debe ser de al menos `aro.seccion + 2`. Pasaria el hueco de la correa de 25 mm igual que el gancho C.
**Decision: no se implementa en P1 a P4.** Efecto de elegirla mas adelante: +1 pieza impresa pequena y +1 pasador por gancho (+2 piezas por nodo), un pestillo que es el
punto de falla conocido segun las fuentes, y ninguna ventaja sobre el snap en la carga de 150 N. Se deja documentada para si el snap de P1 no pasa la probeta.

## Que se uso en cada prototipo

| Prototipo | Gancho | Razon |
|---|---|---|
| P1 minimo | snap-fit | cero tornilleria, menos piezas |
| P2 robusto | C con ranura de correa (V2) | la unica referencia ya ensayada por FEM, mas la correa |
| P3 monocasco, P4 estetico | abrazadera de media luna | se cierra con tornillo; no depende de la flexion del PETG |
