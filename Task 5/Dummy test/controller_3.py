#!/usr/bin/env python3

'''
*****************************************************************************************
*
*        		===============================================
*           		    HolA Bot (HB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script should be used to implement Task 0 of HolA Bot (HB) Theme (eYRC 2022-23).
*
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:		1169
# Author List:		Aditi Phanessh,Amit Hegde,Amogh Ananda,Vishnu Prkash Bharadwaj
# Filename:		controller.py
# Functions:		signal_handler,cleanup,task2_goals_Cb,aruco_feedback_Cb,custom_map,main
# Nodes:		controller_node,detected_aruco,task2_goals


################### IMPORT MODULES #######################

import rospy
import signal		# To handle Signals by OS/user
import sys		# To handle Signals by OS/user
import numpy as np
import socket
import cv2
from time import sleep
#from geometry_msgs.msg import Wrench		# Message type used for publishing force vectors
from geometry_msgs.msg import PoseArray	# Message type used for receiving goals
from geometry_msgs.msg import Pose2D		# Message type used for receiving feedback

import time
import math		# If you find it useful

from tf.transformations import euler_from_quaternion	# Convert angles

################## GLOBAL VARIABLES ######################

PI = 3.14

#x_goals = [250, 250, 250, 250, 250]
x_goals = [350,50,50,350,250]
#y_goals = [250, 250, 250, 250, 250]
y_goals = [350,350,50,50,250]
theta_goals = [0.785, 2.335, -2.335, -0.785, 0]
#theta_goals = [0, PI/2, PI, -PI/2, 0]

#x_goals, y_goals, theta_goals = [400], [400], [0]

hola_x = 0
hola_y = 0
hola_theta = 0

ip = ""
s = None

##################### FUNCTION DEFINITIONS #######################

# NOTE :  You may define multiple helper functions here and use in your code

def signal_handler(sig, frame):
	  
	# NOTE: This function is called when a program is terminated by "Ctr+C" i.e. SIGINT signal 	
	print('Clean-up !')
	cleanup()
	sys.exit(0)

def cleanup():
	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Not mandatory - but it is recommended to do some cleanup over here,
	#	   to make sure that your logic and the robot model behaves predictably in the next run.

	############################################
	s.close()
	print("cleanup done")
	pass
  
def task2_goals_Cb(msg):
	global x_goals, y_goals, theta_goals
	x_goals.clear()
	y_goals.clear()
	theta_goals.clear()

	for waypoint_pose in msg.poses:
		x_goals.append(waypoint_pose.position.x)
		y_goals.append(waypoint_pose.position.y)

		orientation_q = waypoint_pose.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		theta_goal = euler_from_quaternion (orientation_list)[2]
		theta_goals.append(theta_goal)

def aruco_feedback_Cb(msg):
	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Receive & store the feedback / coordinates found by aruco detection logic.
	#	-> This feedback plays the same role as the 'Odometry' did in the previous task.
	############################################
	global hola_x, hola_y, hola_theta
	hola_x = msg.x
	hola_y = msg.y
	hola_theta = msg.theta


def custom_map(X, FL, FH, TL, TH):
	return TH + (TH - TL)*(X-FH)/(FH-FL)



def function_mode():
	# Set up the parameters for the Lissajous curve
	a = 400
	b = 200
	theta = 0

	# Set up the image and drawing parameters
	img_size = (800, 800)
	center = (img_size[0] // 2, img_size[1] // 2)
	scale = 0.25
	thickness = 2
	color = (255, 255, 255)

	# Define the function for the Lissajous curve
	def lissajous(t):
		x = a * np.cos(t)
		y = b * np.sin(2 * t + theta)
		return (2*x, 2*y)

	# Create the image and initialize the drawing
	img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)
	cv2.line(img, (0, center[1]), (img_size[0], center[1]), color, thickness=thickness)
	cv2.line(img, (center[0], 0), (center[0], img_size[1]), color, thickness=thickness)

	# Draw the Lissajous curve
	t = np.linspace(0, 2 * np.pi, 500)
	points = np.array([lissajous(ti) for ti in t], dtype=np.int32)
	points = np.round(points * scale + center).astype(np.int32)
	cv2.polylines(img, [points], False, color, thickness=thickness)

	x = []
	y = []
	for i in points:
		x.append(i[0])
		y.append(i[1])
	return (x,y)

def image_mode():
	#initialising the image
	font = cv2.FONT_HERSHEY_COMPLEX
	image = cv2.imread('smile.png',cv2.FONT_HERSHEY_COMPLEX)
	image_alt = cv2.imread('smile.png',cv2.IMREAD_COLOR)
	image_gray = cv2.imread('smile.png', cv2.IMREAD_GRAYSCALE) #image in grayscale

	#eroding the image
	image_gray = 255 - image_gray
	kernel = np.ones((3,3),np.uint8)
	for i in range(0):
		image_gray = cv2.erode(image_gray, kernel) 

	#resizing image
	image_alt = cv2.resize(image_alt, (500,500))
	image_gray = cv2.resize(image_gray, (500,500))

	# Converting image to a binary image
	# ( black and white only image).
	_, threshold = cv2.threshold(image_gray, 110, 255, cv2.THRESH_BINARY)

	# Detecting contours in image.
	contours, _= cv2.findContours(threshold, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	image_alt = 255-image_alt
    
	#excluding the unessecary contours
	contours = contours[1:]

	#printing the required number of contours
	print("Number of Contours: ",len(contours))

	# Going through every contours found in the image.
	for cnt in contours :

		approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)


		# draws boundary of contours.
		cv2.drawContours(image_alt, contours, -1, (0, 255, 0), 5) 


		# Used to flatted the array containing
		# the co-ordinates of the vertices.
		n = approx.ravel() 
		i = 0
	
		for j in n :
			if(i % 2 == 0):
				x = n[i]
				y = n[i + 1]
    
				# String containing the co-ordinates.
				string = str(x) + " " + str(y) 
                
				if(i == 0):
					pass
					# text on topmost co-ordinate.
					#cv2.putText(image_alt, "Arrow tip", (x, y),image, 0.5, (255, 0, 0)) 
					cv2.putText(image_alt, "Start " + string, (x, y),font, 0.4, (255, 0, ))		
				else:
					pass
					# text on remaining co-ordinates.
					#cv2.putText(image_alt, string, (x, y),image, 0.5, (0, 255, 0)) 
					cv2.putText(image_alt, string, (x, y),font, 0.4, (0, 255, 0))
			i = i + 1
	x = []
	y = []
	for i in contours:
		for j in i:
			for k in j:
				x.append(k[0])
				y.append(k[1])
	return(x,y)
	

def main():
	global x_goals, y_goals, theta_goals, hola_x, hola_y, hola_theta, s, ch
	rospy.init_node('controller_node')
	signal.signal(signal.SIGINT, signal_handler)
	ch = int(input('Enter:\n1. Image Mode\n2. Function Mode'))
	

	# NOTE: You are strictly NOT-ALLOWED to use "cmd_vel" or "odom" topics in this task
	#	Use the below given topics to generate motion for the robot.

	rospy.Subscriber('detected_aruco',Pose2D,aruco_feedback_Cb)
	rospy.Subscriber('task2_goals',PoseArray,task2_goals_Cb)
	#rospy.sleep(5)

    
        

	rate = rospy.Rate(100)

	goal_num = 0
	
	if (ch == 1):
		x_goals,y_goals = image_mode()
		theta_goals = []
		for i in range(len(x_goals)):
			theta_goals.append(0)
	
	elif (ch == 2):
		x_goals,y_goals = function_mode()
	
	else:
		print("Invalid Input!")

    

	while not rospy.is_shutdown():

		#x,y = map.return(function_mode())
		x = x_goals[goal_num]
		y = y_goals[goal_num]
		theta_d = theta_goals[goal_num]
		theta_d = math.atan2(math.sin(theta_d), math.cos(theta_d))

		# Calculate Error from feedback
		e_x = x - hola_x
		e_y = y - hola_y
		e_theta = theta_d - hola_theta
		speed = 5*PI
		kp = 30

		vx, vy, omega = 0, 0, 0

		vx_old, vy_old, omega_old = vx, vy, omega

		while abs(e_x) > 1 or abs(e_y) > 1 or abs(e_theta*180/PI) >= 1:
			print("ex: " + str(e_x) + " ey: " + str(e_y) + " etheta: " + str(e_theta))
			print("x: " + str(hola_x) + " y: " + str(hola_y) + " theta: " + str(hola_theta))

			ct = hola_theta
			x0, y0 = hola_x, hola_y
			diff = math.dist([hola_x, hola_y],[x, y])

			# Change the frame by using Rotation Matrix (If you find it required)
			c = np.matmul(np.linalg.inv([[math.cos(ct),-math.sin(ct)],[math.sin(ct), math.cos(ct)]]), [x - x0, y - y0])
			theta = math.atan2( c[1], c[0])


			if(diff < 50):
				vx = math.cos(theta)*diff
				vy = math.sin(theta)*diff
			else:

				vx = 300*math.cos(theta)*diff/abs(diff)
				vy = 300*math.sin(theta)*diff/abs(diff)
			
			omega = speed*(theta_d - ct)
	
			l = 0.205
			mat = [[0, -1, l],
				   [math.sin(-60), 0.5, l],
				   [math.sin(60), 0.5, l]]
			
			res = np.matmul(mat, [-vy, -vx, omega])
			print(res)
			msg = str(int(custom_map(-kp*res[0], -800, 800, -400, 400))) + ',' + str(int(custom_map(kp*res[1], -800, 800, -400, 400))) + ',' + str(int(custom_map(kp*res[2], -800, 800, -400, 400))) + '\n'
			print(msg)
			conn.sendall(str.encode(msg))

		

			# Modify the condition to Switch to Next goal (given position in pixels instead of meters
			rate.sleep()
			e_x = x - hola_x
			e_y = y - hola_y
			e_theta = theta_d - hola_theta
			vx_old = vx
			vy_old = vy

		if(goal_num == len(x_goals) - 1):
			print("All goals reached")
			rospy.spin()
			
		else:
			print("Goal " + str(goal_num + 1) + " Reached!")
			goal_num += 1
		rospy.sleep(1.5)
    ############################################

if __name__ == "__main__":
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind((ip, 8002))
		s.listen()
		conn, addr = s.accept()
		print(f"Connected by {addr}")

		main()
	except rospy.ROSInterruptException:
		pass
