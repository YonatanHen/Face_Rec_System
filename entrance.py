#This page open the possibilty to enter the system with password&userName
import sqlite3
import datetime
import pygame
from gtts import gTTS
import os
from playsound import playsound

usersDB=sqlite3.connect('users.db')
cursor=usersDB.cursor() #cursor enable traversal over the records in database
while True:
    username=input("Enter user-name:")
    password=input("Enter password:")
    cursor=usersDB.cursor() #cursor enable traversal over the records in database
    cursor.execute("SELECT * FROM users WHERE username=? and password=?",[(username),(password)])
    results=cursor.fetchall()
    if results:
        for i in results:
            print("Welcome "+i[0]+" "+i[1])
            playsound('welcome.mp3',False)
            enter_time=datetime.datetime.now().hour
            print(enter_time)
            if(i[7] =='no'):
                cursor.execute("UPDATE users SET entrance=?,isInside='yes' WHERE username=?",[(enter_time),(username)])
                usersDB.commit()
            elif(i[7]=='yes'):
                now=datetime.datetime.now().hour
                total=now-enter_time
                total=int(i[5])+total
                cursor.execute("UPDATE users SET total=?,isInside='no',entrance=0 WHERE username=?",[(total),(username)])
                usersDB.commit()
        break
    else:
        print("user-name and password not recognized,please enter again")


