// Actividad 04 (ThingSpeak): sensor de temperatura LM35 en tiempo real.
// LM35: GND -> GND, VCC -> VIN (5 V), OUT -> GPIO34. Salida: 10 mV por grado Celsius.
// ThingSpeak: canal con Field 1 = Temperatura (C). Mínimo 15 s entre envíos en la cuenta gratuita.

#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";
const char* TS_API_KEY = "TU_API_KEY";
const char* TS_URL = "http://api.thingspeak.com/update";

const int lm35Pin = 34;
const int NUM_MUESTRAS = 64;
const float VREF = 3.3;
const int ADC_MAX = 4095;
const unsigned long INTERVALO_MS = 20000;
unsigned long ultimoEnvio = 0;

float leerTemperaturaC() {
  long suma = 0;
  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma += analogRead(lm35Pin);
    delay(2);
  }
  float voltaje = (suma / (float)NUM_MUESTRAS) * VREF / ADC_MAX;   // V
  return voltaje * 100.0;                                           // 10 mV/C -> T = V * 100
}

void conectarWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nConectado. IP: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(lm35Pin, ADC_11db);
  conectarWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();

  float t = leerTemperaturaC();
  Serial.print("Temperatura: ");
  Serial.print(t, 1);
  Serial.println(" C");

  if (millis() - ultimoEnvio >= INTERVALO_MS) {
    ultimoEnvio = millis();
    HTTPClient http;
    http.begin(String(TS_URL) + "?api_key=" + TS_API_KEY + "&field1=" + String(t, 1));
    int codigo = http.GET();
    Serial.print("ThingSpeak -> HTTP ");
    Serial.print(codigo);
    Serial.print(", entrada: ");
    Serial.println(http.getString());
    http.end();
  }
  delay(1000);
}
