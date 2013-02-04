int x = 0;

void setup() {
 // initialize serial communications at 9600 bps:
 Serial.begin(9600); 
}

void loop() {
 x++;
 if (x > 100) {
   x = 1;
 }
 
 Serial.println(x);  

 // wait 2 milliseconds before the next loop
 delay(2);                     
}
