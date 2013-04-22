// include the SPI library:
#include <SPI.h>

const int ss = 10;

const int START = 11;
const int DRDY = 9;
const int PWDN = 8;
const int RESET = 7;

void setup() {
  // put your setup code here, to run once:
  
  Serial.begin(57600);
  
  byte regs[20];
  for (int i=0; i<20; i++) {
    regs[i] = 0; 
  }
  
  // initialize SPI
  SPI.begin(ss); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(ss, SPI_MODE1); 
  SPI.setBitOrder(ss, MSBFIRST);
  SPI.setClockDivider(ss, 21);
  
  // Write PWDN HIGH
  digitalWrite(PWDN, HIGH);
  // Write RESET HIGH
  
  delay(1000);
  
  // Write RESET LOW
  // issue reset command
  SPI.transfer(ss, 6);
  // wait 18 clock cycles
  delayMicroseconds(5);
  
  // send SDATAC command
  SPI.transfer(ss, 17, SPI_CONTINUE);
  delayMicroseconds(1);
  digitalWrite(ss, HIGH);
  
  // RREG
  SPI.transfer(ss, 32, SPI_CONTINUE); // RREG start at reg 0
  SPI.transfer(ss, 19, SPI_CONTINUE); // RREG 19 registers
  
  for (int i=0; i<19; i++) {
    regs[i] = SPI.transfer(ss, 0, SPI_CONTINUE);
  }
  regs[19] = SPI.transfer(ss, 0);
  
  for (int i=0; i<20; i++) {
    Serial.println(regs[i]);  
  }
  
}

void loop() {
  // put your main code here, to run repeatedly: 
  
}
