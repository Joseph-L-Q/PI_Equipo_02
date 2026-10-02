# Taller 5 — Internet de las Cosas (IoT)

## Actividades 1 al 5

**Curso:** Proyectos de Ingeniería — Taller de Internet de las Cosas (IoT)

**Integrante:** Joseph Lombardi

**Hardware utilizado:** ESP32 Dev Kit, kit de sensores, protoboard, cables jumper y multímetro.

**Software:** Arduino IDE.

**Plataforma IoT utilizada:** ThingSpeak.

---

## 1. Introducción

En este taller se trabajó con diferentes conceptos básicos de Internet de las Cosas utilizando un ESP32.

El objetivo principal fue aprender cómo obtener información desde sensores, procesarla con el ESP32, conectarnos a una red Wi-Fi y posteriormente enviar los datos hacia una plataforma IoT.

Durante las actividades también se realizó el proceso inverso, es decir, enviar una orden desde una plataforma hacia el ESP32 para controlar un dispositivo.

De manera general, se trabajó con el siguiente flujo:

Sensor → ESP32 → Wi-Fi → Plataforma IoT

Y para el control:

Plataforma IoT → ESP32 → Actuador

---

## 2. Objetivos

### Objetivo general

Implementar diferentes funciones de IoT utilizando un ESP32, desde la lectura de sensores hasta el envío de información y control de dispositivos mediante una plataforma web.

### Objetivos específicos

- Realizar la lectura de un potenciómetro mediante el ADC del ESP32.
- Obtener un promedio de varias lecturas para estabilizar los valores.
- Convertir los valores obtenidos por el ADC a voltaje.
- Conectar el ESP32 a una red Wi-Fi.
- Obtener la dirección IP asignada al ESP32.
- Enviar información desde el ESP32 hacia ThingSpeak.
- Visualizar los datos obtenidos mediante gráficos.
- Leer información de un sensor y enviarla hacia una plataforma IoT.
- Controlar un LED mediante comandos enviados desde una plataforma web.

---

## 3. Materiales utilizados

| Material | Cantidad | Uso |
|---|---:|---|
| ESP32 Dev Kit | 1 | Microcontrolador principal |
| Kit de sensores | 1 | Sensores utilizados en las actividades |
| Potenciómetro | 1 | Generar una señal analógica |
| Protoboard | 1 | Realizar las conexiones |
| Cables jumper | Varios | Conectar los componentes |
| Multímetro | 1 | Comprobar valores de voltaje |
| LED | 1 | Actuador de salida |
| Celular | 1 | Compartir conexión Wi-Fi |
| Cable USB | 1 | Alimentar y programar el ESP32 |

---

# Actividad 01 — Lectura de un potenciómetro

## Enunciado

Mejorar la lectura del potenciómetro utilizando un promedio de datos y convertir el valor obtenido por el ADC a voltaje.

## Conexiones

El potenciómetro se conectó de la siguiente manera:

| Potenciómetro | ESP32 |
|---|---|
| GND | GND |
| VCC | 3.3 V |
| Señal | GPIO34 |

La señal del potenciómetro se conectó al GPIO34 del ESP32 para realizar las lecturas analógicas.

![Figura 1](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014438.png?raw=true)

*Figura 1. Conexión del potenciómetro al ESP32.*

## Código

```cpp
const int potPin = 34;
const int NUM_MUESTRAS = 20;
const float VREF = 3.3;
const int ADC_MAX = 4095;

void setup() {
  Serial.begin(115200);
}

void loop() {

  long suma = 0;

  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma += analogRead(potPin);
    delay(2);
  }

  float promedio = suma / (float)NUM_MUESTRAS;

  float voltaje = promedio * VREF / ADC_MAX;

  Serial.print("ADC promedio: ");
  Serial.print(promedio);

  Serial.print(" | Voltaje: ");
  Serial.print(voltaje, 2);
  Serial.println(" V");

  delay(500);
}
```

## Explicación

El ADC del ESP32 permite convertir una señal analógica en un valor digital.

En este caso, el ESP32 entrega valores aproximadamente entre 0 y 4095.

Para evitar que la lectura varíe demasiado, se realizaron 20 lecturas y posteriormente se calculó el promedio.

Luego el resultado se convirtió a voltaje utilizando la siguiente fórmula:

```text
Voltaje = ADC × 3.3 / 4095
```

De esta manera se puede observar directamente un valor de voltaje en lugar de solamente el valor del ADC.

## Resultados

![Figura 2](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014445.png?raw=true)

*Figura 2. Lectura obtenida con el potenciómetro.*

### Interpretación

Al mover el potenciómetro se observó que el valor leído por el ESP32 también cambiaba.

Cuando el potenciómetro se encontraba cerca de su valor mínimo, el voltaje obtenido se aproximaba a 0 V.

Al moverlo hacia su valor máximo, el voltaje aumentaba hasta aproximadamente 3.3 V.

También se observó que utilizando varias muestras y obteniendo su promedio, la lectura se mantenía más estable.

---

# Actividad 02 — Conexión Wi-Fi

## Enunciado

Crear una red Wi-Fi utilizando un celular como hotspot y conectar el ESP32 a esta red.

Además, se debía mostrar mediante el Monitor Serial la dirección IP asignada al dispositivo.

## Código

```cpp
#include <WiFi.h>

const char* ssid = "NOMBRE_WIFI";
const char* password = "CONTRASEÑA_WIFI";

void setup() {

  Serial.begin(115200);

  WiFi.begin(ssid, password);

  Serial.print("Conectando al WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado");

  Serial.print("Direccion IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {

}
```

## Explicación

Para realizar la conexión se utilizó la librería:

```cpp
#include <WiFi.h>
```

Luego se colocó el nombre de la red y la contraseña.

El ESP32 intenta conectarse mediante:

```cpp
WiFi.begin(ssid, password);
```

Mientras la conexión no se complete, el programa permanece esperando.

Cuando finalmente se conecta, el Monitor Serial muestra la dirección IP asignada utilizando:

```cpp
WiFi.localIP();
```

## Resultados

![Figura 3](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014544.png?raw=true)

*Figura 3. ESP32 conectado a la red Wi-Fi y dirección IP obtenida.*

### Interpretación

El ESP32 logró conectarse correctamente a la red compartida desde el celular.

Una vez establecida la conexión, se mostró la dirección IP asignada automáticamente al dispositivo.

Esto confirmó que el ESP32 ya estaba conectado a la red y podía utilizar Internet para las siguientes actividades.

---

# Actividad 03 — Envío de datos a ThingSpeak

## Enunciado

Enviar hacia una plataforma IoT los valores obtenidos mediante el potenciómetro conectado al ESP32.

Para esta actividad se utilizó ThingSpeak.

## Configuración

Se creó un canal en ThingSpeak donde se almacenarían los datos enviados por el ESP32.

Se configuró un campo para guardar los valores obtenidos mediante el potenciómetro.

![Figura 4](PEGA_AQUI_EL_LINK_DE_LA_CONFIGURACION_DE_THINGSPEAK)

*Figura 4. Canal configurado en ThingSpeak.*

## Código

```cpp
#include <WiFi.h>
#include "ThingSpeak.h"

const char* ssid = "NOMBRE_WIFI";
const char* password = "CONTRASEÑA_WIFI";

unsigned long channelID = TU_CHANNEL_ID;
const char* writeAPIKey = "TU_WRITE_API_KEY";

const int potPin = 34;

WiFiClient client;

void setup() {

  Serial.begin(115200);

  pinMode(potPin, INPUT);

  WiFi.begin(ssid, password);

  Serial.print("Conectando al WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.println("WiFi conectado");

  ThingSpeak.begin(client);
}

void loop() {

  int valorADC = analogRead(potPin);

  float voltaje = valorADC * 3.3 / 4095.0;

  Serial.print("ADC: ");
  Serial.print(valorADC);

  Serial.print(" | Voltaje: ");
  Serial.println(voltaje);

  ThingSpeak.setField(1, voltaje);

  int respuesta = ThingSpeak.writeFields(channelID, writeAPIKey);

  if (respuesta == 200) {
    Serial.println("Dato enviado correctamente");
  } else {
    Serial.print("Error: ");
    Serial.println(respuesta);
  }

  delay(20000);
}
```

## Explicación

Primero el ESP32 se conecta a la red Wi-Fi.

Luego se realiza la lectura del potenciómetro y se convierte el valor obtenido a voltaje.

Después, utilizando la librería de ThingSpeak, el dato es enviado al Field configurado.

```cpp
ThingSpeak.setField(1, voltaje);
```

Finalmente se utiliza:

```cpp
ThingSpeak.writeFields(channelID, writeAPIKey);
```

para enviar la información hacia el canal.

## Resultados

![Figura 5](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014701.png?raw=true)

*Figura 5. Lectura del potenciómetro y envío de datos hacia ThingSpeak.*

![Figura 6](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014711.png?raw=true)

*Figura 6. Variación de los datos recibidos en ThingSpeak.*

### Interpretación

Al variar el potenciómetro, el valor leído por el ESP32 también cambiaba.

Los datos fueron enviados correctamente hacia ThingSpeak y se pudo observar su variación mediante el gráfico de la plataforma.

Con esta actividad se logró realizar el siguiente proceso:

Potenciómetro → ESP32 → Wi-Fi → ThingSpeak

---

# Actividad 04 — Lectura de un sensor y envío a una plataforma IoT

## Enunciado

Realizar la lectura en tiempo real de uno de los sensores disponibles en el kit y enviar sus valores hacia una plataforma IoT.

## Funcionamiento

El sensor utilizado se conecta al ESP32 y este realiza las lecturas de manera periódica.

Posteriormente, la información obtenida es enviada mediante la conexión Wi-Fi hacia la plataforma utilizada.

De esta manera, los datos pueden visualizarse de forma remota.

![Figura 7](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014729.png?raw=true)

*Figura 7. Conexión del sensor utilizado en la Actividad 04.*

## Código

```cpp
// PEGA AQUÍ TU CÓDIGO FINAL DE LA ACTIVIDAD 04
```

## Resultados

![Figura 8](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014751.png?raw=true)

*Figura 8. Lecturas obtenidas por el sensor.*

![Figura 9](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014812.png?raw=true)

*Figura 9. Datos enviados y visualizados en la plataforma IoT.*

### Interpretación

Los valores entregados por el sensor fueron leídos correctamente por el ESP32.

Luego estos datos fueron enviados mediante Internet hacia la plataforma utilizada.

Al observar el gráfico se pudo comprobar que los valores variaban dependiendo de las condiciones detectadas por el sensor.

---

# Actividad 05 — Control de un LED desde una plataforma web

## Enunciado

Conectar un LED al ESP32 y controlar su encendido y apagado desde una plataforma web.

## Funcionamiento

En esta actividad el ESP32 no solamente envía información, sino que también recibe órdenes.

El funcionamiento general fue:

Plataforma web → ESP32 → LED

Cuando se recibe una orden de encendido, el ESP32 coloca el pin del LED en estado HIGH.

Cuando se recibe la orden de apagado, coloca el pin en estado LOW.

## Código

```cpp
// PEGA AQUÍ TU CÓDIGO FINAL DE LA ACTIVIDAD 05
```

## Resultados

![Figura 10](https://github.com/Joseph-L-Q/PI_Equipo_02/blob/3f62288409db33208c72f3af6be81879bd19d7eb/Recursos/Im%C3%A1genes/Captura%20de%20pantalla%202026-10-02%20014907.png?raw=true)

*Figura 10. LED encendido luego de recibir la orden.*

### Interpretación

Al enviar una orden desde la plataforma, el ESP32 recibió el comando y cambió el estado del LED.

Cuando se envió la orden de encendido, el LED se activó.

Cuando se envió la orden de apagado, el LED volvió a su estado inicial.

Esta actividad permitió comprobar que mediante IoT también es posible controlar dispositivos de forma remota.

---

# Conclusiones

- En la Actividad 01 se logró realizar la lectura del potenciómetro utilizando el ADC del ESP32 y convertir los valores obtenidos a voltaje.

- El uso de varias muestras permitió obtener una lectura más estable.

- En la Actividad 02 se logró conectar correctamente el ESP32 a una red Wi-Fi y obtener su dirección IP.

- En la Actividad 03 se enviaron correctamente los datos obtenidos desde el ESP32 hacia ThingSpeak.

- En la Actividad 04 se comprobó que es posible leer un sensor y visualizar sus valores remotamente mediante una plataforma IoT.

- En la Actividad 05 se realizó el proceso inverso, enviando un comando desde una plataforma hacia el ESP32 para controlar un LED.

- En general, las actividades permitieron comprender cómo se realiza la adquisición de datos, comunicación y control dentro de un sistema básico de Internet de las Cosas.

---

# Referencias

[1] Espressif Systems. ESP32 Series Datasheet.  
https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf

[2] Espressif Systems. ESP32 Documentation.  
https://docs.espressif.com/

[3] MathWorks. ThingSpeak Documentation.  
https://www.mathworks.com/help/thingspeak/
