int step = 0;
int text[10];
long rate1 = 9600;
long rate2 = 9600;

void setup() {
  Serial.begin(rate1);
}

void loop() {
  if (!step) {
    delay(2000);
    Serial.print("+++"); // begin command mode
    delay(2000);
    Serial.println();
  }
  if (Serial.available() >= 3) { // expecting 3 bytes: OK\r
    delay(1000);
    int j = 0; // track the number of bytes read
    for (int i = 0; Serial.available() && i < 10; i++) {
      text[i] = Serial.read();
      j++;
    }
    
    int receivedO = 0;
    
    for (int i = 0; i < j; i++) { // only run up to number of bytes read
      Serial.write(text[i]);
      if (receivedO && text[i] == 'K') {
        step++;
        if (step == 1) { // first OK
          Serial.print("ATBD3"); // set baud rate
          Serial.begin(rate2); // change Arduino rate to match new Xbee rate
        }
        else if (step == 2) { // second OK
          Serial.print("ATWR"); // write baud rate permanently to memory
        }
        
      } else if (text[i] == 'O'){
        receivedO = true;
      } else {
       receivedO = false; 
      }
      
//      if (text[i] == 'O' && text[i] == 'K') {
//        step++;
//        if (step == 1) {
//          Serial.print("ATBD7");
//        }
//        else if (step == 2) {
//          Serial.print("ATWR");
//        }
//      }

    }
  }
}
