# Taller IoT
---

## Introducción

El presente taller tiene como finalidad desarrollar y poner en práctica conceptos fundamentales del Internet de las Cosas (IoT) mediante el uso de una tarjeta de desarrollo **ESP32 Dev Kit 1**, diferentes componentes y plataformas de comunicación.

A lo largo de las actividades se implementan procesos de adquisición de datos, comunicación inalámbrica mediante WiFi, envío de información hacia la nube y control remoto de dispositivos utilizando la plataforma **ThingSpeak**.

Las actividades desarrolladas comprenden la lectura de un potenciómetro, la conexión del ESP32 Dev Kit 1 a una red WiFi, el envío de datos hacia ThingSpeak, la medición de temperatura mediante un sensor LM35 y el control remoto del LED integrado de la tarjeta.

## Actividades desarrolladas

- **Actividad 01:** Lectura de un potenciómetro con ESP32.
- **Actividad 02:** Conexión WiFi del ESP32 mediante Hotspot.
- **Actividad 03:** Envío de datos del potenciómetro a la nube mediante ThingSpeak.
- **Actividad 04:** Lectura de temperatura mediante sensor LM35 y envío de datos a ThingSpeak.
- **Actividad 05:** Control remoto del LED integrado del ESP32 mediante ThingSpeak.

---

# Actividad 01: Lectura de un potenciómetro con ESP32 Dev Kit 1

## 1. Objetivo

Realizar la lectura de una señal analógica mediante un potenciómetro conectado a la tarjeta de desarrollo ESP32 Dev Kit 1, aplicando un método de promediado de datos para mejorar la estabilidad de la medición y convirtiendo los valores obtenidos por el ADC en valores de voltaje.

---

## 2. Descripción de la actividad

En esta actividad se realizó la lectura de un potenciómetro utilizando la tarjeta de desarrollo ESP32 Dev Kit 1.

El objetivo principal fue mejorar el código básico de lectura analógica mediante la implementación de un promedio de múltiples muestras, permitiendo obtener valores más estables y reducir pequeñas variaciones producidas durante la adquisición de datos.

Además, los valores obtenidos por el convertidor analógico-digital (ADC) de la tarjeta fueron transformados a valores de voltaje utilizando como referencia una tensión de 3.3 V.

La tarjeta ESP32 Dev Kit 1 utiliza un ADC con resolución de 12 bits, por lo que las lecturas obtenidas se encuentran dentro del rango:

```
0 - 4095
```

Donde:

- `0` representa aproximadamente `0 V`.
- `4095` representa aproximadamente `3.3 V`.

---

# 3. Materiales utilizados

Para el desarrollo de esta actividad se utilizaron los siguientes componentes:

- ESP32 Dev Kit 1.
- Potenciómetro.
- Protoboard.
- Cables jumper.
- Cable USB.
- Computadora con Arduino IDE.

---

# 4. Implementación del circuito

El potenciómetro fue conectado a la tarjeta ESP32 Dev Kit 1 utilizando una entrada analógica. La señal variable generada por el potenciómetro fue enviada al pin GPIO34, el cual permite realizar lecturas mediante el ADC del microcontrolador.

| Potenciómetro | ESP32 Dev Kit 1 |
|---------------|-----------------|
| VCC | 3.3V |
| GND | GND |
| Salida variable | GPIO34 |

---

## Evidencia del montaje del circuito


<img width="1198" height="1600" alt="image" src="https://github.com/user-attachments/assets/4d56c4d5-37cf-4390-808c-a948b9a9d937" />


**Figura 1. Montaje del circuito utilizando la tarjeta ESP32 Dev Kit 1 y un potenciómetro para la adquisición de datos analógicos.**

---

# 5. Desarrollo del programa

El programa desarrollado realiza las siguientes etapas:

1. Configuración del puerto serial para visualizar los resultados.
2. Configuración del ADC con una resolución de 12 bits.
3. Lectura de 32 muestras consecutivas del potenciómetro.
4. Cálculo del promedio de las lecturas obtenidas.
5. Conversión del valor promedio ADC a voltaje.
6. Visualización del resultado en el monitor serial.

---

# 6. Conversión ADC a voltaje

Para transformar la lectura digital del ADC a un valor de voltaje se utilizó la siguiente ecuación:

```
Voltaje = (ADC promedio × 3.3) / 4095
```

Donde:

- **ADC promedio:** valor obtenido después del promedio de 32 lecturas.
- **3.3 V:** voltaje de referencia utilizado.
- **4095:** valor máximo del ADC con resolución de 12 bits.

---

# 7. Código implementado

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


  // Promediado de muestras

  long suma = 0;


  for (int i = 0; i < NUM_MUESTRAS; i++) {

    suma += analogRead(potPin);

    delay(2);

  }


  float promedio = suma / (float)NUM_MUESTRAS;



  // Conversión ADC a voltaje

  float voltaje = promedio * VREF / ADC_MAX;



  // Mostrar resultados

  Serial.print("ADC promedio: ");

  Serial.print(promedio, 1);


  Serial.print("  |  Voltaje: ");

  Serial.print(voltaje, 2);


  Serial.println(" V");


  delay(500);

}
```

---

# 8. Pruebas y resultados obtenidos

Para comprobar el correcto funcionamiento del sistema se realizaron pruebas modificando la posición del potenciómetro.

Se evaluaron dos condiciones:

- Posición mínima del potenciómetro.
- Posición máxima del potenciómetro.

---

# 8.1 Lectura mínima del potenciómetro

Al colocar el potenciómetro en su posición mínima, la tarjeta ESP32 Dev Kit 1 registró el valor más bajo posible de lectura.

Resultados obtenidos:

```
ADC promedio: 0.0

Voltaje: 0.00 V
```

Esto indica que la señal analógica recibida por la tarjeta se encuentra cercana a 0 voltios.

---

<img width="1600" height="891" alt="image" src="https://github.com/user-attachments/assets/5faa299b-0959-4864-9c46-912e571ed93f" />


**Figura 2. Lectura mínima obtenida del potenciómetro mediante el monitor serial del Arduino IDE.**

---

# 8.2 Lectura máxima del potenciómetro

Posteriormente, se giró el potenciómetro hasta alcanzar su valor máximo.

Resultados obtenidos:

```
ADC promedio: 4095.0

Voltaje: 3.30 V
```

Este valor corresponde al límite superior de la resolución ADC de 12 bits utilizada en la tarjeta ESP32 Dev Kit 1.

---
<img width="1600" height="892" alt="image" src="https://github.com/user-attachments/assets/ad35e456-1b76-49c1-9950-69fe70efbfe1" />


**Figura 3. Lectura máxima obtenida del potenciómetro mediante el monitor serial del Arduino IDE.**

---

# 9. Análisis de resultados

Los resultados obtenidos permitieron verificar la relación existente entre la posición del potenciómetro, el valor digital entregado por el ADC y el voltaje calculado.

Se comprobó que:

| Posición del potenciómetro | ADC promedio | Voltaje obtenido |
|----------------------------|--------------|------------------|
| Mínima | 0.0 | 0.00 V |
| Máxima | 4095.0 | 3.30 V |

El uso del promedio de 32 muestras permitió obtener lecturas más estables, reduciendo variaciones durante la adquisición de datos.

---

# 10. Conclusión

En esta actividad se logró implementar correctamente la lectura analógica de un potenciómetro mediante la tarjeta ESP32 Dev Kit 1.

La aplicación del promediado de muestras permitió mejorar la estabilidad de los datos obtenidos, mientras que la conversión ADC a voltaje facilitó la interpretación de la señal generada por el potenciómetro.

Esta práctica permitió comprender el proceso básico de adquisición de datos utilizado en sistemas IoT, donde la información capturada por sensores puede ser procesada posteriormente para aplicaciones de monitoreo y automatización.

---
# Actividad 02: Conexión WiFi del ESP32 Dev Kit 1 mediante Hotspot


## 1. Objetivo

Configurar la tarjeta de desarrollo ESP32 Dev Kit 1 para conectarse a una red WiFi creada mediante un Smartphone como punto de acceso (Hotspot), verificando la conexión mediante la dirección IP asignada y comprobando la comunicación dentro de la red local.

---

# 2. Descripción de la actividad

En esta actividad se realizó la configuración de comunicación inalámbrica de la tarjeta ESP32 Dev Kit 1 mediante una red WiFi generada desde un Smartphone.

Primero, la tarjeta ESP32 Dev Kit 1 fue programada para realizar un escaneo de las redes WiFi disponibles en el entorno, mostrando información como el nombre de la red (SSID) y la intensidad de señal recibida (RSSI).

Posteriormente, se configuraron las credenciales del Hotspot del Smartphone para establecer la conexión con la tarjeta. Una vez conectada, el sistema mostró en el monitor serial la dirección IP asignada y la intensidad de señal de la conexión.

Finalmente, se realizó una prueba de comunicación mediante el comando `ping` desde la computadora hacia la dirección IP asignada a la tarjeta ESP32 Dev Kit 1, verificando que ambos dispositivos pertenecían a la misma red inalámbrica y podían comunicarse correctamente.

---

# 3. Materiales utilizados

Para el desarrollo de esta actividad se utilizaron los siguientes componentes:

- ESP32 Dev Kit 1.
- Smartphone utilizado como punto de acceso WiFi.
- Computadora.
- Cable USB.
- Arduino IDE.

---

# 4. Configuración de la red WiFi

Para realizar la conexión se utilizó un Smartphone como Hotspot con los siguientes parámetros:

| Parámetro | Valor |
|-----------|-------|
| Nombre de red (SSID) | Redmi Note 14 Pro 5G |
| Dispositivo conectado | ESP32 Dev Kit 1 |
| Tipo de conexión | WiFi 2.4 GHz |

---

# 5. Funcionamiento del programa

El programa desarrollado permite realizar las siguientes acciones:

1. Inicializar la comunicación serial de la tarjeta ESP32 Dev Kit 1.
2. Configurar el módulo WiFi en modo estación (`WIFI_STA`).
3. Escanear las redes inalámbricas disponibles.
4. Mostrar los nombres de las redes encontradas y su intensidad de señal.
5. Conectarse al Hotspot configurado mediante SSID y contraseña.
6. Obtener la dirección IP asignada por la red.
7. Mostrar la intensidad de señal RSSI.
8. Mantener la conexión activa y realizar reconexión en caso de pérdida.

---

# 6. Código implementado

```cpp
#include <WiFi.h>

const char* ssid     = "Redmi Note 14 Pro 5G";
const char* password = "11111111";


void setup() {

  Serial.begin(115200);
  delay(1000);


  WiFi.mode(WIFI_STA);

  WiFi.disconnect();

  delay(100);



  // Escaneo de redes

  Serial.println("Escaneando redes...");

  int n = WiFi.scanNetworks();


  Serial.print(n);

  Serial.println(" redes encontradas:");



  for (int i = 0; i < n; i++) {

    Serial.print(i + 1);

    Serial.print(": ");

    Serial.print(WiFi.SSID(i));

    Serial.print(" (");

    Serial.print(WiFi.RSSI(i));

    Serial.println(" dBm");

  }



  // Conexión al Hotspot

  Serial.print("\nConectando a: ");

  Serial.println(ssid);


  WiFi.begin(ssid, password);



  unsigned long inicio = millis();


  while (WiFi.status() != WL_CONNECTED && millis() - inicio < 15000) {

    delay(500);

    Serial.print(".");

  }



  if (WiFi.status() == WL_CONNECTED) {


    Serial.println("\n¡Conectado!");


    Serial.print("Dirección IP: ");

    Serial.println(WiFi.localIP());


    Serial.print("Señal (RSSI): ");

    Serial.print(WiFi.RSSI());

    Serial.println(" dBm");


  } else {


    Serial.println("\nNo se pudo conectar. Revisar credenciales.");

  }

}



void loop() {


  if (WiFi.status() != WL_CONNECTED) {


    Serial.println("Conexión perdida. Reintentando...");


    WiFi.disconnect();

    WiFi.begin(ssid, password);


    delay(5000);

  }


  delay(1000);

}
```

---

# 7. Resultados obtenidos

## 7.1 Escaneo de redes WiFi y conexión del ESP32 Dev Kit 1

La tarjeta ESP32 Dev Kit 1 logró detectar diferentes redes inalámbricas disponibles en el entorno, mostrando el nombre de cada red (SSID) y su intensidad de señal (RSSI).

Posteriormente, se realizó la conexión al Hotspot creado mediante el Smartphone.

El monitor serial mostró la conexión exitosa con los siguientes datos:

```
Conectando a: Redmi Note 14 Pro 5G

¡Conectado!

Dirección IP: 10.199.46.208

Señal (RSSI): -40 dBm
```

Estos resultados indican que la tarjeta ESP32 Dev Kit 1 obtuvo correctamente una dirección IP dentro de la red WiFi creada.

---

<img width="1600" height="869" alt="image" src="https://github.com/user-attachments/assets/c854385b-ad76-4bf5-99e9-7f9ff397d9f8" />


**Figura 1. Escaneo de redes WiFi y conexión exitosa del ESP32 Dev Kit 1 al Hotspot del Smartphone.**

---

# 7.2 Prueba de comunicación mediante Ping

Para comprobar la comunicación entre la computadora y la tarjeta ESP32 Dev Kit 1 se realizó una prueba utilizando el símbolo del sistema de Windows mediante el comando:

```
ping 10.199.46.208 -t
```

La respuesta obtenida permitió verificar que existe comunicación entre ambos dispositivos dentro de la misma red WiFi.

---


<img width="1477" height="754" alt="image" src="https://github.com/user-attachments/assets/9158f848-7521-467f-87ff-2bd886814caf" />


**Figura 2. Prueba de comunicación entre la computadora y el ESP32 Dev Kit 1 mediante el comando ping.**

---

# 8. Análisis de resultados

Los resultados obtenidos permitieron comprobar el funcionamiento del módulo WiFi de la tarjeta ESP32 Dev Kit 1.

Se verificó que:

- La tarjeta ESP32 Dev Kit 1 pudo realizar un escaneo de redes inalámbricas cercanas.
- La tarjeta logró conectarse correctamente al Hotspot del Smartphone.
- Se obtuvo una dirección IP válida dentro de la red local.
- La intensidad de señal obtenida fue de -40 dBm.
- La prueba de ping confirmó la comunicación entre la computadora y la tarjeta ESP32 Dev Kit 1.

---

# 9. Conclusión

En esta actividad se logró establecer correctamente una conexión inalámbrica entre la tarjeta ESP32 Dev Kit 1 y una red WiFi creada mediante un Smartphone.

La práctica permitió comprender el proceso de conexión de dispositivos IoT a redes inalámbricas, donde la asignación de una dirección IP permite la comunicación entre diferentes dispositivos dentro de una misma red.

Esta conexión será utilizada posteriormente para el envío de información hacia plataformas IoT y aplicaciones basadas en la nube.

---
# Actividad 03: Envío de datos del potenciómetro a la nube mediante ThingSpeak

## 1. Objetivo

Implementar el envío de datos obtenidos desde un potenciómetro conectado a la tarjeta de desarrollo ESP32 Dev Kit 1 hacia una plataforma IoT en la nube, permitiendo visualizar la variación del voltaje en tiempo real mediante ThingSpeak.

---

# 2. Descripción de la actividad

En esta actividad se realizó la comunicación entre la tarjeta ESP32 Dev Kit 1 y una plataforma IoT en la nube para transmitir los valores obtenidos desde un potenciómetro.

La actividad planteaba el uso de diferentes plataformas IoT como Arduino Cloud, ThingSpeak y Ubidots. Sin embargo, debido a la disponibilidad de tiempo, se seleccionó **ThingSpeak** como plataforma de implementación.

La tarjeta ESP32 Dev Kit 1 fue configurada para:

- Leer la señal analógica del potenciómetro mediante el pin GPIO34.
- Realizar un promedio de múltiples muestras para mejorar la estabilidad de la medición.
- Convertir el valor obtenido del ADC en un valor de voltaje.
- Conectarse a una red WiFi.
- Enviar periódicamente los datos hacia un canal creado en ThingSpeak.

Finalmente, los valores enviados fueron almacenados y representados mediante una gráfica dentro de la plataforma ThingSpeak.

---

# 3. Materiales utilizados

Para el desarrollo de esta actividad se utilizaron los siguientes componentes:

- ESP32 Dev Kit 1.
- Potenciómetro.
- Protoboard.
- Cables jumper.
- Smartphone utilizado como Hotspot WiFi.
- Computadora con Arduino IDE.
- Plataforma IoT ThingSpeak.

---

# 4. Configuración de ThingSpeak

Para recibir los datos enviados por la tarjeta ESP32 Dev Kit 1 se creó un canal en la plataforma ThingSpeak.

La configuración utilizada fue:

| Parámetro | Valor |
|-----------|-------|
| Plataforma IoT | ThingSpeak |
| Campo utilizado | Field 1 |
| Variable enviada | Voltaje |
| Unidad de medición | Voltios (V) |
| Método de comunicación | HTTP |
| API Key | Clave configurada en ThingSpeak |

La tarjeta ESP32 Dev Kit 1 envía el valor del voltaje mediante una solicitud HTTP utilizando la API Key configurada en el canal de ThingSpeak.

---

# 5. Funcionamiento del programa

El programa desarrollado realiza las siguientes etapas:

1. Conexión de la tarjeta ESP32 Dev Kit 1 a la red WiFi mediante el Hotspot del Smartphone.
2. Lectura analógica del potenciómetro mediante el pin GPIO34.
3. Promedio de 32 muestras para mejorar la estabilidad del dato.
4. Conversión del valor ADC obtenido a voltaje.
5. Envío del valor de voltaje hacia ThingSpeak cada cierto intervalo de tiempo.
6. Visualización de los datos mediante una gráfica en la plataforma IoT.

---

# 6. Comunicación con ThingSpeak

El envío de datos se realiza mediante una solicitud HTTP utilizando la siguiente estructura:

```text
api.thingspeak.com/update

api_key = Clave de autenticación del canal

field1 = Valor de voltaje enviado
```

El valor del voltaje es enviado al campo 1 del canal ThingSpeak:

```cpp
"&field1=" + String(voltaje, 2);
```

---

# 7. Código implementado

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

// ====== WiFi ======

const char* ssid = "Redmi Note 14 Pro 5G";
const char* password = "11111111";

// ====== ThingSpeak ======

const char* TS_API_KEY = "API_KEY_CONFIGURADA";

// ====== Potenciómetro ======

const int potPin = 34;
const int NUM_MUESTRAS = 32;

const unsigned long INTERVALO = 20000;
unsigned long ultimoEnvio = 0;


float leerVoltaje() {

  long suma = 0;

  for (int i = 0; i < NUM_MUESTRAS; i++) {

    suma += analogRead(potPin);

    delay(2);

  }

  float promedio = suma / (float)NUM_MUESTRAS;

  return promedio * 3.3 / 4095.0;

}


void conectarWiFi() {

  Serial.print("Conectando a WiFi");

  WiFi.mode(WIFI_STA);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);

    Serial.print(".");

  }

  Serial.print("\nConectado. IP: ");

  Serial.println(WiFi.localIP());

}


void enviarThingSpeak(float voltaje) {

  HTTPClient http;

  String url = "http://api.thingspeak.com/update?api_key="
               + String(TS_API_KEY)
               + "&field1="
               + String(voltaje, 2);

  http.begin(url);

  int codigo = http.GET();

  if (codigo == 200) {

    Serial.print("ThingSpeak -> entrada #");

    Serial.println(http.getString());

  } else {

    Serial.print("Error HTTP: ");

    Serial.println(codigo);

  }

  http.end();

}


void setup() {

  Serial.begin(115200);

  analogReadResolution(12);

  analogSetPinAttenuation(potPin, ADC_11db);

  conectarWiFi();

}


void loop() {

  if (WiFi.status() != WL_CONNECTED)

    conectarWiFi();

  float voltaje = leerVoltaje();

  Serial.print("Voltaje: ");

  Serial.print(voltaje, 2);

  Serial.println(" V");


  if (millis() - ultimoEnvio >= INTERVALO || ultimoEnvio == 0) {

    ultimoEnvio = millis();

    enviarThingSpeak(voltaje);

  }

  delay(500);

}
```


# 8. Evidencias de funcionamiento

## 8.1 Ejecución del programa en ESP32 Dev Kit 1

Durante la ejecución del programa se observa la lectura del voltaje obtenido desde el potenciómetro y el envío de datos hacia ThingSpeak.

El monitor serial muestra los valores de voltaje medidos y confirma el envío correcto mediante la respuesta del servidor.

<img width="1600" height="902" alt="image" src="https://github.com/user-attachments/assets/4c681be7-477a-482a-87f9-16c82bc89cb7" />

**Figura 1. Código implementado en Arduino IDE y monitor serial mostrando el envío de valores hacia ThingSpeak.**

---

## 8.2 Visualización de datos en ThingSpeak

Los valores enviados por la tarjeta ESP32 Dev Kit 1 fueron recibidos correctamente por ThingSpeak y representados mediante una gráfica.

La plataforma permitió observar la variación del voltaje del potenciómetro en función del tiempo.

<img width="1600" height="787" alt="image" src="https://github.com/user-attachments/assets/829995dc-3419-4b4c-90b1-7267ab2e6f94" />

**Figura 2. Visualización de los valores de voltaje enviados desde el ESP32 Dev Kit 1 hacia ThingSpeak.**

---

# 9. Resultados obtenidos

Los resultados obtenidos permitieron comprobar la comunicación entre la tarjeta ESP32 Dev Kit 1 y una plataforma IoT en la nube.

Se verificó que:

- La tarjeta ESP32 Dev Kit 1 logró conectarse correctamente a la red WiFi.
- La lectura del potenciómetro fue convertida a valores de voltaje.
- Los datos fueron enviados mediante HTTP hacia ThingSpeak.
- La plataforma recibió los datos y generó una gráfica de comportamiento en tiempo real.

---

# 10. Conclusión

En esta actividad se logró implementar un sistema básico de monitoreo IoT utilizando una tarjeta ESP32 Dev Kit 1 y la plataforma ThingSpeak.

El proyecto permitió integrar tres elementos fundamentales de un sistema IoT:

- Adquisición de datos mediante sensores.
- Comunicación inalámbrica mediante WiFi.
- Almacenamiento y visualización de información en la nube.

La práctica permitió comprender cómo un dispositivo IoT puede capturar información del entorno y enviarla hacia una plataforma remota para su análisis y monitoreo.

---
# Actividad 04: Lectura de temperatura mediante sensor LM35 y envío de datos a ThingSpeak

## 1. Objetivo

Implementar un sistema IoT utilizando la tarjeta de desarrollo ESP32 Dev Kit 1 y un sensor de temperatura LM35, permitiendo adquirir datos de temperatura, procesarlos y enviarlos hacia una plataforma IoT en la nube para su monitoreo.

---

# 2. Descripción de la actividad

En esta actividad se realizó la lectura de temperatura mediante un sensor LM35 conectado a la tarjeta ESP32 Dev Kit 1.

El sensor LM35 genera una señal analógica proporcional a la temperatura medida, entregando una relación de 10 mV por cada grado Celsius. Esta señal fue capturada mediante el convertidor analógico-digital (ADC) del ESP32.

Para mejorar la estabilidad de la medición se implementó un promedio de 64 muestras consecutivas. Posteriormente, los valores obtenidos fueron convertidos a grados Celsius y enviados hacia la plataforma IoT ThingSpeak mediante una conexión WiFi.

En esta actividad, el valor de temperatura fue enviado al **Field 3** del canal de ThingSpeak.

Finalmente, los datos obtenidos fueron visualizados mediante el monitor serial del Arduino IDE y mediante la gráfica correspondiente de ThingSpeak.

---

# 3. Materiales utilizados

Para el desarrollo de esta actividad se utilizaron los siguientes componentes:

- ESP32 Dev Kit 1.
- Sensor de temperatura LM35.
- Protoboard.
- Cables jumper.
- Cable USB.
- Smartphone utilizado como Hotspot WiFi.
- Computadora con Arduino IDE.
- Plataforma IoT ThingSpeak.

---

# 4. Implementación del circuito

Para realizar la medición de temperatura se utilizó un sensor LM35 conectado a la tarjeta ESP32 Dev Kit 1 mediante una entrada analógica.

El sensor entrega una señal proporcional a la temperatura del ambiente, la cual es procesada por el ADC interno de la tarjeta para obtener el valor correspondiente en grados Celsius.

La conexión utilizada fue la siguiente:

| Sensor LM35 | ESP32 Dev Kit 1 |
|-------------|-----------------|
| VCC | 3.3 V |
| GND | GND |
| Salida analógica | GPIO34 |

El sensor LM35 utiliza el pin **GPIO34** para enviar la señal analógica que será procesada por el ESP32.

---
### Montaje físico del circuito

En la siguiente imagen se observa el montaje físico de la tarjeta ESP32 Dev Kit 1, el sensor LM35 y la protoboard utilizados durante la actividad.

<img width="1198" height="1600" alt="image" src="https://github.com/user-attachments/assets/ad49cd53-db80-4015-bd6d-6ca996723a56" />


**Figura 1. Montaje físico de la tarjeta ESP32 Dev Kit 1 y sensor LM35 utilizado para la adquisición de temperatura.**

---
# 5. Configuración de ThingSpeak

Para almacenar y visualizar los datos obtenidos se utilizó la plataforma IoT ThingSpeak.

En el canal utilizado se configuraron diferentes campos para las actividades desarrolladas. Para esta actividad, la temperatura se registró específicamente en el **Field 3**.

| Parámetro | Descripción |
|-----------|-------------|
| Plataforma IoT | ThingSpeak |
| Variable enviada | Temperatura |
| Unidad de medición | °C |
| Campo utilizado | Field 3 |
| Método de comunicación | HTTP |
| Intervalo de envío | 20 segundos |

El código realiza el envío de la temperatura mediante una solicitud HTTP utilizando la API Key configurada en ThingSpeak.

La estructura utilizada para enviar el dato es:

```text
api.thingspeak.com/update

api_key = Clave de autenticación del canal

field3 = Valor de temperatura
```

En el código se observa:

```cpp
"&field3=" + String(temperatura, 1);
```

Esto permite enviar el valor de temperatura al tercer campo del canal de ThingSpeak.

---

# 6. Funcionamiento del programa

El programa desarrollado realiza las siguientes etapas:

1. Configuración de la comunicación serial.
2. Configuración del ADC del ESP32 con una resolución de 12 bits.
3. Configuración de la atenuación del pin GPIO34.
4. Conexión de la tarjeta ESP32 Dev Kit 1 a la red WiFi mediante el Hotspot del Smartphone.
5. Lectura de la señal analógica del sensor LM35.
6. Obtención de 64 muestras consecutivas.
7. Cálculo del promedio de las muestras.
8. Conversión de milivoltios a grados Celsius.
9. Envío de la temperatura hacia el **Field 3** de ThingSpeak.
10. Visualización de los valores mediante el monitor serial.
11. Visualización de los datos mediante la gráfica de ThingSpeak.

---

# 7. Conversión del sensor LM35 a temperatura

El sensor LM35 presenta una relación lineal entre la tensión de salida y la temperatura:

```text
10 mV = 1 °C
```

Por esta razón, la temperatura se obtiene mediante la siguiente conversión:

```text
Temperatura = mV / 10
```

Donde:

- **mV:** voltaje obtenido del sensor LM35 en milivoltios.
- **Temperatura:** valor calculado en grados Celsius.

Para mejorar la estabilidad de la medición se utilizaron **64 muestras**, cuyo promedio posteriormente se convirtió a temperatura.

---

# 8. Código implementado

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

// ====== WiFi ======
const char* ssid     = "Redmi Note 14 Pro 5G";
const char* password = "11111111";

// ====== ThingSpeak ======
const char* TS_API_KEY = "API_KEY_CONFIGURADA";

// ====== Sensor LM35 ======
const int lm35Pin = 34;
const int NUM_MUESTRAS = 64;

const unsigned long INTERVALO = 20000;  // ThingSpeak gratis: mínimo 15 s
unsigned long ultimoEnvio = 0;

float leerTemperatura() {
  long suma_mV = 0;

  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma_mV += analogReadMilliVolts(lm35Pin);
    delay(2);
  }

  float mV = suma_mV / (float)NUM_MUESTRAS;

  return mV / 10.0;   // LM35: 10 mV por °C
}

void conectarWiFi() {
  Serial.print("Conectando a WiFi");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.print("\nConectado. IP: ");
  Serial.println(WiFi.localIP());
}

void enviarThingSpeak(float temperatura) {
  HTTPClient http;

  String url = "http://api.thingspeak.com/update?api_key="
               + String(TS_API_KEY)
               + "&field3="
               + String(temperatura, 1);

  http.begin(url);

  int codigo = http.GET();

  if (codigo == 200) {
    Serial.print("ThingSpeak -> entrada #");
    Serial.println(http.getString());   // Si es 0, el dato NO se guardó
  } else {
    Serial.print("Error HTTP: ");
    Serial.println(codigo);
  }

  http.end();
}

void setup() {
  Serial.begin(115200);

  analogReadResolution(12);
  analogSetPinAttenuation(lm35Pin, ADC_11db);

  conectarWiFi();
}

void loop() {

  if (WiFi.status() != WL_CONNECTED)
    conectarWiFi();

  float temperatura = leerTemperatura();

  Serial.print("Temperatura: ");
  Serial.print(temperatura, 1);
  Serial.println(" °C");

  if (millis() - ultimoEnvio >= INTERVALO || ultimoEnvio == 0) {

    ultimoEnvio = millis();

    enviarThingSpeak(temperatura);
  }

  delay(500);
}
```

---

# 9. Evidencias de funcionamiento

## 9.1 Lectura de temperatura mediante ESP32 Dev Kit 1

Durante la ejecución del programa se utilizó la tarjeta ESP32 Dev Kit 1 junto con el sensor LM35 para realizar la adquisición de temperatura.

El monitor serial permitió visualizar los valores obtenidos durante la ejecución del programa.

Entre los valores observados se encuentran:

```text
Temperatura: 14.2 °C
Temperatura: 22.3 °C
Temperatura: 22.8 °C
Temperatura: 16.4 °C
Temperatura: 17.3 °C
Temperatura: 15.6 °C
Temperatura: 15.4 °C
Temperatura: 15.3 °C
```
<img width="1600" height="942" alt="image" src="https://github.com/user-attachments/assets/0e068000-d2fa-487f-90a9-4054ccd97f80" />

**Figura 1. Código implementado en Arduino IDE y monitor serial mostrando las lecturas de temperatura obtenidas mediante el sensor LM35.**

---

## 9.2 Visualización de la temperatura en ThingSpeak

Los valores obtenidos por el sensor LM35 fueron enviados hacia ThingSpeak mediante una conexión WiFi.

Para esta actividad se utilizó el **Field 3**, correspondiente a la variable **Temperatura**.

En la plataforma se observa la gráfica **Field 3 Chart**, donde se representan los valores registrados durante la prueba.

La gráfica muestra valores aproximados entre **14.2 °C y 14.8 °C** para los registros visualizados en ThingSpeak.

<img width="1600" height="899" alt="image" src="https://github.com/user-attachments/assets/b1ae89f3-e206-449a-82f9-806208a28060" />

**Figura 2. Gráfica del Field 3 de ThingSpeak correspondiente a los valores de temperatura enviados por el ESP32 Dev Kit 1.**

---

# 10. Resultados obtenidos

Los resultados obtenidos permitieron comprobar el funcionamiento del sistema de adquisición y transmisión de datos.

Se verificó que:

- La tarjeta ESP32 Dev Kit 1 logró conectarse correctamente a la red WiFi.
- El sensor LM35 proporcionó valores de temperatura en grados Celsius.
- Se utilizaron 64 muestras para obtener un valor promedio.
- La temperatura fue enviada hacia ThingSpeak mediante una solicitud HTTP.
- El valor de temperatura fue registrado en el **Field 3** del canal.
- ThingSpeak permitió visualizar los datos mediante una gráfica.

Durante la ejecución del programa se observaron diferentes valores de temperatura en el monitor serial, entre ellos:

| Registro | Temperatura |
|----------|-------------|
| 1 | 14.2 °C |
| 2 | 22.3 °C |
| 3 | 22.8 °C |
| 4 | 16.4 °C |
| 5 | 17.3 °C |
| 6 | 15.6 °C |
| 7 | 15.4 °C |
| 8 | 15.3 °C |

La gráfica de ThingSpeak correspondiente al **Field 3** permitió observar la variación de los valores registrados durante la prueba.

---

# 11. Conclusión

En esta actividad se logró implementar un sistema IoT utilizando un sensor de temperatura LM35 conectado a la tarjeta ESP32 Dev Kit 1.

El sistema permitió adquirir información mediante el sensor, procesar las lecturas obtenidas y transmitir los datos hacia ThingSpeak mediante una conexión WiFi.

El uso de 64 muestras permitió obtener un promedio de las lecturas antes de realizar la conversión a grados Celsius. Finalmente, los datos fueron registrados en el **Field 3** de ThingSpeak y representados mediante una gráfica para facilitar su visualización.

Esta práctica permitió integrar la adquisición de datos, el procesamiento de señales, la comunicación inalámbrica y el almacenamiento de información en una plataforma IoT.

---
# Actividad 05: Control remoto del LED integrado del ESP32 Dev Kit 1 mediante ThingSpeak

## 1. Objetivo

Implementar un sistema IoT de control remoto utilizando un ESP32 Dev Kit 1 y la plataforma ThingSpeak, permitiendo controlar el estado del LED integrado de la placa mediante comandos enviados desde la nube.

---

# 2. Descripción de la actividad

En esta actividad se desarrolló un sistema de control remoto basado en Internet de las Cosas (IoT), utilizando el ESP32 Dev Kit 1 como dispositivo conectado a una red WiFi.

A diferencia de las actividades anteriores, donde el ESP32 enviaba información hacia la plataforma ThingSpeak, en esta práctica se implementó una comunicación en sentido contrario, donde el dispositivo consulta información almacenada en la nube y ejecuta una acción física.

Para realizar el control se utilizó el LED azul integrado del ESP32 Dev Kit 1, asociado al pin digital GPIO 2.

El funcionamiento del sistema consiste en almacenar un valor de control en el campo 2 de ThingSpeak:

- Valor **1** → Encender LED integrado.
- Valor **0** → Apagar LED integrado.

El ESP32 consulta periódicamente el último valor almacenado en ThingSpeak mediante una conexión WiFi y modifica automáticamente el estado del LED según el comando recibido.

---

# 3. Materiales utilizados

Para el desarrollo de esta actividad se utilizaron los siguientes elementos:

- ESP32 Dev Kit 1.
- Cable USB.
- Computadora con Arduino IDE.
- Smartphone utilizado como Hotspot WiFi.
- Plataforma IoT ThingSpeak.

---

# 4. Implementación del sistema

Para esta actividad se utilizó el LED azul integrado del ESP32 Dev Kit 1, evitando la necesidad de conectar un LED externo.

El LED integrado de la placa se encuentra asociado al siguiente pin digital:

| Componente | Pin ESP32 Dev Kit 1 |
|-----------|----------------------|
| LED integrado azul | GPIO 2 |

El ESP32 fue programado para consultar el estado almacenado en ThingSpeak y modificar la salida digital del GPIO 2.

El proceso realizado fue:

1. El ESP32 Dev Kit 1 se conecta a una red WiFi.
2. El dispositivo consulta periódicamente ThingSpeak.
3. Obtiene el último valor almacenado en el Field 2.
4. Interpreta el comando recibido.
5. Actualiza el estado del LED integrado.

---

# 5. Configuración de ThingSpeak

Para realizar el control remoto se utilizó un canal de ThingSpeak configurado para almacenar diferentes datos correspondientes a las actividades desarrolladas.

En esta actividad se utilizó específicamente el **Field 2**, correspondiente al estado del LED.

La configuración utilizada fue:

| Parámetro | Descripción |
|-----------|-------------|
| Plataforma IoT | ThingSpeak |
| Campo utilizado | Field 2 |
| Variable | Led |
| Valor 1 | LED encendido |
| Valor 0 | LED apagado |
| Comunicación | HTTP |

El ESP32 Dev Kit 1 realiza consultas periódicas al Field 2 del canal para conocer el estado actual del LED.

---

# 6. Funcionamiento del programa

El programa desarrollado realiza las siguientes etapas:

1. Inicialización del puerto serial.
2. Configuración del LED integrado como salida digital.
3. Conexión del ESP32 Dev Kit 1 a la red WiFi.
4. Consulta del estado del LED en ThingSpeak.
5. Lectura del comando recibido.
6. Comparación del valor obtenido.
7. Cambio del estado del LED según el valor recibido.
8. Visualización del comando ejecutado mediante el monitor serial.

La lógica implementada es:

```text
Si Field 2 = 1 → LED ENCENDIDO

Si Field 2 = 0 → LED APAGADO
```

El ESP32 realiza una consulta cada 5 segundos para comprobar si existe un nuevo comando.

---

# 7. Código implementado

```cpp
#include <WiFi.h>
#include <HTTPClient.h>

// ====== WiFi ======
const char* ssid     = "Redmi Note 14 Pro 5G";
const char* password = "11111111";

// ====== ThingSpeak ======
const char* CHANNEL_ID  = "3515252";
const char* TS_READ_KEY = "READ_API_KEY_CONFIGURADA";

// ====== LED integrado ESP32 Dev Kit 1 ======
const int LED_PIN = 2;

const unsigned long INTERVALO = 5000;

unsigned long ultimaConsulta = 0;
int estadoLed = -1;

void conectarWiFi() {

  Serial.print("Conectando a WiFi");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {

    delay(500);
    Serial.print(".");

  }

  Serial.print("\nConectado. IP: ");
  Serial.println(WiFi.localIP());

}

void consultarLed() {

  HTTPClient http;

  String url = "http://api.thingspeak.com/channels/"
               + String(CHANNEL_ID)
               + "/fields/2/last.txt?api_key="
               + String(TS_READ_KEY);

  http.begin(url);

  int codigo = http.GET();

  if (codigo == 200) {

    String respuesta = http.getString();
    respuesta.trim();

    int nuevo = (respuesta == "1") ? 1 : 0;

    if (nuevo != estadoLed) {

      estadoLed = nuevo;

      digitalWrite(LED_PIN, estadoLed ? HIGH : LOW);

      Serial.print("Comando recibido: ");
      Serial.println(
        estadoLed ? "LED ENCENDIDO" : "LED APAGADO"
      );

    }

  } else {

    Serial.print("Error HTTP: ");
    Serial.println(codigo);

  }

  http.end();

}

void setup() {

  Serial.begin(115200);

  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  conectarWiFi();

}

void loop() {

  if (WiFi.status() != WL_CONNECTED)
    conectarWiFi();

  if (millis() - ultimaConsulta >= INTERVALO ||
      ultimaConsulta == 0) {

    ultimaConsulta = millis();

    consultarLed();

  }

}
```

---

# 8. Evidencias de funcionamiento

## 8.1 Montaje del ESP32 Dev Kit 1

En la siguiente evidencia se observa la tarjeta ESP32 Dev Kit 1 utilizada durante la implementación del sistema de control remoto.

El control se realizó utilizando el LED azul integrado de la placa, asociado al GPIO 2.

<img width="900" height="1600" alt="image" src="https://github.com/user-attachments/assets/82aa54db-cd44-455a-95ad-4847dcdf738c" />

**Figura 1. ESP32 Dev Kit 1 utilizado para el control remoto del LED integrado.**

---

## 8.2 Envío del comando para encender el LED

Para activar el LED integrado se envió el valor:

```text
Field 2 = 1
```

El ESP32 Dev Kit 1 consultó este valor desde ThingSpeak y modificó el estado de la salida digital para encender el LED.

<img width="1600" height="945" alt="image" src="https://github.com/user-attachments/assets/d0120145-16b1-4da3-9dc5-fd089757d4ff" />


**Figura 2. Envío del comando de encendido mediante ThingSpeak.**

---

## 8.3 Envío del comando para apagar el LED

Para desactivar el LED integrado se envió el valor:

```text
Field 2 = 0
```

El ESP32 Dev Kit 1 consultó el valor almacenado en ThingSpeak y cambió el estado de la salida digital para apagar el LED.
apagado: https://api.thingspeak.com/update?api_key=L7ZNJ5Z633EXMQE9&field2=0

<img width="1600" height="923" alt="image" src="https://github.com/user-attachments/assets/6277ee21-4947-455e-86a6-edabe114d14a" />


**Figura 3. Envío del comando de apagado mediante ThingSpeak.**

---

## 8.4 Visualización del estado del LED en ThingSpeak

Los comandos enviados al **Field 2** fueron registrados en ThingSpeak y representados mediante una gráfica.

En la gráfica se observan los cambios entre los valores **0 y 1**, correspondientes a los estados de apagado y encendido del LED integrado.

El **Field 2 Chart** permite visualizar la variación del estado del LED en función del tiempo.

> **Nota:** La captura también muestra el **Field 1 Chart**, correspondiente a otra actividad. Para esta actividad se analiza específicamente el **Field 2 Chart (Led)**.

<img width="1600" height="898" alt="image" src="https://github.com/user-attachments/assets/549b7a80-5d21-457c-b190-4639f1376c3f" />

**Figura 4. Visualización del Field 2 de ThingSpeak, correspondiente a los estados de encendido y apagado del LED integrado.**

---

## 8.5 Confirmación mediante monitor serial

El monitor serial permitió verificar la recepción de los comandos enviados desde ThingSpeak.

Durante la prueba se observaron mensajes correspondientes a los cambios de estado del LED:

```text
Conectado. IP: 10.199.46.208

Comando recibido: LED APAGADO

Comando recibido: LED ENCENDIDO
```

Estos mensajes permitieron comprobar que el ESP32 Dev Kit 1 recibió e interpretó correctamente los valores almacenados en el Field 2.

<img width="1600" height="894" alt="image" src="https://github.com/user-attachments/assets/412c6be8-0ba5-4bcb-b834-9285388a4fd4" />


**Figura 5. Monitor serial mostrando los comandos recibidos y ejecutados por el ESP32 Dev Kit 1.**

---

# 9. Resultados obtenidos

Los resultados obtenidos permitieron comprobar el funcionamiento de un sistema IoT de control remoto.

Se verificó que:

- El ESP32 Dev Kit 1 logró conectarse correctamente a la red WiFi.
- El dispositivo pudo consultar información almacenada en ThingSpeak.
- El Field 2 permitió almacenar los estados de control del LED.
- El valor **1** fue utilizado para indicar el encendido del LED.
- El valor **0** fue utilizado para indicar el apagado del LED.
- Los comandos enviados desde ThingSpeak fueron interpretados correctamente.
- El LED azul integrado del ESP32 Dev Kit 1 respondió a los cambios de estado.
- ThingSpeak permitió visualizar gráficamente los valores registrados en el Field 2.
- El monitor serial permitió comprobar los comandos recibidos por el dispositivo.

La comunicación implementada puede representarse de la siguiente manera:

```text
ThingSpeak
     ↓
   Field 2
     ↓
  WiFi / HTTP
     ↓
ESP32 Dev Kit 1
     ↓
 GPIO 2
     ↓
LED integrado
```

---

# 10. Conclusión

En esta actividad se logró implementar un sistema de control remoto IoT utilizando un ESP32 Dev Kit 1 y la plataforma ThingSpeak.

La práctica permitió comprender la comunicación entre un dispositivo IoT y una plataforma en la nube, donde el ESP32 Dev Kit 1 consulta información almacenada remotamente y ejecuta una acción física de acuerdo con el comando recibido.

El uso del LED azul integrado permitió demostrar el control remoto de un actuador sin utilizar componentes externos. Asimismo, la gráfica del Field 2 y el monitor serial permitieron verificar los cambios de estado durante la ejecución de la actividad.

De esta manera, se integraron la conexión WiFi, las solicitudes HTTP, la plataforma ThingSpeak y el control de una salida digital en un sistema básico de Internet de las Cosas.
