// Actividad 03 (Ubidots): potenciómetro en tiempo real por MQTT.
// Potenciómetro: GND -> GND, VCC -> 3V3, SIG -> GPIO34.
// Ubidots: el TOKEN de la cuenta se usa como usuario MQTT (la contraseña va vacía).
// Se publica en /v1.6/devices/<DEVICE_LABEL> un JSON {"voltaje": valor}.
// Biblioteca: PubSubClient (Nick O'Leary).

#include <WiFi.h>
#include <PubSubClient.h>

const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";

const char* MQTT_SERVER = "industrial.api.ubidots.com";
const int MQTT_PORT = 1883;
const char* UBIDOTS_TOKEN = "TU_API_KEY";            // token de Ubidots
const char* DEVICE_LABEL = "esp32-equipo02";         // etiqueta del dispositivo en Ubidots
const char* CLIENT_ID = "esp32-palacios-act03";      // debe ser único por conexión

const int potPin = 34;
const int NUM_MUESTRAS = 32;
const float VREF = 3.3;
const int ADC_MAX = 4095;
const unsigned long INTERVALO_MS = 2000;
unsigned long ultimoEnvio = 0;

WiFiClient espClient;
PubSubClient client(espClient);

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
  analogSetPinAttenuation(potPin, ADC_11db);
  conectarWiFi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();
  if (!client.connected()) reconectarMQTT();
  client.loop();

  if (millis() - ultimoEnvio >= INTERVALO_MS) {
    ultimoEnvio = millis();
    float v = leerVoltaje();
    char topic[64];
    snprintf(topic, sizeof(topic), "/v1.6/devices/%s", DEVICE_LABEL);
    char payload[48];
    snprintf(payload, sizeof(payload), "{\"voltaje\": %.2f}", v);
    client.publish(topic, payload);
    Serial.print("Publicado en ");
    Serial.print(topic);
    Serial.print(": ");
    Serial.println(payload);
  }
}
