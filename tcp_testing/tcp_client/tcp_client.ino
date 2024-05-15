// #include <Ethernet.h>
// #include <SPI.h>

// // Sesuaikan dengan MAC address modul Anda
// byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// // Setting IP server Python laptop
// IPAddress server(192,168,1,100); // Sesuaikan dengan IP laptop 
// const uint16_t server_port = 12345; // Samakan dengan port server.py

// EthernetClient client;

// const int ledPin = 2;

// void setup() {
//   // Set LED pin sebagai output
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW); // Matikan LED pada awalnya

//   // Mulai komunikasi serial untuk debugging
//   Serial.begin(115200);

//   // Memulai Ethernet dan mendapatkan IP dari DHCP
//   if (Ethernet.begin(mac) == 0) {
//     Serial.println("Failed to configure Ethernet using DHCP");
//     // Berikan IP address statis jika DHCP gagal
//     Ethernet.begin(mac, IPAddress(192, 168, 1, 177)); // Sesuaikan dengan jaringan Anda
//   }

//   // Beri waktu untuk memulai koneksi Ethernet
//   delay(1000);
//   Serial.println("Connecting to server...");

//   // Kondisi state ketika connect ke server
//   if (client.connect(server, server_port)) {
//     Serial.println("Connected to server");
//     client.println("Hello, server"); // Mengirim pesan ke server
//   } else {
//     Serial.println("Connection to server failed");
//   }
// }

// void loop() {
//   if (client.connected()) {
//     if (client.available()) {
//       String message = client.readStringUntil('\n');
//       Serial.println("Message dari server adalah: " + message);

//       // Berikan indikator pada hardware
//       blink_led();
//     }
//   } else {
//     // Jika kondisi sudah connect tapi tiba-tiba sinyal terputus
//     client.stop();
//     Serial.println("Disconnected from server");
//     // Menunggu koneksi kembali dalam 1 detik sebelum mencoba lagi
//     delay(1000);
//     if (client.connect(server, server_port)) {
//       Serial.println("Reconnected to server");
//     } else {
//       Serial.println("Reconnection to server failed");
//       digitalWrite(ledPin, HIGH);
//     }
//   }
// }

// // Function indikator hardware
// void blink_led() {
//   digitalWrite(ledPin, HIGH); 
//   delay(500);
//   digitalWrite(ledPin, LOW);  
//   delay(500);
// }



// code debug 
// #include <Ethernet.h>
// #include <SPI.h>

// // Sesuaikan dengan MAC address modul Anda
// byte mac[] = { 0x00, 0x68, 0xEB, 0x3C, 0xB4, 0x2C };

// // Setting IP server Python laptop
// IPAddress server(192, 168, 1, 100); // Sesuaikan dengan IP laptop
// const uint16_t server_port = 12345; // Samakan dengan port server.py

// EthernetClient client;

// const int ledPin = 2;

// void setup() {
//   // Set LED pin sebagai output
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW); // Matikan LED pada awalnya

//   // Mulai komunikasi serial untuk debugging
//   Serial.begin(115200);

//   // Memulai Ethernet dan mendapatkan IP dari DHCP
//   if (Ethernet.begin(mac) == 0) {
//     Serial.println("Failed to configure Ethernet using DHCP");
//     // Berikan IP address statis jika DHCP gagal
//     Ethernet.begin(mac, IPAddress(192, 168, 1, 177)); // Sesuaikan dengan jaringan Anda
//   }

//   // Beri waktu untuk memulai koneksi Ethernet
//   delay(1000);
//   Serial.println("Connecting to server...");

//   // Kondisi state ketika connect ke server
//   if (client.connect(server, server_port)) {
//     Serial.println("Connected to server");
//     client.println("Hello, server"); // Mengirim pesan ke server
//   } else {
//     Serial.println("Connection to server failed");
//   }
// }

// void loop() {
//   if (client.connected()) {
//     if (client.available()) {
//       String message = client.readStringUntil('\n');
//       Serial.println("Message dari server adalah: " + message);

//       // Berikan indikator pada hardware
//       blink_led();
//     }
//   } else {
//     // Jika kondisi sudah connect tapi tiba-tiba sinyal terputus
//     client.stop();
//     Serial.println("Disconnected from server");
//     // Menunggu koneksi kembali dalam 1 detik sebelum mencoba lagi
//     delay(1000);
//     if (client.connect(server, server_port)) {
//       Serial.println("Reconnected to server");
//     } else {
//       Serial.println("Reconnection to server failed");
//       digitalWrite(ledPin, HIGH);
//     }
//   }
// }

// // Function indikator hardware
// void blink_led() {
//   digitalWrite(ledPin, HIGH); 
//   delay(500);
//   digitalWrite(ledPin, LOW);  
//   delay(500);
// }


// #include <Ethernet.h>
// #include <SPI.h>

// // Sesuaikan dengan MAC address modul Anda
// byte mac[] = { 0x00, 0x68, 0xEB, 0x3C, 0xB4, 0x2C };

// // Setting IP server Python laptop
// IPAddress server(192, 168, 1, 100); // Alamat IP server
// const uint16_t server_port = 12345; // Samakan dengan port server.py

// EthernetClient client;

// const int ledPin = 2;

// void setup() {
//   // Set LED pin sebagai output
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW); // Matikan LED pada awalnya

//   // Mulai komunikasi serial untuk debugging
//   Serial.begin(115200);

//   // Memulai Ethernet dan mendapatkan IP dari DHCP
//   if (Ethernet.begin(mac) == 0) {
//     Serial.println("Failed to configure Ethernet using DHCP");
//     // Berikan IP address statis jika DHCP gagal
//     Ethernet.begin(mac, IPAddress(192, 168, 1, 177)); // Sesuaikan dengan jaringan Anda
//   }

//   // Beri waktu untuk memulai koneksi Ethernet
//   delay(1000);
//   Serial.println("Connecting to server...");

//   // Kondisi state ketika connect ke server
//   if (client.connect(server, server_port)) {
//     Serial.println("Connected to server");
//     client.println("Hello, server"); // Mengirim pesan ke server
//   } else {
//     Serial.println("Connection to server failed");
//   }
// }

// void loop() {
//   if (client.connected()) {
//     if (client.available()) {
//       String message = client.readStringUntil('\n');
//       Serial.println("Message dari server adalah: " + message);

//       // Berikan indikator pada hardware
//       blink_led();
//     }
//   } else {
//     // Jika kondisi sudah connect tapi tiba-tiba sinyal terputus
//     client.stop();
//     Serial.println("Disconnected from server");
//     // Menunggu koneksi kembali dalam 1 detik sebelum mencoba lagi
//     delay(1000);
//     if (client.connect(server, server_port)) {
//       Serial.println("Reconnected to server");
//     } else {
//       Serial.println("Reconnection to server failed");
//       digitalWrite(ledPin, HIGH);
//     }
//   }
// }

// // Function indikator hardware
// void blink_led() {
//   digitalWrite(ledPin, HIGH); 
//   delay(500);
//   digitalWrite(ledPin, LOW);  
//   delay(500);
// }


// SIMPLE CODE TO TESTING DHCP

// #include <SPI.h>
// #include <Ethernet.h>

// byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// void setup() {
//   Serial.begin(115200);
//   while (!Serial) {
//     ; // wait for serial port to connect. Needed for native USB port only
//   }

//   // start the Ethernet connection:
//   Serial.println("Trying to get an IP address using DHCP");

//   // start the Ethernet connection:
//   if (Ethernet.begin(mac) == 0) {
//     Serial.println("Failed to configure Ethernet using DHCP");
//     // no point in carrying on, so do nothing forevermore:
//     while (true) {
//       delay(1);
//     }
//   }
//   // print your local IP address:
//   Serial.print("My IP address: ");
//   Serial.println(Ethernet.localIP());
// }

// void loop() {
//   // do nothing
// }

// #include <Ethernet.h>
// #include <SPI.h>

// // Define MAC address for your ESP32 Ethernet module
// byte mac[] = { 0x00, 0x68, 0xEB, 0x3C, 0xB4, 0x2C };

// // Static IP configuration
// IPAddress ip(192, 168, 1, 177); // Static IP address for ESP32 (ensure it's within your network range and not conflicting with other devices)
// IPAddress gateway(192, 168, 1, 1); // Router's IP address
// IPAddress subnet(255, 255, 255, 0); // Subnet mask

// // Server IP and port
// IPAddress server(192, 168, 1, 100); // Server IP address
// const uint16_t server_port = 12345; // Server port

// EthernetClient client;

// const int ledPin = 2;

// void setup() {
//   // Set LED pin as output
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW); // Turn off LED initially

//   // Start serial communication for debugging
//   Serial.begin(115200);

//   // Start Ethernet with static IP
//   Ethernet.begin(mac, ip, gateway, subnet);

//   // Give time for Ethernet to initialize
//   delay(1000);

//   // Print assigned IP address
//   Serial.print("Assigned IP: ");
//   Serial.println(Ethernet.localIP());

//   Serial.println("Connecting to server...");

//   // Attempt to connect to server
//   if (client.connect(server, server_port)) {
//     Serial.println("Connected to server");
//     client.println("Hello, server"); // Send message to server
//   } else {
//     Serial.println("Connection to server failed");
//   }
// }

// void loop() {
//   if (client.connected()) {
//     if (client.available()) {
//       String message = client.readStringUntil('\n');
//       Serial.println("Message from server: " + message);

//       // Indicate successful communication
//       blink_led();
//     }
//   } else {
//     // If connection is lost, stop client and retry
//     client.stop();
//     Serial.println("Disconnected from server");
//     delay(1000);
//     if (client.connect(server, server_port)) {
//       Serial.println("Reconnected to server");
//     } else {
//       Serial.println("Reconnection to server failed");
//       digitalWrite(ledPin, HIGH); // Turn on LED to indicate failure
//     }
//   }
// }

// // Function to blink LED
// void blink_led() {
//   digitalWrite(ledPin, HIGH);
//   delay(500);
//   digitalWrite(ledPin, LOW);
//   delay(500);
// }

#include <Ethernet.h>
#include <SPI.h>

// Sesuaikan dengan MAC address modul Anda
byte mac[] = { 0x00, 0x68, 0xEB, 0x3C, 0xB4, 0x2C };

// Setting IP server Python laptop
IPAddress ip(192, 168, 1, 177); // Static IP address for the ESP32
IPAddress gateway(192, 168, 1, 1); // router's IP address
IPAddress subnet(255, 255, 255, 0); // Subnet mask

const IPAddress server(192, 168, 1, 100); // IP of your server
const uint16_t server_port = 12345; // Port of your server

EthernetClient client;

const int ledPin = 2;

void setup() {
  // Set LED pin as output
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Turn off LED initially

  // Start serial communication for debugging
  Serial.begin(115200);

  // Start Ethernet connection with static IP
  Ethernet.begin(mac, ip, gateway, gateway, subnet);

  // Print the assigned IP address
  Serial.print("Assigned IP: ");
  Serial.println(Ethernet.localIP());

  // Give time for Ethernet to initialize
  delay(1000);
  Serial.println("Connecting to server...");

  // Try to connect to the server
  if (client.connect(server, server_port)) {
    Serial.println("Connected to server");
    client.println("Hello, server"); // Send message to server
  } else {
    Serial.println("Connection to server failed");
  }
}

void loop() {
  if (client.connected()) {
    if (client.available()) {
      String message = client.readStringUntil('\n');
      Serial.println("Message from server: " + message);

      // Indicate on hardware
      blink_led();
    }
  } else {
    // If the connection was established but then lost
    client.stop();
    Serial.println("Disconnected from server");
    // Wait 1 second before trying to reconnect
    delay(1000);
    if (client.connect(server, server_port)) {
      Serial.println("Reconnected to server");
    } else {
      Serial.println("Reconnection to server failed");
      digitalWrite(ledPin, HIGH);
    }
  }
}

// Function to blink the LED
void blink_led() {
  digitalWrite(ledPin, HIGH); 
  delay(500);
  digitalWrite(ledPin, LOW);  
  delay(500);
}





