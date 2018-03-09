import tkinter as tk
import cv2
from PIL import Image, ImageTk


# this code is incomplete so far
width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, show_frame)

def show_frame2():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, show_frame)


root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
root.bind('<Button-3>', lambda e: show_frame())
root.bind('<Button-1>', lambda e: show_frame2())
lmain = tk.Label(root)
lmain.pack()
# show_frame()
root.mainloop()

# idea 1 keep the show frame function outside the gui and try to pass the arg index of the camera idea 2 bind the
# event of a shortcut to switching between camera feeds
# comment: Try the already working code that switches between both cameras in the newbostongui tuto based on aghzal's code
