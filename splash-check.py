import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk


class ImageLabel(tk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                resized = im.resize((500, 500),Image.ANTIALIAS)
                self.frames.append(ImageTk.PhotoImage(resized))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)



 
class DemoSplashScreen:
    def __init__(self, parent):
        self.parent = parent


        
        
         
        self.aSplash()
        self.aWindow()
 
    def aSplash(self):
        # import image menggunakan Pillow
        self.picture = Image.open('fing.jpg')
        
        self.imgSplash = ImageTk.PhotoImage(self.picture)

        
 
    def aWindow(self):
        
        length, height = self.picture.size
 
        halflength = (self.parent.winfo_screenwidth()-length)//2
        halfheight = (self.parent.winfo_screenheight()-height)//2
 
        
        self.parent.geometry("%ix%i+%i+%i" %(length, height,
                                             halflength,halfheight))
 
       
        Label(self.parent, image=self.imgSplash).pack()
         
if __name__ == '__main__':
    root = Tk()
 
   
    root.overrideredirect(True)
    progressbar = ttk.Progressbar(orient=HORIZONTAL, length=10000, mode='determinate')
    progressbar.pack(side="bottom")
    app = DemoSplashScreen(root)

    progressbar.start()
    
    #root.after(1200000, root.destroy)
    root.after(5000, root.destroy) 
    root.mainloop()
