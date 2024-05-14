#include <Ethernet.h>
#include <SPI.h>

// Sesuaikan dengan MAC address modul Anda
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// Setting IP server Python laptop
IPAddress server(192,168,1,100); // Sesuaikan dengan IP laptop 
const uint16_t server_port = 12345; // Samakan dengan port server.py

EthernetClient client;

const int ledPin = 2;

void setup() {
  // Set LED pin sebagai output
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Matikan LED pada awalnya

  // Mulai komunikasi serial untuk debugging
  Serial.begin(115200);

  // Memulai Ethernet dan mendapatkan IP dari DHCP
  if (Ethernet.begin(mac) == 0) {
    Serial.println("Failed to configure Ethernet using DHCP");
    // Berikan IP address statis jika DHCP gagal
    Ethernet.begin(mac, IPAddress(192, 168, 1, 177)); // Sesuaikan dengan jaringan Anda
  }

  // Beri waktu untuk memulai koneksi Ethernet
  delay(1000);
  Serial.println("Connecting to server...");

  // Kondisi state ketika connect ke server
  if (client.connect(server, server_port)) {
    Serial.println("Connected to server");
    client.println("Hello, server"); // Mengirim pesan ke server
  } else {
    Serial.println("Connection to server failed");
  }
}

void loop() {
  if (client.connected()) {
    if (client.available()) {
      String message = client.readStringUntil('\n');
      Serial.println("Message dari server adalah: " + message);

      // Berikan indikator pada hardware
      blink_led();
    }
  } else {
    // Jika kondisi sudah connect tapi tiba-tiba sinyal terputus
    client.stop();
    Serial.println("Disconnected from server");
    // Menunggu koneksi kembali dalam 1 detik sebelum mencoba lagi
    delay(1000);
    if (client.connect(server, server_port)) {
      Serial.println("Reconnected to server");
    } else {
      Serial.println("Reconnection to server failed");
      digitalWrite(ledPin, HIGH);
    }
  }
}

// Function indikator hardware
void blink_led() {
  digitalWrite(ledPin, HIGH); 
  delay(500);
  digitalWrite(ledPin, LOW);  
  delay(500);
}
