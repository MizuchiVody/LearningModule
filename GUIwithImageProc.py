# Import the necessary packages
from tkinter import *  # Make sure you're using Python 3!!!
import datetime
from cv2 import *
from sys import *
from time import *
from serial import *
from numpy import *
from imutils import *
import daytime
from scipy.spatial import distance as dist
from collections import OrderedDict

root = Tk()
label = Label(root)
states = []
checklist = ['Prepower', 'Power Up', 'Failed Bubble Check', 'Lunch', 'Lost Communication', 'ROV retrieval',
             'Demobilization']

for i in range(0, 6):
    var = IntVar()
    chk = Checkbutton(root, text=checklist[i], variable=var)
    chk.pack(side=TOP)
    states.append(var.get())

b = Button(root, text="OK", command=root.quit).pack()
root.mainloop()

cam = VideoCapture(2)  # Capture the video from camera on port 1
def DetectColor(Img, Contour):
    colors = OrderedDict({"Red": (255, 0, 0), "Yellow": (0, 255, 0), "Blue": (0, 0, 255)})
    HSV = zeros((len(colors), 1, 3), dtype="uint8")
    colorNames = []

    for (i, (name, HSV)) in enumerate(colors.items()):
            # Updating the lab array and the color name list
            self.HSV[i] = HSV
            self.colorNames.append(name)
        # Converting the lab array from RGB color space to lab
    self.HSV = cvtColor(self.HSV, cv2.COLOR_RGB2HSV)
    mask = zeros(image.shape[:2], dtype="uint8")
    drawContours(mask, [contour], -1, 255, -1)
    mask = erode(mask, None, iterations=2)
    mean = mean(image, mask=mask)[:3]
    minDist = (inf, None)
    for (i, row) in enumerate(HSV):
        # computing the distance between the current lab color value and the mean og the image
        d = dist.euclidean(row[0], mean)
        # if the distance is smaller than the current distance, update the bookkeeping variable
        if d < minDist[0]:
             minDist = (d, i)

def DetectShape(Contour):
    shape = ""
    peri = arcLength(Contour, True)
    approx = approxPolyDP(Contour, 0.02 * peri, True)
    if len(approx) == 3:
        shape = "Triangle"
    elif len(approx) == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        print(x, y, w, h)
        ar = w / float(h)

        rect = x / float(y)

        shape = "Rectangle"

    return shape

def ProcessImage(image):

    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    blurred = GaussianBlur(resized, (5, 5), 0)
    HSV = cvtColor(blurred, cv2.COLOR_BGR2HSV_FULL)

    lower_blue = array([110, 50, 50])
    upper_blue = array([190, 255, 255])
    HSVblueThresh = inRange(HSV, lower_blue, upper_blue)

    lower_yellow = array([25, 50, 50])
    upper_yellow = array([45, 255, 255])
    HSVyellowThresh = inRange(HSV, lower_yellow, upper_yellow)

    lower_red = array([3, 50, 50])
    upper_red = array([9, 255, 200])
    HSVredThresh = cv2.inRange(HSV, lower_red, upper_red)

    HSVredThresh = cv2.bitwise_and(HSVredThresh, HSVredThresh, mask=HSVredThresh)
    HSVblueThresh = cv2.bitwise_and(HSVblueThresh, HSVblueThresh, mask=HSVblueThresh)
    HSVyellowThresh = cv2.bitwise_and(HSVyellowThresh, HSVyellowThresh, mask=HSVyellowThresh)

    cnts = findContours(HSVyellowThresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    for c in cnts:
        M = moments(c)
        if(M["m00"] != 0):
            cX = int((M["m10"] / M["m00"]) * ratio)
            cY = int((M["m01"] / M["m00"]) * ratio)
        else:
            cX = 0
            cY = 0

        shape = DetectShape(c)
        color = DetectColor(HSV, c)

        c = c.astype("float")
        c *= ratio
        c = c.astype("int")

        text = "{} {}".format(color, shape)
        return text




width = maxsize
height = maxsize

# Set the dimensions for the main camera
cam.set(CAP_PROP_FRAME_WIDTH, width)
cam.set(CAP_PROP_FRAME_HEIGHT, height)
# Set the dimensions for the secondary camera

startTime = datetime.datetime.now()

index = 0  # This variable allows us to switch between the list indexes:
# if index is 0: the main camera will be that on the first port
# if index is 1: the main camera will be that on the second port
secCount = 0
min = 0

ser = Serial()
ser.port = 'COM12'
ser.baudrate = 9600
ser.open()
cnt = 0
read = ser.inWaiting()
s = str(ser.read(read))
s = s[2:]
show = 0
while (True):
    var, frame = cam.read()  # Accessing the camera at the corresponding index (Main Camera)
    # Making the feed taken by the secondary camera appear on top of the main one

    currSec = '0' + str(secCount) if secCount < 10 else str(secCount)

    currTime = '0' + str(min) + ':' + str(secCount) if min < 10 else str(min) + ':' + currSec

    putText(img=frame, text=currTime, org=(370, 90), fontFace=FONT_HERSHEY_DUPLEX, fontScale=3,
            color=(210, 255, 215), thickness=1, lineType=CV_8S)

    timeElapsed = (datetime.datetime.now() - startTime).total_seconds()
    if (timeElapsed >= 1):
        secCount += 1
        timeElapsed = 0
        startTime = datetime.datetime.now()
    if (secCount == 60):
        secCount = 1
        min += 1

    read = ser.inWaiting()
    if(show):
        disp = ProcessImage(frame)
        putText(img=frame, text=disp, org=(40, 420), fontFace=FONT_HERSHEY_DUPLEX, fontScale=1,
                color=(255, 255, 255), thickness=1, lineType=CV_8S)
    if cnt < 15:
        putText(img=frame, text=s, org=(80, 420), fontFace=FONT_HERSHEY_DUPLEX, fontScale=1,
                color=(255, 255, 255), thickness=1, lineType=CV_8S)
        cnt += 1

    else:
        s = str(ser.read(read))
        s = s[2:]
        putText(img=frame, text=s, org=(80, 420), fontFace=FONT_HERSHEY_DUPLEX, fontScale=1,
                color=(255, 255, 255), thickness=1, lineType=CV_8S)
        cnt = 0


    imshow('Frame', frame)

    key = waitKey(1) & 0xFF

    if (k == ord('P')):
        show = 1

    if (key == 27 or key == ord('Q') or key == ord('q')):  # Press ESC or Q to quit
        break

# Release the cameras and destroy the windows
cam.release()
destroyAllWindows()
