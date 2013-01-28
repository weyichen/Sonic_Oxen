// inslude the SPI library:
#include <SPI.h>

// set pin 10 as the slave select for the digital pot:
const int CS = 10;
const int out = 11;
const int in = 12;
const int clock = 13;
int fst = 0;
int snd = 0;

void setup() {
 // initialize serial communications at 9600 bps:
 Serial.begin(115200); 
 
 // set the slaveSelectPin as an output:
 pinMode (CS, OUTPUT);
 pinMode (out, OUTPUT);
 pinMode (in, INPUT);
 pinMode (clock, OUTPUT);
 
 // initialize SPI:
 SPI.begin();
 SPI.setBitOrder(MSBFIRST);
 SPI.setClockDivider(SPI_CLOCK_DIV32);
 digitalWrite(CS, HIGH);
}

void loop() {
 
  
 digitalWrite(CS, LOW);
 fst = SPI.transfer(120);
 snd = SPI.transfer(0);
 Serial.println(((fst & 7) << 8) | snd);
 digitalWrite(CS, HIGH);
 
 delayMicroseconds(20);
}
