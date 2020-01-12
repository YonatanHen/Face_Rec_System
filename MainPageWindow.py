from tkinter import *
import cv2
from tkinter import *
import keyboard
import os
import pygame
import sys
import datetime
import time


i=0
def changecolor():
    global i
    color1=["#C7C7C7","#A8A8A8","#919191","#848484","#7C7C7C","#727272","#737373","#727272","#717171"]
    color2=["#545454","#4B4B4B","#4A4A4A","#434343","#3C3C3C","#323232","#2C2C2C","#242424","#010101"]
    window["bg"]=color1[i]
    label_1["bg"]=color1[i]
    label_1["fg"]=color2[i]
    i+=1
    if(i==9):
        i=0
f=20
def changefontsize():
    global f
    f+=1
    label_1["font"] = ('Arial' , f)
    if(f==30):
        f=20

def WelcomeWindow():  
    window=Tk()
    window.title('Face_Rec_System')
    label_1=Label(window,text="Welcome,Please use the face-recognition system \nor enter password&username to log in\nFace recognition will open automatically\nEnter 'q' to exit and enter the manual system",fg="#696969",font = ('Arial' , f))
    label_1.pack()
    Button(window, text="Open Camera Directly", command=window.destroy,font="verdana 10 bold italic").pack()
    Button(window, text="Change color", command=changecolor,font="verdana 10 bold italic").pack()
    Button(window, text="Change font size", command=changefontsize,font="verdana 10 bold italic").pack()
    window.after(10000, window.destroy)
    window.mainloop()







