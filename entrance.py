#This page open the possibilty to enter the system with password&userName
import sqlite3
import datetime
import pygame
from gtts import gTTS
import os
from playsound import playsound

#Users databse columns order:
#first_name,last_name,username,password,entrance,total,role,isInside

countTries=0
usersDB=sqlite3.connect('users.db')
cursor=usersDB.cursor() #cursor enable traversal over the records in database
while True:
    username=input("Enter user-name:")
    password=input("Enter password:")
    cursor=usersDB.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? and password=?",[(username),(password)])
    results=cursor.fetchall()
    if results:
        for i in results:
            #print(enter_time)
            if(i[7] =='no'):
                print("Welcome "+i[0]+" "+i[1])
                playsound('welcome.mp3',False)
                enter_time=datetime.datetime.now().hour
                cursor.execute("UPDATE users SET entrance=?,isInside='yes' WHERE username=?",[(enter_time),(username)])
                usersDB.commit()
            elif(i[7]=='yes'):
                print("goodbye "+i[0]+" "+i[1])
                total=datetime.datetime.now().hour-int(i[4])
                total=int(i[5])+total
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


