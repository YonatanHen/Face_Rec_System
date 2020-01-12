#This page include all the functions that program py files need

import numpy as np
import cv2
import pickle
import camera
import datetime
import time
from gtts import gTTS
import os 
from playsound import playsound
import sqlite3
from getpass import getpass
from time import sleep
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import shutil
import pygame
from gtts import gTTS
from tkinter import messagebox
from adminMenu import AdminMenu


def faces():
    #playing sound in background helping with accessability for visually impaired users.
    pygame.mixer.init()
    pygame.mixer.music.load('background_audio.mp3')
    pygame.mixer.music.play(999)
    #set volume of background music
    pygame.mixer.music.set_volume(0.4)
    if os.path.isfile("match.mp3"):
        os.remove("match.mp3")
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./recognizers/face-trainner.yml")
    labels = {"person_name": 1}
    with open("pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}
    cap = cv2.VideoCapture(0)
    #make 4k
    cap.set(3, 3840)
    cap.set(4, 2160)
    i=0
    isRecCounter = 0
    counter2 = 0
    lrcounter = 8
    name = "None"
    tempname = "None"
    color = (0,0,255)
    beepflag = 1
    tempmatch = "analyzing..."
    trysCounter=0
    #beepuls = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    stroke = 2 #font thickness
    playsound('Take_Down.mp3',False)
    while(True):
        '''
        if cv2.waitKey(20) & 0xFF == ord('v'):
            if beepflag == 0:
                beepflag = 1
            if beepflag == 1:
                beepflag = 0
        if beepflag == 1:
            beepuls += 1
            if beepuls % 25 == 0:
                playsound('beep.mp3',False)
                '''
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=12, minNeighbors=5)
        for (x, y, w, h) in faces:
            #print(x,yq,w,h)
            roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]
            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf>=54.5 and conf <= 60:
                #print(conf)
                #print(5:id_)
                #print(labels[id_], name, isRecCounter,counter2)
                if labels[id_] == name or name == "None":
                    isRecCounter=isRecCounter+1
                    counter2 = 0
                    if isRecCounter == 5:
                        tempname = name
                if tempname != name:
                    counter2 += 1
                #if counter2 % 8==0:
                #    isRecCounter = 0
                    
                name = labels[id_]
                #match sound
                if isRecCounter > 10:
                    match = "Match found: " + tempname
                    color = (0, 255, 0)
                    cv2.putText(frame, match, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                    tts = gTTS(text=match, lang = 'en')
                    tts.save("match.mp3")
                    if os.path.isfile("match.mp3"):
                        playsound("match.mp3",False)
                        cv2.imshow('frame',frame)
                        #delete camera window if match found.
                        cap.release()
                        cv2.destroyAllWindows()
                        sleep(2)
                        usersDB=sqlite3.connect('users.db')
                        cursor=usersDB.cursor() #cursor enable traversal over the records in database
                        results=face_recognize(tempname)
                        for i in results:
                            if(i[6] != "blind worker"):
                                #print("Time is:{0}".format(datetime.datetime.now()))
                                if(i[7] =='no'):
                                    welcome=Tk()
                                    welcome.title("Welcome "+i[0]+" "+i[1])
                                    time_label=Label(welcome,text="Date & Time:{0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                    time_label.pack()
                                    playsound("welcome.mp3",False)
                                    watchDataVar=IntVar()
                                    watchDataVar.set(0)
                                    Checkbutton(welcome,text="Mark the box to watch your data", variable=watchDataVar).pack()
                                    Button(welcome,text="Submit",command=lambda:showDetails(watchDataVar.get(),str(i[2]))).pack()
                                    #Admin's menu
                                    if(i[6]=='Admin' or i[6]=='admin'):
                                        Button(welcome,text="open admin menu",command=AdminMenu).pack()
                                    welcome.mainloop()
                                    enter_time=float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)
                                    cursor.execute("UPDATE users SET entrance=?,isInside='yes' WHERE username=?",[(enter_time),(tempname)])
                                    usersDB.commit()
                                elif(i[7]=='yes'):
                                    print("Goodbye "+i[0]+" "+i[1])
                                    total=str(float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)-(float(i[4])))
                                    total="%.2f" %(float(i[5])+float(total))
                                    total = Time_Fixer(total)
                                    cursor.execute("UPDATE users SET total=?,isInside='no',entrance=0 WHERE username=?",[(total),(tempname)])
                                    usersDB.commit()
                                    playsound("godbye.mp3",False)
                                break
                            else:
                                if(i[7] =='no'):
                                    print("Welcome "+i[0]+" "+i[1])
                                    playsound("welcome.mp3",False)
                                    enter_time=float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)
                                    cursor.execute("UPDATE users SET entrance=?,isInside='yes' WHERE username=?",[(enter_time),(tempname)])
                                    usersDB.commit()
                                else:
                                    print("Goodbye "+i[0]+" "+i[1])
                                    total=str(float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)-(float(i[4])))
                                    total="%.2f" %(float(i[5])+float(total))
                                    total = Time_Fixer(total)
                                    cursor.execute("UPDATE users SET total=?,isInside='no',entrance=0 WHERE username=?",[(total),(tempname)])
                                    usersDB.commit()
                                    playsound("godbye.mp3",False) 
                        if os.path.isfile("match.mp3") :
                            os.remove("match.mp3")
                        tempmatch = match
                        pygame.mixer.music.pause()
                    os.system("main.py")
                elif isRecCounter > 5:
                    color = (0, 255, 0) #green
                    cv2.putText(frame, tempname, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                    
                else:
                    color = (0, 0, 255) #red
                    cv2.putText(frame, "analyzing...", (x,y), font, 1, color, stroke, cv2.LINE_AA)
                                
            else:
                trysCounter+=1
                #counter2+=1
                if trysCounter==5:
                    cv2.putText(frame,"Failed attempt !", (x,y), font, 1, color, stroke, cv2.LINE_AA)
                    for _ in range(100):
                        cv2.imshow('frame',frame)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            # sound
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
                if isRecCounter>10 and counter2 == 0:
                    img_item =  "images\\" + tempname + "\\" + tempname + str(i) +".png"
                else:
                    img_item =  "unknown\\unknown" + str(i) +".png" 
                cv2.imwrite(img_item, roi_color)
                now = (datetime.datetime.now()).strftime("%Y-%m-%d %H_%M_%S")
            subitems = smile_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in subitems:
            #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if trysCounter>100:
            color = (0, 0, 255)
            playsound("Five_failed_attempts.mp3")
            cv2.putText(frame, "Failed attempts !", (x,y), font, 1, color, stroke, cv2.LINE_AA)
            for _ in range(100):
                cv2.imshow('frame',frame)
                
            img_item =  "unknown\\unknown" + str(i) +".png"
            cv2.imwrite(img_item, roi_color)
            pygame.mixer.music.pause()
            cap.release()
            cv2.destroyAllWindows()
            time.sleep(1)
            os.system("main.py")
            break
        if cv2.waitKey(20) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break



class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=BOTTOM)
    
        self.username_but1 = Button(self,text = "Log in/out with username",bg="white",fg="red",command=lambda:controller.show_frame(User_login),font="verdana 15 bold italic")
        self.face_but2 = Button(self,text = "Log in/out with face recognition",bg="white",fg="green",command=lambda:faces(),font="verdana 15 bold italic")

        self.color_but3 = Button(self, text="Change color",command=lambda:changecolor_StartPage(self),bg="white",fg="orange",font="verdana 15 bold italic")   #להפעיל שינוי צבעים 

        self.font_size8 = Button(self,text = "Set font size",bg="white",fg="gold",command=lambda:Change_font_size(self),font="verdana 15 bold italic")

        self.vol_up_but4 = Button(self,text = " Set volume up ",bg="white",fg="blue",command=lambda:change_vol_up(self),font="verdana 15 bold italic")
        self.vol_down_but5 = Button(self,text = "Set volume down",bg="white",fg="blue",command=lambda:change_vol_down(self),font="verdana 15 bold italic")
        self.mute_but6 = Button(self,text = "Mute",bg="white",fg="blue",command=lambda:turn_DU_music(self),font="verdana 15 bold italic")
        self.quit_but7 = Button(self,text = "Quit",bg="white",fg="purple",command=quit,font="verdana 15 bold italic")
        

        self.theLabel = Label(self,text="Welcome !",font="verdana 15 bold italic")
        self.theLabel.pack(fill=X)
        self.username_but1.pack(fill=X)
        self.username_but1.bind("<Button-1>", self.log_sound)
        self.username_but1.bind("<Button-3>", self.log_sound)
        self.face_but2.pack(fill=X)
        self.face_but2.bind("<Button-1>", self.face_sound)
        self.face_but2.bind("<Button-3>", self.face_sound)
        self.color_but3.pack(fill=X)
        self.color_but3.bind("<Button-1>", self.Change_color_sound)
        self.color_but3.bind("<Button-3>", self.Change_color_sound)
        self.font_size8.pack(fill=X)
        self.font_size8.bind("<Button-1>", self.Font_size_sound)
        self.font_size8.bind("<Button-3>", self.Font_size_sound)
        self.space_label1 = Label(self,text="")
        self.space_label1.pack(fill=X)
        self.vol_up_but4.pack(fill=X)
        self.vol_up_but4.bind("<Button-1>", self.vol_up_sound)
        self.vol_up_but4.bind("<Button-3>", self.vol_up_sound)
        self.vol_down_but5.pack(fill=X)
        self.vol_down_but5.bind("<Button-1>", self.vol_down_sound)
        self.vol_down_but5.bind("<Button-3>", self.vol_down_sound)
        self.mute_but6.pack(fill=X)
        self.mute_but6.bind("<Button-1>", self.Mute_sound)
        self.mute_but6.bind("<Button-3>", self.Mute_sound)
        self.space_label2 = Label(self,text="")
        self.space_label2.pack(fill=X)
        self.quit_but7.pack(fill=X)
        self.quit_but7.bind("<Button-1>", self.Quit_sound)
        self.quit_but7.bind("<Button-3>", self.Quit_sound)
        
        self.object_arr=[self.theLabel,self.username_but1,self.face_but2,self.color_but3,self.font_size8,self.space_label1,self.vol_up_but4,self.vol_down_but5,self.mute_but6,self.space_label2,self.quit_but7]
    
    def log_sound(self, event):
        playsound('event sounds\\log.mp3',False)

    def face_sound(self, event):
        playsound('event sounds\\face.mp3',False)

    def Change_color_sound(self, event):
        playsound('event sounds\\Change color.mp3',False)

    def Font_size_sound(self, event):
        playsound('event sounds\\Font_size.mp3',False)

    def vol_up_sound(self, event):
        playsound('event sounds\\vol_up.mp3',False)

    def vol_down_sound(self, event):
        playsound('event sounds\\vol_down.mp3',False)

    def Mute_sound(self, event):
        playsound('event sounds\\Mute.mp3',False)

    def Quit_sound(self, event):
        playsound('event sounds\\Quit.mp3',False)


 
class User_login(tk.Frame):
    global color_changer,color1,color2,is_color_changed,countTries
    def __init__(self,parent,controller):
      
        tk.Frame.__init__(self,parent)
        self.lable_1 = Label(self,text="User Name:",font="verdana 15 bold italic")
        self.lable_2 = Label(self,text="Password:",font="verdana 15 bold italic")
        
        self.username=StringVar()
        self.password=StringVar()

        self.lable_1.grid(row=0,sticky=E)
        self.lable_2.grid(row=1)
        
        self.entry_1=Entry(self,textvariable=self.username)
        self.entry_2=Entry(self,show="*",textvariable=self.password)
        self.back_but1 = Button(self,text = "Go back",bg=color1[9],fg=color2[9],command=lambda:controller.show_frame(StartPage),font="verdana 15 bold italic")
        self.enter_but2 = Button(self,text = "Enter",bg=color1[9],fg=color2[9],command=lambda:enterCommand(self,controller),font="verdana 15 bold italic")
        self.quit_but3 = Button(self,text = "Quit",bg=color1[9],fg=color2[9],command=lambda:quitCommand(controller),font="verdana 15 bold italic")

        self.username.set("")
        self.password.set("")

        self.entry_1.grid(row=0,column=1)
        self.entry_1.bind("<Leave>", self.User_Name_sound)
        self.entry_2.grid(row=1,column=1)
        self.entry_2.bind("<Leave>", self.Password_sound)
        self.back_but1.grid(row=4,columnspan=2)
        self.back_but1.bind("<Leave>", self.Go_back_sound)
        self.enter_but2.grid(row=3,columnspan=2)
        self.enter_but2.bind("<Leave>", self.enter_sound)
        self.quit_but3.grid(row=5,columnspan=2)
        self.quit_but3.bind("<Leave>", self.quit_sound)
        self.ER_label = Label(self,text="")
        self.ER_label.grid(row=7,column=2)

        self.object_arr=[self.lable_1,self.lable_2,self.back_but1,self.enter_but2,self.quit_but3]


    def enter_sound(self, event):
        playsound('event sounds\\Enter.mp3',False)
    
    def quit_sound(self, event):
        playsound('event sounds\\Quit.mp3',False)
    
    def Go_back_sound(self, event):
        playsound('event sounds\\Go back.mp3',False)

    def User_Name_sound(self, event):
        playsound('event sounds\\User Name.mp3',False)

    def Password_sound(self, event):
        playsound('event sounds\\Password.mp3',False)


def quitCommand(controller):
    controller.destroy()
    os.system("main.py")

def enterCommand(self,controller):
    log(self,controller)
    quitCommand(controller)
    
def recognize(username,password):
    """function check if username and password match one of the users in users.db,and return the relevant data"""
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? and password=?",[(username),(password)])
    return cursor.fetchall()

def face_recognize(username):
    """function check if username match one of the users in users.db,and return the relevant data"""
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?",[(username)])
    return cursor.fetchall()


def Time_Fixer(time_string):
    # Separator - hours/minutes
    i=0
    hours=''
    while(time_string[i]!='.'):
        hours=hours+time_string[i]
        i=i+1
    i=i+1
    if time_string[i+1]:
        minutes = time_string[i] + time_string[i+1]
    else:
        minutes = time_string[i] + '0'

    # minutes check
    if(int(minutes)>=60):
        temp_time=str("%.2f" % (float(minutes)/60))
        print(temp_time)
        temp_h=''
        i=0
        while(temp_time[i]!='.'):
            temp_h=temp_h+temp_time[i]
            i=i+1
        i=i+1
        
        hours=int(hours)+int(temp_h)
        minutes = int(minutes)- 60
        
    return str(hours)+'.'+str(minutes)



def printUserDetails(username):
    print(username)
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    "".join(username)
    result=cursor.execute("SELECT * FROM users WHERE username=?",[(username)])
    days=0
    root=Tk()
    root.title("Show {} details".format(username))
    for row in result:
        Label(root,text="total hours:"+ row[5]).grid(row=0,column=0)
        if(float(row[5])%24!=0):
            days+=1
        if (float(row[5])>=24):
            days=float(row[5])//24
        Label(root,text="total days:"+ str(days)).grid(row=1,column=0)
        Label(root,text="Enter your hourly wage: ").grid(row=2,column=0)
        salary=DoubleVar()
        Entry(root,textvariable=salary).grid(row=2,column=1)
        Button(root,text="Submit",command=lambda:Label(root,\
        text="Total gross profits are {0}".format(float(entry1.get())*float(row[5]))).grid(row=3) if salary.get()>=0\
        else messagebox.showerror("Error","Salary must be postivie number!")).grid(row=2,column=2)
    root.mainloop()


music_vol=1
music_flag=0
countTries=0 #counter entrance tries
def change_vol_down(self):
    global music_vol
    if(music_vol>0):
        music_vol-=0.25
        pygame.mixer.music.set_volume(music_vol)
    elif(music_vol==0):
        self.mute_but6["fg"]="red"

def change_vol_up(self):
    global music_vol
    if(music_vol<1):
        music_vol+=0.25
        pygame.mixer.music.set_volume(music_vol)
        self.mute_but6["fg"]="blue"

def turn_DU_music(self):
    global music_flag,music_vol
    if(music_flag==0) & (music_vol!=0):
        pygame.mixer.music.set_volume(0)
        self.mute_but6["fg"]="red"
        music_flag=1
    else:
        music_flag=0
        if(music_vol==0):
            music_vol=0.25
        pygame.mixer.music.set_volume(music_vol)
        self.mute_but6["fg"]="blue"


def log(self,controller):
    global countTries
    if recognize(self.username.get(),self.password.get()):
        entrance(self.username.get(),self.password.get())
    elif(countTries!=5):
        pack_text(self,"user-name and password not recognized,please enter again")
        countTries+=1
    else:
        countTries=0
        pack_text(self,"You tried to enter 5 times unssuccessfully!")
        controller.show_frame(StartPage)
        #os.system("main.py")

def text_window(str):
    global font_size
    tts = gTTS(text=str, lang = 'en')
    tts.save("text_window.mp3")
    playsound('text_window.mp3',False)
    text_window = Tk()
    text_window.title('text_window')
    Label(text_window, text=str,font="verdana 15 bold italic").pack(side=TOP)

    if os.path.isfile("text_window.mp3"):
        os.remove("text_window.mp3")

    text_window.after(5000, text_window.destroy)

def pack_text(self,stri):
    global font_size
    tts = gTTS(text=stri, lang = 'en')
    tts.save("pack_text.mp3")
    playsound('pack_text.mp3',False)
    self.ER_label["text"]=stri
    self.ER_label["font"]="verdana "+ str(font_size-1) +" bold italic"
    if os.path.isfile("pack_text.mp3"):
        os.remove("pack_text.mp3")

color_changer=0
color1=["#C7C7C7","#A8A8A8","#919191","#848484","#7C7C7C","#727272","#737373","#727272","#717171","white"] #["bg"]
color2=["#545454","#4B4B4B","#4A4A4A","#434343","#3C3C3C","#323232","#2C2C2C","#242424","#010101","black"] #["fg"]

def changecolor_StartPage(self):
    global color_changer,color1,color2
    if(color_changer!=9):
        if(str(self)!=".!frame.!startpage"):
            color_changer-=1
        for i in range(len(self.object_arr)):
            self.object_arr[i]["bg"]=color1[color_changer]
            self.object_arr[i]["fg"]=color2[color_changer]
        color_changer+=1
    if(color_changer==9):
        for i in range(len(self.object_arr)):
            self.object_arr[i]["bg"]=color1[color_changer]
        
        self.username_but1["fg"]="red"
        self.face_but2["fg"]="green"
        self.color_but3["fg"]="orange"
        self.font_size8["fg"]="gold"
        self.vol_up_but4["fg"]="blue"
        self.vol_down_but5["fg"]="blue"
        self.mute_but6["fg"]="blue"
        self.quit_but7["fg"]="purple"
        self.space_label1["bg"] = color1[9]
        self.space_label1["fg"] = color1[9]
        self.space_label2["bg"] = color1[9]
        self.space_label2["fg"] = color1[9]
        color_changer=0
        

def changecolor_User_login(self):
    global color_changer
    if(color_changer!=0):
        self["bg"]=color1[color_changer-1]
        for i in range(len(self.object_arr)):
            self.object_arr[i]["bg"]=color1[color_changer-1]
            self.object_arr[i]["fg"]=color2[color_changer-1]

    else:
        for i in range(len(self.object_arr)):
            self.object_arr[i]["bg"]=color1[9]
            self.object_arr[i]["fg"]=color2[9]


font_size=16
def Change_font_size(self):
    global font_size
    if(str(self)!=".!frame.!startpage"):
        font_size-=1
    for i in range(len(self.object_arr)):
        self.object_arr[i]["font"] = "verdana " + str(font_size) + " bold italic"
    font_size+=1
    if((font_size==30) & (str(self)!=".!frame.!startpage")) | (font_size==31):
        font_size=16


def showDetails(x,username):
    if (x):
        usersDB=sqlite3.connect('users.db')
        cursor=usersDB.cursor()
        result=cursor.execute("SELECT * FROM users WHERE username=?",[(username)])
        days=0
        for row in result:
            root=Tk()
            root.title("Show {} details".format(row[2]))
            Label(root,text="total hours: {}".format(row[5])).grid(row=0)
            if(float(row[5])%24!=0):
                days+=1
            if (float(row[5])>=24):
                days=float(row[5])//24
            Label(root,text="total days: {}".format(days)).grid(row=1)
            Label(root,text="Enter your hourly wage: ").grid(row=2,column=0)
            salary=DoubleVar(root,0.0)
            Entry(root,textvariable=salary).grid(row=2,column=1)
            Button(root,text="Submit",command=lambda:Label(root,text="Total gross profits are {0}".format(salary.get()*float(row[5]))).grid(row=3) if\
            salary.get()>=0 else
            messagebox.showerror("Error","Salary must be postivie number!")).grid(row=2,column=2)
        root.mainloop()
    else:
        messagebox.showinfo("Info","OK! Have a nice Day!")

def entrance(username,password):
    #Users databse columns order:
    #0.first_name,1.last_name,2.username,3.password,4.entrance,5.total,6.role,7.isInside
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor() #cursor enable traversal over the records in database
    global countTries
    while True:
        results=recognize(username,password)
        if results: #if results!=NULL, in other words, if user found in the DB
            for i in results:
                if(i[7] =='no'):
                    welcome=Tk()
                    welcome.title("Welcome "+i[0]+" "+i[1])
                    time_label=Label(welcome,text="Date & Time:{0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    time_label.pack()
                    playsound("welcome.mp3",False)
                    watchDataVar=IntVar(welcome,0)
                    Checkbutton(welcome,text="Mark the box to watch your data", variable=watchDataVar).pack()
                    Button(welcome,text="Submit",command=lambda:showDetails(watchDataVar.get(),str(i[2]))).pack()
                    #Admin's menu
                    if(i[6]=='Admin' or i[6]=='admin'):
                        Button(welcome,text="open admin menu",command=AdminMenu).pack()
                    welcome.mainloop()
                    playsound('welcome.mp3',False)
                    enter_time=float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)
                    cursor.execute("UPDATE users SET entrance=?,isInside='yes' WHERE username=?",[(enter_time),(username)])
                    usersDB.commit()
                elif(i[7]=='yes'):
                    print("Goodbye "+i[0]+" "+i[1])
                    total=str(float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)-(float(i[4])))
                    total="%.2f" %(float(i[5])+float(total))
                    total = Time_Fixer(total)
                    cursor.execute("UPDATE users SET total=?,isInside='no',entrance=0 WHERE username=?",[(total),(username)])
                    usersDB.commit()
            break
