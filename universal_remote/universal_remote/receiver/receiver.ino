#include <IRremoteESP8266.h>
#include <IRrecv.h>

// const int IR_PENERIMA = 15;  
// IRrecv irrecv(IR_PENERIMA);
// decode_results results;

// void setup() {
//   Serial.begin(9600);
//   irrecv.enableIRIn();
// }

// void loop() {
//   if (irrecv.decode(&results)) {
//     Serial.println("Code HEX :" );
//     Serial.println(results.value, HEX);
//     delay(1000);
//     irrecv.resume();
//   }
// }
const int ledPin = 2;   // LED indicator
const int IR_PIN = 15;  // Receiver HEX  

IRrecv irrecv(IR_PIN);  // Fucntion library 
decode_results results; // Conversi

void setup() {
  Serial.begin(9600);
  irrecv.enableIRIn();
  pinMode(ledPin, OUTPUT);
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.print("Received IR data: ");
    Serial.print(results.value, HEX);
    Serial.print(" (");
    Serial.print(results.decode_type);
    Serial.print(")");
    Serial.println();
    if (results.value == 0xFF52AD){
      digitalWrite(ledPin, HIGH);
    }
    else if (results.value == 0xFF7887){
      digitalWrite(ledPin, LOW);
    }
    delay(1000);
    irrecv.resume();
  }
}
