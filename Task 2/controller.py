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

# Team ID:		[ Team-ID ]
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

from geometry_msgs.msg import Wrench		# Message type used for publishing force vectors
from geometry_msgs.msg import PoseArray	# Message type used for receiving goals
from geometry_msgs.msg import Pose2D		# Message type used for receiving feedback

import time
import math		# If you find it useful

from tf.transformations import euler_from_quaternion	# Convert angles

################## GLOBAL VARIABLES ######################

PI = 3.14

x_goals = []
y_goals = []
theta_goals = []

hola_x = 0
hola_y = 0
hola_theta = 0

right_wheel_pub = None
left_wheel_pub = None
front_wheel_pub = None


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

def inverse_kinematics():
	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Use the target velocity you calculated for the robot in previous task, and
	#	Process it further to find what proportions of that effort should be given to 3 individuals wheels !!
	#	Publish the calculated efforts to actuate robot by applying force vectors on provided topics
	############################################
	pass

def main():
	global x_goals, y_goals, theta_goals, hola_x, hola_y, hola_theta
	rospy.init_node('controller_node')
	signal.signal(signal.SIGINT, signal_handler)

	# NOTE: You are strictly NOT-ALLOWED to use "cmd_vel" or "odom" topics in this task
	#	Use the below given topics to generate motion for the robot.
	right_wheel_pub = rospy.Publisher('/right_wheel_force', Wrench, queue_size=10)
	front_wheel_pub = rospy.Publisher('/front_wheel_force', Wrench, queue_size=10)
	left_wheel_pub = rospy.Publisher('/left_wheel_force', Wrench, queue_size=10)

	right_vel = Wrench()
	left_vel = Wrench()
	front_vel = Wrench()

	rospy.Subscriber('detected_aruco',Pose2D,aruco_feedback_Cb)
	rospy.Subscriber('task2_goals',PoseArray,task2_goals_Cb)
	rospy.sleep(5)

	rate = rospy.Rate(100)

	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Make use of the logic you have developed in previous task to go-to-goal.
	#	-> Extend your logic to handle the feedback that is in terms of pixels.
	#	-> Tune your controller accordingly.
	# 	-> In this task you have to further implement (Inverse Kinematics!)
	#      find three omni-wheel velocities (v1, v2, v3) = left/right/center_wheel_force (assumption to simplify)
	#      given velocity of the chassis (Vx, Vy, W)
	#
	#x = 150
	#y = 150
	#theta_d = PI/4

	right_vel.force.y = 0
	right_vel.force.z = 0

	left_vel.force.y = 0
	left_vel.force.z = 0

	front_vel.force.y = 0
	front_vel.force.z = 0

	goal_num = 0

	while not rospy.is_shutdown():

		x = x_goals[goal_num]
		y = y_goals[goal_num]
		theta_d = theta_goals[goal_num]
		theta_d = math.atan2(math.sin(theta_d), math.cos(theta_d))

		# Calculate Error from feedback
		e_x = x - hola_x
		e_y = y - hola_y
		e_theta = theta_d - hola_theta
		speed = 4*PI
		kp = 3.5

		while abs(e_x) > 0 or abs(e_y) > 0 or abs(e_theta*180/PI) >= 5:
			#print("ex: " + str(e_x) + " ey: " + str(e_y) + " etheta: " + str(e_theta))
			#print("x: " + str(hola_x) + " y: " + str(hola_y) + " theta: " + str(hola_theta))
			ct = hola_theta
			x0, y0 = hola_x, hola_y
			diff = math.dist([hola_x, hola_y],[x, y])

			# Change the frame by using Rotation Matrix (If you find it required)
			c = np.matmul(np.linalg.inv([[math.cos(ct),-math.sin(ct)],[math.sin(ct), math.cos(ct)]]), [x - x0, y - y0])
			theta = math.atan2( c[1], c[0])
			#print("diff: " + str(diff) + " theta: " + str(theta))

			# Calculate the required velocity of bot for the next iteration(s)
			vx = kp*math.cos(theta)*diff
			vy = kp*math.sin(theta)*diff
			omega = kp*speed*(theta_d - ct)
			#print("vx: " + str(vx) + " vy: " + str(vy) + " omega: " + str(omega))

			# Find the required force vectors for individual wheels from it.(Inverse Kinematics)
			l = 0.17483
			mat = [[0, -1, l],
				   [math.sin(-60), 0.5, l],
				   [math.sin(60), 0.5, l]]
			
			res = np.matmul(mat, [-vy, -vx, -omega])
			#print(res)

			# Apply appropriate force vectors
			#print("------------------------------------------")
			front_vel.force.x = kp*res[0]
			right_vel.force.x = kp*res[1]
			left_vel.force.x = kp*res[2]

			front_wheel_pub.publish(front_vel)
			right_wheel_pub.publish(right_vel)
			left_wheel_pub.publish(left_vel)
		

		# Modify the condition to Switch to Next goal (given position in pixels instead of meters
			rate.sleep()
			e_x = x - hola_x
			e_y = y - hola_y
			e_theta = theta_d - hola_theta

		front_vel.force.x = 0
		right_vel.force.x = 0
		left_vel.force.x = 0

		front_wheel_pub.publish(front_vel)
		right_wheel_pub.publish(right_vel)
		left_wheel_pub.publish(left_vel)

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
		main()
	except rospy.ROSInterruptException:
		pass

