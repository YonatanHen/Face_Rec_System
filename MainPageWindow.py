from tkinter import *
import cv2
from tkinter import *
import keyboard
import os
import pygame
import sys
import datetime
import time


# WelcomeWindow function - open an explanation window
def WelcomeWindow():  
    window=Tk()
    f=20
    window.title('Face_Rec_System')
    label_1=Label(window,text="Welcome,Please use the face-recognition system \nor enter password&username to log in\nFace recognition will open automatically\nEnter 'q' to exit and enter the manual system",fg="#696969",font = ('Arial' , f))
    label_1.pack()
    window.after(10000, window.destroy)
    window.mainloop()







