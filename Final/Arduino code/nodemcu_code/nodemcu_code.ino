/*

  Team Id: HB_1169
  
  Author List: Vishnu Prakash Bharadwaj, Amit Hegde
  
  Filename: nodemcu_code
  
  Theme: HolA Bot (HB)
  
  Functions: penDown(),penUp(), setup() , HTTP_handleroot() , loop() , setup()
  
  Global Variables: const char* ssid ,const char* pass,String msg ,String prevMsg,String vf, vr, vl,p1,p2,m
  
*/

//=======================================================================  

#include <WiFiClient.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>


const char* ssid = "HOLA_1169";
const char* pass = "Hola@123";
ESP8266WebServer server(80);

String msg = "dum";
String prevMsg = "";
int pen1 = 0, pen2 = 0;
String vf, vr, vl,p1,p2, m;
//======================================================================= 
/*
  Function Name: setup()
  
  Input: None
  
  Output: Setup of WIFI access point ,call penUp() and penDown() fucntion once for testing and connets to HTTP server.
  
  Logic: None
  
  Example Call: Automatically called once.
*/
 
void setup() {
  
  Serial.begin(115200);
  
  pinMode(D7,OUTPUT); 
  pinMode(D6,OUTPUT); 
  pinMode(D5,OUTPUT);
  pinMode(D4,OUTPUT);

  penDown();
  pen2Down();
  penUp();
  pen2Up();
  
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid,pass);


  server.on("/",HTTP_handleroot);
  server.onNotFound(HTTP_handleroot);
  server.begin();

}
//=======================================================================
/*
  Function Name: loop()
  
  Input: None.
  
  Output: Sends string data(velocity data) to avr_controller.
  
  Logic: None.
  
  Example Call: Automatically called in an infinte loop.
*/ 
void loop() {
  
  server.handleClient();
  
  m = server.arg("mode");

  if(m == "0"){
    p1 = server.arg("p1");
    p2 = server.arg("p2");
    if(p1 != "" && p2 != ""){
      msg = "<" + m +"," + p1 + "," + p2 + ">";
      if(msg != prevMsg){
        if(p1 == "1" && pen1 == 0){
          penDown();
          pen1 = 1;
        }else if(p1 == "0" && pen1 == 1){
          penUp();
          pen1 = 0;
        }

        if(p2 == "1" && pen2 == 0){
          pen2Down();
          pen2 = 1;
        }else if(p2 == "0" && pen2 == 1){
          pen2Up();
          pen2 = 0;
        }
        prevMsg = msg;
      }
    }
  }else if(m == "1"){
    vf = server.arg("v1");
    vr = server.arg("v2");
    vl = server.arg("v3");

    if(vf != "" && vr != "" && vl != ""){
      msg = "<" + m + "," + vf + "," + vr + "," + vl + ">";
      if(msg != prevMsg){
      Serial.println(msg);
      Serial.flush();
     prevMsg = msg;
      }
    }
  }
  
}
//=======================================================================
/*
  Function Name: setup()
  
  Input: None.
  
  Output: Pen goes down in bot.
  
  Logic: Till D5 goes high the pen will go down.
  
  Example Call: penDown();
*/  
void penDown(){
  digitalWrite(D7,LOW);
  digitalWrite(D6,HIGH);
  delay(1000);
  digitalWrite(D7,LOW);
  digitalWrite(D6,LOW);
}

void pen2Down(){
  digitalWrite(D5,LOW);
  digitalWrite(D4,HIGH);
  delay(1000);
  digitalWrite(D5,LOW);
  digitalWrite(D4,LOW);
}
//=======================================================================
/*
  Function Name: setup()
  
  Input: None.
  
  Output:Pen goes up for 0.6 seconds in bot.
  
  Logic: For 0.6seconds it'll go up using digital pins D7 and D6.
  
  Example Call: penUp();
*/ 
void penUp(){
  digitalWrite(D7,HIGH);
  digitalWrite(D6,LOW);
  delay(1000);
  digitalWrite(D7,LOW);
  digitalWrite(D6,LOW);
}

void pen2Up(){
  digitalWrite(D5,HIGH);
  digitalWrite(D4,LOW);
  delay(1000);
  digitalWrite(D5,LOW);
  digitalWrite(D4,LOW);
}

//=======================================================================
/*
  Function Name: HTTP_handleroot(void)
  
  Input: None.
  
  Output: Sends OK status to client.
  
  Logic: None.
  
  Example Call: It's automatically called when a HTTP client sends a request.
*/ 
void HTTP_handleroot(void){
  server.send(200,"text/html","");
  delay(10);
}
