// Actividad 02: conectar el ESP32 al hotspot del celular y mostrar la IP en el monitor serial.
// El ESP32 solo trabaja en 2.4 GHz: activar "banda compatible" / 2.4 GHz en el hotspot del celular.

#include <WiFi.h>

const char* WIFI_SSID = "TU_RED_WIFI";          // nombre del hotspot del celular
const char* WIFI_PASS = "TU_PASSWORD_WIFI";     // clave del hotspot

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.print("Conectando a ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);                  // modo estación (cliente)
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  int intentos = 0;
  while (WiFi.status() != WL_CONNECTED && intentos < 40) {   // hasta 20 s
    delay(500);
    Serial.print(".");
    intentos++;
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi conectado");
    Serial.print("Direccion IP asignada: ");
    Serial.println(WiFi.localIP());     // IP entregada por el DHCP del hotspot
    Serial.print("Intensidad de senal (RSSI): ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println("No se pudo conectar. Revisar SSID, clave y banda 2.4 GHz.");
  }
}

void loop() {
  // Si se pierde la conexión, se intenta reconectar
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Conexion perdida, reconectando...");
    WiFi.disconnect();
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    delay(5000);
  }
  delay(1000);
}
