#This page include all the functions that program py files need

import numpy as np
import cv2
import pickle
import camera
import datetime
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
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
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
        Label(root,text="Enter your hourly wage").grid(row=2,column=0)
        salary=DoubleVar()
        Entry(root,textvariable=salary).grid(row=2,column=1)
        Button(root,text="Submit",command=lambda:Label(root,\
        text="Total gross profits are {0}".format(float(salary.get())*float(row[5]))) if salary.get()>=0\
        else messagebox.showerror("Error","Salary must be postivie number!")).grid(row=2,column=2)
    root.mainloop()

#def changefont(s):
#    window.f=s

"""

def adminMenu():
    exit=False
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    print("Please choose one of the options below:")
    while(exit==False):
        print("1.Change user data\n2.Change the volume of the system\n3.Delete user\s\n4.watch users data\n5.add new user\n6.Add new photo to an exist user\n7.change font size\n8.change color\n9.Exit")
        option=input("Enter an option: ")
        if(option=='1'):
            uname=input("Enter the username:")
            cursor.execute("SELECT * FROM users WHERE username=?",[(uname)])
            flag=cursor.fetchall()
            if flag:
                field=input("Enter a field that you want to change:")
                newVal=input("Enter the new value of {} {}:".format(uname,field))
                cursor.execute("UPDATE users SET {}=? WHERE username=?".format(field),[(str(newVal)),(uname)])
                usersDB.commit()
            else:
                print("Username not found...")
        elif(option=='2'):
            print("Please enter numbers between 0 to 100")
            vol=input()
            vol=vol/100
            pygame.mixer.music.set_volume(vol)
        elif(option=='3'):
            usernameDel=input("Enter the username that you want to delete:")
            flag=cursor.execute("SELECT username FROM users WHERE username=?",[(usernameDel)])
            if(flag):
                cursor.execute("DELETE from users WHERE username=?",[(usernameDel)])
                usersDB.commit()
                shutil.rmtree("images//"+str(usernameDel), ignore_errors=True)
                print("User deleted successfully!\n")
            else:
                print("Username wasn't found in the database.")   
        elif(option=='4'):
            cursor.execute("select * from users")
            for row in cursor:
                print(row)
        elif(option=='5'):
            uname=input("Enter the username: ")
            flag=cursor.execute("SELECT * FROM users WHERE username=?",[(uname)])
            flag=cursor.fetchall()
            if flag:
                print("user name already exist...")
            else:
                fName=input("Enter first name: ")
                lName=input("Enter last name: ")
                password=input("Enter password: ")
                role=input("Enter role (admin or worker): ")
                total=entrance=0
                isInside='no'
                #add the entred data to the database
                cursor.execute("""'''INSERT INTO users (first_name, last_name, username, password, entrance, total, role, isInside)
                    VALUES (?,?,?,?,?,?,?,?)'''""",[(fName),(lName),(uname),(password),(entrance),(total),(role),(isInside)])
                usersDB.commit() 
                print("Data added succesfully")
                print("Now, take few pictures of the new worker... press p -take a picture/q -stop Capturing")
                
                key = cv2. waitKey(1)
                webcam = cv2.VideoCapture(0)
                
                sleep(2)
                path="images//"+str(uname)
                os.mkdir(path)
                i=0
                while True:
                    check, frame = webcam.read()
                    frame = cv2.flip(frame,1)
                    cv2.imshow('Capturing', frame)
                    if cv2.waitKey(20) & 0xFF == ord('p'):
                        i+=1
                        cv2.imwrite(filename="images\\" + str(uname) + "\\" + str(uname) + str(i) +".png", img=frame)
                        print("Image saved!")
                        
                    elif cv2.waitKey(20) & 0xFF == ord('q'):
                        webcam.release()
                        cv2.destroyAllWindows()
                        break

        elif (option=='6'):
            root = tk.Tk()
            root.withdraw()
            while(True):
                user_fol=input("Enter username to add a picture to: ")
                root.attributes("-topmost", True)
                if os.path.isdir("images\\" + user_fol):
                    add_photo=None
                    while add_photo!='1' and add_photo!='2' and add_photo!='3':
                        add_photo=input("For choose an exist photo press 1, to take a new photo press 2, to go back to menu press 3: ")
                    if add_photo=='1':
                        file_path = filedialog.askopenfilename()
                        newPath = shutil.copy(file_path, "images\\" + user_fol + "\\" )
                        print("\nNow the user have a new picture !\n")
                    elif add_photo=='2':
                        webcam = cv2.VideoCapture(0)
                        i=0
                        while  os.path.isfile("images\\" + user_fol + "\\" + user_fol + str(i) +".png"):
                            i+=1
                        i-=1
                        while True:
                            check, frame = webcam.read()
                            frame = cv2.flip(frame,1)
                            cv2.imshow('Capturing', frame)
                            if cv2.waitKey(20) & 0xFF == ord('p'):
                                i+=1
                                cv2.imwrite(filename="images\\" + user_fol + "\\" + user_fol + str(i) +".png", img=frame)
                                print("Image saved!")
                                
                            elif cv2.waitKey(20) & 0xFF == ord('q'):
                                webcam.release()
                                cv2.destroyAllWindows()
                                sleep(2)
                                print("\nNow the user have a new picture/s !\n")
                                break
                    else:
                        break            
                else:                    
                    try_again=None
                    while try_again!='y' and try_again!='n':
                        try_again=input(("There is no folder to username - {0}, do you want to try again? y/n: ".format(user_fol)))
                    if try_again=='n':
                        break
                    

        elif (option=='7'):
            print("Enter font size\n0-30")
            size=input()

        elif(option=='8'):
            print("enter a color for backgound")
            color=input()

        elif(option=='9'):
            exit=True
            print("Exiting admin's menu...")
        else:
            print("Wrong input,Enter again.")

"""




music_vol=1
music_flag=0
countTries=0 #counter entrance tries
def change_vol_down(self):
    global music_vol
    if(music_vol>0):
        music_vol-=0.25
        pygame.mixer.music.set_volume(music_vol)

def change_vol_up():
    global music_vol
    if(music_vol<1):
        music_vol+=0.25
        pygame.mixer.music.set_volume(music_vol)
        self.mute_but6["fg"]="blue"
    else:
        self.mute_but6["fg"]="red"

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


def log(controller,us,passw):
    global countTries
    if recognize(us,passw):
        entrance(us,passw)
        text_window("have a nice day !")
    elif(countTries!=5):
        text_window("user-name and password not recognized,please enter again")
        countTries+=1
    else:
        countTries=0
        text_window("You tried to enter 5 times unssuccessfully!")
        controller.show_frame(User_login)

def text_window(str):
    tts = gTTS(text=str, lang = 'en')
    tts.save("text_window.mp3")
    playsound('text_window.mp3',False)
    text_window = Tk()
    text_window.title('text_window')
    Label(text_window, text=str,font="verdana 15 bold italic").pack(side=TOP)

    if os.path.isfile("text_window.mp3"):
        os.remove("text_window.mp3")

    text_window.after(5000, text_window.destroy)


    
color_changer=0
color1=["#C7C7C7","#A8A8A8","#919191","#848484","#7C7C7C","#727272","#737373","#727272","#717171","white"] #["bg"]
color2=["#545454","#4B4B4B","#4A4A4A","#434343","#3C3C3C","#323232","#2C2C2C","#242424","#010101","black"] #["fg"]

def changecolor_StartPage(self):
    global color_changer,color1,color2
    if(color_changer!=9):
        self.username_but1["bg"]=color1[color_changer]
        self.username_but1["fg"]=color2[color_changer]
        self.theLabel["bg"]=color1[color_changer]
        self.theLabel["fg"]=color2[color_changer]
        self.face_but2["bg"]=color1[color_changer]
        self.face_but2["fg"]=color2[color_changer]
        self.color_but3["bg"]=color1[color_changer]
        self.color_but3["fg"]=color2[color_changer]
        self.vol_up_but4["bg"]=color1[color_changer]
        self.vol_up_but4["fg"]=color2[color_changer]
        self.vol_down_but5["bg"]=color1[color_changer]
        self.vol_down_but5["fg"]=color2[color_changer]
        self.mute_but6["bg"]=color1[color_changer]
        self.mute_but6["fg"]=color2[color_changer]
        self.quit_but7["bg"]=color1[color_changer]
        self.quit_but7["fg"]=color2[color_changer]

        self.space_label1["bg"] = color1[color_changer]
        self.space_label1["fg"] = color1[color_changer]
        self.space_label2["bg"] = color1[color_changer]
        self.space_label2["fg"] = color1[color_changer]
        color_changer+=1
    if(color_changer==9):
        self.theLabel["bg"]=color1[color_changer]
        self.username_but1["bg"]=color1[color_changer]
        self.username_but1["fg"]="red"
        self.face_but2["bg"]=color1[color_changer]
        self.face_but2["fg"]="green"
        self.color_but3["bg"]=color1[color_changer]
        self.color_but3["fg"]="orange"
        self.vol_up_but4["bg"]=color1[color_changer]
        self.vol_up_but4["fg"]="blue"
        self.vol_down_but5["bg"]=color1[color_changer]
        self.vol_down_but5["fg"]="blue"
        self.mute_but6["bg"]=color1[color_changer]
        self.mute_but6["fg"]="blue"
        self.quit_but7["bg"]=color1[color_changer]
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
        self.back_but1["bg"]=color1[color_changer-1]
        self.back_but1["fg"]=color2[color_changer-1]
        self.enter_but2["bg"] = color1[color_changer-1]
        self.enter_but2["fg"] = color2[color_changer-1]
        self.quit_but3["bg"] = color1[color_changer-1]
        self.quit_but3["fg"] = color2[color_changer-1]
        self.lable_1["bg"] = color1[color_changer-1]
        self.lable_1["fg"] = color2[color_changer-1]
        self.lable_2["bg"] = color1[color_changer-1]
        self.lable_2["fg"] = color2[color_changer-1]
    else:
        self.back_but1["bg"]=color1[9]
        self.back_but1["fg"]=color2[9]
        self.enter_but2["bg"] = color1[9]
        self.enter_but2["fg"] = color2[9]
        self.quit_but3["bg"] = color1[9]
        self.quit_but3["fg"] = color2[9]
        self.lable_1["bg"] = color1[9]
        self.lable_1["fg"] = color2[9]
        self.lable_2["bg"] = color1[9]
        self.lable_2["fg"] = color2[9]
