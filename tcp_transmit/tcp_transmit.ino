#include <Ethernet2.h>
#include <SPI.h>

// Define the MAC address and IP address of your Arduino
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 177); // Change to your Arduino's IP address

// Define the IP address and port of your mini PC
IPAddress serverIP(192, 168, 1, 100); // Change to your mini PC's IP address
int serverPort = 1234; // Change to the port number your mini PC is listening on

EthernetClient client;

void setup() {
  // Start the Ethernet connection
  Ethernet.begin(mac, ip);

  // Initialize serial communication for debugging
  Serial.begin(9600);

  // Wait for Ethernet to be ready
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
  // Send data to the server
  if (client.connected()) {
    client.println("hello world");
    client.flush(); // Flush the buffer
    Serial.println("Data sent to server");
  } else {
    Serial.println("Connection lost");
  }

  // Wait for 2 seconds
  delay(2000);
}
