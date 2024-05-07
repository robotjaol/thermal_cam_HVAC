#include "LowPower.h"
#include <IRremote.h>

const int b1 = 2;
const int b2 = 4;
const int b3 = 5;
const int b4 = 6;
const int b5 = 7;
const int b6 = 8;
const int b7 = 9;
const int b8 = 10;
const int b9 = 11;
const int b10 = 12;

const unsigned long IR_CODES[] = {
  // Define your IR codes here for each button
  0x00000000, // Placeholder for button 1
  0x11111111, // Placeholder for button 2
  // Add more IR codes for other buttons if needed
};

IRsend irsend;

void setup(){
  pinMode(b1, INPUT);
  pinMode(b2, INPUT);
  pinMode(b3, INPUT);
  pinMode(b4, INPUT);
  pinMode(b5, INPUT);
  pinMode(b6, INPUT);
  pinMode(b7, INPUT);
  pinMode(b8, INPUT);
  pinMode(b9, INPUT);
  pinMode(b10, INPUT);
}

void loop(){
unsigned long currentCode = 0;

  if (digitalRead(b1) == HIGH) {
    currentCode = IR_CODES[0];
  } else if (digitalRead(b2) == HIGH) {
    currentCode = IR_CODES[1];
  } else if (digitalRead(b3) == HIGH) {
    currentCode = IR_CODES[2];
  } else if (digitalRead(b4) == HIGH) {
    currentCode = IR_CODES[3];
  } else if (digitalRead(b5) == HIGH) {
    currentCode = IR_CODES[4];
  } else if (digitalRead(b6) == HIGH) {
    currentCode = IR_CODES[5];
  } else if (digitalRead(b7) == HIGH) {
    currentCode = IR_CODES[6];
  } else if (digitalRead(b8) == HIGH) {
    currentCode = IR_CODES[7];
  } else if (digitalRead(b9) == HIGH) {
    currentCode = IR_CODES[8];
  } else if (digitalRead(b10) == HIGH) {
    currentCode = IR_CODES[9];
  }

    if (currentCode != 0) {
    irsend.sendNEC(currentCode, 32);
    delay(50); // Delay to avoid multiple triggers
  }
  // LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
}