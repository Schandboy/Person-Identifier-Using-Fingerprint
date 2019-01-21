# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 19:42:13 2018

@author: jagdi
"""

import tkinter as tk
from keras import backend as K
from PIL import Image, ImageTk
from itertools import count
#from tkinter import BOTH
import subprocess
import os
import sqlite3
import numpy as np

from myPackage import tools as tl
from myPackage import preprocess
from enhancementFP import image_enhance as img_e
from os.path import basename, splitext, exists
#from numpy import mean, std
import cv2



#from keras.preprocessing import image as kimage
from keras.models import load_model



TITLE_FONT = ("Helvetica", 18, "bold")


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




class SampleApp(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)



        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self, c):
        frame = self.frames[c]
        frame.tkraise()
        
    def get_page(self, page_class):
        return self.frames[page_class]
    
    
   


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller=controller
       
        label = tk.Label(self, text="PERSON IDENTIFIER USING FINGERPRINT",foreground = "Red", font=("Times New Roman", 30, "bold"))
        label.pack(side="top")
        sublabel = tk.Label(self, text="[PIUF]",foreground = "Red",
                            font=("Times New Roman", 20))
        sublabel.pack()

        self.lbl = ImageLabel(self)
        self.lbl.pack()
        self.lbl.place(x=530,y=150)
       
        self.v = tk.StringVar()
        self.pro = tk.StringVar()
        
        self.lbl2 = ImageLabel(self)
        self.lbl2.pack()
#        self.lbl2.place(x=630,y=200)
        self.lbl2.place(x=530,y=150)
        
        self.lbl.load('phuto.gif')
        
#        tk.Button(self, text="Take Finger Print", width=20,height=2
#                   ,bg='brown',fg='white', command=lambda: controller.show_frame(PageOne)).place(x=200,y=600)
        tk.Button(self, text="Take Finger Print", width=20,height=2
                   ,bg='brown',fg='white', command=self.cmd).place(x=600,y=700)
        
#        button2 = tk.Button(self, text="Go to Page Two",
#                            command=lambda: controller.show_frame(PageTwo))
#        tk.Button(self, text="Identify", width=20,height=2,bg='brown',fg='white',command=self.identify).place(x=400,y=600)
       
#        tk.Button(self, text="show", width=20,height=2,bg='brown',fg='white',command=lambda: controller.show_frame(PageTwo)).place(x=600,y=600)
        
        #to access to the new class
#         p2 = PageTwo(parent,controller)
#        tk.Button(self, text="show", width=20,height=2,bg='brown',fg='white',command=lambda: p2.show(controller)).place(x=600,y=600)
#        button2.pack(side="bottom")
#        button1.pack(side="bottom")
#        self.btn1= tk.Button(self,text='Identify', width=20,height=2,bg='brown',fg='white',command=self.identify).place(x=800,y=700)
        self.pro = 'identify'
        self.btnb = tk.Button(self)
        self.btnb.configure(text=self.pro,width=20,height=2,bg='brown',fg='white',command=self.identify)
        self.btnb.place(x=800,y=700)
      
        
   
    def identify(self):
        top = tk.Toplevel(self)
        top.geometry('1000x700')
        
# =============================================================================
#         
# =============================================================================
        image_ext = '.jpg'
        plot = False
        path = None
        # ratio = 0.2
        # Create folders for results
        # -r ../Data/Results/fingerprints
    #    if args.get("results") is not None:
    #        if not exists(args["results"]):
    #            tl.makeDir(args["results"])
    #        path = args["results"]
        # Extract names
    #    all_images = tl.natSort(tl.getSamples(args["path"], image_ext))
    #    all_images = tl.natSort(tl.getSamples('C:\\Users\\jagdi\\Desktop\\project\\MinutiaeFingerprint-master', image_ext))
        
        all_images = tl.natSort(tl.getSamples('C:\\Program Files\\PIUF\\images_folder\\temp', image_ext))
    
    
        # Split train and test data
        # train_data, test_data = tl.split_train_test(all_images, ratio)
        print("\nAll_images size: {}\n".format(len(all_images)))
       # all_times= []
        print ("all images\n", all_images)
        for image in all_images:
    #        start = time.time()
            name = splitext(basename(image))[0]
            print("\nProcessing image '{}'".format(name))
            self.pro = 'processing image'
            
    #        print("path ={} ".format(args["path"]))
            print("image ={}".format(image))
            img = cv2.imread(str(image),0)
            equ = cv2.equalizeHist(img)
            
            
            
            cv2.imwrite('equalized\\'+str(name)+'.jpg',equ)
    
            
        all_eqimages = all_images = tl.natSort(tl.getSamples('equalized', image_ext))
        for image in all_eqimages:
            name = splitext(basename(image))[0]
            print("\nProcessing image '{}'".format(name))
            self.pro = 'processing'
            cleaned_img = preprocess.blurrImage(image, name, plot)
            enhanced_img = img_e.image_enhance(cleaned_img, name, plot)
            cleaned_img = preprocess.cleanImage(enhanced_img, name, plot)
    
            skeleton = preprocess.thinImage(cleaned_img, name, plot)
            revert = cv2.bitwise_not(skeleton)
            cv2.imwrite('thinned\\'+str(name)+'.jpg',revert)
            
        
        folder = 'equalized'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
               
            except Exception as e:
                print(e)

        num_channel=1        
        
        test_image = cv2.imread('thinned/temp.jpg')
        test_image=cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        test_image=cv2.resize(test_image,(128,128))
        test_image = np.array(test_image)
        test_image = test_image.astype('float32')
        test_image /= 255

        if num_channel==1:
                if K.image_dim_ordering()=='th':
                        test_image= np.expand_dims(test_image, axis=0)
                        test_image= np.expand_dims(test_image, axis=0)
                        print (test_image.shape)
                else:
                        test_image= np.expand_dims(test_image, axis=3) 
                        test_image= np.expand_dims(test_image, axis=0)
                        print (test_image.shape)
                        
        else:
                if K.image_dim_ordering()=='th':
                        test_image=np.rollaxis(test_image,2,0)
                        test_image= np.expand_dims(test_image, axis=0)
                        print (test_image.shape)
                else:
                        test_image= np.expand_dims(test_image, axis=0)
                        print (test_image.shape)
        
        
        
        loaded_model = load_model('model8.h5') 
        result = int(loaded_model.predict_classes(test_image))

       
        self.v.set(self.switch_demo(result))
        
        b = tk.Button(top, text="OK", width=20,height=2
                   ,bg='brown',fg='white',command=lambda win=top: win.destroy())
        b.pack(side="bottom")

        
        name1 = self.v.get()
        print(name1)
        
        label_2 = tk.Label(top, text="First Name",width=20,font=("bold", 10))
        label_2.place(x=70,y=170)
        
        label_3 = tk.Label(top, text="Last Name",width=20,font=("bold", 10))
        label_3.place(x=70,y=200)
        
        label_4 = tk.Label(top, text="Gender",width=20,font=("bold", 10))
        label_4.place(x=70,y=230)
        
        label_5 = tk.Label(top, text="Email Address",width=20,font=("bold", 10))
        label_5.place(x=70,y=260)
        
        label_6 = tk.Label(top, text="Contact No.",width=20,font=("bold", 10))
        label_6.place(x=70,y=290)
        
        label_7 = tk.Label(top, text="Address",width=20,font=("bold", 10))
        label_7.place(x=70,y=320)
        
        label_8 = tk.Label(top, text="Faculty",width=20,font=("bold", 10))
        label_8.place(x=70,y=350)

        
        conn = sqlite3.connect('Form.db')
        
       
        
        with conn:
          cursor=conn.cursor()
          cursor.execute('SELECT First_Name FROM Student where First_Name="'+name1+'"')
          rows = cursor.fetchall()
          label_2 = tk.Label(top, text=rows,width=20,font=("bold", 10))
          label_2.place(x=240,y=170)
          cursor.execute('SELECT Last_Name FROM Student where First_Name="'+name1+'"')
          rows1 = cursor.fetchall()
          label_3 = tk.Label(top, text=rows1,width=20,font=("bold", 10))
          label_3.place(x=240,y=200)
          cursor.execute('SELECT Gender FROM Student where First_Name="'+name1+'"')
          rows2 = cursor.fetchall()
          label_4 = tk.Label(top, text=rows2,width=20,font=("bold", 10))
          label_4.place(x=240,y=230)
          cursor.execute('SELECT Email FROM Student where First_Name="'+name1+'"')
          rows3 = cursor.fetchall()
          label_5 = tk.Label(top, text=rows3,width=20,font=("bold", 10))
          label_5.place(x=240,y=260)
          cursor.execute('SELECT Contact_No FROM Student where First_Name="'+name1+'"')
          rows4 = cursor.fetchall()
          label_6 = tk.Label(top, text=rows4,width=20,font=("bold", 10))
          label_6.place(x=240,y=290)
          cursor.execute('SELECT Address FROM Student where First_Name="'+name1+'"')
          rows5 = cursor.fetchall()
          label_7 = tk.Label(top, text=rows5,width=20,font=("bold", 10))
          label_7.place(x=240,y=320)
          cursor.execute('SELECT Faculty FROM Student where First_Name="'+name1+'"')
          rows6 = cursor.fetchall()
          label_8 = tk.Label(top, text=rows6,width=20,font=("bold", 10))
          label_8.place(x=240,y=350)
          cursor.execute('SELECT Photo FROM Student where First_Name="'+name1+'"')
          rows7 = cursor.fetchall()
         
          print(rows1)
          print(rows2)
          print(rows3)
          print(rows4)
          print(rows5)
          print(rows6)
          print(rows7)
         
            
          img = ImageLabel(top)
          img.pack(side="right")
          img.load(str(rows7[0][0]))
          
          
          
          
    
    def cmd(self):
   # command="cmd"
     
        subprocess.call(["WindowsFormsApplication2.exe"], shell=True)
        if os.path.isfile("C:\\Program Files\\PIUF\\images_folder\\temp\\temp.jpg"):
            self.lbl.destroy()
            self.lbl2.load('C:\\Program Files\\PIUF\\images_folder\\temp\\temp.jpg')
        else:
            self.lbl.load('phuto.gif')

    def switch_demo(self,argument):
             return {
                0: "Jagdish",
                1: "JagdishLeft",
                2: "Pujan",
                3: "PujanLeft",
                4: "Susan",
                5: "SusanLeft",
                6: "Manoj",
                7: "ManojLeft"
            }.get(argument, "Invalid")
        

    
   

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller=controller
                
        lgbutton=tk.Button(self, text="CANCEL", command=self) 
        button = tk.Button(self, text="OK",
                           command=lambda: controller.show_frame(StartPage))
        lgbutton.pack()
        button.pack(side="bottom")


class PageTwo(tk.Frame): 

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        pass

        
        '''
        
        
        page1 = self.controller.get_page(PageOne)
        a= page1.v.get()
        label = tk.Label(self, text=a, font=TITLE_FONT, foreground="blue")
        label.pack(side="top", fill="x", pady=10)
        
        
        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame(StartPage))

        sendbutton = tk.Button(self, text = "Send Mail", command=self.sendmail)

        senderl.pack(side="top", anchor="w")
        rmail.pack(side="top", anchor="nw")
        senderdomain.pack(side="top", anchor="nw")
        self.textw.pack(fill="both")
        button.pack(side="bottom")
        sendbutton.pack(side="bottom")

    def sendmail(self):
        sent = tk.Label(self, text="Email has been sent")
        if self.senderoption.get() == "@gmail.com":
            try: 
                server.sendmail(self.v.get()+self.optionv.get(), self.reciever.get()+self.senderoption.get(), "YES")
                print("Success")
                sent.pack()
            except:
                print("Unsuccesful")
                print(PageOne.self.v.get())
'''

if __name__ == "__main__":
    app = SampleApp()
    app.title("Person Identifier Using Fingerprint")
#    app.geometry("750x680")
    app.state('zoomed')
    app.mainloop()
