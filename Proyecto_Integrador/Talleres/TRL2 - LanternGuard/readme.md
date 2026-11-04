
<h1 align="center">LanternGuard</h1>

<h2 align="center">TRL 2 — Formulación conceptual de la propuesta tecnológica</h2>

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

LanternGuard es una propuesta tecnológica orientada al monitoreo periódico de la bioincrustación en las mallas de las linternas utilizadas para el cultivo suspendido de concha de abanico (*Argopecten purpuratus*). El sistema contempla la integración de dos cámaras submarinas Arducam Mega de 5 MP, un acelerómetro LIS3DH y tecnologías de comunicación para obtener información sobre el estado de las regiones observadas de las mallas. Mediante el procesamiento digital de imágenes, se propone estimar el porcentaje de cobertura visible y desarrollar un algoritmo propio para estimar el volumen de bioincrustación acumulada en dichas regiones. Esta información permitirá apoyar las decisiones de inspección y mantenimiento, sin que LanternGuard realice actividades de limpieza.


La presente propuesta se formula considerando los indicadores referenciales del nivel de madurez tecnológica TRL 2 establecidos en el Anexo 1 de la Directiva N.º 001-2022-CONCYTEC-P [\[1\]](#ref-1).

---

## 1. Artículos científicos relacionados con la propuesta tecnológica

### 1.1. Bioincrustación en linternas y necesidad de monitoreo

Loayza-Aguilar et al. [\[2\]](#ref-2) investigaron el efecto del recambio de linternas utilizadas en el cultivo suspendido de concha de abanico (*Argopecten purpuratus*) en la bahía de Samanco, Perú. Los investigadores compararon linternas reemplazadas durante la etapa final del cultivo con aquellas mantenidas hasta la cosecha. Los resultados mostraron una reducción del 64,6 % en el peso de la bioincrustación y una mejora del 10,8 % en la supervivencia de los organismos, bajo las condiciones evaluadas. Este estudio constituye un antecedente directamente relacionado con LanternGuard, ya que demuestra la importancia del manejo de la bioincrustación en las estructuras de cultivo. Sin embargo, la investigación no evaluó sistemas de monitoreo mediante cámaras submarinas ni estableció indicadores visuales para determinar cuándo realizar el mantenimiento.

De manera complementaria, Chen et al. [\[3\]](#ref-3) analizaron mediante ensayos con modelos físicos los efectos de diferentes tipos de bioincrustación artificial sobre las características hidrodinámicas de paneles de redes acuícolas. Los resultados evidenciaron que la acumulación de incrustaciones puede incrementar considerablemente la resistencia al flujo y modificar las condiciones de circulación del agua a través de las redes. Aunque el estudio no se realizó específicamente en linternas de concha de abanico, proporciona fundamentos científicos para considerar la obstrucción de las aberturas como una característica relevante en el seguimiento de estas estructuras.

En conjunto, ambas investigaciones respaldan la importancia del monitoreo periódico de la bioincrustación en las estructuras de cultivo. A partir de estos antecedentes, LanternGuard propone utilizar imágenes submarinas para estimar el porcentaje de cobertura visible por organismos incrustantes en regiones seleccionadas de las mallas, generando información que contribuya a la planificación de inspecciones y actividades de limpieza.

### 1.2. Análisis de imágenes para el monitoreo visual de bioincrustación

Qiu, Pakrashi y Ghosh [\[4\]](#ref-4) desarrollaron un procedimiento para evaluar el estado de redes acuícolas mediante imágenes submarinas. Su método incluye la selección de regiones de interés, la corrección de distorsión y visibilidad, la segmentación de organismos incrustantes y el análisis de las aberturas de las redes para estimar su porcentaje de bloqueo. Este antecedente aporta fundamentos para LanternGuard al demostrar la utilidad del procesamiento digital de imágenes en la identificación y análisis de bioincrustación. Su metodología constituye una referencia para formular un procedimiento orientado a estimar la cobertura visible de organismos incrustantes en las mallas.

De manera complementaria, Cappaert et al. [\[5\]](#ref-5) desarrollaron una herramienta de procesamiento de imágenes para estimar la oclusión en redes utilizadas en la acuicultura de salmones. Su procedimiento emplea técnicas de segmentación basadas en aprendizaje profundo para diferenciar regiones de agua y no agua, considerando además el área ocupada por la estructura de la malla. Los autores reportaron una precisión media de prueba cercana al 93,5 % en la clasificación de píxeles de las imágenes evaluadas. Este estudio proporciona fundamentos para la identificación y clasificación de elementos presentes en fotografías submarinas, aspectos relevantes para el análisis visual propuesto en LanternGuard.

A partir de estos antecedentes, LanternGuard propone analizar fotografías submarinas para identificar las zonas visibles cubiertas por organismos incrustantes y estimar su proporción respecto al área de referencia seleccionada para el análisis. Para ello, se contempla la delimitación de regiones de interés, la diferenciación entre los organismos y la estructura de la malla, así como el tratamiento de variaciones de iluminación, turbidez y perspectiva. Estos criterios permitirán orientar la definición conceptual del procedimiento de procesamiento de imágenes.

De manera complementaria, LanternGuard contempla desarrollar un algoritmo propio orientado a estimar el volumen de bioincrustación acumulada sobre las regiones fotografiadas de las mallas. A diferencia del porcentaje de cobertura visible, la estimación volumétrica requerirá establecer criterios geométricos, referencias de escala y un procedimiento de cálculo que considere las limitaciones de las imágenes submarinas. Esta función se encuentra en etapa conceptual y su metodología y precisión deberán validarse posteriormente.

### 1.3. Sustento para la arquitectura de adquisición y comunicación

Augustin et al. [\[6\]](#ref-6) analizaron las características y el desempeño de la tecnología LoRa, destacando su capacidad de comunicación a largas distancias y su bajo consumo energético, aunque con limitaciones en la velocidad de transmisión de datos. De manera complementaria, Jebril et al. [\[7\]](#ref-7) investigaron alternativas para transmitir imágenes mediante LoRa, mediante la división de los archivos en paquetes. Este último estudio se considera un antecedente tecnológico, pero la transmisión de fotografías completas por LoRa no forma parte de la arquitectura seleccionada para LanternGuard. En la propuesta, LoRa se destina a mensajes breves de estado, metadatos de las inspecciones e indicadores resumidos cuando estén disponibles; las fotografías completas se reservarán para una transferencia local posterior. El alcance y desempeño del enlace deberán evaluarse en etapas posteriores.

Respecto a la adquisición de información, la documentación técnica de Arducam [\[8\]](#ref-8) describe las características de las cámaras Mega de 5 MP con interfaz SPI, seleccionadas para la captura de imágenes submarinas. Por su parte, STMicroelectronics [\[9\]](#ref-9) describe el acelerómetro triaxial LIS3DH, que permite registrar aceleraciones y movimientos. Estos componentes sustentan la selección tecnológica de LanternGuard, donde las cámaras permitirán observar regiones de las mallas, mientras que el acelerómetro proporcionará información complementaria sobre el movimiento del módulo durante la captura.

### 1.4. Síntesis de la aplicación de los antecedentes

<p align="center"><strong>Tabla 1. Relación entre los antecedentes científicos y su aplicación en LanternGuard</strong></p>

| Fuente | Evidencia científica documentada | Aplicación conceptual en LanternGuard |
|---|---|---|
| Loayza-Aguilar et al. [\[2\]](#ref-2) | Evaluaron los efectos del recambio de linternas sobre la bioincrustación y la supervivencia de *Argopecten purpuratus* en Samanco. | Sustentar la necesidad del monitoreo periódico de las linternas para apoyar las decisiones de mantenimiento. |
| Chen et al. [\[3\]](#ref-3) | Analizaron los efectos de la bioincrustación sobre el comportamiento hidrodinámico de redes acuícolas. | Sustentar la importancia del seguimiento de la bioincrustación acumulada en las mallas. |
| Qiu et al. [\[4\]](#ref-4) | Desarrollaron un método de análisis de imágenes submarinas para estimar el bloqueo de aberturas de redes. | Considerar técnicas de segmentación para identificar organismos incrustantes en imágenes submarinas. |
| Cappaert et al. [\[5\]](#ref-5) | Desarrollaron un procedimiento de segmentación de imágenes para estimar la oclusión de redes salmoneras. | Orientar la diferenciación visual entre organismos incrustantes, estructura de la malla y regiones de agua. |
| Augustin et al. [\[6\]](#ref-6) y Jebril et al. [\[7\]](#ref-7) | Estudiaron las características y limitaciones de LoRa y las dificultades de transmitir imágenes mediante esta tecnología. | Fundamentar el uso de LoRa para mensajes breves y reservar las fotografías completas para transferencia local, sin incluir su transmisión por LoRa en la arquitectura propuesta. |

<p align="center"><em><strong>Nota.</strong> Elaboración propia a partir de los antecedentes científicos revisados en los apartados 1.1, 1.2 y 1.3.</em></p>

Las investigaciones revisadas proporcionan fundamentos científicos y tecnológicos para la formulación de LanternGuard. Los estudios sobre bioincrustación justifican la importancia de monitorear su acumulación en las estructuras de cultivo, mientras que los métodos de procesamiento de imágenes aportan antecedentes para identificar y analizar visualmente organismos incrustantes. Asimismo, las investigaciones sobre comunicación LoRa sustentan su uso para transmitir información breve de las inspecciones, teniendo en cuenta sus limitaciones de velocidad. A partir de estos antecedentes, LanternGuard plantea integrar tecnologías existentes en un sistema de monitoreo periódico orientado a estimar la cobertura visible de bioincrustación en las mallas de las linternas utilizadas para el cultivo de *Argopecten purpuratus*.

---

## 2. Análisis preliminar de patentabilidad y protección

### 2.1. Criterios de evaluación

La Decisión 486 de la Comunidad Andina [\[10\]](#ref-10), que establece el Régimen Común sobre Propiedad Industrial, señala que una patente de invención debe cumplir tres requisitos: novedad (artículo 16), nivel inventivo (artículo 18) y aplicación industrial (artículo 19). Asimismo, el artículo 81 contempla la protección mediante modelos de utilidad cuando una nueva forma, configuración o disposición de elementos de un objeto permite mejorar su funcionamiento, utilización o fabricación, o proporciona una ventaja o efecto técnico.

A partir de estos criterios, el análisis de patentabilidad de LanternGuard se orienta a identificar posibles características diferenciadoras frente a las tecnologías existentes y evaluar si su configuración podría ofrecer una ventaja técnica. Para ello, se revisan publicaciones de patentes relacionadas con sistemas de inspección submarina, monitoreo de redes acuícolas y detección de bioincrustación.

### 2.2. Publicaciones de patentes relacionadas con la propuesta

Se realizó una búsqueda exploratoria en Google Patents utilizando términos relacionados con cámaras para acuicultura, monitoreo de redes sumergidas, inspección de mallas y detección de bioincrustación. Se identificaron cuatro publicaciones de patentes relacionadas con la propuesta tecnológica de LanternGuard, cuyas características permiten establecer semejanzas y diferencias respecto al sistema planteado. La Tabla 2 presenta los principales antecedentes encontrados.

<p align="center"><strong>Tabla 2. Comparación de publicaciones de patentes relacionadas con LanternGuard</strong></p>

| Documento | Tecnología descrita | Comparación con LanternGuard |
|---|---|---|
| WO2024072597A1 [\[11\]](#ref-11) | Sistema de montaje ajustable de cámaras para modificar su campo de visión en entornos de acuicultura. | Ambas propuestas utilizan cámaras; LanternGuard contempla cámaras orientadas hacia regiones de las mallas, sin incorporar el mecanismo de ajuste descrito en la publicación. |
| US20240130336A1 [\[12\]](#ref-12) | Dispositivo de monitoreo de redes sumergidas mediante impulsos mecánicos y señales relacionadas con la tensión de las redes. | Comparte el monitoreo de estructuras acuícolas, pero utiliza un principio de medición diferente del análisis de imágenes propuesto en LanternGuard. |
| NO20240761A1 [\[13\]](#ref-13) | Sistema de inspección de redes acuícolas mediante un dispositivo submarino móvil, captura de imágenes y posicionamiento ultrasónico. | Comparte el uso de imágenes submarinas; sin embargo, el antecedente incorpora posicionamiento ultrasónico, mientras que LanternGuard propone inspecciones periódicas mediante un módulo situado respecto a una linterna de cultivo, sin utilizar un vehículo móvil para recorrer las redes. |
| US20200326279A1 [\[14\]](#ref-14) | Dispositivo de detección no invasiva de incrustaciones en sistemas acuáticos mediante técnicas ópticas de medición de superficies. | Aborda la detección no invasiva de incrustaciones mediante técnicas ópticas, mientras que LanternGuard propone estimar la cobertura visible por bioincrustación mediante fotografías submarinas. |

<p align="center"><em><strong>Nota.</strong> Elaboración propia a partir de las publicaciones consultadas en Google Patents [\[11\]](#ref-11)–[\[14\]](#ref-14).</em></p>

La publicación noruega NO20240761A1 pertenece a la misma familia de patentes que WO2023108307A1, por lo que ambas se consideran un mismo antecedente tecnológico [\[13\]](#ref-13). Asimismo, la solicitud estadounidense US20240130336A1 dio lugar a la patente concedida US12426577B2 [\[12\]](#ref-12). Estas relaciones permiten identificar las publicaciones vinculadas, aunque no constituyen una evaluación completa de su situación jurídica en todos los territorios.

La comparación muestra que existen tecnologías orientadas al monitoreo submarino, la inspección de redes y la detección de bioincrustación. Frente a estos antecedentes, LanternGuard plantea una configuración dirigida específicamente al seguimiento periódico de las mallas de linternas utilizadas en el cultivo de *Argopecten purpuratus*, mediante la integración de captura de imágenes, mediciones complementarias y comunicación entre un módulo sumergido y una boya de superficie. Esta diferenciación constituye una característica de la propuesta que deberá considerarse en el análisis preliminar de patentabilidad, sin que por sí sola demuestre novedad o nivel inventivo.

### 2.3. Evaluación preliminar de novedad, nivel inventivo y aplicación industrial

**Novedad.** La configuración propuesta de LanternGuard integra dos cámaras submarinas, sensores complementarios, una boya de superficie, comunicación RS-485 y LoRa, y procesamiento de imágenes para estimar la cobertura visible de bioincrustación en las mallas de linternas utilizadas para el cultivo de *Argopecten purpuratus*. Esta combinación específica no se identificó en las cuatro publicaciones de patentes examinadas. Sin embargo, sus principales componentes y funciones ya se encuentran presentes en tecnologías existentes relacionadas con la inspección submarina, el monitoreo de redes acuícolas y la detección de bioincrustación. Por ello, la búsqueda realizada no permite establecer de manera definitiva la novedad de la propuesta, siendo necesario ampliar la revisión del estado de la técnica [\[10\]](#ref-10)–[\[14\]](#ref-14).

**Nivel inventivo.** La integración de cámaras, microcontroladores, sensores comerciales y tecnologías de comunicación conocidas podría considerarse una solución previsible para una persona especializada en este campo tecnológico. Para determinar si LanternGuard presenta nivel inventivo, sería necesario identificar características técnicas de su configuración que no resulten evidentes a partir de las tecnologías existentes. Entre los aspectos que podrían analizarse se encuentran la disposición de los componentes para observar regiones específicas de las mallas y el sistema de montaje del dispositivo sumergido. En esta etapa no se dispone de evidencia suficiente para establecer que dichas características cumplen este requisito [\[10\]](#ref-10).

**Aplicación industrial.** LanternGuard presenta una aplicación potencial en el sector acuícola, específicamente en el monitoreo de las linternas utilizadas para el cultivo suspendido de conchas de abanico. Su arquitectura contempla componentes electrónicos y estructuras que podrían fabricarse e integrarse para obtener información sobre el estado visible de las mallas y apoyar la planificación del mantenimiento. Por tanto, la propuesta presenta una posible aplicación industrial conforme al artículo 19 de la Decisión 486, aunque este criterio no implica por sí solo el cumplimiento de los requisitos de novedad y nivel inventivo [\[10\]](#ref-10).

### 2.4. Posibles vías de protección

A partir del análisis realizado, LanternGuard podría considerar diferentes mecanismos de protección de propiedad intelectual. Una eventual patente de invención requeriría ampliar la búsqueda del estado de la técnica y verificar el cumplimiento de los requisitos de patentabilidad. Asimismo, podría evaluarse la protección de una configuración mecánica mediante un modelo de utilidad, siempre que presente una nueva disposición de elementos que proporcione una ventaja técnica, conforme al artículo 81 de la Decisión 486 de la Comunidad Andina [\[10\]](#ref-10).

Por otro lado, el software original desarrollado para la adquisición y el procesamiento de imágenes podría protegerse mediante derecho de autor. La viabilidad de estas alternativas dependerá de las características definitivas de la propuesta y de las condiciones de titularidad aplicables.

---

## 3. Perfil o propuesta del proyecto

### 3.1. Problema, propósito y alcance

En el cultivo suspendido de concha de abanico (*Argopecten purpuratus*), las mallas de las linternas están expuestas a la acumulación de organismos incrustantes que pueden obstruir progresivamente sus aberturas. Las investigaciones sobre bioincrustación han evidenciado la importancia de este fenómeno en las estructuras acuícolas y su relación con las condiciones de cultivo y circulación del agua [\[2\]](#ref-2), [\[3\]](#ref-3). Ante esta problemática, se identifica la necesidad de disponer de información visual periódica y comparable sobre el estado de las mallas para apoyar la planificación de las inspecciones y actividades de mantenimiento.

**Objetivo general.** Formular conceptualmente un sistema de monitoreo periódico de la bioincrustación en las mallas de las linternas utilizadas para el cultivo de *Argopecten purpuratus*, mediante la captura y el procesamiento de imágenes submarinas y el registro de mediciones complementarias, con la finalidad de estimar el porcentaje de cobertura visible y desarrollar un algoritmo propio orientado a estimar el volumen de bioincrustación acumulada en las regiones observadas, proporcionando información que apoye las decisiones de inspección y mantenimiento.

**Alcance.** La propuesta comprende el monitoreo periódico de regiones seleccionadas de las mallas mediante dos cámaras submarinas y el registro del movimiento del módulo mediante el acelerómetro LIS3DH. Se contempla estimar el porcentaje de cobertura visible y el volumen de bioincrustación acumulada mediante procesamiento digital de imágenes. Los resultados corresponderán a las regiones analizadas y no representarán necesariamente la totalidad de la linterna. La metodología de estimación volumétrica deberá desarrollarse y validarse en etapas posteriores. LanternGuard está orientado al monitoreo y no contempla realizar la limpieza de las mallas de cultivo.

### 3.2. Arquitectura funcional propuesta

LanternGuard se organiza en cuatro elementos principales: módulo sumergido, boya de superficie, estación receptora terrestre y servicio de procesamiento de imágenes. El módulo sumergido se conecta con la boya mediante un cable umbilical que permite transferir fotografías y registros por comunicación RS-485. Desde la boya, LoRa se utilizará para transmitir a la estación terrestre mensajes breves sobre las inspecciones, como metadatos, estado e indicadores resumidos cuando estén disponibles, pero no fotografías completas. Estas últimas se conservarán para su recuperación mediante una transferencia local posterior, cuyo medio específico aún no se define en esta etapa conceptual. Una vez que el equipo terrestre disponga de las fotografías, gestionará su envío al servicio de procesamiento de imágenes mediante una conexión a internet.

<p align="center"><strong>Tabla 3. Componentes y funciones de la arquitectura conceptual de LanternGuard</strong></p>

| Elemento | Composición conceptual | Función prevista |
|---|---|---|
| **Módulo sumergido** | ESP32-S3-DevKitC-1-N16R8, dos cámaras Arducam Mega 5 MP, acelerómetro LIS3DH, microSD, iluminación y transceptor MAX3485. Integración mediante placa universal perforada. | Capturar imágenes submarinas, registrar mediciones complementarias, almacenar temporalmente la información y transferirla a la boya mediante RS-485. |
| **Boya de superficie** | Heltec WiFi LoRa 32 V3, RTC DS3231, transceptor MAX3485 y PCB personalizada. Se contempla alimentación mediante panel solar, batería y circuito de gestión energética, además de almacenamiento temporal. | Coordinar las inspecciones programadas, recibir los datos y fotografías del módulo sumergido, conservarlos temporalmente y enviar mediante LoRa información resumida de las inspecciones; las fotografías completas se recuperarían por transferencia local posterior. |
| **Estación receptora terrestre** | Receptor Heltec WiFi LoRa 32 V3 y equipo informático con acceso a internet. | Recibir por LoRa los mensajes breves de las inspecciones y gestionar, después de la recuperación local de las fotografías completas, su envío al servicio de procesamiento. |
| **Servicio de procesamiento de imágenes** | Sistema de almacenamiento y procesamiento digital de imágenes, por configurar, que contempla el desarrollo de un algoritmo propio de estimación volumétrica. | Procesar las fotografías recuperadas, identificar las regiones cubiertas por organismos incrustantes, estimar el porcentaje de cobertura visible y desarrollar la estimación del volumen de bioincrustación acumulada en las regiones analizadas, para presentar los resultados en el aplicativo. |


<p align="center"><em><strong>Nota.</strong> Elaboración propia a partir de la arquitectura conceptual propuesta para LanternGuard.</em></p>

La selección de los componentes electrónicos se sustenta en la documentación técnica de sus fabricantes. Espressif Systems [\[15\]](#ref-15) describe las características del ESP32-S3-DevKitC-1, Arducam [\[8\]](#ref-8) documenta las cámaras Mega de 5 MP y STMicroelectronics [\[9\]](#ref-9) presenta las características del acelerómetro LIS3DH. Asimismo, Analog Devices documenta el transceptor MAX3485 [\[16\]](#ref-16) y el reloj de tiempo real DS3231 [\[17\]](#ref-17), mientras que Heltec Automation [\[18\]](#ref-18) proporciona las especificaciones de la placa WiFi LoRa 32 V3.

La arquitectura contempla dos soluciones de integración electrónica. En la boya de superficie se propone utilizar una placa de circuito impreso (PCB) personalizada, cuyo diseño electrónico y distribución de pistas han sido elaborados. Por su parte, los componentes del módulo sumergido se integrarán mediante una placa universal perforada, utilizando como referencia su esquemático de conexiones. Ambas configuraciones se complementan para desarrollar las funciones de adquisición, comunicación y procesamiento previstas en LanternGuard.

### 3.3. Secuencia prevista de operación e indicador

LanternGuard contempla realizar inspecciones periódicas cada 15 días, con una duración aproximada de cinco minutos para la captura de imágenes y el registro de mediciones. La programación temporal se gestionaría mediante el reloj de tiempo real (RTC) ubicado en la boya de superficie. Durante cada inspección, el módulo sumergido utilizaría dos cámaras orientadas hacia diferentes regiones de las mallas, mientras que el acelerómetro registraría mediciones complementarias de movimiento.

Las fotografías y mediciones obtenidas se almacenarían inicialmente en una tarjeta microSD del módulo sumergido y posteriormente se transferirían a la boya mediante comunicación RS-485. La boya conservaría temporalmente las fotografías completas; estas no se enviarían por LoRa, sino que se recuperarían mediante una transferencia local posterior, cuyo medio aún debe definirse. El enlace LoRa se reservaría para mensajes breves de estado y metadatos de las inspecciones, así como indicadores resumidos cuando estén disponibles. Una vez recibidas las fotografías completas en tierra, se gestionarían su almacenamiento y envío al servicio de procesamiento de imágenes, donde se estimaría la cobertura visible de bioincrustación para presentarla en el aplicativo. Los cinco minutos previstos corresponden únicamente a la adquisición de información y no incluyen las etapas posteriores de transferencia y procesamiento.

El indicador principal de LanternGuard será el porcentaje estimado de cobertura visible por bioincrustación en regiones seleccionadas de las mallas. Para su obtención, se propone analizar las fotografías mediante técnicas de procesamiento de imágenes que permitan identificar las zonas ocupadas por organismos incrustantes y diferenciarlas de la estructura de la malla. El cálculo se planteará a partir de la proporción de área visible cubierta por bioincrustación respecto al área de referencia definida para cada región de análisis. Asimismo, se contempla comparar regiones equivalentes en inspecciones sucesivas, considerando las variaciones de iluminación, turbidez y perspectiva. La definición del procedimiento se apoyará en los antecedentes de análisis de imágenes submarinas [\[4\]](#ref-4), [\[5\]](#ref-5).

Como indicador complementario, se propone estimar el volumen de bioincrustación acumulada sobre las regiones fotografiadas de las mallas, mediante un algoritmo propio desarrollado por el equipo. Su formulación requerirá definir un procedimiento de estimación geométrica, referencias de escala y criterios para interpretar las imágenes obtenidas. Esta estimación se realizaría en el servicio de procesamiento de imágenes, una vez recuperadas las fotografías completas. El algoritmo, sus requerimientos técnicos y su precisión deberán desarrollarse y validarse en etapas posteriores.

El acelerómetro LIS3DH permitiría registrar información sobre el movimiento del módulo durante la captura. Esta variable complementaría el análisis visual, sin sustituir la estimación de cobertura obtenida mediante las fotografías.


### Análisis funcional y generación de alternativas de diseño

Como parte del diseño conceptual de LanternGuard, se realiza el análisis funcional del sistema mediante la caja negra, el esquema de funciones, la matriz morfológica y tres bocetos de alternativas de diseño. Estas herramientas permiten identificar las funciones necesarias para el monitoreo de la bioincrustación y sustentar las soluciones consideradas antes del modelado tridimensional.

#### Caja negra del sistema LanternGuard

La caja negra permite identificar las principales entradas y salidas del sistema LanternGuard, clasificadas en flujos de energía, materia, información y señales, sin describir todavía el funcionamiento interno de sus componentes.

Entre las entradas se consideran la energía solar, el agua de mar como medio de operación del módulo sumergido, las señales de encendido y control, y los parámetros de referencia necesarios para el monitoreo. Como salidas se incluyen la energía lumínica de los LED, la energía calorífica residual, el agua de mar y la información obtenida durante las inspecciones.

Asimismo, LanternGuard contempla la captura de imágenes submarinas para estimar el porcentaje de cobertura visible y el volumen de bioincrustación acumulada sobre las regiones observadas de las mallas. La estimación volumétrica se realizará mediante un algoritmo propio, cuyo desarrollo y validación forman parte de las siguientes etapas del proyecto. Los resultados permitirán apoyar las decisiones de inspección y mantenimiento de las linternas.

Asimismo, la caja negra contempla señales de interacción con el usuario, avisos de mantenimiento e indicación del estado de encendido y apagado. Estas funciones se consideran dentro de la propuesta conceptual y deberán definirse y validarse durante las siguientes etapas de desarrollo.

La Figura 1 presenta las entradas y salidas consideradas en el diseño conceptual de LanternGuard.

<p align="center"><strong><em>Figura 1. Caja negra del sistema LanternGuard.</em></strong></p>

<p align="center">
<img width="1302" height="1036" alt="Infografía de caja negra LanternGuard" src="https://github.com/user-attachments/assets/5532407b-77fc-4fa2-9468-492b2be28218" />

</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se representan los flujos de energía, materia, información y señales del sistema LanternGuard, considerando el monitoreo de la bioincrustación y la estimación propuesta de su cobertura visible y volumen.</em></p>

#### Esquema de funciones del sistema LanternGuard

El esquema de funciones de LanternGuard representa la organización de las funciones necesarias para el monitoreo de la bioincrustación en las mallas de las linternas utilizadas para el cultivo de concha de abanico (*Argopecten purpuratus*). A diferencia de la caja negra, este esquema permite identificar las funciones internas del sistema y las relaciones entre ellas mediante flujos de energía, materia, información y señales.

Como se muestra en la Figura 2, la propuesta se organiza en seis bloques funcionales: sensores, actuadores, control y procesamiento, módulo eléctrico, módulo mecánico y comunicación.

El **bloque de sensores** comprende la captura de imágenes submarinas mediante las cámaras Arducam Mega de 5 MP y el registro del movimiento del módulo sumergido mediante el acelerómetro LIS3DH. Asimismo, contempla la digitalización de las señales obtenidas y el envío de la información hacia el procesamiento. Estas funciones permiten disponer de fotografías de las regiones observadas de las mallas y de registros complementarios sobre el movimiento del dispositivo.

El **bloque de actuadores** considera el encendido de la iluminación LED para favorecer la captura de fotografías submarinas y la indicación del estado de encendido o apagado del sistema. Como salidas se representan la energía lumínica y la señal indicadora del estado de funcionamiento. Estas funciones corresponden a los mecanismos de iluminación y señalización previstos para LanternGuard.

El **bloque de control y procesamiento** contempla las funciones de monitorear el estado del sistema, gestionar los ciclos de trabajo y suspensión, identificar datos, sincronizar y validar la información de entrada, recibir fotografías y validar la calidad de las imágenes. Asimismo, incorpora la función de procesar y estimar la cobertura visible y el volumen de bioincrustación acumulada sobre las regiones observadas de las mallas. Para ello, el equipo propone desarrollar un algoritmo propio cuya metodología, requerimientos de información y precisión deberán establecerse y validarse en etapas posteriores. De acuerdo con la arquitectura conceptual de LanternGuard, el procesamiento de las fotografías completas se realizaría posteriormente en el servicio de procesamiento de imágenes, por lo que esta función se representa dentro del proceso general de control y procesamiento del sistema.

El **módulo eléctrico** contempla las funciones de captar y convertir la energía solar, regular la carga, almacenar energía, medir el nivel de batería y distribuir y proteger el suministro eléctrico. Asimismo, considera el acondicionamiento de energía para los sensores, actuadores, procesamiento y control, y comunicación. Estas funciones tienen como finalidad proporcionar la alimentación eléctrica necesaria para el funcionamiento de los componentes y las inspecciones programadas.

El **módulo mecánico** comprende las funciones de garantizar la hermeticidad subacuática, proteger los elementos electrónicos y sostener los componentes del dispositivo. También incorpora la función de reducir la adherencia de bioincrustación en la zona de captura, con el propósito de disminuir la acumulación de organismos sobre las superficies de protección de las cámaras y favorecer la obtención de fotografías. Esta función corresponde a una medida de protección del propio dispositivo y no implica que LanternGuard realice la limpieza de las mallas de cultivo. En este bloque, el agua de mar se representa como entrada y salida de materia, debido a las condiciones de operación del módulo sumergido.

Finalmente, el **bloque de comunicación** comprende las funciones de transmitir datos e imágenes hacia el servicio en la nube, confirmar el envío de información, actualizar el historial de inspecciones, gestionar reportes, administrar el aplicativo y notificar al usuario. En la arquitectura propuesta, los mensajes breves de estado y los metadatos de las inspecciones se transmitirían mediante LoRa, mientras que las fotografías completas se recuperarían mediante una transferencia local posterior, cuyo medio específico aún debe definirse, para su envío al servicio de procesamiento de imágenes. Como salidas se contemplan los datos e imágenes, los indicadores de bioincrustación y volumen estimado, y las señales de alerta de mantenimiento. Estas funciones se consideran conceptuales y deberán implementarse y validarse durante las siguientes etapas de desarrollo.

La Figura 2 presenta el esquema de funciones de LanternGuard, mostrando las relaciones entre los seis bloques funcionales y los flujos necesarios para su operación. Esta representación permite establecer una base para la elaboración de la matriz morfológica y la generación de alternativas de diseño.

<p align="center"><strong><em>Figura 2. Esquema de funciones del sistema LanternGuard.</em></strong></p>

<p align="center">
<img width="1254" height="1254" alt="image" src="https://github.com/user-attachments/assets/84184189-fc87-4736-9f15-76c560fe6dfd" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se representan los bloques de sensores, actuadores, control y procesamiento, módulo eléctrico, módulo mecánico y comunicación, así como sus relaciones mediante flujos de energía, materia, información y señales. El esquema incluye la captura de imágenes submarinas, el registro de movimiento mediante el acelerómetro LIS3DH, la protección de los componentes frente al entorno marino, la gestión energética y la estimación propuesta de cobertura visible y volumen de bioincrustación. Las funciones de estimación volumétrica, comunicación y notificación deberán desarrollarse y validarse en etapas posteriores.</em></p>

#### Matriz morfológica del sistema LanternGuard

La matriz morfológica de LanternGuard se elaboró a partir del análisis funcional del sistema, con la finalidad de identificar y comparar alternativas tecnológicas para el monitoreo de la bioincrustación en las mallas de las linternas utilizadas para el cultivo de concha de abanico (*Argopecten purpuratus*). Esta herramienta permite organizar las posibles soluciones de cada función y establecer combinaciones que orientan el diseño conceptual del dispositivo.

La matriz presenta 16 funciones distribuidas en seis módulos: sensores, actuadores, control y procesamiento, módulo eléctrico, módulo mecánico y comunicación. Para cada función se plantearon tres alternativas, denominadas Solución 1, Solución 2 y Solución 3, identificadas mediante códigos de portadores de función y representadas por líneas verticales de color rojo, verde y azul, respectivamente.

En el **módulo de sensores**, se presentan alternativas para registrar el movimiento y capturar imágenes submarinas. La Solución 1 contempla el acelerómetro LIS3DH y dos cámaras Arducam Mega de 5 MP con enfoque automático, componentes considerados en el diseño de LanternGuard.

El **módulo de actuadores** comprende la función de encender la iluminación durante las capturas fotográficas. Se comparan alternativas de iluminación LED, seleccionándose en la primera solución un aro LED de luz blanca para favorecer la observación de las regiones de las mallas.

En el **módulo de control y procesamiento**, se presentan alternativas para controlar el módulo sumergido, gestionar la comunicación y supervisión desde la boya, así como procesar la información obtenida. La Solución 1 contempla el ESP32-S3-DevKitC-1-N16R8 para el módulo sumergido y la placa Heltec WiFi LoRa 32 V3 para la boya. Asimismo, se considera la función de estimar la cobertura visible y el volumen de bioincrustación mediante un algoritmo propio. De acuerdo con la arquitectura conceptual, el análisis de las fotografías completas se realizaría posteriormente en un servicio de procesamiento, cuyo desarrollo y validación están pendientes.

La matriz también considera la **gestión de los ciclos de trabajo y suspensión**, proponiendo en la primera solución inspecciones periódicas mediante programación temporal y modos de ahorro energético. Esta función permitirá organizar la activación del sistema durante los periodos previstos para la adquisición de información.

En el **módulo eléctrico**, se comparan alternativas de almacenamiento y acondicionamiento de energía. La propuesta contempla una batería recargable de ion-litio, circuitos de regulación eléctrica y el aprovechamiento de energía solar para contribuir a la alimentación del sistema. La configuración definitiva de la gestión energética deberá completarse y verificarse durante el desarrollo de la propuesta.

El **módulo mecánico** comprende las funciones de sostener y proteger los componentes, garantizar la hermeticidad subacuática, reducir la adherencia de bioincrustación y mantener las condiciones de las ventanas ópticas. Para la fabricación de la carcasa se consideran PETG, ABS y ASA. El equipo seleccionó PETG como material de referencia por su disponibilidad, facilidad de fabricación mediante impresión 3D y conveniencia económica para el proyecto. Asimismo, se plantean alternativas de ventanas transparentes y tratamientos superficiales destinados a disminuir la adherencia de organismos incrustantes sobre las zonas de captura. La eficacia y compatibilidad de estos tratamientos deberán evaluarse posteriormente.

Finalmente, el **módulo de comunicación** contempla alternativas para transmitir información, almacenar registros y notificar al usuario. La arquitectura seleccionada de LanternGuard utiliza comunicación LoRa para enviar mensajes breves y metadatos de las inspecciones, mientras que las fotografías completas se conservarían para una transferencia local posterior, cuyo medio específico aún debe definirse. También se propone utilizar almacenamiento microSD y un aplicativo LanternGuard para visualizar la información obtenida. Como alternativas de presentación se consideran un dashboard web y un bot de WhatsApp.

Las tres soluciones se representan mediante rutas verticales que permiten identificar las alternativas correspondientes a cada función. La tabla inferior presenta la secuencia de códigos de los portadores de función utilizados en cada combinación.

De las alternativas planteadas, el equipo adoptó la **Solución 1** como base del diseño conceptual de LanternGuard, considerando la compatibilidad de sus principales componentes con la arquitectura propuesta, su disponibilidad y las condiciones económicas del proyecto. Esta selección orienta los modelos tridimensionales y los diseños electrónicos presentados en los siguientes apartados.

La Figura 3 presenta la matriz morfológica de LanternGuard, mostrando las funciones consideradas, las alternativas tecnológicas propuestas y las tres rutas de solución.

<p align="center"><strong><em>Figura 3. Matriz morfológica del sistema LanternGuard.</em></strong></p>

<p align="center">
<img width="1133" height="1388" alt="image" src="https://github.com/user-attachments/assets/a02a78c8-6fab-4a22-adc0-afaa2d7d666d" />
</p>
<p align="center"><em><strong>Nota.</strong> Elaboración propia. La matriz presenta 16 funciones organizadas en seis módulos funcionales, con tres alternativas de solución para cada función. Las líneas roja, verde y azul representan las combinaciones propuestas. La Solución 1 corresponde a la configuración elegida como referencia por el equipo. La estimación volumétrica, los tratamientos de protección superficial y determinados aspectos de comunicación y gestión energética requieren desarrollo o validación posterior.</em></p>

#### Boceto 1 - Solución preliminar 1

El primer boceto representa la configuración conceptual de LanternGuard correspondiente a la Solución 1 de la matriz morfológica. Se muestra la integración de una boya de superficie con un módulo sumergido instalado sobre una linterna de cultivo de concha de abanico (*Argopecten purpuratus*), así como los principales componentes electrónicos, estructurales y de comunicación considerados en la propuesta.

**Descripción técnica y funcional:**

* **Estrategia de muestreo:**
  * Inspecciones periódicas programadas cada 15 días, con una duración aproximada de cinco minutos para la adquisición de información.
  * Uso previsto de temporización y modos de bajo consumo energético (*deep sleep*) entre inspecciones.

* **Boya de superficie (nodo boya):**
  * **Alimentación:** Panel solar, baterías recargables de ion-litio 18650 y circuitos de regulación y gestión energética. Se contempla el regulador LM2596 para acondicionamiento de tensión; la configuración definitiva de carga solar deberá completarse.
  * **Control y comunicación:** Placa Heltec WiFi LoRa 32 V3, que integra un microcontrolador ESP32-S3 y un transceptor LoRa SX1262.
  * **Programación:** Reloj de tiempo real DS3231 para coordinar las inspecciones.
  * **Control de alimentación:** Interruptor de encendido y apagado.
  * **Comunicación con el módulo sumergido:** Enlace cableado RS-485 mediante transceptores MAX3485 y cable umbilical.
  * **Telemetría:** Transmisión de mensajes breves, estados y metadatos de inspección mediante LoRa hacia una estación receptora terrestre.

* **Barra y módulo sumergido (nodo sumergido):**
  * **Control:** Microcontrolador ESP32-S3-DevKitC-1-N16R8, ubicado dentro de un compartimento electrónico protegido.
  * **Registro de movimiento:** Acelerómetro triaxial LIS3DH para obtener información complementaria sobre el movimiento y la inclinación del módulo.
  * **Almacenamiento:** Módulo microSD mediante interfaz SPI para almacenar las fotografías y los registros obtenidos durante las inspecciones.
  * **Comunicación interna:** Cable umbilical RS-485 para la transferencia de información entre el módulo sumergido y la boya.
  * **Estructura:** Barra de soporte y piezas estructurales fabricables mediante impresión 3D con material PETG.
  * **Protección:** Compartimento electrónico estanco y medidas de protección frente al ambiente marino.

* **Cápsulas de cámara:**
  * **Captura de imágenes:** Dos cámaras Arducam Mega de 5 MP con enfoque automático, orientadas hacia diferentes regiones de las mallas.
  * **Posicionamiento:** Soportes de cámara que permiten establecer las orientaciones de captura previstas en el diseño.
  * **Iluminación:** Aros LED de luz blanca para favorecer la adquisición de fotografías submarinas.
  * **Protección óptica:** Ventanas transparentes de acrílico y elementos de sellado mediante juntas O-ring.
  * **Protección superficial:** Aplicación propuesta de un tratamiento antifouling y de un recubrimiento transparente hidrofóbico para reducir la adherencia de organismos y favorecer las condiciones de las ventanas ópticas. Su eficacia deberá evaluarse posteriormente.

* **Comunicación, procesamiento y visualización:**
  * **Recepción terrestre:** Estación receptora basada en Heltec WiFi LoRa 32 V3 para recibir los mensajes transmitidos desde la boya.
  * **Fotografías completas:** Almacenamiento y recuperación mediante una transferencia local posterior, cuyo procedimiento específico aún debe definirse.
  * **Procesamiento de imágenes:** Servicio de procesamiento destinado a estimar el porcentaje de cobertura visible de bioincrustación y desarrollar un algoritmo propio para estimar el volumen acumulado en las regiones analizadas.
  * **Notificación al usuario:** Aplicativo LanternGuard para visualizar fotografías, resultados e historial de inspecciones, sin limitar su uso exclusivamente a dispositivos móviles.

La Solución preliminar 1 constituye la alternativa seleccionada por el equipo como base para el diseño conceptual de LanternGuard. Su configuración permite integrar las funciones de adquisición de imágenes submarinas, registro de movimiento, alimentación, protección estructural y comunicación, orientadas al monitoreo periódico de la bioincrustación.

<p align="center"><strong><em>Figura 4. Boceto de la Solución preliminar 1 del sistema LanternGuard.</em></strong></p>

<p align="center">
 <img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/a5e23aaf-b8f5-4b65-97db-a3880adfd248" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se presenta la vista general de LanternGuard y los detalles conceptuales de la boya de superficie, el módulo sumergido y la cápsula de cámara. El boceto corresponde a la Solución 1 de la matriz morfológica y considera los componentes y materiales seleccionados por el equipo. Las funciones de estimación volumétrica, gestión energética y recuperación local de fotografías requieren desarrollo o validación posterior.</em></p>

#### Boceto 2 - Solución preliminar 2

El segundo boceto representa una alternativa conceptual de LanternGuard basada en la Solución 2 de la matriz morfológica. Conserva la organización general del sistema mediante una boya de superficie y un módulo sumergido conectado por cable umbilical, pero plantea diferentes componentes electrónicos, materiales y mecanismos de adquisición, procesamiento y comunicación.

**Descripción técnica y funcional:**

* **Estrategia de muestreo:** Muestreo por umbral, basado en la activación del sistema ante un evento previamente definido. La condición de activación y sus parámetros deberán establecerse y validarse posteriormente.

* **Boya de superficie (nodo boya):**
  * **Alimentación:** Batería Li-Po de 10 000 mAh y módulo BMS para protección y gestión de la batería.
  * **Control y procesamiento:** Raspberry Pi Zero 2 W, considerada para supervisar las funciones de la boya y realizar procesamiento local de la información.
  * **Telemetría:** Módulo LoRa SX1276 para transmitir mensajes breves y metadatos hacia una estación receptora terrestre.
  * **Comunicación interna:** Enlace RS-485 mediante cable umbilical con el módulo sumergido.
  * **Visualización:** Dashboard web para consultar los resultados del monitoreo.

* **Barra y módulo sumergido (nodo sumergido):**
  * **Control:** Microcontrolador ESP32-WROOM-32U alojado en un compartimento electrónico protegido.
  * **Registro de movimiento:** Sensor inercial MPU-6050 para obtener información de aceleración y movimiento durante las inspecciones.
  * **Almacenamiento:** Memoria Flash W25Q128 como alternativa de almacenamiento electrónico, cuya capacidad disponible y suficiencia deberán evaluarse.
  * **Estructura y protección:** Carcasa fabricable mediante impresión 3D en ABS, con recubrimiento de resina epóxica como alternativa de protección superficial.
  * **Comunicación:** Transferencia de información hacia la boya mediante RS-485.

* **Cápsulas de cámara:**
  * **Captura:** Dos cámaras Arducam Mega de 5 MP con lente M12, orientadas hacia diferentes regiones de las mallas.
  * **Iluminación:** Módulos LED infrarrojos para apoyar la adquisición de imágenes, cuya compatibilidad con las cámaras deberá verificarse.
  * **Protección óptica:** Ventanas de vidrio templado marino y sellado mediante juntas O-ring.
  * **Tratamiento superficial:** Film hidrofóbico PET como alternativa para reducir la acumulación de agua y suciedad sobre las ventanas ópticas, pendiente de evaluación en condiciones submarinas.

* **Procesamiento y comunicación:**
  * **Procesamiento local:** Se contempla utilizar la Raspberry Pi Zero 2 W para desarrollar procedimientos de análisis de imágenes orientados a estimar la cobertura visible y el volumen de bioincrustación.
  * **Transmisión inalámbrica:** LoRa se utilizaría para mensajes breves y metadatos, mientras que las fotografías completas requerirían un procedimiento de transferencia local.
  * **Notificación:** Dashboard web para visualizar indicadores, registros e historial de inspecciones.

Esta alternativa utiliza componentes y materiales distintos de los seleccionados para el diseño principal de LanternGuard. Su representación permite comparar las posibilidades técnicas de la Solución 2 frente a las demás alternativas de la matriz morfológica.

<p align="center"><strong><em>Figura 5. Boceto de la Solución preliminar 2 del sistema LanternGuard.</em></strong></p>

<p align="center">
  <img width="1672" height="941" alt="image" src="https://github.com/user-attachments/assets/b66c5076-6e49-4c28-863a-85913905350e" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se presenta la alternativa de diseño correspondiente a la Solución 2 de la matriz morfológica, considerando sus componentes electrónicos, materiales estructurales y funciones propuestas. Las características de procesamiento, comunicación y protección óptica deberán evaluarse y validarse durante etapas posteriores.</em></p>

### 3.4. Representación del modelado tridimensional

Como parte del diseño conceptual de LanternGuard, se desarrolló un modelo tridimensional que representa la configuración estructural del módulo sumergido, la boya de superficie y su integración mediante un cable umbilical. El modelado permite visualizar la distribución de los componentes, los sistemas de soporte y la disposición física de los elementos que conforman la propuesta tecnológica.

#### 3.4.1. Diseño tridimensional del módulo sumergido

El módulo sumergido de LanternGuard se diseñó para posicionarse sobre la linterna de cultivo y realizar la captura periódica de imágenes submarinas y mediciones complementarias. Su estructura presenta un compartimento central destinado a alojar la electrónica de control, incluyendo el ESP32-S3-DevKitC-1-N16R8, los componentes de comunicación y almacenamiento, así como las conexiones de los sensores.

El diseño incorpora dos brazos laterales que permiten ubicar las cámaras Arducam Mega de 5 MP con diferentes orientaciones hacia regiones de las mallas. Asimismo, se contempla la integración del acelerómetro LIS3DH para obtener información sobre el movimiento del dispositivo durante las inspecciones.

Una característica importante del modelo es su sistema de sujeción, conformado por elementos de enganche que permiten fijar el módulo a la estructura de la linterna. Esta disposición busca mantener una posición de observación consistente y reducir los desplazamientos que podrían modificar los ángulos de captura entre inspecciones.

En la representación se incluye un cilindro gris que simula la linterna de cultivo y permite visualizar el acoplamiento del dispositivo. Este cilindro no forma parte de las piezas que se fabricarán, ya que se utiliza únicamente como referencia para representar la instalación del módulo. Las piezas estructurales del dispositivo destinadas a impresión 3D se desarrollarán utilizando PETG.

<p align="center"><strong><em>Figura 7. Modelo tridimensional del módulo sumergido de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/5a6a724f-c839-4907-ae4e-fec3eb274d64" alt="Modelo tridimensional del módulo sumergido" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se muestra la configuración estructural del módulo sumergido, la disposición de las cámaras y los elementos de sujeción respecto a la linterna de cultivo representada mediante el cilindro gris.</em></p>

#### 3.4.2. Diseño tridimensional de la boya de superficie

La boya de superficie de LanternGuard se diseñó para mantener sobre el agua los componentes encargados de la gestión energética, programación de inspecciones y comunicación con la estación receptora terrestre. Su estructura integra un compartimento central para la electrónica, un soporte superior para el panel solar y elementos laterales destinados a proporcionar flotabilidad al conjunto.

En la parte superior se ubica el panel solar, cuya función será captar energía para contribuir a la alimentación eléctrica del sistema. Debajo de este se encuentra el compartimento destinado a alojar la PCB personalizada de la boya, que integra el módulo Heltec WiFi LoRa 32 V3, el transceptor MAX3485 y las conexiones del reloj de tiempo real DS3231, junto con los elementos asociados a la alimentación eléctrica.

El modelo incorpora elementos cilíndricos laterales destinados a mejorar la flotabilidad y contribuir a la estabilidad de la estructura. Estos flotadores se integrarán mediante soportes de fijación que permitirán mantenerlos sujetos al conjunto. Los elementos flotantes serán componentes independientes, mientras que los soportes y las piezas estructurales se fabricarán mediante impresión 3D utilizando PETG.

Esta configuración permite organizar los componentes de superficie en una estructura que integra las funciones de alimentación, control y comunicación de la boya, manteniendo el compartimento electrónico separado del contacto directo con el agua.

<p align="center"><strong><em>Figura 8. Modelo tridimensional de la boya de superficie de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/87f4c021-e6ef-4b26-bffe-4bd2f1af378d" alt="Modelo tridimensional de la boya de superficie" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se presenta la distribución del panel solar, el compartimento electrónico, los soportes estructurales y los elementos laterales de flotación. Las piezas estructurales destinadas a impresión 3D se desarrollarán en PETG.</em></p>

#### 3.4.3. Diseño tridimensional del sistema completo LanternGuard

El modelo tridimensional del sistema completo representa la integración de la boya de superficie y el módulo sumergido mediante un cable umbilical. Esta configuración permite visualizar la relación física entre ambos subsistemas y la distribución de las funciones tecnológicas de LanternGuard.

La boya permanecerá en la superficie del agua, donde se concentrarán las funciones de gestión energética, programación temporal y comunicación inalámbrica. Por su parte, el módulo sumergido se instalará sobre la linterna de cultivo mediante su sistema de sujeción, con la finalidad de capturar imágenes de las mallas y registrar mediciones complementarias.

El cable umbilical establecerá la conexión física entre ambos módulos, permitiendo la transferencia de información mediante comunicación RS-485. De esta manera, el diseño integra las funciones de adquisición submarina y gestión de información en superficie dentro de una misma arquitectura tecnológica.

<p align="center"><strong><em>Figura 9. Modelo tridimensional del sistema completo LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b8ed4069-34f3-413c-84da-51e8caa14c2f" alt="Modelo tridimensional del sistema completo" width="360" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Se muestra la integración de la boya de superficie y el módulo sumergido, unidos mediante el cable umbilical, de acuerdo con la configuración estructural propuesta para LanternGuard.</em></p>

### 3.4.4. Planos dimensionales de los componentes estructurales de LanternGuard

Como complemento del modelado tridimensional, se presentan los planos dimensionales de los componentes estructurales de LanternGuard. Estos documentos técnicos permiten identificar las características geométricas de las piezas, sus dimensiones, perforaciones y elementos de fijación, proporcionando información para orientar su fabricación y posterior ensamblaje.

Los planos incluyen vistas ortogonales e isométricas, cotas expresadas en milímetros y especificaciones relacionadas con el material y la cantidad requerida de cada componente. Esta documentación complementa la representación conceptual del sistema y facilita la identificación de las características constructivas de las piezas diseñadas.

#### 3.4.4.1. Planos dimensionales de la boya de superficie

Los siguientes planos corresponden a componentes estructurales de la boya de superficie de LanternGuard. Se presentan individualmente las piezas B1_casco, B2_cubierta, B3_caja y B4_tapa, fabricables mediante impresión 3D utilizando material PETG.

Cada plano contiene las vistas y cotas necesarias para describir la geometría de la pieza, así como los detalles de sus perforaciones, soportes y puntos de unión. De acuerdo con los cajetines de los cuatro planos, se requiere una unidad de cada componente.

##### 3.4.4.1.1. Plano dimensional de la pieza B1_casco

La pieza **B1_casco** presenta una estructura abierta conformada por una base, elementos laterales y divisiones verticales. Su geometría incorpora aberturas poligonales distribuidas en los laterales, así como ranuras y perforaciones ubicadas en diferentes zonas de la pieza.

El plano muestra las vistas ortogonales e isométricas, con una dimensión longitudinal principal de 254 mm y cotas adicionales que permiten identificar la distribución y separación de sus elementos estructurales. También se detallan las características de las aberturas y los puntos de fijación previstos en el diseño. Esta información proporciona una referencia técnica para su fabricación e integración en el conjunto de la boya de superficie.

<p align="center">
  <strong><em>Figura 10. Plano dimensional de la pieza B1_casco de la boya de superficie de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/62168797-64c9-4a5d-81d2-fd60a1c1dd78"
       alt="Plano dimensional de la pieza B1_casco"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones principales, aberturas geométricas y detalles de fijación de la pieza B1_casco. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.1.2. Plano dimensional de la pieza B2_cubierta

La pieza **B2_cubierta** presenta una configuración estructural abierta, formada por barras longitudinales y transversales que delimitan espacios interiores. Su diseño incorpora elementos verticales de soporte, perforaciones distribuidas en las barras y detalles geométricos en las uniones de la estructura.

El plano incluye las vistas ortogonales e isométricas, con dimensiones generales de 254 mm y 225,6 mm en planta, además de cotas correspondientes a la separación, disposición y características de sus elementos. También se indican perforaciones y detalles de acabado, como chaflanes en determinadas uniones. Esta documentación permite identificar las características constructivas de la pieza para su posterior fabricación e integración con los demás elementos de la boya.

<p align="center">
  <strong><em>Figura 11. Plano dimensional de la pieza B2_cubierta de la boya de superficie de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e1c05a38-a533-4c50-b44e-9ffdc9ebd91a"
       alt="Plano dimensional de la pieza B2_cubierta"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se muestran las vistas ortogonales e isométricas, dimensiones, barras estructurales, soportes verticales, perforaciones y detalles de unión de la pieza B2_cubierta. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.1.3. Plano dimensional de la pieza B3_caja

La pieza **B3_caja** presenta un compartimento de geometría rectangular, abierto en su parte superior y provisto de un borde perimetral. Su configuración incorpora paredes laterales, elementos internos de soporte, perforaciones y puntos de fijación distribuidos en diferentes zonas del compartimento.

El plano establece dimensiones exteriores principales de **166,8 mm de largo, 116,8 mm de ancho y 74,4 mm de alto**. Asimismo, presenta detalles de las perforaciones, soportes internos y elementos de montaje que deberán considerarse durante su fabricación y ensamblaje. Estas características permiten definir la geometría del compartimento y su integración estructural dentro de la boya de superficie.

<p align="center">
  <strong><em>Figura 12. Plano dimensional de la pieza B3_caja de la boya de superficie de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/84b62519-172c-4f24-8a99-2e2bbe104586"
       alt="Plano dimensional de la pieza B3_caja"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones exteriores, soportes internos y puntos de fijación de la pieza B3_caja. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.1.4. Plano dimensional de la pieza B4_tapa

La pieza **B4_tapa** presenta una geometría rectangular de perfil delgado, con esquinas redondeadas y perforaciones distribuidas alrededor de su perímetro. Su configuración corresponde a un elemento de cierre que contempla puntos de fijación para su integración con un compartimento estructural.

El plano muestra las vistas de la pieza y una representación isométrica, incluyendo cotas correspondientes a su geometría, espesor y ubicación de las perforaciones. También se indican radios de redondeo en las esquinas y dimensiones relacionadas con la distribución de los puntos de fijación. Esta información permite establecer las características necesarias para su fabricación mediante impresión 3D y su posterior montaje.

<p align="center">
  <strong><em>Figura 13. Plano dimensional de la pieza B4_tapa de la boya de superficie de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/f4e3a1dc-f382-4bd7-8876-acbada48378c"
       alt="Plano dimensional de la pieza B4_tapa"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se muestran las vistas y representación isométrica, geometría, espesor, esquinas redondeadas y perforaciones de fijación de la pieza B4_tapa. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.1.5. Plano dimensional de la pieza B5_cuna

La pieza **B5_cuna** presenta una estructura abierta y alargada, conformada por paredes laterales, divisiones internas y elementos verticales de soporte. Su diseño incorpora aberturas poligonales distribuidas en las paredes, así como perforaciones y elementos de fijación ubicados en diferentes zonas de la estructura.

El plano muestra las vistas ortogonales e isométricas, con una longitud principal de **254 mm**, una altura de **85,4 mm** y otras cotas que permiten identificar la geometría y disposición de sus elementos. Asimismo, se indican detalles constructivos relacionados con los soportes y chaflanes de la base. Esta información proporciona una referencia técnica para la fabricación de la pieza y su integración en el conjunto estructural de la boya de superficie.

<p align="center">
  <strong><em>Figura 14. Plano dimensional de la pieza B5_cuna de la boya de superficie de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/537b7afa-2499-469e-8b2c-0c51b316aee7"
       alt="Plano dimensional de la pieza B5_cuna"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones principales, aberturas laterales, elementos de soporte y perforaciones de fijación de la pieza B5_cuna. Material: PETG. Cantidad requerida: 2 unidades. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.1.6. Plano dimensional de la pieza B6_correa

La pieza **B6_correa** presenta una geometría prismática rectangular y alargada, con dos perforaciones circulares situadas cerca de sus extremos. Su configuración corresponde a un elemento estructural sencillo que dispone de puntos de fijación para su integración con otros componentes del conjunto.

El plano incluye vistas ortogonales e isométricas que permiten identificar sus dimensiones de **103,8 mm de longitud, 14 mm de ancho y 4 mm de espesor**. Asimismo, se especifican dos perforaciones de **3,4 mm de diámetro**, cuya disposición se representa en el dibujo técnico. Estas características proporcionan la información geométrica necesaria para orientar su fabricación mediante impresión 3D.

<p align="center">
  <strong><em>Figura 15. Plano dimensional de la pieza B6_correa de la boya de superficie de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/0149ba69-3b40-41d2-ab2c-29bf16fc1ff0"
       alt="Plano dimensional de la pieza B6_correa"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se muestran las vistas ortogonales e isométricas de la pieza B6_correa, con dimensiones de 103,8 × 14 × 4 mm y dos perforaciones de 3,4 mm de diámetro. Material: PETG. Cantidad requerida: 4 unidades. Cotas expresadas en milímetros.</em>
</p>

#### 3.4.4.2. Planos dimensionales del módulo sumergido

A continuación, se presentan los planos dimensionales de los componentes estructurales correspondientes al módulo sumergido de LanternGuard. Estos documentos permiten identificar la geometría de las piezas, las dimensiones principales, las perforaciones y los elementos de fijación considerados en su diseño.

Los planos complementan la representación tridimensional del módulo sumergido y proporcionan información técnica para orientar la fabricación mediante impresión 3D y el posterior ensamblaje de sus componentes.

##### 3.4.4.2.1. Plano dimensional de la pieza M1s_caja_cuerpo

La pieza **M1s_caja_cuerpo** presenta un compartimento de geometría rectangular, abierto en su parte superior y provisto de un borde perimetral con perforaciones de fijación. Su configuración incorpora paredes laterales, elementos internos de soporte, una sección inferior sobresaliente y un elemento lateral con una abertura circular y perforaciones para montaje.

El plano muestra vistas ortogonales e isométricas, con dimensiones generales de **147 mm por 146 mm en planta y una altura de 107 mm**. Asimismo, se especifican perforaciones de diferentes diámetros, elementos internos de soporte y detalles geométricos relacionados con el montaje del compartimento. Estos elementos proporcionan información sobre la configuración estructural prevista para la pieza y su integración con otros componentes del módulo sumergido.

<p align="center">
  <strong><em>Figura 16. Plano dimensional de la pieza M1s_caja_cuerpo del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/9605dd6c-c475-42f4-9f9c-dc9833000f8b"
       alt="Plano dimensional de la pieza M1s_caja_cuerpo"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones generales, borde perimetral, elementos internos de soporte y perforaciones de fijación de la pieza M1s_caja_cuerpo. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.2. Plano dimensional de la pieza M2_caja_tapa

La pieza **M2_caja_tapa** presenta una placa de geometría rectangular, con esquinas redondeadas y perforaciones distribuidas alrededor de su perímetro. Sobre una de sus superficies incorpora una estructura elevada de soporte, conformada por un elemento transversal con refuerzos laterales y una sección circular perforada en su parte superior.

El plano muestra las vistas ortogonales e isométricas, con dimensiones principales de **135 mm por 134 mm en planta**. También se especifica una perforación circular de **12,6 mm de diámetro**, situada fuera del centro de la placa, así como perforaciones de fijación de **3,4 mm de diámetro** en el perímetro. La estructura elevada presenta, además, una sección circular con diámetros indicados de **20 mm y 10 mm**. Estos detalles permiten reconocer la geometría de la tapa y los elementos considerados para su fabricación y posterior montaje.

<p align="center">
  <strong><em>Figura 17. Plano dimensional de la pieza M2_caja_tapa del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/85b6309f-a0a8-40bf-b3c5-26f0563591e9"
       alt="Plano dimensional de la pieza M2_caja_tapa"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones principales, perforaciones de fijación y geometría de la estructura elevada de la pieza M2_caja_tapa. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.3. Plano dimensional de la pieza M3s_riel_gancho

La pieza **M3s_riel_gancho** presenta una estructura alargada de sección rectangular, con una placa de fijación en uno de sus extremos y un elemento inferior terminado en forma de gancho abierto. Su diseño incorpora aberturas triangulares distribuidas en las caras laterales del cuerpo principal, además de perforaciones circulares y una abertura en la zona frontal de la estructura.

El plano muestra las vistas ortogonales e isométricas, con una longitud total de **141,5 mm** y una cota de **30 mm** correspondiente a la altura de una de las caras del cuerpo longitudinal. Asimismo, se indican perforaciones de **4,2 mm de diámetro**, una abertura circular frontal de **8 mm de diámetro** y radios que permiten definir la geometría del gancho inferior. Estas características proporcionan información para la fabricación de la pieza y su posterior integración en el conjunto estructural del módulo sumergido.

<p align="center">
  <strong><em>Figura 18. Plano dimensional de la pieza M3s_riel_gancho del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/a306688f-f00e-4f7e-b8e0-64d4f88bde7f"
       alt="Plano dimensional de la pieza M3s_riel_gancho"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones principales, aberturas triangulares, perforaciones de fijación y geometría del gancho de la pieza M3s_riel_gancho. Material: PETG. Cantidad requerida: 2 unidades. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.4. Plano dimensional de la pieza M3t_tapa_bolsillo

La pieza **M3t_tapa_bolsillo** presenta una geometría rectangular de perfil delgado, con superficies planas y dos perforaciones circulares ubicadas cerca de sus extremos. Su configuración corresponde a una placa destinada a integrarse con otros elementos del conjunto mediante los puntos de fijación representados en el plano.

El dibujo técnico incluye vistas ortogonales e isométricas, con dimensiones principales de **117 mm de longitud y 57 mm de ancho**. Asimismo, se especifican dos perforaciones de **3,4 mm de diámetro**, acompañadas de detalles circulares concéntricos acotados con un diámetro de **6,72 mm**. Estas características permiten identificar la geometría de la pieza y los detalles necesarios para orientar su fabricación y posterior ensamblaje.

<p align="center">
  <strong><em>Figura 19. Plano dimensional de la pieza M3t_tapa_bolsillo del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/a96de4f3-b913-49fa-9fa1-155e552397c5"
       alt="Plano dimensional de la pieza M3t_tapa_bolsillo"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se muestran las vistas ortogonales e isométricas, dimensiones de la placa y detalles de sus dos puntos de fijación. Material: PETG. Cantidad requerida: 2 unidades. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.5. Plano dimensional de la pieza M4_capsula_cuerpo

La pieza **M4_capsula_cuerpo** presenta una estructura hueca de geometría prismática rectangular, conformada por un cuerpo posterior y una placa frontal cuadrada con esquinas redondeadas. La placa incorpora cuatro perforaciones distribuidas en sus esquinas, mientras que el interior del cuerpo presenta una cavidad y elementos de geometría circular. También se observa una perforación circular en una de las paredes laterales.

El plano incluye vistas ortogonales e isométricas, con dimensiones de **56 mm por 56 mm** para la placa frontal y una extensión posterior acotada de **38 mm**. Asimismo, se especifican perforaciones de fijación de **3,4 mm de diámetro**, una perforación lateral de **12,6 mm de diámetro** y detalles circulares interiores con diámetros de **26 mm y 30,4 mm**. Estas especificaciones permiten definir la geometría de la pieza y los elementos considerados para su fabricación e integración con otros componentes del módulo sumergido.

<p align="center">
  <strong><em>Figura 20. Plano dimensional de la pieza M4_capsula_cuerpo del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/91754ce8-8c18-4ff7-b52b-438fe0708653"
       alt="Plano dimensional de la pieza M4_capsula_cuerpo"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones de la placa frontal, cavidad interior, perforaciones y detalles geométricos de la pieza M4_capsula_cuerpo. Material: PETG. Cantidad requerida: 2 unidades. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.6. Plano dimensional de la pieza M5_capsula_tapa_pie

La pieza **M5_capsula_tapa_pie** presenta una configuración estructural compuesta por una placa rectangular con abertura interior, un elemento de soporte inclinado y una sección superior en forma de U. Esta última está conformada por dos paredes paralelas unidas mediante una base, con perforaciones circulares ubicadas en las paredes laterales. La placa inferior incorpora, además, perforaciones distribuidas alrededor de su perímetro.

El plano muestra vistas ortogonales e isométricas que permiten identificar la disposición de estos elementos y sus dimensiones. Entre las cotas principales se encuentran **50 mm** de ancho y **36 mm** de altura para la sección superior, una altura de **48,5 mm** para la placa rectangular y una longitud acotada de **57,38 mm** en uno de los elementos inclinados. Asimismo, se especifican dos perforaciones de **4,2 mm de diámetro** en la sección superior. Esta información proporciona una referencia para la fabricación de la pieza y su posterior integración estructural en el módulo sumergido.

<p align="center">
  <strong><em>Figura 21. Plano dimensional de la pieza M5_capsula_tapa_pie del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/7b2008ac-7305-4777-a113-7431c3c239b7"
       alt="Plano dimensional de la pieza M5_capsula_tapa_pie"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones, placa rectangular, soporte inclinado y sección superior en forma de U de la pieza M5_capsula_tapa_pie. Material: PETG. Cantidad requerida: 2 unidades. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.7. Plano dimensional de la pieza M6_capsula_bisel

La pieza **M6_capsula_bisel** presenta una geometría anular, conformada por un contorno exterior circular y una abertura central concéntrica. Su diseño incorpora tres perforaciones circulares distribuidas alrededor de la superficie del anillo, las cuales constituyen puntos de fijación para su integración con otros elementos del conjunto.

El plano muestra vistas ortogonales e isométricas que permiten identificar un diámetro exterior de **42 mm**, un diámetro interior de **28 mm** y un espesor de **2,5 mm**. Asimismo, se especifican tres perforaciones de **2,4 mm de diámetro**. Estas características permiten definir la geometría y los detalles de fijación de la pieza para orientar su fabricación mediante impresión 3D.

<p align="center">
  <strong><em>Figura 22. Plano dimensional de la pieza M6_capsula_bisel del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b9b9b8ea-0644-4ff0-afb5-06fb3bdf7598"
       alt="Plano dimensional de la pieza M6_capsula_bisel"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, diámetros exterior e interior, espesor y tres perforaciones de fijación de la pieza M6_capsula_bisel. Material: PETG. Cantidad requerida: 2 unidades. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.8. Plano dimensional de la pieza M11_bandeja

La pieza **M11_bandeja** presenta una estructura formada por una placa de base, cuatro soportes cilíndricos ubicados cerca de sus esquinas y una abertura central de geometría compuesta por dos regiones circulares unidas. Su contorno incorpora dos escotaduras rectangulares situadas en lados opuestos, mientras que los soportes presentan perforaciones longitudinales destinadas a proporcionar puntos de fijación.

El plano incluye vistas ortogonales e isométricas, con una dimensión principal acotada de **111 mm** y una altura de **27 mm** correspondiente al conjunto representado en la vista lateral. Asimismo, se especifican cuatro soportes con diámetro exterior de **8 mm** y perforaciones de **3,4 mm de diámetro**, además de radios de **13,66 mm** para las regiones curvas de la abertura central. Estas características permiten identificar la distribución de los elementos estructurales y los detalles geométricos considerados para su fabricación y ensamblaje.

<p align="center">
  <strong><em>Figura 23. Plano dimensional de la pieza M11_bandeja del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/a16b8732-d6bb-422b-a18c-c2c063e51677"
       alt="Plano dimensional de la pieza M11_bandeja"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se muestran las vistas ortogonales e isométricas, dimensiones, cuatro soportes cilíndricos, abertura central y escotaduras laterales de la pieza M11_bandeja. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.9. Plano dimensional de la pieza M11_bandeja_sup

La pieza **M11_bandeja_sup** presenta una geometría de placa plana con esquinas ligeramente redondeadas y dos escotaduras rectangulares ubicadas en lados opuestos. Su diseño incorpora cuatro perforaciones circulares distribuidas cerca de las esquinas, que constituyen puntos de fijación para su integración con otros componentes estructurales.

El plano muestra vistas ortogonales e isométricas, con una dimensión principal de **111 mm**, un espesor de **3 mm** y cuatro perforaciones de **3,4 mm de diámetro**. Asimismo, se incluyen cotas para la ubicación y dimensiones de las escotaduras laterales, entre ellas una abertura acotada de **21,32 mm**. Estos detalles permiten definir la geometría de la placa y proporcionar una referencia técnica para su fabricación y posterior montaje.

<p align="center">
  <strong><em>Figura 24. Plano dimensional de la pieza M11_bandeja_sup del módulo sumergido de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/51b40b00-5495-4dac-b2d3-5a6f171a58fe"
       alt="Plano dimensional de la pieza M11_bandeja_sup"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se presentan las vistas ortogonales e isométricas, dimensiones principales, espesor, escotaduras laterales y cuatro perforaciones de fijación de la pieza M11_bandeja_sup. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

##### 3.4.4.2.10. Plano dimensional de la pieza SKIN_concha_v1

La pieza **SKIN_concha_v1** presenta una geometría de placa rectangular con esquinas redondeadas, perforaciones distribuidas alrededor de su perímetro y elementos gráficos integrados en una de sus superficies. El diseño incorpora los textos **UPCH** y **LanternGuard**, una región rectangular delimitada y una composición geométrica radial que representa de manera estilizada una concha de abanico.

El plano muestra vistas ortogonales e isométricas, con dimensiones exteriores de **135 mm de ancho y 134 mm de alto**. Asimismo, se presenta una región rectangular acotada de **51,16 mm por 36 mm**, junto con relieves y elementos geométricos distribuidos en la zona inferior de la placa. La representación permite identificar las características dimensionales y visuales de esta pieza complementaria, considerada para su fabricación mediante impresión 3D.

<p align="center">
  <strong><em>Figura 25. Plano dimensional de la pieza SKIN_concha_v1 de LanternGuard.</em></strong>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/cf48c53e-9e03-412f-9d45-9cd1c82fbb45"
       alt="Plano dimensional de la pieza SKIN_concha_v1"
       width="850" />
</p>

<p align="center">
  <em><strong>Nota.</strong> Elaboración propia. Se muestran las vistas ortogonales e isométricas, dimensiones exteriores, perforaciones perimetrales y elementos gráficos de la pieza SKIN_concha_v1, incluyendo los textos UPCH y LanternGuard y la representación estilizada de una concha de abanico. Material: PETG. Cantidad requerida: 1 unidad. Cotas expresadas en milímetros.</em>
</p>

### 3.5. Diseño electrónico del módulo sumergido

Para el módulo sumergido de LanternGuard se desarrolló un esquemático electrónico mediante EasyEDA, con el propósito de establecer las conexiones de los componentes encargados de la captura de imágenes, almacenamiento, comunicación y control de iluminación. A diferencia de la boya de superficie, este módulo no contará con una PCB personalizada, ya que sus componentes se integrarán mediante una placa universal perforada, conocida como *galleta electrónica*, sobre la cual se realizarán las conexiones correspondientes.

El esquemático se organiza en bloques funcionales de control y procesamiento, captura de imágenes, alimentación, almacenamiento, comunicación RS-485, control de iluminación y monitoreo, como se muestra en la Figura 26.

**Control y procesamiento.** La unidad principal corresponde al ESP32-S3-DevKitC-1-N16R8, encargado de coordinar la adquisición de imágenes, el registro de mediciones, el almacenamiento de información y la comunicación con la boya. Esta placa dispone de interfaces digitales que permiten integrar los diferentes componentes del módulo sumergido [\[15\]](#ref-15).

**Captura de imágenes y almacenamiento.** El diseño incorpora conectores para dos cámaras Arducam Mega de 5 MP, que comparten las señales de comunicación SPI y disponen de líneas de selección independientes. Esta configuración permite coordinar la captura de fotografías desde diferentes orientaciones hacia las mallas de la linterna. Asimismo, se contempla una tarjeta microSD conectada mediante SPI para almacenar inicialmente las fotografías y mediciones obtenidas durante las inspecciones [\[8\]](#ref-8).

**Comunicación RS-485.** Para transferir la información hacia la boya se utiliza un transceptor MAX3485, conectado al microcontrolador mediante señales de transmisión, recepción y control. El circuito también incorpora elementos de terminación y conexión al cable umbilical, estableciendo la interfaz de comunicación entre ambos módulos [\[16\]](#ref-16).

**Alimentación y control de iluminación.** El esquemático contempla conexiones de alimentación de 5 V y 3,3 V, destinadas a los diferentes componentes electrónicos. Además, incorpora dos circuitos de control mediante transistores MOSFET AO3400A, que permitirán activar las fuentes de iluminación asociadas a las cámaras para favorecer la captura de imágenes submarinas.

**Monitoreo y mediciones complementarias.** El diseño incluye un conector de expansión I²C que permitirá integrar el acelerómetro LIS3DH, destinado al registro de movimientos del módulo durante las inspecciones [\[9\]](#ref-9).

La integración electrónica se realizará sobre una placa universal perforada, donde se organizarán las conexiones entre los módulos comerciales. Esta solución permitirá reunir los componentes del sistema de adquisición dentro del compartimento electrónico del dispositivo sumergido, de acuerdo con la disposición estructural presentada en el modelo tridimensional.

<p align="center"><strong><em>Figura 26. Esquemático electrónico del módulo sumergido de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/cd6aca38-78cf-4cef-9093-3f1e1348016e" alt="Esquemático electrónico del módulo sumergido" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia en EasyEDA. Se muestran los bloques de control y procesamiento, captura de imágenes, alimentación, almacenamiento, comunicación RS-485, control de iluminación y monitoreo. La integración física se realizará mediante una placa universal perforada.</em></p>

### 3.6. Diseño electrónico de la boya de superficie

Para la boya de superficie de LanternGuard se desarrolló un esquemático electrónico y el diseño de una placa de circuito impreso (PCB) personalizada mediante EasyEDA. Este subsistema tiene como finalidad gestionar la programación temporal de las inspecciones, recibir la información procedente del módulo sumergido y coordinar su transmisión inalámbrica hacia la estación receptora terrestre.

**Esquemático electrónico de la boya**

El esquemático se organiza en cinco bloques funcionales: alimentación, control y procesamiento, comunicación, control de salida y tiempo, y sistema de montaje, como se muestra en la Figura 27.

El **bloque de alimentación** contempla una entrada de batería identificada como VBAT y la conexión de un convertidor DC-DC elevador de tensión (*Step Up*), destinado a proporcionar una alimentación regulada de 5 V a los componentes correspondientes. Este bloque permitirá integrar el suministro eléctrico de la boya con los circuitos encargados de su funcionamiento.

El **bloque de control y procesamiento** está constituido por la placa Heltec WiFi LoRa 32 V3, que incorpora un microcontrolador ESP32-S3 y un transceptor LoRa. Esta unidad será la encargada de coordinar las funciones electrónicas de la boya, gestionar la comunicación con el módulo sumergido y organizar el envío inalámbrico de mensajes breves de estado, metadatos e indicadores resumidos cuando estén disponibles, sin transmitir las fotografías completas mediante LoRa [\[18\]](#ref-18).

En el **bloque de comunicación** se incorpora el transceptor MAX3485, que permite establecer el enlace RS-485 entre la boya y el módulo sumergido mediante el cable umbilical. El circuito dispone de conexiones para las señales de transmisión, recepción y control, además de resistencias de terminación y polarización asociadas al enlace diferencial [\[16\]](#ref-16).

Por su parte, el **bloque de control de salida y tiempo** incluye un conector para el módulo RTC DS3231, cuya función será proporcionar la referencia temporal necesaria para programar las inspecciones periódicas cada 15 días [\[17\]](#ref-17). Asimismo, integra una etapa de conmutación formada por un MOSFET AO3401A y un transistor 2N3904, destinada al control electrónico de una salida de alimentación del sistema.

Finalmente, el esquema incorpora cuatro puntos de montaje que permitirán fijar la placa dentro del compartimento electrónico de la boya.

<p align="center"><strong><em>Figura 27. Esquemático electrónico de la boya de superficie de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b81e2db7-7854-48f7-b860-ad28dced2bc2" alt="Esquemático electrónico de la boya de superficie" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia en EasyEDA. Se muestran los bloques de alimentación, control y procesamiento, comunicación RS-485, control temporal y sistema de montaje.</em></p>

**Diseño de la placa PCB ruteada de la boya**

A partir del esquemático electrónico se elaboró el diseño de una PCB personalizada, en la cual se distribuyeron las huellas de los componentes, los conectores y las pistas de interconexión eléctrica, como se observa en la Figura 28.

En la zona central de la placa se ubica la huella destinada al módulo Heltec WiFi LoRa 32 V3, mientras que a su alrededor se distribuyen los componentes auxiliares y las conexiones correspondientes al transceptor MAX3485, el módulo RTC y los circuitos de alimentación y control. El diseño también incorpora cuatro perforaciones en las esquinas para facilitar la fijación de la PCB dentro de la estructura de la boya.

El ruteado de las pistas permite organizar las conexiones eléctricas de los diferentes componentes sobre una misma placa, reduciendo la necesidad de utilizar cableado individual para las interconexiones internas. Esta configuración facilita la integración del subsistema electrónico dentro del compartimento central representado en el modelo tridimensional.

La PCB se ha diseñado para su posterior fabricación y ensamblaje. Su integración permitirá reunir las principales funciones electrónicas de la boya en una estructura compacta, mientras que el panel solar, la batería y el circuito de gestión de carga se consideran dentro del sistema de alimentación previsto, cuya configuración definitiva deberá completarse.

<p align="center"><strong><em>Figura 28. Diseño de la placa PCB ruteada de la boya de superficie de LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/c3c2b51e-7a33-4ec2-b2a7-6d31ed5453c5" alt="PCB ruteada de la boya de superficie" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia en EasyEDA. Se presenta la distribución de las huellas electrónicas, las pistas ruteadas, los conectores y las perforaciones de montaje de la PCB personalizada.</em></p>

En conjunto, los modelos tridimensionales y los esquemáticos electrónicos permiten representar la configuración física y funcional de LanternGuard, integrando el módulo sumergido, la boya de superficie y los medios de comunicación propuestos. Estos diseños proporcionan una base técnica para el desarrollo del sistema de monitoreo de bioincrustación en las linternas de cultivo de *Argopecten purpuratus*.

### 3.7. Propuesta preliminar de interfaz del aplicativo LanternGuard

Como complemento de la arquitectura tecnológica de LanternGuard, se propone el desarrollo de un aplicativo destinado a visualizar y organizar la información obtenida durante las inspecciones de las linternas de cultivo. Su finalidad será presentar el porcentaje estimado de cobertura visible por bioincrustación y, cuando el algoritmo correspondiente haya sido desarrollado y validado, el volumen estimado de bioincrustación acumulada en las regiones fotografiadas. Esta información permitirá al acuicultor realizar el seguimiento del estado de las mallas y apoyar las decisiones relacionadas con su inspección y mantenimiento.

La interfaz propuesta contempla un panel de monitoreo que presenta la cantidad de linternas registradas, las fechas de captura y los indicadores de biofouling. Asimismo, incorpora la visualización de fotografías submarinas, gráficos de evolución temporal y una sección de comparación de imágenes correspondientes a diferentes inspecciones. Esta organización busca facilitar la interpretación de la información y el seguimiento de los cambios observados en las mallas.

La Figura 29 muestra el diseño preliminar de la interfaz del aplicativo LanternGuard, como representación conceptual de las funciones previstas. Los porcentajes, fechas y niveles de biofouling presentados en la imagen son ilustrativos y permiten visualizar cómo se mostraría la información generada por el sistema.

<p align="center"><strong><em>Figura 29. Propuesta preliminar de la interfaz del aplicativo LanternGuard.</em></strong></p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e1dcad7c-e80a-48d6-be4d-5a9829fb891c" alt="Interfaz preliminar del aplicativo LanternGuard" width="760" />
</p>

<p align="center"><em><strong>Nota.</strong> Elaboración propia. Representación conceptual del aplicativo para visualizar capturas submarinas, porcentajes estimados de cobertura visible por bioincrustación y evolución temporal del monitoreo. Los datos mostrados son referenciales.</em></p>

---

## Referencias bibliográficas

<a name="ref-1"></a>
**[1]** Consejo Nacional de Ciencia, Tecnología e Innovación Tecnológica (CONCYTEC), *Directiva N.º 001-2022-CONCYTEC-P: Uso de la metodología Nivel de Madurez Tecnológica (TRL)*, Resolución de Presidencia N.º 020-2022-CONCYTEC-P, Perú, 2022. [En línea]. Disponible en: <https://vinculate.concytec.gob.pe/wp-content/files/RP-020-2022-CONCYTEC-P.pdf>

<a name="ref-2"></a>
**[2]** R. E. Loayza-Aguilar, G. B. Saldaña-Rojas, F. Merino y G. E. Olivos-Ramirez, "Biofouling reduction by lantern nets exchange and its relationship with production and survival of Argopecten purpuratus in Samanco Bay, Peru," *Journal of the World Aquaculture Society*, vol. 56, n.º 5, art. e70054, 2025. doi: <https://doi.org/10.1111/jwas.70054>

<a name="ref-3"></a>
**[3]** Q.-P. Chen, C.-W. Bi, Z.-X. Zhang y Y.-P. Zhao, "Hydrodynamic effect of different biofouling types on aquaculture netting," *Ocean Engineering*, vol. 279, art. 114430, 2023. doi: <https://doi.org/10.1016/j.oceaneng.2023.114430>

<a name="ref-4"></a>
**[4]** W. Qiu, V. Pakrashi y B. Ghosh, "Fishing net health state estimation using underwater imaging," *Journal of Marine Science and Engineering*, vol. 8, n.º 9, art. 707, 2020. doi: <https://doi.org/10.3390/jmse8090707>

<a name="ref-5"></a>
**[5]** R. Cappaert, W. Yang, D. J. Ross, C. Johnston, C. MacLeod y C. A. White, "Development of an image binarization software tool for net occlusion estimations," *Aquacultural Engineering*, vol. 107, art. 102466, 2024. doi: <https://doi.org/10.1016/j.aquaeng.2024.102466>

<a name="ref-6"></a>
**[6]** A. Augustin, J. Yi, T. Clausen y W. M. Townsley, "A study of LoRa: Long range & low power networks for the Internet of Things," *Sensors*, vol. 16, n.º 9, art. 1466, 2016. doi: <https://doi.org/10.3390/s16091466>

<a name="ref-7"></a>
**[7]** A. H. Jebril, A. Sali, A. Ismail y M. F. A. Rasid, "Overcoming limitations of LoRa physical layer in image transmission," *Sensors*, vol. 18, n.º 10, art. 3257, 2018. doi: <https://doi.org/10.3390/s18103257>

<a name="ref-8"></a>
**[8]** Arducam, "MEGA-5MP: Cámara SPI de 5 megapíxeles," documentación técnica, s. f. [En línea]. Disponible en: <https://docs.arducam.com/Arduino-SPI-camera/MEGA-SPI/MEGA-5MP/>

<a name="ref-9"></a>
**[9]** STMicroelectronics, "LIS3DH: 3-axis MEMS accelerometer," documentación técnica, s. f. [En línea]. Disponible en: <https://www.st.com/en/mems-and-sensors/lis3dh.html>

<a name="ref-10"></a>
**[10]** Comunidad Andina, *Decisión 486: Régimen Común sobre Propiedad Industrial*, 2000. [En línea]. Disponible en: <https://www.comunidadandina.org/StaticFiles/DocOf/DEC486.pdf>

<a name="ref-11"></a>
**[11]** M. Stokes, H. Pham y T. R. Swanson, "Adjustable aquaculture camera mounting system," publicación de patente WO2024072597A1, 2024. [En línea]. Disponible en: <https://patents.google.com/patent/WO2024072597A1/en>

<a name="ref-12"></a>
**[12]** H. Pham y T. R. Swanson, "Underwater net monitoring device," publicación de patente US20240130336A1, 2024. [En línea]. Disponible en: <https://patents.google.com/patent/US20240130336A1/en>

<a name="ref-13"></a>
**[13]** M. D. Zúñiga Barraza *et al.*, "System for inspecting farming netting in aquaculture cages," publicación de patente NO20240761A1, familia WO2023108307A1, 2024. [En línea]. Disponible en: <https://patents.google.com/patent/NO20240761A1/en>

<a name="ref-14"></a>
**[14]** L. Fortunato y T. Leiknes, "In-situ non-invasive device for early detection of fouling in aquatic systems," publicación de patente US20200326279A1, 2020. [En línea]. Disponible en: <https://patents.google.com/patent/US20200326279A1/en>

<a name="ref-15"></a>
**[15]** Espressif Systems, "ESP32-S3-DevKitC-1: Placas de desarrollo ESP32-S3," documentación técnica del fabricante, s. f. [En línea]. Disponible en: <https://www.espressif.com/en/products/devkits/esp32-s3-series/esp32-s3-devkitc-1>

<a name="ref-16"></a>
**[16]** Analog Devices, "MAX3485: Transceptor RS-485/RS-422 de 3,3 V," ficha técnica, s. f. [En línea]. Disponible en: <https://www.analog.com/en/products/max3485.html>

<a name="ref-17"></a>
**[17]** Analog Devices, "DS3231: Reloj de tiempo real integrado con interfaz I²C," ficha técnica, s. f. [En línea]. Disponible en: <https://www.analog.com/en/products/ds3231.html>

<a name="ref-18"></a>
**[18]** Heltec Automation, "WiFi LoRa 32 (V3): ESP32-S3 y SX1262," documentación técnica, s. f. [En línea]. Disponible en: <https://heltec.org/project/wifi-lora-32-v3/>

