//sends an alternating signal to the serial port

int i, upper, lower = 0;

void setup() {
  Serial.begin(9600);
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
  
  Serial.write(upper);
  Serial.write(lower);
  delay(100);
  
  //Serial.print(i);
}

