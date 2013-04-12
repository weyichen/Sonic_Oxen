long data[5];
double r = 0.;
byte wait = 1;

String start_code = "Begin!";
String stop_code = "Stop!";


void setup() {
 // initialize serial communications at 57600 bps:
 Serial.begin(57600);
 
 digitalWrite(8, HIGH);
 pinMode(8, OUTPUT);
 
 // Wait until asked to start
 while (wait) {
   if (Serial.available() >= 6) {
     char cmd[7];
     cmd[6] = '\0';
     for (int i = 0; i < 6; i++)  {
       cmd[i] = Serial.read();
     }
     if (start_code.equals(cmd)) {
       wait = 0;
     }
   }
 }
}

void loop() {
 r=r+0.05;
 long amp = 1000000;
 
 for (int i=0; i<5; i++){
  data[i] = long(amp*sin((i+1) * r));
 }
 
 byte byte1, byte2, byte3, byte4;
 
 for (int i=0; i<5; i++){
  byte1 = byte(data[i] >> 24 & 255);
  byte2 = byte((data[i] >> 16) & 255);
  byte3 = byte((data[i] >> 8) & 255);
  byte4 = byte(data[i] & 255);
  
  Serial.write(byte1);
  Serial.write(byte2);
  Serial.write(byte3);
  Serial.write(byte4);
 }
 
 if (Serial.available() >= 5) {
   char cmd[6];
   cmd[5] = '\0';
   for (int i = 0; i < 5; i++)  {
     cmd[i] = Serial.read();
   }
   if (stop_code.equals(cmd)) {
     digitalWrite(8, LOW);
   }
 }

 // wait 2 milliseconds before the next loop
 delayMicroseconds(2);                  
}
