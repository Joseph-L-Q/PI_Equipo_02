# HANDOFF — Proyecto Integrador UPCH C7328, Equipo 02

Sistema de inspección de bioincrustación (*biofouling*) en linternas de cultivo suspendido de concha de abanico (*Argopecten purpuratus*). Metodología VDI 2206 (modelo V).

---

## 1. Fecha y rama

- **Fecha de la sesión:** 27 de agosto de 2026
- **Rama de trabajo:** `docs/lista-exigencias-rev3` (creada desde `main`)
- **Repositorio:** https://github.com/Joseph-L-Q/PI_Equipo_02.git
- **Commit de la sesión:** `5fb93ea` — `docs(entregable1): lista de exigencias rev. 3 - arquitectura de dos camaras sobre linterna`

---

## 2. Qué se hizo en esta sesión

Se actualizó la **lista de exigencias (Entregable 1)** para reflejar el cambio de arquitectura del sistema, con criterio de diff mínimo: se conservaron columnas, orden de filas, categorías, tipo E/D y responsables.

### Cambio de arquitectura (contexto para entender las ediciones)

- **Antes:** módulo cilíndrico de 220 mm × 130 mm con ventana hemisférica única, sujeto al cabo de suspensión (no a la linterna), que recorría verticalmente los 2 m de la linterna, con cámara + sensores ambientales (temperatura y turbidez), y PCB a medida fabricada fuera del país.
- **Ahora:** prisma rectangular que se apoya y se asegura sobre el aro superior de la linterna. ESP32 alojado en el centro, cableado interno hacia **dos cámaras gran angular** en los extremos, inclinadas hacia abajo. Cuerpo más largo que el diámetro exterior de la linterna para que las cámaras queden fuera de la proyección de la malla. **Sin sensores, sin partes móviles, sin PCB a medida.** Detección por comparación contra una **imagen de referencia de la malla limpia**, midiendo el **porcentaje de área libre de malla**.

### Archivos modificados

- **`Proyecto_Integrador/Entregables/Entregable1_Listadeexigencias.md`** — 14 filas editadas (columna Fecha puesta en `27/08/2026` solo en esas filas):
  - Función Principal, Geometría, Cinemática, Fuerzas, Energía, Señales, Control, Electrónica, Software (E), Fabricación, Montaje, Transporte, Uso, Costos.
  - **Filas NO tocadas** (siguen en `20/08/2026`): Software (D), Comunicaciones, Seguridad y Marco Legal, Ergonomía, Mantenimiento, Mantenimiento — Mejora Deseable, Plazos.
  - Se agregó la referencia **`[13]`** al final de la bibliografía, sin renumerar ni reordenar las existentes:
    ```
    * [13] Fondo Nacional de Desarrollo Pesquero (FONDEPES), *Manual de cultivo suspendido de concha de abanico*, Ministerio de la Producción, Lima, Perú, s.f.
    ```
    Se cita en **Geometría** (límite de 1 m de longitud del cuerpo) y en **Fuerzas** (hundimiento de la línea por fouling; corriente de 3 a 25 cm/s).
- **`README.md`** — 3 líneas, quitando la arquitectura anterior:
  - línea 61: se eliminó "y variables ambientales" del objetivo general.
  - línea 66: el objetivo específico 2 medía temperatura y turbidez; se reescribió como registro de imágenes para conformar la base de datos de referencia. Se mantuvo la numeración de la lista.
  - línea 90: "visión artificial y sensores ambientales" → "visión artificial".
- **`docs/handoff/HANDOFF.md`** — este archivo (nuevo).

### Verificación hecha

- La tabla renderiza en GitHub: se comprobó que las 23 filas tienen exactamente 6 pipes (5 columnas).
- Se extrajeron las 60 páginas del PDF `Manual-de-Concha-de-Abanico.pdf` con `pypdf` y se verificaron **contra el texto real** los datos citados: 1 m entre amarres de linternas (p. 13, 28, 32-33), corriente 3–25 cm/s (p. 21, Wildish y Saulnier 1993), hundimiento de la línea por peso del fouling y reflote (p. 71-73), aberturas de malla L1–L3 de 15/21/32 mm (p. 69, 72).

---

## 3. Decisiones técnicas y por qué

### Decisiones aplicadas

1. **El diámetro exterior de la linterna (0.5 m) se citó con `[1]`, no se marcó como tentativo.** El manual FONDEPES **no** trae diámetro ni altura de linterna. Se encontró que la referencia `[1]` ya presente en la lista (Loayza y Tresierra, bahía Samanco) describe linternas de **2 m de altura, 0.5 m de diámetro, 10 pisos y 2 cm de abertura**. Por eso no hizo falta agregar otra fuente ni renumerar.
2. **El manual FONDEPES entró como `s.f.` (sin fecha).** No figura año en portada, créditos ni presentación del PDF. Los metadatos del archivo dicen creación 2017-08-04 (CorelDRAW X7), pero eso no es dato editorial publicado, así que no se usó. **Falta confirmar el año.**
3. **No se agregó URL a la referencia `[13]`** porque no se verificó la URL oficial en fondepes.gob.pe.
4. **La flotabilidad NO se marcó como tentativa.** La fila Fuerzas ya fijaba numéricamente el peso aparente en **0.2 a 0.5 kgf**; marcar además "flotabilidad cercana a la neutra *(tentativo)*" habría duplicado y contradicho un valor ya fijado. Solo se agregó "el menor peso sumergido posible".
5. **Se eliminaron la resolución mínima de 1600 × 1200 px y la iluminación LED blanca difusa** de Electrónica (y el LED de Energía y Costos). Estaban atadas a la cámara única y al procesamiento a bordo, que ya no existen. La exigencia ahora pide **resolver las aberturas de malla a la distancia de trabajo**, no "buena calidad de imagen".
6. **La Raspberry Pi Zero 2 W se eliminó de Electrónica** (estaba descrita como CPU dentro del módulo sumergido). Se reemplazó por "procesamiento en una unidad externa al módulo", sin nombrar hardware.
7. **El "30 % a 10 %" del asesor NO se escribió en el documento.** Fue explícitamente ilustrativo; el umbral real queda por fijar.
8. **La salinidad 34,4 a 34,9 ‰ del manual no se usó.** En Materia bastaba exigir resistencia a salinidad sin escribir el rango, y así no hizo falta la cita.

### Decisiones descartadas (y por qué)

1. **NO se editó la fila `Comunicaciones`.** Hoy afirma transmisión inalámbrica por **ondas acústicas submarinas** (transceptores de ultrasonido), lo que implica hardware que la nueva arquitectura no contempla, y además contradice el "cable umbilical" que decía Control. Se dejó intacta porque las comunicaciones acústicas no estaban en la lista de disparadores de edición acordada (sensores, datos ambientales, recorrido vertical, cilindro 220×130, ventana única, sujeción al cabo, PCB/fabricación externa, Raspberry Pi). **Esta fila queda pendiente de decisión del equipo.**
2. **NO se agregaron filas ni categorías nuevas**, por regla explícita del encargo. Quedaron como propuestas (ver §7).
3. **NO se corrigieron erratas preexistentes**, por diff mínimo:
   - Fabricación: *"La carcasa externa **utilizará será** impresa en 3D (PETG) y **sellado** herméticamente"* (concordancia rota).
   - Electrónica: responsable escrito **"Y.P, J,L"** (coma en vez de punto).
   - Se propone corregirlas en un commit aparte de estilo.
4. **NO se tocó el Deseo Software (D)**, que sigue diciendo "porcentaje de cobertura" mientras la Función Principal ahora dice "área libre". No menciona sensores, y los Deseos estaban protegidos. **La terminología conviene alinearla.**
5. **NO se tocó el plan de trabajo.** El Gantt **no es Mermaid**: es una imagen PNG embebida (línea 40 del entregable, `https://github.com/user-attachments/assets/dfecfb81-...`). No se pudo renombrar ninguna tarea de "dataset"/"entrenamiento"/sensores/PCB. **Hay que regenerar la imagen.**
6. **NO se tocaron `.docx`, `.pptx` ni `.pdf`.**

---

## 4. Valores marcados como TENTATIVO

Buscados con `git grep -n -i "tentativ"`. Los 6 están todos en `Proyecto_Integrador/Entregables/Entregable1_Listadeexigencias.md`:

| # | Línea | Fila | Valor tentativo | Qué falta para confirmarlo |
|---|---|---|---|---|
| 1 | 15 | Geometría | Voladizo en cada extremo del prisma | Definir cuánto sobresale cada cámara más allá del diámetro de 0.5 m. Depende del ángulo de visión del módulo de cámara elegido y del ángulo rasante aceptable sobre los pisos inferiores. Restricción dura: la longitud total **no puede pasar de 1 m**, que es la separación entre amarres de linternas en la línea madre `[13]` |
| 2 | 16 | Cinemática | Ángulo de inclinación de las cámaras, fijado en el montaje | Verificar por trazado geométrico o simulación que con 2 m de altura y 10 niveles las cámaras cubren toda la malla sin que los pisos bajos queden demasiado oblicuos |
| 3 | 17 | Fuerzas | Medio de sujeción al aro superior | El equipo aún no define si el módulo solo se apoya o se asegura. La exigencia solo pide que no se desplace |
| 4 | 19 | Señales | Franja de cada celda reservada al crecimiento de las conchas (**1/4 a 1/2**) | Medir en muestras reales cuánto tapan las conchas desde adentro la parte inferior de cada abertura. Indicación del asesor: está entre un cuarto y la mitad |
| 5 | 19 | Señales | Umbral de obstrucción | Fijar el porcentaje de área libre por debajo del cual se declara obstrucción. El "de 30 % a 10 %" del asesor fue ilustrativo, **no** es el valor |
| 6 | 28 | Montaje | Medio de sujeción de ajuste manual | Mismo pendiente que el #3; deben resolverse juntos |

---

## 5. Estado de los scripts

**El repositorio no contiene ningún script propio del proyecto que corra.** Lo que hay:

| Ruta | Estado | Nota |
|---|---|---|
| `Proyecto/MóduloSoftware/Source code/main.ino` | **No aplica al proyecto** | Es un sketch de plantilla de **estación meteorológica** generado por Arduino IoT Cloud ("Spkfn_Weather_Station"), con variables de humedad, lluvia, viento, UV y rayos. No tiene relación con el sistema de inspección. No se ejecutó ni se modificó |
| `Proyecto/MóduloMecánico/WeatherStation_v2_Base_v2.stl` | **No aplica al proyecto** | Plantilla de estación meteorológica |
| `Proyecto/MóduloMecánico/WeatherStation_v2_windmill_v4.stl` | **No aplica al proyecto** | Plantilla de estación meteorológica |
| `Proyecto/MóduloElectrónico/Esquema electrónico del proyecto.pdf` | **No aplica al proyecto** | Esquema de **sensores de flexión** (Flex Sensor, FSensor1, FSensor2), de otra plantilla |
| `Proyecto/MóduloElectrónico/README.md`, `MóduloMecánico/README.md`, `MóduloSoftware/README.md` | Vacíos | Sin contenido |

**Script usado en la sesión pero NO versionado:** se escribió un extractor de PDF ad hoc con `pypdf` en el directorio temporal de la sesión para leer `Manual-de-Concha-de-Abanico.pdf`. **Ese directorio temporal se pierde.** Si hace falta releer el manual en la máquina nueva, es un script de ~10 líneas: `PdfReader(ruta)` y `page.extract_text()` sobre las 60 páginas. Ojo: el PDF es **2-up** (dos páginas impresas por hoja), por eso las 60 hojas cubren ~113 páginas impresas.

**Ningún script falló.** No hay errores pendientes de este tipo.

---

## 6. Qué sigue, en orden

1. **Subir la rama.** No se pudo hacer en esta sesión (ver §7). Primer comando concreto en la máquina nueva, después de clonar:
   ```
   git push -u origin docs/lista-exigencias-rev3
   ```
2. **Abrir el PR** contra `main`. El cuerpo completo ya está redactado (ver §7 sobre dónde está) o se puede reconstruir desde este HANDOFF.
3. **Resolver la fila `Comunicaciones`** (§3, descartada #1): decidir entre cable a superficie o almacenamiento local con descarga al izar, y corregir esa celda.
4. **Confirmar los 6 valores TENTATIVO** de §4, empezando por el par medio de sujeción (#3 y #6), que bloquea el diseño mecánico.
5. **Regenerar la imagen del plan de trabajo** con las tareas renombradas (fuera "dataset"/"entrenamiento"/sensores/PCB; dentro "imágenes de referencia" y "validación a escala"), sin mover fechas.
6. **Agregar las filas propuestas** (Materia, Control de calidad/Pruebas, Solución de referencia) si el equipo aprueba crecer la tabla.
7. **Limpiar los archivos de plantilla ajenos** listados en §5.

---

## 7. Bloqueos y preguntas abiertas

### Bloqueos

- **No se pudo hacer push.** En la máquina de esta sesión **git no estaba instalado** (se usó un MinGit portable en el directorio temporal) y **`gh` no está instalado**. El push falló con:
  ```
  fatal: could not read Username for 'https://github.com': terminal prompts disabled
  ```
  El commit `5fb93ea` **existe solo en local en la máquina vieja**. En la máquina nueva hay que rehacer el trabajo desde el push, o clonar y verificar si la rama ya llegó al remoto.
- **`PR_BODY_rev3.md` está FUERA del repo** y por lo tanto **no viaja con git**. Ruta en la máquina vieja:
  `C:\Users\vient\Documents\PROYECTO ITNEGRADOR UPCH\PR_BODY_rev3.md`
  Si todavía tienes acceso a esa máquina, **cópialo antes de migrar**. Si no, este HANDOFF contiene lo esencial para reconstruirlo.

### Preguntas abiertas para el equipo

- **(a)** ¿Cómo se conectan dos cámaras a un solo ESP32? Opciones: dos ESP32-CAM sincronizados, cámaras SPI en un ESP32-S3, o multiplexor. La celda de Electrónica quedó abierta (SPI o I²C, con multiplexado secuencial si no hay captura simultánea).
- **(b)** **Transmisión:** el Wi-Fi no propaga bajo el agua. Definir cable a superficie o almacenamiento local con descarga al izar. Bloquea también la fila `Comunicaciones`.
- **(c)** Voladizo y ángulo de inclinación frente al **ángulo rasante** sobre los niveles inferiores: con 2 m de altura y cámaras arriba, los pisos bajos se ven muy oblicuos.
- **(d)** Masa y flotabilidad del módulo. Ya hay valor fijo (0.2–0.5 kgf); si se quiere reabrir, hay que editarlo explícitamente.
- **(e)** **Conflicto de espacio:** se exigió "paso libre para el cabo de suspensión" por el centro del prisma, pero el ESP32 también va al centro. Hay que resolverlo en el diseño.
- **(f)** Rol de la Raspberry Pi: se sacó del módulo. ¿Se conserva como estación de procesamiento en superficie?
- **(g)** ¿Un módulo por linterna o un módulo itinerante de muestreo? El manual indica **~100 linternas por línea**, lo que hace inviable un módulo por linterna al costo actual.
- **(h)** **Año del manual FONDEPES** (quedó como `s.f.`).
- **(i)** Política de la columna Fecha: se puso `27/08/2026` solo en las 14 filas modificadas. La **Fecha del encabezado del documento sigue en `20/08/2026`** — ¿debe actualizarse?
- **(j)** Valor del umbral de obstrucción y del porcentaje de área libre de referencia.
- **(k)** Fracción de celda reservada a las conchas (rango actual 1/4 a 1/2).
- **(l)** Captura simultánea vs. multiplexada y uso de microSD.
- **(m)** Procesamiento en estación vs. nube, y cómo llega la imagen desde el módulo (ligado a **b**).
- **(n)** Medio de sujeción al aro superior.
- **(o)** Contacto sugerido por el asesor para imágenes reales o visita: **María Rivera Chira, Centro de Innovación Productiva (CITE)**. Falta buscar el correo institucional.
- **(p)** Según el asesor, el fouling por algas se concentra en **verano y primavera** (sin fuente). Considerarlo al programar pruebas de campo.

### Propuestas no aplicadas (no se agregaron por regla de no crecer la tabla)

1. **Fila "Materia"** con resistencia a radiación UV, salinidad y humedad. **La categoría Materia no existe** en el documento. La plantilla VDI la contempla.
2. **Fila "Control de calidad" o "Pruebas"** — **no existe**, y el asesor la exigió el 27/08/2026. Contenido propuesto: (i) validación a escala en tanque o balde con **dos muestras de malla, una limpia y una con fouling**; (ii) verificar que las cámaras resuelven aberturas de **15 a 32 mm** de linternas L1 a L3 `[13]` a la distancia de trabajo; (iii) verificar el algoritmo con imágenes de referencia anotadas.
3. **Línea "Solución de referencia (tentativa)"** — **no existe**; los componentes se nombran dentro de las celdas. Se propone crearla para separar exigencia de solución (VDI 2206, Checkpoint 2, pregunta 5) y alojar: ESP32 con cámaras por SPI o I²C, captura secuencial multiplexada, microSD, PETG, acrílico, Python/OpenCV, procesamiento en estación o nube.
4. **Deseos ausentes:** no existen deseos (D) de deep learning en etapa 2 ni de retiro/fin de vida. Se propone agregarlos; el de deep learning redactado como **reconocimiento de patrones (algas)** con base de datos propia formada con las imágenes de esta etapa.

---

## 8. Estado fuera de git

Rellenar a mano. **No se encontró ninguna de estas URLs en el repositorio** (`git grep -i -E "onshape|simscale"` no devolvió resultados), así que están vacías:

- **Documento de Onshape:**
- **Proyecto de SimScale:**
- **PR abierto:**

URL de compare para abrir el PR una vez subida la rama:
`https://github.com/Joseph-L-Q/PI_Equipo_02/compare/main...docs/lista-exigencias-rev3`

---

## 9. Dependencias instaladas en la máquina de esta sesión

Para reinstalar en la máquina nueva:

```
pip install pypdf
```

- **`pypdf` 6.16.2** (pip) — usado solo para extraer el texto de `Manual-de-Concha-de-Abanico.pdf` y verificar los datos citados. **No es dependencia del proyecto**, solo de la verificación documental.
- **No se instaló nada por npm.**
- **Git portable (MinGit 2.47.1):** se descargó a un directorio temporal porque **git no estaba instalado en la máquina vieja**. En la máquina nueva conviene instalar git normalmente:
  ```
  winget install --id Git.Git -e
  winget install --id GitHub.cli -e
  ```

---

## Clonado y checkout en la máquina nueva

```bash
git clone https://github.com/Joseph-L-Q/PI_Equipo_02.git
cd PI_Equipo_02
git fetch origin
git checkout docs/lista-exigencias-rev3
```

Si la rama **no existe en el remoto** (porque el push de esta sesión no llegó a completarse), créala desde `main` y rehaz el trabajo a partir de este documento:

```bash
git checkout main
git pull
git checkout -b docs/lista-exigencias-rev3
```
