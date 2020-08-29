import tkinter as tk
from tkinter import *
from playsound import playsound
import User_login
import pygame
from gtts import gTTS
import time
import os 
import numpy as np
import cv2
import pickle
import datetime
import sqlite3
from time import sleep
from adminMenu import AdminMenu
from Functions import Time_Fixer,showDetails

music_vol=1
music_flag=0
#color_changer - an index to color arrays
color_changer=0

#["bg"] color blinders - beckground colors array
color1=["#C7C7C7","#A8A8A8","#919191","#848484","#7C7C7C","#727272","#737373","#727272","#717171","white"]

#["fg"] color blinders - font colors array
color2=["#545454","#4B4B4B","#4A4A4A","#434343","#3C3C3C","#323232","#2C2C2C","#242424","#010101","black"] 

class StartPage(tk.Frame):
    ''' StartPage class - GUI menu page '''
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=BOTTOM)

        self.theLabel = Label(self,text="Welcome !",font="verdana 15 bold italic")
        self.username_but1 = Button(self,text = "Log in/out with username and password",bg="white",fg="red",command=lambda:controller.show_frame(ul),font="verdana 15 bold italic")
        self.face_but2 = Button(self,text = "Log in/out with face recognition",bg="white",fg="green",command=lambda:faces(),font="verdana 15 bold italic")
        self.color_but3 = Button(self, text="Change color",command=lambda:changecolor(self),bg="white",fg="orange",font="verdana 15 bold italic") 
        self.font_size8 = Button(self,text = "Set font size",bg="white",fg="gold",command=lambda:Change_font_size(self),font="verdana 15 bold italic")
        self.vol_up_but4 = Button(self,text = " Set volume up ",bg="white",fg="blue",command=lambda:self.change_vol_up(),font="verdana 15 bold italic")
        self.vol_down_but5 = Button(self,text = "Set volume down",bg="white",fg="blue",command=lambda:self.change_vol_down(),font="verdana 15 bold italic")
        self.mute_but6 = Button(self,text = "Mute",bg="white",fg="blue",command=lambda:self.turn_DU_music(),font="verdana 15 bold italic")
        self.quit_but7 = Button(self,text = "Turn off system",bg="white",fg="purple",command=quit,font="verdana 15 bold italic")
        
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
        self.quit_but7.bind("<Button-1>", self.Turn_of_sound)
        self.quit_but7.bind("<Button-3>", self.Turn_of_sound)
        
        self.object_arr=[self.theLabel,self.username_but1,self.face_but2,self.color_but3,self.font_size8,self.space_label1,self.vol_up_but4,self.vol_down_but5,self.mute_but6,self.space_label2,self.quit_but7]
    
    def log_sound(self, event):
        ''' When clicked "Log in/out with username" button, it will be said - "Log in/out with username" '''
        playsound('event audio\\log.mp3',False)

    def face_sound(self, event):
        ''' when clicked "Log in/out with face recognition" , it will be said - "Log in/out with face recognition" '''
        playsound('event audio\\face.mp3',False)

    def Change_color_sound(self, event):
        ''' when clicked "Change color" , it will be said - "Change color" '''
        playsound('event audio\\Change color.mp3',False)

    def Font_size_sound(self, event):
        ''' when clicked "Set font size" , it will be said - "Set font size" '''
        playsound('event audio\\Font_size.mp3',False)

    def vol_up_sound(self, event):
        ''' when clicked "Set volume up" , it will be said - "Set volume up" '''
        playsound('event audio\\vol_up.mp3',False)

    def change_vol_up(self):
        ''' when clicked "Set volume up" , increase the volume '''
        global music_vol
        if(music_vol<1):
            music_vol+=0.25
            pygame.mixer.music.set_volume(music_vol)
            self.mute_but6["fg"]="blue"

    def vol_down_sound(self, event):
        ''' when clicked to enter "Change color" , it will be said - "Set volume down" '''
        playsound('event audio\\vol_down.mp3',False)

    def change_vol_down(self):
        ''' when "Set sound volume down" clicked , decrease the volume'''
        global music_vol
        if(music_vol>0):
            music_vol-=0.25
            pygame.mixer.music.set_volume(music_vol)
        if(music_vol==0):
            self.mute_but6["fg"]="red"

    def Mute_sound(self, event):
        '''  When "Mute" clicked , it will be said - "Mute" '''
        playsound('event audio\\Mute.mp3',False)

    def turn_DU_music(self):
        ''' When "mute" clicked, it will be said "Mute sound " '''
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

    def Turn_of_sound(self, event):
        ''' When "Turn off system" clicked- it will be said "Turn off system" '''
        playsound('event audio\\Turn_off.mp3',True)


def changecolor(self):
    global color_changer,color1,color2
    if(str(self)==".!frame.!startpage"):
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
    else:
        if(color_changer!=0):
            self["bg"]=color1[color_changer-1]
            for i in range(len(self.object_arr)):
                self.object_arr[i]["bg"]=color1[color_changer-1]
                self.object_arr[i]["fg"]=color2[color_changer-1]

        else:
            for i in range(len(self.object_arr)):
                self.object_arr[i]["bg"]=color1[9]
                self.object_arr[i]["fg"]=color2[9]

# font_size -current font size
font_size=16
def Change_font_size(self):
    ''' change font size of the classes '''
    global font_size
    if(str(self)!=".!frame.!startpage"):
        font_size-=1
    for i in range(len(self.object_arr)):
        self.object_arr[i]["font"] = "verdana " + str(font_size) + " bold italic"
    font_size+=1
    if((font_size==30) & (str(self)!=".!frame.!startpage")) | (font_size==31):
        font_size=16

def faces():
    ''' Face recognition function operates the face recogintion process  '''
    # playing sound in background helping with accessability for visually impaired users.
    pygame.mixer.init()
    pygame.mixer.music.load('general audio\\background_audio.mp3')
    pygame.mixer.music.play(999)
    # set volume of background music
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
    stroke = 2 # font thickness
    playsound('general audio\\Take_Down.mp3',False)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray)
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]
            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf>=54.5 and conf <= 60:
                if labels[id_] == name or name == "None":
                    isRecCounter=isRecCounter+1
                    counter2 = 0
                    if isRecCounter == 10:
                        tempname = name
                if tempname != name:
                    counter2 += 1
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
                                    playsound("general audio\\goodbye.mp3",False)
                                break
                            else:
                                if(i[7] =='no'):
                                    print("Welcome "+i[0]+" "+i[1])
                                    playsound("general audio\\welcome.mp3",False)
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
                                    playsound("general audio\\goodbye.mp3",False) 
                        if os.path.isfile("match.mp3") :
                            os.remove("match.mp3")
                        tempmatch = match
                        pygame.mixer.music.pause()
                    os.system("main.py")
                elif isRecCounter > 9:
                    color = (0, 255, 0) #green
                    cv2.putText(frame, tempname, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                    
                else:
                    color = (0, 0, 255) #red
                    cv2.putText(frame, "analyzing...", (x,y), font, 1, color, stroke, cv2.LINE_AA)
                                
            else:
                trysCounter+=1
                if trysCounter==10:
                    cv2.putText(frame,"Failed attempt !", (x,y), font, 1, color, stroke, cv2.LINE_AA)
                    for _ in range(100):
                        cv2.imshow('frame',frame)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            if trysCounter<=100:
                cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            # sound
            if x < 350:
                if lrcounter % 10 == 0:
                    playsound('general audio\\moveright.mp3',False)
                lrcounter+=1
            
            elif x > 680:
                if lrcounter % 10 == 0:
                    playsound('general audio\\moveleft.mp3',False)
                lrcounter+=1
            if cv2.waitKey(20) & 0xFF == ord('p'):
                i+=1
                if isRecCounter>15 and counter2 == 0:
                    img_item =  "images\\" + tempname + "\\" + tempname + str(i) +".png"
                else:
                    img_item =  "unknown\\unknown" + str(i) +".png" 
                cv2.imwrite(img_item, roi_color)
                now = (datetime.datetime.now()).strftime("%Y-%m-%d %H_%M_%S")
            subitems = smile_cascade.detectMultiScale(roi_gray)
        # Display the resulting frame
        cv2.imshow('frame',frame)

        if trysCounter>100:
            color = (0, 0, 255)
            playsound("general audio\\Five_failed_attempts.mp3")
            cv2.putText(frame, "Failed attempts !", (x,y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
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
            pygame.mixer.music.pause()
            cap.release()
            cv2.destroyAllWindows()
            break

def face_recognize(username):
    ''' Check if the face is in the database (Utility function to faces)
    function checks if username match one of the users in users.db, and return the relevant data '''
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?",[(username)])
    return cursor.fetchall()