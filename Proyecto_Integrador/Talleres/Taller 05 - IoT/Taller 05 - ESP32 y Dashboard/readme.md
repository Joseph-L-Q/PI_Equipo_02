# Mini Proyecto IoT: ESP32 Dev Kit 1, MQTT y Node-RED

## 1. Descripción

Como parte del taller de Internet de las Cosas (IoT), se realizó una implementación utilizando una tarjeta **ESP32 Dev Kit 1**, comunicación mediante el protocolo **MQTT** y una interfaz desarrollada en **Node-RED**.

En esta parte del mini proyecto se configuró el ESP32 Dev Kit 1 para conectarse a una red Wi-Fi y posteriormente al broker MQTT utilizado durante el taller.

El código inicial fue adaptado para trabajar con los tópicos correspondientes al **Equipo 02**. Posteriormente, se comprobó la publicación de datos mediante MQTT y se implementó el control remoto del LED azul integrado del ESP32.

Finalmente, mediante Node-RED se desarrolló un dashboard que permitió visualizar los datos enviados por el dispositivo y controlar el encendido y apagado del LED.


---

## 2. Objetivo

Implementar una comunicación IoT utilizando un ESP32 Dev Kit 1 y el protocolo MQTT, permitiendo el envío de información hacia un broker y el control remoto del LED integrado de la tarjeta mediante Node-RED.

---

## 3. Materiales y herramientas utilizadas

- ESP32 Dev Kit 1
- Protoboard
- Cable USB
- Computadora
- Smartphone
- Arduino IDE
- Node-RED
- Broker MQTT
- Biblioteca `WiFi.h`
- Biblioteca `PubSubClient.h`
- Biblioteca `ArduinoJson.h`

---

## 4. Configuración inicial del código

Para iniciar la actividad se utilizó el código proporcionado durante el taller.

El programa utiliza las siguientes bibliotecas:

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
```

La biblioteca `WiFi.h` permite realizar la conexión del ESP32 Dev Kit 1 a una red Wi-Fi.

La biblioteca `PubSubClient.h` permite establecer la comunicación mediante MQTT.

La biblioteca `ArduinoJson.h` permite organizar la información que será enviada utilizando formato JSON.

Código inicial : 
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ================= CONFIGURACIÓN WIFI =================
const char* WIFI_SSID = "POCO_F5";
const char* WIFI_PASS = "87654321";

// ================= CONFIGURACIÓN MQTT =================
// Puedes usar el dominio o la IP directa 108.181.195.81
const char* MQTT_SERVER   = "mqtt.rcr-labs.com"; 
const int   MQTT_PORT     = 1883;

// Credenciales configuradas en EMQX (Autenticación interna)
const char* MQTT_USER     = "alumno";          // o equipo0, equipo1, etc.
const char* MQTT_PASSWORD = "UPCH2026";
const char* CLIENT_ID     = "ESP32_Equipo02";

// Topics MQTT
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

// Recepción de mensajes suscritos (por si deseas controlar actuadores desde Node-RED)
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Mensaje recibido en topic [");
  Serial.print(topic);
  Serial.print("]: ");

  String mensaje = "";
  for (unsigned int i = 0; i < length; i++) {
    mensaje += (char)payload[i];
  }
  Serial.println(mensaje);

  // Ejemplo: procesar comando
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
    
    // Autenticación con credenciales en EMQX
    if (client.connect(CLIENT_ID, MQTT_USER, MQTT_PASSWORD)) {
      Serial.println(" ¡Conectado!");
      
      // Suscribirse a tópicos de control si es necesario
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
  pinMode(2,OUTPUT);
}

void loop() {
  // Asegurar persistencia de la sesión MQTT
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Envío periódico sin usar delay() para no congelar la recepción
  unsigned long ahora = millis();
  if (ahora - ultimoEnvio >= intervaloEnvio) {
    ultimoEnvio = ahora;

    // Simulación de lectura de sensores (ej. DHT22 o BMP280)
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

### Configuración de la red Wi-Fi

Para conectar el ESP32 Dev Kit 1 a la red Wi-Fi utilizada durante la prueba, se modificaron las credenciales de conexión de la siguiente manera:

```cpp
const char* WIFI_SSID = "POCO_F5";
const char* WIFI_PASS = "87654321";

<img width="1600" height="943" alt="image" src="https://github.com/user-attachments/assets/bb8b158f-104b-4489-946d-dc50b5d5774a" />

**Figura 1. Código inicial utilizado para configurar la conexión Wi-Fi y la comunicación MQTT del ESP32 Dev Kit 1.**

---

## 5. Configuración para el Equipo 02

Después de revisar el código inicial, se realizaron las modificaciones correspondientes para identificar al **Equipo 02**.

El identificador utilizado para el dispositivo fue:

```cpp
const char* CLIENT_ID = "ESP32_Equipo02";
```

También se modificaron los tópicos de publicación y suscripción.

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

<img width="1600" height="943" alt="image" src="https://github.com/user-attachments/assets/3f26d93f-ae3d-46a5-8287-d416b04a2c71" />


**Figura 2. Código modificado con los tópicos MQTT correspondientes al Equipo 02.**

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

---

## 7. Verificación de la publicación MQTT

Para comprobar que los mensajes enviados desde el ESP32 Dev Kit 1 llegaban correctamente al broker MQTT, se realizó una prueba utilizando un cliente MQTT desde un smartphone.

En la aplicación se visualizaron los mensajes correspondientes al tópico del Equipo 02.

<img width="720" height="1600" alt="image" src="https://github.com/user-attachments/assets/0b7cb643-f5fa-4b45-96dd-2b1c82a731f7" />


**Figura 3. Recepción en un smartphone de los mensajes publicados por el ESP32 Dev Kit 1 mediante el tópico `equipo02/sensor/datos`.**

Esta prueba permitió verificar que el dispositivo estaba publicando correctamente la información mediante MQTT.

---

## 8. Control remoto del LED

Además de publicar información, el ESP32 Dev Kit 1 fue configurado para recibir comandos mediante MQTT.

El dispositivo se suscribió al tópico:

```text
equipo02/actuadores/led
```

Dentro del código se configuraron dos comandos:

```text
ON
OFF
```

Cuando el ESP32 recibe el comando `ON`, se activa el LED integrado.

Cuando recibe el comando `OFF`, el LED se apaga.

La parte del código responsable de esta función es:

```cpp
if (String(topic) == TOPIC_SUB) {

  if (mensaje == "ON") {

    digitalWrite(2, HIGH);
    Serial.println("Comando: Encender LED");

  } else if (mensaje == "OFF") {

    digitalWrite(2, LOW);
    Serial.println("Comando: Apagar LED");
  }
}
```

---

## 9. Prueba con el LED apagado

Primero se realizó una prueba enviando el comando:

```text
OFF
```

En el Monitor Serial se pudo visualizar la recepción del mensaje correspondiente al tópico del Equipo 02.

```text
Mensaje recibido en topic [equipo02/actuadores/led]: OFF
Comando: Apagar LED
```

<img width="1600" height="941" alt="image" src="https://github.com/user-attachments/assets/5b7823e1-26f2-4500-be41-92e2a592f393" />


**Figura 4. Recepción del comando `OFF` mediante MQTT para apagar el LED azul integrado del ESP32 Dev Kit 1.**

Posteriormente, se verificó físicamente el estado del ESP32 Dev Kit 1.

<img width="1198" height="1600" alt="image" src="https://github.com/user-attachments/assets/e54fc706-676e-4d56-8837-6990ba83d214" />


**Figura 5. Montaje físico del ESP32 Dev Kit 1 en la protoboard con el LED azul apagado.**

---

## 10. Prueba con el LED encendido

Luego se realizó una segunda prueba enviando el comando:

```text
ON
```

En el Monitor Serial se visualizó:

```text
Mensaje recibido en topic [equipo02/actuadores/led]: ON
Comando: Encender LED
```

<img width="1600" height="947" alt="image" src="https://github.com/user-attachments/assets/d5292833-ef80-426f-8248-d6a6d569f965" />


**Figura 6. Recepción del comando `ON` mediante MQTT para encender el LED azul integrado del ESP32 Dev Kit 1.**

También se comprobó físicamente que el LED azul de la tarjeta se encendiera.

<img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/41189eae-1c7e-4159-ad49-7a00be5d2028" />


**Figura 7. Montaje físico del ESP32 Dev Kit 1 en la protoboard con el LED azul encendido después de recibir el comando `ON` mediante MQTT.**

---

## 11. Dashboard en Node-RED

Posteriormente, se utilizó **Node-RED** para desarrollar una interfaz de visualización y control.

El dashboard del Equipo 02 permite observar la información recibida desde el ESP32 Dev Kit 1.

Dentro del dashboard se muestran:

- Identificación del dispositivo.
- Temperatura simulada.
- Humedad simulada.
- Control del LED.

El dispositivo aparece identificado como:

```text
ESP32_Equipo02
```

También se incorporó un control para el LED que permite enviar los comandos `ON` y `OFF`.

<img width="1600" height="842" alt="image" src="https://github.com/user-attachments/assets/aed357c0-e7b0-427a-b13e-6d82da3a2321" />


**Figura 8. Dashboard desarrollado en Node-RED para visualizar los datos enviados por el ESP32 Dev Kit 1 y controlar el LED.**

---

## 12. Flujo implementado en Node-RED

En Node-RED se configuró un flujo para recibir los mensajes publicados mediante el tópico:

```text
equipo02/sensor/datos
```

Los datos recibidos se procesan para obtener los valores correspondientes a:

- Temperatura
- Humedad
- Dispositivo

Estos valores son enviados posteriormente a los elementos gráficos del dashboard.

De manera general, la recepción de información funciona de la siguiente manera:

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

<img width="1600" height="849" alt="image" src="https://github.com/user-attachments/assets/0c0b8a7c-9ab2-4ea8-a380-63457bc85318" />


**Figura 9. Flujo implementado en Node-RED para recibir los datos publicados por el ESP32 Dev Kit 1 y enviar comandos para controlar el LED.**

---

## 13. Código utilizado

El siguiente código corresponde a la configuración utilizada durante esta parte del mini proyecto.

> Por seguridad, las contraseñas reales de Wi-Fi y MQTT no se muestran en el repositorio.

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ================= CONFIGURACIÓN WIFI =================

const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";

// ================= CONFIGURACIÓN MQTT =================

const char* MQTT_SERVER = "mqtt.rcr-labs.com";
const int MQTT_PORT = 1883;

const char* MQTT_USER = "alumno";
const char* MQTT_PASSWORD = "TU_PASSWORD_MQTT";

const char* CLIENT_ID = "ESP32_Equipo02";

// Topics MQTT

const char* TOPIC_PUB = "equipo02/sensor/datos";
const char* TOPIC_SUB = "equipo02/actuadores/led";

// ================= OBJETOS Y VARIABLES =================

WiFiClient espClient;
PubSubClient client(espClient);

unsigned long ultimoEnvio = 0;

const long intervaloEnvio = 5000;

// ================= CONEXIÓN WIFI =================

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

// ================= RECEPCIÓN MQTT =================

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

// ================= RECONEXIÓN MQTT =================

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

// ================= CONFIGURACIÓN =================

void setup() {

  Serial.begin(115200);

  setupWiFi();

  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);

  pinMode(2, OUTPUT);
}

// ================= EJECUCIÓN PRINCIPAL =================

void loop() {

  if (!client.connected()) {

    reconnect();
  }

  client.loop();

  unsigned long ahora = millis();

  if (ahora - ultimoEnvio >= intervaloEnvio) {

    ultimoEnvio = ahora;

    // Datos simulados

    float tempSimulada =
        24.0 + (random(0, 100) / 10.0);

    float humSimulada =
        55.0 + (random(0, 200) / 10.0);

    // Creación del documento JSON

    StaticJsonDocument<200> doc;

    doc["dispositivo"] = CLIENT_ID;

    doc["temperatura"] =
        serialized(String(tempSimulada, 2));

    doc["humedad"] =
        serialized(String(humSimulada, 2));

    char jsonBuffer[256];

    serializeJson(doc, jsonBuffer);

    // Publicación MQTT

    Serial.print("Publicando en ");
    Serial.print(TOPIC_PUB);
    Serial.print(": ");

    Serial.println(jsonBuffer);

    client.publish(TOPIC_PUB, jsonBuffer);
  }
}
```

---

## 14. Resultados

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

---

## 15. Conclusiones

La actividad permitió comprobar de manera práctica el funcionamiento de la comunicación MQTT utilizando un ESP32 Dev Kit 1.

La modificación de los tópicos permitió identificar la comunicación correspondiente al **Equipo 02**, separándola de los demás equipos participantes.

También se comprobó que el ESP32 Dev Kit 1 puede trabajar de manera bidireccional mediante MQTT, publicando información hacia el broker y recibiendo comandos para controlar su LED integrado.

Finalmente, el uso de Node-RED permitió integrar la información recibida en un dashboard y realizar el control remoto del LED, demostrando una aplicación básica del Internet de las Cosas utilizando **ESP32 Dev Kit 1, MQTT y Node-RED**.

---


