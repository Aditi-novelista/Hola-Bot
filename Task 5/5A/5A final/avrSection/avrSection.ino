#include <AccelStepper.h>

int A = 400;
int Vf = 0, Vr = 0, Vl = 0;
int stepsPerRevolution = 200;
int r = 6;
int g = 8;
int b = 7;
String msg = "0";

AccelStepper Fw(1,4,46);//0B,5A
AccelStepper Rw(1,5,7);//3A,4B
AccelStepper Lw(1,9,11);//2B,1A

String getValue(String data, char separator, int index){
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void setup() {
  Serial.begin(115200);
  pinMode(r,OUTPUT);
  pinMode(g,OUTPUT);
  pinMode(b,OUTPUT);
  
  Fw.setMaxSpeed(A);
  Lw.setMaxSpeed(A);
  Rw.setMaxSpeed(A);

  Fw.setSpeed(0);
  Lw.setSpeed(0);
  Rw.setSpeed(0);



}

void loop() {
  //Serial.println("In for loop");
  
  if(Serial.available()){                  //Check if any data is available on Serial
    msg = Serial.readStringUntil('\n');    //Read message on Serial until new char(\n) which indicates end of message. Received data is stored in msg
    Vf = getValue(msg, ',', 0).toInt();
    Vr = getValue(msg, ',', 1).toInt();
    Vl = getValue(msg, ',', 2).toInt();
    
    analogWrite(r,255);
    analogWrite(g,255);
    analogWrite(b,0);
  }else{
    //Serial.write(0);  
    analogWrite(r,0);
    analogWrite(g,255);
    analogWrite(b,255);
  }

    Fw.setSpeed(Vf);
    Lw.setSpeed(Vl);
    Rw.setSpeed(Vr);
    
    Fw.runSpeed();
    Lw.runSpeed();
    Rw.runSpeed();
}
