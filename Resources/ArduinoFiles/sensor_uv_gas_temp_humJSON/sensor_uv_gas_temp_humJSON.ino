
#include "Adafruit_CCS811.h"
#include "DHT.h"

int uv_ain=A0;
int ad_value;

#define DHTPIN 6     // Pin donde está conectado el sensor
#define DHTTYPE DHT22   // Sensor DHT22

DHT dht(DHTPIN, DHTTYPE);
Adafruit_CCS811 ccs;

void setup() {
  pinMode(uv_ain,INPUT);
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
  ad_value=analogRead(uv_ain);
  
  if(ccs.available()){
    if(!ccs.readData()){
      //Serial.print("CO2: ");
      if(ccs.geteCO2() != 0){
        Serial.println("{\"CO2\":"+String(ccs.geteCO2())+
                      ",\"TVOC\":"+String(ccs.getTVOC())+
                      ",\"HUM\":"+String(h)+
                      ",\"TEMP\":"+String(t)+
                      ",\"UV\":"+String(ad_value)+"}");
      }
      //Serial.print("ppm, TVOC: ");
      // (gramos/metrocubico)productos químicos que se convierten 
      //fácilmente en vapores o gases (metano, etano, propano, n-butano, n-pentano, benceno, tolueno, xileno y etileno)
      
    }
    else{
      Serial.println("None");
      while(1);
    }
  }
  delay(2000);
}
