from ColorDetection import ColorLabeler
from ShapeDetection import ShapeDetector
import imutils
import cv2

# 'C:/Users/user/Desktop/The new ultimate/Computer science/PYTHON programming/ROV Software/shapes_and_colors.jpg'
# 'C:/Users/user/Desktop/The new ultimate/Robotics and mechatronics/UnderWater '
#    'ROV/ROV2018MizuchyVody/ROVsoftware/TailSection2.jpg'
image = cv2.imread(
    'C:/Users/user/Desktop/The new ultimate/Robotics and mechatronics/UnderWater '
    'ROV/ROV2018MizuchyVody/ROVsoftware/TailSection1.jpg', -1)

resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# blur the resized image slightly, then convert it to both
# grayscale and the L*a*b* color spaces
blurred = cv2.GaussianBlur(resized, (5, 5), 0)
gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
# lab???
# THRESH_BINARY
# Tweak the args
# Understand the code more

"""cv2.imshow("Image", blurred)
cv2.waitKey(0)"""
cv2.imshow("Image", lab)
cv2.waitKey(0)
cv2.imshow("Image", gray)
cv2.waitKey(0)
cv2.imshow("Image", thresh)
cv2.waitKey(0)
# find contours in the thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

# initialize the shape detector and color labeler in initial shape and initial color
iShape = ShapeDetector()
iColor = ColorLabeler()

# loop over the contours
for c in cnts:
    # compute the center of the contour
    M = cv2.moments(c)
    if M["m00"] !=0:
        cX = int((M["m10"] / M["m00"]) * ratio)
        cY = int((M["m01"] / M["m00"]) * ratio)
    else:
        cX = 0
        cY = 0

    # detect the shape of the contour and label the color
    shape = iShape.DetectTheShape(c)
    color = iColor.LabelTheColor(lab, c)

    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape and labeled
    # color on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")
    text = "{} {}".format(color, shape)
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.putText(image, text, (cX, cY),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)