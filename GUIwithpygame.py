import pygame
from pygame.locals import *
from cv2 import *
from numpy import *
from sys import *
from clock import *
import datetime
from tkinter import *

cam1 = VideoCapture(1)
cam2 = VideoCapture(0)
secCount = 0
min = 0
cnt = 0
index = 0

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

pygame.init()
pygame.display.set_caption("CamFeedback")
screen = pygame.display.set_mode([1280, 1280])


width, height = maxsize, maxsize

cam1.set(CAP_PROP_FRAME_WIDTH, width)
cam1.set(CAP_PROP_FRAME_HEIGHT, height)

cam2.set(CAP_PROP_FRAME_WIDTH, 200)
cam2.set(CAP_PROP_FRAME_HEIGHT, 200)
startTime = datetime.datetime.now()

cams = [cam1, cam2]

def Missions():
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
        rt1.mainloop
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

def switch_feeds():
    global index
    index = 1 - index
    cams[index].set(CAP_PROP_FRAME_WIDTH, width)
    cams[index].set(CAP_PROP_FRAME_HEIGHT, height)
    cams[1 - index].set(CAP_PROP_FRAME_WIDTH, 100)
    cams[1 - index].set(CAP_PROP_FRAME_HEIGHT, 300)


def text_objects(text, font):
    textSurface = font.render(text, True, (255, 255, 255))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)

while True:
    var, frame = cams[index].read()
    var, frame2 = cams[1 - index].read()
    screen.fill([0, 0, 0])
    frame[10:10 + frame2.shape[0], 10:10 + frame2.shape[1]] = frame2
    frame = cvtColor(frame, COLOR_BGR2RGB)
    frame = rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))

    button("Switch", 100, 620, 100, 50, (255, 0, 0), (255, 110, 0), switch_feeds)
    pygame.display.update()

    button("Missions", 100, 580, 100, 50, (255, 0, 0), (255, 110, 0), Missions)
    pygame.display.update()

    currSec = '0' + str(secCount) if secCount < 10 else str(secCount)

    currTime = '0' + str(min) + ':' + str(secCount) if min < 10 else str(min) + ':' + currSec


    font = pygame.font.SysFont("monospace", 80)
    time = font.render(currTime, 5, (255, 255, 255))
    screen.blit(time, (50, 50))

    timeElapsed = (datetime.datetime.now() - startTime).total_seconds()
    if (timeElapsed >= 1):
        secCount += 1
        timeElapsed = 0
        startTime = datetime.datetime.now()
    if (secCount == 60):
        secCount = 1
        min += 1
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            destroyAllWindows()
