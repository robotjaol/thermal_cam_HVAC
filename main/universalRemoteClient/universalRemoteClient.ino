// MAIN PROGRAM IKI BUOOOSS
#include <SPI.h>
#include <Ethernet.h>
#include <IRremote.h>

//SETUP PIN IR COMMUNICATION
const int irTran = 4;  //IR TRANSMISSION PIN
const int irRecv = 13; //IR RECEIVE TO COLLECT HEX CODE

//SETUP BUTTON MODE
const int buttonRecv  = 27; //RECEIVE HEX CODE MODE
const int buttonTrans = 26; //TRANSMISSION HEX CODE MODE
const int buttonManual = 25; //MODE MANUAL UNIVERSAL REMOTE

//SETUP PIN W5500
#define SPI_MISO 19
#define SPI_MOSI 23
#define SPI_SCK 18
#define SPI_CS 5

//SETUP PIN INDIKATOR 
const int ledPin = 2;   //LED ESP32
const int ledBox = 12;  //LED BOX UNIVERSAL REMOTE
const int buzzer = 14;  //BUZZER BOX

//MODE
bool irReceiverMode = false;
bool irTransmitterMode = false;
bool manual = false;

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED }; // DEFAULT

// CEK DULU DI IFCONFIG
IPAddress ip(192, 168, 1, 177);    
IPAddress myDns(192, 168, 1, 1);
IPAddress gateway(192, 168, 1, 1);
IPAddress subnet(255, 255, 255, 0);

EthernetClient client;

//IR declaration
IRrecv irReceiver(irRecv);
IRsend irSender;

void setup() {
  Serial.begin(115200);  //SETTING BAUD BEBAS
  SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI, SPI_CS); // INPUT SEMUA PIN
  
  pinMode(SPI_CS, OUTPUT); //SETTING CS PIN
  digitalWrite(SPI_CS, HIGH); // TES FUNCTIONAL CS

  Ethernet.init(SPI_CS);
  Ethernet.begin(mac, ip, myDns, gateway, subnet);
  delay(1000);

  Serial.print("Alamat IP saya: ");
  Serial.println(Ethernet.localIP());

  if (Ethernet.localIP() == IPAddress(0, 0, 0, 0)) { // INDIKATOR GAGAL
    Serial.println("Gagal mengkonfigurasi Ethernet");
    while (true);
  }

  // LED PINMODE
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  connectToServer();

  // BUTTON PINMODE
  pinMode(buttonRecv, INPUT_PULLUP);
  pinMode(buttonTrans, INPUT_PULLUP);
  pinMode(buttonManual, INPUT_PULLUP);

  irReceiver.enableIRIn(); // ON mode receive IR
}

// MAIN PROGRAM
void loop() {
  // bool MODE_MANUAL = digitalRead(buttonManual);
  // if(MODE_MANUAL == HIGH){
  //   manualModeUniversalRemote();
  // }
  // else{
  //   MODE_AUTO();
  // }

  serverLed(); // TESTING CLIEN SERVER FUNCTION
  // receiveIR()  // UNCOMMENT UNTUK READ DATA IR HEX
  // connectToServer(); // ** MAIN PROGRAM **

}

//FUNCTION DEPLOYMENT IP > void setup, void serverLed
void connectToServer() { 
  Serial.println("Menghubungkan ke server...");
  if (client.connect(IPAddress(192, 168, 1, 100), 8899)) {
    Serial.println("Terhubung ke server");
    // transmitIR();
    blinkLed();
  } else {
    Serial.println("Gagal terhubung ke server");
  }
}

// FUNCTION TES TRANSMISI SIMPLE CONTROL LED > void loop
void serverLed(){
  if (client.connected()) {
    if (client.available()) {
      String message = client.readStringUntil('\n');
      Serial.println("Pesan dari server: " + message);
      if (message == "LED_ON") {
        blinkLed();       // INDIKATOR KALAU SUKSES BOSKU
      }
      client.println("LED_ON diterima");
    }
  } else {
    Serial.println("Terputus dari server");
    delay(1000);
    connectToServer();  // MENCOBA KONEK LAGI KALAU MASIH PUTUS SAMA SERVERNYA 
    for(int k = 0; k<10; k++){
      digitalWrite(ledPin, HIGH);
      delay(100);
      digitalWrite(ledPin, LOW);
      delay(100);
    }
  }
  delay(100);
}

// FUNCTION BLINK LED INDIKATOR > void loop, void serverLed
void blinkLed() {
  for (int i = 0; i < 10000; i++) {
    digitalWrite(ledPin, HIGH);
    delay(3000);
    digitalWrite(ledPin, LOW);
    delay(1000);
  }
}

//FUNCTION TRANSMISSION HEX CODE
void transmitIR() { //COBA AKSI NYA DENGAN BLINK LED
  if (client.connected()) {
    if (client.available()) {
      String message = client.readStringUntil('\n');
      Serial.println("Pesan dari server: " + message);
      if (message == "ON_AC1") {
        digitalWrite(ledPin, HIGH); 
        delay(1000);
        digitalWrite(ledPin,LOW);
        delay(1000);
        Serial.println(message + "\n");
      } 
      else if (message == "OFF_AC1") {
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        Serial.println(message + "\n");
      } 
      else if (message == "ON_AC2") {
        Serial.println(message + "\n");
        digitalWrite(ledPin, HIGH); 
        delay(2000);
        digitalWrite(ledPin,LOW);
        delay(2000);
        digitalWrite(ledPin, HIGH); 
        delay(2000);
        digitalWrite(ledPin,LOW);
        delay(2000);
        digitalWrite(ledPin, HIGH); 
        delay(2000);
        digitalWrite(ledPin,LOW);
        delay(2000);
      } 
      else if (message == "OFF_AC2") {
        Serial.println(message + "\n");
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
      } 
      else if (message == "PLUS") {
        Serial.println(message + "\n");
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
      } 
      else if (message == "MINUS") {
        Serial.println(message + "\n");
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
        digitalWrite(ledPin, HIGH); 
        delay(100);
        digitalWrite(ledPin,LOW);
        delay(100);
      } 
      else {
        Serial.println("Pesan tidak valid");
      }
    }
  } else {
    Serial.println("Koneksi ke server terputus");
    connectToServer();
    delay(100);
  }
}


// void transmitIR() { // ** AKSINYA PAKAI IR TRANSMIT REALL GAN **
//   if (client.connected()) {
//     if (client.available()) {
//       String message = client.readStringUntil('\n');
//       Serial.println("Pesan dari server: " + message);
      
//       // Memeriksa pesan dari server dan mengirimkan sinyal IR sesuai dengan pesan
//       if (message == "ON_AC1") {
//         irSender.sendNEC(0x12345678, 32); // Contoh pengiriman sinyal IR untuk "ON_AC1"
//       } else if (message == "OFF_AC1") {
//         irSender.sendNEC(0x87654321, 32); // Contoh pengiriman sinyal IR untuk "OFF_AC1"
//       } else if (message == "ON_AC2") {
//         irSender.sendNEC(0xABCD1234, 32); // Contoh pengiriman sinyal IR untuk "ON_AC2"
//       } else if (message == "OFF_AC2") {
//         irSender.sendNEC(0xDCBA4321, 32); // Contoh pengiriman sinyal IR untuk "OFF_AC2"
//       } else if (message == "PLUS") {
//         irSender.sendNEC(0x11111111, 32); // Contoh pengiriman sinyal IR untuk "PLUS"
//       } else if (message == "MINUS") {
//         irSender.sendNEC(0x22222222, 32); // Contoh pengiriman sinyal IR untuk "MINUS"
//       } else {
//         Serial.println("Pesan tidak valid");
//       }
//     }
//   } else {
//     Serial.println("Koneksi ke server terputus");
//     connectToServer();
//     delay(100);
//   }
// }

//FUNCTION RECEIVER HEX CODE
void receiveIR(){
  if (irReceiver.decode()) {
    Serial.print("Kode IR diterima: 0x");
    Serial.println(irReceiver.decodedIRData.command, HEX);
    irReceiver.resume();
  }
}










// -------------------------------------------------------------------------------
// ---------------- syntax uji coba -----------------------

// void manualModeUniversalRemote(){
//   bool buttonReceiverMode = digitalRead(buttonRecv);
//   bool buttonTransmitterMode = digitalRead(buttonTrans);

//   if(buttonReceiverMode == LOW){
//     irReceiverMode == true;
//     irTransmitterMode == false;
//   }
//   if (buttonTransmitterMode == LOW){
//     irReceiverMode == false;
//     irTransmitterMode == true;
//   }

//   if(irReceiverMode){
//     receiveIR();
//   }
//   if(irTransmitterMode){
//     transmitIR();
//   }
// }



// --------------------------------------------------------------
// TESTIMONIAL CODE
// #include <SPI.h>
// #include <Ethernet.h>

// #define SPI_MISO 19
// #define SPI_MOSI 23
// #define SPI_SCK 18
// #define SPI_CS 5

// byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED }; // DEFAULT

// // CEK DULU DI IFCONFIG
// IPAddress ip(192, 168, 1, 177);    
// IPAddress myDns(192, 168, 1, 1);
// IPAddress gateway(192, 168, 1, 1);
// IPAddress subnet(255, 255, 255, 0);

// EthernetClient client;
// const int ledPin = 2; // INDIKATOR DATA TRANSMISSION DARI SERVER

// void setup() {
//   Serial.begin(115200);  //SETTING BAUD BEBAS
//   SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI, SPI_CS); // INPUT SEMUA PIN
  
//   pinMode(SPI_CS, OUTPUT); //SETTING CS PIN
//   digitalWrite(SPI_CS, HIGH); // TES FUNCTIONAL CS

//   Ethernet.init(SPI_CS);
//   Ethernet.begin(mac, ip, myDns, gateway, subnet);
//   delay(1000);

//   Serial.print("Alamat IP saya: ");
//   Serial.println(Ethernet.localIP());

//   if (Ethernet.localIP() == IPAddress(0, 0, 0, 0)) { // INDIKATOR GAGAL
//     Serial.println("Gagal mengkonfigurasi Ethernet");
//     while (true);
//   }
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW); // LAMPU MATI JIKA GAGAL KONEK
//   connectToServer();
// }

// void loop() {
//   if (client.connected()) {
//     if (client.available()) {
//       String message = client.readStringUntil('\n');
//       Serial.println("Pesan dari server: " + message);
//       if (message == "LED_ON") {
//         blink_led();
//       }
//       client.println("Perintah LED_ON diterima");
//     }
//   } else {
//     Serial.println("Terputus dari server");
//     delay(1000);
//     connectToServer();
//   }
//   delay(100);
// }

// void connectToServer() {
//   Serial.println("Menghubungkan ke server...");
//   if (client.connect(IPAddress(192, 168, 1, 100), 8899)) {
//     Serial.println("Terhubung ke server");
//     blink_led();
//   } else {
//     Serial.println("Gagal terhubung ke server");
//   }
// }

// void blink_led() {
//   for (int i = 0; i < 10000; i++) {
//     digitalWrite(ledPin, HIGH);
//     delay(1000);
//     digitalWrite(ledPin, LOW);
//     delay(500);
//   }
// }

// -------------------------------------------------------------
// PROGRAM UNTUK DEBUG WATU TIMEOUT TCP

// #include <SPI.h>
// #include <Ethernet.h>

// #define SPI_MISO 19
// #define SPI_MOSI 23
// #define SPI_SCK 18
// #define SPI_CS 5

// byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// IPAddress ip(192, 168, 1, 177);
// IPAddress myDns(192, 168, 1, 1);
// IPAddress gateway(192, 168, 1, 1);
// IPAddress subnet(255, 255, 255, 0);

// EthernetClient client;
// const int ledPin = 2;

// unsigned long previousMillis = 0;
// const long interval = 5000;

// void setup() {
//   Serial.begin(115200);
//   SPI.begin(SPI_SCK, SPI_MISO, SPI_MOSI, SPI_CS);
//   pinMode(SPI_CS, OUTPUT);
//   digitalWrite(SPI_CS, HIGH);
//   Ethernet.init(SPI_CS);
//   Ethernet.begin(mac, ip, myDns, gateway, subnet);
//   delay(1000);
//   Serial.print("Alamat IP saya: ");
//   Serial.println(Ethernet.localIP());
//   if (Ethernet.localIP() == IPAddress(0, 0, 0, 0)) {
//     Serial.println("Gagal mengkonfigurasi Ethernet");
//     while (true);
//   }
//   pinMode(ledPin, OUTPUT);
//   digitalWrite(ledPin, LOW);
//   connectToServer();
// }

// void loop() {
//   unsigned long currentMillis = millis();
//   if (client.connected()) {
//     if (client.available()) {
//       String message = client.readStringUntil('\n');
//       Serial.println("Pesan dari server: " + message);
//       if (message == "LED_ON") {
//         blink_led();
//       }
//       client.println("Perintah LED_ON diterima");
//     }
//     if (currentMillis - previousMillis >= interval) {
//       previousMillis = currentMillis;
//       client.print("ping");
//     }
//   } else {
//     Serial.println("Terputus dari server");
//     delay(1000);
//     connectToServer();
//   }
//   delay(100);
// }

// void connectToServer() {
//   Serial.println("Menghubungkan ke server...");
//   if (client.connect(IPAddress(192, 168, 1, 100), 8899)) {
//     Serial.println("Terhubung ke server");
//     blink_led();
//   } else {
//     Serial.println("Gagal terhubung ke server");
//   }
// }

// void blink_led() {
//   for (int i = 0; i < 10; i++) {
//     digitalWrite(ledPin, HIGH);
//     delay(100);
//     digitalWrite(ledPin, LOW);
//     delay(100);
//   }
// }

