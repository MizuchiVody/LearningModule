# Import the necessary packages
from tkinter import *  # Make sure you're using Python 3!!!
import datetime
from cv2 import *
from sys import *
from time import *
from serial import *
from numpy import *
import daytime

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
ser.open ()
cnt = 0
read = ser.inWaiting()
s = str(ser.read(read))
s = s[2:]
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

    if (key == 27 or key == ord('Q') or key == ord('q')):  # Press ESC or Q to quit
        break

# Release the cameras and destroy the windows
cam.release()
destroyAllWindows()
