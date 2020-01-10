import cv2
from tkinter import *
from tkinter import ttk
import tkinter as tk
import keyboard
import sys
import datetime
import faces
from playsound import playsound
from Functions import *
from entrance import *


class ManageAppFrames(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.title('Hours registration system')
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
        frame = self.frames[controller]
        frame.tkraise() #make front

    

class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        
        bottomFrame = tk.Frame(self)
        bottomFrame.pack(side=BOTTOM)
    
        username_but1 = Button(self,text = "Log in/out with username",bg="white",fg="red",command=lambda:controller.show_frame(User_login),font="verdana 8 bold italic")
        face_but2 = Button(self,text = "Log in/out with face recognition",bg="white",fg="green",command=lambda:faces.faces(),font="verdana 8 bold italic")
        color_but3 = Button(self, text="Change color",bg="white",fg="orange",font="verdana 8 bold italic")   #להפעיל שינוי צבעים command=changecolor
        vol_up_but4 = Button(self,text = " Set volume up ",bg="white",fg="blue",command=lambda:change_vol_up(),font="verdana 8 bold italic")
        vol_down_but5 = Button(self,text = "Set volume down",bg="white",fg="blue",command=lambda:change_vol_down(),font="verdana 8 bold italic")
        mute_but6 = Button(self,text = "Mute",bg="white",fg="blue",command=turn_DU_music,font="verdana 8 bold italic")
        quit_but7 = Button(self,text = "Quit",bg="white",fg="purple",command=quit,font="verdana 8 bold italic")
        

        
        theLabel = Label(self,text="Welcome !",font="verdana 8 bold italic")
        theLabel.pack()
        username_but1.pack(fill=X)
        face_but2.pack(fill=X)
        color_but3.pack(fill=X)
        space_label1 = Label(self,text=" ")
        space_label1.pack()
        vol_up_but4.pack(fill=X)
        vol_down_but5.pack(fill=X)
        mute_but6.pack(fill=X)
        space_label2 = Label(self,text=" ")
        space_label2.pack()
        quit_but7.pack(fill=X)
        
        
        # מוסיף קוביה לכתיבה ומד
        #m1 = PanedWindow() 
        #m1.pack(fill = BOTH, expand = 1) 
        #left = Entry(m1, bd = 5) // write box 
        #m2 = PanedWindow(m1, orient = VERTICAL) 
        #m1.add(m2) 

        #top = Scale( m2, orient = HORIZONTAL) #meuzan
        #m2.add(top) 

        #w = Scale(m1, from_=0, to=42) #meunah
        #w.pack(side=LEFT) 

 
class User_login(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        lable_1 = Label(self,text="User Name:",font="verdana 8 bold italic")
        lable_2 = Label(self,text="Password:",font="verdana 8 bold italic")
        
        username=StringVar()
        password=StringVar()

        lable_1.grid(row=0,sticky=E)
        lable_2.grid(row=1)
        
        entry_1=Entry(self,textvariable=username).grid(row=0,column=1)
        entry_2=Entry(self,textvariable=password).grid(row=1,column=1)
        back_but1 = Button(self,text = "Go back",bg="white",fg="black",command=lambda:controller.show_frame(StartPage),font="verdana 8 bold italic")
        enter_but2 = Button(self,text = "Enter",bg="white",fg="black",command=lambda:log(controller,username.get(),password.get()),font="verdana 8 bold italic")
        quit_but3 = Button(self,text = "Quit",bg="white",fg="black",command=quit,font="verdana 8 bold italic")
        

        username.set("")
        password.set("")

        global countTries
        
        c=Checkbutton(self,text="Keep me logged in !",font="verdana 8 bold italic")
        back_but1.grid(row=3,columnspan=1)
        enter_but2.grid(row=3,columnspan=2)
        quit_but3.grid(row=4,columnspan=1)
        c.grid(columnspan=2)
 
def OpenMenu():
    app=ManageAppFrames()
    app.mainloop()


OpenMenu()


'''
#playing sound in background helping with accessability for visually impaired users.
pygame.mixer.init()
pygame.mixer.music.load('background_audio.mp3')
pygame.mixer.music.play(999)
#set volume of background music
pygame.mixer.music.set_volume(0.4)

if keyboard.is_pressed('s'):
    pygame.mixer.music.pause()

os.system('MainPageWindow.py')
print(datetime.datetime.now())
x = True

#opening face recognition system when running
pygame.mixer.music.pause()
faces.faces()

while x:
    if keyboard.is_pressed('1'):
        pygame.mixer.music.pause()
        faces.faces()
        x = False
    if keyboard.is_pressed('2'):
        pygame.mixer.music.pause()
        os.system('entrance.py')
        x = False
    if keyboard.is_pressed('s'):
        pygame.mixer.music.pause()
    if keyboard.is_pressed('q'):
        cap.release()
        cv2.destroyAllWindows()
        x=False'''
