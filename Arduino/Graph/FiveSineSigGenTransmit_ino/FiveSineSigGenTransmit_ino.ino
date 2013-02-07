float x = 0.;
float y = 0.;
float z = 0.;
float a = 0.;
float b = 0.;
float r = 0.;

void setup() {
 // initialize serial communications at 9600 bps:
 Serial.begin(9600); 
}

void loop() {
 r=r+0.1;
 x=20*sin(r)+100;
 y=40*sin(r)+100;
 z=60*sin(r)+100;
 a=80*sin(r)+100;
 b=100*sin(r)+100;
  
 Serial.write(int(x));
 Serial.write(int(y));
 Serial.write(int(z));
 Serial.write(int(a));
 Serial.write(int(b));

 // wait 2 milliseconds before the next loop
 delayMicroseconds(50);                     
}
