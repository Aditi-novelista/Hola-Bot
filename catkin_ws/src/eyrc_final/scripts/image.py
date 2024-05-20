import cv2
import numpy as np
import math
from random import randint
import sys

#################### PRE-PROCESSING ########################################
url = "/home/vishnu/catkin_ws/src/eyrc_final/scripts/images/robotFinal.png"
slice_value = 4
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

for i in range(len(final_list)):
	orig_copy = image_alt.copy()

	cv2.drawContours(orig_copy, final_list, i, (0,0,255), 3)
	cv2.imshow('contour ' + str(i), orig_copy)

	key = cv2.waitKey(0) & 0xFF

	if key == ord('y'):
		cv2.destroyAllWindows()


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

