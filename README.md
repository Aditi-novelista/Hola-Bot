
# e-yantra

 Private repository for all the files in e-yantra(2022-23) of team HB#1169
 
## Team ID: 1169

![WhatsApp Image 2023-03-25 at 12 14 46 PM](https://user-images.githubusercontent.com/119444037/228140566-02208dd6-2b4e-4e80-8640-5c368e5d7f48.jpeg)



### Contributers:

- Aditi Phaneesh @ https://github.com/Aditi-novelista
- Amit Chandrashekhar Hegde @ https://github.com/AmitHegde3
- Vishnu Prakash Bharadwaj @ https://github.com/VishnuPrakashBharadwaj

### Task 0:



- Turtlesim - Moving turtle in a semicircle
- Steps to run it:

  - Run the launch file: 
  >roslaunch <your_pkg_name> task0.launch

### Task 1:


- Controller.py - Built a logic to move the robot to the desired goal and pose using inverse kinematics
- Also robot took form and we added chassis and wheels.
- Steps to run it:
  - Run gazebo using the command: roslaunch <your_pkg_name> .launch 
  >roslaunch holabot.launch
  - In a separate terminal, run controller
  > rosrun <your_pkg_name> <your_filename>.py

### Task 2:
- Aruco.py - feedback from aruco, detects corners of the robot
- Steps to run:
  - Launch the gazebo launch file 
    > roslaunch <your_pkg_name> <filenmae>.launch
  - Run the feedback file 
    > rosrun <your_pkg_name> feedback.py
  - Run the controller file 
    > rosrun <your_pkg_name> controller.py

### Task 3:
- Did the recapitulation video
- We also designed the robot chassis 
 
 ![WhatsApp Image 2023-03-28 at 11 08 57 AM](https://user-images.githubusercontent.com/119444037/228140892-f02fad47-8c19-4f29-ad0a-20ef3f1ee511.jpeg)

 
### Task 4:
 - Task 4A:
   - Component Testing: Hardware Kit was delivered, we made all connections and wired the robot.
 - Task 4B:
   - Made a circle, L-shape and a triangle.
   - Logic:
     - Circle -  used delta connection shm equations and gave the velocities
     - L-shape - gave two wheels same velocities and the front wheel roughly double that.
     - Triangle - R&L velocity, L&F velocity, F&R velocity in the same order negative and positive signs
   - Steps to run:
     - Port in Arduino: ATMega
     - Flash the board using cable.
     - Arduino files named circle.ino,l_shape.ino and triangle.ino
     - Link to Task 4 files
 
 
       [eyrc22_HB_1169/Task 4/4B/L_shape/](https://github.com/AmitHegde3/eyrc22_HB_1169/tree/Aditi-novelista-patch-1/Task%204/4B)
      
 
 
### Task 5:
  - Task 5A:
      - Camera Calibartion: Use the checkerboard and dance below the camera until X,Y,Skew,Size are completed to the maximum extent possible.
      - Calibrate, Save, Commit will be activated. 
      - Click them in order. 
      - If screen freezes after calibrate dance again until screen unfreezes. 
      - Meanwhile, terminal will show sample collection.
      - Camera calibrated.
      - Steps to calibrate:
        - First run 
          > roslaunch cv_basics usb_cam_for_calibrate.launch
        - Then in a new terminal run 
          > rosrun camera_calibration cameracalibrator.py --size 8x6 --square 0.108 image:=/usb_cam/image_raw camera:=/usb_cam --no-service-check
        - Then run 
          > rosrun image_view image_view image:=/usb_cam/image_rect 
 
          > roslaunch cv_basics usb_cam_for_calibrate.launch
 
          > roslaunch cv_basics img_proc.launch
        - The above 3 steps check whether camera calibartion has been finished.
        - Run them in SEPARATE terminals
 
 
 - Task 5B:
    - Drawing snapchat and smilie using image mode
 
       ![WhatsApp Image 2023-03-03 at 3 50 32 PM](https://user-images.githubusercontent.com/119444037/228139099-d6fe98f0-8201-4249-9d0d-1ce8f69d6f4c.jpeg)
 
 
 
    - Steps to run:
      - Run the launch file
      - Run the python file to control the bot. 
      - Run the Aruco feedback file.
      - Links to the files:
 
        https://github.com/AmitHegde3/eyrc22_HB_1169/blob/Aditi-novelista-patch-1/Task%205/5B/Arduino/avr_controller_final/avr_controller_final.ino
 
 
        https://github.com/AmitHegde3/eyrc22_HB_1169/blob/Aditi-novelista-patch-1/Task%205/5B/Arduino/nodemcu_code/nodemcu_code.ino
 
 ### Task 6
 - Run the launch file 
 > roslaunch <your_pkg_name> <your_filename> .launch
 - Run the feedback file
 > rosrun <your_pkg_name>aruco.py
 - Run the controller file
 > rosrun <your_pkg_name> controller.py
 
 ![WhatsApp Image 2023-03-10 at 9 52 36 PM](https://user-images.githubusercontent.com/119444037/228140218-06f639aa-9af6-4708-a03c-13938263d005.jpeg)
 
 
 - Links to Eyrc_final files:
 
   https://github.com/AmitHegde3/eyrc22_HB_1169/tree/main/catkin_ws/src/eyrc_final

 
