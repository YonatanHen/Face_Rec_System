import cv2
from tkinter import *
from tkinter import ttk
import tkinter as tk
import keyboard
import sys
import datetime
from faces import faces
from playsound import playsound
from Functions import *
from entrance import *

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


    def show_frame(self,controller):
        from Functions import color_changer
        if(str(controller)=="<class '__main__.User_login'>"):
            changecolor_User_login(self.frames[controller])
            Change_font_size(self.frames[controller])
        if(color_changer!=0):
            self.frames[controller]["bg"]=color1[color_changer-1]
        else:
            self.frames[controller]["bg"]=color1[9]
        frame = self.frames[controller]
        frame.tkraise() #make front

    

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=BOTTOM)
    
        self.username_but1 = Button(self,text = "Log in/out with username",bg="white",fg="red",command=lambda:controller.show_frame(User_login),font="verdana 15 bold italic")
        self.face_but2 = Button(self,text = "Log in/out with face recognition",bg="white",fg="green",command=lambda:faces.faces(),font="verdana 15 bold italic")

        self.color_but3 = Button(self, text="Change color",command=lambda:changecolor_StartPage(self),bg="white",fg="orange",font="verdana 15 bold italic")   #להפעיל שינוי צבעים 

        self.font_size8 = Button(self,text = "Set font size",bg="white",fg="gold",command=lambda:Change_font_size(self),font="verdana 15 bold italic")

        self.vol_up_but4 = Button(self,text = " Set volume up ",bg="white",fg="blue",command=lambda:change_vol_up(self),font="verdana 15 bold italic")
        self.vol_down_but5 = Button(self,text = "Set volume down",bg="white",fg="blue",command=lambda:change_vol_down(self),font="verdana 15 bold italic")
        self.mute_but6 = Button(self,text = "Mute",bg="white",fg="blue",command=lambda:turn_DU_music(self),font="verdana 15 bold italic")
        self.quit_but7 = Button(self,text = "Quit",bg="white",fg="purple",command=quit,font="verdana 15 bold italic")
        

        
        self.theLabel = Label(self,text="Welcome !",font="verdana 15 bold italic")
        self.theLabel.pack(fill=X)
        self.username_but1.pack(fill=X)
        self.face_but2.pack(fill=X)
        self.color_but3.pack(fill=X)
        self.font_size8.pack(fill=X)
        self.space_label1 = Label(self,text="")
        self.space_label1.pack(fill=X)
        self.vol_up_but4.pack(fill=X)
        self.vol_down_but5.pack(fill=X)
        self.mute_but6.pack(fill=X)
        self.space_label2 = Label(self,text="")
        self.space_label2.pack(fill=X)
        self.quit_but7.pack(fill=X)



def OpenMenu():
    app=ManageAppFrames()
    app.mainloop()


faces.faces()
OpenMenu()
