#!/usr/bin/env python3

from time import sleep
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import PoseArray
import numpy as np

pi = 3.14159265358973
hola_x = 0
hola_y = 0
hola_theta = 0

x_goals, y_goals, theta_goals = [0,1,-1,0,0], [1,-1,-1,1,-1], [0, 0, 0, 0, 0]
#x_goals, y_goals, theta_goals = [1,-1,-1,1,0], [1,1,-1,-1,0], [0.785, 2.335, -2.335, -0.785, 0]
#x_goals, y_goals, theta_goals = [1,-1,-1,1,0], [1,1,-1,-1,0], [0, pi/2, pi, 3*pi/2, 2*pi]
#x_goals, y_goals, theta_goals = [1,0,0,0,1], [0,1,0,0,0], [0, 0, 0, 3, -3]
#x_goals, y_goals, theta_goals = [2, 1, 0 ,-1 ,-2, -1, 0, 1, 0], [0, 1, 2, 1, 0, -1, -2, -1, 0], [0, pi/4, pi/2, 3*pi/4, pi, -3*pi/4, -pi/2, -pi/4, 0]
#x_goals, y_goals, theta_goals = [0,10,-10,0,0], [10,-10,-10,10,-10], [0, 0, 0, 0, 0]
#x_goals = y_goals = theta_goals = []

def odometryCb(data):
	global hola_x, hola_y, hola_theta
	efq_list = [data.pose.pose.orientation.x, data.pose.pose.orientation.y,
				data.pose.pose.orientation.z, data.pose.pose.orientation.w]
	roll, pitch, hola_theta = euler_from_quaternion(efq_list)
	hola_x, hola_y = data.pose.pose.position.x, data.pose.pose.position.y

def task1_goals_Cb(msg):
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

def main():
	global hola_x, hola_y, hola_theta, pi, x_goals, y_goals, theta_goals

	rospy.init_node('controller', anonymous=True)
	
	cmd_vel_topic = '/cmd_vel'
	pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)
	position_topic = '/odom'
	odomsub = rospy.Subscriber(position_topic, Odometry, odometryCb)
	rospy.Subscriber('/task1_goals', PoseArray, task1_goals_Cb)

	#delay added for giving sufficient time for the nodes to connect and callback function to return data
	rospy.sleep(5)

	vel = Twist()
	vel.linear.x = 0
	vel.linear.y = 0
	vel.linear.z = 0
	vel.angular.x = 0
	vel.angular.y = 0
	vel.angular.z = 0
	pub.publish(vel)

	goal_num = 0

	while not rospy.is_shutdown():
		x_d = x_goals[goal_num]
		y_d = y_goals[goal_num]
		theta_d = theta_goals[goal_num]
		go_to_goal_pose(x_d, y_d, theta_d)
		#print("Pose reached!")
		#print("current x : " + str(hola_x) + " current y : " + str(hola_y) + " Current theta: " + str(hola_theta * 180/pi))
		if(goal_num == len(x_goals) - 1):
			rospy.spin()
			#rospy.spin()
			#print("All goals reached")
		else:
			goal_num += 1
		rospy.sleep(1.5)

def go_to_goal_pose(x, y, theta_d):
	global  hola_x, hola_y, hola_theta, pi

	theta_d = math.atan2(math.sin(theta_d), math.cos(theta_d))

	e_x = x - hola_x
	e_y = y - hola_y
	e_theta = theta_d - hola_theta
	speed = 2*pi
	max_vel = 3

	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
	vel = Twist()
	rate = rospy.Rate(100)
	vel.linear.z = 0
	vel.angular.x = 0
	vel.angular.y = 0

	while abs(e_x) >= 0.01 or abs(e_y) >= 0.01 or abs(e_theta) >= 0.01:
		ct = hola_theta
		x0, y0 = hola_x, hola_y
		diff = math.dist([hola_x, hola_y],[x, y])
		c = np.matmul(np.linalg.inv([[math.cos(ct),-math.sin(ct)],[math.sin(ct), math.cos(ct)]]), [x - x0, y - y0])
		theta = math.atan2( c[1], c[0])
		diff = min(5, diff)

		vel.linear.x = max_vel*math.cos(theta)*diff
		vel.linear.y = max_vel*math.sin(theta)*diff
		vel.angular.z = speed*(theta_d - ct)
		pub.publish(vel)
		#print("x: " + str(hola_x) + " y: " + str(hola_y) + " theta: " + str(hola_theta) + " ex: " + str(e_x) + " ey: " + str(e_y))
		rate.sleep()
		e_x = x - hola_x
		e_y = y - hola_y
		e_theta = theta_d - hola_theta

	vel.linear.x = 0
	vel.linear.y = 0
	vel.linear.z = 0
	vel.angular.x = 0
	vel.angular.y = 0
	vel.angular.z = 0
	pub.publish(vel)

if __name__ == "__main__":
	try:
		main()
	except rospy.ROSInterruptException:
		pass