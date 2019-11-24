<<<<<<< HEAD
import cv2
from tkinter import *
import keyboard
import os

print("Welcome,Please use the face-recognition system or enter password&username to log in")
print("Enter 1 for face recognition or 2 to password&username")
x = True

while x:
    if keyboard.is_pressed('1'):
        os.system('C:\\Users\\your_location\\Documents\\Python_Projects\\opencvtube\\src\\faces.py')
        x = False
=======
import cv2
from tkinter import *
import keyboard
import os

print("Welcome,Please use the face-recognition system or enter password&username to log in")
print("Enter 1 for face recognition or 2 to password&username:")
x = True

while x:
    if keyboard.is_pressed('1'):
        os.system('C:\\Users\\יונתן\\Documents\\Python_Projects\\Face_recognition_system_project\\opencvtube\\src\\faces.py')
        x = False
    if keyboard.is_pressed('2'):
        os.system('C:\\Users\\יונתן\\Documents\\Python_Projects\\Face_recognition_system_project\\entrance.py')
        x = False
>>>>>>> create new folder
