# define BAUD "ATBD7\r"

int step = 0;
int text[10];
long rate1 = 115200;
//long rate2 = 115200;

// helper function: send a command with appropriate delays
void talk(char* cmd) {
  delay(2000); // need this delay for the same reason as below
  Serial.print(cmd); // send command
  delay(2000); // need this delay so that +++ are the only characters seen
  Serial.println();
}

// helper function: step++ if OK was received from Xbee module
void rec_ok(int bytesExp) {
  if (Serial.available() >= bytesExp) {
    
    int numbytes = Serial.available();
    
    // get all bytes received
    for (int i=0; i < numbytes; i++) {
      text[i] = Serial.read();  
    }
    
    // print out all bytes received
    for (int i=0; i < numbytes; i++) {
      Serial.write(text[i]);
    }
    Serial.println();
    
    // move to the next step if we receive okay
    //if (text[0] == 'O' && text[1] == 'K') {
      step++;
    //}
  }
}

void setup() {
  Serial.begin(rate1);
}

void loop() {
  
  // Step 0: attempt to enter command mode
  if (!step) {
    talk("+++");
    rec_ok(3);
  }
  
  // Step 1: get current baud rate
  else if (step == 1) {
    talk("ATBD\r");
    rec_ok(1);
    
//    // output current baud rate
//    if (Serial.available()) {
//      Serial.write(Serial.read());
//      Serial.println();
//      step++;
//    }
  }
  
  // Step 2: get ID
  else if (step == 2) {
    talk("ATID\r");
    rec_ok(4);
  }
  
 // Step 3: get CH
  else if (step == 3) {
    talk("ATCH\r");
    rec_ok(1);
  }
  
  // Step 4: get MY
  else if (step == 4) {
    talk("ATMY\r");
    rec_ok(1);
  }
  
  // Step 4: get DH
  else if (step == 5) {
    talk("ATDH\r");
    rec_ok(1);
  }
  
  // Step 4: get DL
  else if (step == 6) {
    talk("ATDL\r");
    rec_ok(1);
  }
  
  // Step 4: get SH
  else if (step == 7) {
    talk("ATSH\r");
    rec_ok(16);
  }

  // Step 4: get SL
  else if (step == 8) {
    talk("ATSL\r");
    rec_ok(16);
  }

  // Step 4: close command mode
  else if (step == 9) {
    talk("ATCN\r");
    rec_ok(3);
  }
}
