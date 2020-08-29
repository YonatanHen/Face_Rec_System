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


def entrance(username,password):
    '''  Username and password recognition function '''
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
                    playsound('general audio\\welcome.mp3',False)
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

def recognize(username,password):
    ''' function check if username and password match one of the users in users.db,and return the relevant data '''
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? and password=?",[(username),(password)])
    return cursor.fetchall()

def Time_Fixer(time_string):
    ''' fix difference of times (Utility function to faces and entrance functions) '''
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



#["bg"] color blinders - beckground colors array
color1=["#C7C7C7","#A8A8A8","#919191","#848484","#7C7C7C","#727272","#737373","#727272","#717171","white"]

#["fg"] color blinders - font colors array
color2=["#545454","#4B4B4B","#4A4A4A","#434343","#3C3C3C","#323232","#2C2C2C","#242424","#010101","black"] 


def showDetails(x,username):
    ''' show details of a user'''
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


def printUserDetails(username):
    ''' Function prints user details '''
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
        entry1=Entry(root,textvariable=salary).grid(row=2,column=1)
        Button(root,text="Submit",command=lambda:Label(root,\
        text="Total gross profits are {0}".format(float(entry1.get())*float(row[5]))).grid(row=3) if salary.get()>=0
        else messagebox.showerror("Error","Salary must be postivie number!")).grid(row=2,column=2)
    root.mainloop()

font_size=16
def pack_text(self,stri):
    ''' Function gets a string and pack a label with it to the window (the "self"). finally,reads it. '''
    global font_size
    self.ER_label["text"]=stri
    self.ER_label["font"]="verdana "+ str(font_size-1) +" bold italic"
    tts = gTTS(text=stri, lang = 'en')
    tts.save("pack_text.mp3")
    playsound('pack_text.mp3',False)
    if os.path.isfile("pack_text.mp3"):
        os.remove("pack_text.mp3")

def text_window(str):
    ''' Gets string and open a window with the sane string. later,read it (enterCommand function helper) '''
    global font_size
    tts = gTTS(text=str, lang = 'en')
    tts.save("text_window.mp3")
    text_window = Tk()
    text_window.title('text_window')
    Label(text_window, text=str,font="verdana 15 bold italic").pack(side=TOP)
    t_end = time.time() + 3*1
    while time.time() < t_end:
        t_end=t_end
    playsound('text_window.mp3',True)

    if os.path.isfile("text_window.mp3"):
        os.remove("text_window.mp3")

    text_window.after(5000, text_window.destroy)
