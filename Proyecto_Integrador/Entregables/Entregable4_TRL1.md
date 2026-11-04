
<h2 align="center">LANTERNGUARD</h2>

<h1 align="center">TRL 1 — Principios básicos reportados de la tecnología propuesta</h1>

<p align="center"><strong>Informe de sustento científico y tecnológico</strong></p>

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


## Presentación y alcance

LanternGuard es una propuesta de desarrollo tecnológico orientada al monitoreo periódico de la bioincrustación (*biofouling*) en las mallas de las linternas utilizadas para el cultivo de conchas de abanico (*Argopecten purpuratus*). Su finalidad es obtener fotografías submarinas para estimar el porcentaje de cobertura visible por organismos incrustantes en regiones seleccionadas de las mallas y proponer un algoritmo propio para estimar el volumen de bioincrustación acumulada en esas regiones. Para ello, se contemplan dos cámaras submarinas, un acelerómetro para registrar el movimiento del módulo, tecnologías de comunicación y un servicio posterior de procesamiento de imágenes. La estimación volumétrica es una función prevista cuya metodología y precisión aún deben desarrollarse y validarse. LanternGuard busca aportar información para planificar inspecciones y mantenimiento: no limpia las linternas ni pretende determinar la bioincrustación total de toda su estructura.

El presente informe, correspondiente al TRL 1 establecido por CONCYTEC [[1]](#ref-1), se centra en la revisión de los principios científicos que sustentan estas tecnologías. Como antecedente, Loayza-Aguilar et al. [[2]](#ref-2) investigaron el control de la bioincrustación en linternas de cultivo de conchas de abanico en la bahía de Samanco, Perú, evidenciando la importancia de su mantenimiento.

**Pregunta científica orientadora.** ¿Qué principios científicos sustentan la captura y el procesamiento de imágenes submarinas, el registro del movimiento mediante un acelerómetro y la comunicación de datos para estimar la cobertura visible de bioincrustación y formular una futura estimación de su volumen en regiones de mallas acuícolas?

## 1. Fundamentos científicos del fenómeno y principios de funcionamiento de las tecnologías

### 1.1. Bioincrustación marina

Las biopelículas marinas son comunidades microbianas adheridas a superficies que participan en los procesos de colonización y favorecen interacciones con otros organismos. Qian et al. [[3]](#ref-3) revisaron sus características y su relación con la bioincrustación. A medida que se acumulan organismos sobre las mallas, su geometría y el área abierta al paso del agua pueden modificarse. Chen et al. [[4]](#ref-4) examinaron ese efecto sobre redes acuícolas mediante modelos físicos con incrustación simulada y documentaron cambios en la resistencia hidrodinámica. Estos conocimientos permiten comprender los efectos de la bioincrustación sobre las estructuras que LanternGuard busca monitorear.

### 1.2. Cámaras Arducam Mega 5MP Autofocus B040101

Los sensores de imagen CMOS convierten la luz recibida por sus elementos fotosensibles en señales eléctricas que se leen y digitalizan para construir imágenes; este fundamento fue descrito por Fossum [[5]](#ref-5). Bajo el agua, la absorción y la dispersión de la luz alteran el color, el contraste y la visibilidad de los objetos, como explicaron Akkaynak y Treibitz [[6]](#ref-6).

LanternGuard contempla dos cámaras Arducam Mega 5MP Autofocus B040101, situadas en los extremos opuestos de un brazo de soporte y orientadas diagonalmente hacia la malla de la linterna. Según la documentación técnica de Arducam [[7]](#ref-7), este modelo cuenta con una resolución máxima de 2592 × 1944 píxeles, enfoque automático, un campo de visión diagonal nominal de 68,75° y comunicación mediante interfaz SPI (*Serial Peripheral Interface*). La calidad de las imágenes submarinas también dependerá de las condiciones de iluminación, la separación entre las cámaras y la malla, y las propiedades ópticas del agua [[6]](#ref-6). Al tratarse de cámaras destinadas a capturas submarinas, será necesario considerar una protección adecuada frente a la inmersión.

### 1.3. Procesamiento digital y segmentación de imágenes

La segmentación permite diferenciar regiones de una imagen a partir de las características de sus píxeles. Qiu et al. [[8]](#ref-8) analizaron imágenes submarinas de redes acuícolas mediante técnicas de preprocesamiento y segmentación con *k-means++*, diferenciando la estructura de la red, el crecimiento marino y sus aberturas para estimar porcentajes de obstrucción.

Por su parte, Cappaert et al. [[9]](#ref-9) desarrollaron una herramienta que utiliza aprendizaje profundo para clasificar los píxeles en agua y elementos distintos del agua, con el propósito de estimar la obstrucción de redes utilizadas en salmonicultura. Ambos estudios proporcionan fundamentos computacionales para analizar imágenes de mallas acuícolas. LanternGuard toma estos principios como referencia para identificar regiones cubiertas por organismos incrustantes y formular una estimación de su porcentaje de cobertura visible en las zonas fotografiadas.

La cobertura visible describe la proporción de área observada en una imagen, pero no equivale por sí sola al volumen tridimensional de los organismos adheridos. Para formular el algoritmo propio de estimación volumétrica se deberán definir referencias de escala, supuestos geométricos y un procedimiento que permita obtener o aproximar información sobre el relieve o espesor de la bioincrustación. Los antecedentes citados respaldan el análisis y la segmentación de imágenes, pero no demuestran que el volumen pueda estimarse con precisión mediante la configuración propuesta; esa función permanece pendiente de desarrollo y validación.

### 1.4. Sensor acelerómetro LIS3DH para detección de movimiento e inclinación

Los acelerómetros microelectromecánicos (MEMS) funcionan mediante estructuras sensibles a la aceleración. En los sensores capacitivos, el desplazamiento de una masa interna produce variaciones de capacitancia eléctrica que se transforman en señales de medición. Yazdi, Ayazi y Najafi [[10]](#ref-10) estudiaron los principios de funcionamiento de estos sensores inerciales.

Para LanternGuard se contempla utilizar el acelerómetro digital de tres ejes LIS3DH, de STMicroelectronics [[11]](#ref-11), para registrar las aceleraciones del módulo sumergido y estimar su inclinación en condiciones de movimiento reducido. Estas mediciones permitirían estudiar los movimientos del dispositivo asociados con las condiciones del entorno acuático y apoyar la identificación de periodos de menor movimiento para realizar las capturas fotográficas.

### 1.5. Control electrónico y comunicaciones

#### 1.5.1. Microcontrolador ESP32-S3-DevKitC-1-N16R8

Los microcontroladores funcionan mediante circuitos electrónicos digitales capaces de ejecutar instrucciones almacenadas en memoria y comunicarse con dispositivos periféricos. Para LanternGuard se contempla utilizar la placa ESP32-S3-DevKitC-1-N16R8, con 16 MB de memoria Flash y 8 MB de PSRAM, de acuerdo con la configuración de memoria indicada por Espressif [[12]](#ref-12). Su función prevista es controlar las cámaras, recibir los registros del acelerómetro y organizar la información obtenida por el módulo sumergido.

#### 1.5.2. Comunicación cableada mediante transceptores RS-485 MAX3485

RS-485 es un estándar de comunicación eléctrica basado en la señalización diferencial, mediante la cual los datos se representan por la diferencia de voltaje entre dos conductores. Este principio reduce la susceptibilidad a interferencias eléctricas y es ampliamente utilizado en sistemas industriales. El MAX3485, documentado por Analog Devices [[13]](#ref-13), es un transceptor semidúplex que convierte las señales lógicas del microcontrolador en señales eléctricas diferenciales para su transmisión y realiza el proceso inverso durante la recepción. En Lantern Guard se propone emplear estos transceptores para establecer un enlace de comunicación cableada entre el módulo submarino y la boya mediante un cable umbilical.

#### 1.5.3. Comunicación inalámbrica mediante Heltec WiFi LoRa 32 V3

Para la comunicación inalámbrica de LanternGuard se consideran dos placas Heltec WiFi LoRa 32 V3, que incorporan el transceptor SX1262 [[14]](#ref-14). La tecnología LoRa utiliza modulación de espectro ensanchado por chirps (*Chirp Spread Spectrum*), basada en variaciones de frecuencia de la señal de radio para representar información digital. Augustin et al. [[15]](#ref-15) estudiaron esta tecnología y documentaron sus características de largo alcance, bajo consumo energético y velocidad de transmisión limitada. En LanternGuard, una placa estaría ubicada en la boya para transmitir mensajes breves de estado, metadatos e indicadores resumidos cuando estén disponibles, y la otra en una estación receptora terrestre para recibirlos. Las fotografías completas no se enviarían por LoRa: tras su transferencia mediante RS-485 desde el módulo sumergido hacia la boya, se recuperarían mediante un procedimiento local posterior aún por definir, antes del procesamiento de imágenes.

### 1.6. Tecnologías auxiliares

LanternGuard contempla una tarjeta microSD, basada en memoria no volátil, para almacenar fotografías y registros. Asimismo, utilizará dos miniaros LED blancos de 5 V, cuyo funcionamiento se fundamenta en la electroluminiscencia de materiales semiconductores, para iluminar las mallas durante las capturas fotográficas [[16]](#ref-16). La alimentación de la boya considera un panel solar que convierte la radiación luminosa en energía eléctrica mediante el efecto fotovoltaico [[17]](#ref-17) y una batería recargable de ion-litio que almacena energía mediante procesos electroquímicos.

Adicionalmente, el reloj de tiempo real DS3231 utiliza un oscilador de cristal compensado en temperatura para mantener una referencia de fecha y hora [[18]](#ref-18), mientras que el circuito BQ24074 permite gestionar la carga de una batería de ion-litio de una celda y la alimentación eléctrica del sistema [[19]](#ref-19). Estos componentes cumplen funciones complementarias de almacenamiento, iluminación, temporización y suministro energético.

## 2. Estado del arte

Las investigaciones revisadas permiten identificar avances científicos relacionados con los efectos de la bioincrustación en estructuras acuícolas y las técnicas de procesamiento de imágenes utilizadas para evaluar la obstrucción de las mallas. La Tabla 1 presenta los principales aportes de estos estudios y su relación con los objetivos tecnológicos de LanternGuard.

**Tabla 1. Investigaciones relacionadas con la bioincrustación y el monitoreo de mallas acuícolas**

| Investigación | Aporte científico y tecnológico | Relación con LanternGuard |
| --- | --- | --- |
| Loayza-Aguilar et al. (2025) [[2]](#ref-2) | Evaluaron el efecto del mantenimiento mediante recambio de linternas sobre la bioincrustación en cultivos de conchas de abanico en la bahía de Samanco, Perú. | Sustenta la importancia de controlar la acumulación de organismos en las linternas. LanternGuard busca aportar información sobre su estado para ayudar al acuicultor a decidir cuándo realizar el mantenimiento. |
| Chen et al. (2023) [[4]](#ref-4) | Analizaron mediante modelos físicos con incrustación simulada cómo la bioincrustación modifica la resistencia hidrodinámica y el comportamiento de las redes acuícolas frente al flujo de agua. | Fundamenta la importancia de observar la acumulación de organismos y la obstrucción de las mallas, fenómenos que LanternGuard propone monitorear mediante imágenes. |
| Qiu et al. (2020) [[8]](#ref-8) | Desarrollaron un método de procesamiento de imágenes submarinas que diferencia la estructura de la red, el crecimiento marino y las aberturas para estimar porcentajes de obstrucción. | Proporciona un antecedente computacional para estudiar la identificación de zonas con bioincrustación y aberturas visibles mediante las fotografías capturadas por LanternGuard. |
| Cappaert et al. (2024) [[9]](#ref-9) | Desarrollaron una herramienta basada en aprendizaje profundo que clasifica regiones de agua y elementos distintos del agua para estimar la obstrucción de redes utilizadas en salmonicultura. | Aporta un procedimiento de segmentación que puede servir como referencia para identificar regiones cubiertas por organismos incrustantes en las fotografías y estimar su cobertura visible. |

*Nota.* Elaboración propia a partir de las investigaciones citadas.

En conjunto, los antecedentes revisados permiten relacionar el problema de la bioincrustación con los fundamentos tecnológicos de LanternGuard. Loayza-Aguilar et al. [[2]](#ref-2) y Chen et al. [[4]](#ref-4) aportan evidencia sobre la importancia y los efectos de la acumulación de organismos en estructuras acuícolas, mientras que Qiu et al. [[8]](#ref-8) y Cappaert et al. [[9]](#ref-9) presentan métodos computacionales para analizar la obstrucción mediante imágenes. Desde el punto de vista tecnológico, estas investigaciones permiten identificar procedimientos existentes de mantenimiento y análisis visual de mallas, que constituyen referencias para la propuesta de monitoreo de LanternGuard.

## 3. Bases de datos

Para la revisión científica de LanternGuard se consultaron registros bibliográficos y plataformas académicas relacionados con la bioincrustación marina, el procesamiento digital de imágenes, los sensores inerciales y las comunicaciones inalámbricas. Entre los recursos utilizados se encuentran PubMed, para verificar publicaciones sobre biopelículas marinas; ScienceDirect, para acceder a investigaciones sobre redes acuícolas y estimación de obstrucciones; y los portales de IEEE y MDPI, para consultar publicaciones sobre sensores, procesamiento de imágenes y comunicación LoRa.

La búsqueda se orientó mediante términos como *marine biofouling*, *underwater imaging*, *aquaculture net occlusion*, *MEMS accelerometer* y *LoRa communication*. Se priorizaron publicaciones cuyo contenido permitiera sustentar los principios científicos de las tecnologías consideradas para LanternGuard.

## 4. Libros

Gonzalez y Woods [[20]](#ref-20), en *Digital Image Processing*, presentan fundamentos de representación, mejoramiento y segmentación de imágenes digitales. Estos conocimientos proporcionan una base teórica para comprender los procedimientos computacionales relacionados con el análisis visual de las mallas acuícolas que contempla LanternGuard.

## 5. Tesis

Moreno Zuñiga [[21]](#ref-21) investigó la bioincrustación en redes de nylon impregnadas con nanopartículas de óxido de cobre, utilizadas para elaborar linternas de cultivo de conchas de abanico (*Argopecten purpuratus*), en la Universidad Nacional de Tumbes. Esta investigación constituye un antecedente académico sobre la acumulación de organismos incrustantes en estructuras de cultivo similares a las consideradas en LanternGuard, aunque se enfoca en un tratamiento del material y no en la detección mediante imágenes digitales.

## 6. Síntesis de evidencias del TRL 1

La revisión documental permitió identificar fundamentos científicos relacionados con la bioincrustación marina, la captura y procesamiento digital de imágenes submarinas, el registro de movimiento mediante acelerómetros y las tecnologías de comunicación. Estos conocimientos se sustentan en artículos científicos, estudios previos, documentación técnica, libros y tesis, conforme a las evidencias referenciales del TRL 1 establecidas por CONCYTEC.

En conjunto, las fuentes revisadas proporcionan una base científica y tecnológica para LanternGuard, propuesta orientada a estimar la cobertura visible de bioincrustación en regiones fotografiadas de las mallas de las linternas utilizadas para el cultivo de conchas de abanico. Sobre esa base, se contempla formular un algoritmo propio para estimar el volumen de bioincrustación en dichas regiones, aunque su fundamento geométrico específico y su precisión requieren desarrollo y validación posteriores. El propósito del sistema es apoyar la planificación de inspecciones y mantenimiento, sin ejecutar labores de limpieza ni extrapolar automáticamente los resultados a toda la linterna.

## Referencias bibliográficas

<a name="ref-1"></a>

**[1]** CONCYTEC, *Directiva N.º 001-2022-CONCYTEC-P: Uso de la metodología Nivel de Madurez Tecnológica (TRL)*, 2022. [https://vinculate.concytec.gob.pe/wp-content/files/RP-020-2022-CONCYTEC-P.pdf](https://vinculate.concytec.gob.pe/wp-content/files/RP-020-2022-CONCYTEC-P.pdf)

<a name="ref-2"></a>

**[2]** R. E. Loayza-Aguilar, G. B. Saldaña-Rojas, F. Merino y G. E. Olivos-Ramirez, «Biofouling reduction by lantern nets exchange and its relationship with production and survival of Argopecten purpuratus in Samanco Bay, Peru», *Journal of the World Aquaculture Society*, vol. 56, n.º 5, e70054, 2025. [https://doi.org/10.1111/jwas.70054](https://doi.org/10.1111/jwas.70054)

<a name="ref-3"></a>

**[3]** P.-Y. Qian, A. Cheng, R. Wang y R. Zhang, «Marine biofilms: diversity, interactions and biofouling», *Nature Reviews Microbiology*, vol. 20, pp. 671–684, 2022. [https://doi.org/10.1038/s41579-022-00744-7](https://doi.org/10.1038/s41579-022-00744-7)

<a name="ref-4"></a>

**[4]** Q.-P. Chen, C.-W. Bi, Z.-X. Zhang y Y.-P. Zhao, «Hydrodynamic effect of different biofouling types on aquaculture netting», *Ocean Engineering*, vol. 279, 114430, 2023. [https://doi.org/10.1016/j.oceaneng.2023.114430](https://doi.org/10.1016/j.oceaneng.2023.114430)

<a name="ref-5"></a>

**[5]** E. R. Fossum, «CMOS image sensors: electronic camera-on-a-chip», *IEEE Transactions on Electron Devices*, vol. 44, n.º 10, pp. 1689–1698, 1997. [https://doi.org/10.1109/16.628824](https://doi.org/10.1109/16.628824)

<a name="ref-6"></a>

**[6]** D. Akkaynak y T. Treibitz, «A revised underwater image formation model», en *Proceedings of CVPR*, pp. 6723–6732, 2018. [https://doi.org/10.1109/CVPR.2018.00703](https://doi.org/10.1109/CVPR.2018.00703)

<a name="ref-7"></a>

**[7]** Arducam, *Arducam New 5MP Mega SPI Autofocus Camera Module for Any MCU (B040101)*, ficha del fabricante, s. f. [https://www.arducam.com/arducam-new-5mp-mega-spi-autofocus-camera-module-for-any-mcu.html](https://www.arducam.com/arducam-new-5mp-mega-spi-autofocus-camera-module-for-any-mcu.html)

<a name="ref-8"></a>

**[8]** W. Qiu, V. Pakrashi y B. Ghosh, «Fishing net health state estimation using underwater imaging», *Journal of Marine Science and Engineering*, vol. 8, n.º 9, 707, 2020. [https://doi.org/10.3390/jmse8090707](https://doi.org/10.3390/jmse8090707)

<a name="ref-9"></a>

**[9]** R. Cappaert, W. Yang, D. J. Ross, C. Johnston, C. MacLeod y C. A. White, «Development of an image binarization software tool for net occlusion estimations», *Aquacultural Engineering*, vol. 107, 102466, 2024. [https://doi.org/10.1016/j.aquaeng.2024.102466](https://doi.org/10.1016/j.aquaeng.2024.102466)

<a name="ref-10"></a>

**[10]** N. Yazdi, F. Ayazi y K. Najafi, «Micromachined inertial sensors», *Proceedings of the IEEE*, vol. 86, n.º 8, pp. 1640–1659, 1998. [https://doi.org/10.1109/5.704269](https://doi.org/10.1109/5.704269)

<a name="ref-11"></a>

**[11]** STMicroelectronics, *LIS3DH: MEMS digital output motion sensor*, ficha técnica, s. f. [https://www.st.com/en/mems-and-sensors/lis3dh.html](https://www.st.com/en/mems-and-sensors/lis3dh.html)

<a name="ref-12"></a>

**[12]** Espressif Systems, *ESP32-S3-DevKitC-1 v1.1 User Guide*, documentación técnica, s. f. [https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.1.html)

<a name="ref-13"></a>

**[13]** Analog Devices, *MAX3485: 3.3V Powered RS-485/RS-422 Transceiver*, ficha técnica, s. f. [https://www.analog.com/en/products/max3485.html](https://www.analog.com/en/products/max3485.html)

<a name="ref-14"></a>

**[14]** Heltec Automation, *WiFi LoRa 32 (V3), ESP32-S3 + SX1262*, documentación técnica, s. f. [https://heltec.org/project/wifi-lora-32-v3/](https://heltec.org/project/wifi-lora-32-v3/)

<a name="ref-15"></a>

**[15]** A. Augustin, J. Yi, T. Clausen y W. M. Townsley, «A study of LoRa: long range & low power networks for the Internet of Things», *Sensors*, vol. 16, n.º 9, 1466, 2016. [https://doi.org/10.3390/s16091466](https://doi.org/10.3390/s16091466)

<a name="ref-16"></a>

**[16]** U.S. Department of Energy, *LED Basics*, s. f. [https://www.energy.gov/cmei/ssl/led-basics](https://www.energy.gov/cmei/ssl/led-basics)

<a name="ref-17"></a>

**[17]** U.S. Department of Energy, *Solar Photovoltaic Cell Basics*, s. f. [https://www.energy.gov/cmei/systems/solar-photovoltaic-cell-basics](https://www.energy.gov/cmei/systems/solar-photovoltaic-cell-basics)

<a name="ref-18"></a>

**[18]** Analog Devices, *DS3231: Extremely Accurate I²C-Integrated RTC/TCXO/Crystal*, ficha técnica, s. f. [https://www.analog.com/en/products/ds3231.html](https://www.analog.com/en/products/ds3231.html)

<a name="ref-19"></a>

**[19]** Texas Instruments, *BQ24074: Standalone 1-Cell Linear Battery Charger with PowerPath*, ficha técnica, s. f. [https://www.ti.com/product/BQ24074](https://www.ti.com/product/BQ24074)

<a name="ref-20"></a>

**[20]** R. C. Gonzalez y R. E. Woods, *Digital Image Processing*, 4.ª ed., Pearson, 2018. [https://www.imageprocessingplace.com/DIP-4E/dip4e_main_page.htm](https://www.imageprocessingplace.com/DIP-4E/dip4e_main_page.htm)

<a name="ref-21"></a>

**[21]** V. S. Moreno Zuñiga, «Evaluación de la incrustación de biofouling en redes de nylon impregnados con nanopartículas de óxido de cobre en el cultivo de Argopecten purpuratus», tesis de maestría, Universidad Nacional de Tumbes, 2025. [https://repositorio.untumbes.edu.pe/items/22877110-0b7b-4710-b275-76ff452ec91d](https://repositorio.untumbes.edu.pe/items/22877110-0b7b-4710-b275-76ff452ec91d)
