from tkinter import *
from PIL import Image, ImageTk
import cv2


class RunFrontPage:

    def __init__(self, window):
        self.root = window

        self.clips = ["video1.mp4","video2.mp4","video3.mp4","video4.mp4"]
        self.current_clip_index = 0

        self.bg_video = cv2.VideoCapture("clips\\"+ str(self.clips[self.current_clip_index]))

        #create Canvas
        self.canvas = Canvas(self.root, width = 900, height = 600)
        self.canvas.grid(row=0,column=0, columnspan=7)

        self.update()



    
    def update(self):

        try:
            ret, frame = self.bg_video.read()

            if ret:
                self.photo = ImageTk.PhotoImage(image= Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0,-145, image=self.photo, anchor= NW)
            else:
                self.current_clip_index += 1
                if self.current_clip_index >= 3:
                    self.current_clip_index = 0
                else:
                    self.bg_video = cv2.VideoCapture("clips\\"+ str(self.clips[self.current_clip_index]))

            self.root.after(10,self.update)
        except Exception as e:
            print()