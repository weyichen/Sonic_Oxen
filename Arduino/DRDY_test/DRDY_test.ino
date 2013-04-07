#include <SPI.h>

void setup() {
//  Serial.begin(57600);
//  
  SPI.begin(); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(SPI_MODE1); 
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV8);
  
  digitalWrite(7, HIGH);
}

void loop() {
  digitalWrite(7, LOW);
  delay(2000);
  digitalWrite(7, HIGH);
}
