byte data;

void setup() {
 Serial.begin(57600);
}

void loop() {
  if (Serial.available()) {
    
    data = Serial.read();
    Serial.write(data);
  }
}
