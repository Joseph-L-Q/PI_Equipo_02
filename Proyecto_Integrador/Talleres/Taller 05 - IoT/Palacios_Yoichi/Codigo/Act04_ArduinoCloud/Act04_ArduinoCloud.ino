// Actividad 04 (Arduino Cloud): sensor de temperatura LM35.
// LM35: GND -> GND, VCC -> VIN (5 V), OUT -> GPIO34. Salida: 10 mV por grado Celsius.
// Thing con una variable float "temperatura" (solo lectura) y un widget en el dashboard.

#include "thingProperties.h"

const int lm35Pin = 34;
const int NUM_MUESTRAS = 64;
const float VREF = 3.3;
const int ADC_MAX = 4095;

float leerTemperaturaC() {
  long suma = 0;
  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma += analogRead(lm35Pin);
    delay(2);
  }
  return (suma / (float)NUM_MUESTRAS) * VREF / ADC_MAX * 100.0;   // 10 mV/C
}

void setup() {
  Serial.begin(115200);
  delay(1500);
  analogReadResolution(12);
  analogSetPinAttenuation(lm35Pin, ADC_11db);

  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);
  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();
  temperatura = leerTemperaturaC();
  delay(500);
}
