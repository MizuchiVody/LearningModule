from tkinter import *
from cv2 import *
from sys import *

# Initialize cameras to corresponding ports
cam1 = VideoCapture(0)
cam2 = VideoCapture(1)

width = maxsize
height = maxsize

# Set Camera Dimensions
cam1.set(CAP_PROP_FRAME_WIDTH, width)
cam1.set(CAP_PROP_FRAME_HEIGHT, height)

cam2.set(CAP_PROP_FRAME_WIDTH, 460)
cam2.set(CAP_PROP_FRAME_HEIGHT, 180)

cams = [cam1, cam2]

root = Tk()
label = Label(root)

label.pack(side = TOP, fill = BOTH, expand = YES)
index = 0
while (True):
    var, frame = cams[index].read()
    var, frame2 = cams[1 - index].read()
    frame[10:10 + frame2.shape[0], 10:10 + frame2.shape[1]] = frame2
    imshow('Frame', frame)
    key = waitKey(1) & 0xFF
    if(key == ord('S')): #Press S to switch the feed
        index = 1 - index
        
        #Switch the set
        
        if(index == 0):
            cam1.set(CAP_PROP_FRAME_WIDTH, width)
            cam1.set(CAP_PROP_FRAME_HEIGHT, height)

            cam2.set(CAP_PROP_FRAME_WIDTH, 460)
            cam2.set(CAP_PROP_FRAME_HEIGHT, 180)

        else:
            cam1.set(CAP_PROP_FRAME_WIDTH, 460)
            cam1.set(CAP_PROP_FRAME_HEIGHT, 180)

            cam2.set(CAP_PROP_FRAME_WIDTH, width)
            cam2.set(CAP_PROP_FRAME_HEIGHT, height)
    if (key == 27 or key == ord('Q')): #Press ESC or Q to quit
        break
        
cam1.release()
cam2.release()
destroyAllWindows()
root.mainloop()
