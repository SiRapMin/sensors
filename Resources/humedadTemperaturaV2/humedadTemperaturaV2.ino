#include "DHT.h"

#define DHTPIN 6     // Pin donde está conectado el sensor

//#define DHTTYPE DHT11   // Descomentar si se usa el DHT 11
#define DHTTYPE DHT22   // Sensor DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}
void loop() {
  delay(1000);
  float h = dht.readHumidity(); //Leemos la Humedad
  float t = dht.readTemperature(); //Leemos la temperatura en grados Celsius
  float f = dht.readTemperature(true); //Leemos la temperatura en grados Fahrenheit
  //--------Enviamos las lecturas por el puerto serial-------------
  /*
  Serial.print("{Humedad: ");
  Serial.print(String(h)+",");
  Serial.print("Temperatura: ");
  Serial.println(String(t)+"}");
  */
  Serial.println(h);
  Serial.println(t);
}
