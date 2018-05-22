from tkinter import *
import datetime
from cv2 import *
from sys import *
from time import *
from numpy import *
from imutils import *
from serial import *
from collections import *
import os

def ProcessImage(img):
    resized = resize(img, width=300)
    ratio = img.shape[0] / float(resized.shape[1])

    blurred = GaussianBlur(resized, (5, 5), 0)
    thresh = threshold(blurred, 60, 255, THRESH_BINARY)[1]

    HSV = cvtColor(blurred, COLOR_BGR2HSV_FULL)
    lower_blue = array([90, 50, 50])
    upper_blue = array([170, 255, 255])
    hsvbluethresh = inRange(HSV, lower_blue, upper_blue)

    lower_yellow = array([13, 90, 90])
    upper_yellow = array([30, 255, 255])
    hsvyellowthresh = inRange(HSV, lower_yellow, upper_yellow)

    lower_red = array([0, 100, 100])
    upper_red = array([10, 255, 255])
    hsvredthresh = inRange(HSV, lower_red, upper_red)

    hsvredthresh = cv2.bitwise_and(hsvredthresh, hsvredthresh, mask=hsvredthresh)
    hsvbluethresh = cv2.bitwise_and(hsvbluethresh, hsvbluethresh, mask=hsvbluethresh)
    hsvyellowthresh = cv2.bitwise_and(hsvyellowthresh, hsvyellowthresh, mask=hsvyellowthresh)

    ThreshColors = [hsvbluethresh, hsvredthresh, hsvyellowthresh]

    color = {0: "Blue", 1: "Red", 2: "Yellow"}
    tailTri = {0: "G7C", 1: "UH8", 2: "L6R"}
    tailRect = {0: "A2X", 1: "S1P", 3: "JW3"}

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
                shape = "Rectangle"

            tail = "Unknown"
            if shape == "Triangle":
                tail = tailTri[i]
            elif shape == "Rectangle":
                if i == 0:
                    tail = "A2X"
                elif i == 1:
                    tail = "S1P"
                else:
                    tail = "JW3"

            if(shape != "Unknown" and tail != "Unknown"):
                cnt = cnt.astype("float")
                cnt *= ratio
                cnt = cnt.astype("int")
                drawContours(img, [cnt], 0, (0, 255, 0), 2)
                ans = color[i] + ' ' + shape + ' ' + tail
                putText(img=img,text=ans,org=(X, Y),fontFace=FONT_HERSHEY_DUPLEX,fontScale=1, color=(255, 255, 255), thickness=2)

fields = ('heading', 'ascent airspeed', 'ascent rate', 'engine failure time', 'decsent airspeed', 'decsent rate', 'wind', 'a', 'b', 'c')

def Mission1():
    fields_1 = (
    'heading', 'ascent airspeed', 'ascent rate', 'engine failure time', 'decsent airspeed', 'decsent rate', 'wind', 'a',
    'b', 'c')
    fields_3 = ('number of turbines', 'water density', 'turbine radius', 'velocity in water', 'turbine efficiency')

    # functions for mission 1
    def ascentmovement(entries):
        h = float(entries['heading'].get())
        aas = float(entries['ascent airspeed'].get())
        t = float(entries['engine failure time'].get())
        global ycomp
        ycomp = aas * t * cos(deg2rad(h))
        global xcomp
        xcomp = aas * t * sin(deg2rad(h))
        print("ascent movement: ")
        print(xcomp)
        print(ycomp)

    def descentmovement(entries):
        aar = float(entries['ascent rate'].get())
        h = float(entries['heading'].get())
        das = float(entries['decsent airspeed'].get())
        t = float(entries['engine failure time'].get())
        t2 = (t * aar) / 6
        adr = float(entries['decsent rate'].get())
        global Ycomp
        Ycomp = das * t2 * cos(deg2rad(h))
        global Xcomp
        Xcomp = das * t2 * sin(deg2rad(h))
        print("descent movement: ")
        print(Xcomp)
        print(Ycomp)

    def windmovement(entries):
        aar = float(entries['ascent rate'].get())
        global h
        h = float(entries['heading'].get())
        das = float(entries['decsent airspeed'].get())
        t = float(entries['engine failure time'].get())
        t2 = (t * aar) / 6
        adr = float(entries['decsent rate'].get())
        A = float(entries['a'].get())
        B = float(entries['b'].get())
        C = float(entries['c'].get())
        w = float(entries['wind'].get())
        global ypos
        ypos = (1 / 3 * A * t2 ** 3 + 1 / 2 * B * t2 ** 2 + C * t2) * (cos(deg2rad(w - 180)))
        global xpos
        xpos = (1 / 3 * A * t2 ** 3 + 1 / 2 * B * t2 ** 2 + C * t2) * sin(deg2rad(w - 180))
        print("wind movement: ")
        print(xpos)
        print(ypos)

    def totmovement(entries):

        global xtot
        xtot = xcomp + Xcomp + xpos
        global ytot
        ytot = ycomp + Ycomp + ypos
        print("total movement:")
        print(xtot)
        print(ytot)

    # def degree (entries):							arctan (sum (sines) / sum (cosines))
    def result(entries):
        dist = sqrt(xtot ** 2 + ytot ** 2)
        kaka = xtot / ytot
        direction = rad2deg(arctan(abs(kaka)))
        print('reported search zone :')
        print(dist)
        # print (direction)
        if (xtot > 0 and ytot < 0):
            # direction+=180
            direction = 180 - direction

        elif (xtot > 0 and ytot > 0):
            # direction+=90
            direction = 90 - direction

        elif (xtot < 0 and ytot > 0):
            # direction-=360
            direction = 360 - direction

        elif (xtot < 0 and ytot < 0):
            direction = 270 - direction

        print(direction)

    # functions for mission 3

    def doval(entries):
        N = float(entries['number of turbines'].get())
        d = float(entries['water density'].get())
        r = float(entries['turbine radius'].get())
        v = float(entries['velocity in water'].get())
        e = float(entries['turbine efficiency'].get())
        global P
        P = 0.5 * (N * d * pi * (r ** 2) * (v ** 3))
        rt1 = Tk()
        Label(rt1, text='Maximum power that could be generated is:')
        rt1.mainloop()
        # print("Maximum Power: %f" % float(P))

    def makeform_for_1(root, fields):
        entries = {}
        for field in fields_1:
            row = Frame(root)
            lab = Label(row, width=22, text=field + ": ", anchor='w')
            ent = Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries[field] = ent
        return entries

    def makeform_for_3(root, fields):
        entries = {}
        for field in fields_3:
            row = Frame(root)
            lab = Label(row, width=22, text=field + ": ", anchor='w')
            ent = Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries[field] = ent
        return entries

    def prompt1():
        ents = makeform_for_1(root, fields_1)
        b1 = Button(root, text='validate',
                    command=lambda: [ascentmovement(ents), descentmovement(ents), windmovement(ents),
                                     totmovement(ents), result(ents)]).pack(side=LEFT, padx=5, pady=5)
        b3 = Button(root, text='Quit', command=root.quit).pack(side=LEFT, padx=5, pady=5)
        root.mainloop()

    def prompt3():
        ents = makeform_for_3(root, fields_3)
        b1 = Button(root, text='validate', command=lambda: [doval(ents)]).pack(side=LEFT, padx=3, pady=3)
        b3 = Button(root, text='Quit', command=root.quit).pack(side=LEFT, padx=3, pady=3)
        root.mainloop()

    root = Tk()
    zebi = Label(root, text="which mission do you wish to complete?", padx=2, pady=2, anchor='n', height=3, width=70)
    zebi.pack()
    btn1 = Button(root, text="Mission 1", command=prompt1)
    btn1.config(height=3, width=20)
    btn1.pack()
    btn3 = Button(root, text="Mission 3", command=prompt3)
    btn3.config(height=3, width=20)
    btn3.pack()
    b1 = Button(root, text='validate', command=lambda: [ascentmovement(ents), descentmovement(ents), windmovement(ents), totmovement(ents),result(ents)])
    root.mainloop()

root = Tk()
label = Label(root)

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

    k = waitKey(1) & 0xFF

    if(k == ord('m')):
        Mission1()

    if(waitKey(10) & 0xFF == ord('P')):
        ProcessImage(frame)

    imshow('Frame', frame)

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

