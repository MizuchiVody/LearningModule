from tkinter import *
import datetime
from cv2 import *
from sys import *
from time import *
from numpy import *
from imutils import *
from collections import *

def ProcessImage(img):
    resized = resize(img, width=300)
    ratio = img.shape[0] / float(resized.shape[1])

    blurred = GaussianBlur(resized, (5, 5), 0)
    thresh = threshold(blurred, 60, 255, THRESH_BINARY)[1]

    HSV = cvtColor(blurred, COLOR_BGR2HSV_FULL)
    lower_blue = array([80, 150, 0])
    upper_blue = array([160, 255, 255])
    hsvbluethresh = inRange(HSV, lower_blue, upper_blue)

    lower_yellow = array([25, 150, 0])
    upper_yellow = array([32, 255, 255])
    hsvyellowthresh = inRange(HSV, lower_yellow, upper_yellow)

    lower_red = array([0, 150, 0])
    upper_red = array([12, 255, 255])
    hsvredthresh = inRange(HSV, lower_red, upper_red)

    hsvredthresh = cv2.bitwise_and(hsvredthresh, hsvredthresh, mask=hsvredthresh)
    hsvbluethresh = cv2.bitwise_and(hsvbluethresh, hsvbluethresh, mask=hsvbluethresh)
    hsvyellowthresh = cv2.bitwise_and(hsvyellowthresh, hsvyellowthresh, mask=hsvyellowthresh)

    ThreshColors = [hsvbluethresh, hsvredthresh, hsvyellowthresh]

    color = {0: "Blue", 1: "Red", 2: "Yellow"}
    for i in range(0, 3):

        countours = findContours(ThreshColors[i].copy(), RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)
        countours = countours[0] if is_cv2() else countours[1]

        for cnt in countours:

            M = moments(cnt)
            X = int((M["m10"] / M["m00"]) * ratio) if(M["m00"] != 0) else 0
            Y = int((M["m01"] / M["m00"]) * ratio) if(M["m00"] != 0) else 0

            approx = approxPolyDP(cnt, 0.02 * arcLength(cnt, True), True)

            shape = "Unknown"
            l = len(approx)

            if l == 3:
                shape = "Triangle"

            elif l == 4:
                (x, y, w, h) = boundingRect(approx)
                ar = w / float(h)

                shape = "Square" if ar >= 0.95 and ar <= 1.05 else "Rectangle"

            cnt = cnt.astype("float")
            cnt *= ratio
            cnt = cnt.astype("int")

            if(shape != "Unknown"):
                drawContours(img, [cnt], 0, (0, 255, 0), 2)
                ans = color[i] + shape
                putText(img=img,text=ans,org=(X, Y),fontFace=FONT_HERSHEY_DUPLEX,fontScale=1,
                            color=(255, 255, 255), thickness=2)



root = Tk()
label = Label(root)

states = []
checklist = ['Prepower', 'Power Up', 'Failed Bubble Check', 'Lunch', 'Lost Communication', 'ROV retrieval', 'Demobilization']

for i in range (0, 6):
    var = IntVar()
    chk = Checkbutton(root, text=checklist[i], variable=var)
    chk.pack(side=TOP)
    states.append(var.get())

b = Button(root, text="OK", command=root.quit).pack()
root.mainloop()

cam1 = VideoCapture(0)
cam2 = VideoCapture(1)

width, height = maxsize, maxsize

cam1.set(CAP_PROP_FRAME_WIDTH, width)
cam1.set(CAP_PROP_FRAME_HEIGHT, height)

cam2.set(CAP_PROP_FRAME_WIDTH, 100)
cam2.set(CAP_PROP_FRAME_HEIGHT, 300)

cams = [cam1, cam2]

startTime = datetime.datetime.now()

index = 0
secCount = 0
min = 0
cnt = 0
show = 0

while(True):
    var, frame = cams[index].read()
    var, frame2 = cams[1 - index].read()

    frame[10:10 + frame2.shape[0], 10:10 + frame2.shape[1]] = frame2

    currSec = '0' + str(secCount) if secCount < 10 else str(secCount)

    currTime = '0' + str(min) + ':' + str(secCount) if min < 10 else str(min) + ':' + currSec

    putText(img=frame, text=currTime, org=(1000, 90), fontFace=FONT_HERSHEY_DUPLEX, fontScale=4,
            color=(210, 255, 215), thickness=1, lineType=CV_8S)

    timeElapsed = (datetime.datetime.now() - startTime).total_seconds()
    if (timeElapsed >= 1):
        secCount += 1
        timeElapsed = 0
        startTime = datetime.datetime.now()
    if (secCount == 60):
        secCount = 1
        min += 1

    ProcessImage(frame)

    imshow('Frame', frame)

    k = waitKey(1) & 0xFF

    if (k == 13 or k == ord('s')):
        index = 1 - index

        cams[index].set(CAP_PROP_FRAME_WIDTH, width)
        cams[index].set(CAP_PROP_FRAME_HEIGHT, height)

        cams[1 - index].set(CAP_PROP_FRAME_WIDTH, 100)
        cams[1 - index].set(CAP_PROP_FRAME_HEIGHT, 100)


    if (k == 27 or k == ord('Q') or k == ord('q')):  # Press ESC or Q to quit
        break


cam1.release()
cam2.release()
destroyAllWindows()
