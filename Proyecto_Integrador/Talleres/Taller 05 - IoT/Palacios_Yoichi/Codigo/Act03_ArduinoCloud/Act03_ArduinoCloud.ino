// Actividad 03 (Arduino Cloud): potenciómetro en tiempo real.
// Se crea en Arduino Cloud una "Thing" con una variable float llamada "voltaje" (solo lectura),
// se asocia el ESP32 y se agrega un widget (gauge o gráfico) en el dashboard.
// Arduino Cloud genera thingProperties.h; aquí se deja una copia sin credenciales.

#include "thingProperties.h"

const int potPin = 34;
const int NUM_MUESTRAS = 32;
const float VREF = 3.3;
const int ADC_MAX = 4095;

float leerVoltaje() {
  long suma = 0;
  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma += analogRead(potPin);
    delay(2);
  }
  return (suma / (float)NUM_MUESTRAS) * VREF / ADC_MAX;
}

void setup() {
  Serial.begin(115200);
  delay(1500);
  analogReadResolution(12);
  analogSetPinAttenuation(potPin, ADC_11db);

  initProperties();                                    // definida en thingProperties.h
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();                               // mantiene la conexión y sincroniza las variables
  voltaje = leerVoltaje();                             // al cambiar, Arduino Cloud la envía sola
  delay(200);
}
