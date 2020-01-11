import numpy as np
import cv2
import pickle
from subprocess import call
import camera
import datetime
from gtts import gTTS
import os 
from playsound import playsound
import sqlite3
from getpass import getpass
from time import sleep
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import shutil


##########################################change user data###################################################
def changeUserData():
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    uname=input("Enter the username:")
    cursor.execute("SELECT * FROM users WHERE username=?",[(uname)])
    flag=cursor.fetchall()
    if flag:
        field=input("Enter a field that you want to change:")
        newVal=input("Enter the new value of {} {}:".format(uname,field))
        cursor.execute("UPDATE users SET {}=? WHERE username=?".format(field),[(str(newVal)),(uname)])
        usersDB.commit()
        print("Data changed successfully!")
    else:
        print("Username not found...")

#######################################Change the volume of the system##################################################
def changeVol():
    print("Please enter numbers between 0 to 100")
    vol=input()
    vol=vol/100
    pygame.mixer.music.set_volume(vol)

############################################Delete user#################################################################

def deleteUser():
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    usernameDel=input("Enter the username that you want to delete:")
    flag=cursor.execute("SELECT username FROM users WHERE username=?",[(usernameDel)])
    if(flag):
        cursor.execute("DELETE from users WHERE username=?",[(usernameDel)])
        usersDB.commit()
        shutil.rmtree("images//"+str(usernameDel), ignore_errors=True)
        print("User deleted successfully!\n")
    else:
        print("Username wasn't found in the database.")

###############################################Watch users Data############################################

def watchData():
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
    cursor.execute("select * from users")
    for row in cursor:
        print(row)

###########################################Add new User#####################################################

def add():
    usersDB=sqlite3.connect('users.db')
    cursor=usersDB.cursor()
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


###########################################Add [phoro to user#####################################################

def addPhoto():
    root = Tk()
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

##########################################################################################################3              




def AdminMenu():
    menu=Tk()
    menu.title("Admin menu")
    exit=False
    Label(menu,text="Choose one of the following options, operate them in CMD window:",font=('Ariel',12)).pack()
    Button(menu,text="Change user data",command=lambda:changeUserData()).pack()
    Button(menu,text="Change the volume of the system",command=lambda:changeVol()).pack()
    Button(menu,text="Delete user",command=lambda:deleteUser()).pack()
    Button(menu,text="Watch users data",command=lambda:watchData()).pack()
    Button(menu,text="Add new user",command=lambda:add()).pack()
    Button(menu,text="Add new photo to exist user",command=lambda:addPhoto()).pack()
    Button(menu,text="Quit",command=lambda:menu.destroy()).pack()
    menu.mainloop()

AdminMenu()