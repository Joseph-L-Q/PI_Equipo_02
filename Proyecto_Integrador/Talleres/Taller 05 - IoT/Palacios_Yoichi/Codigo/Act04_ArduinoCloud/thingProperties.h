// Archivo normalmente autogenerado por Arduino Cloud. Credenciales reemplazadas por texto genérico.
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

const char DEVICE_LOGIN_NAME[] = "TU_DEVICE_ID";
const char SSID[]              = "TU_RED_WIFI";
const char PASS[]              = "TU_PASSWORD_WIFI";
const char DEVICE_KEY[]        = "TU_API_KEY";

float temperatura;                                     // variable de la Thing (solo lectura)

void initProperties() {
  ArduinoCloud.setBoardId(DEVICE_LOGIN_NAME);
  ArduinoCloud.setSecretDeviceKey(DEVICE_KEY);
  ArduinoCloud.addProperty(temperatura, READ, 1 * SECONDS, NULL);
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);
