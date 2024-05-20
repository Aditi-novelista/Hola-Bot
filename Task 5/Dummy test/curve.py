import cv2
import numpy as np

# Load the image
img = cv2.imread("robotFinal.png")

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Perform Canny edge detection
edges = cv2.Canny(gray, 50, 150)

# Find contours in the edge image
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a black image to draw the contour on
contour_img = np.zeros_like(img)

# Loop over the contours
for i in range(len(contours)):
    # Calculate the area of each contour
    area = cv2.contourArea(contours[i])
    print("Area = ", end = " ")
    print(area)

   
   
# If the area is greater than a certain threshold, draw the contour with a thick line
    #if area < 500 and area>293:
    if area <= 17652:

    	cv2.drawContours(contour_img,contours[8],i,(255,255,255),thickness=2)

# Display the contour image
cv2.imshow("Contour Image", contour_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
