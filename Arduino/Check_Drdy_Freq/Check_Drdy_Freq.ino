// include the SPI library:
#include <SPI.h>

long current;
long samples;
long intervals;
void setup() {
  
  Serial.begin(57600);
  
  // initialize SPI
  SPI.begin(); // SCK, MOSI, SS to OUTPUT, SCK, MOSI to LOW, SS to HIGH
  SPI.setDataMode(SPI_MODE1); 
  SPI.setBitOrder(MSBFIRST);
  SPI.setClockDivider(SPI_CLOCK_DIV16);
  
  digitalWrite(7, HIGH);
  
  long current = millis();
  intervals = 0;
  long samples = 0;
  attachInterrupt( 6, update, FALLING);
}

void loop() {
  SPI.transfer(0);
}

void update() {
  long next = millis();
  Serial.println(next - current);
  current = next;
}


