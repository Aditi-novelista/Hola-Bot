#!/usr/bin/env python3

'''
*
* Team Id:			1169
* Author List:		Aditi Phaneesh, Amit Chandrashekhar Hegde, Amogh Ananda, Vishnu Prakash Bharadwaj
* Filename:			controller.py
* Theme:			HolA Bot (HB)
* Functions:		signal_handler, cleanup, aruco_feedback_Cb, image_mode, function_mode,
*					control_pens, send_wheel_velocities, main
* Global Variables: PI, pi, x_goals, y_goals, theta_goals, hola_x, hola_y, hola_theta, pen1, MODE, URL
*
'''

from cv_basics.msg import aruco_data
from std_msgs.msg import String
from std_msgs.msg import Int32
import rospy, signal, sys, requests, numpy as np, time, math, cv2

#Global Variables.
PI = 3.14
pi = 3.14159265358973
x_goals, y_goals, theta_goals = [],[],[]
hola_x = 0
hola_y = 0
hola_theta = 0
pen1 = 0
pen2 = 0
MODE = 0
URL = "http://192.168.4.1/"


'''
*
* Function Name:	signal_handler
* Input:			sig -> signal
*					frame ->					
* Output:			Prints 'Clean-up' message. Calls cleanup function and then exits with exit code 0.
* Logic:			This is a signal handler function. This function is called when a program 
*					is terminated by "Ctr+C". SIGINT stands for Signal Interupt.
* Example Call:		This function is automatically called when bound with a specific signal.
*	
'''
def signal_handler(sig, frame): 
	#This function is called when a program is terminated by "Ctr+C" i.e. SIGINT signal 	
	print('Clean-up !')
	cleanup()
	sys.exit(0)

'''
*
* Function Name:	cleanup
* Input:			NONE
* Output:			Prints 'cleanup done' after successful <200 OK> response from HTTP server.
* Logic:			This function is used for stopping the bot and lifting the pens up, so that
*					the bot can run correctly in the next run. Used for avoiding intervention.
*					Please refer to the control_pens and send_wheel_velocities functions. In 
*					this function we are making all the wheel velocities zero and all the pens up.
* Example Call:		cleanup()
*
'''
def cleanup():
	global pen1
	#Stopping the wheels of the bot
	send_wheel_velocities(0,0,0,0)

	#Checking whether the pen is already up or not
	if(pen1 != 0):
		#Lifting both the pens up
		control_pens(0,0)
		pen1 = 0
	print("cleanup done")
	pass

'''
*
* Function Name:	aruco_feedback_Cb
* Input:			msg -> type: aruco_data
* Output:			None
* Logic:			This is a callback function. This function is called when new data arrives at
*	 				'/detected_aruco' topic from the 'aruco_feedback_node'. Changes the value of 
*					global variables hola_x, hola_y and hola_theta with x, y and theta recieved 
*					from '/detected_aruco' topic.
* Example Call:		This function is automatically called.
*
'''
def aruco_feedback_Cb(msg):
	global hola_x, hola_y, hola_theta
	#Setting the x, y and theta from the received data.
	hola_x = msg.x
	hola_y = msg.y
	hola_theta = msg.theta

'''
* Function Name: image_mode
*
* Input: 		image_file_path -> absolute path of the image which we want to draw
*
* Ouput:		Returns two lists, one containing the x coordinates, and the other containing the 
*				y coordinates that the robot must traverse through to draw the specified function.
*
* Logic:		The function reads the required image using openCV and makes two copies of it, one
*			 	in grayscale. The grayscale image is converted into a binary file and the binary 
*			 	file is converted to contours. The contours are non-intersecting curves which depict
*			 	the edges of the given image. Contours, which are essentially curves are broken down
*			 	into cartesian coordinates. The resulting cartesian coordinates can be be sent to 
*			 	x_goals and y_goals and are used by the robot to plot the required the image.
*
* Example Call:	x_goals,y_goals = image_mode('test.png')
'''
def image_mode(image_file_path):
	global slice_value
	#initialising the image
	font = cv2.FONT_HERSHEY_COMPLEX

	image = cv2.imread(image_file_path,0)
	ret,image = cv2.threshold(image,40,255,0)

	image_alt = cv2.imread(image_file_path,cv2.IMREAD_COLOR)
	image_gray = image

	#eroding the image
	image_gray = 255 - image_gray
	kernel = np.ones((3,3),np.uint8)
	for i in range(2):
		image_gray = cv2.erode(image_gray, kernel)

	#resizing image
	image_alt = cv2.resize(image_alt, (500,500))
	image_gray = cv2.resize(image_gray, (500,500))


	# Converting image to a binary image
	# ( black and white only image).
	_, threshold = cv2.threshold(image_gray, 110, 255, cv2.THRESH_BINARY)
	  
	# Detecting contours in image.
	contours, _= cv2.findContours(threshold, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

	#inverting the bits
	image_alt = 255-image_alt
	
	#Choosing only the required contours.
	final = contours[0:1] + contours[11:12] + contours[9:11] + contours[12:] + contours[7:8] + contours[2:3] + contours[4:5] + contours[1:2] + contours[6:7]
	contours = final

	x = []
	y = []

	for i in contours:
		x_subgoals = []
		y_subgoals = []

		for j in i:
			for k in j:
				x_subgoals.append(k[0])
				y_subgoals.append(500 - k[1])
		#Slicing contour values to get desired number of sub goals
		x_subgoals = x_subgoals[::slice_value]
		y_subgoals = y_subgoals[::slice_value]
		x.append(x_subgoals);
		y.append(y_subgoals);

	return (x,y)

'''
* Function Name: 	function_mode
*
* Input: 			None
*
* Ouput:			Returns three lists, one containing the x coordinates, one containing the y 
*					coordinates and the last containing the angles that the robot musttraverse through
*					to draw the specified function
*
* Logic:			The function takes the parameters for the Lissajous curve and using numpy cos 
*					and sine functions, it gives a specific point corresponding to the given value 
*					of t [0,2*pi]. The corresponding point is returned and stored in a numpy array.
*					The array of points is then converted to an image using openCV. The image that 
*					results from openCV is the required lissajous curve. The points of this curve 
*					is then sent to x_goals, y_goals and theta_goals and is plotted by the HolA bot.
*
* Example Call:		x_goals,y_goals,theta_goals = function_mode()
'''
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

	# Defining the function for the Lissajous curve
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
		#Defining theta equation.
		theta = (pi/4)*np.sin(t) + pi/2
		return(theta)

	for i in t:
		#Appending each angle to the ang list.
		ang.append(l_angle(i))


	for i in points:
		#Appending x and y co-ordinates
		x.append(i[0])
		y.append(i[1])

	return (x,y,ang)

'''
*
* Function Name:	control_pens
* Input:			pen1, pen2 -> Integers - either 0 or 1, to indicate whether pen1 and pen2
*					should be up or down. 0 represents up and 1 represents down.
* Output:			None
* Logic:			This function is used for controlling the pen positions of the holA bot.
*					In the parameters, the "mode" parameter indicates what parameter of the bot
*					we are controlling. mode = 0 is used for controlling pens position.
*					"p1" and "p2" are used for controlling the pen positons of pen 1 and pen 2
*					respectively.
* Example Call:		control_pens(1,0)
*					This lowers the pen 1 and lifts the pen 2. This is used in image mode.
*					control_pens(1,1)
*					This lowers both the pens. This is used for function mode.
'''
def control_pens(pen1,pen2):
	#mode 0 represents that we are controlling the pens.
	PARAMS = {'mode':0,'p1':pen1,'p2':pen2}
	#Submitting a HTTP-request
	response = requests.get(url= URL, params = PARAMS)

'''
*
* Function Name:	send_wheel_velocities
*
* Input:			v1,v2,v3 ->	Floating point numbers, v1, v2, v3 represent velocities of
*					front wheel, right wheel and left wheel respectively.
*					A -> Velocity scale factor. This is used for increasing velocity values by a certain factor.
*
* Output:			None
*
* Logic:			This function is used for controlling the wheel velocities of the hola bot.
*					In the parameters, the "mode" parameter indicates what parameter of the bot
*					we are controlling. mode = 1 is used for controlling wheel velocities. "v1"
*					"v2" and "v3" are used for controlling velocities of front wheel, right
*					wheel and left wheel respectively.
*
* Example Call:		send_wheel_velocities(20,-30,50,2)
*					The above call sends the 20, -30, 50 velocities to the esp-12E. Before sending,
*					the values are multiplied by the factor 2.
*
'''
def send_wheel_velocities(v1,v2,v3,A):
	#Sending whell velocity to the bot
	PARAMS = {'mode':1 ,'v1':int(A*v1),'v2':int(A*v2),'v3':int(A*v3)}
	response = requests.get(url= URL, params = PARAMS)

'''
*
* Function Name:	main
* Input:			None
* Output:			This is the main loop where all our side functions are called in order
*					control the bot.
* Logic:			This function calls the signal_handler whenever there is 'CTRL + C' signal
*					detected. Ros subscribers and publishers are defined in this section.
*					Defining the MODE, reading image/ generating function coordinates, generating
*					contours, reading the aruco feedback and calculating error in the position for
*					each point on contours and sending appropriate velocities are the primary goals
*					of this function.
* Example Call:		main()
*
'''
def main():
	global x_goals, y_goals, theta_goals, hola_x, hola_y, hola_theta,MODE, pen1

	#Initiating rospy controller_node
	rospy.init_node('controller_node')

	#Initiating a signal handler and binding it with the signal_handler function
	signal.signal(signal.SIGINT, signal_handler)

	#Subscribing for detected_aruco topic to get aruco feedback data
	rospy.Subscriber('/detected_aruco',aruco_data,aruco_feedback_Cb)

	#Publisher for publishing contours genrated by the image_mode function
	contourPub = rospy.Publisher('/contours', String, queue_size=10)
	cData = String()

	#Publisher for publishing pen up and down data
	penPub = rospy.Publisher('/penStatus', Int32, queue_size=10)
	penData = Int32()

	#Publisher for publishing the start and end of the task
	taskStatusPub = rospy.Publisher('/taskStatus', Int32, queue_size=10)
	taskStatus = Int32()
	
	#Rate variable required for running rate at 20 hertz
	rate = rospy.Rate(20)
	
	#checking whether the MODE is set to image mode or function mode
	if(MODE == 0):
		#MODE = 0 represents image mode and reads the image file from the given path and populates the x_goals and y_goals
		x_goals, y_goals = image_mode(r"/home/vishnu/catkin_ws/src/cv_basics/scripts/taskImages/snapchat.png")

		#publishing the contours to ros
		cData.data = str([x_goals,y_goals])
		contourPub.publish(cData)

		#Generating list of theta = 0 values equal to the length of each contours in x_goals and y_goals
		#We could have neglected this part if we had placed the pen exactly at the center of the bot.
		#But we have placed the pen on the sides due to space constraint, hence we are defining theta as zero.
		for cnt in x_goals:
			theta_g = []
			for i in range(len(cnt)):
				theta_g.append(0);
			theta_goals.append(theta_g)


		#Checking if pen is already down or not, and forcefully lifting them up.
		if(pen1 != 0):
			control_pens(0,0)

			#Submitting pen data
			penData.data = 0
			penPub.publish(penData)
			pen1 = 0
			
	else:
		#MODE = 1 represents image mode function mode and hence calls function_mode function to generate x, y and theta goals
		x_g, y_g = [], []
		x_g, y_g, theta_goals = function_mode()
		x_goals.append(x_g)
		y_goals.append(y_g)
		


	#Initializing goal number and contour number to 0
	goal_num = 0
	contour_num = 0
	
	#Indicating the start of task
	taskStatus.data = 0   #indicating start of the run
	taskStatusPub.publish(taskStatus);

	#Executing till the shutdown rospy
	while not rospy.is_shutdown():

		#Assigning current x and y goals to the contour points 
		x = x_goals[contour_num][goal_num] + offset_x + trans_offset_x
		y = y_goals[contour_num][goal_num] + offset_y + trans_offset_y

		#Assigning current angle values
		theta_d = theta_goals[goal_num]

		#Forcefully converting the angle to lie between (-pi,pi)
		theta_d = math.atan2(math.sin(theta_d), math.cos(theta_d))

		print(str(x) + " " + str(y) + " " + str(theta_d))

		# Calculate Error from feedback
		e_x = x - hola_x
		e_y = y - hola_y
		e_theta = theta_d - hola_theta

		#Proportional gain constants for x, y and theta
		kpx = 10
		kpy = kpx*3
		kpt = kpx*15*PI

		#Iterating till the absolute value of erros are above the tolerance values
		while abs(e_x) > 1 or abs(e_y) > 1 or abs(e_theta*180/PI) > 4:
			print("ex: " + str(e_x) + " ey: " + str(e_y) + " etheta: " + str(e_theta))
			print("x: " + str(hola_x) + " y: " + str(hola_y) + " theta: " + str(hola_theta))

			#Current theta(ct)
			ct = hola_theta

			#Current x and y coordinates
			x0, y0 = hola_x, hola_y

			#Applying rotation matrix to get the coordinates of the goal in the new system of axes
			c = np.matmul(np.linalg.inv([[math.cos(ct),-math.sin(ct)],[math.sin(ct), math.cos(ct)]]), [x - x0, y - y0])
			
			#Angle in the new system equals tan inverse of y / x
			theta = math.atan2( c[1], c[0])

			#Checking whether the error in each variable has reached the tolerance value and then making the respective parameter 0

			if(abs(e_x) > 1):
				vx = kpx*math.cos(theta)*(abs(e_x))
			else:
				vx = 0

			if(abs(e_y) > 1):
				vy = kpy*math.sin(theta)*(abs(e_y))
			else:
				vy = 0

			if(abs(e_theta*180/PI)):
				omega = kpt*e_theta
			else:
				omega = 0

			print("vx: " + str(vx) + " vy: " + str(vy) + " omega: " + str(omega))

			#Distance between center of the bot and an extreme arm
			l = 0.205 #in meters

			#inverse of coefficient matrix from the kinematics equations
			mat = [[0, -1, l],
				   [math.sin(-60), 0.5, l],
				   [math.sin(60), 0.5, l]]


			#Multiplying the inverse matrix and vx, vy and omega parameters to get the desired wheel velocities
			velocities = np.matmul(mat, [-vy, -vx, -omega])

			#Sending the wheel velocities over HTTP request
			send_wheel_velocities(velocities[0],velocities[1],velocities[2],1)


			#calculating errors in x, y and theta
			e_x = x - hola_x
			e_y = y - hola_y
			e_theta = theta_d - hola_theta
			
			#Maintaing the loop rate
			rate.sleep()

		#Checking if last goal of the contour is reached or not
		if(goal_num == len(x_goals[contour_num]) - 1):

			#In image mode, we have to lift the pen from one contour to another
			if(MODE == 0):
				if(pen1 != 0):
					control_pens(0,0)
					pen1 = 0
				print("Pen Up!")
				penData.data = 0
				penPub.publish(penData)

			print("All goals of contour " + str(contour_num + 1) + " reached!")
			cleanup()

			#Checking if the goal reached was the last goal of the last contour
			if(contour_num == len(x_goals) - 1):
				print("All the contours drawn!")

				#Sending task status 1, indicating end of the run
				taskStatus.data = 1
				taskStatusPub.publish(taskStatus);
				rospy.spin()
			else:
				#if the current contour is not the last contour, then moving on to next contour
				contour_num += 1
				#resetting the goal number to 1
				goal_num = 0
			
		else:
			#Printig "Goal Reached" at the end of the run.
			print("Goal " + str(goal_num + 1) + " Reached!")
			if(goal_num == 0):
				if(pen1 != 1):
					control_pens(1,0)
					pen1 = 1
				print("Pen Down!")
				#At the end of the run setting penDown status.
				penData.data = 1
				#Publishing the penData.
				penPub.publish(penData)
				
			
			#Iterarting each goal number to next goal.
			goal_num += 1

if __name__ == "__main__":
	try:
		#Calling main function
		main()
	except rospy.ROSInterruptException:
		#Exception for operations that interrupted.
		pass
