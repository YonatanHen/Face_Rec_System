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


