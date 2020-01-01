from tkinter import *
import cv2
from tkinter import *
import keyboard
import os
import pygame
import sys
import datetime
import time



window=Tk()
label_1=Label(window,text="Welcome,Please use the face-recognition system \nor enter password&username to log in\nFace recognition will open automatically\nEnter 'q' to exit \nIf you regret and want to enter with face recognition,enter 1\nIf you want to enter with password&username enter 2\nStop music with 's' button",fg="#696969",font="verdana 20 bold italic")
#label_2=Label(window,text="or enter password&username to log in",fg="#696969",font="verdana 20 bold italic")
#label_3=Label(window,text="Face recognition will open automatically\nEnter 'q' to exit",fg="#696969",font="verdana 20 bold italic")
#label_4=Label(window,text="If you regret and want to enter with face recognition,enter 1.",fg="#696969",font="verdana 20 bold italic")
#label_5=Label(window,text="If you want to enter with password&username enter 2",fg="#696969",font="verdana 20 bold italic")
#label_6=Label(window,text="Stop music with 's' button",fg="#696969",font="verdana 20 bold italic")
label_1.pack()
#label_2.pack()
#label_3.pack()
#label_4.pack()
#label_5.pack()
#label_6.pack()
Button(window, text="Quit", command=window.destroy).pack()
window.after(10000, window.destroy) 
window.mainloop()









