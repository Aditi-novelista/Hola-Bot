import cv2
import numpy as np
# Read the input image
img = cv2.imread("robotFinal.png")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold the image
ret, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

# Invert the image
inv = cv2.bitwise_not(thresh)

# Apply the Zhang-Suen algorithm to skeletonize the image
size = np.size(inv)
skel = np.zeros(inv.shape, np.uint8)
kernel1 = np.ones((1,1),np.uint8)
kernel3 = np.ones((3,3),np.uint8)
kernel5 = np.ones((5,5),np.uint8)

ret, inv = cv2.threshold(inv, 10, 255, 0)

element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
done = False

while(not done):
    eroded = cv2.erode(inv, element)
    temp = cv2.dilate(eroded, element)
    temp = cv2.subtract(inv, temp)
    skel = cv2.bitwise_or(skel, temp)
    inv = eroded.copy()

    zeros = size - cv2.countNonZero(inv)
    if zeros == size:
        done = True

opening = cv2.morphologyEx(skel,cv2.MORPH_OPEN,kernel1)
closing = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel5)
# Display the skeletonized image
#image_path = r'/home/amit/Documents/GitHub/e-yantra'
cv2.imshow("Skeletonized Image", skel)
cv2.imshow("Skel and open", opening)
cv2.imshow("Skel and close", closing)
#cv2.imshow("Threshold Image", thresh)
#cv2.imwrite("skel.png",skel)
cv2.waitKey(0)
cv2.destroyAllWindows()

