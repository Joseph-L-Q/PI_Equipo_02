# Diseño y Simulación Estructural de Componentes del Grupo 2

A continuación, se presenta la documentación detallada del modelado 3D y el análisis de elementos finitos (FEA) de los componentes que conforman el sistema de monitoreo submarino, evaluando su comportamiento mecánico bajo las condiciones reales de operación en el entorno marino.

---

## Diseño de la Pieza 1 en Onshape

Se diseñó este componente, el cual corresponde a una de las mitades de la pieza central de la estructura. Cuenta con una perforación circular destinada al paso y conexión de los cables hacia la pieza 3 (una de las cajas de las cámaras). Asimismo, incluye una cavidad rebajada que representa la mitad del compartimento donde se estarán el microcontrolador ESP32 y las baterías. La pieza está diseñada para unirse mediante encaje directo con la pieza 2.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza1_Onshape_Bustos.png" alt="Modelo CAD 3D de la Pieza 1" width="100%"/>
  <br>
  <em>Figura 1. Vista general del modelado 3D de la carcasa principal en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** [Ver modelo en Onshape](https://cad.onshape.com/documents/823093ea5158517335111a07/w/534bbd9bcc4404bff8c5c0c9/e/e0badff72f909b6f093e9bcc)

---

## Simulación de Esfuerzos Mecánicos de la Pieza 1 en SimScale

Se analizó el comportamiento de la pieza asignando material PETG ($\rho = 1270 \text{ kg/m}^3$, $E = 2.1 \text{ GPa}$, $\nu = 0.38$). Mediante un análisis estático, se aplicó una sujeción fija en la cara posterior de unión y una presión hidrostática externa de $50\,000 \text{ Pa}$ ($0.5 \text{ bar}$) sobre las 5 caras exteriores. Los resultados de la simulación muestran que el esfuerzo máximo de Von Mises alcanza un valor pico de $2.129 \times 10^6 \text{ Pa}$ ($2.13 \text{ MPa}$), concentrándose principalmente en la zona interna de la cavidad. Este valor se encuentra muy por debajo del límite elástico del PETG ($50 \text{ MPa}$), lo que confirma que la estructura soporta adecuadamente las cargas del entorno marino sin riesgo de deformaciones plásticas ni fallas.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza1_Simscale_Bustos.png" alt="Simulación de Esfuerzos de la Pieza 1" width="100%"/>
  <br>
  <em>Figura 2. Mapa de resultados de la simulación estructural en SimScale para la carcasa.</em>
</p>

* **Enlace a la simulación en SimScale:** [Ver proyecto en SimScale](https://www.simscale.com/workbench/?pid=3635885982911573950&rru=f8fc2047-d041-48a8-847e-e0277bf55f11&ci=23f6dcd0-09fd-4092-b64b-868768afe6a9&mt=SIMULATION_RESULT&ct=SOLUTION_FIELD)

---
---

## Diseño de la Pieza 3 en Onshape

Se diseñó este componente, correspondiente a la carcasa de la cámara del sistema de monitoreo submarino. La pieza cuenta con una estructura tipo caja con una tapa superior para proteger los componentes internos frente a las condiciones del entorno marino. Asimismo, presenta una perforación lateral destinada al paso de conexiones y fue diseñada considerando su integración con los demás componentes del sistema.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza3_Onshape_Santamaria.png" alt="Modelo CAD 3D de la Pieza 3" width="100%"/>
  <br>
  <em>Figura 1. Vista general del modelado 3D de la carcasa de la cámara en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** [Ver modelo en Onshape](https://cad.onshape.com/documents/abaf97f135b791090d5654a3/w/1b2e7b3ab154f4d4ad8ff047/e/2992f9c7802c3002f6d76ee6)

---

## Simulación de Esfuerzos Mecánicos de la Pieza 3 en SimScale

Se analizó el comportamiento estructural de la pieza asignando material PETG ($\rho = 1270 \text{ kg/m}^3$, $E = 2.1 \text{ GPa}$, $\nu = 0.38$). Mediante un análisis estático, se aplicó una sujeción fija en las zonas de unión de la carcasa y una presión externa uniforme de $50\,000 \text{ Pa}$ ($0.5 \text{ bar}$) sobre las caras exteriores expuestas. 

Los resultados de la simulación permiten evaluar la resistencia mecánica de la carcasa mediante el esfuerzo equivalente de Von Mises, verificando que la pieza soporta adecuadamente las cargas aplicadas durante las condiciones de operación previstas.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza3_SimScale_Santamaria.png" alt="Simulación de Esfuerzos de la Pieza 3" width="100%"/>
  <br>
  <em>Figura 2. Mapa de resultados de la simulación estructural en SimScale para la carcasa de la cámara.</em>
</p>

* **Enlace a la simulación en SimScale:** [Ver simulación interactiva en SimScale](https://www.simscale.com/workbench/?pid=3625990943939288531)

---






## Diseño de la Pieza 5 en Onshape

Se diseñó la tapa superior de acceso a la pieza principal (pieza 1 y 2). Esta pieza cuenta con una geometría plana con bordes ajustados para un encaje sellado (*press-fit*) y una manija central ergonómica para facilitar la apertura y el mantenimiento en campo por parte del operario.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/pieza%205_OneShape_Antezana.png" alt="Modelo CAD 3D de la Tapa" width="100%"/>
  <br>
  <em>Figura 9. Vista del modelado 3D de la tapa en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** [Ver modelo interactivo en Onshape](https://cad.onshape.com/documents/92c43fa99b5db15195bb939b/w/b8fcf09428ae9fe8132781fd/e/07d8c02eb93c5e076a980b94?renderMode=0&uiState=6a90e4f97b02dbf7abc36dcd)

---

## Simulación de Esfuerzos Mecánicos de la Pieza 5 en SimScale

Se parametrizó este análisis con material PETG (Polietileno Tereftalato de Glicol), seleccionando propiedades mecánicas estándar ($\rho = 1270 \text{ kg/m}^3$, $E = 2.1 \text{ GPa}$, $\nu = 0.38$, $\sigma_y = 50 \text{ MPa}$). Se realizó un Análisis Estructural Estático (*Static Structural Analysis*) en SimScale para validar la resistencia de la tapa frente a la presión hidrostática del agua de mar y las corrientes marinas. Se configuró una sujeción fija (*Fixed Support*) en los 4 bordes laterales que encajan en la estructura de la pieza central y una carga de presión uniforme (*Pressure Load*) de $50\,000 \text{ Pa}$ ($50 \text{ kPa} / 0.5 \text{ bar}$) sobre la cara exterior. La simulación arrojó un esfuerzo máximo de Von Mises de $5.14 \times 10^5 \text{ Pa}$ ($0.514 \text{ MPa}$), el cual es significativamente menor al límite elástico del PETG ($50 \text{ MPa}$), confirmando que la pieza no sufrirá deformaciones plásticas ni fallas mecánicas.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza%205_SimScale_Antezana.png" alt="Simulación de Esfuerzos Von Mises" width="100%"/>
  <br>
  <em>Figura 10. Distribución de esfuerzos de Von Mises sobre la tapa en SimScale.</em>
</p>

* **Enlace a la Simulación en SimScale:** [Ver simulación interactiva en SimScale](https://www.simscale.com/workbench/?pid=8438599269814585137&mi=spec:702f1579-d37a-45de-abbe-df4b2b98800c%2Cservice:SIMULATION%2Cstrategy:1)
