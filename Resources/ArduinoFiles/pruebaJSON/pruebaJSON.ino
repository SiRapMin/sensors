void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("{\"CO2\":"+String(random(350,370))+
                      ",\"TVOC\":"+String(random(100,120))+
                      ",\"HUM\":"+String(random(50,60))+
                      ",\"TEMP\":"+String(random(18,20))+
                      ",\"UV\":"+String(random(4,7))+"}");
  delay(2000);
}
