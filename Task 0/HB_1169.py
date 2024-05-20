#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (KB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			HB#1169
# Author List:		Aditi Phaneesh, Amit Hegde, Amogh Ananda, Vishnu Prakash Bharadwaj
# Filename:			HB_1169.py
# Functions:		callback(), main(), semicircle(), linear(), rotate()
# Nodes:		    Velocity_publisher, Pose_subscriber 


####################### IMPORT MODULES #######################
import sys
import traceback
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math
import time
from std_srvs.srv import Empty
PI = 3.14159265358973
##############################################################


def callback(pose_message):
	"""
	Purpose:
	---
	This function should be used as a callback. Refer Example #1: Pub-Sub with Custom Message in the Learning Resources Section of the Learning Resources.
    You can write your logic here.
    NOTE: Radius value should be 1. Refer expected output in document and make sure that the turtle traces "same" path.

	Input Arguments:
	---
        `data`  : []
            data received by the call back function

	Returns:
	---
        May vary depending on your logic.

	Example call:
	---
        Depends on the usage of the function.
	"""
	global x, y, yaw # accessing global variables x,y and yaw
	x = pose_message.x 			#Receiving x from Pose subscriber
	y = pose_message.y 			#Receiving y from Pose subscriber
	yaw = pose_message.theta	#Receiving theta from Pose subscriber

def main():
	"""
	Purpose:
	---
	This function will be called by the default main function given below.
    You can write your logic here.

	Input Arguments:
	---
        None

	Returns:
	---
        None

	Example call:
	---
        main()
	"""
	
	#Initializing Ros node
	rospy.init_node('task_0', anonymous=True)
	cmd_vel_topic = '/turtle1/cmd_vel'
	#defining velocity publisher for the turtlesim
	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
	
	position_topic = '/turtle1/pose'
	#defining position subscriber, to recieve callback from the turtlesim
	pose_subscriber = rospy.Subscriber(position_topic, Pose, callback)
	time.sleep(2)
	#Drawing a semicircular arc of radius 1.0 unit with PI/4 rads/s in forward direction
	semicircle(PI/4,1.0,True)
	#Rotating the turtle by 90 degrees at the speed of 45 deg/s in the CCW direction
	rotate(45,90,0)
	#Moving the turtle in a straight line by 2 units
	linear(1.0,2.0,True)
	#Forcibly ends the node when ctrl + c is entered
	rospy.spin()


################# ADD GLOBAL VARIABLES HERE #################
x = 0
y = 0
yaw = 0

##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
	
def semicircle(speed, distance, is_forward):

	#Defining velocity message to control velocity parameters of the turtle
	velocity_message = Twist()
	#Accessing global variable x
	global x

	#Storing copy of original value of x
	x0 = x
	
	#Based on the is_forward parameter, providing suitable input for the linear x of the turtle
	#Using V = R*W formula from physics, let angular.z = W (speed), and distance = R(radius), therefore V = R*W
	if (is_forward):
		velocity_message.linear.x = distance*abs(speed)
	else:
		velocity_message.linear.x = -distance*abs(speed)
	
	#setting other parameters to 0
	velocity_message.linear.y = 0
	velocity_message.linear.z = 0
	velocity_message.angular.x = 0
	velocity_message.angular.y = 0

	#Angular velocity of the turtle in z direction
	velocity_message.angular.z = speed

	#To make the loop run at 10Hz
	loop_rate = rospy.Rate(10)

	#local publisher
	cmd_vel_topic = '/turtle1/cmd_vel'
	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
	
	#Moving on a semicircular arc till x coordinate is same as the original position
	#Due to inaccuracy in our calculations, and also the loop runs at 10hz, we have provided the min difference to be 0.05
	while True:
		velocity_publisher.publish(velocity_message)
		loop_rate.sleep()
		print("My turtleBot is: Moving in circle!!")
		if abs(x-x0) <= 0.05:
			break
	
	#stopping the robot
	velocity_message.linear.x = 0
	velocity_message.angular.z = 0
	velocity_publisher.publish(velocity_message)
	
#function to move the turtle in y direction
def linear(speed, distance, is_forward):
	#Defining velocity message to control velocity parameters of the turtle
	velocity_message = Twist()

	#Accessing global variables and storing a copy of it in local vars
	global x, y
	x0, y0 = x, y

	#Determing the direction of motion based on is_forward value
	if (is_forward):
		velocity_message.linear.x = abs(speed)
	else:
		velocity_message.linear.x = -abs(speed)

	#To make the loop run at 20Hz
	loop_rate = rospy.Rate(20)
	cmd_vel_topic = '/turtle1/cmd_vel'
	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
	
	#Moving in a straight line till the difference between current y and initial y is equal to the given distance
	while True:
		print("My turtleBot is: Moving Straight!!!")
		velocity_publisher.publish(velocity_message)
		loop_rate.sleep()
		if abs(y-y0) >= distance:
			print("Done")
			break

	velocity_message.linear.x = 0
	velocity_publisher.publish(velocity_message)

#function to rotate the turtle by a given angle
def rotate(speed, angle, clockwise):
	#local velocity publisher
	cmd_vel_topic = '/turtle1/cmd_vel'
	velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
	velocity_message = Twist()
	
	#converting the given parameters in terms of radians
	angular_speed = speed*2*PI/360
	relative_angle = angle*2*PI/360

	#Setting other parameters to 0
	velocity_message.linear.x = 0
	velocity_message.linear.y = 0
	velocity_message.linear.z = 0
	velocity_message.angular.x = 0
	velocity_message.angular.y = 0


	#Determining the direction of rotation based on the clockwise param value
	if clockwise:
		velocity_message.angular.z = -abs(angular_speed)
	else:
		velocity_message.angular.z = abs(angular_speed)

	#Getting the current time for distance calculus
	t0 = rospy.Time.now().to_sec()
	current_angle = 0

	#Rotating the turtle till current angle reaches the relative angle
	while(current_angle < relative_angle):
		velocity_publisher.publish(velocity_message)
		print("My turtleBot is: Rotating!!")
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed*(t1-t0)

	#Stopping the rotation
	velocity_message.angular.z = 0
	velocity_publisher.publish(velocity_message)


##############################################################


######### YOU ARE NOT ALLOWED TO MAKE CHANGES TO THIS PART #########
if __name__ == "__main__":
    try:
        print("------------------------------------------")
        print("         Python Script Started!!          ")
        print("------------------------------------------")
        main()

    except:
        print("------------------------------------------")
        traceback.print_exc(file=sys.stdout)
        print("------------------------------------------")
        sys.exit()

    finally:
        print("------------------------------------------")
        print("    Python Script Executed Successfully   ")
        print("------------------------------------------")
