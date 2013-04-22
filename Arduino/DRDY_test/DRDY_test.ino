#include <SPI.h>

const int ss = 10;
const int START = 11;
const int DRDY = 9;

byte drdy_val = 0;
byte drdy_temp = 0;

void setup() {
  Serial.begin(57600);
 
  SPI.begin(ss); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(ss, SPI_MODE1); 
  SPI.setBitOrder(ss, MSBFIRST);
  SPI.setClockDivider(ss, 21);
  
  digitalWrite(ss, HIGH);
  
  // Write START HIGH
  digitalWrite(START, HIGH);
  delay(5);
  
  //
  
  // Reset
  SPI.transfer(ss, 6);
  delayMicroseconds(9);
}

void loop() {
  drdy_temp = digitalRead(DRDY);
  
  if (drdy_temp != drdy_val) {
    drdy_val = drdy_temp;
    Serial.println(drdy_val);
  }
  
}
