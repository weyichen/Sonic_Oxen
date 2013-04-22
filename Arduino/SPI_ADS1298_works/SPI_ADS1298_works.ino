// include the SPI library:
#include <SPI.h>

String start_code = "Begin!";
String stop_code = "Stop!";

const int clk_div = 21;
const int ss = 10;

const int START = 11;
const int DRDY = 9;
const int PDWN = 8;
const int RESET = 8;

byte regs[26];

// Read registers
void read_regs() {  
  SPI.transfer(ss, 32, SPI_CONTINUE); // RREG start at reg 0
  SPI.transfer(ss, 25, SPI_CONTINUE); // RREG 26 registers  
  for (int i=0; i<26; i++) regs[i] = SPI.transfer(ss, 0, SPI_CONTINUE);
  digitalWrite(ss, HIGH);
  for (int i=0; i<26; i++) Serial1.println(regs[i]);
}

void setup() {
  // put your setup code here, to run once:
  
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
  
  read_regs();
  
  // Write setting registers
  // WREG CONFIG1 0x86
  // WREG CONFIG1 0x86
  SPI.transfer(ss, 65, SPI_CONTINUE); // start at register 1
  SPI.transfer(ss, 1, SPI_CONTINUE); // # regs to write - 1
  SPI.transfer(ss, 134, SPI_CONTINUE); // set in HR Mode and DR = f /1024 (x86)
  SPI.transfer(ss, 0); // set CONFIG2 to 0
  
//  // Set All Channels to Input Short (1)
//  SPI.transfer(ss, 69, SPI_CONTINUE); // start at register 5
//  SPI.transfer(ss, 7, SPI_CONTINUE); // # write 8 registers
//  for (int i=0; i<8; i++) SPI.transfer(ss, 1, SPI_CONTINUE);
//  digitalWrite(ss, HIGH);
  
  Serial1.println("NEW VALUES");
  // Read registers again
  read_regs();
  
  // Set test signals
  // SDATAC
//  SPI.transfer(ss, 17, SPI_CONTINUE);
//  delayMicroseconds(1);
//  digitalWrite(ss, HIGH);
//  
//  // WREG CONFIG2 0x10
//  SPI.transfer(ss, 66, SPI_CONTINUE); // start at register 2
//  SPI.transfer(ss, 0, SPI_CONTINUE);
//  SPI.transfer(ss, 16);
//  
//  Serial1.println("Ready to test square wave");
//  
//  // Activate a 1mV x Vref/2.4) square-wave test signal on all channels (5)
//  SPI.transfer(ss, 69, SPI_CONTINUE); // start at register 5
//  SPI.transfer(ss, 7, SPI_CONTINUE); // # write 8 registers
//  for (int i=0; i<8; i++) SPI.transfer(ss, 5, SPI_CONTINUE);
//  digitalWrite(ss, HIGH);
  
    // Set START HIGH
  digitalWrite(START, HIGH);
  delay(5);

  // Put device back in RDATAC mode
  SPI.transfer(ss, 16, SPI_CONTINUE);
  delayMicroseconds(1);
  digitalWrite(ss, HIGH);
  
  byte drdy_temp = 1;
  byte drdy_val = 1;
  byte d_out[27];
  for (int i=0; i<27; i++) d_out[i] = 0;
  
 Serial1.println("Ready to check noise");
  
  // Capture data and check noise
  // Look for DRDY and issue 24 + n * 24 SCLKs
  int counter = 0;
  
   byte wait = 1;
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
  
  while (counter < 100000) {
   drdy_temp = digitalRead(DRDY);
   
   // if drdy has toggled
   if (drdy_temp != drdy_val) {
    drdy_val = drdy_temp;
    
    // if toggled to low, data is available
    if (drdy_val == 0) {
      // SPI.transfer(ss, 18);
      for (int i=0; i<27; i++) d_out[i] = SPI.transfer(ss, 0, SPI_CONTINUE);
      digitalWrite(ss, HIGH);
      
      for (int i=0; i<27; i++) Serial1.write(d_out[i]);
      //
      counter++;
    }
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
  }
  
  // Capture Data and Test Signal
  // Look for DRDY and issue 24 + n * 24 SCLKs
 
}

void loop() {
  // put your main code here, to run repeatedly: 
  
}
