from tkinter import *
from tkinter import font
from cv2 import *

# Added a functionality that displays a camera feed in a new window.
# The camera feeds is displayed at first.
# To quit the camera feed press 'q' lower case
# Press any buttons to display a new camera feed

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
        for F in (Frame1, Frame2):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Frame1",0)
    # 'index' parameter represents which camera feed: 0 for the first, 1 for the second...
    def show_frame(self, page_name,index):
        '''Show a frame for the given page name'''
        cap = cv2.VideoCapture(index)

        while (True):
            # Capture frame-by-frame
            ret, label = cap.read()

            # Our operations on the frame come here
            gray = cv2.cvtColor(label, cv2.COLOR_BGR2RGBA)

            # Display the resulting frame
            cv2.imshow('camera feed', gray)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()
        frame = self.frames[page_name]
        frame.tkraise()


class Frame1(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This is frame 1", font = controller.title_font)
        label.pack()

        button1 = Button(self, text = "Go to frame 2", command = lambda: controller.show_frame("Frame2",0))

        button1.pack()


class Frame2(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text = "This is frame 2", font = controller.title_font)
        label.pack()
        
        button2 = Button(self, text="Go to frame 1", command = lambda: controller.show_frame("Frame1",0))

        button2.pack()


app = App()
app.mainloop()
