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


<img width="1600" height="900" alt="image" src="https://github.com/user-attachments/assets/2fb83206-0041-4388-bada-d97784d9564c" />


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
