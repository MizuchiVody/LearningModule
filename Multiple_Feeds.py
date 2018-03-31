# Import the necessary packages
from tkinter import *  # Make sure you're using Python 3!!!
import datetime
from cv2 import *
from sys import *
from time import *
from numpy import *
import daytime

root = Tk()
label = Label(root)
states = []
checklist = ['Prepower', 'Power Up', 'Failed Bubble Check', 'Lunch', 'Lost Communication', 'ROV retrieval', 'Demobilization']

for i in range(0, 6):
        var = IntVar()
        chk = Checkbutton(root, text= checklist[i], variable=var)
        chk.pack(side=TOP)
        states.append(var.get())

b = Button(root, text = "OK", command = root.quit).pack()
root.mainloop()

cam1 = VideoCapture(0)  # Capture the video from camera on port 0
cam2 = VideoCapture(1)  # Capture the video from camera on port 1

width = maxsize
height = maxsize

# Set the dimensions for the main camera
cam1.set(CAP_PROP_FRAME_WIDTH, width)
cam1.set(CAP_PROP_FRAME_HEIGHT, height)
# Set the dimensions for the secondary camera

cam2.set(CAP_PROP_FRAME_WIDTH, 200)
cam2.set(CAP_PROP_FRAME_HEIGHT, 180)

# In this list we'll store both our feeds and keep switching between them
cams = [cam1, cam2]

startTime = datetime.datetime.now()

index = 0  # This variable allows us to switch between the list indexes:
# if index is 0: the main camera will be that on the first port
# if index is 1: the main camera will be that on the second port
secCount = 0
min = 0

while (True):
    var, frame = cams[index].read()  # Accessing the camera at the corresponding index (Main Camera)
    var, frame2 = cams[1 - index].read()  # Accessing the other camera (Secondary camera)
    # Making the feed taken by the secondary camera appear on top of the main one
    frame[10:10 + frame2.shape[0], 10:10 + frame2.shape[1]] = frame2

    currSec = '0' + str(secCount) if secCount < 10 else str(secCount)

    currTime = '0' + str(min) + ':' + str(secCount) if min < 10 else str(min) + ':' + currSec

    putText(img=frame, text=currTime, org=(1000, 90), fontFace=FONT_HERSHEY_DUPLEX, fontScale=3,
                         color=(255, 255, 255), thickness=4, lineType=CV_8S)

    timeElapsed = (datetime.datetime.now() - startTime).total_seconds()
    if (timeElapsed >= 1):
        secCount += 1
        timeElapsed = 0
        startTime = datetime.datetime.now()
    if (secCount == 60):
        secCount = 1
        min += 1
        
    file = open('data.txt', 'r')
    a = []

    for line in file:
        l = len(line)
        line = line[:(l - 1)]
        a.append(line)
    y = 600

    for s in a:
        putText(img=frame, text=s, org=(900, y), fontFace=FONT_HERSHEY_DUPLEX, fontScale=1,
                     color=(255, 255, 255), thickness=1, lineType=CV_8S)
        y += 50


    imshow('Frame', frame)
    key = waitKey(1) & 0xFF
    if(key == ord('S') or key == ord('s') or key == 13):  # Press S or ENTER to switch the feed

        index = 1 - index  # Changing the index`

        # Switch the sizes of the feeds

        if (index == 0):
            cam1.set(CAP_PROP_FRAME_WIDTH, width)
            cam1.set(CAP_PROP_FRAME_HEIGHT, height)

            cam2.set(CAP_PROP_FRAME_WIDTH, 200)
            cam2.set(CAP_PROP_FRAME_HEIGHT, 180)

        else:
            cam1.set(CAP_PROP_FRAME_WIDTH, 200)
            cam1.set(CAP_PROP_FRAME_HEIGHT, 180)

            cam2.set(CAP_PROP_FRAME_WIDTH, width)
            cam2.set(CAP_PROP_FRAME_HEIGHT, height)
    file.close()
    if (key == 27 or key == ord('Q') or key == ord('q')):  # Press ESC or Q to quit
         break

# Release the cameras and destroy the windows
cam1.release()
cam2.release()
destroyAllWindows()
