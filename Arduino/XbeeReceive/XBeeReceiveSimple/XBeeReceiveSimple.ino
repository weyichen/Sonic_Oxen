int incomingByte;
int upper, lower;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() >= 2) {
    // read the oldest byte in the serial buffer:
    upper = Serial.read();
    lower = Serial.read();
    
    incomingByte = (upper << 8) | lower;
    Serial.println(incomingByte);
  }
}
