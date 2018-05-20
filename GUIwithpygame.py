import pygame
from pygame.locals import *
from cv2 import *
import numpy as np
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
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))

    button("Switch", 100, 620, 100, 50, (255, 0, 0), (255, 110, 0), switch_feeds)
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
