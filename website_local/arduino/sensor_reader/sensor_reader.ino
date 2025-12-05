#include <DHT.h>
#include <math.h>

// Define pins
#define DHTPIN 8
#define DHTTYPE DHT22
#define SOIL_PIN A0

DHT dht(DHTPIN, DHTTYPE);

const int sen_max = 570;
const int sen_min = 246;

void setup() {
  Serial.begin(115200); 
  dht.begin();
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();  

    if (command == "read") {
      int soilMoistureValue = analogRead(SOIL_PIN);
      float soilMoisturePercent = map(soilMoistureValue, sen_max, sen_min, 0.0, 100.0);
      soilMoisturePercent = constrain(soilMoisturePercent, 0.0, 100.0);

      float humidity = dht.readHumidity();
      float temperature = dht.readTemperature();

      if (isnan(humidity)) humidity = 0.0;
      if (isnan(temperature)) temperature = 0.0;

      
      Serial.print(soilMoisturePercent, 1);
      Serial.print(",");
      Serial.print(temperature, 1);
      Serial.print(",");
      Serial.println(humidity, 1);

      Serial.flush();  
    }
  }
}
