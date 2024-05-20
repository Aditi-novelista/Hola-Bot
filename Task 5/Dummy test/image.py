import numpy as np
import cv2

#initialising the image
font = cv2.FONT_HERSHEY_COMPLEX
image = cv2.imread('robotFinal.png',cv2.FONT_HERSHEY_COMPLEX)
image 
image_alt = cv2.imread('robotFinal.png',cv2.IMREAD_COLOR)
image_gray = cv2.imread('robotFinal.png', cv2.IMREAD_GRAYSCALE) #image in grayscale

#eroding the image
#image_gray = 255 - image_gray
kernel = np.ones((3,3),np.uint8)
for i in range(0):
    image_gray = cv2.erode(image_gray, kernel) 

#resizing image
image_alt = cv2.resize(image_alt, (500,500))
image_gray = cv2.resize(image_gray, (500,500))

# Converting image to a binary image
# ( black and white only image).
_, threshold = cv2.threshold(image_gray, 110, 255, cv2.THRESH_BINARY)
  
# Detecting contours in image.
contours, _= cv2.findContours(threshold, cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
image_alt = 255-image_alt

#excluding the unessecary contours
contours = contours[1:]

#printing the required number of contours
print("Number of Contours: ",len(contours))
  
# Going through every contours found in the image.
for cnt in contours :
  
    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)
  
    # draws boundary of contours.
    cv2.drawContours(image_alt, contours, -1, (0, 255, 0), 5) 
    
  
    # Used to flatted the array containing
    # the co-ordinates of the vertices.
    n = approx.ravel() 
    i = 0
  
    for j in n :
        if(i % 2 == 0):
            x = n[i]
            y = n[i + 1]
  
            # String containing the co-ordinates.
            string = str(x) + " " + str(y) 
  
            if(i == 0):
                pass
                # text on topmost co-ordinate.
                #cv2.putText(image_alt, "Arrow tip", (x, y),image, 0.5, (255, 0, 0)) 
                cv2.putText(image_alt, "Start " + string, (x, y),font, 0.4, (255, 0, 0))
            else:
                pass
                # text on remaining co-ordinates.
                #cv2.putText(image_alt, string, (x, y),image, 0.5, (0, 255, 0)) 
                cv2.putText(image_alt, string, (x, y),font, 0.4, (0, 255, 0))
        i = i + 1
  
# Showing the final image.
cv2.imshow('Final Image', image_alt) 
cv2.waitKey(0)
