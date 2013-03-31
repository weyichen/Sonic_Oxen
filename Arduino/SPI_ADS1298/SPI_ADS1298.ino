// include the SPI library:
#include <SPI.h>

// set SPI interface pins
//const int SS = 10;
//const int MOSI = 11;
//const int MISO = 12;
//const int SCK = 13;

void setup() {
  
  Serial.begin(57600);
  
  // initialize SPI
  SPI.begin(); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(SPI_MODE1); 
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV4);
  
  digitalWrite(SS, LOW);
  shiftOut(MOSI, SCK, MSBFIRST, 11);
  //SPI.transfer(11); // Stop Read Data Continuously mode
  digitalWrite(SS, HIGH);
  
  delayMicroseconds(2); // wait >4 cycles = 0.25uS * 4 = 1uS
 
  byte regs[20];
  
  for (int i=0; i<20; i++) {
    regs[i] = 0; 
  }  
 
  // RREG
  digitalWrite(SS, LOW);
  shiftOut(MOSI, SCK, MSBFIRST, 32);
  regs[9] = shiftIn(MISO, SCK, MSBFIRST);
//  SPI.transfer(32); // RREG start at reg 0
  //delayMicroseconds(2);
  shiftOut(MOSI, SCK, MSBFIRST, 3);
//  SPI.transfer(3); // RREG 19 registers

  regs[0] = shiftIn(MISO, SCK, MSBFIRST);
  //delayMicroseconds(2);
  regs[1] = shiftIn(MISO, SCK, MSBFIRST);
  //delayMicroseconds(2);
  regs[2] = shiftIn(MISO, SCK, MSBFIRST);
  //delayMicroseconds(2);
  digitalWrite(SS, HIGH);
  
//  regs[0] = SPI.transfer(0);
//  regs[1] = SPI.transfer(0);
//  regs[2] = SPI.transfer(0);
  
//  for (int i=0; i<20; i++) {
//    regs[i] = SPI.transfer(0);  
//  }

  for (int i=0; i<20; i++) {
    Serial.println(regs[i]);  
  }  
  
 // reset the ADS1298
 //digitalWrite(SS, LOW);
 //SPI.transfer(6); // RESET
 
 //digitalWrite(SS, HIGH);
}

void loop() {
  digitalWrite(SS, LOW);
}
