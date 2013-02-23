void setup() {
 Serial.begin(115200); 
}

byte data;

void loop() {
  
  if (Serial.available()) {
    
    data = Serial.read();
    Serial.write(data);
    
  }
}
