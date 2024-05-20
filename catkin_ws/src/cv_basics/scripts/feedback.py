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
import numpy as np				# If you find it required
import rospy 				
from sensor_msgs.msg import Image 	# Image is the message type for images in ROS
from cv_bridge import CvBridge	# Package to convert between ROS and OpenCV Images
import cv2				# OpenCV Library
import math				# If you find it required
from geometry_msgs.msg import Pose2D	# Required to publish ARUCO's detected position & orientation

############################ GLOBALS #############################
pi = 3.14159265358973
width, height = 500, 500
get_frame = None
corners_final = {}

##################### FUNCTION DEFINITIONS #######################

# NOTE :  You may define multiple helper functions here and use in your code


def callback(data):
	#print('callback called')
	# Bridge is Used to Convert ROS Image message to OpenCV image
	global pi, get_frame, corners_final, width, height
	aruco_publisher = rospy.Publisher('detected_aruco', Pose2D, queue_size=10)
	aruco_msg = Pose2D()

	br = CvBridge()
	#rospy.loginfo("receiving camera frame")
	get_frame = br.imgmsg_to_cv2(data, "mono8")		# Receiving raw image in a "grayscale" format
	#current_frame = cv2.resize(get_frame, (500, 500), interpolation = cv2.INTER_LINEAR)

	arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
	arucoParams = cv2.aruco.DetectorParameters_create()
	(corners, ids, rejected) = cv2.aruco.detectMarkers(get_frame, arucoDict, parameters=arucoParams)
	
	# ARUCO MARKERS CORNERS DETECTION 
	#
	#			ARENA
	#
	# 0--1---------------------0--1
	# | 8|					   |10|
	# 3--2                     3--2
	# |							  |
	# |			    ^		  	  |
	# |			   / \ 	 	      |
	# |			  /   \			  |
	# |			 /  15 \		  |
	# |			---------		  |
	# |							  |
	# |							  |
	# 0--1                     0--1
	# | 4|					   |12|
	# 3--2---------------------3--2




	if len(corners_final) == 0:
		#print(ids)
		#print(corners)
		for i in range(len(ids)):
			#corners_final[ids[i][0]] = [(corners[i][0][0][0] + corners[i][0][2][0])/2,(corners[i][0][0][1] + corners[i][0][2][1])/2]
			corners_final[ids[i][0]] = [corners[i][0].tolist()]
			#print(i, corners[i])
		print(corners_final)

	#pts1 = np.float32([corners_final[10],corners_final[8],corners_final[4],corners_final[12]])
	pts1 = np.float32([corners_final[8][0][0],corners_final[10][0][1],corners_final[4][0][3],corners_final[12][0][2]])
	pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
	matrix = cv2.getPerspectiveTransform(pts1,pts2)
	imgOutput = cv2.warpPerspective(get_frame,matrix,(width,height))

	#print(ids)
	(corners2, ids2, rejected) = cv2.aruco.detectMarkers(imgOutput, arucoDict, parameters=arucoParams)
	text = ''
	if(ids2 != None):
		k = np.where(ids2 == [15])
		k = k[0][0]
		#print(k[0])
		x_mid = (corners2[k][0][0][0] + corners2[k][0][2][0])/2
		y_mid = (1000 - corners2[k][0][0][1] - corners2[k][0][2][1])/2
		theta = math.atan2(corners2[k][0][0][1] - corners2[k][0][1][1],corners2[k][0][1][0] - corners2[k][0][0][0])
		#print(x_mid, y_mid, 57.29577951*math.atan2(corners[0][0][3][1] - corners[0][0][0][1],corners[0][0][1][0] - corners[0][0][3][0]))
		#print("----------------------------------------")
		aruco_msg.x = x_mid
		aruco_msg.y = y_mid
		aruco_msg.theta = theta
		aruco_publisher.publish(aruco_msg)
		text = 'x:' + str(x_mid) + ' , y:' + str(y_mid) + ' , w:' + str(theta*180/pi)[0:4]
		print("x: " + str(x_mid) + " y: " + str(y_mid) + " theta: " + str(theta*180/pi))
	#print(corners)
	else:
		text = 'x: - ' + ' , y: - ' + ' , w: - '
		print('Bot could not be detected')

	cv2.putText(imgOutput, text,(40,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0),1,cv2.LINE_AA)
	cv2.imshow("test",imgOutput)
	if cv2.waitKey(1) & 0xFF == ord('q'):  
		print('closing')
      
def main():
	rospy.init_node('aruco_feedback_node')  
	rospy.Subscriber('usb_cam/image_rect', Image, callback)

	rospy.spin()
  
if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass