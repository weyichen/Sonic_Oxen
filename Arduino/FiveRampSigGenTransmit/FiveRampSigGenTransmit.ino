int x = 0;
int y = 0;
int z = 0;
int a = 100;
int b = 100;

void setup() {
 // initialize serial communications at 9600 bps:
 Serial.begin(9600); 
}

void loop() {
 x++;
 if (x > 100) {
   x = 1;
 }
 y += 4;
 if (y > 100) {
   y = 1;
 }
 z += 7;
 if (z > 100) {
   z = 1;
 }
 a -= 3;
 if (a < 4) {
   a = 100;
 }
 b -= 5;
 if (b < 6) {
   b = 100;
 } 
  
 Serial.print(x);
 Serial.print(",");
 Serial.print(y);
 Serial.print(","); 
 Serial.print(z);
 Serial.print(","); 
 Serial.print(a);
 Serial.print(","); 
 Serial.println(b);

 // wait 2 milliseconds before the next loop
 delayMicroseconds(50);                     
}
