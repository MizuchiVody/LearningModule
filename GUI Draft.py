from tkinter import *
import tkinter as tk
from cv2 import *
from PIL import Image, ImageTk
from sys import *


width, height = maxsize, maxsize
SecondWidth, SecondHeight = 200, 180
MainCamFeed = cv2.VideoCapture(1)
#MainCamFeed.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#MainCamFeed.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

SecondaryCamFeed = cv2.VideoCapture(0)
#SecondaryCamFeed.set(cv2.CAP_PROP_FRAME_WIDTH, SecondWidth)
#SecondaryCamFeed.set(cv2.CAP_PROP_FRAME_HEIGHT, SecondHeight)

def GetFrames(CamFeed1, CamFeed2,width1,width2,height1,height2):
    CamFeed1.set(cv2.CAP_PROP_FRAME_WIDTH, width1)
    CamFeed1.set(cv2.CAP_PROP_FRAME_HEIGHT, height1)
    CamFeed2.set(cv2.CAP_PROP_FRAME_WIDTH, width2)
    CamFeed2.set(cv2.CAP_PROP_FRAME_HEIGHT, height2)

    Cameras = [CamFeed1, CamFeed2]
    while True:
        var, MainFeed = Cameras[0].read()
        var, SecondFeed = Cameras[1].read()
        MainFeed[0:0 + SecondFeed.shape[0], 0:0 + SecondFeed.shape[1]] = SecondFeed
        imshow('GUI', MainFeed)
        key = waitKey(1) & 0xFF
        # MainFeed = cv2.flip(MainFeed, 1)
        # SecondFeed = cv2.flip(SecondFeed, 1)
        # cv2image = cv2.cvtColor(MainFeed, cv2.COLOR_BGR2RGBA)
        # cv2Image2 = cv2.cvtColor(SecondFeed, cv2.COLOR_BGR2RGBA)
        # img = Image.fromarray(cv2image)
        # imgnd = Image.fromarray(cv2Image2)
        # SecondaryFrame = ImageTk.PhotoImage(image=imgnd)
        # PrimaryFrame = ImageTk.PhotoImage(image=img)
        # PrimaryFrame.img = img
        # main.configure(image=img)
        if key == 27:
            break


'''

def DisplayMainCamFeed(BigFeed, SmallFeed):


def DisplaySecondaryCamFeed (BigFeed, SmallFeed):

'''

root = tk.Tk()

#root.bind('<Escape>', lambda e: root.quit())
root.bind('<Button-1>', lambda e: GetFrames(MainCamFeed, SecondaryCamFeed,width,SecondWidth,height,SecondHeight))
root.bind('<Button-3>', lambda e: GetFrames(SecondaryCamFeed, MainCamFeed,width,SecondWidth,height,SecondHeight))
main = tk.Label(root)
main.pack()
GetFrames(MainCamFeed, SecondaryCamFeed,width,SecondWidth,height,SecondHeight)
destroyAllWindows()
root.mainloop()
