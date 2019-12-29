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
        print("1.Change user data\n2.Change the volume of the system\n3.Delete user\s\n4.watch users data\n5.add new user\n6.Exit menu")
        option=input("Enter an option:")
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
                print("User deleted successfully!")
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
                print("Now, take few pictures of the new worker...")
                from time import sleep
                key = cv2. waitKey(1)
                webcam = cv2.VideoCapture(0)
                sleep(2)
                path="images//"+str(uname)
                os.mkdir(path)
                while True:
                    check, frame = webcam.read()
                    cv2.imshow("Capturing", frame)
                    i=0
                    if cv2.waitKey(20) & 0xFF == ord('p'):
                        cv2.imwrite(filename='saved_img.jpg', img=frame)
                        webcam.release()
                        print("Processing image...")
                        img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
                        print("Converting RGB image to grayscale...")
                        gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                        print("Converted RGB image to grayscale...")
                        print("Resizing image to 100X100 scale...")
                        img_ = cv2.resize(gray,(100,100))
                        print("Resized...")
                        cv2.imwrite(filename="images\\" + str(uname) + "\\" + str(uname) + str(i) +".png", img=img_)
                        print("Image saved!")
                    elif cv2.waitKey(20) & 0xFF == ord('q'):
                        webcam.release()
                        cv2.destroyAllWindows()
                        break
        elif (option=='6'):
            exit=True
            print("Exiting admin's menu...")
        else:
            print("Wrong input,Enter again.")

