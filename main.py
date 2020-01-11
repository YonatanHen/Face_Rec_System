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
        from Functions import color_changer
        if(str(controller)=="<class '__main__.User_login'>"):
            changecolor_User_login(self.frames[controller])
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
    
        self.username_but1 = Button(self,text = "Log in/out with username",bg="white",fg="red",command=lambda:controller.show_frame(User_login),font="verdana 8 bold italic")
        self.face_but2 = Button(self,text = "Log in/out with face recognition",bg="white",fg="green",command=lambda:faces.faces(),font="verdana 8 bold italic")

        self.color_but3 = Button(self, text="Change color",command=lambda:changecolor_StartPage(self),bg="white",fg="orange",font="verdana 8 bold italic")   #להפעיל שינוי צבעים 

        self.vol_up_but4 = Button(self,text = " Set volume up ",bg="white",fg="blue",command=lambda:change_vol_up(),font="verdana 8 bold italic")
        self.vol_down_but5 = Button(self,text = "Set volume down",bg="white",fg="blue",command=lambda:change_vol_down(self),font="verdana 8 bold italic")
        self.mute_but6 = Button(self,text = "Mute",bg="white",fg="blue",command=lambda:turn_DU_music(self),font="verdana 8 bold italic")
        self.quit_but7 = Button(self,text = "Quit",bg="white",fg="purple",command=quit,font="verdana 8 bold italic")
        

        
        self.theLabel = Label(self,text="Welcome !",font="verdana 8 bold italic")
        self.theLabel.pack(fill=X)
        self.username_but1.pack(fill=X)
        self.face_but2.pack(fill=X)
        self.color_but3.pack(fill=X)
        self.space_label1 = Label(self,text="")
        self.space_label1.pack(fill=X)
        self.vol_up_but4.pack(fill=X)
        self.vol_down_but5.pack(fill=X)
        self.mute_but6.pack(fill=X)
        self.space_label2 = Label(self,text="")
        self.space_label2.pack(fill=X)
        self.quit_but7.pack(fill=X)
        
        
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
    global color_changer,color1,color2,is_color_changed,countTries
    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent)
        self.lable_1 = Label(self,text="User Name:",font="verdana 8 bold italic")
        self.lable_2 = Label(self,text="Password:",font="verdana 8 bold italic")
        
        username=StringVar()
        password=StringVar()

        self.lable_1.grid(row=0,sticky=E)
        self.lable_2.grid(row=1)
        
        self.entry_1=Entry(self,textvariable=username).grid(row=0,column=1)
        self.entry_2=Entry(self,textvariable=password).grid(row=1,column=1)
        self.back_but1 = Button(self,text = "Go back",bg=color1[9],fg=color2[9],command=lambda:controller.show_frame(StartPage),font="verdana 8 bold italic")
        self.enter_but2 = Button(self,text = "Enter",bg=color1[9],fg=color2[9],command=lambda:log(controller,username.get(),password.get()),font="verdana 8 bold italic")
        self.quit_but3 = Button(self,text = "Quit",bg=color1[9],fg=color2[9],command=quit,font="verdana 8 bold italic")
        

        username.set("")
        password.set("")
        
        self.back_but1.grid(row=3,columnspan=1)
        self.enter_but2.grid(row=3,columnspan=2)
        self.quit_but3.grid(row=4,columnspan=1)

    
 
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
