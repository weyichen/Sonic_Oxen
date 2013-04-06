//sends an alternating signal to the serial port

int i, upper, lower = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (i < 250) {
    i+=10;
  } 
  else {
    i = 0;
  }
  analogWrite(3, i);
  delay(10);
  
  //Serial.print(i);
}

