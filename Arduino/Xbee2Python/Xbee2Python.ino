byte wait;

void setup() {
 Serial.begin(57600);
 Serial1.begin(57600);
 
 // Wait until asked to start
 String start_code = "Begin!";
 wait = 1;
 
 while (wait) {
   if (Serial.available() >= 6) {
     char cmd[7];
     cmd[6] = '\0';
     for (int i = 0; i < 6; i++)  {
       cmd[i] = Serial.read();
     }
     if (start_code.equals(cmd)) {
       wait = 0;
       Serial1.print(start_code);
     }
     else {
       Serial.println(cmd);
     }
   }
 }
 
}

byte data;

void loop() {
  
  if (Serial1.available()) {
    
    data = Serial1.read();
    Serial.write(data);
    
  }
}
