import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter
import numpy as np
import cv2
import pickle
from playsound import playsound
import camera
import datetime
from gtts import gTTS
import os
import pygame
import sys
import faces
import entrance
import User_login

LARGE_FONT=("verdana",10)

class SeaofBTCapp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.title('Hours registeration system')
        container = tk.Frame(self)

        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}

        for F in (StartPage,User_login):
            frame=F(container,self)
            self.frames[F] = frame
            frame.grid(row = 0,column = 0,sticky = "nsew")
        self.show_frame(StartPage)


    def show_frame(self,controller):
        frame = self.frames[controller]
        frame.tkraise() #make front

    
class StartPage(tk.Frame):
    ''' Start page class '''
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=BOTTOM)
    
        username_but1 = Button(self,text = "Log in/out with username",bg="white",fg="red",command=lambda:controller.show_frame(User_login))
        vol_but2 = Button(self,text = "Turn down/up music",bg="white",fg="blue")
        button3 = Button(self,text = "Login",bg="white",fg="green")
        quit_but4 = Button(self,text = "Quit",bg="white",fg="purple",command=quit)
        username_but1.pack(fill=X)
        vol_but2.pack(fill=X)
        quit_but4.pack(fill=X)
        m1 = PanedWindow() 
        m1.pack(fill = BOTH, expand = 1) 
        w = Scale(m1, from_=0, to=42) #Horizontal
        w.pack(side=LEFT) 

 
class User_login(tk.Frame):
    ''' User login class '''
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label_1 = Label(self,text="User Name:")
        label_2 = Label(self,text="Password:")
        
        self.username=StringVar()
        self.password=StringVar()

        label_1.grid(row=0,sticky=E)
        label_2.grid(row=1)
        entry_1=Entry(self,textvariable=self.username).grid(row=0,column=1)
        entry_2=Entry(self,textvariable=self.password).grid(row=1,column=1)
        back_but1 = Button(self,text = "Go back",bg="white",fg="black",command=lambda:controller.show_frame(StartPage))
        enter_but2 = Button(self,text = "Enter",bg="white",fg="black",command=lambda:entrance.entrance(self.username.get(),self.password.get()))
        quit_but3 = Button(self,text = "Quit",bg="white",fg="black",command=quit)

        c=Checkbutton(self,text="Keep me logging in !")
        back_but1.grid(row=3,columnspan=1)
        enter_but2.grid(row=3,columnspan=2)
        quit_but3.grid(row=4,columnspan=1)
        c.grid(columnspan=2)


class camera_frame(tk.Frame):
    def __init__(self,parent,controller):
            tk.Frame.__init__(self,parent)
            if os.path.isfile("match.mp3"):
                os.remove("match.mp3")
                #print("removed")
            face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')
            eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
            smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("./recognizers/face-trainner.yml")

            labels = {"person_name": 1}
            with open("pickles/face-labels.pickle", 'rb') as f:
                og_labels = pickle.load(f)
                labels = {v:k for k,v in og_labels.items()}

            self.canvas.pack(side=RIGHT)
            self.cap = cv2.VideoCapture(0)
            self.cap.set(3, 3840)
            self.cap.set(4, 2160)
            i=0
            counter1 = 0
            counter2 = 0
            lrcounter = 8
            name = "None"
            tempname = "None"
            color = (0,0,255)
            beepflag = 1
            tempmatch = 'None'
            
            while(True):
                # Capture frame-by-frame
                ret, self = self.cap.read()
                self = cv2.flip(self,1)
                gray  = cv2.cvtColor(self, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=12, minNeighbors=5)
        
                # Display the resulting frame
                cv2.imshow('frame',self)

                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
                
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()

