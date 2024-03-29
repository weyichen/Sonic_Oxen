// include the SPI library:
#include <SPI.h>

const int ss = 10;
const int START = 11;
const int DRDY = 9;

void setup() {
  
  Serial.begin(57600);
  
  byte regs[20];
  for (int i=0; i<20; i++) {
    regs[i] = 0; 
  }
  
  // initialize SPI
  SPI.begin(ss); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(ss, SPI_MODE0); 
  SPI.setBitOrder(ss, MSBFIRST);
  SPI.setClockDivider(ss, 42);
  
//  // Write START HIGH
//  digitalWrite(START, HIGH);
//  
//  // Reset
//  SPI.transfer(ss, 6);
//  delayMicroseconds(9);
  
  // Stop Read Data Continuously mode
  SPI.transfer(ss, 17, SPI_CONTINUE);
  delayMicroseconds(2);
  digitalWrite(ss, HIGH);

  // RREG
  SPI.transfer(ss, 32, SPI_CONTINUE); // RREG start at reg 0
  SPI.transfer(ss, 19, SPI_CONTINUE); // RREG 19 registers
  
  for (int i=0; i<19; i++) {
    regs[i] = SPI.transfer(ss, 0, SPI_CONTINUE);
  }
  regs[19] = SPI.transfer(ss, 0);
  
  /*
  regs[0] = SPI.transfer(ss, 0, SPI_CONTINUE);
  regs[1] = SPI.transfer(ss, 0, SPI_CONTINUE);
  regs[2] = SPI.transfer(ss, 0, SPI_LAST);
  */
  
  for (int i=0; i<20; i++) {
    Serial.println(regs[i]);  
  }
  
}
  
void loop() {
}
