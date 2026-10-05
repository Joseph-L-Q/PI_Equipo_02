// Actividad 05: encender y apagar un LED desde una plataforma web (Ubidots, por MQTT).
// LED: ánodo -> resistencia de 220 ohm -> GPIO4, cátodo -> GND (o se puede usar el LED integrado, GPIO2).
// En Ubidots: variable "led" (por ejemplo con un widget Switch) dentro del dispositivo <DEVICE_LABEL>.
// El ESP32 se suscribe a /v1.6/devices/<DEVICE_LABEL>/led/lv: ahí llega el último valor (1 o 0).
// Biblioteca: PubSubClient.

#include <WiFi.h>
#include <PubSubClient.h>

const char* WIFI_SSID = "TU_RED_WIFI";
const char* WIFI_PASS = "TU_PASSWORD_WIFI";

const char* MQTT_SERVER = "industrial.api.ubidots.com";
const int MQTT_PORT = 1883;
const char* UBIDOTS_TOKEN = "TU_API_KEY";
const char* DEVICE_LABEL = "esp32-equipo02";
const char* VARIABLE_LED = "led";
const char* CLIENT_ID = "esp32-palacios-act05";

const int LED_PIN = 4;

WiFiClient espClient;
PubSubClient client(espClient);
char topicLed[96];

void callback(char* topic, byte* payload, unsigned int length) {
  String mensaje = "";
  for (unsigned int i = 0; i < length; i++) mensaje += (char)payload[i];
  float valor = mensaje.toFloat();                  // Ubidots envía "1.0" o "0.0"

  Serial.print("Mensaje en [");
  Serial.print(topic);
  Serial.print("]: ");
  Serial.println(mensaje);

  if (valor >= 0.5) {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("LED ENCENDIDO");
  } else {
    digitalWrite(LED_PIN, LOW);
    Serial.println("LED APAGADO");
  }
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
      client.subscribe(topicLed);                   // escuchar los cambios del switch
      Serial.print("Suscrito a: ");
      Serial.println(topicLed);
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
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  snprintf(topicLed, sizeof(topicLed), "/v1.6/devices/%s/%s/lv", DEVICE_LABEL, VARIABLE_LED);
  conectarWiFi();
  client.setServer(MQTT_SERVER, MQTT_PORT);
  client.setCallback(callback);
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) conectarWiFi();
  if (!client.connected()) reconectarMQTT();
  client.loop();                                    // procesa los mensajes entrantes
}
