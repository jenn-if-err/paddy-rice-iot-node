#include <DHT.h>
#include <math.h>

// Define pins
#define DHTPIN 8
#define DHTTYPE DHT22
#define SOIL_PIN A0

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);
int sen_max = 570;
int sen_min = 246;

void setup() {
  // Start serial communication
  Serial.begin(115200);

  // Start DHT sensor
  dht.begin();
}  // <-- This closing brace was missing

void loop() {
  // Read soil moisture
  int soilMoistureValue = analogRead(SOIL_PIN);
  double soilMoisturePercent = map(soilMoistureValue, sen_max, sen_min, 0.0, 100.0);
  if (soilMoisturePercent < 0) soilMoisturePercent = 0;

  // Read temperature and humidity
  double humidity = dht.readHumidity();
  double temperature = dht.readTemperature();

  // Check if any reads failed and exit early
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    temperature = 0.0;
    humidity = 0.0;
  }

     Serial.print(soilMoisturePercent, 1);
      Serial.print(",");
      Serial.print(temperature, 1);
      Serial.print(",");
      Serial.println(humidity, 1);

      Serial.flush();  // Ensure it's all sent

  // Delay before next reading
  delay(10000);
}
