#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>


const char *ssid = "STUDBME2"; //Enter your WIFI ssid
const char *password = "BME2Stud"; //Enter your WIFI password
const char *server_url = "http://192.168.1.6:80/Readings";// Nodejs application endpoint

// Set up the client objet
WiFiClient client;
HTTPClient http;

int findElement(String arr[], int n, String val);

String saved_networks[] = {"","STUDBME2","Aalaa Tarek", "khaleesiH", "Esraa","STUDBME1","Sbme-Staff","RehabLab","CMP_LAB1","CMP_LAB3","Gadgooda"};

String scanned_ssids[12];
int rssi_values[12];

int w_len = sizeof(saved_networks)/sizeof(saved_networks[0]);
int s_len = sizeof(scanned_ssids)/sizeof(scanned_ssids[0]);
int s_index = 0;          // index for scanned_ssids
int w_index = 0;          // index for saved_networks

StaticJsonBuffer<2000> jsonBuffer;


void setup()
{
    // Debug console
    delay(10000);
    Serial.begin(9600);
    Serial.println("DATA,STUDBME2,Aalaa Tarek,khaleesiH,Esraa,STUDBME1,Sbme-Staff,RehabLab,CMP_LAB1,CMP_LAB3,Gadgooda,Label");

     WiFi.begin("Lola","lola##**");
     while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
     }
     Serial.println("WiFi connected");
//     delay(1000);
}

void loop()
{

    JsonObject& values = jsonBuffer.createObject();

    // WiFi.scanNetworks will return the number of networks found
    int n = WiFi.scanNetworks();
    

    Serial.print("DATA,");

    // Save SSIDs and RSSIs to array
    for (int i = 0; i < n; ++i)
    {
        // Check if the ssid exists in the saved networks
        s_index = findElement(saved_networks, w_len, WiFi.SSID(i));
        if (s_index != -1)
        {
            scanned_ssids[s_index] = WiFi.SSID(i);
            rssi_values[s_index] = WiFi.RSSI(i);
        }
    }

    // Check if there's a network in saved and not scanned (Error while scanning)
    // So put it's RSSI = 0 (Take average later)
    for (int i = 0; i < w_len; i++)
    {
        w_index = findElement(scanned_ssids, w_len, saved_networks[i]);
        // If it is saved network and not scanned -> put rssi = 0
        if (w_index == -1)
        {
            scanned_ssids[i] = saved_networks[i];
            rssi_values[i] = 0;
        }
    }

     
    // Send data to csv
    for (int i = 0; i < s_len; i++)
    { 
        Serial.print(rssi_values[i]);
        Serial.print(",");
        delay(10);
    }
    Serial.print("1"); // label
    Serial.print(",");
    Serial.println();
    
    // Wait a bit before scanning again
    delay(500);
    WiFi.scanDelete();  

   values[saved_networks[1]] = rssi_values[1] ;
   values[saved_networks[2]] = rssi_values[2] ;
   values[saved_networks[3]] = rssi_values[3] ;
   values[saved_networks[4]] = rssi_values[4] ;
   values[saved_networks[5]] = rssi_values[5] ;
   values[saved_networks[6]] = rssi_values[6] ;
   values[saved_networks[7]] = rssi_values[7] ;
   values[saved_networks[8]] = rssi_values[8] ;
   values[saved_networks[9]] = rssi_values[9] ;
   values[saved_networks[10]] = rssi_values[10] ;
//   values[saved_networks[11]] = rssi_values[11] ;
   


    http.begin(client, server_url);
    http.addHeader("Content-Type", "application/json");
    char arr[500];
  values.prettyPrintTo(arr, sizeof(arr));
    int httpCode = http.POST(arr);
      
    if(httpCode > 0){
      
      if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.print("Response: ");Serial.println(payload);
        }
    }
    else{
         Serial.printf("[HTTP] GET... failed, error: %s", http.errorToString(httpCode).c_str());
         Serial.println();
    }
    http.end();
    delay(5000);

   
}


// Function to find element in an array
// return its index if found and -1 if not
int findElement(String arr[], int n, String val)
{
    int indx = -1;

    for (int i = 0; i < n; i++)
    {
        // if found -> 0 -> !0 = 1 = True
        if(val == String(arr[i]))
        {
            indx = i;
            break;
        }
    }
    return indx;
}
