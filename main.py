import cv2
from tkinter import *
from tkinter import ttk
import tkinter as tk
import keyboard
import sys
import datetime
from playsound import playsound
from Functions import *
from MainPageWindow import WelcomeWindow

'''
====================================================================================================
            ManageAppFrames class - make a main window for all the other GUI classes -
                                    to open at the same window
====================================================================================================
'''
class ManageAppFrames(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.title('Hours registration system')
        self.geometry("1000x850")
        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)
        #playing sound in background helping with accessability for visually impaired users.
        pygame.mixer.init()
        pygame.mixer.music.load('background_audio.mp3')
        pygame.mixer.music.play(999)
        #set volume of background music
        global music_vol
        pygame.mixer.music.set_volume(music_vol)

        self.frames={}

        for F in (StartPage,User_login):
            frame=F(container,self)
            self.frames[F] = frame
            frame.grid(row = 0,column = 0,sticky = "nsew")
        self.show_frame(StartPage)

    # show_frame - make the asked window to open
    def show_frame(self,controller):
        from Functions import color_changer
        if(str(controller)=="<class 'Functions.User_login'>"):
            changecolor(self.frames[controller])
            Change_font_size(self.frames[controller])
        if(color_changer!=0):
            self.frames[controller]["bg"]=color1[color_changer-1]
        else:
            self.frames[controller]["bg"]=color1[9]
        frame = self.frames[controller]
        frame.tkraise() #make front
####################################################################################################
# OpenMenu - make an ManageAppFrames object and play it
def OpenMenu():
    app=ManageAppFrames()
    app.mainloop()
####################################################################################################
# play all the system (main)
WelcomeWindow()
faces()
OpenMenu()
####################################################################################################q