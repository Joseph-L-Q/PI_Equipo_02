// Actividad 01: lectura de un potenciómetro con promediado y conversión del ADC a voltaje.
// Placa: ESP32 Dev Module. Potenciómetro: GND -> GND, VCC -> 3V3, SIG -> GPIO34.

const int potPin = 34;          // GPIO34 (ADC1, solo entrada)
const int NUM_MUESTRAS = 32;    // lecturas que se promedian
const float VREF = 3.3;         // voltaje de referencia del ESP32 (V)
const int ADC_MAX = 4095;       // resolución de 12 bits

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);                   // ADC de 12 bits: 0 a 4095
  analogSetPinAttenuation(potPin, ADC_11db);  // rango de entrada aprox. 0 a 3.3 V
}

void loop() {
  // 1. Promediado: la media de N lecturas reduce el ruido aleatorio en un factor raiz(N)
  long suma = 0;
  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma += analogRead(potPin);
    delay(2);                                 // pausa corta entre muestras
  }
  float promedio = suma / (float)NUM_MUESTRAS; // (float) evita la división entera

  // 2. Conversión del valor del ADC a voltaje
  float voltaje = promedio * VREF / ADC_MAX;

  Serial.print("ADC promedio: ");
  Serial.print(promedio, 1);
  Serial.print("  |  Voltaje: ");
  Serial.print(voltaje, 2);
  Serial.println(" V");

  delay(500);
}
