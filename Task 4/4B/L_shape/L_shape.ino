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
  //Forward for 3 seconds
  Lw.setSpeed(-300);
  Rw.setSpeed(300);
  while((millis() - starttime)<= 3000){
    Lw.runSpeed();
    Rw.runSpeed();
  }
  //Backward for 3 seconds
  Lw.setSpeed(300);
  Rw.setSpeed(-300);
  starttime = millis();
  while((millis() - starttime)<= 3000){
    Lw.runSpeed();
    Rw.runSpeed();
  }
  //Leftward for 3 seconds
  Fw.setSpeed(-300);
  Lw.setSpeed(150);
  Rw.setSpeed(150);
  
  starttime = millis();
  while((millis() - starttime)<= 3000){
    Fw.runSpeed();
    Lw.runSpeed();
    Rw.runSpeed();
  }

  Fw.setSpeed(300);
  Lw.setSpeed(-150);
  Rw.setSpeed(-150);
  
  starttime = millis();
  while((millis() - starttime)<= 3000){
    Fw.runSpeed();
    Lw.runSpeed();
    Rw.runSpeed();
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:

}
