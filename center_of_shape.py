import imutils
from cv2 import *

# load the image, convert it to grayscale, blur it slightly,
# and threshold it
# path: C:/Users/user/Desktop/The new ultimate/Computer science/PYTHON programming/ROV Software/
# uploading the image in natural unchanged colors
image = cv2.imread('C:/Users/user/Desktop/The new ultimate/Computer science/PYTHON programming/ROV Software/shapes_and_colors.png',-1)
# Converting the image to gray scale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# Introducing Gaussian blur or smoothening to reduce the amount of details and make it easier to process the image
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
# loop over the contours
for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    # Making sure the center in this case is not zero, because not all images have same values
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0,0

    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

# show the image
cv2.imshow("Image", image)
cv2.waitKey(0)
