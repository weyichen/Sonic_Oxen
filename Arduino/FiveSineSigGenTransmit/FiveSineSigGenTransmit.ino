String start_code = "Begin!";
String stop_code = "Stop!";
long data[5];
double r = 0.;
byte wait = 1;

void setup() {
 // initialize serial communications at 57600 bps:
 Serial1.begin(57600);
 //digitalWrite(8, HIGH);
 //pinMode(8, OUTPUT);
}

void loop() {
  // Wait until asked to start
   while (wait) {
     if (Serial1.available() >= 6) {
       char cmd[7];
       cmd[6] = '\0';
       for (int i = 0; i < 6; i++)  {
         cmd[i] = Serial1.read();
       }
       if (start_code.equals(cmd)) {
         wait = 0;
       }
       else {
         // Flush input and retry
         while (Serial1.available()) {
           Serial1.read();
         }
       }
     }
   }
 
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
  
  Serial1.write(byte1);
  Serial1.write(byte2);
  Serial1.write(byte3);
  Serial1.write(byte4);
 }
 
 if (Serial1.available() >= 5) {
   char cmd[6];
   cmd[5] = '\0';
   for (int i = 0; i < 5; i++)  {
     cmd[i] = Serial1.read();
   }
   if (stop_code.equals(cmd)) {
     wait = 1;
   }
   // Flush input if not appropriate
   else {
     Serial1.println();
     while(Serial1.available()) {
       Serial1.write(Serial1.read());
     }
   }
 }

 // wait 2 milliseconds before the next loop
 delay(2);                  
}
