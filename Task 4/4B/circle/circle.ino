#include <AccelStepper.h>

int A = 400;
int Vf = 0, Vr = 0, Vl = 0;

AccelStepper Lw(1, 5, 7);//3A,4B
AccelStepper Rw(1, 9, 11); //2B,1A
AccelStepper Fw(1, 4, 46); //0B,5A

void setup() {
  // put your setup code here, to run once:
  Lw.setMaxSpeed(A);
  Rw.setMaxSpeed(A);
  Fw.setMaxSpeed(A);
  Fw.setSpeed(0);
  Lw.setSpeed(0);
  Rw.setSpeed(0);

  delay(1000);

  for(float t = 0; t <= 6.28; t += 0.0005){
    Vf = A*cos(t);
    Vl = A*cos(t + 2.094);
    Vr = A*cos(t - 2.094);
    Fw.setSpeed(Vf);
    Lw.setSpeed(Vl);
    Rw.setSpeed(Vr);
    
    Fw.runSpeed();
    Lw.runSpeed();
    Rw.runSpeed();
  }
  
}

void loop() {
  // put your main code here, to run repeatedly:

}
