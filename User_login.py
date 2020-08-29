import tkinter as tk
from tkinter import *
import StartPage as sp
import os
from playsound import playsound
from Functions import entrance,recognize,text_window


#["bg"] color blinders - beckground colors array
color1=["#C7C7C7","#A8A8A8","#919191","#848484","#7C7C7C","#727272","#737373","#727272","#717171","white"]

#["fg"] color blinders - font colors array
color2=["#545454","#4B4B4B","#4A4A4A","#434343","#3C3C3C","#323232","#2C2C2C","#242424","#010101","black"] 
countTries=0 #counter entrance tries
class User_login(tk.Frame):
    ''' GUI user and password log in/out class '''
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.label_1 = Label(self,text="User Name:",font="verdana 15 bold italic")
        self.label_2 = Label(self,text="Password:",font="verdana 15 bold italic")
        
        self.username=StringVar()
        self.password=StringVar()

        self.label_1.grid(row=0,sticky=E)
        self.label_2.grid(row=1)
        
        self.entry_1=Entry(self,textvariable=self.username)
        self.entry_2=Entry(self,show="*",textvariable=self.password)
        self.back_but1 = Button(self,text = "Go back",bg=color1[9],fg=color2[9],command=lambda:controller.show_frame(sp),font="verdana 15 bold italic")
        self.enter_but2 = Button(self,text = "Enter",bg=color1[9],fg=color2[9],command=lambda:self.enterCommand(controller),font="verdana 15 bold italic")
        self.quit_but3 = Button(self,text = "Quit",bg=color1[9],fg=color2[9],command=lambda:self.quitCommand(controller),font="verdana 15 bold italic")

        self.username.set("")
        self.password.set("")

        self.entry_1.grid(row=0,column=1)
        self.entry_1.bind("<Leave>", self.User_Name_sound)
        self.entry_2.grid(row=1,column=1)
        self.entry_2.bind("<Leave>", self.Password_sound)
        self.back_but1.grid(row=4,columnspan=2)
        self.back_but1.bind("<Leave>", self.Go_back_sound)
        self.enter_but2.grid(row=3,columnspan=2)
        self.enter_but2.bind("<Leave>", self.enter_sound)
        self.quit_but3.grid(row=5,columnspan=2)
        self.quit_but3.bind("<Leave>", self.quit_sound)
        self.ER_label = Label(self,text="")
        self.ER_label.grid(row=7,column=2)

        self.object_arr=[self.label_1,self.label_2,self.back_but1,self.enter_but2,self.quit_but3,self.ER_label]

    # enter_sound function - when the mouse pass over Enter button say - "Enter"
    def enter_sound(self, event):
        playsound('event audio\\Enter.mp3',False)
    
    # quit_sound function - when the mouse pass over Quit button say - "Quit"
    def quit_sound(self, event):
        playsound('event audio\\Quit.mp3',False)
    
    # Go_back_sound function - when the mouse pass over Go back button say - "Go back"
    def Go_back_sound(self, event):
        playsound('event audio\\Go back.mp3',False)

    # User_Name_sound function - when the mouse pass over User Name box say - "User Name box"
    def User_Name_sound(self, event):
        playsound('event audio\\User Name.mp3',False)

    # Password_sound function - when the mouse pass over Password box say - "Password box"
    def Password_sound(self, event):
        playsound('event audio\\Password.mp3',False)

    # enterCommand function - check if the username and password that ansered is in the system and doing proper action
    def enterCommand(self,controller):
        global countTries
        if recognize(self.username.get(),self.password.get()):
            entrance(self.username.get(),self.password.get())
            countTries=0
            self.ER_label["text"]=""
            self.entry_1.delete(0, 'end')
            self.entry_2.delete(0, 'end')
            self.quitCommand(controller)
        elif(countTries!=4):
            self.pack_unrec_us()
            countTries+=1
        else:
            countTries=0
            text_window("You tried to enter 5 times unssuccessfully!")
            self.ER_label["text"]=""
            self.entry_1.delete(0, 'end')
            self.entry_2.delete(0, 'end')
            controller.show_frame(sp) 

    
    def pack_unrec_us(self):
        ''' show a message when username and password are'nt recognized'''
        font_size=16
        self.ER_label["text"]="user-name and password not recognized,please enter again"
        self.ER_label["font"]="verdana "+ str(font_size-1) +" bold italic"
        playsound('not_rec.mp3',False)

    def quitCommand(self,controller):
        ''' quit GUI window and reopen the system '''
        controller.destroy()
        os.system("main.py")