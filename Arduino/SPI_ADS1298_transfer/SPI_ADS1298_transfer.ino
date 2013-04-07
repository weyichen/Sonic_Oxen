// include the SPI library:
#include <SPI.h>

void setup() {
  
  Serial.begin(57600);
  
  // initialize SPI
  SPI.begin(); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(SPI_MODE1); 
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV4);
  
  digitalWrite(SS, LOW);
  SPI.transfer(11); // Stop Read Data Continuously mode
  delayMicroseconds(2);
  digitalWrite(SS, HIGH);
  
  byte regs[20];
  for (int i=0; i<20; i++) {
    regs[i] = 0; 
  }
  
  // RREG
  digitalWrite(SS, LOW);
  SPI.transfer(32); // RREG start at reg 0
  
  //delayMicroseconds(2);
  
  SPI.transfer(3); // RREG 19 registers
  
  regs[0] = SPI.transfer(0);
  regs[1] = SPI.transfer(0);
  regs[2] = SPI.transfer(0);
  
  delayMicroseconds(2);
  digitalWrite(SS, HIGH);  
  
  for (int i=0; i<20; i++) {
    Serial.println(regs[i]);  
  }
  
}
  
void loop() {
}
