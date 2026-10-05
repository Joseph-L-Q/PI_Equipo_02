// Actividad 04 (Ubidots): sensor de temperatura LM35 por MQTT.
// LM35: GND -> GND, VCC -> VIN (5 V), OUT -> GPIO34. Salida: 10 mV por grado Celsius.
// Se publica {"temperatura": valor} en /v1.6/devices/<DEVICE_LABEL>. Biblioteca: PubSubClient.

#include <WiFi.h>
#include <PubSubClient.h>

const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";

const char* MQTT_SERVER = "industrial.api.ubidots.com";
const int MQTT_PORT = 1883;
const char* UBIDOTS_TOKEN = "TU_API_KEY";
const char* DEVICE_LABEL = "esp32-equipo02";
const char* CLIENT_ID = "esp32-palacios-act04";

const int lm35Pin = 34;
const int NUM_MUESTRAS = 64;
const float VREF = 3.3;
const int ADC_MAX = 4095;
const unsigned long INTERVALO_MS = 5000;
unsigned long ultimoEnvio = 0;

WiFiClient espClient;
PubSubClient client(espClient);

float leerTemperaturaC() {
  long suma = 0;
  for (int i = 0; i < NUM_MUESTRAS; i++) {
    suma += analogRead(lm35Pin);
    delay(2);
  }
  return (suma / (float)NUM_MUESTRAS) * VREF / ADC_MAX * 100.0;   // 10 mV/C
}

void conectarWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("\nWiFi OK, IP: ");
  Serial.println(WiFi.localIP());
}

void reconectarMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando a Ubidots...");
    if (client.connect(CLIENT_ID, UBIDOTS_TOKEN, "")) {
      Serial.println(" conectado");
    } else {
      Serial.print(" fallo, rc=");
      Serial.print(client.state());
      Serial.println(". Reintento en 5 s");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(lm35Pin, ADC_11db);
  conectarWiFi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();
  if (!client.connected()) reconectarMQTT();
  client.loop();

  if (millis() - ultimoEnvio >= INTERVALO_MS) {
    ultimoEnvio = millis();
    float t = leerTemperaturaC();
    char topic[64];
    snprintf(topic, sizeof(topic), "/v1.6/devices/%s", DEVICE_LABEL);
    char payload[48];
    snprintf(payload, sizeof(payload), "{\"temperatura\": %.1f}", t);
    client.publish(topic, payload);
    Serial.print("Publicado en ");
    Serial.print(topic);
    Serial.print(": ");
    Serial.println(payload);
  }
}
