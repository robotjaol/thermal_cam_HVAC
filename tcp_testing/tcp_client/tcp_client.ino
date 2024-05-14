#include <Ethernet.h>
#include <SPI.h>

byte mac[] =  { 0xDE, 0xAD, 0xBE, 0xEF, 0xED}; //sesuaikan dengan Mac addres modul anda

//setting IP server Python laptop
IPAddress server(192,168,1,10);     //sesuaikan dengan IP laptop
const uin16_t server_port = 12345;  //samakan dengen port server.py

EthernetClient client;

void setup(){
  //start serial communication 
  Serial.begin(115200);
  if (Ethernet.begin(mac) == 0){
    Serial.println("Failed to connect DHCP");         //indikator gagal connect
    Ethernet.begin(mac, IPAddress(192,168,1,10));     // Input manual
  }

  delay(1000);
  Serial.println("Connecting to server ... ");

  //condition state ketika connect ke server
  if(client.connect(server, server_port)){
    Serial.println("Connect ke sever Lur");
    Serial.println("Halo dunia");
  }
  else{
    Serial.println("Alamat sudah ke lock, tapi belum bisa connect lur");
  }
}

void loop(){
  if(client.connected()){
    if(client.avaible()){
      String message = client.readStringUntil('\n');
      Serial.println("Message dari server adalah : " + message);
    }
  }else{
    // jika kondisi udah connect tapi tiba tiba sinyal nge loss
    client.stop();
    Serial.println("Disconnected dari sever lur");
    while(true);
  }

}
