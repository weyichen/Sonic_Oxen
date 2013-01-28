//sends an alternating signal to the serial port

void setup() {
  Serial.begin(9600);
}

void loop() {
 if (i < 200) {
   i+=10; 
 } else {
   i = 0;
 }
   Serial.println(i);
   Serial.print("\n");
   
   delay(100);
 }

}
