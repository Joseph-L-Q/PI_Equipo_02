# LanternGuard — Evidencias de integración electrónica y software

**Proyecto:** LanternGuard · **Curso:** Proyecto Integrador 2026-II · **Etapa:** Pruebas de banco para validación de subsistemas (TRL 3) y preparación de integración de laboratorio (TRL 4).

> **Alcance:** Esta bitácora diferencia resultados observados de objetivos pendientes. Las fotografías de montaje e iluminación fueron proporcionadas por el equipo en la conversación de trabajo. Los archivos originales de esas fotografías y las capturas de pantalla aún deben incorporarse a la carpeta `evidencias/` de esta rama para que queden versionados y visibles en GitHub.

## 1. Objetivo

Integrar y verificar progresivamente los subsistemas de adquisición de imágenes, iluminación, medición de inclinación y comunicación inalámbrica para inspeccionar mallas de linternas de cultivo de concha de abanico.

## 2. Arquitectura ensayada

- **Controlador de banco:** ESP32-S3.
- **Captura:** dos cámaras Arducam Mega 5 MP, interfaz SPI; SCK GPIO12, MISO GPIO13, MOSI GPIO11, CS individuales GPIO10 y GPIO21.
- **Iluminación:** dos anillos de ocho LED direccionables, datos en GPIO4 y GPIO5.
- **Inclinación:** MPU6050 mediante I²C, SDA GPIO8 y SCL GPIO7, dirección 0x68.
- **Comunicación inalámbrica ensayada por separado:** enlace LoRa 915 MHz entre placas Heltec, con reconstrucción de imágenes en Python en el receptor.

Las conexiones anteriores describen el **montaje de prueba**; no constituyen todavía un diseño final de PCB ni una validación de estanqueidad.

## 3. Evidencias de montaje e iluminación

| Evidencia | Descripción | Resultado observable |
|---|---|---|
| Fotografía 01 | Vista superior del cableado, protoboard, placa controladora y dos anillos LED | Componentes distribuidos en banco |
| Fotografía 02 | Vista alternativa del conjunto de conexiones | Integración física provisional |
| Fotografía 03 | Dos anillos LED encendidos en el montaje | Encendido simultáneo observado |
| Fotografía 04 | Vista lateral del banco con los anillos LED iluminados | Encendido y disposición física observados |
| Fotografía 05 | Vista general del cableado y los anillos sin iluminación | Registro complementario del montaje |

**Pendiente editorial:** insertar aquí las imágenes originales proporcionadas por el equipo, una vez subidas al repositorio, con sus rutas relativas y pies de figura. No sustituirlas por fotografías de referencia de internet.

## 4. Pruebas de subsistemas

### 4.1. Iluminación LED

Se logró encender ambos anillos LED durante las pruebas de banco. **Validado:** funcionamiento visual de la iluminación. **Pendiente:** medición de corriente, evaluación térmica, uniformidad lumínica, sincronización con la captura y pruebas bajo agua.

### 4.2. MPU6050

El sensor fue detectado mediante I²C y se obtuvieron lecturas de aceleración en pruebas previas. Su función prevista es estimar la inclinación/estabilidad del módulo. **Pendiente:** calibración, umbrales de movimiento y validación de la decisión automática de captura.

### 4.3. Cámaras Arducam Mega

Durante diagnósticos individuales, las cámaras llegaron a inicializarse en el bus SPI utilizando el cableado de la primera cámara (CS GPIO10). En una prueba posterior de captura JPEG, el programa se reiniciaba o detenía durante `camara.begin()`, antes de confirmar una nueva captura. **No se considera validada la captura simultánea de ambas cámaras** ni su integración estable con todos los sensores.

### 4.4. LoRa y reconstrucción en Python

En pruebas anteriores del enlace LoRa se consiguió transmitir datos de imágenes y reconstruir automáticamente archivos JPEG mediante un programa Python conectado al receptor. Esta evidencia corresponde a un ensayo del subsistema de comunicaciones; **no demuestra aún la transmisión extremo a extremo desde las dos cámaras del montaje actual**. Se registró además que software antivirus o la ocupación del puerto serie pueden interferir con la ejecución del receptor.

## 5. Estado de validación

| Subsistema | Evidencia disponible | Estado |
|---|---|---|
| Montaje electrónico | Fotografías del prototipo | Documentado visualmente |
| Dos anillos LED | Fotografías de encendido | Encendido verificado en banco |
| MPU6050 | Lecturas de prueba previas | Comunicación I²C verificada |
| Cámara individual | Mensajes de inicialización previos | Inicialización observada, estabilidad pendiente |
| Dos cámaras simultáneas | Diagnóstico parcial | Pendiente |
| Captura JPEG integrada | Reinicios en `begin()` | Pendiente de resolver |
| LoRa + reconstrucción Python | Ensayos previos de transmisión | Validado como subsistema separado |
| Análisis de biofouling / detección de roturas | Objetivo de desarrollo | Pendiente |
| Prueba submarina y estanqueidad | Sin evidencia en esta bitácora | Pendiente |

## 6. Próximos ensayos

1. Aislar la causa de reinicios en la inicialización SPI de cámara; revisar alimentación, cableado, biblioteca y registro de reinicio.
2. Capturar y guardar un JPEG con una cámara de forma reproducible.
3. Incorporar la segunda cámara con CS independiente y confirmar selección correcta del dispositivo.
4. Sincronizar iluminación y captura; registrar exposición y consumo eléctrico.
5. Integrar acelerómetro y criterio de estabilidad.
6. Probar la cadena completa: captura → transmisión → reconstrucción → almacenamiento → análisis de biofouling.
7. Ejecutar pruebas mecánicas y de sellado antes de cualquier inmersión.

## 7. Criterio TRL

Estas evidencias respaldan **pruebas de concepto y de subsistemas en banco**. No se afirma que el prototipo completo haya alcanzado TRL 4 ni que exista validación submarina hasta contar con pruebas integradas reproducibles y sus registros.

**Nota de trazabilidad:** adjuntar fotografías originales, capturas del monitor serie, scripts, versiones de bibliotecas, fechas y responsables de cada ensayo en futuras actualizaciones.
