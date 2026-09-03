# Diseño de la Pieza 5 en Onshape

Se diseñó la tapa superior de acceso a la pieza principal (pieza 1 y 2). Esta pieza cuenta con una geometría plana con bordes ajustados para un encaje sellado (*press-fit*) y una manija central ergonómica para facilitar la apertura y el mantenimiento en campo por parte del operario.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/pieza%205_OneShape_Antezana.png" alt="Modelo CAD 3D de la Tapa" width="100%"/>
  <br>
  <em>Figura 9. Vista del modelado 3D de la tapa en Onshape.</em>
</p>

* **Enlace al Modelo 3D en Onshape:** [Ver modelo interactivo en Onshape](https://cad.onshape.com/documents/92c43fa99b5db15195bb939b/w/b8fcf09428ae9fe8132781fd/e/07d8c02eb93c5e076a980b94?renderMode=0&uiState=6a90e4f97b02dbf7abc36dcd)

---

# Simulación de Esfuerzos Mecánicos de la Pieza 5 en SimScale

Se parametrizó este análisis con material PETG (Polietileno Tereftalato de Glicol), seleccionando propiedades mecánicas estándar ($\rho = 1270 \text{ kg/m}^3$, $E = 2.1 \text{ GPa}$, $\nu = 0.38$, $\sigma_y = 50 \text{ MPa}$). Se realizó un Análisis Estructural Estático (*Static Structural Analysis*) en SimScale para validar la resistencia de la tapa frente a la presión hidrostática del agua de mar y las corrientes marinas. Se configuró una sujeción fija (*Fixed Support*) en los 4 bordes laterales que encajan en la estructura de la pieza central y una carga de presión uniforme (*Pressure Load*) de $50\,000 \text{ Pa}$ ($50 \text{ kPa} / 0.5 \text{ bar}$) sobre la cara exterior. La simulación arrojó un esfuerzo máximo de Von Mises de $5.14 \times 10^5 \text{ Pa}$ ($0.514 \text{ MPa}$), el cual es significativamente menor al límite elástico del PETG ($50 \text{ MPa}$), confirmando que la pieza no sufrirá deformaciones plásticas ni fallas mecánicas.

<p align="center">
  <img src="https://github.com/Joseph-L-Q/PI_Equipo_02/blob/main/Recursos/Im%C3%A1genes/Pieza%205_SimScale_Antezana.png" alt="Simulación de Esfuerzos Von Mises" width="100%"/>
  <br>
