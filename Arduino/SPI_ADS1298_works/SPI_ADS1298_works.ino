// include the SPI library:
#include <SPI.h>

/* Operational Modes
0 - read initial registers only
1 - check noise
2 - square-wave signal test
3 - regular input mode
*/
const int op_mode = 3;

// use xbee transmission 0 / 1
const int xbee = 1;

// start() or print to serial monitor
const int debug = 0;

const int clk_div = 21;

const int ss = 10;
const int START = 11;
const int DRDY = 9;
const int PDWN = 8;
const int RESET = 8;

byte regs[26];

byte drdy_temp;
byte drdy_val;
byte d_out[27];

byte wait;

// Read registers
void read_regs() {  
  SPI.transfer(ss, 32, SPI_CONTINUE); // RREG start at reg 0
  SPI.transfer(ss, 25, SPI_CONTINUE); // RREG 26 registers  
  for (int i=0; i<26; i++) regs[i] = SPI.transfer(ss, 0, SPI_CONTINUE);
  digitalWrite(ss, HIGH);
  for (int i=0; i<26; i++) {
    Serial.print("R");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(regs[i]);
  }
}

boolean is_start_code(char code[]) {
  if (code[0] == 'B' && code[1] == 'e' &&
    code[2] == 'g' && code[3] == 'i' &&
    code[4] == 'n' && code[5] == '!')
    return true;
  return false;
}

boolean is_stop_code(char code[]) {
  if (code[0] == 'S' && code[1] == 't' &&
    code[2] == 'o' && code[3] == 'p' &&
    code[4] == '!')
    return true;
  return false;
}

void get_data() {
  for (int i=0; i<27; i++) d_out[i] = SPI.transfer(ss, 0, SPI_CONTINUE);
    if (!debug) {
      for (int i=0; i<27; i++) Serial1.write(d_out[i]);
    } else if (debug) {
      for (int i=0; i<27; i++) Serial.println(d_out[i]);
    }
    digitalWrite(ss, HIGH);
}

void setup() {
  // put your setup code here, to run once:
  
  if (debug == 1) Serial.begin(9600);
  Serial1.begin(57600);
  pinMode(START, OUTPUT);
  pinMode(PDWN, OUTPUT);
  pinMode(DRDY, INPUT);
  
  for (int i=0; i<26; i++) regs[i] = 0;
  
  // initialize SPI
  SPI.begin(ss); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(ss, SPI_MODE1); 
  SPI.setBitOrder(ss, MSBFIRST);
  SPI.setClockDivider(ss, clk_div);
  
  // Write PDWN HIGH
  digitalWrite(PDWN, HIGH);
  // Write RESET HIGH
  digitalWrite(RESET, HIGH);
  // wait 1 second for power-on reset
  delay(1000);
  
  // issue reset command
  SPI.transfer(ss, 6);
  // wait 18 clock cycles
  delayMicroseconds(5);
  
  // send SDATAC command
  SPI.transfer(ss, 17, SPI_CONTINUE);
  delayMicroseconds(1);
  digitalWrite(ss, HIGH);
  
  if (debug == 1) read_regs();
  
  // WREG CONFIG1 0x86
  SPI.transfer(ss, 65, SPI_CONTINUE); // start at register 1
  SPI.transfer(ss, 0, SPI_CONTINUE); // # regs to write - 1
  SPI.transfer(ss, 134, SPI_CONTINUE); // set in HR Mode and DR = f /1024 (x86)
  delayMicroseconds(1);
  digitalWrite(ss, HIGH);
  
  if (op_mode == 1) {
    // WREG CONFIG2 0x00
    SPI.transfer(ss, 66, SPI_CONTINUE); // start at register 1
    SPI.transfer(ss, 0, SPI_CONTINUE); // set CONFIG2 to 0
    SPI.transfer(ss, 0, SPI_CONTINUE);
    delayMicroseconds(1);
    digitalWrite(ss, HIGH);
    
    // Set All Channels to Input Short (1)
    SPI.transfer(ss, 69, SPI_CONTINUE); // start at register 5
    SPI.transfer(ss, 7, SPI_CONTINUE); // # write 8 registers
    for (int i=0; i<8; i++) SPI.transfer(ss, 1, SPI_CONTINUE);
    digitalWrite(ss, HIGH);
    
    if (debug == 1) {
      Serial.println("Noise Testing: New Register Values");
      // Read registers again
      read_regs();
    }
  }
  
  if (op_mode == 2) {
    // WREG CONFIG2 0x10
    SPI.transfer(ss, 66, SPI_CONTINUE); // start at register 2
    SPI.transfer(ss, 0, SPI_CONTINUE);
    SPI.transfer(ss, 16, SPI_CONTINUE);
    delayMicroseconds(1);
    digitalWrite(ss, HIGH);
    
    // Activate a 1mV x Vref/2.4) square-wave test signal on all channels (5)
    SPI.transfer(ss, 69, SPI_CONTINUE); // start at register 5
    SPI.transfer(ss, 7, SPI_CONTINUE); // # write 8 registers
    for (int i=0; i<8; i++) SPI.transfer(ss, 5, SPI_CONTINUE);
    digitalWrite(ss, HIGH);
    
    // Read registers again
    if (debug == 1) {
      Serial.println("Square-Wave Testing: New Register Values");
      read_regs();
    }
  }
  
  if (op_mode == 3) {
    if (debug == 1) {
      Serial.println("Regular Input mode");
      read_regs();
    }  
  }
  
  // Set START HIGH
  digitalWrite(START, HIGH);
  delay(5);

  // Put device back in RDATAC mode
  SPI.transfer(ss, 16, SPI_CONTINUE);
  delayMicroseconds(1);
  digitalWrite(ss, HIGH);
  
  drdy_temp = 1;
  drdy_val = 1;
  for (int i=0; i<27; i++) d_out[i] = 0;
  
  if (debug == 1) Serial.println("Ready to collect data!");
  
  if (xbee) wait = 1;
  
}

void loop() {
  // put your main code here, to run repeatedly:
  
   if (xbee) {
     // Wait until asked to start
     while (wait) {
       if (Serial1.available() >= 6) {
         char cmd[7];
         cmd[6] = '\0';
         for (int i = 0; i < 6; i++)  {
           cmd[i] = Serial1.read();
         }
         if (is_start_code(cmd)) {
           wait = 0;
         }
         else {
           Serial1.println(cmd);
           // Flush input and retry
           while (Serial1.available()) {
             Serial1.println(Serial1.read());
           }
         }
       }
     }
  }
  
 // check DRDY and send data to XBee
  drdy_temp = digitalRead(DRDY);
  if (drdy_temp != drdy_val) {
    drdy_val = drdy_temp;
    if (!drdy_val) {
      for (int i=0; i<27; i++) d_out[i] = SPI.transfer(ss, 0, SPI_CONTINUE);
      if (!debug) {
        for (int i=0; i<27; i++) Serial1.write(d_out[i]);
      } else if (debug) {
        for (int i=0; i<27; i++) Serial.println(d_out[i]);
      }
      digitalWrite(ss, HIGH);
    }
  }
  
   if (xbee) {
   if (!wait) {
  if (Serial1.available() >= 5) {
     char cmd[6];
     cmd[5] = '\0';
     for (int i = 0; i < 5; i++)  {
     cmd[i] = Serial1.read();
     }
     if (is_stop_code(cmd)) {
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
  }
  } 
   
}
