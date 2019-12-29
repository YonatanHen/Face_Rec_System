#This page open the possibilty to enter the system with password&userName
import sqlite3
import datetime
import pygame
from gtts import gTTS
import os
from playsound import playsound
from getpass import getpass


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

"""
def adminMenu():
    """"""function open the admin's menu option""""""
    exit=False
    print("Please choose one of the option below:")
    while(exit==False):
        print("1.Change user data\n2.Change the volume of the system\n3.Delete user\s\n4.watch users data\n5.Exit menu")
        option=input("Enter an option:")
        if(option=='1'):
            uname=input("Enter the username")
            cursor.execute("SELECT * FROM users WHERE username=?",[(uname)])
            cursor.execute("UPDATE users SET entrance=?,isInside='yes' WHERE username=?")
        elif(option=='2'):
        elif(option=='3'):
        elif(option=='4'):
        elif(option=='5'):
            exit=True
            print("Exiting admin's menu...")
        else:
            print("Wrong input,Enter again.")
"""



#Users databse columns order:
#0.first_name,1.last_name,2.username,3.password,4.entrance,5.total,6.role,7.isInside
print("======================================================")
countTries=0
usersDB=sqlite3.connect('users.db')
cursor=usersDB.cursor() #cursor enable traversal over the records in database
while True:
    username=input("Enter user-name:")
    password=getpass("Enter password:")
    
    results=recognize(username,password)
    if results: #if results!=NULL, in other words, if user found in the DB
        for i in results:
            print("Time is:{0}".format(datetime.datetime.now()))
            if(i[7] =='no'):
                print("Welcome "+i[0]+" "+i[1])
                #Admin's menu
                """if(i[6]=='Admin'):
                    option=input("Hey admin! Do you want to reach the menu? y/n")
                    if(option=='y' or option=='Y'):
                        adminMenu()
                    elif(option=='n' or option=='N'):
                        print("OK,Have a nice day!")
                    else:
                        print("I see that as 'no',Have a nice day!")"""
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
        

