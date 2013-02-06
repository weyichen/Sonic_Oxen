const int LED = 13;
int start = 0;
int text[10];

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  digitalWrite(LED,LOW);
}

void loop() {
  if (!start) {
    delay(1000);
    start++;
    Serial.print("+++");
  }
  if (Serial.available() >= 3) {
    digitalWrite(LED, HIGH);
    delay(2000);
    digitalWrite(LED, LOW);
    for (int i = 0; Serial.available() && i < 10; i++) {
      text[i] = Serial.read();
      Serial.write(text[i]);
    }
    Serial.print("ATBD 7");
  }
}
