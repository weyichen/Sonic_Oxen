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
void rec_ok() {
  if (Serial.available() >= 3) {
    
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
    if (text[0] == 'O' && text[1] == 'K') {
      step++;
    }
  }
}

void setup() {
  Serial.begin(rate1);
}

void loop() {
  
  // Step 0: attempt to enter command mode
  if (!step) {
    talk("+++");
    rec_ok();
  }
  
  // Step 1: get current baud rate
  else if (step == 1) {
    talk("ATBD\r");
    
    // output current baud rate
    if (Serial.available()) {
      Serial.write(Serial.read());
      Serial.println();
      step++;
    }
  }
  
  // Step 2: change the baud rate
  else if (step == 2) {
    talk(BAUD);
    
    rec_ok();
  }
  
  // Step 3: write data to memory
  else if (step == 3) {
    delay(2000); // need this delay for the same reason as below
    Serial.print("ATWR\r"); // send command
    delay(2000); // need this delay so that +++ are the only characters seen
    Serial.println();
    
    
    //talk("ATWR\r");
    rec_ok();
  }
  
  // Step 4: leave command mode
  else if (step == 4) {
    talk("ATCN\r");
    rec_ok();
  }
}
