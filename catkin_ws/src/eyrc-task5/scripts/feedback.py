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
# Filename:		feedback.py
# Functions:
#			[ Comma separated list of functions in this file ]
# Nodes:		Add your publishing and subscribing node


######################## IMPORT MODULES ##########################

from glob import glob
from matplotlib.pyplot import imshow
import numpy				# If you find it required
import rospy 				
from sensor_msgs.msg import Image 	# Image is the message type for images in ROS
from cv_bridge import CvBridge	# Package to convert between ROS and OpenCV Images
import cv2				# OpenCV Library
import math				# If you find it required
from geometry_msgs.msg import Pose2D	# Required to publish ARUCO's detected position & orientation

############################ GLOBALS #############################
pi = 3.14159265358973

#aruco_img = cv2.imread('/home/vishnu/catkin_ws/src/eyrc-task2/meshes/ARUCO_15.png')

##################### FUNCTION DEFINITIONS #######################

# NOTE :  You may define multiple helper functions here and use in your code
print('callback called')

def callback(data):
	# Bridge is Used to Convert ROS Image message to OpenCV image
	print('callback called')
	global pi
	aruco_publisher = rospy.Publisher('detected_aruco', Pose2D, queue_size=10)
	aruco_msg = Pose2D()

	br = CvBridge()
	#rospy.loginfo("receiving camera frame")
	get_frame = br.imgmsg_to_cv2(data, "mono8")		# Receiving raw image in a "grayscale" format
	current_frame = cv2.resize(get_frame, (500, 500), interpolation = cv2.INTER_LINEAR)
	############ ADD YOUR CODE HERE ############

	# INSTRUCTIONS & HELP : 
	#	-> Use OpenCV to find ARUCO MARKER from the IMAGE
	#	-> You are allowed to use any other library for ARUCO detection, 
	#        but the code should be strictly written by your team and
	#	   your code should take image & publish coordinates on the topics as specified only.  
	#	-> Use basic high-school geometry of "TRAPEZOIDAL SHAPES" to find accurate marker coordinates & orientation :)
	#	-> Observe the accuracy of aruco detection & handle every possible corner cases to get maximum scores !
	############################################

	cv2.imshow("test",current_frame)
      
def main():
	print('main called')
	rospy.init_node('aruco_feedback_node')  
	rospy.Subscriber('usb_cam/image_rect', Image, callback)

	#aruco_msg.x = 100
	#aruco_msg.y = 100
	#aruco_msg.theta = 1.47
	#aruco_publisher.publish(aruco_msg)

	rospy.spin()
 
if __name__ == '__main__':
	main()
