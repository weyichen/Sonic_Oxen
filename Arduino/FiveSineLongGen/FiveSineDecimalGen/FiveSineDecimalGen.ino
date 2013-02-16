long data[5];
double r = 0.;

void setup() {
 // initialize serial communications at 9600 bps:
 Serial.begin(115200);
}

void loop() {
 r=r+0.1;
 long amp = 0;
 
 for (int i=0; i<5; i++){
   amp = amp + 200000;
  data[i] = long(amp*sin(r));
 }
 
 byte byte1, byte2, byte3, byte4;
 
 for (int i=0; i<5; i++){
  byte1 = byte(data[i] >> 24);
  byte2 = byte((data[i] >> 16) & 255);
  byte3 = byte((data[i] >> 8) & 255);
  byte4 = byte(data[i] & 255);
  
  Serial.write(byte1);
  Serial.write(byte2);
  Serial.write(byte3);
  Serial.write(byte4);
  
//  Serial.print("long ");
//  Serial.println(data[i]);
//  Serial.print("byte1 ");
//  Serial.println(byte1);
//  Serial.print("byte2 ");
//  Serial.println(byte2);
//  Serial.print("byte3 ");
//  Serial.println(byte3);
//  Serial.print("byte4 ");
//  Serial.println(byte4);
 }

 // wait 2 milliseconds before the next loop
 delayMicroseconds(200);                     
}
