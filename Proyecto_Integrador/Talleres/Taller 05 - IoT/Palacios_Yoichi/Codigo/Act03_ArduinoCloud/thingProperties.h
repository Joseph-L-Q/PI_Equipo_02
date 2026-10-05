// Archivo normalmente autogenerado por Arduino Cloud. Credenciales reemplazadas por texto genérico.
#include <ArduinoIoTCloud.h>
#include <Arduino_ConnectionHandler.h>

const char DEVICE_LOGIN_NAME[] = "TU_DEVICE_ID";       // ID del dispositivo en Arduino Cloud
const char SSID[]              = "TU_RED_WIFI";
const char PASS[]              = "TU_PASSWORD_WIFI";
const char DEVICE_KEY[]        = "TU_API_KEY";         // Secret Key del dispositivo

float voltaje;                                         // variable de la Thing (solo lectura)

void initProperties() {
  ArduinoCloud.setBoardId(DEVICE_LOGIN_NAME);
  ArduinoCloud.setSecretDeviceKey(DEVICE_KEY);
  ArduinoCloud.addProperty(voltaje, READ, 1 * SECONDS, NULL);   // actualiza cada 1 s o al cambiar
}

WiFiConnectionHandler ArduinoIoTPreferredConnection(SSID, PASS);
