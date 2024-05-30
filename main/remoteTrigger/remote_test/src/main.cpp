#include <Arduino.h>

const int buttonMINUS = 26; // MINUS THERMAL
const int buttonPLUS = 25;  // PLUS THERMAL

void setup() {
  int i ;
  for (i = 0; i < 5; i++)
  {
    pinMode(buttonPLUS, OUTPUT);
    digitalWrite(buttonPLUS, HIGH);
    delay(1000);
    digitalWrite(buttonPLUS, LOW);
    delay(500);
  }

  if (i == 5){
    pinMode(buttonPLUS, INPUT);
    pinMode(buttonMINUS, OUTPUT);
    for (int x = 0; x < 5; x++)
    {
    digitalWrite(buttonMINUS, HIGH);
    delay(1000);
    digitalWrite(buttonMINUS, LOW);
    delay(500);
    }
    pinMode(buttonPLUS, INPUT);
    pinMode(buttonMINUS, INPUT);
  }
}

void loop() {
  // digitalWrite(buttonMINUS, HIGH);
  // delay(2000);
  // digitalWrite(buttonMINUS, LOW);
  // delay(500);
  // digitalWrite(buttonMINUS, HIGH);
  // delay(2000);
  // digitalWrite(buttonMINUS, LOW);
  // delay(500);
  // digitalWrite(buttonMINUS, HIGH);
  // delay(2000);
  // digitalWrite(buttonMINUS, LOW);
  // delay(500);
  // digitalWrite(buttonMINUS, HIGH);
  // delay(2000);
  // digitalWrite(buttonMINUS, LOW);
  // delay(500);
  // digitalWrite(buttonMINUS, HIGH);
  // delay(2000);
  // digitalWrite(buttonMINUS, LOW);
  // delay(500);
}
