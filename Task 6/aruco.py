#!/usr/bin/env python3

'''
*
* Team Id:			1169
* Author List:		Aditi Phaneesh, Amit Chandrashekhar Hegde, Amogh Ananda, Vishnu Prakash Bharadwaj
* Filename:			aruco.py
* Theme:			HolA Bot (HB)
* Functions:		callback,main
* Global Variables: pi,width,height,get_frame,corners_final
*
'''

from glob import glob
from matplotlib.pyplot import imshow
import numpy as np				
import rospy 				
from sensor_msgs.msg import Image 	# Image is the message type for images in ROS
from cv_bridge import CvBridge		# Package to convert between ROS and OpenCV Images
import cv2							# OpenCV Library
import math				
from cv_basics.msg import aruco_data# Required to publish ARUCO's detected position & orientation

#Global Variables.
pi = 3.14159265358973
width, height = 500, 500
get_frame = None
corners_final = {}

'''
*
* Function Name:	callback
* Input:			data -> data from the camera.				
* Output:			Gives the aruco data to controller.
* Logic:			Using OpenCv all 5 aruco markers are detected(4 corners and 1 bot).The arena is resized into 500*500px and Center of each 						aruco is caluclated and is published as deteted aruco.
* Example Call:		rospy.Subscriber('/usb_cam/image_rect', Image, callback) -> It is called whenever image_rect topic is subscribed.
*	
'''

def callback(data):

	
	global pi, get_frame, corners_final, width, height
	#Creating a publisher node.
	aruco_publisher = rospy.Publisher('/detected_aruco', aruco_data, queue_size=10)
	aruco_msg = aruco_data()
	
	
	# Bridge is Used to Convert ROS Image message to OpenCV image
	br = CvBridge()
	
	# Receiving raw image in a "grayscale" format
	get_frame = br.imgmsg_to_cv2(data, "mono8")	
		
	#Detecting aruco markers from camera feed.
	arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
	arucoParams = cv2.aruco.DetectorParameters_create()
	(corners, ids, rejected) = cv2.aruco.detectMarkers(get_frame, arucoDict, parameters=arucoParams)
	
	#To print the detetcted corner aruco markers.
	if len(corners_final) == 0:

		for i in range(len(ids)):
			corners_final[ids[i][0]] = [corners[i][0].tolist()]
			
		print(corners_final)

	#Storing all the corner(of id 8,10,4,12) and applying perspective transform.
	pts1 = np.float32([corners_final[8][0][0],corners_final[10][0][1],corners_final[4][0][3],corners_final[12][0][2]])
	pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
	matrix = cv2.getPerspectiveTransform(pts1,pts2)
	imgOutput = cv2.warpPerspective(get_frame,matrix,(width,height))


	(corners2, ids2, rejected) = cv2.aruco.detectMarkers(imgOutput, arucoDict, parameters=arucoParams)
	text = ''
	
	#If bot is detetcted(aruco of id 15)
	if(ids2 != None):
		k = np.where(ids2 == [15])
		k = k[0][0]
		#Finding the a,y and theta from the aruco marker.
		x_mid = (corners2[k][0][0][0] + corners2[k][0][2][0])/2
		y_mid = (1000 - corners2[k][0][0][1] - corners2[k][0][2][1])/2
		theta = math.atan2(corners2[k][0][0][1] - corners2[k][0][1][1],corners2[k][0][1][0] - corners2[k][0][0][0])
		
		#Storing each value of x,y and theta in aruco_msg for publishing.
		aruco_msg.x = x_mid
		aruco_msg.y = y_mid
		aruco_msg.theta = theta
		#Publishing the data.
		aruco_publisher.publish(aruco_msg)
		
		#To show the x,y and theta on the display window.
		text = 'x:' + str(x_mid) + ' , y:' + str(y_mid) + ' , w:' + str(theta*180/pi)[0:4]
		#Printign values of x,y and theta.
		print("x: " + str(x_mid) + " y: " + str(y_mid) + " theta: " + str(theta*180/pi))
	
	#If aruco marker is not detected.
	else:
		#To show the x,y and theta on the display window.
		text = 'x: - ' + ' , y: - ' + ' , w: - '
		print('Bot could not be detected')

	#To display the x,y and theta on the display window.
	cv2.putText(imgOutput, text,(40,30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0),1,cv2.LINE_AA)
	#Display window
	cv2.imshow("HB_1169_feedback",imgOutput)
	
	#To close the display window.
	if cv2.waitKey(1) & 0xFF == ord('q'):  
		print('closing')
 
'''
*
* Function Name:	main
* Input:			None.				
* Output:			Initializes 'aruco_feedback_node'and subsribes to image_rect topic. Calls the callback function.
* Logic:			None.
* Example Call:		main()
*	
'''     
def main():
	#Initializing node called 'aruco_feedback_node'
	rospy.init_node('aruco_feedback_node') 
	#Subscribing to image_rect topic(which gives image without fish-eye effect) 
	rospy.Subscriber('/usb_cam/image_rect', Image, callback)
	
	#Go into an infinite loop until it receives a shutdown signal
	rospy.spin()
  
if __name__ == '__main__':
	try:
		#Calling main function
		main()
	except rospy.ROSInterruptException:
		#Exception for operations that interrupted.
		pass
