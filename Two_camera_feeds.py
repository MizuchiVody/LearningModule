from tkinter import *
import tkinter as tk
import cv2
from PIL import Image, ImageTk

width, height = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

width1, height1 = 640, 360
cap1 = cv2.VideoCapture(0)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, width1)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, height1)

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()
main2 = tk.Label(root)
main2.pack()
# root.bind('1', lambda e: lmain.lower())
# root.bind('2', lambda e: lmain.lift())

def show_frame():
    _, frame = cap.read()
    _, frame1 = cap1.read()
    frame = cv2.flip(frame, 1)
    frame1 = cv2.flip(frame1, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    cv2image1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    img1 = Image.fromarray(cv2image1)
    imgtk = ImageTk.PhotoImage(image=img)
    imgtk1 = ImageTk.PhotoImage(image=img1)
    lmain.imgtk = imgtk
    main2.imgtk1 = imgtk1
    lmain.configure(image=imgtk)
    main2.configure(image=imgtk1)
    lmain.after(10, show_frame)
    main2.after(10, show_frame)




show_frame()
root.mainloop()
