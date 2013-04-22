byte data;

void setup() {
 Serial1.begin(57600);
}

void loop() {
  if (Serial1.available()) {
    
    data = Serial1.read();
    Serial1.write(data);
  }
}
