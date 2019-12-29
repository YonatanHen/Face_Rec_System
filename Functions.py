
#This page include all the functions that program py files need

import numpy as np
import cv2
import pickle
import camera
import datetime
from gtts import gTTS
import os 
from playsound import playsound
import sqlite3
from getpass import getpass
from time import sleep
import tkinter as tk
from tkinter import filedialog
import shutil 

def recognize(username,password):
    """function check if username and password match one of the users in users.db,and return the relevant data"""
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? and password=?",[(username),(password)])
    return cursor.fetchall()

def face_recognize(username):
    """function check if username match one of the users in users.db,and return the relevant data"""
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?",[(username)])
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
        minutes = time_string[i] + '0'

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


def adminMenu():
    exit=False
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    print("Please choose one of the option below:")
    while(exit==False):
        print("1.Change user data\n2.Change the volume of the system\n3.Delete user\s\n4.watch users data\n5.add new user\n6.Add new photo to an exist user\n7.Exit menu")
        option=input("Enter an option: ")
        if(option=='1'):
            uname=input("Enter the username:")
            cursor.execute("SELECT * FROM users WHERE username=?",[(uname)])
            flag=cursor.fetchall()
            if flag:
                field=input("Enter a field that you want to change:")
                newVal=input("Enter the new value of {} {}:".format(uname,field))
                cursor.execute("UPDATE users SET {}=? WHERE username=?".format(field),[(str(newVal)),(uname)])
                usersDB.commit()
            else:
                print("Username not found...")
        elif(option=='2'):
            print("Please enter numbers between 0 to 100")
            vol=input()
            vol=vol/100
            pygame.mixer.music.set_volume(vol)
        elif(option=='3'):
            usernameDel=input("Enter the username that you want to delete:")
            flag=cursor.execute("SELECT username FROM users WHERE username=?",[(usernameDel)])
            if(flag):
                cursor.execute("DELETE from users WHERE username=?",[(usernameDel)])
                usersDB.commit()
                shutil.rmtree("images//"+str(usernameDel), ignore_errors=True)
                print("User deleted successfully!\n")
            else:
                print("Username wasn't found in the database.")   
        elif(option=='4'):
            cursor.execute("select * from users")
            for row in cursor:
                print(row)
        elif(option=='5'):
            uname=input("Enter the username: ")
            flag=cursor.execute("SELECT * FROM users WHERE username=?",[(uname)])
            flag=cursor.fetchall()
            if flag:
                print("user name already exist...")
            else:
                fName=input("Enter first name: ")
                lName=input("Enter last name: ")
                password=input("Enter password: ")
                role=input("Enter role (admin or worker): ")
                total=entrance=0
                isInside='no'
                #add the entred data to the database
                cursor.execute("""INSERT INTO users (first_name, last_name, username, password, entrance, total, role, isInside)
                    VALUES (?,?,?,?,?,?,?,?)""",[(fName),(lName),(uname),(password),(entrance),(total),(role),(isInside)])
                usersDB.commit() 
                print("Data added succesfully")
                print("Now, take few pictures of the new worker... press p -take a picture/q -stop Capturing")
                
                key = cv2. waitKey(1)
                webcam = cv2.VideoCapture(0)
                
                sleep(2)
                path="images//"+str(uname)
                os.mkdir(path)
                i=0
                while True:
                    check, frame = webcam.read()
                    frame = cv2.flip(frame,1)
                    cv2.imshow('Capturing', frame)
                    if cv2.waitKey(20) & 0xFF == ord('p'):
                        i+=1
                        cv2.imwrite(filename="images\\" + str(uname) + "\\" + str(uname) + str(i) +".png", img=frame)
                        print("Image saved!")
                        
                    elif cv2.waitKey(20) & 0xFF == ord('q'):
                        webcam.release()
                        cv2.destroyAllWindows()
                        break

        elif (option=='6'):
            root = tk.Tk()
            root.withdraw()
            while(True):
                user_fol=input("Enter username to add a picture to: ")
                root.attributes("-topmost", True)
                if os.path.isdir("images\\" + user_fol):
                    add_photo=None
                    while add_photo!='1' and add_photo!='2' and add_photo!='3':
                        add_photo=input("For choose an exist photo press 1, to take a new photo press 2, to go back to menu press 3: ")
                    if add_photo=='1':
                        file_path = filedialog.askopenfilename()
                        newPath = shutil.copy(file_path, "images\\" + user_fol + "\\" )
                        print("\nNow the user have a new picture !\n")
                    elif add_photo=='2':
                        webcam = cv2.VideoCapture(0)
                        i=0
                        while  os.path.isfile("images\\" + user_fol + "\\" + user_fol + str(i) +".png"):
                            i+=1
                        i-=1
                        while True:
                            check, frame = webcam.read()
                            frame = cv2.flip(frame,1)
                            cv2.imshow('Capturing', frame)
                            if cv2.waitKey(20) & 0xFF == ord('p'):
                                i+=1
                                cv2.imwrite(filename="images\\" + user_fol + "\\" + user_fol + str(i) +".png", img=frame)
                                print("Image saved!")
                                
                            elif cv2.waitKey(20) & 0xFF == ord('q'):
                                webcam.release()
                                cv2.destroyAllWindows()
                                sleep(2)
                                print("\nNow the user have a new picture/s !\n")
                                break
                    else:
                        break            
                else:                    
                    try_again=None
                    while try_again!='y' and try_again!='n':
                        try_again=input(("There is no folder to username - {0}, do you want to try again? y/n: ".format(user_fol)))
                    if try_again=='n':
                        break
                    

        elif (option=='7'):
            exit=True
            print("Exiting admin's menu...")
            
        else:
            print("Wrong input,Enter again.")
        
        
