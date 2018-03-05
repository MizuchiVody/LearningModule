from tkinter import *
from tkinter import font
from cv2 import *


class App(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        #In the container we'll stack all of our frames on top of each other

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Frame1, Frame2, Frame3):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Frame1")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class Frame1(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This is frame 1", font = controller.title_font)
        label.pack()

        button1 = Button(self, text = "Go to frame 2", command = lambda: controller.show_frame("Frame2"))
        button2 = Button(self, text = "Go to frame 3", command = lambda: controller.show_frame("Frame3"))

        button1.pack()
        button2.pack()


class Frame2(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This is frame 2", font = controller.title_font)
        label.pack()
        button1 = Button(self, text="Go to frame 3", command = lambda: controller.show_frame("Frame3"))
        button2 = Button(self, text="Go to frame 1", command = lambda: controller.show_frame("Frame1"))

        button1.pack()
        button2.pack()


class Frame3(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This is frame 3", font = controller.title_font)
        label.pack()
        button1 = Button(self, text = "Go to frame 2", command = lambda: controller.show_frame("Frame2"))
        button2 = Button(self, text = "Go to frame 1", command = lambda: controller.show_frame("Frame1"))

        button1.pack()
        button2.pack()


app = App()
app.mainloop()
