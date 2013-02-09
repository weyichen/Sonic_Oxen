int step = 0;
int text[10];

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (!step) {
    delay(2000);
    Serial.print("+++");
    delay(2000);
    Serial.println();
  }
  if (Serial.available() >= 3) {
    delay(1000);
    for (int i = 0; Serial.available() && i < 10; i++) {
      text[i] = Serial.read();
      Serial.write(text[i]);
      if (i && text[i] == 'K' && text[i - 1] == 'O') {
        step++;
        if (step == 1) {
          Serial.print("ATBD7");
        }
        else if (step == 2) {
          Serial.print("ATWR");
        }
      }
    }
  }
}
