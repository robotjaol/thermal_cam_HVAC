// SPI DEBUG CLIENT BISA MENERIMA DATA
// #include <SPI.h>
// #include <Ethernet.h>

// // SPI pin definitions for ESP32
// #define SPI_MISO 19
// #define SPI_MOSI 23
// #define SPI_SCK 18
// #define SPI_CS 5

// // MAC address for W5500
// byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// // Network settings
// IPAddress ip(192, 168, 1, 177); // Static IP for the ESP32
// IPAddress myDns(192, 168, 1, 1); // DNS server IP
// IPAddress gateway(192, 168, 1, 1); // Gateway IP
// IPAddress subnet(255, 255, 255, 0); // Subnet mask

// EthernetClient client;
// const int ledPin = 2; // Pin for the LED

// void setup() {
//   // Initialize serial communication for debugging
//   Serial.begin(115200);

//   // Initialize SPI
//   SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI, SPI_CS);
//   pinMode(SPI_CS, OUTPUT);
//   digitalWrite(SPI_CS, HIGH);

//   // Initialize Ethernet with static IP configuration
//   Ethernet.init(SPI_CS);
//   Ethernet.begin(mac, ip, myDns, gateway, subnet);

//   // Allow time for the Ethernet hardware to initialize
//   delay(1000);

//   // Check if the Ethernet module obtained the IP address correctly
//   Serial.print("My IP address: ");
//   Serial.println(Ethernet.localIP());

//   if (Ethernet.localIP() == IPAddress(0, 0, 0, 0)) {
//     Serial.println("Failed to configure Ethernet");
//     while (true); // Halt the program
//   }

//   // Set the LED pin as output
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW); // Turn off LED initially

//   // Attempt to connect to the server
//   Serial.println("Connecting to server...");
//   if (client.connect(IPAddress(192, 168, 1, 100), 8888)) {
//     Serial.println("Connected to server");
//     client.println("Hello, server"); // Send a message to the server
//   } else {
//     Serial.println("Connection to server failed");
//   }
// }

// void loop() {
//   if (client.connected()) {
//     if (client.available()) {
//       String message = client.readStringUntil('\n');
//       Serial.println("Message from server: " + message);

//       if (message == "LED_ON") {
//         blink_led();
//       }
//     }
//   } else {
//     client.stop();
//     Serial.println("Disconnected from server");
//     delay(1000);
//     if (client.connect(IPAddress(192, 168, 1, 100), 8888)) {
//       Serial.println("Reconnected to server");
//     } else {
//       Serial.println("Reconnection to server failed");
//       digitalWrite(ledPin, HIGH); // Turn on LED to indicate error
//     }
//   }
// }

// void blink_led() {
//   for (int i = 0; i < 10; i++) {
//     digitalWrite(ledPin, HIGH);
//     delay(500);
//     digitalWrite(ledPin, LOW);
//     delay(500);
//   }
// }

// LOOPING MENERIMA DATA

#include <SPI.h>
#include <Ethernet.h>

// Definisi pin SPI untuk ESP32
#define SPI_MISO 19
#define SPI_MOSI 23
#define SPI_SCK 18
#define SPI_CS 5

// Alamat MAC untuk W5500
byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// Pengaturan jaringan
IPAddress ip(192, 168, 1, 177); // IP statis untuk ESP32
IPAddress myDns(192, 168, 1, 1); // IP server DNS
IPAddress gateway(192, 168, 1, 1); // IP gateway
IPAddress subnet(255, 255, 255, 0); // Subnet mask

EthernetClient client;
const int ledPin = 2; // Pin untuk LED

void setup() {
  // Inisialisasi komunikasi serial untuk debugging
  Serial.begin(115200);

  // Inisialisasi SPI
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI, SPI_CS);
  pinMode(SPI_CS, OUTPUT);
  digitalWrite(SPI_CS, HIGH);

  // Inisialisasi Ethernet dengan konfigurasi IP statis
  Ethernet.init(SPI_CS);
  Ethernet.begin(mac, ip, myDns, gateway, subnet);

  // Beri waktu untuk perangkat keras Ethernet menginisialisasi
  delay(1000);

  // Periksa jika modul Ethernet telah memperoleh alamat IP dengan benar
  Serial.print("Alamat IP saya: ");
  Serial.println(Ethernet.localIP());

  if (Ethernet.localIP() == IPAddress(0, 0, 0, 0)) {
    Serial.println("Gagal mengkonfigurasi Ethernet");
    while (true); // Berhenti program
  }

  // Set pin LED sebagai output
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Matikan LED pada awalnya

  // Mencoba untuk terhubung ke server
  connectToServer();
}

void loop() {
  if (client.connected()) {
    if (client.available()) {
      String message = client.readStringUntil('\n');
      Serial.println("Pesan dari server: " + message);

      if (message == "LED_ON") {
        blink_led();
      }

      // Mengirim respons kembali ke server (opsional)
      client.println("Perintah LED_ON diterima");
    }
  } else {
    // Mencoba untuk menyambung kembali jika koneksi terputus
    Serial.println("Terputus dari server");
    delay(1000);
    connectToServer();
  }

  // Menambahkan sedikit penundaan untuk menghindari penutupan server
  delay(100);
}

void connectToServer() {
  Serial.println("Menghubungkan ke server...");
  if (client.connect(IPAddress(192, 168, 1, 100), 12345)) {
    Serial.println("Terhubung ke server");
    blink_led();
  } else {
    Serial.println("Gagal terhubung ke server");
  }
}

void blink_led() {
  for (int i = 0; i < 10000; i++) {
    digitalWrite(ledPin, HIGH);
    delay(1000);
    digitalWrite(ledPin, LOW);
    delay(500);
  }
}


// #include <Ethernet.h>
// #include <SPI.h>

// // Sesuaikan dengan MAC address modul Anda
// byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// // Setting IP server Python laptop
// IPAddress server(192, 168, 1, 100); // Sesuaikan dengan IP laptop 
// const uint16_t server_port = 8888; // Samakan dengan port server.py

// // Static IP address configuration
// IPAddress ip(192, 168, 1, 177); // Sesuaikan dengan jaringan Anda
// IPAddress myDns(192, 168, 1, 1); // DNS server IP (optional)

// EthernetClient client;

// const int ledPin = 2;

// void setup() {
//   // Set LED pin sebagai output
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW); // Matikan LED pada awalnya

//   // Mulai komunikasi serial untuk debugging
//   Serial.begin(115200);

//   // Memulai Ethernet dengan IP statis
//   Ethernet.begin(mac, ip, myDns);
//   Serial.print("My IP address: ");
//   Serial.println(Ethernet.localIP());

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

//       if (message == "LED_ON") {
//         blink_led();
//       }
//     }
//   } else {
//     // Jika kondisi sudah connect tapi tiba-tiba sinyal terputus
//     client.stop();
//     Serial.println("Disconnected from server");
//     blink_led();
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
//   for(int i = 0; i < 10; i++){
//     digitalWrite(ledPin, HIGH); 
//     delay(500);
//     digitalWrite(ledPin, LOW);  
//     delay(500);
//   }
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

// #include <Ethernet.h>
// #include <SPI.h>

// // Sesuaikan dengan MAC address modul Anda
// byte mac[] = { 0x00, 0x68, 0xEB, 0x3C, 0xB4, 0x2C };

// // Setting IP server Python laptop
// IPAddress ip(192, 168, 1, 177); // Static IP address for the ESP32
// IPAddress gateway(192, 168, 1, 1); // router's IP address
// IPAddress subnet(255, 255, 255, 0); // Subnet mask

// const IPAddress server(192, 168, 1, 100); // IP of your server
// const uint16_t server_port = 12345; // Port of your server

// EthernetClient client;

// const int ledPin = 2;

// void setup() {
//   // Set LED pin as output
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW); // Turn off LED initially

//   // Start serial communication for debugging
//   Serial.begin(115200);

//   // Start Ethernet connection with static IP
//   Ethernet.begin(mac, ip, gateway, gateway, subnet);

//   // Print the assigned IP address
//   Serial.print("Assigned IP: ");
//   Serial.println(Ethernet.localIP());

//   // Give time for Ethernet to initialize
//   delay(1000);
//   Serial.println("Connecting to server...");

//   // Try to connect to the server
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

//       // Indicate on hardware
//       blink_led();
//     }
//   } else {
//     // If the connection was established but then lost
//     client.stop();
//     Serial.println("Disconnected from server");
//     // Wait 1 second before trying to reconnect
//     delay(1000);
//     if (client.connect(server, server_port)) {
//       Serial.println("Reconnected to server");
//     } else {
//       Serial.println("Reconnection to server failed");
//       digitalWrite(ledPin, HIGH);
//     }
//   }
// }

// // Function to blink the LED
// void blink_led() {
//   digitalWrite(ledPin, HIGH); 
//   delay(500);
//   digitalWrite(ledPin, LOW);  
//   delay(500);
// }


// #include <SPI.h>
// #include <Ethernet.h> // Ensure you are using the correct Ethernet library

// // MAC address for Ethernet shield
// byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
// IPAddress ip(192, 168, 1, 177); // Static IP address
// IPAddress gateway(192, 168, 1, 1); // Gateway IP address
// IPAddress subnet(255, 255, 255, 0); // Subnet mask

// EthernetServer server(8888);

// void setup() {
//   Serial.begin(115200);
//   Ethernet.init(5); // CS pin for W5500 module
  
//   // Start Ethernet connection with static IP
//   Ethernet.begin(mac, ip, gateway, subnet);
  
//   // Start the server
//   server.begin();
  
//   Serial.println("Server started.");
//   Serial.print("IP Address: ");
//   Serial.println(Ethernet.localIP());
// }

// void loop() {
//   EthernetClient client = server.available();

//   if (client) {
//     Serial.println("New client connected.");
//     while (client.connected()) {
//       if (client.available()) {
//         String command = client.readStringUntil('\n');
//         Serial.println("Received command: " + command);
//         // Process received command here
//       }
//     }
//     client.stop();
//     Serial.println("Client disconnected.");
//   }
// }


