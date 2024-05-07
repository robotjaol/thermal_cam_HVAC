#include <IRremote.h>

const int RECV_PIN = 8; // DATA IR MASUK PIN 8 
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup() {
  Serial.begin(9600);
  irrecv.enableIRIn(); // Function untuk running IR read
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.println(results.value, HEX);
    irrecv.resume(); // function menerima data
  }
}
