
#include "Adafruit_CCS811.h"
#include "DHT.h"

#define DHTPIN 6     // Pin donde está conectado el sensor
#define DHTTYPE DHT22   // Sensor DHT22

DHT dht(DHTPIN, DHTTYPE);
Adafruit_CCS811 ccs;

void setup() {
  Serial.begin(9600);
  dht.begin();
  if(!ccs.begin()){
    Serial.println("Failed to start sensor! Please check your wiring.");
    while(1);
  }
  // Wait for the sensor to be ready
  while(!ccs.available());
}

void loop() {
  float h = dht.readHumidity(); //Leemos la Humedad
  float t = dht.readTemperature(); //Leemos la temperatura en grados Celsius
  if(ccs.available()){
    if(!ccs.readData()){
      //Serial.print("CO2: ");
      if(ccs.geteCO2() != 0){
        Serial.println(ccs.geteCO2());    //Particulas por millon de dioxido de carbono
        Serial.println(ccs.getTVOC());
        Serial.println(h);
        Serial.println(t);
      }
      //Serial.print("ppm, TVOC: ");
      // (gramos/metrocubico)productos químicos que se convierten 
      //fácilmente en vapores o gases (metano, etano, propano, n-butano, n-pentano, benceno, tolueno, xileno y etileno)
      
    }
    else{
      Serial.println("ERROR!");
      while(1);
    }
  }
  delay(2000);
}
