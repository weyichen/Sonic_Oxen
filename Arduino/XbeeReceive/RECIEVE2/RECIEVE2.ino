 const int ledPin = 13; // the pin that the LED is attached to
int incomingByte;      // a variable to read incoming serial data into
int upper, lower;

void setup() {
 // initialize serial communication:
 Serial.begin(9600);
 // initialize the LED pin as an output:
 pinMode(ledPin, OUTPUT);
}

void loop() {
 // see if there's incoming serial data:
 // make sure both upper and lower bits have been received
 
 // Code to read in a 16-bit int by separately receiving and 
 // concatenating upper and lower 8-bits
 
 // receiving strings
 if (Serial.available() >= 5) {
   int vals[5];
   for (int i = 0; i < 5; i++) {
     vals[i] = Serial.read();
   }
   Serial.print(vals[0]);
   for (int i = 1; i < 5; i++) {
     Serial.print(",");
     Serial.print(vals[i]);
   }
   Serial.println();
 }
}
