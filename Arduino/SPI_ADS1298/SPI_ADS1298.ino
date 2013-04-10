// include the SPI library:
#include <SPI.h>

const int ss = 10;
const int mosi = 11;
const int miso = 12;
const int sck = 13;

void setup() {
  
  byte regs[20];
  for (int i=0; i<20; i++) {
    regs[i] = 0; 
  }  
  
  Serial.begin(57600);
  
  // initialize SPI
  SPI.begin(); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(SPI_MODE1); 
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(ss,21);
  
  digitalWrite(ss, LOW);
  shiftOut(mosi, sck, MSBFIRST, 17);
  delayMicroseconds(2); // wait >4 cycles = 0.25uS * 4 = 1uS
  digitalWrite(ss, HIGH);
 
  // RREG
  digitalWrite(ss, LOW);
  
  shiftOut(mosi, sck, MSBFIRST, 32);
  //delayMicroseconds(2);
  shiftOut(mosi, sck, MSBFIRST, 3);
//  SPI.transfer(3); // RREG 19 registers

  regs[0] = shiftIn(miso, sck, MSBFIRST);
  //delayMicroseconds(2);
  regs[1] = shiftIn(miso, sck, MSBFIRST);
  //delayMicroseconds(2);
  regs[2] = shiftIn(miso, sck, MSBFIRST);
  
  delayMicroseconds(2);
  digitalWrite(ss, HIGH);
  
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
  //digitalWrite(SS, LOW);
}

