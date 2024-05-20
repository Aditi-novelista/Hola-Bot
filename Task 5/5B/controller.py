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

# Team ID:		[ 1169 ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:		controller.py
# Functions:
#			[ Comma separated list of functions in this file ]
# Nodes:		Add your publishing and subscribing node


################### IMPORT MODULES #######################

import rospy
import signal		# To handle Signals by OS/user
import sys		# To handle Signals by OS/user
import numpy as np
import socket
from time import sleep
#from geometry_msgs.msg import Wrench		# Message type used for publishing force vectors
from geometry_msgs.msg import PoseArray	# Message type used for receiving goals
from cv_basics.msg import aruco_data		# Message type used for receiving feedback
from std_msgs.msg import String
from std_msgs.msg import Int32
import requests
import time
import math		# If you find it useful
import cv2

from tf.transformations import euler_from_quaternion	# Convert angles

################## GLOBAL VARIABLES ######################

PI = 3.14
pi = 3.14159265358973

#x_goals = [250, 250, 250, 250, 250]
#x_goals = [250,350,150,150,350]
#y_goals = [250, 250, 250, 250, 250]
#y_goals = [250,300,300,150,150]
#theta_goals = [0, pi/4,3*pi/4, -3*pi/4, -pi/4]
#theta_goals = [0, 0, 0, 0, 0]

#x_goals, y_goals, theta_goals = [50,350,50,250,250], [350,50,50,350,50], [0, 0, 0, 0, 0]

x_goals, y_goals, theta_goals = [],[],[]

hola_x = 0
hola_y = 0
hola_theta = 0
p1 = 0
pen2 = 0
mode = 0

#offset_x = 30
#offset_y = -5
offset_x = 0
offset_y = 0
trans_offset_x = 0
trans_offset_y = 0
#280,245
URL = "http://192.168.4.1/"
#s = None

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
	#s.close()
	global p1
	PARAMS = {"mode": 1, 'v1':0,'v2':0,'v3':0}
			#conn.sendall(str.encode(msg))
	response = requests.get(url= URL, params = PARAMS)

	if(p1 != 0):
		pen(0,0)
		p1 = 0
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

def image_mode(url):
	#initialising the image
	font = cv2.FONT_HERSHEY_COMPLEX
	#image = cv2.imread(url,cv2.FONT_HERSHEY_COMPLEX)
	image = cv2.imread(url)
	#cv2.imshow("image",image)
	#image = cv2.flip(image,0)
	image_alt = cv2.imread(url,cv2.IMREAD_COLOR)
	image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #image in grayscale

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
	#print("Number of Contours: ",len(contours))

	# Going through every contours found in the image.
	for cnt in contours :

		approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)


		# draws boundary of contours.
		cv2.drawContours(image_alt, contours, -1, (0, 255, 0), 5) 


		# Used to flatted the array containing
		# the co-ordinates of the vertices.
		n = approx.ravel() 
		i = 0


	
		# for j in n :
		# 	if(i % 2 == 0):
		# 		x = n[i]
		# 		y = n[i + 1]

		# 		# String containing the co-ordinates.
		# 		string = str(x) + " " + str(y) 

		# 		if(i == 0):
		# 			pass
		# 			# text on topmost co-ordinate.
		# 			#cv2.putText(image_alt, "Arrow tip", (x, y),image, 0.5, (255, 0, 0)) 
		# 			cv2.putText(image_alt, "Start " + string, (x, y),font, 0.4, (255, 0, ))		
		# 		else:
		# 			pass
		# 			# text on remaining co-ordinates.
		# 			#cv2.putText(image_alt, string, (x, y),image, 0.5, (0, 255, 0)) 
		# 			cv2.putText(image_alt, string, (x, y),font, 0.4, (0, 255, 0))
		# 	i = i + 1
	
	x = []
	y = []

	for i in contours:
		x_subgoals = []
		y_subgoals = []

		for j in i:
			for k in j:
				x_subgoals.append(k[0])
				y_subgoals.append(k[1])

		x_subgoals = x_subgoals[::5]
		y_subgoals = y_subgoals[::5]
		x.append(x_subgoals);
		y.append(y_subgoals);
	
	#print(x)
	#print(y)
	return (x,y)

def function_mode():
	# Set up the parameters for the Lissajous curve
	a = 200
	b = 100
	phase = 0

	# Set up the image and drawing parameters
	img_size = (500, 500)
	center = (img_size[0] // 2, img_size[1] // 2)
	scale = 0.25
	thickness = 2
	color = (255, 255, 255)

	# Define the function for the Lissajous curve
	def lissajous(t):
		x = a * np.cos(t)
		y = b * np.sin(2 * t)

		return (2*x, 2*y)

	# Create the image and initialize the drawing
	img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)
	cv2.line(img, (0, center[1]), (img_size[0], center[1]), color, thickness=thickness)
	cv2.line(img, (center[0], 0), (center[0], img_size[1]), color, thickness=thickness)

	# Draw the Lissajous curve
	t = np.linspace(0, 2*np.pi, 600)
	points = np.array([lissajous(ti) for ti in t], dtype=np.int32)
	points = np.round(points * scale + center).astype(np.int32)
	cv2.polylines(img, [points], False, color, thickness=thickness)

	x = []
	y = []
	ang = []

	def l_angle(t):
		theta = (pi/4)*np.sin(t) + pi/2
		return(theta)

	for i in t:
		ang.append(l_angle(i))


	for i in points:
		x.append(i[0])
		y.append(i[1])

	return (x,y,ang)

def pen(p1,p2):
	#PARAMS = {'mode':0,'p1':p1,'p2':p2}
	PARAMS = {'mode':0,'p1':p1,'p2':p2}
	response = requests.get(url= URL, params = PARAMS)

def vel(v1,v2,v3,kp):
	PARAMS = {'mode':1 ,'v1':int(kp*v1),'v2':int(kp*v2),'v3':int(kp*v3)}
	response = requests.get(url= URL, params = PARAMS)

def main():
	global x_goals, y_goals, theta_goals, hola_x, hola_y, hola_theta,mode, p1
	rospy.init_node('controller_node')
	signal.signal(signal.SIGINT, signal_handler)

	rospy.Subscriber('/detected_aruco',aruco_data,aruco_feedback_Cb)
	rospy.Subscriber('/task2_goals',PoseArray,task2_goals_Cb)
	#rospy.sleep(5)

	rate = rospy.Rate(20)

	contourPub = rospy.Publisher('/contours', String, queue_size=10)
	cData = String()

	penPub = rospy.Publisher('/penStatus', Int32, queue_size=10)
	penData = Int32()

	taskStatusPub = rospy.Publisher('/taskStatus', Int32, queue_size=10)
	taskStatus = Int32()
	
	#rospy.Subscriber('endSignal',Int32,endSignalCb) #optional

	

	x_g, y_g = [], []

	if(mode == 0):
		x_goals, y_goals = image_mode(r"/home/vishnu/catkin_ws/src/cv_basics/scripts/taskImages/smile.png")

		#x_goals, y_goals = [[100,450]], [[100,450]]
		cData.data = str([x_goals,y_goals])
		contourPub.publish(cData)
		if(p1 != 0):
			pen(0,0)
			penData.data = 0
			penPub.publish(penData)
			p1 = 0

		#PARAMS = {'mode':0,'p1':0,'p2':0}
		#conn.sendall(str.encode(msg))
		#response = requests.get(url= URL, params = PARAMS)
		rospy.sleep(0.2)
		#print(response)
	else:
		x_g, y_g, theta_goals = function_mode()
		x_goals.append(x_g)
		y_goals.append(y_g)

	


	goal_num = 0
	contour_num = 0
	
	taskStatus.data = 0   #indicating start of the run
	taskStatusPub.publish(taskStatus);

	while not rospy.is_shutdown():

		x = x_goals[contour_num][goal_num] + offset_x + trans_offset_x
		y = y_goals[contour_num][goal_num] + offset_y + trans_offset_y
		if(mode == 0):
			for i in range(len(x_goals[contour_num])):
				theta_goals.append(0);
		theta_d = theta_goals[goal_num]
		theta_d = math.atan2(math.sin(theta_d), math.cos(theta_d))

		print(str(x) + " " + str(y) + " " + str(theta_d))

		# Calculate Error from feedback
		e_x = x - hola_x
		e_y = y - hola_y
		e_theta = theta_d - hola_theta
		speed = 15*PI
		kp = 15

		while abs(e_x) > 1 or abs(e_y) > 1 or abs(e_theta*180/PI) > 4:
			print("ex: " + str(e_x) + " ey: " + str(e_y) + " etheta: " + str(e_theta))
			print("x: " + str(hola_x) + " y: " + str(hola_y) + " theta: " + str(hola_theta))


			ct = hola_theta
			x0, y0 = hola_x, hola_y
			diff = math.dist([hola_x, hola_y],[x, y])

			# Change the frame by using Rotation Matrix (If you find it required)
			c = np.matmul(np.linalg.inv([[math.cos(ct),-math.sin(ct)],[math.sin(ct), math.cos(ct)]]), [x - x0, y - y0])
			theta = math.atan2( c[1], c[0])
			#print("diff: " + str(diff) + " theta: " + str(theta))

			if(abs(e_x) > 1):
				vx = kp*math.cos(theta)*(abs(e_x))
			else:
				vx = 0

			if(abs(e_y) > 1):
				vy = 3*kp*math.sin(theta)*(abs(e_y))
			else:
				vy = 0

			if(abs(e_theta*180/PI)):
				omega = kp*speed*e_theta
			else:
				omega = 0

			print("vx: " + str(vx) + " vy: " + str(vy) + " omega: " + str(omega))
			# Find the required force vectors for individual wheels from it.(Inverse Kinematics)
			l = 0.205
			#r = 0.058 / 2
			r = 1
			mat = [[0, -1/r, l/r],
				   [math.sin(-60)/r, 0.5/r, l/r],
				   [math.sin(60)/r, 0.5/r, l/r]]
			
			res = np.matmul(mat, [-vy, -vx, -omega])
			#vf, vr, vl = inverse_kinematics(vx,vy,omega)
			print(res)
			#msg = str(int(kp*res[0])) + ',' + str(int(kp*res[1])) + ',' + str(int(kp*res[2])) + '\n'
			#print(msg)
			#PARAMS = {'mode':1 ,'v1':int(kp*vf),'v2':int(kp*vr),'v3':int(kp*vl)}
			#conn.sendall(str.encode(msg))
			#response = requests.get(url= URL, params = PARAMS)
			vel(res[0],res[1],res[2],2)
			# Modify the condition to Switch to Next goal (given position in pixels instead of meters
			#rate.sleep()
			e_x = x - hola_x
			e_y = y - hola_y
			e_theta = theta_d - hola_theta
			rate.sleep()

		if(goal_num == len(x_goals[contour_num]) - 1):
			if(mode == 0):
				#PARAMS = {'mode': 0, 'p1':0, 'p2':0}
				#response = requests.get(url= URL, params = PARAMS)
				if(p1 != 0):
					pen(0,0)
					p1 = 0
				print("Pen Up!")
				penData.data = 0
				penPub.publish(penData)

			print("All goals of contour " + str(contour_num + 1) + " reached!")
			cleanup()
			if(contour_num == len(x_goals) - 1):
				print("All the contours drawn!")
				taskStatus.data = 1
				taskStatusPub.publish(taskStatus);
				rospy.spin()
			else:
				contour_num += 1
				goal_num = 0
			
		else:
			print("Goal " + str(goal_num + 1) + " Reached!")
			if(goal_num == 0):
				#PARAMS = {'mode': 0, 'p1':1, 'p2':0}
				#response = requests.get(url= URL, params = PARAMS)
				if(p1 != 1):
					pen(1,0)
					p1 = 1
				#rospy.sleep(1);
				print("Pen Down!")
				penData.data = 1
				penPub.publish(penData)
			#cleanup()
			goal_num += 1
		#rospy.sleep(1.5)

if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass
