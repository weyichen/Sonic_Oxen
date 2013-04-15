String start_code = "Begin!";
String stop_code = "Stop!";
long data[12];
double r = 0.;
byte wait = 1;
int delaytest_count;
long amp = 1000000;

void setup() {
 // initialize serial communications at 57600 bps:
 Serial.begin(57600);
 //Serial.begin(9600);
 //digi//Serial.talWrite(8, HIGH);
 //pinMode(8, OUTPUT);
 
 //Serial.println("HIGHAMP");
}

void loop() {
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
       else {
         // Flush input and retry
         while (Serial.available()) {
           Serial.read();
         }
       }
     }
   }
 
  r=r+0.05;
  
  delaytest_count++;
  if (delaytest_count == 500) {
    amp = 500000;
    //Serial.println("LOWAMP");
  } else if (delaytest_count == 1000) {
    amp = 1000000;
    //Serial.println("HIGHAMP");
    delaytest_count = 0;
  }
 
 for (int i=0; i<12; i++){
  data[i] = long(amp*sin((i+1) * r));
 }
 
 byte byte1, byte2, byte3, byte4;
 
 for (int i=0; i<12; i++){
  byte1 = byte(data[i] >> 16 & 255);
  byte2 = byte((data[i] >> 8) & 255);
  byte3 = byte(data[i] & 255);
  
  Serial.write(byte1);
  Serial.write(byte2);
  Serial.write(byte3);
 }
 
 if (Serial.available() >= 5) {
   char cmd[6];
   cmd[5] = '\0';
   for (int i = 0; i < 5; i++)  {
     cmd[i] = Serial.read();
   }
   if (stop_code.equals(cmd)) {
     wait = 1;
   }
   // Flush input if not appropriate
   else {
     Serial.println();
     while(Serial.available()) {
       Serial.write(Serial.read());
     }
   }
 }

 // wait 2 milliseconds before the next loop
 delay(2);                  
}
