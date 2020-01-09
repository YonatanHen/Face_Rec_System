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

def recognize(username,password):
    "function check if username and password match one of the users in users.db,and return the relevant data"
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? and password=?",[(username),(password)])
    return cursor.fetchall()

def Time_Fixer(time_string):
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
        minutes = time_string[i]

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
            countTries=countTries+1
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
    
        username_but1 = Button(self,text = "Login with username",bg="white",fg="red",command=lambda:controller.show_frame(User_login))
        vol_but2 = Button(self,text = "Turn down/up beep",bg="white",fg="blue")
        button3 = Button(self,text = "Login",bg="white",fg="green")
        quit_but4 = Button(self,text = "Quit",bg="white",fg="purple",command=quit)
        
        theLabel = Label(self,text="Yarin avraham !")
        theLabel.pack()
        username_but1.pack(fill=X)
        vol_but2.pack(fill=X)
        #button3.pack(side=LEFT)
        quit_but4.pack(fill=X)
        
        # מוסיף קוביה לכתיבה ומד
        m1 = PanedWindow() 
        m1.pack(fill = BOTH, expand = 1) 
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
        lable_1 = Label(self,text="User Name:")
        lable_2 = Label(self,text="Password:")
        
        username=StringVar()
        password=StringVar()

        lable_1.grid(row=0,sticky=E)
        lable_2.grid(row=1)
        entry_1=Entry(self,textvariable=username).grid(row=0,column=1)
        entry_2=Entry(self,textvariable=password).grid(row=1,column=1)
        back_but1 = Button(self,text = "Go back",bg="white",fg="black",command=lambda:controller.show_frame(StartPage))
        enter_but2 = Button(self,text = "Enter",bg="white",fg="black",command=lambda:entrance(username.get(),password.get()))
        quit_but3 = Button(self,text = "Quit",bg="white",fg="black",command=quit)

        c=Checkbutton(self,text="Keep me logged in !")
        back_but1.grid(row=3,columnspan=1)
        enter_but2.grid(row=3,columnspan=2)
        quit_but3.grid(row=4,columnspan=1)
        c.grid(columnspan=2)
          
def OpenMenu():
    app=SeaofBTCapp()
    app.mainloop()

#counter entrance tries
countTries=0
OpenMenu()
