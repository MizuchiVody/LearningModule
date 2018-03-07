from tkinter import *
from cv2 import *
from sys import *
cam1 = VideoCapture(0)
cam2 = VideoCapture(1)

width = maxsize
height = maxsize

cam1.set(CAP_PROP_FRAME_WIDTH, width)
cam1.set(CAP_PROP_FRAME_HEIGHT, height)

cam2.set(CAP_PROP_FRAME_WIDTH, 128)
cam2.set(CAP_PROP_FRAME_HEIGHT, 0)

root = Tk()
label = Label(root)

label.pack(side = TOP, fill = BOTH, expand = YES)
while (True):
    var, frame = cam1.read()
    var, frame2 = cam2.read()
    frame[872:1000, 0:128] = frame2
    imshow('Frame', frame)
    key = waitKey(1) & 0xFF
    if (key == 27 or key == ord('q')):
        break
        
cam1.release()
cam2.release()
destroyAllWindows()
root.mainloop()
