// include the SPI library:
#include <SPI.h>

const int ss = 52;

void setup() {
  
  Serial.begin(57600);
  
  byte regs[20];
  for (int i=0; i<20; i++) {
    regs[i] = 1; 
  }
  
  // initialize SPI
  SPI.begin(ss); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(ss, SPI_MODE1); 
  SPI.setBitOrder(ss, MSBFIRST);
  SPI.setClockDivider(ss, 21);
  
  SPI.transfer(ss, 11, SPI_LAST); // Stop Read Data Continuously mode

  // RREG
  SPI.transfer(ss, 16, SPI_CONTINUE); // RREG start at reg 0
  SPI.transfer(ss, 19, SPI_CONTINUE); // RREG 19 registers
  
  for (int i=0; i<19; i++) {
    regs[i] = SPI.transfer(ss, 1, SPI_CONTINUE);
  }
  regs[19] = SPI.transfer(ss, 1, SPI_LAST);
  
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
