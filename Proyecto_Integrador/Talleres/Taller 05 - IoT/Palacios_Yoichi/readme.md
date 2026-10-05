# Taller 5 (IoT): Actividades 01 a 05 con ESP32, Arduino Cloud, ThingSpeak y Ubidots

---

**Curso:** Proyectos de Ingeniería, Taller de Internet de las Cosas (IoT)

**Equipo:** Equipo 02

**Integrante:** Palacios, Yoichi

**Hardware:** ESP32 Dev Kit 1, kit de sensores Keyestudio, potenciómetro, LED, multímetro, protoboard y cables

**Software:** Arduino IDE, núcleo `esp32`, lenguaje C++ (Arduino)

**Plataformas IoT:** Arduino Cloud, ThingSpeak y Ubidots

> **Nota de seguridad:** por ser un repositorio público, las credenciales aparecen como `TU_RED_WIFI`, `TU_PASSWORD_WIFI` y `TU_API_KEY`. Los valores reales no se publican.

> **Nota sobre las capturas:** los textos marcados con *(confirmar con captura)* dependen de la prueba en el hardware y se completan al subir la imagen correspondiente. Los códigos de `Codigo/` están escritos siguiendo la documentación de cada plataforma, pero no se pudieron compilar en el equipo donde se redactó este documento (sin Arduino IDE), así que la verificación real es la prueba en la placa.

---

## 1. Introducción

Este taller recorre la cadena completa de una solución IoT con un ESP32: leer una señal analógica, conectarse a una red, enviar el dato a una plataforma en la nube y controlar un actuador de vuelta desde la nube [1]. El patrón es el mismo en las cinco actividades: **sensor, microcontrolador, red, plataforma, decisión**.

Mi trabajo es la parte del equipo en que, además de ThingSpeak (que usaron mis compañeros y que practicamos juntos), implementé las tres plataformas que pedía la consigna para las actividades 03 y 04, y el control del LED por MQTT en Ubidots para la actividad 05.

## 2. Objetivos

- **Act. 01:** promediar lecturas del ADC y convertirlas a voltaje.
- **Act. 02:** conectar el ESP32 a un hotspot del celular y mostrar la IP en el monitor serial.
- **Act. 03:** mostrar la variación de un potenciómetro en tiempo real en Arduino Cloud, ThingSpeak y Ubidots.
- **Act. 04:** lo mismo con un sensor del kit Keyestudio (elegí el LM35, temperatura) en las tres plataformas.
- **Act. 05:** controlar un LED desde una plataforma web.

## 3. Materiales

| Elemento | Cantidad | Uso |
|---|---|---|
| ESP32 Dev Kit 1 | 1 | Microcontrolador con Wi-Fi |
| Potenciómetro | 1 | Señal analógica variable (Act. 01 y 03) |
| Sensor LM35 (kit Keyestudio) | 1 | Temperatura, 10 mV por °C (Act. 04) |
| LED y resistencia de 220 Ω | 1 | Actuador (Act. 05) |
| Multímetro | 1 | Validar el voltaje medido |
| Protoboard y cables | 1 | Conexiones |
| Celular con hotspot 2.4 GHz | 1 | Red Wi-Fi (Act. 02 en adelante) |

## 4. Organización del código

Cada sketch está en su propia carpeta con el mismo nombre del `.ino`, que es lo que exige el Arduino IDE:

| Carpeta en `Codigo/` | Actividad | Plataforma | Biblioteca |
|---|---|---|---|
| `Act01_ADC_Promedio/` | 01 | Ninguna (monitor serial) | Ninguna |
| `Act02_WiFi_Hotspot/` | 02 | Ninguna (monitor serial) | `WiFi.h` |
| `Act03_ArduinoCloud/` | 03 | Arduino Cloud | `ArduinoIoTCloud` |
| `Act03_ThingSpeak/` | 03 | ThingSpeak | `WiFi.h`, `HTTPClient.h` |
| `Act03_Ubidots/` | 03 | Ubidots | `PubSubClient` |
| `Act04_ArduinoCloud/` | 04 | Arduino Cloud | `ArduinoIoTCloud` |
| `Act04_ThingSpeak/` | 04 | ThingSpeak | `WiFi.h`, `HTTPClient.h` |
| `Act04_Ubidots/` | 04 | Ubidots | `PubSubClient` |
| `Act05_LED_Ubidots/` | 05 | Ubidots | `PubSubClient` |

Las tres plataformas se diferencian en cómo llega el dato:

| Plataforma | Cómo se envía | Autenticación | Detalle importante |
|---|---|---|---|
| ThingSpeak [2] | HTTP GET a `api.thingspeak.com/update` | Write API Key en la URL | La cuenta gratuita acepta un dato cada 15 s como mínimo |
| Ubidots [3] | MQTT, publicación en `/v1.6/devices/<dispositivo>` | El token es el usuario MQTT, contraseña vacía | El dato se manda como JSON `{"variable": valor}` |
| Arduino Cloud [4] | Biblioteca `ArduinoIoTCloud`, la variable se sincroniza sola | ID y clave secreta del dispositivo | El IDE genera `thingProperties.h` |

---

## 5. Actividad 01: lectura de un potenciómetro con promediado y voltaje

### 5.1 Enunciado

> Mejorar el código anterior haciendo uso de un promediado de los datos y convirtiendo los valores del ADC a valores de voltaje.

### 5.2 Conexiones

| Pin del potenciómetro | Pin del ESP32 |
|---|---|
| GND | GND |
| VCC | 3V3 |
| SIG | GPIO34 |

El potenciómetro va a 3.3 V y no a 5 V porque los pines del ESP32 toleran como máximo 3.3 V. GPIO34 pertenece al ADC1, que sigue disponible cuando el Wi-Fi está encendido, y solo sirve como entrada.

![Figura 1](../../../../Recursos/Imágenes/Taller5_Palacios_Act01_conexion.png)

**Figura 1.** Conexión del potenciómetro al ESP32 (GND, 3V3 y señal al GPIO34).

### 5.3 Código

Archivo: `Codigo/Act01_ADC_Promedio/Act01_ADC_Promedio.ino`

```cpp
const int potPin = 34;
const int NUM_MUESTRAS = 32;
const float VREF = 3.3;
const int ADC_MAX = 4095;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(potPin, ADC_11db);
}

void loop() {
  long suma = 0;
  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma += analogRead(potPin);
    delay(2);
  }
  float promedio = suma / (float)NUM_MUESTRAS;
  float voltaje = promedio * VREF / ADC_MAX;
  Serial.print("ADC promedio: "); Serial.print(promedio, 1);
  Serial.print("  |  Voltaje: "); Serial.print(voltaje, 2);
  Serial.println(" V");
  delay(500);
}
```

| Bloque | Qué hace | Por qué |
|---|---|---|
| `analogReadResolution(12)` | ADC de 12 bits | El rango pasa a 0 a 4095 |
| `analogSetPinAttenuation(..., ADC_11db)` | Amplía el rango de entrada hasta cerca de 3.3 V | Con la atenuación por defecto se satura antes |
| Bucle `for` con 32 lecturas | Suma 32 muestras separadas 2 ms | Es el promediado pedido |
| `suma / (float)NUM_MUESTRAS` | Media de las lecturas | El `(float)` evita la división entera |
| `promedio * VREF / ADC_MAX` | Convierte cuentas a voltios | Es la conversión pedida |

**Por qué promediar.** Si el ruido de cada lectura es aleatorio e independiente, promediar N muestras reduce su desviación estándar en un factor √N. Con N = 32 son unas 5.7 veces menos. El costo es que cada medida tarda unos 32 × 2 ms = 64 ms, que no importa para un potenciómetro.

### 5.4 Resultado

![Figura 2](../../../../Recursos/Imágenes/Taller5_Palacios_Act01_serial.png)

**Figura 2.** Monitor serial con el ADC promedio y el voltaje.

![Figura 3](../../../../Recursos/Imágenes/Taller5_Palacios_Act01_multimetro.png)

**Figura 3.** Voltaje medido con el multímetro en el mismo punto, para validar la conversión.

Resultado esperado: el voltaje en el monitor serial debe coincidir con el del multímetro con una diferencia de pocas décimas de voltio, porque el ADC del ESP32 no es lineal en los extremos del rango [5]. *(confirmar con captura: valores de ADC y voltaje en el mínimo y el máximo, y lectura del multímetro)*

---

## 6. Actividad 02: conexión Wi-Fi con el hotspot del celular

### 6.1 Enunciado

> Crear una red WIFI usando su Smartphone como Hotspot, y conectarse a ella con el ESP32. En el monitor serial se deberá visualizar la dirección IP asignada.

### 6.2 Código

Archivo: `Codigo/Act02_WiFi_Hotspot/Act02_WiFi_Hotspot.ino`

```cpp
#include <WiFi.h>

const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 40) { delay(500); Serial.print("."); intentos++; }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.print("Direccion IP asignada: "); Serial.println(WiFi.localIP());
    Serial.print("RSSI: "); Serial.print(WiFi.RSSI()); Serial.println(" dBm");
  }
}
```

(La versión completa del archivo agrega reconexión automática en `loop()`.)

| Elemento | Qué hace |
|---|---|
| `WiFi.mode(WIFI_STA)` | El ESP32 actúa como cliente (estación) y no como punto de acceso |
| `WiFi.begin(ssid, clave)` | Inicia la conexión con el hotspot |
| `WiFi.status() == WL_CONNECTED` | Espera hasta que el DHCP del celular entrega una IP |
| `WiFi.localIP()` | Devuelve la IP asignada |
| `WiFi.RSSI()` | Intensidad de la señal en dBm (más cercano a 0 es mejor) |

El ESP32 solo trabaja en la banda de 2.4 GHz, así que el hotspot del celular debe emitir en esa banda. Si el celular solo ofrece 5 GHz, el ESP32 no encuentra la red.

### 6.3 Resultado

![Figura 4](../../../../Recursos/Imágenes/Taller5_Palacios_Act02_ip_serial.png)

**Figura 4.** Monitor serial con la conexión al hotspot y la IP asignada.

La IP la entrega el servidor DHCP del celular, normalmente dentro de un rango privado (`10.x.x.x`, `172.16.x.x` o `192.168.x.x`). *(confirmar con captura: IP asignada y RSSI)*

---

## 7. Actividad 03: el potenciómetro en tiempo real en tres plataformas

### 7.1 Enunciado

> Escribir un código que muestre en tiempo real la variación del potenciómetro conectado al ESP32 en las siguientes plataformas de IoT: Arduino Cloud, ThingSpeak y Ubidots.

La conexión del potenciómetro es la de la Act. 01. La función de lectura (promedio de 32 muestras y conversión a voltaje) se reutiliza en los tres sketches.

### 7.2 Arduino Cloud

Archivos: `Codigo/Act03_ArduinoCloud/Act03_ArduinoCloud.ino` y `thingProperties.h`.

1. En Arduino Cloud se crea una *Thing* con una variable `voltaje` de tipo `float` y permiso de solo lectura, con actualización cada segundo.
2. Se asocia el ESP32 como dispositivo (Arduino Cloud entrega un ID y una clave secreta) y se ingresan el Wi-Fi.
3. En un *Dashboard* se agrega un widget (medidor o gráfico) enlazado a `voltaje`.

El sketch solo hace dos cosas: llamar a `ArduinoCloud.update()` y asignar `voltaje = leerVoltaje()`. Cuando el valor cambia, la biblioteca lo envía sola, sin escribir código de red.

![Figura 5](../../../../Recursos/Imágenes/Taller5_Palacios_Act03_ArduinoCloud.png)

**Figura 5.** Dashboard de Arduino Cloud con el voltaje del potenciómetro.

### 7.3 ThingSpeak

Archivo: `Codigo/Act03_ThingSpeak/Act03_ThingSpeak.ino`.

1. Se crea un canal con el *Field 1* = Voltaje y se copia la *Write API Key*.
2. El sketch envía un `GET` a `http://api.thingspeak.com/update?api_key=...&field1=<voltaje>` cada 20 s.
3. ThingSpeak responde con el número de entrada del dato. Si responde `0`, el dato fue rechazado (por ejemplo, por enviar antes de los 15 s).

Como el límite de la cuenta gratuita es de un dato cada 15 s, el gráfico de ThingSpeak es una versión muestreada de lo que se ve en el monitor serial (que se refresca cada segundo).

![Figura 6](../../../../Recursos/Imágenes/Taller5_Palacios_Act03_ThingSpeak.png)

**Figura 6.** Gráfico del Field 1 en ThingSpeak.

### 7.4 Ubidots

Archivo: `Codigo/Act03_Ubidots/Act03_Ubidots.ino`.

1. Se copia el *token* de la cuenta de Ubidots, que sirve como usuario MQTT (contraseña vacía).
2. El ESP32 se conecta a `industrial.api.ubidots.com:1883` y publica en el tópico `/v1.6/devices/esp32-equipo02` el JSON `{"voltaje": 1.65}` cada 2 s.
3. Ubidots crea el dispositivo y la variable `voltaje` automáticamente al recibir el primer mensaje. En el *Dashboard* se agrega un widget enlazado a esa variable.

![Figura 7](../../../../Recursos/Imágenes/Taller5_Palacios_Act03_Ubidots.png)

**Figura 7.** Dashboard de Ubidots con el voltaje del potenciómetro.

### 7.5 Resultado

![Figura 8](../../../../Recursos/Imágenes/Taller5_Palacios_Act03_serial.png)

**Figura 8.** Monitor serial durante el envío (respuesta de ThingSpeak y mensajes publicados a Ubidots).

| Plataforma | Protocolo | Periodo de envío | Resultado |
|---|---|---|---|
| Arduino Cloud | Propio de la biblioteca | 1 s, al cambiar | *(confirmar con captura)* |
| ThingSpeak | HTTP | 20 s (mínimo 15 s) | *(confirmar con captura)* |
| Ubidots | MQTT | 2 s | *(confirmar con captura)* |

---

## 8. Actividad 04: el sensor LM35 en tiempo real en tres plataformas

### 8.1 Sensor y conexiones

El LM35 entrega **10 mV por grado Celsius** [6], de modo que la temperatura es `T (°C) = V × 100`. Por ejemplo, 0.25 V corresponden a 25 °C.

| Pin del LM35 | Pin del ESP32 |
|---|---|
| GND | GND |
| VCC | VIN (5 V) |
| OUT | GPIO34 |

Con esa alimentación, la salida a temperatura ambiente es de solo unos 0.2 a 0.3 V, muy por debajo de los 3.3 V que tolera el pin. Un detalle conocido del ESP32 es que su ADC es poco lineal en la parte baja del rango, por lo que el valor puede diferir en 1 a 2 °C de un termómetro de referencia [5]. Por eso el código promedia 64 muestras.

![Figura 9](../../../../Recursos/Imágenes/Taller5_Palacios_Act04_conexion.png)

**Figura 9.** Conexión del LM35 al ESP32.

### 8.2 Código

Los tres sketches (`Codigo/Act04_ArduinoCloud/`, `Act04_ThingSpeak/` y `Act04_Ubidots/`) tienen la misma estructura que los de la Act. 03. Cambia solo la función de lectura:

```cpp
float leerTemperaturaC() {
  long suma = 0;
  for (int i = 0; i < 64; i++) { suma += analogRead(34); delay(2); }
  float voltaje = (suma / 64.0) * 3.3 / 4095;   // V
  return voltaje * 100.0;                        // 10 mV/C
}
```

### 8.3 Resultados

![Figura 10](../../../../Recursos/Imágenes/Taller5_Palacios_Act04_ArduinoCloud.png)

**Figura 10.** Temperatura en Arduino Cloud.

![Figura 11](../../../../Recursos/Imágenes/Taller5_Palacios_Act04_ThingSpeak.png)

**Figura 11.** Temperatura en ThingSpeak.

![Figura 12](../../../../Recursos/Imágenes/Taller5_Palacios_Act04_Ubidots.png)

**Figura 12.** Temperatura en Ubidots.

Prueba de respuesta: sujetar el LM35 entre los dedos y verificar que la temperatura sube y vuelve a bajar al soltarlo. *(confirmar con captura: temperatura ambiente y temperatura con la mano)*

---

## 9. Actividad 05: controlar un LED desde una plataforma web

### 9.1 Estrategia

Elegí Ubidots con MQTT. En Ubidots se crea una variable `led` en el dispositivo `esp32-equipo02` con un widget tipo *Switch* (valores 1 y 0). El ESP32 se suscribe al tópico `/v1.6/devices/esp32-equipo02/led/lv`, que entrega el último valor de la variable, y enciende o apaga el LED según el valor recibido.

A diferencia de lo que hicimos con ThingSpeak, donde el ESP32 consulta periódicamente (sondeo), aquí es el broker quien empuja el mensaje apenas cambia el switch, así que la respuesta es casi inmediata. Esa es la ventaja de publicación/suscripción de MQTT [7].

| Componente | Pin del ESP32 |
|---|---|
| LED (ánodo, con resistencia de 220 Ω) | GPIO4 |
| LED (cátodo) | GND |

### 9.2 Código

Archivo: `Codigo/Act05_LED_Ubidots/Act05_LED_Ubidots.ino`. La parte clave es la función de recepción:

```cpp
void callback(char* topic, byte* payload, unsigned int length) {
  String mensaje = "";
  for (unsigned int i = 0; i < length; i++) mensaje += (char)payload[i];
  float valor = mensaje.toFloat();          // Ubidots envía "1.0" o "0.0"
  digitalWrite(LED_PIN, valor >= 0.5 ? HIGH : LOW);
}
```

| Elemento | Qué hace |
|---|---|
| `client.setCallback(callback)` | Registra la función que se ejecuta al llegar un mensaje |
| `client.subscribe(topicLed)` | Se suscribe al tópico `.../led/lv` al conectar |
| `client.loop()` | Procesa los mensajes entrantes; debe llamarse en cada vuelta de `loop()` |
| `digitalWrite(LED_PIN, ...)` | Enciende o apaga el LED |

### 9.3 Resultados

![Figura 13](../../../../Recursos/Imágenes/Taller5_Palacios_Act05_Ubidots_switch.png)

**Figura 13.** Widget Switch en Ubidots.

![Figura 14](../../../../Recursos/Imágenes/Taller5_Palacios_Act05_serial.png)

**Figura 14.** Monitor serial con los mensajes recibidos y los avisos «LED ENCENDIDO» y «LED APAGADO».

![Figura 15](../../../../Recursos/Imágenes/Taller5_Palacios_Act05_led_on.png)

**Figura 15.** LED encendido tras activar el switch.

![Figura 16](../../../../Recursos/Imágenes/Taller5_Palacios_Act05_led_off.png)

**Figura 16.** LED apagado tras desactivar el switch.

Latencia observada entre mover el switch y el cambio del LED: *(confirmar con captura)*

---

## 10. Aplicación en LanternGuard

LanternGuard monitorea el biofouling en linternas de concha de abanico. Un nodo sumergido con un ESP32 y dos cámaras Arducam se comunica por RS-485 con una boya que lleva un ESP32-S3 con LoRa, y el procesamiento de imágenes se hace fuera del nodo. Cada actividad del taller tiene su contraparte:

| Actividad | Equivalente en LanternGuard |
|---|---|
| 01. Promediado y conversión del ADC | Lectura estable de sensores del nodo (por ejemplo, voltaje de batería y temperatura del agua). Promediar reduce el ruido, importante porque el ADC del ESP32 no es lineal |
| 02. Conexión Wi-Fi y reconexión | En la boya el enlace a internet no será Wi-Fi, pero la lógica de reconexión automática sirve igual para LoRa y para la salida a la red |
| 03 y 04. Datos a la nube | La boya publicaría lecturas y resultados de la detección de biofouling a una plataforma. Ubidots por MQTT calza mejor que HTTP porque cada mensaje es más liviano |
| 05. Control remoto | Enviar comandos al nodo desde la nube: cambiar la frecuencia de captura, pedir una foto o activar una alerta |

Conclusiones de diseño que salen del taller:

- **Frecuencia de envío.** La restricción de 15 s de ThingSpeak es un ejemplo de un límite real: LoRa también tiene ciclos de trabajo restringidos y el nodo funciona con energía limitada. Conviene enviar poco y resumido (por ejemplo, un índice de biofouling) y no las imágenes completas.
- **Bidireccional.** El nodo sumergido pasa casi todo el tiempo dormido. Un esquema de suscripción como el de la Act. 05 supone que el dispositivo está despierto escuchando, así que en el nodo real los comandos se aplicarían en ventanas de escucha programadas.
- **Seguridad.** Los tokens y claves no se publican en el repositorio. Aquí se usaron marcadores como `TU_API_KEY`.

---

## 11. Conclusiones

- La conversión del ADC a voltaje y el promediado son la base de cualquier lectura confiable. Hay que validar con el multímetro.
- Obtener una IP por DHCP no implica tener un servidor: sin código que escuche peticiones, la IP no responde en el navegador.
- Las tres plataformas resuelven el mismo problema con distinto nivel de abstracción: Arduino Cloud oculta la red, ThingSpeak usa HTTP simple pero limita la frecuencia, y Ubidots usa MQTT, que sirve también para el camino de vuelta.
- Para control remoto, publicación/suscripción (MQTT) es más directo que consultar cada cierto tiempo.

---

## 12. Referencias

[1] Espressif Systems, "ESP32 Series Datasheet." [En línea]. Disponible: https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf

[2] MathWorks, "ThingSpeak Documentation." [En línea]. Disponible: https://www.mathworks.com/help/thingspeak/

[3] Ubidots, "Conectar un ESP32 DevKitC a Ubidots a través de MQTT." [En línea]. Disponible: https://help.ubidots.com/es/articles/748067-conectar-un-esp32-devkitc-a-ubidots-a-traves-de-mqtt

[4] Arduino, "Arduino Cloud: overview." [En línea]. Disponible: https://docs.arduino.cc/arduino-cloud/guides/overview/

[5] Last Minute Engineers, "Getting Started with ESP32 Development Board (Pinout)." [En línea]. Disponible: https://lastminuteengineers.com/getting-started-with-esp32/

[6] Texas Instruments, "LM35 Precision Centigrade Temperature Sensors," hoja de datos. [En línea]. Disponible: https://www.ti.com/lit/ds/symlink/lm35.pdf

[7] OASIS, "MQTT Version 3.1.1." [En línea]. Disponible: https://docs.oasis-open.org/mqtt/mqtt/v3.1.1/mqtt-v3.1.1.html

---

## Anexo A. Pines y conexiones

| Actividad | Componente | Pin del ESP32 | Alimentación |
|---|---|---|---|
| 01 y 03 | Potenciómetro (SIG) | GPIO34 | 3V3 |
| 02 | Solo Wi-Fi | n/a | USB |
| 04 | LM35 (OUT) | GPIO34 | VIN (5 V) |
| 05 | LED con resistencia de 220 Ω | GPIO4 | n/a |

## Anexo B. Capturas pendientes

Las imágenes referenciadas en este documento se guardan en `Recursos/Imágenes/` con el prefijo `Taller5_Palacios_`:
`Act01_conexion`, `Act01_serial`, `Act01_multimetro`, `Act02_ip_serial`, `Act03_ArduinoCloud`, `Act03_ThingSpeak`, `Act03_Ubidots`, `Act03_serial`, `Act04_conexion`, `Act04_ArduinoCloud`, `Act04_ThingSpeak`, `Act04_Ubidots`, `Act05_Ubidots_switch`, `Act05_serial`, `Act05_led_on` y `Act05_led_off` (todas en `.png`).
