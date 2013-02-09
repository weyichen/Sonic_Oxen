/* Use to write new network ID code to Xbee.
Open up serial monitor after uploading code.  Use Xbee mode.
*/

void setup()
{
 Serial.begin(9600);
 Serial.flush();
}
boolean primed = false;

void loop()
{
 while(Serial.available())
 {
   Serial.read();
 }

 if(!primed)
   prime();

 delay(1000);      //Delay required for new settings to take effect
}
int l = 0;
void prime()
{
 Serial.print("attempt ");
 Serial.print(l);
 l=l++;
 delay(1500);      //Delay required before trying to enter command mode
 Serial.print("+++");

 delay(1500);
 Serial.print("ATID\r");       // Use this line to read network ID number
 Serial.print("ATID1111\r");   // Comment out to read network ID
 Serial.print("ATWR\r");       // Comment out to read network ID
 Serial.print("ATCN\r");       // Comment out to read network ID
 delay(1000);
 while(Serial.available())
 {
   primed = true;
   Serial.print(Serial.read());
//    Serial.read();
 }
}
