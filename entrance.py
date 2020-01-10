#This page open the possibilty to enter the system with password&userName
import sqlite3
import datetime
import pygame
from gtts import gTTS
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter
from playsound import playsound
from getpass import getpass
from Functions import *
import faces

music_vol=1
music_flag=0
countTries=0 #counter entrance tries
def change_vol_down():
    global music_vol
    if(music_vol>0):
        music_vol-=0.25
        pygame.mixer.music.set_volume(music_vol)

def change_vol_up():
    global music_vol
    if(music_vol<1):
        music_vol+=0.25
        pygame.mixer.music.set_volume(music_vol)

def turn_DU_music():
    global music_flag,music_vol
    if(music_flag==0) & (music_vol!=0):
        pygame.mixer.music.set_volume(0)
        music_flag=1
    else:
        music_flag=0
        if(music_vol==0):
            music_vol=0.25
        pygame.mixer.music.set_volume(music_vol)


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


def log(controller,us,passw):
    global countTries
    print(countTries)
    if recognize(us,passw):
        entrance(us,passw)
        text_window("have a nice day !")
    elif(countTries!=5):
        text_window("user-name and password not recognized,please enter again")
        countTries+=1
        if(countTries%2!=0):
            controller.show_frame(User_login2)
        else:
            controller.show_frame(User_login)
    else:
        countTries=0
        text_window("You tried to enter 5 times unssuccessfully!")
        controller.show_frame(User_login)

def entrance(username,password):
    #Users databse columns order:
    #0.first_name,1.last_name,2.username,3.password,4.entrance,5.total,6.role,7.isInside
    #countTries=0
    print("======================================================")
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor() #cursor enable traversal over the records in database
    global countTries
    while True:
        '''
        username=input("Enter user-name:")
        password=getpass("Enter password:")
        '''
        results=recognize(username,password)
        if results: #if results!=NULL, in other words, if user found in the DB
            for i in results:
                print("Time is:{0}".format(datetime.datetime.now()))
                if(i[7] =='no'):
                    print("Welcome "+i[0]+" "+i[1])
                    if(i[6] != "blind worker"):
                        #print on the screen user details if user is not visually impaired
                        showDetails=input("Do you want to watch your data? y/n:")
                        if(showDetails=='y' or showDetails=='Y'):
                            printUserDetails(i[2])
                        elif(showDetails=='n' or showDetails=='N'):
                            print("OK,Have a nice day!")
                        else:
                            print("I see that as 'no',Have a nice day!")
                    #Admin's menu
                    if(i[6]=='Admin'):
                        option=input("Hey admin! Do you want to reach the menu? y/n")
                        if(option=='y' or option=='Y'):
                            adminMenu()
                        elif(option=='n' or option=='N'):
                            print("OK")
                        else:
                            print("I see that as 'no',Have a nice day!")
                    playsound('welcome.mp3',False)
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
        else:
            countTries+=1
            if(countTries==5):
                print("You tried to enter 5 times unssuccessfully!")
                os._exit(0)
            else:
                print("user-name and password not recognized,please enter again")
                OpenMenu()


class SeaofBTCapp(tk.Tk):
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

        for F in (StartPage,User_login,User_login2):
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
    
class User_login2(tk.Frame):
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
    app=SeaofBTCapp()
    app.mainloop()


OpenMenu()
