#!/usr/bin/env python3

from cv_basics.msg import aruco_data		# Message type used for receiving feedback
from std_msgs.msg import String
from std_msgs.msg import Int32
import requests
import time
import math		# If you find it useful
import cv2
import rospy
import signal		# To handle Signals by OS/user
import sys		# To handle Signals by OS/user
import numpy as np
import socket
from random import randint

PI = 3.14 				# Approximate value of Pi
pi = 3.14159265358973	# Accurate value of Pi

x_goals, y_goals, theta_goals = [],[],[]

hola_x = 0
hola_y = 0
hola_theta = 0
pen1 = 0
pen2 = 0
mode = 1
slice_value = 4

offset_x = 0
offset_y = 0
trans_offset_x = 0
trans_offset_y = 0
URL = "http://192.168.4.1/"

def signal_handler(sig, frame):
	print('Clean-up !')
	cleanup()
	sys.exit(0)

def cleanup():
	global pen1
	send_wheel_velocities(0,0,0,0)
	if(pen1 != 0):
		control_pens(0,0)
		pen1 = 0
	print("cleanup done")
	pass

def aruco_feedback_Cb(msg):
	global hola_x, hola_y, hola_theta
	hola_x = msg.x
	hola_y = msg.y
	hola_theta = msg.theta

def image_mode(url):
	global slice_value
	#initialising the image
	finalSelection = False

	#initialising the image
	font = cv2.FONT_HERSHEY_COMPLEX

	image = cv2.imread(url,0)
	ret,image = cv2.threshold(image,40,255,0)

	image_alt = cv2.imread(url,cv2.IMREAD_COLOR)
	image_alt = cv2.resize(image_alt, (500,500))
	image_alt = 255 - image_alt

	image_gray = image
	blank = np.zeros((500, 500, 3), dtype = np.uint8)

	#eroding the image
	image_gray = 255 - image_gray
	kernel = np.ones((3,3),np.uint8)
	for i in range(2):
		image_gray = cv2.erode(image_gray, kernel)
	#resizing image
	image_gray = cv2.resize(image_gray, (500,500))



	# Converting image to a binary image
	# ( black and white only image).
	_ , threshold = cv2.threshold(image_gray, 110, 255, cv2.THRESH_BINARY)

	#################### CONTOUR DETECTION ######################################

	contours, _ = cv2.findContours(threshold, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

	#################### CONTOUR SELECTION ######################################
	final = []
	colours = []



	while(not finalSelection):

		print("CONTOUR SELECTION")
		print("")

		for i in range(len(contours)):
			orig_copy = image_alt.copy()

			rand_color = (randint(0,255),randint(0,255),randint(0,255))

			cv2.drawContours(orig_copy, contours, i, (0,0,255), 3)
			cv2.imshow('contour ' + str(i), orig_copy)

			key = cv2.waitKey(0) & 0xFF

			if key == ord('y'):
				final.append(contours[i])
				colours.append(rand_color)
				print("Contour " + str(i) + " selected.")
				cv2.destroyAllWindows()

			elif key == ord('q'):
				cv2.destroyAllWindows()
				exit(0)

			else:
				print("Contour " + str(i) + " not selected.")
				cv2.destroyAllWindows()

		blank_copy = blank.copy()
		print("Final contour list?")

		for i in range(len(final)):
			cv2.drawContours(blank_copy, final, i, colours[i], 1)

		cv2.imshow('Original image', image_alt)
		cv2.imshow('Final image ??? ', blank_copy)
		

		key = cv2.waitKey(0) & 0xFF

		if key == ord('y'):
			finalSelection = True
			print('Final contours list saved !')
			cv2.destroyAllWindows()

		elif key == ord('q'):
			cv2.destroyAllWindows()
			exit(0)
		else :
			final.clear()
			colours.clear()
			print('Contour list discarded! ')
			cv2.destroyAllWindows()

	print("Total no. of contours: " + str(len(final)))

	#################### CONTOUR SORTING ######################################
	#Contour sorting
	final_copy = final
	final_list = []
	final_list.append(final[0])
	#print(final_list[0][0][0])	
	final.pop(0)

	for i in range(len(final)):
		distance = math.dist([0,0],[500,500])
		count = 0
		elemIndex = 0

		for j in final:
			dist2 = math.dist([j[0][0][0], j[0][0][1]], [final_list[-1][0][0][0], final_list[-1][0][0][1]])
			if(dist2 < distance):
				elemIndex = count
				distance = dist2
			count += 1

		final_list.append(final[elemIndex])
		final.pop(elemIndex)


	print(len(final_list))
	#for i in final_list:
	#	print(i)
	'''
	for i in range(len(final_list)):
		orig_copy = image_alt.copy()

		cv2.drawContours(orig_copy, final_list, i, (0,0,255), 3)
		cv2.imshow('contour ' + str(i), orig_copy)

		key = cv2.waitKey(0) & 0xFF

		if key == ord('y'):
			cv2.destroyAllWindows()
	'''

	x = []
	y = []

	for i in final_list:
		x_subgoals = []
		y_subgoals = []

		for j in i:
			for k in j:
				x_subgoals.append(k[0])
				y_subgoals.append(500 - k[1])

		x_subgoals = x_subgoals[::slice_value]
		y_subgoals = y_subgoals[::slice_value]
		x.append(x_subgoals);
		y.append(y_subgoals);

	return (x,y)

def function_mode():
	phase_shift = -pi/2

	def r(t):
		return 60*np.ceil(4 - t/np.pi)*np.sin(2*t)

	def a(t):
		return t + np.pi/2

	def x_and_y(t):
		x = 0
		y = 0
		if t >= 0:
			x = r(t)*np.cos(a(t))
			y = r(t)*np.sin(a(t))
		else:
			y = 200*t

		return (x,y)

	def theta(t):
		val = 0
		if t >= 0:
			val = 2*t + np.pi/2  
		else:
			val = (t+1)*np.pi/2

		val += phase_shift
		return val


	img_size = (500, 500)
	center = (img_size[0] // 2, img_size[1] // 2)
	scale = 1
	thickness = 2
	color = (255, 255, 255)

	# Create the image and initialize the drawing
	img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)
	#cv2.line(img, (0, center[1]), (img_size[0], center[1]), color, thickness=thickness)
	#cv2.line(img, (center[0], 0), (center[0], img_size[1]), color, thickness=thickness)

	t = np.linspace(-1, 4*np.pi, 1000)
	points = np.array([x_and_y(ti) for ti in t], dtype=np.int32)
	points = np.round(points * scale + center).astype(np.int32)
	#cv2.polylines(img, [points], False, color, thickness=thickness)

	x = []
	y = []
	ang = []

	for i in t:
		ang.append(theta(i))

	for i in points:
		x.append(i[0])
		y.append(i[1])

	#print(x)
	#print(y)
	#print(ang)

	return (x,y,ang)

def control_pens(pen1,pen2):
	PARAMS = {'mode':0,'p1':pen1,'p2':pen2}
	response = requests.get(url= URL, params = PARAMS)

def send_wheel_velocities(v1,v2,v3,kp):
	PARAMS = {'mode':1 ,'v1':int(kp*v1),'v2':int(kp*v2),'v3':int(kp*v3)}
	response = requests.get(url= URL, params = PARAMS)

def main():
	global x_goals, y_goals, theta_goals, hola_x, hola_y, hola_theta,mode, pen1
	signal.signal(signal.SIGINT, signal_handler)
	rospy.init_node('controller_node')

	rospy.Subscriber('/detected_aruco',aruco_data,aruco_feedback_Cb)

	contourPub = rospy.Publisher('/contours', String, queue_size=10)
	cData = String()

	penPub = rospy.Publisher('/penStatus', Int32, queue_size=10)
	penData = Int32()

	taskStatusPub = rospy.Publisher('/taskStatus', Int32, queue_size=10)
	taskStatus = Int32()
	
	rate = rospy.Rate(20)

	

	if(mode == 0):
		x_goals, y_goals = image_mode(r"/home/aditi/catkin_ws/src/eyrc_final/scripts/images/download.jpeg")
		
		if(pen1 != 0):
			control_pens(0,0)
			pen1 = 0

		rospy.sleep(0.2)
		#print(response)
	else:
		#x_g, y_g = [], []
		x_g, y_g, theta_g = function_mode()
		x_goals.append(x_g)
		y_goals.append(y_g)
		theta_goals.append(theta_g)

		if(pen1 != 1):
			control_pens(1,1)
			pen1 = 1

	penData.data = 0
	penPub.publish(penData)

	cData.data = str([x_goals,y_goals])
	contourPub.publish(cData)

	goal_num = 0
	contour_num = 0
	
	taskStatus.data = 0   #indicating start of the run
	taskStatusPub.publish(taskStatus);

	if(mode == 0):
		for cnt in x_goals:
			theta_g = []
			for i in range(len(cnt)):
				theta_g.append(0);
			theta_goals.append(theta_g)

	no_of_rotations = 0
	prev_theta = 0

	while not rospy.is_shutdown():


		x = x_goals[contour_num][goal_num] + offset_x + trans_offset_x
		y = y_goals[contour_num][goal_num] + offset_y + trans_offset_y
		
		theta_d = theta_goals[contour_num][goal_num]

		# Uncomment the below line to convert the angles to get in the range (-pi,pi]
		#theta_d = math.atan2(math.sin(theta_d), math.cos(theta_d))

		#print(str(x) + " " + str(y) + " " + str(theta_d))

		# Calculate Error from feedback
		ct = hola_theta
		x0, y0 = hola_x, hola_y
		c = np.matmul(np.linalg.inv([[math.cos(ct),-math.sin(ct)],[math.sin(ct), math.cos(ct)]]), [x - x0, y - y0])
		e_x = c[0]
		e_y = c[1]
		e_theta = theta_d - (hola_theta + no_of_rotations*2*pi)
		speed = 15*PI
		kp = 11

		while abs(e_x) > 3 or abs(e_y) > 3 or abs(e_theta*180/PI) > 4:
			#print("ex: " + str(e_x) + " ey: " + str(e_y) + " etheta: " + str(e_theta))
			print("x: " + str(hola_x) + " y: " + str(hola_y) + " theta: " + str(hola_theta))

			ct = hola_theta

			if (ct - prev_theta) > pi:
				no_of_rotations -= 1
			elif (ct - prev_theta) < -pi:
				no_of_rotations += 1
				
			x0, y0 = hola_x, hola_y
			#diff = math.dist([hola_x, hola_y],[x, y])

			# Change the frame by using Rotation Matrix (If you find it required)
			c = np.matmul(np.linalg.inv([[math.cos(ct),-math.sin(ct)],[math.sin(ct), math.cos(ct)]]), [x - x0, y - y0])
			theta = math.atan2( c[1], c[0])
			#print("diff: " + str(diff) + " theta: " + str(theta))

			vx = kp*e_x

			vy = 3*kp*e_y

			omega = kp*speed*e_theta

			l = 0.205
			mat = [[0, -1, l],
				   [math.sin(-60), 0.5, l],
				   [math.sin(60), 0.5, l]]

			velocities = np.matmul(mat, [-vy, -vx, -omega])
			send_wheel_velocities(velocities[0],velocities[1],velocities[2],3)

			e_x = c[0]#x - hola_x
			e_y = c[1]#y - hola_y
			e_theta = theta_d - (ct + no_of_rotations*2*pi)
			prev_theta = ct
			rate.sleep()

		if(goal_num == len(x_goals[contour_num]) - 1):
			if(mode == 0):
				if(pen1 != 0):
					control_pens(0,0)
					pen1 = 0
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
				if(pen1 != 1):
					control_pens(1,0)
					pen1 = 1
				print("Pen Down!")
				penData.data = 1
				penPub.publish(penData)
			goal_num += 1

if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass
