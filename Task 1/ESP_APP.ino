//All The Includes:
#include <Arduino.h>
#include <WebSocketsServer.h>
#include "DHT.h"
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <string.h>

//Consts , macros and variables
#define TO_STRING(val) #val

//WiFi scan param.
char* username;
char* password;
char* data[]={"usernameusernameusername","password"};// The password of the Wi-Fi network

const char *ssid =  "SBMELAB23-PC 6126";   //Wifi SSID (Name)   
const char *pass =  "v>15H900"; //wifi password

//DHT Param
#define DHTPIN D2     // what digital pin the DHT11 is conected to
#define DHTTYPE DHT11   // setting the type as DHT11
DHT dht(DHTPIN, DHTTYPE); // DHT Configuration

//Alarm Led
int ledpin = D3; //defining the OUTPUT pin for LED (D3)
WebSocketsServer webSocket = WebSocketsServer(81); //websocket init with port 81

// The server IP on the host
const char *server_url = "http://**.**.**.**/Readings";// application endpoint

// Data Transmittion buffer (json object)
StaticJsonBuffer<10000> jsonBuffer;

// WiFi and HTTP clients objets
WiFiClient client;
HTTPClient http;


void setup() {

  //For initialization and opening the serial monitor
    delay(5000);
  //Baud rate
    Serial.begin(9600);
      
   //Asking for the desired Network parameters   
    Serial.println('\n');
    Serial.println("Please Enter The SSID You Want To Connect To: ");
    username = serial_tochar(0);
    Serial.println("Please Enter Password: ");
    password = strtok(serial_tochar(1), " ");
    Serial.println('\n');
    
    // prints the received data
    Serial.print("The SSID you connecting to is: ");
    Serial.println( username);
    
    Serial.print("Password is: ");
    Serial.println(password);
    Serial.println('\n');
    
    // WIFI CONNECTION !!
    WiFi.begin("iPhone 11", "Me5wme5w");             // Connect to the network
    Serial.print("Connecting to ");
    Serial.print(username); Serial.println(" ...");
    
    int i = 0;
    while (WiFi.status() != WL_CONNECTED) 
    {
      // Wait for the Wi-Fi to connect
      delay(1000);
      Serial.print("."); Serial.print(' ');
    }
  
    Serial.println('\n');
    Serial.println("Connection established!");  
    Serial.print("IP address:\t");
    Serial.println(WiFi.localIP());   // Prints the IP address of the ESP8266 to the computer


    //Web Socket Configurations:
    Serial.println("Connecting to wifi");
    IPAddress apIP(172, 28, 128, 1);   //Static IP for wifi gateway 192.168.137.1
    WiFi.softAPConfig(apIP, apIP, IPAddress(255, 255, 255, 0)); //set Static IP gateway on NodeMCU
    WiFi.softAP(username, password); //turn on WIFI
    
    webSocket.begin(); //websocket Begin
    //When led button pressed, it calls the event function
    webSocket.onEvent(webSocketEvent); //set Event for websocket (LED Button Pressed)
    Serial.println("Websocket is started");


}


void loop() 
{
    webSocket.loop(); //keep this line on loop method

    //Create a json dataype named Values to keep the readings
    JsonObject& values = jsonBuffer.createObject();

  
    //First: WIFI Scanning Function
    Serial.println("Scanning The Available Networks..... ");
    Serial.println('\n');
    Serial.println("The Available Networks: ");

   // Printing the available networks on the serial monitor
    int numberOfNetworks = WiFi.scanNetworks();
    for(int i =0; i<numberOfNetworks; i++)
     {
      Serial.print(i+1);
      Serial.print("-Network name: ");
      Serial.println(WiFi.SSID(i));
      Serial.print("  Signal strength: ");
      Serial.print(WiFi.RSSI(i));
      Serial.println(" dB");
      Serial.println("-----------------------------------------");
      //Hold the values
      values["name"] = WiFi.SSID(i);
      values["strength"] = WiFi.RSSI(i);
      values["label"]= 0;
      }
 

  // Start the connection
  http.begin(client, server_url);
  
  //Assign the datatype to be transered 
  http.addHeader("Content-Type", "application/json");

  //Create The JSON file
  char arr[200];
  values.prettyPrintTo(arr, sizeof(arr));
  //Post method to send the data 
  int httpCode = http.POST(arr);
      
    if(httpCode > 0)
    {
      if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) 
      {
          String payload = http.getString();
          Serial.print("Response: ");Serial.println(payload);
       
       }
    }
    
    else
    {
      
         Serial.printf("[HTTP] GET... failed, error: %s", http.errorToString(httpCode).c_str());
         Serial.println();
    }
    http.end();

delay(500);
}

// A Functions that reads the serial inputs into strings
char* serial_tochar(int choose_data) {
    while(Serial.available()==0) { }
    String str =Serial.readString();
    str.toCharArray(data[choose_data], str.length());
    return data[choose_data];
}



void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length) 
{
//webscket event method
    String cmd = "";
    switch(type) 
    {
        case WStype_DISCONNECTED:
            Serial.println("Websocket is disconnected");
            //case when Websocket is disconnected
            break;
            
        case WStype_CONNECTED:{
            //wcase when websocket is connected
            Serial.println("Websocket is connected");
            Serial.println(webSocket.remoteIP(num).toString());
            webSocket.sendTXT(num, "connected");}
            break;
            
        case WStype_TEXT:
            cmd = "";
            for(int i = 0; i < length; i++) {
                cmd = cmd + (char) payload[i]; 
            } //merging payload to single string
            Serial.println(cmd);

            if(cmd == "poweron")
            { //when command from app is "poweron"
                digitalWrite(ledpin, HIGH);   //make ledpin output to HIGH  
            }
            else if(cmd == "poweroff")
            {
                digitalWrite(ledpin, LOW);    //make ledpin output to LOW on 'pweroff' command.
            }

//             webSocket.sendTXT(num, TO_STRING(cmd) + ":success");
             webSocket.sendTXT(num, cmd);
             //send response to mobile, if command is "poweron" then response will be "poweron:success"
             //this response can be used to track down the success of command in mobile app.
            break;
            
        case WStype_FRAGMENT_TEXT_START:
            break;
            
        case WStype_FRAGMENT_BIN_START:
            break;
            
        case WStype_BIN:
            hexdump(payload, length);
            break;
            
        default:
            break;
    }
}
