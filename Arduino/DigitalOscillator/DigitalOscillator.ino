//sends an alternating signal to the serial port

int i, upper, lower = 0;

void setup() {
  Serial.begin(9600);
  digitalWrite(3, LOW);
}
void loop() {
  if (i < 500) {
    i+=10;
  } 
  else {
    i = 0;
  }
  
  upper = i >> 8;
  lower = i & 255;
  
  digitalWrite(3, HIGH);
  delay(i);
  digitalWrite(3, LOW);
  delay(i);
  
  
  //Serial.print(i);
}

