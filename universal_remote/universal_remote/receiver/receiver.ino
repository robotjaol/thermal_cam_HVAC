
#include <IRremoteESP8266.h>
#include <IRrecv.h>

IRrecv irrecv(15);
decode_results results;

void setup(){
  irrecv.enableIRIn();
  Serial.begin(115200);
}

void loop(){
  if(irrecv.decode(&results)){
    Serial.println(results.value, HEX);
    delay(1000);
    irrecv.resume();
  }
}