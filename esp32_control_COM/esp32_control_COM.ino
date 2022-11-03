
#include <WiFi.h>


#include <EmonLib.h>

#include "WiFi.h" // Enables the ESP32 to connect to the local network (via WiFi)



#include <PubSubClient.h>





EnergyMonitor emon1;
//Inserire la tensione della vostra rete elettrica
int rede = 230.0; // Italia 230V in alcuni paesi 110V 
int pin_sct = 14;

// Code for the ESP32



// WiFi
const char* ssid = "BEN_WIFI";                 // Your personal network SSID
const char* wifi_password = "bernardo"; // Your personal network password

// MQTT
const char* mqtt_server = "192.168.1.90";  // IP of the MQTT broker
const char* humidity_topic = "home/livingroom/humidity";
const char* temperature_topic = "home/livingroom/temperature";

const char* mqtt_username = "torre01"; // MQTT username
const char* mqtt_password = "torre"; // MQTT password
const char* clientID = "vedetta"; // MQTT client ID

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
// 1883 is the listener port for the Broker
PubSubClient client(mqtt_server, 1883, wifiClient); 


// Custom function to connet to the MQTT broker via WiFi
void connect_MQTT(){
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to the WiFi
  WiFi.begin(ssid, wifi_password);
  

  // Wait until the connection has been confirmed before continuing
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Debugging - Output the IP Address of the ESP8266
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  // If the connection is failing, make sure you are using the correct MQTT Username and Password (Setup Earlier in the Instructable)
  if (client.connect(clientID, mqtt_username, mqtt_password)) {
    Serial.println("Connected to MQTT Broker!");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }
}


void setup() {
  Serial.begin(9600);
  emon1.current(pin_sct, 29);
  
  
}

void loop() {
  connect_MQTT();

  Serial.setTimeout(2000);
  
  double t = emon1.calcIrms(1480);
  //Mostra il valore della Corrente
  
  Serial.print("Corrente : ");
  Serial.print(t); // Irmsù

  double h = t*rede;
  Serial.print(" Potenza : ");
  Serial.print(h);
  


  String hs="Amp: "+String((float)t)+" A ";
  String ts="Watt: "+String((float)h)+" W ";
  
  
  



  

  // PUBLISH to the MQTT Broker (topic = Humidity, defined at the beginning)
  if (client.publish(temperature_topic, String(t).c_str())) {
    Serial.println("Current sent!");
  }
  // Again, client.publish will return a boolean value depending on whether it succeded or not.
  // If the message failed to send, we will try again, as the connection may have broken.
  else {
    Serial.println("Current failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(temperature_topic, String(t).c_str());
  }
  if (client.publish(humidity_topic, String(h).c_str())) {
  Serial.println("Pot sent!");
  }
  else {
    Serial.println("Pot failed to send. Reconnecting to MQTT Broker and trying again");
    client.connect(clientID, mqtt_username, mqtt_password);
    delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
    client.publish(humidity_topic, String(h).c_str());
  }
  
  client.disconnect();  // disconnect from the MQTT broker
  delay(1000*10);       // print new values every 1 Minute
  
}
