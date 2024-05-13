#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 177); // ESP32/arduino IP

IPAddress serverIP(192, 168, 1, 100); // PC IP
int serverPort = 1234; //PORT PC

EthernetClient client;

void setup() {
  Ethernet.begin(mac, ip);
  Serial.begin(9600);

  // Delay ethernet
  delay(1000);
  Serial.println("Ethernet ready");

  // Connect to the server
  if (client.connect(serverIP, serverPort)) {
    Serial.println("Connected to server");
  } else {
    Serial.println("Failed to connect to server");
  }
}

void loop() {
  if (client.connected()) {
    client.println("hello world");
    client.flush(); // buffer is empty
    Serial.println("Data sent to server");
  } else {
    Serial.println("Connection lost");
  }
  delay(2000); //Transmit setiap 2 detik
}
