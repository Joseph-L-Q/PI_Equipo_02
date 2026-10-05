// Actividad 03 (ThingSpeak): potenciómetro en tiempo real.
// Potenciómetro: GND -> GND, VCC -> 3V3, SIG -> GPIO34.
// ThingSpeak: canal con Field 1 = Voltaje. La cuenta gratuita acepta un dato cada 15 s como mínimo.

#include <WiFi.h>
#include <HTTPClient.h>

const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";
const char* TS_API_KEY = "TU_API_KEY";               // Write API Key del canal
const char* TS_URL = "http://api.thingspeak.com/update";

const int potPin = 34;
const int NUM_MUESTRAS = 32;
const float VREF = 3.3;
const int ADC_MAX = 4095;
const unsigned long INTERVALO_MS = 20000;            // 20 s, por encima del mínimo de 15 s
unsigned long ultimoEnvio = 0;

float leerVoltaje() {
  long suma = 0;
  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma += analogRead(potPin);
    delay(2);
  }
  return (suma / (float)NUM_MUESTRAS) * VREF / ADC_MAX;
}

void conectarWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Conectando a Wi-Fi");
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
  analogSetPinAttenuation(potPin, ADC_11db);
  conectarWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();

  // Lectura local cada 1 s para ver la variación; envío a la nube cada INTERVALO_MS
  float v = leerVoltaje();
  Serial.print("Voltaje: ");
  Serial.print(v, 2);
  Serial.println(" V");

  if (millis() - ultimoEnvio >= INTERVALO_MS) {
    ultimoEnvio = millis();
    HTTPClient http;
    String url = String(TS_URL) + "?api_key=" + TS_API_KEY + "&field1=" + String(v, 2);
    http.begin(url);
    int codigo = http.GET();                          // ThingSpeak responde con el número de entrada (0 = rechazado)
    String respuesta = http.getString();
    Serial.print("ThingSpeak -> HTTP ");
    Serial.print(codigo);
    Serial.print(", entrada: ");
    Serial.println(respuesta);
    http.end();
  }
  delay(1000);
}
