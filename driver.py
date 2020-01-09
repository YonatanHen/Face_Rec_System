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

LARGE_FONT=("verdana",10)

class SeaofBTCapp(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.title('Hours registration system')
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
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=BOTTOM)
    
        username_but1 = Button(self,text = "Login with username",bg="white",fg="red",command=lambda:controller.show_frame(User_login))
        vol_but2 = Button(self,text = "Turn down/up beep",bg="white",fg="blue")
        button3 = Button(self,text = "Login",bg="white",fg="green")
        quit_but4 = Button(self,text = "Quit",bg="white",fg="purple",command=quit)
        
        theLabel = Label(self,text="Yarin avraham !")
        theLabel.pack()
        username_but1.pack(fill=X)
        vol_but2.pack(fill=X)
        #button3.pack(side=LEFT)
        quit_but4.pack(fill=X)
        
        # מוסיף קוביה לכתיבה ומד
        m1 = PanedWindow() 
        m1.pack(fill = BOTH, expand = 1) 
        #left = Entry(m1, bd = 5) // write box 
        #m2 = PanedWindow(m1, orient = VERTICAL) 
        #m1.add(m2) 

        #top = Scale( m2, orient = HORIZONTAL) #meuzan
        #m2.add(top) 

        w = Scale(m1, from_=0, to=42) #meunah
        w.pack(side=LEFT) 

 
class User_login(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        lable_1 = Label(self,text="User Name:")
        lable_2 = Label(self,text="Password:")
        
        username=StringVar()
        password=StringVar()

        lable_1.grid(row=0,sticky=E)
        lable_2.grid(row=1)
        entry_1=Entry(self,textvariable=username).grid(row=0,column=1)
        entry_2=Entry(self,textvariable=password).grid(row=1,column=1)

        coutnt_try=0
        back_but1 = Button(self,text = "Go back",bg="white",fg="black",command=lambda:controller.show_frame(StartPage))
        enter_but2 = Button(self,text = "Enter",bg="white",fg="black",command=lambda:entrance.entrance(username.get(),password.get()))
        quit_but3 = Button(self,text = "Quit",bg="white",fg="black",command=quit)

        c=Checkbutton(self,text="Keep me logged in !")
        back_but1.grid(row=3,columnspan=1)
        enter_but2.grid(row=3,columnspan=2)
        quit_but3.grid(row=4,columnspan=1)
        c.grid(columnspan=2)


class camera_frame(tk.Frame):
    def __init__(self,parent,controller):
            tk.Frame.__init__(self,parent)
            if os.path.isfile("match.mp3"):
                os.remove("match.mp3")
                print("removed")
            face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')
            eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
            smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')

            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read("./recognizers/face-trainner.yml")

            labels = {"person_name": 1}
            with open("pickles/face-labels.pickle", 'rb') as f:
                og_labels = pickle.load(f)
                labels = {v:k for k,v in og_labels.items()}

            #self.canvas = tkinter.Canvas(self, width = 1500, height = 720)
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
            #beepuls = 0
            
            while(True):
                # Capture frame-by-frame
                ret, self = self.cap.read()
                self = cv2.flip(self,1)
                gray  = cv2.cvtColor(self, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=12, minNeighbors=5)
                ''' 
                for (x, y, w, h) in faces:
                    #print(x,y,w,h)
                    roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
                    roi_color = frame[y:y+h, x:x+w]

                    # recognize? deep learned model predict keras tensorflow pytorch scikit learn
                    id_, conf = recognizer.predict(roi_gray)
                    if conf>=54.5 and conf <= 60:
                        #print(conf)
                        #print(5: #id_)
                        print(labels[id_], name, counter1,counter2)

                        font = cv2.FONT_HERSHEY_SIMPLEX
                        if labels[id_] == name or name == "None":
                            counter1+=1
                            counter2 = 0
                            if counter1 == 10:
                                tempname = name
                        if tempname != name:
                            counter2 += 1
                        if counter2 >= 8:
                            counter1 = 0
                            
                        name = labels[id_]
                        
                        stroke = 2 #font thickness

                        if counter1 > 10:
                            color = (0, 255, 0) #green
                            cv2.putText(frame, tempname, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                            
                        else:
                            color = (0, 0, 255) #red
                            cv2.putText(frame, "analyzing...", (x,y), font, 1, color, stroke, cv2.LINE_AA)
                            
                    else:
                        counter2+=1
                    
                    cv2.imshow('frame',frame)

                    stroke = 2
                    end_cord_x = x + w
                    end_cord_y = y + h
                    cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
                    # sound
                    print(x)
                    if x < 350:
                        if lrcounter % 10 == 0:
                            playsound('moveright.mp3',False)
                        lrcounter+=1
                    
                    elif x > 680:
                        if lrcounter % 10 == 0:
                            playsound('moveleft.mp3',False)
                        lrcounter+=1

                    if cv2.waitKey(20) & 0xFF == ord('p'):
                        i+=1
                        if counter1>10 and counter2 == 0:
                            img_item =  "images\\" + tempname + "\\" + tempname + str(i) +".png"
                        else:
                            img_item =  "unknown\\unknown" + str(i) +".png" 
                        cv2.imwrite(img_item, roi_color)
                        #now = (datetime.datetime.now()).strftime("%Y-%m-%d %H_%M_%S")
                    #subitems = smile_cascade.detectMultiScale(roi_gray)
                    #for (ex,ey,ew,eh) in subitems:
                    #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
                '''
                # Display the resulting frame
                cv2.imshow('frame',self)

                if cv2.waitKey(20) & 0xFF == ord('q'):
                    break
                
            # When everything done, release the capture
            cap.release()
            cv2.destroyAllWindows()

app = SeaofBTCapp()
app.mainloop()
