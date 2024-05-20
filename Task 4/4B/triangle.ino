#include <AccelStepper.h>

int A = 400;

AccelStepper Lw(1, 5, 7);
AccelStepper Rw(1, 9, 11); 
AccelStepper Fw(1, 4, 46); 

void setup() {
  // put your setup code here, to run once:
  Lw.setMaxSpeed(A);
  Rw.setMaxSpeed(A);
  Fw.setMaxSpeed(A);
  Fw.setSpeed(0);
  Lw.setSpeed(0);
  Rw.setSpeed(0);

  delay(1000);

  long int starttime = millis();
  long int endtime = starttime;
  
  starttime = millis();
  Lw.setSpeed(-300);
  Rw.setSpeed(300);
  while((millis() - starttime)<= 3000){
    Lw.runSpeed();
    Rw.runSpeed();
  }
  //Backward for 3 seconds
  starttime = millis();
  Rw.setSpeed(-300);
  Fw.setSpeed(300);
  while((millis() - starttime)<= 3000){
    Rw.runSpeed();
    Fw.runSpeed();
  }
  //Leftward for 3 seconds
  
  starttime = millis();
  Fw.setSpeed(-300);
  Lw.setSpeed(300);
  while((millis() - starttime)<= 3000){
    Fw.runSpeed();
    Lw.runSpeed();
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
