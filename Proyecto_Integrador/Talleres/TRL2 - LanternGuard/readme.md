
# LanternGuard

## TRL 2 — Formulación conceptual de la propuesta tecnológica

<h2 align="center">Información académica</h2>

<div align="center">
  <table>
    <thead>
      <tr>
        <th align="center">Campo</th>
        <th align="center">Información</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Proyecto</strong></td>
        <td align="center">LanternGuard</td>
      </tr>
      <tr>
        <td><strong>Curso</strong></td>
        <td align="center">Proyecto Integrador</td>
      </tr>
      <tr>
        <td><strong>Docentes</strong></td>
        <td>
          <ul>
            <li>Umbert Lewis de la Cruz Rodriguez</li>
            <li>Renzo Jose Chan Rios</li>
            <li>Maria Angelica Rejas Nuñez</li>
            <li>Harry Anderson Rivera Tito</li>
          </ul>
        </td>
      </tr>
      <tr>
        <td><strong>Integrantes</strong></td>
        <td>
          <ul>
            <li>Antezana De la Cruz, María</li>
            <li>Santamaria Huaytan, Gabriela</li>
            <li>Bustos Montañez, Melissa</li>
            <li>Lombardi Quispe, Joseph</li>
            <li>Palacios Tanaka, Yoichi</li>
          </ul>
        </td>
      </tr>
      <tr>
        <td><strong>Periodo académico</strong></td>
        <td align="center">2026</td>
      </tr>
    </tbody>
  </table>
</div>

---

## Presentación

LanternGuard es una propuesta tecnológica orientada al monitoreo periódico de la bioincrustación en las mallas de las linternas utilizadas para el cultivo suspendido de concha de abanico (*Argopecten purpuratus*). El sistema contempla la integración de cámaras submarinas, sensores complementarios y tecnologías de comunicación para obtener información visual sobre el estado de estas estructuras.

La presente propuesta se formula considerando los indicadores referenciales del nivel de madurez tecnológica TRL 2 establecidos en el Anexo 1 de la Directiva N.º 001-2022-CONCYTEC-P [1](#ref-1).

---

## 1. Artículos científicos relacionados con la propuesta tecnológica

### 1.1. Bioincrustación en linternas y necesidad de monitoreo

Loayza-Aguilar et al. [2](#ref-2) investigaron el efecto del recambio de linternas utilizadas en el cultivo suspendido de concha de abanico (*Argopecten purpuratus*) en la bahía de Samanco, Perú. Los investigadores compararon linternas reemplazadas durante la etapa final del cultivo con aquellas mantenidas hasta la cosecha. Los resultados mostraron una reducción del 64,6 % en el peso de la bioincrustación y una mejora del 10,8 % en la supervivencia de los organismos, bajo las condiciones evaluadas. Este estudio constituye un antecedente directamente relacionado con LanternGuard, ya que demuestra la importancia del manejo de la bioincrustación en las estructuras de cultivo. Sin embargo, la investigación no evaluó sistemas de monitoreo mediante cámaras submarinas ni estableció indicadores visuales para determinar cuándo realizar el mantenimiento.

De manera complementaria, Chen et al. [3](#ref-3) analizaron mediante ensayos con modelos físicos los efectos de diferentes tipos de bioincrustación artificial sobre las características hidrodinámicas de paneles de redes acuícolas. Los resultados evidenciaron que la acumulación de incrustaciones puede incrementar considerablemente la resistencia al flujo y modificar las condiciones de circulación del agua a través de las redes. Aunque el estudio no se realizó específicamente en linternas de concha de abanico, proporciona fundamentos científicos para considerar la obstrucción de las aberturas como una característica relevante en el seguimiento de estas estructuras.

En conjunto, ambas investigaciones respaldan la importancia del monitoreo periódico de la bioincrustación en las estructuras de cultivo. A partir de estos antecedentes, LanternGuard propone utilizar imágenes submarinas para estimar el porcentaje de cobertura visible por organismos incrustantes en regiones seleccionadas de las mallas, generando información que contribuya a la planificación de inspecciones y actividades de limpieza.

### 1.2. Análisis de imágenes para el monitoreo visual de bioincrustación

Qiu, Pakrashi y Ghosh [4](#ref-4) desarrollaron un procedimiento para evaluar el estado de redes acuícolas mediante imágenes submarinas. Su método incluye la selección de regiones de interés, la corrección de distorsión y visibilidad, la segmentación de organismos incrustantes y el análisis de las aberturas de las redes para estimar su porcentaje de bloqueo. Este antecedente aporta fundamentos para LanternGuard al demostrar la utilidad del procesamiento digital de imágenes en la identificación y análisis de bioincrustación. Su metodología constituye una referencia para formular un procedimiento orientado a estimar la cobertura visible de organismos incrustantes en las mallas.

De manera complementaria, Cappaert et al. [5](#ref-5) desarrollaron una herramienta de procesamiento de imágenes para estimar la oclusión en redes utilizadas en la acuicultura de salmones. Su procedimiento emplea técnicas de segmentación basadas en aprendizaje profundo para diferenciar regiones de agua y no agua, considerando además el área ocupada por la estructura de la malla. Los autores reportaron una precisión media de prueba cercana al 93,5 % en la clasificación de píxeles de las imágenes evaluadas. Este estudio proporciona fundamentos para la identificación y clasificación de elementos presentes en fotografías submarinas, aspectos relevantes para el análisis visual propuesto en LanternGuard.

A partir de estos antecedentes, LanternGuard propone analizar fotografías submarinas para identificar las zonas visibles cubiertas por organismos incrustantes y estimar su proporción respecto al área de referencia seleccionada para el análisis. Para ello, se contempla la delimitación de regiones de interés, la diferenciación entre los organismos y la estructura de la malla, así como el tratamiento de variaciones de iluminación, turbidez y perspectiva. Estos criterios permitirán orientar la definición conceptual del procedimiento de procesamiento de imágenes.

### 1.3. Sustento para la arquitectura de adquisición y comunicación

Augustin et al. [6](#ref-6) analizaron las características y el desempeño de la tecnología LoRa, destacando su capacidad de comunicación a largas distancias y su bajo consumo energético, aunque con limitaciones en la velocidad de transmisión de datos. De manera complementaria, Jebril et al. [7](#ref-7) investigaron la transmisión de imágenes mediante LoRa, utilizando la división de la información en paquetes para superar las restricciones del enlace inalámbrico. Ambos estudios proporcionan fundamentos para la arquitectura de comunicación propuesta en LanternGuard, que contempla el almacenamiento temporal de fotografías, su transmisión mediante paquetes de datos y la posterior reconstrucción de los archivos en la estación receptora terrestre. No obstante, la velocidad efectiva y el alcance de comunicación dependerán de las características y condiciones del enlace utilizado.

Respecto a la adquisición de información, la documentación técnica de Arducam [8](#ref-8) describe las características de las cámaras Mega de 5 MP con interfaz SPI, seleccionadas para la captura de imágenes submarinas. Asimismo, DFRobot [9](#ref-9) especifica que el sensor ultrasónico SEN0598 permite medir distancias bajo el agua en un rango nominal de 2 a 300 cm mediante comunicación UART. Por su parte, STMicroelectronics [10](#ref-10) describe el acelerómetro triaxial LIS3DH, que permite registrar aceleraciones y movimientos. Estos componentes sustentan la selección tecnológica de LanternGuard, donde las cámaras permitirán observar regiones de las mallas, mientras que el sensor ultrasónico y el acelerómetro proporcionarán mediciones complementarias para caracterizar las condiciones de captura.

### 1.4. Síntesis de la aplicación de los antecedentes

<p align="center"><strong>Tabla 1. Relación entre los antecedentes científicos y su aplicación en LanternGuard</strong></p>

| Fuente | Evidencia científica documentada | Aplicación conceptual en LanternGuard |
|---|---|---|
| Loayza-Aguilar et al. [2](#ref-2) | Evaluaron los efectos del recambio de linternas sobre la bioincrustación y la supervivencia de *Argopecten purpuratus* en Samanco. | Sustentar la necesidad del monitoreo periódico de las linternas para apoyar las decisiones de mantenimiento. |
| Chen et al. [3](#ref-3) | Analizaron los efectos de la bioincrustación sobre el comportamiento hidrodinámico de redes acuícolas. | Sustentar la importancia del seguimiento de la bioincrustación acumulada en las mallas. |
| Qiu et al. [4](#ref-4) | Desarrollaron un método de análisis de imágenes submarinas para estimar el bloqueo de aberturas de redes. | Considerar técnicas de segmentación para identificar organismos incrustantes en imágenes submarinas. |
| Cappaert et al. [5](#ref-5) | Desarrollaron un procedimiento de segmentación de imágenes para estimar la oclusión de redes salmoneras. | Orientar la diferenciación visual entre organismos incrustantes, estructura de la malla y regiones de agua. |
| Augustin et al. [6](#ref-6) y Jebril et al. [7](#ref-7) | Estudiaron las características y limitaciones de LoRa, así como alternativas para transmitir imágenes mediante esta tecnología. | Sustentar una arquitectura de almacenamiento temporal, fragmentación y reconstrucción de fotografías. |

<p align="center"><em><strong>Nota.</strong> Elaboración propia a partir de los antecedentes científicos revisados en los apartados 1.1, 1.2 y 1.3.</em></p>

Las investigaciones revisadas proporcionan fundamentos científicos y tecnológicos para la formulación de LanternGuard. Los estudios sobre bioincrustación justifican la importancia de monitorear su acumulación en las estructuras de cultivo, mientras que los métodos de procesamiento de imágenes aportan antecedentes para identificar y analizar visualmente organismos incrustantes. Asimismo, las investigaciones sobre comunicación LoRa respaldan la arquitectura propuesta para transmitir la información capturada. A partir de estos antecedentes, LanternGuard plantea integrar tecnologías existentes en un sistema de monitoreo periódico orientado a estimar la cobertura visible de bioincrustación en las mallas de las linternas utilizadas para el cultivo de *Argopecten purpuratus*.

---

## 2. Análisis preliminar de patentabilidad y protección

### 2.1. Criterios de evaluación

La Decisión 486 de la Comunidad Andina [11](#ref-11), que establece el Régimen Común sobre Propiedad Industrial, señala que una patente de invención debe cumplir tres requisitos: novedad (artículo 16), nivel inventivo (artículo 18) y aplicación industrial (artículo 19). Asimismo, el artículo 81 contempla la protección mediante modelos de utilidad cuando una nueva forma, configuración o disposición de elementos de un objeto permite mejorar su funcionamiento, utilización o fabricación, o proporciona una ventaja o efecto técnico.

A partir de estos criterios, el análisis de patentabilidad de LanternGuard se orienta a identificar posibles características diferenciadoras frente a las tecnologías existentes y evaluar si su configuración podría ofrecer una ventaja técnica. Para ello, se revisan publicaciones de patentes relacionadas con sistemas de inspección submarina, monitoreo de redes acuícolas y detección de bioincrustación.

### 2.2. Publicaciones de patentes relacionadas con la propuesta

Se realizó una búsqueda exploratoria en Google Patents utilizando términos relacionados con cámaras para acuicultura, monitoreo de redes sumergidas, inspección de mallas y detección de bioincrustación. Se identificaron cuatro publicaciones de patentes relacionadas con la propuesta tecnológica de LanternGuard, cuyas características permiten establecer semejanzas y diferencias respecto al sistema planteado. La Tabla 2 presenta los principales antecedentes encontrados.

<p align="center"><strong>Tabla 2. Comparación de publicaciones de patentes relacionadas con LanternGuard</strong></p>

| Documento | Tecnología descrita | Comparación con LanternGuard |
|---|---|---|
| WO2024072597A1 [12](#ref-12) | Sistema de montaje ajustable de cámaras para modificar su campo de visión en entornos de acuicultura. | Ambas propuestas utilizan cámaras; LanternGuard contempla cámaras orientadas hacia regiones de las mallas, sin incorporar el mecanismo de ajuste descrito en la publicación. |
| US20240130336A1 [13](#ref-13) | Dispositivo de monitoreo de redes sumergidas mediante impulsos mecánicos y señales relacionadas con la tensión de las redes. | Comparte el monitoreo de estructuras acuícolas, pero utiliza un principio de medición diferente del análisis de imágenes propuesto en LanternGuard. |
| NO20240761A1 [14](#ref-14) | Sistema de inspección de redes acuícolas mediante un dispositivo submarino móvil, captura de imágenes y posicionamiento ultrasónico. | Comparte el uso de imágenes y tecnología ultrasónica, pero LanternGuard propone inspecciones periódicas mediante un módulo situado respecto a una linterna de cultivo, sin utilizar un vehículo móvil para recorrer las redes. |
| US20200326279A1 [15](#ref-15) | Dispositivo de detección no invasiva de incrustaciones en sistemas acuáticos mediante técnicas ópticas de medición de superficies. | Aborda la detección no invasiva de incrustaciones mediante técnicas ópticas, mientras que LanternGuard propone estimar la cobertura visible por bioincrustación mediante fotografías submarinas. |

<p align="center"><em><strong>Nota.</strong> Elaboración propia a partir de las publicaciones consultadas en Google Patents [12](#ref-12)–[15](#ref-15).</em></p>

La publicación noruega NO20240761A1 pertenece a la misma familia de patentes que WO2023108307A1, por lo que ambas se consideran un mismo antecedente tecnológico [14](#ref-14). Asimismo, la solicitud estadounidense US20240130336A1 dio lugar a la patente concedida US12426577B2 [13](#ref-13). Estas relaciones permiten identificar las publicaciones vinculadas, aunque no constituyen una evaluación completa de su situación jurídica en todos los territorios.

La comparación muestra que existen tecnologías orientadas al monitoreo submarino, la inspección de redes y la detección de bioincrustación. Frente a estos antecedentes, LanternGuard plantea una configuración dirigida específicamente al seguimiento periódico de las mallas de linternas utilizadas en el cultivo de *Argopecten purpuratus*, mediante la integración de captura de imágenes, mediciones complementarias y comunicación entre un módulo sumergido y una boya de superficie. Esta diferenciación constituye una característica de la propuesta que deberá considerarse en el análisis preliminar de patentabilidad, sin que por sí sola demuestre novedad o nivel inventivo.

### 2.3. Evaluación preliminar de novedad, nivel inventivo y aplicación industrial

**Novedad.** La configuración propuesta de LanternGuard integra dos cámaras submarinas, sensores complementarios, una boya de superficie, comunicación RS-485 y LoRa, y procesamiento de imágenes para estimar la cobertura visible de bioincrustación en las mallas de linternas utilizadas para el cultivo de *Argopecten purpuratus*. Esta combinación específica no se identificó en las cuatro publicaciones de patentes examinadas. Sin embargo, sus principales componentes y funciones ya se encuentran presentes en tecnologías existentes relacionadas con la inspección submarina, el monitoreo de redes acuícolas y la detección de bioincrustación. Por ello, la búsqueda realizada no permite establecer de manera definitiva la novedad de la propuesta, siendo necesario ampliar la revisión del estado de la técnica [11](#ref-11)–[15](#ref-15).

**Nivel inventivo.** La integración de cámaras, microcontroladores, sensores comerciales y tecnologías de comunicación conocidas podría considerarse una solución previsible para una persona especializada en este campo tecnológico. Para determinar si LanternGuard presenta nivel inventivo, sería necesario identificar características técnicas de su configuración que no resulten evidentes a partir de las tecnologías existentes. Entre los aspectos que podrían analizarse se encuentran la disposición de los componentes para observar regiones específicas de las mallas y el sistema de montaje del dispositivo sumergido. En esta etapa no se dispone de evidencia suficiente para establecer que dichas características cumplen este requisito [11](#ref-11).

**Aplicación industrial.** LanternGuard presenta una aplicación potencial en el sector acuícola, específicamente en el monitoreo de las linternas utilizadas para el cultivo suspendido de conchas de abanico. Su arquitectura contempla componentes electrónicos y estructuras que podrían fabricarse e integrarse para obtener información sobre el estado visible de las mallas y apoyar la planificación del mantenimiento. Por tanto, la propuesta presenta una posible aplicación industrial conforme al artículo 19 de la Decisión 486, aunque este criterio no implica por sí solo el cumplimiento de los requisitos de novedad y nivel inventivo [11](#ref-11).

### 2.4. Posibles vías de protección

A partir del análisis realizado, LanternGuard podría considerar diferentes mecanismos de protección de propiedad intelectual. Una eventual patente de invención requeriría ampliar la búsqueda del estado de la técnica y verificar el cumplimiento de los requisitos de patentabilidad. Asimismo, podría evaluarse la protección de una configuración mecánica mediante un modelo de utilidad, siempre que presente una nueva disposición de elementos que proporcione una ventaja técnica, conforme al artículo 81 de la Decisión 486 de la Comunidad Andina [11](#ref-11).

Por otro lado, el software original desarrollado para la adquisición y el procesamiento de imágenes podría protegerse mediante derecho de autor. La viabilidad de estas alternativas dependerá de las características definitivas de la propuesta y de las condiciones de titularidad aplicables.

---

## 3. Perfil o propuesta del proyecto

### 3.1. Problema, propósito y alcance

En el cultivo suspendido de concha de abanico (*Argopecten purpuratus*), las mallas de las linternas están expuestas a la acumulación de organismos incrustantes que pueden obstruir progresivamente sus aberturas. Las investigaciones sobre bioincrustación han evidenciado la importancia de este fenómeno en las estructuras acuícolas y su relación con las condiciones de cultivo y circulación del agua [2](#ref-2), [3](#ref-3). Ante esta problemática, se identifica la necesidad de disponer de información visual periódica y comparable sobre el estado de las mallas para apoyar la planificación de las inspecciones y actividades de mantenimiento.

**Objetivo general.** Formular conceptualmente un sistema de monitoreo periódico de la bioincrustación en las mallas de las linternas utilizadas para el cultivo de *Argopecten purpuratus*, mediante la captura de imágenes submarinas y mediciones complementarias, con la finalidad de estimar el porcentaje de cobertura visible por organismos incrustantes en las regiones observadas y proporcionar información que apoye las decisiones de inspección y mantenimiento.

**Alcance.** La propuesta se centra en la estimación de la cobertura visible de bioincrustación en las regiones de malla capturadas por las cámaras, por lo que sus resultados no representarán necesariamente el estado completo de cada linterna ni la cantidad total de organismos incrustantes presentes. Asimismo, LanternGuard está orientado al monitoreo de la bioincrustación y no contempla realizar actividades de limpieza.

### 3.2. Arquitectura funcional propuesta

LanternGuard se organiza en cuatro elementos principales: módulo sumergido, boya de superficie, estación receptora terrestre y servicio de procesamiento de imágenes. El módulo sumergido se conecta con la boya mediante un cable umbilical que permite establecer la comunicación RS-485. Desde la boya, la información se transmitiría hacia la estación terrestre mediante tecnología LoRa. Posteriormente, la estación gestionaría el envío de los archivos a un servicio de procesamiento de imágenes a través de una conexión a internet.

<p align="center"><strong>Tabla 3. Componentes y funciones de la arquitectura conceptual de LanternGuard</strong></p>

| Elemento | Composición conceptual | Función prevista |
|---|---|---|
| **Módulo sumergido** | ESP32-S3-DevKitC-1-N16R8, dos cámaras Arducam Mega 5 MP, sensor ultrasónico SEN0598, acelerómetro LIS3DH, microSD, iluminación y transceptor MAX3485. Integración mediante placa universal perforada. | Capturar imágenes submarinas, registrar mediciones complementarias, almacenar temporalmente la información y transferirla a la boya mediante RS-485. |
| **Boya de superficie** | Heltec WiFi LoRa 32 V3, RTC DS3231, transceptor MAX3485 y PCB personalizada. Se contempla alimentación mediante panel solar, batería y circuito de gestión energética, además de almacenamiento temporal. | Coordinar las inspecciones programadas, recibir información del módulo sumergido, gestionar su almacenamiento temporal y transmitirla hacia tierra mediante LoRa. |
| **Estación receptora terrestre** | Receptor Heltec WiFi LoRa 32 V3 y equipo informático con acceso a internet. | Recibir los datos transmitidos por LoRa, reconstruir los archivos y gestionar su envío al servicio de procesamiento. |
| **Servicio de procesamiento de imágenes** | Sistema de almacenamiento y procesamiento digital de imágenes, por configurar. | Procesar las fotografías recibidas, identificar las regiones cubiertas por organismos incrustantes, estimar el porcentaje de cobertura visible de bioincrustación y presentar los resultados del monitoreo. |

<p align="center"><em><strong>Nota.</strong> Elaboración propia a partir de la arquitectura conceptual propuesta para LanternGuard.</em></p>

La selección de los componentes electrónicos se sustenta en la documentación técnica de sus fabricantes. Espressif Systems [16](#ref-16) describe las características del ESP32-S3-DevKitC-1, Arducam [8](#ref-8) documenta las cámaras Mega de 5 MP, DFRobot [9](#ref-9) especifica el funcionamiento del sensor ultrasónico SEN0598 y STMicroelectronics [10](#ref-10) presenta las características del acelerómetro LIS3DH. Asimismo, Analog Devices documenta el transceptor MAX3485 [17](#ref-17) y el reloj de tiempo real DS3231 [18](#ref-18), mientras que Heltec Automation [19](#ref-19) proporciona las especificaciones de la placa WiFi LoRa 32 V3.

La arquitectura contempla dos soluciones de integración electrónica. En la boya de superficie se propone utilizar una placa de circuito impreso (PCB) personalizada, cuyo diseño electrónico y distribución de pistas han sido elaborados. Por su parte, los componentes del módulo sumergido se integrarán mediante una placa universal perforada, utilizando como referencia su esquemático de conexiones. Ambas configuraciones se complementan para desarrollar las funciones de adquisición, comunicación y procesamiento previstas en LanternGuard.

### 3.3. Secuencia prevista de operación e indicador

LanternGuard contempla realizar inspecciones periódicas cada 15 días, con una duración aproximada de cinco minutos para la captura de imágenes y el registro de mediciones. La programación temporal se gestionaría mediante el reloj de tiempo real (RTC) ubicado en la boya de superficie. Durante cada inspección, el módulo sumergido utilizaría dos cámaras orientadas hacia diferentes regiones de las mallas, mientras que el sensor ultrasónico y el acelerómetro registrarían mediciones complementarias de distancia y movimiento.

Las fotografías y mediciones obtenidas se almacenarían inicialmente en una tarjeta microSD del módulo sumergido y posteriormente se transferirían a la boya mediante comunicación RS-485. Desde la boya se contempla el envío de fotografías hacia la estación receptora terrestre mediante tecnología LoRa, considerando su almacenamiento temporal y la posible compresión y fragmentación de los archivos. La estación terrestre se encargaría de reconstruir las fotografías y gestionar su transferencia al servicio de procesamiento de imágenes. Los cinco minutos previstos corresponden únicamente a la adquisición de información y no incluyen las etapas posteriores de transferencia y transmisión.

El indicador principal de LanternGuard será el porcentaje estimado de cobertura visible por bioincrustación en regiones seleccionadas de las mallas. Para su obtención, se propone analizar las fotografías mediante técnicas de procesamiento de imágenes que permitan identificar las zonas ocupadas por organismos incrustantes y diferenciarlas de la estructura de la malla. El cálculo se planteará a partir de la proporción de área visible cubierta por bioincrustación respecto al área de referencia definida para cada región de análisis. Asimismo, se contempla comparar regiones equivalentes en inspecciones sucesivas, considerando las variaciones de iluminación, turbidez y perspectiva. La definición del procedimiento se apoyará en los antecedentes de análisis de imágenes submarinas [4](#ref-4), [5](#ref-5).

Las mediciones del sensor ultrasónico permitirían obtener información de distancia respecto a una superficie de referencia, mientras que el acelerómetro aportaría datos sobre el movimiento del módulo durante la captura. Estas variables complementarían el análisis visual, sin sustituir la estimación de cobertura obtenida mediante las fotografías.

### 3.4. Representación del modelado tridimensional

Como parte del diseño conceptual de LanternGuard, se desarrolló un modelo tridimensional que representa la configuración estructural del módulo sumergido, la boya de superficie y su integración mediante un cable umbilical. El modelado permite visualizar la distribución de los componentes, los sistemas de soporte y la disposición física de los elementos que conforman la propuesta tecnológica.

#### 3.4.1. Diseño tridimensional del módulo sumergido

El módulo sumergido de LanternGuard se diseñó para posicionarse sobre la linterna de cultivo y realizar la captura periódica de imágenes submarinas y mediciones complementarias. Su estructura presenta un compartimento central destinado a alojar la electrónica de control, incluyendo el ESP32-S3-DevKitC-1-N16R8, los componentes de comunicación y almacenamiento, así como las conexiones de los sensores.

El diseño incorpora dos brazos laterales que permiten ubicar las cámaras Arducam Mega de 5 MP con diferentes orientaciones hacia regiones de las mallas. Asimismo, se contempla la integración del sensor ultrasónico SEN0598 para registrar distancias y del acelerómetro LIS3DH para obtener información sobre el movimiento del dispositivo durante las inspecciones.

Una característica importante del modelo es su sistema de sujeción, conformado por elementos de enganche que permiten fijar el módulo a la estructura de la linterna. Esta disposición busca mantener una posición de observación consistente y reducir los desplazamientos que podrían modificar los ángulos de captura entre inspecciones.

En la representación se incluye un cilindro gris que simula la linterna de cultivo y permite visualizar el acoplamiento del dispositivo. Este cilindro no forma parte de las piezas que se fabricarán, ya que se utiliza únicamente como referencia para representar la instalación del módulo. Las piezas estructurales del dispositivo destinadas a impresión 3D se desarrollarán utilizando PETG.

<p align="center"><strong><em>Figura 1. Modelo tridimensional del módulo sumergido de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/5a6a724f-c839-4907-ae4e-fec3eb274d64" alt="Modelo tridimensional del módulo sumergido" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se muestra la configuración estructural del módulo sumergido, la disposición de las cámaras y los elementos de sujeción respecto a la linterna de cultivo representada mediante el cilindro gris.</em></p>

#### 3.4.2. Diseño tridimensional de la boya de superficie

La boya de superficie de LanternGuard se diseñó para mantener sobre el agua los componentes encargados de la gestión energética, programación de inspecciones y comunicación con la estación receptora terrestre. Su estructura integra un compartimento central para la electrónica, un soporte superior para el panel solar y elementos laterales destinados a proporcionar flotabilidad al conjunto.

En la parte superior se ubica el panel solar, cuya función será captar energía para contribuir a la alimentación eléctrica del sistema. Debajo de este se encuentra el compartimento destinado a alojar la PCB personalizada de la boya, que integra el módulo Heltec WiFi LoRa 32 V3, el transceptor MAX3485 y las conexiones del reloj de tiempo real DS3231, junto con los elementos asociados a la alimentación eléctrica.

El modelo incorpora elementos cilíndricos laterales destinados a mejorar la flotabilidad y contribuir a la estabilidad de la estructura. Estos flotadores se integrarán mediante soportes de fijación que permitirán mantenerlos sujetos al conjunto. Los elementos flotantes serán componentes independientes, mientras que los soportes y las piezas estructurales se fabricarán mediante impresión 3D utilizando PETG.

Esta configuración permite organizar los componentes de superficie en una estructura que integra las funciones de alimentación, control y comunicación de la boya, manteniendo el compartimento electrónico separado del contacto directo con el agua.

<p align="center"><strong><em>Figura 2. Modelo tridimensional de la boya de superficie de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/87f4c021-e6ef-4b26-bffe-4bd2f1af378d" alt="Modelo tridimensional de la boya de superficie" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se presenta la distribución del panel solar, el compartimento electrónico, los soportes estructurales y los elementos laterales de flotación. Las piezas estructurales destinadas a impresión 3D se desarrollarán en PETG.</em></p>

#### 3.4.3. Diseño tridimensional del sistema completo LanternGuard

El modelo tridimensional del sistema completo representa la integración de la boya de superficie y el módulo sumergido mediante un cable umbilical. Esta configuración permite visualizar la relación física entre ambos subsistemas y la distribución de las funciones tecnológicas de LanternGuard.

La boya permanecerá en la superficie del agua, donde se concentrarán las funciones de gestión energética, programación temporal y comunicación inalámbrica. Por su parte, el módulo sumergido se instalará sobre la linterna de cultivo mediante su sistema de sujeción, con la finalidad de capturar imágenes de las mallas y registrar mediciones complementarias.

El cable umbilical establecerá la conexión física entre ambos módulos, permitiendo la transferencia de información mediante comunicación RS-485. De esta manera, el diseño integra las funciones de adquisición submarina y gestión de información en superficie dentro de una misma arquitectura tecnológica.

<p align="center"><strong><em>Figura 3. Modelo tridimensional del sistema completo LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b8ed4069-34f3-413c-84da-51e8caa14c2f" alt="Modelo tridimensional del sistema completo" width="360" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se muestra la integración de la boya de superficie y el módulo sumergido, unidos mediante el cable umbilical, de acuerdo con la configuración estructural propuesta para LanternGuard.</em></p>

### 3.5. Diseño electrónico del módulo sumergido

Para el módulo sumergido de LanternGuard se desarrolló un esquemático electrónico mediante EasyEDA, con el propósito de establecer las conexiones de los componentes encargados de la captura de imágenes, almacenamiento, comunicación y control de iluminación. A diferencia de la boya de superficie, este módulo no contará con una PCB personalizada, ya que sus componentes se integrarán mediante una placa universal perforada, conocida como *galleta electrónica*, sobre la cual se realizarán las conexiones correspondientes.

El esquemático se organiza en bloques funcionales de control y procesamiento, captura de imágenes, alimentación, almacenamiento, comunicación RS-485, control de iluminación y monitoreo, como se muestra en la Figura 4.

**Control y procesamiento.** La unidad principal corresponde al ESP32-S3-DevKitC-1-N16R8, encargado de coordinar la adquisición de imágenes, el registro de mediciones, el almacenamiento de información y la comunicación con la boya. Esta placa dispone de interfaces digitales que permiten integrar los diferentes componentes del módulo sumergido [16](#ref-16).

**Captura de imágenes y almacenamiento.** El diseño incorpora conectores para dos cámaras Arducam Mega de 5 MP, que comparten las señales de comunicación SPI y disponen de líneas de selección independientes. Esta configuración permite coordinar la captura de fotografías desde diferentes orientaciones hacia las mallas de la linterna. Asimismo, se contempla una tarjeta microSD conectada mediante SPI para almacenar inicialmente las fotografías y mediciones obtenidas durante las inspecciones [8](#ref-8).

**Comunicación RS-485.** Para transferir la información hacia la boya se utiliza un transceptor MAX3485, conectado al microcontrolador mediante señales de transmisión, recepción y control. El circuito también incorpora elementos de terminación y conexión al cable umbilical, estableciendo la interfaz de comunicación entre ambos módulos [17](#ref-17).

**Alimentación y control de iluminación.** El esquemático contempla conexiones de alimentación de 5 V y 3,3 V, destinadas a los diferentes componentes electrónicos. Además, incorpora dos circuitos de control mediante transistores MOSFET AO3400A, que permitirán activar las fuentes de iluminación asociadas a las cámaras para favorecer la captura de imágenes submarinas.

**Monitoreo y mediciones complementarias.** El diseño incluye un conector de expansión I²C que permitirá integrar el acelerómetro LIS3DH, destinado al registro de movimientos del módulo durante las inspecciones [10](#ref-10). Asimismo, se contempla la incorporación del sensor ultrasónico SEN0598, que proporcionará mediciones de distancia respecto a una superficie de referencia mediante comunicación UART [9](#ref-9). Su conexión específica y alimentación deberán incorporarse al esquema de interconexión del montaje.

La integración electrónica se realizará sobre una placa universal perforada, donde se organizarán las conexiones entre los módulos comerciales. Esta solución permitirá reunir los componentes del sistema de adquisición dentro del compartimento electrónico del dispositivo sumergido, de acuerdo con la disposición estructural presentada en el modelo tridimensional.

<p align="center"><strong><em>Figura 4. Esquemático electrónico del módulo sumergido de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/cd6aca38-78cf-4cef-9093-3f1e1348016e" alt="Esquemático electrónico del módulo sumergido" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia en EasyEDA. Se muestran los bloques de control y procesamiento, captura de imágenes, alimentación, almacenamiento, comunicación RS-485, control de iluminación y monitoreo. La integración física se realizará mediante una placa universal perforada.</em></p>

### 3.6. Diseño electrónico de la boya de superficie

Para la boya de superficie de LanternGuard se desarrolló un esquemático electrónico y el diseño de una placa de circuito impreso (PCB) personalizada mediante EasyEDA. Este subsistema tiene como finalidad gestionar la programación temporal de las inspecciones, recibir la información procedente del módulo sumergido y coordinar su transmisión inalámbrica hacia la estación receptora terrestre.

**Esquemático electrónico de la boya**

El esquemático se organiza en cinco bloques funcionales: alimentación, control y procesamiento, comunicación, control de salida y tiempo, y sistema de montaje, como se muestra en la Figura 5.

El **bloque de alimentación** contempla una entrada de batería identificada como VBAT y la conexión de un convertidor DC-DC elevador de tensión (*Step Up*), destinado a proporcionar una alimentación regulada de 5 V a los componentes correspondientes. Este bloque permitirá integrar el suministro eléctrico de la boya con los circuitos encargados de su funcionamiento.

El **bloque de control y procesamiento** está constituido por la placa Heltec WiFi LoRa 32 V3, que incorpora un microcontrolador ESP32-S3 y un transceptor LoRa. Esta unidad será la encargada de coordinar las funciones electrónicas de la boya, gestionar la comunicación con el módulo sumergido y organizar el envío inalámbrico de la información hacia tierra [19](#ref-19).

En el **bloque de comunicación** se incorpora el transceptor MAX3485, que permite establecer el enlace RS-485 entre la boya y el módulo sumergido mediante el cable umbilical. El circuito dispone de conexiones para las señales de transmisión, recepción y control, además de resistencias de terminación y polarización asociadas al enlace diferencial [17](#ref-17).

Por su parte, el **bloque de control de salida y tiempo** incluye un conector para el módulo RTC DS3231, cuya función será proporcionar la referencia temporal necesaria para programar las inspecciones periódicas cada 15 días [18](#ref-18). Asimismo, integra una etapa de conmutación formada por un MOSFET AO3401A y un transistor 2N3904, destinada al control electrónico de una salida de alimentación del sistema.

Finalmente, el esquema incorpora cuatro puntos de montaje que permitirán fijar la placa dentro del compartimento electrónico de la boya.

<p align="center"><strong><em>Figura 5. Esquemático electrónico de la boya de superficie de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b81e2db7-7854-48f7-b860-ad28dced2bc2" alt="Esquemático electrónico de la boya de superficie" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia en EasyEDA. Se muestran los bloques de alimentación, control y procesamiento, comunicación RS-485, control temporal y sistema de montaje.</em></p>

**Diseño de la placa PCB ruteada de la boya**

A partir del esquemático electrónico se elaboró el diseño de una PCB personalizada, en la cual se distribuyeron las huellas de los componentes, los conectores y las pistas de interconexión eléctrica, como se observa en la Figura 6.

En la zona central de la placa se ubica la huella destinada al módulo Heltec WiFi LoRa 32 V3, mientras que a su alrededor se distribuyen los componentes auxiliares y las conexiones correspondientes al transceptor MAX3485, el módulo RTC y los circuitos de alimentación y control. El diseño también incorpora cuatro perforaciones en las esquinas para facilitar la fijación de la PCB dentro de la estructura de la boya.

El ruteado de las pistas permite organizar las conexiones eléctricas de los diferentes componentes sobre una misma placa, reduciendo la necesidad de utilizar cableado individual para las interconexiones internas. Esta configuración facilita la integración del subsistema electrónico dentro del compartimento central representado en el modelo tridimensional.

La PCB se ha diseñado para su posterior fabricación y ensamblaje. Su integración permitirá reunir las principales funciones electrónicas de la boya en una estructura compacta, mientras que el panel solar, la batería y el circuito de gestión de carga se consideran dentro del sistema de alimentación previsto, cuya configuración definitiva deberá completarse.

<p align="center"><strong><em>Figura 6. Diseño de la placa PCB ruteada de la boya de superficie de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/c3c2b51e-7a33-4ec2-b2a7-6d31ed5453c5" alt="PCB ruteada de la boya de superficie" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia en EasyEDA. Se presenta la distribución de las huellas electrónicas, las pistas ruteadas, los conectores y las perforaciones de montaje de la PCB personalizada.</em></p>

En conjunto, los modelos tridimensionales y los esquemáticos electrónicos permiten representar la configuración física y funcional de LanternGuard, integrando el módulo sumergido, la boya de superficie y los medios de comunicación propuestos. Estos diseños proporcionan una base técnica para el desarrollo del sistema de monitoreo de bioincrustación en las linternas de cultivo de *Argopecten purpuratus*.

### 3.7. Propuesta preliminar de interfaz del aplicativo LanternGuard

Como complemento de la arquitectura tecnológica de LanternGuard, se propone el desarrollo de un aplicativo destinado a visualizar y organizar la información obtenida durante las inspecciones de las linternas de cultivo. Su finalidad será presentar el porcentaje estimado de cobertura visible por bioincrustación (biofouling) en las regiones de malla fotografiadas, facilitando al acuicultor el seguimiento de la acumulación de organismos incrustantes y la evaluación de la necesidad de realizar actividades de limpieza.

La interfaz propuesta contempla un panel de monitoreo que presenta la cantidad de linternas registradas, las fechas de captura y los indicadores de biofouling. Asimismo, incorpora la visualización de fotografías submarinas, gráficos de evolución temporal y una sección de comparación de imágenes correspondientes a diferentes inspecciones. Esta organización busca facilitar la interpretación de la información y el seguimiento de los cambios observados en las mallas.

La Figura 7 muestra el diseño preliminar de la interfaz del aplicativo LanternGuard, como representación conceptual de las funciones previstas. Los porcentajes, fechas y niveles de biofouling presentados en la imagen son ilustrativos y permiten visualizar cómo se mostraría la información generada por el sistema.

<p align="center"><strong><em>Figura 7. Propuesta preliminar de la interfaz del aplicativo LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e1dcad7c-e80a-48d6-be4d-5a9829fb891c" alt="Interfaz preliminar del aplicativo LanternGuard" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Representación conceptual del aplicativo para visualizar capturas submarinas, porcentajes estimados de cobertura visible por bioincrustación y evolución temporal del monitoreo. Los datos mostrados son referenciales.</em></p>

---

## Referencias bibliográficas — Formato IEEE

<a name="ref-1"></a>
**[[1]](https://vinculate.concytec.gob.pe/wp-content/files/RP-020-2022-CONCYTEC-P.pdf)** Consejo Nacional de Ciencia, Tecnología e Innovación Tecnológica (CONCYTEC), *Directiva N.º 001-2022-CONCYTEC-P: Uso de la metodología Nivel de Madurez Tecnológica (TRL)*, Resolución de Presidencia N.º 020-2022-CONCYTEC-P, Perú, 2022. [En línea]. Disponible en: [Abrir fuente](https://vinculate.concytec.gob.pe/wp-content/files/RP-020-2022-CONCYTEC-P.pdf)

<a name="ref-2"></a>
**[[2]](https://doi.org/10.1111/jwas.70054)** R. E. Loayza-Aguilar, G. B. Saldaña-Rojas, F. Merino y G. E. Olivos-Ramirez, "Biofouling reduction by lantern nets exchange and its relationship with production and survival of Argopecten purpuratus in Samanco Bay, Peru," *Journal of the World Aquaculture Society*, vol. 56, n.º 5, art. e70054, 2025. doi: [Abrir fuente](https://doi.org/10.1111/jwas.70054)

<a name="ref-3"></a>
**[[3]](https://doi.org/10.1016/j.oceaneng.2023.114430)** Q.-P. Chen, C.-W. Bi, Z.-X. Zhang y Y.-P. Zhao, "Hydrodynamic effect of different biofouling types on aquaculture netting," *Ocean Engineering*, vol. 279, art. 114430, 2023. doi: [Abrir fuente](https://doi.org/10.1016/j.oceaneng.2023.114430)

<a name="ref-4"></a>
**[[4]](https://doi.org/10.3390/jmse8090707)** W. Qiu, V. Pakrashi y B. Ghosh, "Fishing net health state estimation using underwater imaging," *Journal of Marine Science and Engineering*, vol. 8, n.º 9, art. 707, 2020. doi: [Abrir fuente](https://doi.org/10.3390/jmse8090707)

<a name="ref-5"></a>
**[[5]](https://doi.org/10.1016/j.aquaeng.2024.102466)** R. Cappaert, W. Yang, D. J. Ross, C. Johnston, C. MacLeod y C. A. White, "Development of an image binarization software tool for net occlusion estimations," *Aquacultural Engineering*, vol. 107, art. 102466, 2024. doi: [Abrir fuente](https://doi.org/10.1016/j.aquaeng.2024.102466)

<a name="ref-6"></a>
**[[6]](https://doi.org/10.3390/s16091466)** A. Augustin, J. Yi, T. Clausen y W. M. Townsley, "A study of LoRa: Long range & low power networks for the Internet of Things," *Sensors*, vol. 16, n.º 9, art. 1466, 2016. doi: [Abrir fuente](https://doi.org/10.3390/s16091466)

<a name="ref-7"></a>
**[[7]](https://doi.org/10.3390/s18103257)** A. H. Jebril, A. Sali, A. Ismail y M. F. A. Rasid, "Overcoming limitations of LoRa physical layer in image transmission," *Sensors*, vol. 18, n.º 10, art. 3257, 2018. doi: [Abrir fuente](https://doi.org/10.3390/s18103257)

<a name="ref-8"></a>
**[[8]](https://docs.arducam.com/Arduino-SPI-camera/MEGA-SPI/MEGA-5MP/)** Arducam, "MEGA-5MP: Cámara SPI de 5 megapíxeles," documentación técnica, s. f. [En línea]. Disponible en: [Abrir fuente](https://docs.arducam.com/Arduino-SPI-camera/MEGA-SPI/MEGA-5MP/)

<a name="ref-9"></a>
**[[9]](https://wiki.dfrobot.com/sen0598/)** DFRobot, "IP68 Underwater Ultrasonic Obstacle Avoidance Sensor (3m), SEN0598," documentación técnica, s. f. [En línea]. Disponible en: [Abrir fuente](https://wiki.dfrobot.com/sen0598/)

<a name="ref-10"></a>
**[[10]](https://www.st.com/en/mems-and-sensors/lis3dh.html)** STMicroelectronics, "LIS3DH: 3-axis MEMS accelerometer," documentación técnica, s. f. [En línea]. Disponible en: [Abrir fuente](https://www.st.com/en/mems-and-sensors/lis3dh.html)

<a name="ref-11"></a>
**[[11]](https://www.comunidadandina.org/StaticFiles/DocOf/DEC486.pdf)** Comunidad Andina, *Decisión 486: Régimen Común sobre Propiedad Industrial*, 2000. [En línea]. Disponible en: [Abrir fuente](https://www.comunidadandina.org/StaticFiles/DocOf/DEC486.pdf)

<a name="ref-12"></a>
**[[12]](https://patents.google.com/patent/WO2024072597A1/en)** M. Stokes, H. Pham y T. R. Swanson, "Adjustable aquaculture camera mounting system," publicación de patente WO2024072597A1, 2024. [En línea]. Disponible en: [Abrir fuente](https://patents.google.com/patent/WO2024072597A1/en)

<a name="ref-13"></a>
**[[13]](https://patents.google.com/patent/US20240130336A1/en)** H. Pham y T. R. Swanson, "Underwater net monitoring device," publicación de patente US20240130336A1, 2024. [En línea]. Disponible en: [Abrir fuente](https://patents.google.com/patent/US20240130336A1/en)

<a name="ref-14"></a>
**[[14]](https://patents.google.com/patent/NO20240761A1/en)** M. D. Zúñiga Barraza *et al.*, "System for inspecting farming netting in aquaculture cages," publicación de patente NO20240761A1, familia WO2023108307A1, 2024. [En línea]. Disponible en: [Abrir fuente](https://patents.google.com/patent/NO20240761A1/en)

<a name="ref-15"></a>
**[[15]](https://patents.google.com/patent/US20200326279A1/en)** L. Fortunato y T. Leiknes, "In-situ non-invasive device for early detection of fouling in aquatic systems," publicación de patente US20200326279A1, 2020. [En línea]. Disponible en: [Abrir fuente](https://patents.google.com/patent/US20200326279A1/en)

<a name="ref-16"></a>
**[[16]](https://www.espressif.com/en/products/devkits/esp32-s3-series/esp32-s3-devkitc-1)** Espressif Systems, "ESP32-S3-DevKitC-1: Placas de desarrollo ESP32-S3," documentación técnica del fabricante, s. f. [En línea]. Disponible en: [Abrir fuente](https://www.espressif.com/en/products/devkits/esp32-s3-series/esp32-s3-devkitc-1)

<a name="ref-17"></a>
**[[17]](https://www.analog.com/en/products/max3485.html)** Analog Devices, "MAX3485: Transceptor RS-485/RS-422 de 3,3 V," ficha técnica, s. f. [En línea]. Disponible en: [Abrir fuente](https://www.analog.com/en/products/max3485.html)

<a name="ref-18"></a>
**[[18]](https://www.analog.com/en/products/ds3231.html)** Analog Devices, "DS3231: Reloj de tiempo real integrado con interfaz I²C," ficha técnica, s. f. [En línea]. Disponible en: [Abrir fuente](https://www.analog.com/en/products/ds3231.html)

<a name="ref-19"></a>
**[[19]](https://heltec.org/project/wifi-lora-32-v3/)** Heltec Automation, "WiFi LoRa 32 (V3): ESP32-S3 y SX1262," documentación técnica, s. f. [En línea]. Disponible en: [Abrir fuente](https://heltec.org/project/wifi-lora-32-v3/)




