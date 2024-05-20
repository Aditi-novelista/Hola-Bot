/*

  Team Id: HB_1169
  
  Author List: Vishnu Prakash Bharadwaj, Amit Hegde
  
  Filename: avr_controller_final
  
  Theme: HolA Bot (HB)
  
  Functions: recvWithStartEndMarkers(), parseData(), setup() , loop()
  
  Global Variables: const byte numChars ,char receivedChars[numChars],char tempChars[numChars],char messageFromPC[numChars],
                    int integer1FromPC, integer2FromPC, integer3FromPC, integer4FromPC,float floatFromPC,boolean newData,int A
  
*/

//=======================================================================  
//The SoftwareSerial library allows serial communication
#include <SoftwareSerial.h>

//The AccelStepper library allows Arduino boards to control a variety of stepper motors.
#include <AccelStepper.h>


AccelStepper Fw(1,2,5);
AccelStepper Rw(1,3,6);
AccelStepper Lw(1,4,7);


const byte numChars = 32;
char receivedChars[numChars];
// temporary array for use when parsing
char tempChars[numChars];
char messageFromPC[numChars] = {0};
int integer1FromPC = 0, integer2FromPC = 0, integer3FromPC = 0, integer4FromPC = 0;

boolean newData = false;
int A = 400;


//=======================================================================
/*
  Function Name: setup()
  
  Input: None.
  
  Output: Defines the max speed of stepper motors and initial speed to 0.
  
  Logic: None.
  
  Example Call: Automatically called once.
*/ 
void setup() {
    Serial.begin(115200);
    Fw.setMaxSpeed(A);
    Lw.setMaxSpeed(A);
    Rw.setMaxSpeed(A);
  
    Fw.setSpeed(0);
    Lw.setSpeed(0);
    Rw.setSpeed(0);
}

//=======================================================================
/*
  Function Name: loop()
  
  Input: None
  
  Output: Calls recvWithStartEndMarkers() and feeds the required velocities to each wheel.
  
  Logic: None.
  
  Example Call: Automatically called in an infinite loop.
*/
void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
        parseData();
        newData = false;
    }

    Fw.runSpeed();
    Rw.runSpeed();
    Lw.runSpeed();
}

//=======================================================================

/*
  Function Name:recvWithStartEndMarkers()
  
  Input: None.
  
  Output: Receives the string from nodemcu.
  
  Logic: Receives data from serial and checks for start and end markers(In our case '<' and '>')
  
  Example Call: recvWithStartEndMarkers();
*/

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//=======================================================================

/*
  Function Name: parseData()
  
  Input: eNone
  
  Output: Splits data from the received string and sets the speed to each stepper motor.
  
  Logic: This function splits the data received into parts using converts the split part into integer to feed it to each wheel(wheel velocity)
  
  Example Call: parseData();
  
*/

void parseData() {                            // split the data into its parts

    char * strtokIndx;                        // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");       // get the first part - the string
    integer1FromPC = atoi(strtokIndx);

    if(integer1FromPC == 1){
      strtokIndx = strtok(NULL, ",");         // this continues where the previous call left off
      integer2FromPC = atoi(strtokIndx);      // convert this part to an integer

      strtokIndx = strtok(NULL, ",");
      integer3FromPC = atoi(strtokIndx);      // convert this part to a integer
      
      strtokIndx = strtok(NULL, ",");
      integer4FromPC = atoi(strtokIndx);      // convert this part to a integer

      Fw.setSpeed(integer2FromPC);
      Rw.setSpeed(integer3FromPC);
      Lw.setSpeed(integer4FromPC);
    }
}
