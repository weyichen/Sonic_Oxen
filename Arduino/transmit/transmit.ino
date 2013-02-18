int analogPin = 5;
int val;
int i, upper, lower = 0;


void setup() {
  
Serial.begin(9600);
}


void loop() {

val = analogRead(analogPin); // read the input pin
//Serial.write(val); // debug value
//Serial.w("\n");
upper = val >> 8;
lower = val & 255;
Serial.write(upper);
Serial.write(lower);
delay(100);
}



