# Mini Proyecto IoT: ESP32 Dev Kit 1, MQTT y Node-RED

---

**Curso:** Proyectos de Ingeniería — Taller de Internet de las Cosas (IoT)

**Equipo:** Equipo 02

**Docentes:** De la Cruz, Lewis; Chan, Renzo; Rejas, María; Rivera, Harry.

**Tarjeta:** ESP32 Dev Kit 1 (en Arduino IDE: *ESP32 Dev Module*)

**Protocolo:** MQTT, con el broker `mqtt.rcr-labs.com`

**Interfaz:** Dashboard en Node-RED

**Sensor:** DHT11, temperatura y humedad

> **Nota de seguridad:** por ser un repositorio público, las contraseñas de Wi-Fi y de MQTT aparecen como `TU_RED_WIFI`, `TU_PASSWORD_WIFI` y `TU_PASSWORD_MQTT`. Los valores reales no se publican.

---

## 1. Descripción

En este taller armamos un sistema IoT completo con una tarjeta **ESP32 Dev Kit 1**. El sistema hace tres cosas:

1. **Se conecta a Internet** por Wi-Fi y al **broker MQTT** del taller.
2. **Envía datos** de temperatura y humedad cada 5 segundos.
3. **Recibe órdenes** para encender y apagar el LED azul de la tarjeta.

Todo se ve y se controla desde un **dashboard en Node-RED**.

El trabajo tuvo dos etapas:

- **Etapa 1:** usamos el código del taller, que **inventa** los valores de temperatura y humedad con números al azar (datos simulados). Con eso probamos la comunicación.
- **Etapa 2 (mejora):** cambiamos el código para que los valores sean **reales**, medidos con un sensor **DHT11**.

---

## 2. Objetivo

**Objetivo general**

Comunicar un ESP32 con un broker MQTT para enviar datos de sensores y controlar un LED de forma remota desde un dashboard en Node-RED.

**Objetivos específicos**

- Conectar el ESP32 a una red Wi-Fi y al broker MQTT.
- Configurar los tópicos del Equipo 02 para no mezclar nuestros mensajes con los de otros equipos.
- Publicar datos de temperatura y humedad en formato JSON.
- Recibir los comandos `ON` y `OFF` para controlar el LED azul de la tarjeta.
- Visualizar los datos y controlar el LED desde Node-RED.
- Mejorar el código para publicar **datos reales** con un sensor DHT11.

---

## 3. Materiales y herramientas utilizadas

<div align="center">
  
| Elemento | Para qué se usó |
|---|---|
| ESP32 Dev Kit 1 | Cerebro del sistema: se conecta al Wi-Fi y habla con el broker |
| Sensor DHT11 | Medir temperatura y humedad reales (etapa 2) |
| Protoboard y cables | Conectar el sensor a la tarjeta |
| Cable USB | Alimentar y programar la tarjeta |
| Computadora con Arduino IDE | Escribir y subir el código |
| Celular | Compartir Wi-Fi (hotspot) y comprobar los mensajes MQTT con una app cliente |
| Broker MQTT (`mqtt.rcr-labs.com`, EMQX) | Reparte los mensajes |
| Node-RED | Dashboard para ver datos y controlar el LED |
| Biblioteca `WiFi.h` | Conexión Wi-Fi |
| Biblioteca `PubSubClient.h` | Comunicación MQTT |
| Biblioteca `ArduinoJson.h` | Armar los mensajes en formato JSON |
| Biblioteca `DHT sensor library` (Adafruit) | Leer el sensor DHT11 |

</div>

---

## 4. Conceptos usados

Para el desarrollo de este taller fue fundamenta entender que MQTT es una forma muy ligera de enviar mensajes entre dispositivos. Funciona como un grupo de WhatsApp con temas:

<div align="center">

| Concepto | Explicación simple |
|---|---|
| **Broker** | La "oficina de correos": recibe todos los mensajes y los reparte a quien corresponde |
| **Tópico** | El "tema" o dirección del mensaje, por ejemplo `equipo02/sensor/datos` |
| **Publicar** | Enviar un mensaje a un tópico |
| **Suscribirse** | Pedirle al broker que nos avise cuando llegue un mensaje a un tópico |
| **Cliente** | Cualquier dispositivo o programa conectado al broker (el ESP32, Node-RED, la app del celular) |

</div>

```mermaid
flowchart LR
  E["ESP32"] -- "publica en equipo02/sensor/datos" --> B(("Broker MQTT"))
  B -- "entrega los datos" --> N["Node-RED (dashboard)"]
  B -- "entrega los datos" --> C["App en el celular"]
  N -- "publica ON / OFF en equipo02/actuadores/led" --> B
  B -- "entrega el comando" --> E
```

El ESP32 **publica** datos y se **suscribe** a los comandos. Node-RED hace lo contrario: se suscribe a los datos y publica los comandos.

---

## 5. Configuración inicial del código

Para empezar usamos el código que nos dio el profesor. Este código **no usa ningún sensor**: genera la temperatura y la humedad con números al azar.

<details>
<summary><b>Ver el código inicial completo</b></summary>

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ================= CONFIGURACIÓN WIFI =================
const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";

// ================= CONFIGURACIÓN MQTT =================
const char* MQTT_SERVER   = "mqtt.rcr-labs.com";
const int   MQTT_PORT     = 1883;

const char* MQTT_USER     = "alumno";
const char* MQTT_PASSWORD = "TU_PASSWORD_MQTT";
const char* CLIENT_ID     = "ESP32_Equipo02";

// Topics MQTT (versión del taller)
const char* TOPIC_PUB     = "taller/sensor/datos";
const char* TOPIC_SUB     = "taller/actuadores/led";

// ================= OBJETOS Y VARIABLES ===============
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long ultimoEnvio = 0;
const long intervaloEnvio = 5000; // Envío cada 5 segundos (no bloqueante)

// Conexión a la red Wi-Fi
void setupWiFi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a Wi-Fi: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado con éxito");
  Serial.print("Dirección IP local: ");
  Serial.println(WiFi.localIP());
}

// Recepción de mensajes suscritos (control del LED desde Node-RED)
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensaje recibido en topic [");
  Serial.print(topic);
  Serial.print("]: ");

  String mensaje = "";
  for (unsigned int i = 0; i < length; i++) {
    mensaje += (char)payload[i];
  }
  Serial.println(mensaje);

  if (String(topic) == TOPIC_SUB) {
    if (mensaje == "ON") {
      digitalWrite(2, HIGH);
      Serial.println("Comando: Encender LED");
    } else if (mensaje == "OFF") {
      digitalWrite(2, LOW);
      Serial.println("Comando: Apagar LED");
    }
  }
}

// Reconexión automática al broker EMQX
void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conectar con broker MQTT...");

    if (client.connect(CLIENT_ID, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println(" ¡Conectado!");
      client.subscribe(TOPIC_SUB);
      Serial.print("Suscrito a: ");
      Serial.println(TOPIC_SUB);
    } else {
      Serial.print(" Falló. Código de error rc=");
      Serial.print(client.state());
      Serial.println(" Reintentando en 5 segundos...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setupWiFi();

  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
  pinMode(2, OUTPUT);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long ahora = millis();
  if (ahora - ultimoEnvio >= intervaloEnvio) {
    ultimoEnvio = ahora;

    // Simulación de lectura de sensores (números al azar)
    float tempSimulada = 24.0 + (random(0, 100) / 10.0);
    float humSimulada  = 55.0 + (random(0, 200) / 10.0);

    // Creación del documento JSON
    StaticJsonDocument<200> doc;
    doc["dispositivo"] = CLIENT_ID;
    doc["temperatura"] = serialized(String(tempSimulada, 2));
    doc["humedad"]     = serialized(String(humSimulada, 2));

    char jsonBuffer[256];
    serializeJson(doc, jsonBuffer);

    // Publicación hacia EMQX
    Serial.print("Publicando en ");
    Serial.print(TOPIC_PUB);
    Serial.print(": ");
    Serial.println(jsonBuffer);

    client.publish(TOPIC_PUB, jsonBuffer);
  }
}
```

</details>

<p align="center">
  <img src="https://github.com/user-attachments/assets/bb8b158f-104b-4489-946d-dc50b5d5774a" alt="Código inicial del taller" width="80%"/>
  <br>
  <em><b>Figura 1.</b> Código inicial del taller para la conexión Wi-Fi y MQTT del ESP32.</em>
</p>

### 5.1 Explicación del código en palabras simples

<div align="center">
  
| Parte del código | Qué hace |
|---|---|
| `#include <WiFi.h>` | Trae las funciones para conectarse al Wi-Fi |
| `#include <PubSubClient.h>` | Trae las funciones para usar MQTT |
| `#include <ArduinoJson.h>` | Ayuda a armar el mensaje en formato JSON (ordenado en pares "nombre: valor") |
| `WIFI_SSID` y `WIFI_PASS` | Nombre y contraseña del Wi-Fi que se va a usar |
| `MQTT_SERVER` y `MQTT_PORT` | Dirección del broker y el "puerto" (la puerta) por donde se conecta; 1883 es la puerta estándar sin cifrado |
| `MQTT_USER` y `MQTT_PASSWORD` | Usuario y contraseña para entrar al broker |
| `TOPIC_PUB` | Tópico donde el ESP32 **publica** sus datos |
| `TOPIC_SUB` | Tópico donde el ESP32 **escucha** las órdenes |
| `setupWiFi()` | Se conecta al Wi-Fi y muestra la IP que le asignaron |
| `callback()` | Se ejecuta sola cada vez que llega un mensaje. Si el mensaje es `ON` enciende el LED y si es `OFF` lo apaga |
| `reconnect()` | Si se cae la conexión con el broker, intenta volver a conectarse y se suscribe de nuevo |
| `setup()` | Se ejecuta una vez al inicio: prepara el Serial, el Wi-Fi, el broker y el LED |
| `loop()` | Se repite siempre: mantiene la conexión y, cada 5 segundos, arma y envía el mensaje con los datos |
| `millis()` en lugar de `delay()` | Permite esperar los 5 segundos **sin congelar** el ESP32, para que pueda seguir recibiendo órdenes |
| `random(...)` | Inventa números al azar: así se simulan la temperatura y la humedad |

</div>

---

### 5.2 Configuraciones adicionales

Se modificó el identificador del equipo, la red Wi-Fi y los tópicos de publicación y suscripción.

Después de revisar el código inicial, se realizaron las modificaciones correspondientes para identificar al **Equipo 02**.

### Identificador

El identificador utilizado para el dispositivo fue:

```cpp
const char* CLIENT_ID = "ESP32_Equipo02";
```

Además, es importante resaltar que se modificaron las credenciales de conexión, las cuales no serán mostradas por temas de seguridad, y también se modificó 
la ruta del tópico (TOPIC_PUB) de "taller/sensor/datos" a "equipo02/sensor/datos"; de manera similar con TOPIC_SUB que pasó de "taller/actuadores/led" a "equipo 02/actuadores/led"

### Tópico de publicación

```cpp
const char* TOPIC_PUB = "equipo02/sensor/datos";
```

Este tópico permite publicar la información generada por el ESP32 Dev Kit 1.

### Tópico de suscripción

```cpp
const char* TOPIC_SUB = "equipo02/actuadores/led";
```

Este tópico permite recibir los comandos utilizados para controlar el LED azul integrado del ESP32.


En resumen, para que nuestros mensajes no se mezclen con los de los demás equipos, se hicieron los cambios mencionados anteriormente.

<div align="center">

| Elemento | Antes (taller) | Ahora (Equipo 02) |
| :--- | :--- | :--- |
| Tópico de publicación | `taller/sensor/datos` | `equipo02/sensor/datos` |
| Tópico de suscripción | `taller/actuadores/led` | `equipo02/actuadores/led` |
| Identificador | `ESP32_Equipo02` | `ESP32_Equipo02` |

</div>

<p align="center">
  <img src="https://github.com/user-attachments/assets/3f26d93f-ae3d-46a5-8287-d416b04a2c71" alt="Código con los tópicos del Equipo 02" width="80%"/>
  <br>
  <em><b>Figura 2.</b> Código modificado con los tópicos MQTT del Equipo 02.</em>

---

## 6. Publicación de datos mediante MQTT

Una vez realizada la configuración, el ESP32 Dev Kit 1 fue conectado al broker MQTT.

El programa utilizado genera valores simulados de temperatura y humedad:

```cpp
float tempSimulada = 24.0 + (random(0, 100) / 10.0);
float humSimulada  = 55.0 + (random(0, 200) / 10.0);
```

Estos datos se organizan en formato JSON:

```cpp
StaticJsonDocument<200> doc;

doc["dispositivo"] = CLIENT_ID;
doc["temperatura"] = serialized(String(tempSimulada, 2));
doc["humedad"] = serialized(String(humSimulada, 2));
```

Por ejemplo:

```json
{
  "dispositivo": "ESP32_Equipo02",
  "temperatura": 31.90,
  "humedad": 55.10
}
```

Los valores son enviados periódicamente mediante el tópico:

```text
equipo02/sensor/datos
```

En esta parte del proyecto, los valores de temperatura y humedad fueron **simulados mediante el código**. No corresponden a lecturas realizadas mediante sensores físicos.

<p align="center">
  <img src="URL_IMG_SERIAL_SUSCRITO" alt="Monitor serie publicando datos simulados" width="80%"/>
  <br>
  <em><b>Figura 3.</b> Monitor serie: el ESP32 se suscribe al tópico del LED y publica datos simulados cada 5 segundos.</em>
</p>

---

## 7. Verificación de la publicación MQTT

Para comprobar que los mensajes enviados desde el ESP32 Dev Kit 1 llegaban correctamente al broker MQTT, se realizó una prueba utilizando un cliente MQTT desde un smartphone.

En la aplicación MyMQTT se visualizaron los mensajes correspondientes al tópico del Equipo 02.

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/0b7cb643-f5fa-4b45-96dd-2b1c82a731f7" width="30%"/>
  <br>
  <em><b>Figura 4.</b> Mensajes del ESP32 recibidos en el celular mediante el tópico <code>equipo02/sensor/datos</code>.</em>
</p>

**Interpretación:** la app muestra los mismos mensajes que imprime el ESP32. Eso confirma que los datos salen del ESP32, pasan por el broker y llegan a otro dispositivo. Además, los valores cambian mucho de un mensaje a otro sin ningún motivo (por ejemplo, la temperatura salta de 26.7 °C a 31.9 °C en 5 segundos). Eso es normal en datos simulados, pero no ocurre en el mundo real; lo veremos en la sección 11.

---

## 8. Control remoto del LED

Además de publicar, el ESP32 **escucha** el tópico `equipo02/actuadores/led`. Entiende dos órdenes:

<div align="center">
  
| Orden | Qué hace el ESP32 |
|---|---|
| `ON` | Enciende el LED azul de la tarjeta |
| `OFF` | Apaga el LED azul |

</div>

El LED azul está conectado internamente al pin **GPIO2**. El código que lo controla es:

```cpp
if (String(topic) == TOPIC_SUB) {
  if (mensaje == "ON") {
    digitalWrite(2, HIGH);               // enciende el LED
    Serial.println("Comando: Encender LED");
  } else if (mensaje == "OFF") {
    digitalWrite(2, LOW);                // apaga el LED
    Serial.println("Comando: Apagar LED");
  }
}
```

### 8.1 Prueba con el LED apagado (`OFF`)

El monitor serie mostró:

```text
Mensaje recibido en topic [equipo02/actuadores/led]: OFF
Comando: Apagar LED
```

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/5b7823e1-26f2-4500-be41-92e2a592f393" width="80%"/>
  <br>
  <em><b>Figura 5.</b> Monitor serie: el ESP32 recibe el comando <code>OFF</code> y apaga el LED.</em>
</p>

<p align="center">
  <img alt="image" src="--" width="80%"/>
  <br>
  <em><b>Figura 6.</b> ESP32 en la protoboard con el LED azul apagado (solo queda la luz roja de alimentación).</em>
</p>

### 8.2 Prueba con el LED encendido (`ON`)

El monitor serie mostró:

```text
Mensaje recibido en topic [equipo02/actuadores/led]: ON
Comando: Encender LED
```

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/d5292833-ef80-426f-8248-d6a6d569f965" width="80%"/>
  <br>
  <em><b>Figura 7.</b> Monitor serie: el ESP32 recibe el comando <code>ON</code> y enciende el LED.</em>
</p>

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/41189eae-1c7e-4159-ad49-7a00be5d2028" width="80%"/>
  <br>
  <em><b>Figura 8.</b> ESP32 en la protoboard con el LED azul encendido después de recibir <code>ON</code>.</em>
</p>

**Interpretación:** en ambas pruebas, lo que dice el monitor serie coincide con lo que se ve en la tarjeta. Esto confirma que la comunicación funciona en los dos sentidos: el ESP32 **envía** datos y también **recibe** órdenes. Se ve además que, mientras llegan comandos, el ESP32 sigue publicando datos sin detenerse.

---

## 9. Dashboard en Node-RED

Posteriormente, se utilizó **Node-RED** para desarrollar una interfaz de visualización y control a partir de los datos recibidos mediante MQTT.

El desarrollo del dashboard se realizó en dos etapas. Primero se implementó una versión inicial que permitía comprobar las funciones principales del sistema. Después de verificar su funcionamiento, esta interfaz fue ampliada con nuevas herramientas de monitoreo, procesamiento y control.

### 9.1 Versión inicial del dashboard

En la primera versión se buscó comprobar que Node-RED pudiera recibir correctamente los mensajes publicados por el ESP32 y representar la información dentro de una interfaz gráfica.

El dashboard permitía visualizar:

- La identificación del dispositivo.
- Los valores de temperatura.
- Los valores de humedad.
- El control del LED integrado del ESP32.

El dispositivo utilizado durante las pruebas se identificó como:

```text
ESP32_Equipo02
```

Para controlar el LED se incorporaron los comandos `ON` y `OFF`, enviados desde Node-RED mediante el tópico:

```text
equipo02/actuadores/led
```

Esta primera implementación permitió comprobar que Node-RED podía utilizarse tanto para recibir la información publicada por el ESP32 como para enviar instrucciones hacia el dispositivo.

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/7da0cc5b-e4a7-45fa-b6c7-1d1c56dbebd8"  width="80%"/>
  <br>
  <em><b>Figura 9.</b> Versión inicial del dashboard desarrollado en Node-RED para visualizar los datos enviados por el ESP32 Dev Kit 1 y controlar el LED.</em>
</p>

### 9.2 Mejoras implementadas en el dashboard

Una vez comprobado el funcionamiento de la versión inicial, se realizaron mejoras en el flujo de Node-RED y en la interfaz del dashboard. El objetivo fue organizar mejor la información disponible y añadir herramientas que permitieran interpretar el comportamiento del sistema con mayor facilidad.

La versión mejorada incorporó las siguientes funciones:

- Estado de conexión del dispositivo mediante los indicadores **EN LÍNEA**, **SIN SEÑAL** y **ESPERANDO DATOS**.
- Identificación del dispositivo conectado.
- Registro de la hora correspondiente a la última lectura recibida.
- Contador de lecturas procesadas.
- Visualización del valor actual de temperatura.
- Visualización del valor actual de humedad relativa.
- Cálculo de los valores mínimo, promedio y máximo de temperatura.
- Cálculo de los valores mínimo, promedio y máximo de humedad.
- Gráfico histórico de temperatura y humedad.
- Indicador visual del estado del LED.
- Botones independientes para **ENCENDER** y **APAGAR** el LED.
- Función adicional para hacer **parpadear el LED tres veces**.
- Umbral configurable para la temperatura.
- Generación de una alerta cuando la temperatura supera el límite establecido.
- Opción para reiniciar las estadísticas y el gráfico.
- Validación de las lecturas recibidas antes de mostrarlas en la interfaz.

El encabezado del dashboard permite identificar rápidamente si el dispositivo continúa enviando información. Cuando se reciben datos, se muestra el estado **EN LÍNEA**, junto con el identificador del ESP32, la hora de la última lectura y la cantidad de registros recibidos.

Si transcurren más de **15 segundos** sin recibir un nuevo mensaje MQTT, el sistema cambia el estado mostrado en la interfaz para indicar que no se están recibiendo datos.

### 9.3 Visualización de temperatura y humedad

La temperatura y la humedad se presentan mediante tarjetas independientes.

Cada tarjeta muestra el valor recibido más recientemente y, además, conserva estadísticas calculadas durante la ejecución:

```text
mínimo
promedio
máximo
```

De esta manera, el usuario no observa únicamente el valor instantáneo, sino también cómo se ha comportado cada variable desde que comenzaron a procesarse los datos.

También se incorporó un gráfico denominado:

```text
Historial · últimos 10 minutos
```

En este gráfico se representan simultáneamente las variaciones de temperatura y humedad, lo que facilita observar la evolución de ambas variables a lo largo del tiempo.

### 9.4 Control mejorado del LED

El control del LED mantiene los comandos MQTT empleados en la primera versión:

```text
ON  → encender
OFF → apagar
```

Estos comandos se publican en:

```text
equipo02/actuadores/led
```

La interfaz incorpora un indicador gráfico que representa el último estado enviado. Cuando se utiliza el comando `ON`, el indicador cambia a **Encendido**; al utilizar `OFF`, cambia a **Apagado**.

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/602af289-c757-49bf-8407-b8a897f22848"  width="80%"/>
  <br>
  <em><b>Figura 10.</b> Versión mejorada del dashboard con el indicador del LED en estado apagado.</em>
</p>

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/f5f3a76d-6b59-442f-8a31-5b84dcc091ec"  width="80%"/>
  <br>
  <em><b>Figura 11.</b> Versión mejorada del dashboard después de enviar el comando de encendido al LED del ESP32.</em>
</p>

Además de los comandos individuales, se incorporó el botón:

```text
Parpadear 3 veces
```

Al utilizarlo, Node-RED genera automáticamente la secuencia:

```text
ON → OFF → ON → OFF → ON → OFF
```

Los cambios se envían con intervalos de aproximadamente 500 ms, produciendo tres ciclos de encendido y apagado. La secuencia termina con el LED apagado.

### 9.5 Umbral y alerta de temperatura

También se añadió una herramienta para establecer un **umbral de temperatura**.

El valor inicial utilizado es:

```text
30 °C
```

El dashboard permite modificar este límite mediante un control deslizante dentro del rango:

```text
20 °C a 40 °C
```

El valor seleccionado se guarda dentro del flujo de Node-RED y se compara con cada nueva temperatura recibida.

Cuando:

```text
Temperatura > Umbral
```

se genera una alerta indicando que la temperatura ha superado el límite establecido.

La tarjeta de temperatura también incluye una marca visual que representa la posición del umbral, permitiendo comparar rápidamente el valor actual con el límite configurado.

### 9.6 Validación y reinicio de los datos

Antes de actualizar el dashboard, el flujo comprueba que los valores recibidos puedan interpretarse correctamente como temperatura y humedad.

También se establecieron límites para evitar que datos evidentemente fuera de rango sean utilizados para actualizar las estadísticas:

```text
Temperatura: -20 °C a 60 °C
Humedad:      0 % a 100 %
```

Si una lectura se encuentra fuera de estos límites, se descarta y el flujo genera un aviso para facilitar la identificación de posibles errores.

Finalmente, se añadió el botón:

```text
Reiniciar estadísticas y gráfico
```

Esta función permite borrar los valores acumulados de mínimo, promedio y máximo, además de limpiar los datos mostrados en el gráfico, para comenzar una nueva observación sin necesidad de reiniciar todo el sistema.

---

## 10. Flujo implementado en Node-RED

### 10.1 Flujo inicial

En la primera versión de Node-RED se configuró un flujo para recibir los mensajes publicados mediante el tópico:

```text
equipo02/sensor/datos
```

Los mensajes recibidos contienen principalmente la identificación del dispositivo, la temperatura y la humedad.

La recepción de datos puede representarse de la siguiente manera:

```text
ESP32 Dev Kit 1
       │
       ▼
   Broker MQTT
       │
       ▼
equipo02/sensor/datos
       │
       ▼
    Node-RED
       │
       ├── Temperatura
       │
       ├── Humedad
       │
       └── Dispositivo
```

Para el control del LED se utiliza el proceso inverso:

```text
Dashboard Node-RED
        │
        ▼
   Control LED
        │
        ▼
equipo02/actuadores/led
        │
        ▼
   Broker MQTT
        │
        ▼
ESP32 Dev Kit 1
        │
        ▼
     LED azul
```

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/2163734e-61d9-4dbb-b37f-6c9be8f5ffcf" width="80%"/>
  <br>
  <em><b>Figura 12.</b> Flujo inicial implementado en Node-RED para recibir datos mediante MQTT y enviar comandos al LED del ESP32.</em>
</p>

### 10.2 Flujo mejorado

A partir del flujo inicial se incorporaron nuevos nodos para ampliar el procesamiento de la información y las funciones disponibles en el dashboard.

El nodo principal denominado **Procesar datos** recibe los mensajes provenientes del tópico:

```text
equipo02/sensor/datos
```

y se encarga de validar y distribuir la información hacia los distintos componentes de la interfaz.

De manera general, el flujo mejorado funciona de la siguiente forma:

```text
equipo02/sensor/datos
        │
        ▼
    Datos ESP32
        │
        ├── Ver mensajes
        │
        ├── Sin datos 15 s
        │       │
        │       └── Estado del dispositivo
        │
        └── Procesar datos
                │
                ├── Tarjeta temperatura
                ├── Tarjeta humedad
                ├── Gráfico histórico
                ├── Encabezado
                └── Aviso de temperatura
```

El nodo **Procesar datos** realiza varias operaciones antes de actualizar la interfaz:

```text
Lectura del mensaje MQTT
        ↓
Conversión de temperatura y humedad
        ↓
Validación de los valores
        ↓
Actualización del contador
        ↓
Cálculo de mínimo, promedio y máximo
        ↓
Comparación con el umbral
        ↓
Distribución hacia el dashboard
```

De forma paralela, el nodo **Sin datos 15 s** supervisa la llegada de mensajes. Si transcurre ese periodo sin recibir una nueva lectura, la interfaz cambia el estado del dispositivo para informar que se ha perdido temporalmente el flujo de datos.

### 10.3 Flujo de control del LED

El control del LED se mantiene separado del procesamiento de temperatura y humedad.

Los botones **ENCENDER** y **APAGAR** generan directamente los mensajes:

```text
ON
OFF
```

que se publican mediante el nodo **Comandos LED** en:

```text
equipo02/actuadores/led
```

El flujo de control es:

```text
Dashboard
    │
    ├── ENCENDER ──→ ON
    │
    ├── APAGAR   ──→ OFF
    │
    └── Parpadear 3 veces
                │
                ▼
       Secuencia ON/OFF
                │
                ▼
        Comandos LED
                │
                ▼
equipo02/actuadores/led
                │
                ▼
           Broker MQTT
                │
                ▼
             ESP32
```

Para la función de parpadeo se utiliza una secuencia programada:

```text
ON → OFF → ON → OFF → ON → OFF
```

Después de completar los tres ciclos, el estado final enviado es `OFF`.

### 10.4 Flujo del umbral de temperatura

Para el sistema de alerta se estableció inicialmente un umbral de:

```text
30 °C
```

Este valor es enviado al control deslizante del dashboard y posteriormente almacenado dentro del flujo.

El proceso puede resumirse como:

```text
Umbral inicial 30 °C
        │
        ▼
     Slider
        │
        ▼
  Guardar umbral
        │
        ├── Actualizar texto de la regla
        │
        └── Comparar con temperatura
```

Cuando la temperatura supera el umbral seleccionado, el sistema genera una notificación.

<p align="center">
  <img alt="image" src="https://github.com/user-attachments/assets/7ce10bf3-1d90-45a0-b032-0b2bbcf2ca8c" width="80%"/>
  <br>
  <em><b>Figura 13.</b> Flujo mejorado en Node-RED con procesamiento de datos, monitoreo del estado de conexión, control del LED, alertas y configuración del umbral de temperatura.</em>
</p>

---

## 11. Mejora del código: datos reales con el sensor DHT11

### 11.1 ¿Por qué mejorar el código?

Hasta ahora, la temperatura y la humedad eran **números inventados**. Para que el sistema sirva de verdad, necesitamos que sean **mediciones reales**. Por eso conectamos un sensor **DHT11** y cambiamos el código.

### 11.2 ¿Qué es el DHT11?

Es un sensor pequeño y económico que mide **la temperatura** y **la humedad del aire**. Envía los dos datos al ESP32 por **un solo cable de datos**.

<div align="center">
  
| Característica | Valor del DHT11 |
|---|---|
| Rango de temperatura | 0 a 50 °C |
| Error de temperatura | ± 2 °C |
| Rango de humedad | 20 a 90 % |
| Error de humedad | ± 5 % |
| Velocidad máxima de lectura | 1 vez por segundo |
| Alimentación | 3.3 V a 5 V |

</div>

Como mide en pasos grandes, la humedad aparece en **números enteros** (55.0, 59.0, 66.0...) [3].

### 11.3 Conexión del sensor

<div align="center">
  
| Pin del DHT11 | Pin del ESP32 |
|---|---|
| Datos (S, OUT o DATA) | GPIO4 (D4) |
| Alimentación (V o +) | 3V3 |
| Tierra (G o −) | GND |

</div>

<p align="center">
  <img src="URL_IMG_CONEXION_DHT11" alt="Conexión del DHT11" width="80%"/>
  <br>
  <em><b>Figura 11.</b> Conexión del sensor DHT11 al ESP32 (datos al GPIO4, alimentación a 3V3 y tierra a GND).</em>
</p>

### 11.4 Biblioteca necesaria

Se instaló en Arduino IDE la biblioteca **DHT sensor library** (de Adafruit), junto con **Adafruit Unified Sensor**, que necesita para funcionar [4].

### 11.5 Qué cambió: antes y después

Solo hubo cuatro cambios. Todo lo demás (Wi-Fi, MQTT, tópicos y control del LED) quedó igual.

<div align="center">

| # | Cambio | Antes (simulado) | Después (real) |
|---|---|---|---|
| 1 | Biblioteca del sensor | — | `#include <DHT.h>` |
| 2 | Definir el sensor | — | `#define DHTPIN 4`, `#define DHTTYPE DHT11` y `DHT dht(DHTPIN, DHTTYPE);` |
| 3 | Iniciar el sensor | — | `dht.begin();` dentro de `setup()` |
| 4 | Obtener los valores | Números al azar con `random()` | Lecturas del sensor con `dht.readTemperature()` y `dht.readHumidity()` |

</div>

**Antes** (datos simulados):

```cpp
float tempSimulada = 24.0 + (random(0, 100) / 10.0);
float humSimulada  = 55.0 + (random(0, 200) / 10.0);
```

**Después** (datos reales):

```cpp
// Lectura REAL del DHT11
float temperatura = dht.readTemperature();   // en °C
float humedad     = dht.readHumidity();      // en %

// Si el sensor falla, devuelve NaN (no es un número): no publicamos datos inválidos
if (isnan(temperatura) || isnan(humedad)) {
  Serial.println("Error al leer el DHT11. Revisa el cableado.");
  return;
}
```

Además, el mensaje JSON ahora se arma con **un decimal** en lugar de dos, porque el DHT11 no es tan preciso como para justificar más:

```cpp
doc["temperatura"] = serialized(String(temperatura, 1));
doc["humedad"]     = serialized(String(humedad, 1));
```

### 11.6 Explicación de lo nuevo en palabras simples

<div align="center">
  
| Línea | Qué hace |
|---|---|
| `#define DHTPIN 4` | Le dice al ESP32 en qué pin está conectado el cable de datos del sensor |
| `#define DHTTYPE DHT11` | Le dice qué modelo de sensor es (existen otros, como el DHT22) |
| `DHT dht(DHTPIN, DHTTYPE);` | Crea el "objeto" sensor con esos datos |
| `dht.begin();` | Enciende y prepara el sensor |
| `dht.readTemperature()` | Le pide al sensor la temperatura en °C |
| `dht.readHumidity()` | Le pide al sensor la humedad en % |
| `isnan(...)` | Revisa si la lectura falló. Si falló, el código avisa y **no envía datos falsos** |
| `return;` | Salta este envío y espera al siguiente ciclo |

</div>

### 11.7 Código mejorado completo

<details>
<summary><b>Ver el código mejorado completo</b></summary>

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>

// ================= CONFIGURACIÓN WIFI =================
const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";

// ================= CONFIGURACIÓN MQTT =================
const char* MQTT_SERVER   = "mqtt.rcr-labs.com";
const int   MQTT_PORT     = 1883;

const char* MQTT_USER     = "alumno";
const char* MQTT_PASSWORD = "TU_PASSWORD_MQTT";
const char* CLIENT_ID     = "ESP32_Equipo02";

// Topics MQTT del Equipo 02
const char* TOPIC_PUB     = "equipo02/sensor/datos";
const char* TOPIC_SUB     = "equipo02/actuadores/led";

// ================= SENSOR DHT11 =================
#define DHTPIN  4          // Pin de datos del DHT11 (GPIO4)
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// ================= OBJETOS Y VARIABLES ===============
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long ultimoEnvio = 0;
const long intervaloEnvio = 5000; // Envío cada 5 segundos (no bloqueante)

// Conexión a la red Wi-Fi
void setupWiFi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a Wi-Fi: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado con éxito");
  Serial.print("Dirección IP local: ");
  Serial.println(WiFi.localIP());
}

// Recepción de mensajes suscritos (control del LED desde Node-RED)
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensaje recibido en topic [");
  Serial.print(topic);
  Serial.print("]: ");

  String mensaje = "";
  for (unsigned int i = 0; i < length; i++) {
    mensaje += (char)payload[i];
  }
  Serial.println(mensaje);

  if (String(topic) == TOPIC_SUB) {
    if (mensaje == "ON") {
      digitalWrite(2, HIGH);
      Serial.println("Comando: Encender LED");
    } else if (mensaje == "OFF") {
      digitalWrite(2, LOW);
      Serial.println("Comando: Apagar LED");
    }
  }
}

// Reconexión automática al broker EMQX
void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conectar con broker MQTT...");

    if (client.connect(CLIENT_ID, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println(" ¡Conectado!");
      client.subscribe(TOPIC_SUB);
      Serial.print("Suscrito a: ");
      Serial.println(TOPIC_SUB);
    } else {
      Serial.print(" Falló. Código de error rc=");
      Serial.print(client.state());
      Serial.println(" Reintentando en 5 segundos...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  dht.begin();                 // Inicia el sensor DHT11
  setupWiFi();

  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long ahora = millis();
  if (ahora - ultimoEnvio >= intervaloEnvio) {
    ultimoEnvio = ahora;

    // Lectura REAL del DHT11
    float temperatura = dht.readTemperature();   // °C
    float humedad     = dht.readHumidity();      // %

    // Si el sensor falla, devuelve NaN: no publicamos datos inválidos
    if (isnan(temperatura) || isnan(humedad)) {
      Serial.println("Error al leer el DHT11. Revisa el cableado.");
      return;
    }

    // Creación del documento JSON
    StaticJsonDocument<200> doc;
    doc["dispositivo"] = CLIENT_ID;
    doc["temperatura"] = serialized(String(temperatura, 1));
    doc["humedad"]     = serialized(String(humedad, 1));

    char jsonBuffer[256];
    serializeJson(doc, jsonBuffer);

    Serial.print("Publicando en ");
    Serial.print(TOPIC_PUB);
    Serial.print(": ");
    Serial.println(jsonBuffer);

    client.publish(TOPIC_PUB, jsonBuffer);
  }
}
```

</details>

### 11.8 Resultados con el sensor real

**Prueba 1: el sensor en reposo.** Con el sensor quieto en el aire del laboratorio, los valores se mantuvieron estables: la humedad se quedó en **55.0 %** y la temperatura bajó muy poco, entre **26.6 °C y 26.3 °C**.

<p align="center">
  <img src="URL_IMG_DHT_REPOSO" alt="Datos reales del DHT11 en reposo" width="80%"/>
  <br>
  <em><b>Figura 12.</b> Código mejorado y monitor serie con datos reales del DHT11 en reposo: valores estables.</em>
</p>

**Prueba 2: soplando aire con la boca.** Para comprobar que el sensor realmente mide, le soplamos aire con la boca. El aire que sale de la boca está **más húmedo y un poco más caliente** que el del ambiente.

<p align="center">
  <img src="URL_IMG_DHT_SOPLAR" alt="Humedad subiendo al soplar" width="80%"/>
  <br>
  <em><b>Figura 13.</b> Monitor serie al soplar aire sobre el DHT11: la humedad sube de 55 % a 76 % en unos 30 segundos.</em>
</p>

Lecturas de la Figura 13, una cada 5 segundos:

<div align="center">
  
| Lectura | Temperatura (°C) | Humedad (%) |
|---|---|---|
| 1 | 25.8 | 55.0 |
| 2 | 25.8 | 55.0 |
| 3 | 25.8 | 59.0 |
| 4 | 26.0 | 66.0 |
| 5 | 26.1 | 71.0 |
| 6 | 26.2 | 72.0 |
| 7 | 26.3 | 76.0 |

</div>

**Interpretación:**

- La **humedad subió 21 puntos** (de 55 % a 76 %) en unos 30 segundos. El aliento lleva vapor de agua, así que el aire alrededor del sensor se volvió más húmedo y el sensor lo detectó.
- La **temperatura subió medio grado** (de 25.8 °C a 26.3 °C), porque el aliento está más caliente que el ambiente.
- Los cambios son **suaves y tienen sentido**: suben poco a poco mientras sopla. Esto es muy distinto de los datos simulados, que saltaban sin motivo (por ejemplo, de 25.7 °C a 33.9 °C en solo 5 segundos).
- El sensor **no reacciona de golpe**: la humedad tarda unos segundos en subir. Es normal en el DHT11, que es un sensor lento.

Estos resultados demuestran que el código mejorado ya publica **datos reales** y que el sensor responde a cambios del ambiente.

### 11.9 Datos reales en el dashboard

Con la mejora, los datos que llegan a Node-RED ya no son inventados: son las mediciones del sensor. No fue necesario cambiar el dashboard, porque el mensaje JSON conserva la misma estructura (`dispositivo`, `temperatura` y `humedad`).

<p align="center">
  <img src="URL_IMG_DASHBOARD_REAL" alt="Dashboard con datos reales del DHT11" width="80%"/>
  <br>
  <em><b>Figura 14.</b> Dashboard de Node-RED mostrando la temperatura y la humedad reales medidas por el DHT11.</em>
</p>

---

## 12. Comparación: datos simulados vs. datos reales

<div align="center">
  
| Aspecto | Etapa 1 (simulado) | Etapa 2 (DHT11) |
|---|---|---|
| Origen de los datos | Números al azar (`random`) | Medición del sensor |
| Decimales en el mensaje | 2 | 1 |
| Comportamiento | Saltos bruscos sin motivo | Cambios suaves que dependen del ambiente |
| Reacciona al ambiente | No | Sí (por ejemplo, al soplar) |
| ¿Sirve para tomar decisiones? | No | Sí, con el error propio del DHT11 |
| Si el sensor falla | No aplica | El código lo detecta y no envía datos falsos |

</div>

---

## 13. Resultados

Durante esta parte del mini proyecto se logró:

- Conectar correctamente el ESP32 Dev Kit 1 a la red Wi-Fi.
- Establecer comunicación con el broker MQTT.
- Configurar los tópicos correspondientes al Equipo 02.
- Publicar datos simulados de temperatura y humedad.
- Verificar la recepción de los mensajes mediante un cliente MQTT.
- Recibir comandos mediante el tópico `equipo02/actuadores/led`.
- Apagar el LED azul mediante el comando `OFF`.
- Encender el LED azul mediante el comando `ON`.
- Visualizar la información mediante un dashboard en Node-RED.
- Controlar el LED del ESP32 Dev Kit 1 desde Node-RED.

Después de comprobar estas funciones en la versión inicial, se mejoró el código para publicar datos reales de temperatura y humedad con un sensor DHT11 y se comprobó que el sensor respondiera: vimos que la humedad subió de 55 % a 76 % al soplar aire sobre él.

Asimismo, el dashboard fue ampliado con nuevas herramientas de monitoreo y control. 

La versión mejorada permitió visualizar el valor actual de temperatura y humedad junto con sus respectivos valores mínimo, promedio y máximo. También se incorporó un gráfico histórico que permite observar la evolución de ambas variables.

Asimismo, se implementó un indicador para conocer el estado de recepción de datos del dispositivo. Si los mensajes llegan correctamente, el dashboard muestra **EN LÍNEA**; si dejan de recibirse durante más de 15 segundos, el sistema informa la ausencia de señal.

El control del LED fue ampliado con un indicador visual de estado y una función para hacerlo parpadear tres veces mediante una secuencia automática de comandos `ON` y `OFF`.

Finalmente, se añadió un umbral configurable de temperatura que permite generar una alerta al superar el límite seleccionado, además de una opción para reiniciar las estadísticas y el gráfico.

Estas mejoras permitieron pasar de una interfaz básica de visualización y control a un dashboard con mayores capacidades de monitoreo, procesamiento e interacción.

---

## 14. Conclusiones

La actividad permitió comprobar de manera práctica el funcionamiento de la comunicación MQTT utilizando un ESP32 Dev Kit 1.

La modificación de los tópicos permitió identificar la comunicación correspondiente al **Equipo 02**, separándola de los demás equipos participantes.

También se comprobó que el ESP32 Dev Kit 1 puede trabajar de manera bidireccional mediante MQTT, publicando información sobre el entorno y recibiendo comandos para controlar su LED integrado.

El reemplazo de los datos simulados por el sensor **DHT11** permitió medir la temperatura y humedad del ambiente en tiempo real, comprobando su respuesta al aplicar flujo de aire directamente sobre él.

Además, el uso de un mensaje JSON bien estructurado permitió cambiar la fuente de datos en el código con solo cuatro modificaciones, manteniendo el dashboard funcionando sin cambios.

La inclusión de la función `isnan()` mejoró la seguridad del programa, evitando el envío de datos erróneos en caso de fallas o desconexiones del sensor.

El desarrollo del dashboard en Node-RED evolucionó desde un control básico con botones `ON` y `OFF` hasta una interfaz avanzada con gráficos históricos, estadísticas, monitoreo de conexión y alertas por umbral de temperatura.

De esta manera, el mini proyecto demuestra la integración de **ESP32, MQTT y Node-RED** para medir, transmitir y controlar datos en tiempo real, sirviendo como base para la arquitectura de nuestro proyecto **LanternGuard**.

---
