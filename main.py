import cv2
<<<<<<< HEAD
#from tkinter import *
=======
from tkinter import *
>>>>>>> 3fb30c904ad4dcda241248889ff324c3f880a933
import keyboard
import os
import pygame
import sys


#playing sound in background helping with accessability for visually impaired users
pygame.mixer.init()
pygame.mixer.music.load('background_audio.mp3')
pygame.mixer.music.play(999)

print("Welcome,Please use the face-recognition system or enter password&username to log in")
print("Face recognition will open automatically\nEnter 'q' to exit")
print("If you want to enter with password&username enter 2,if you regret and want to enter with face recognition,enter 1.")
x = True

#opening face recognition system when running

os.system('faces.py')

#os.system('C:\\Users\\יונתן\\Documents\\Python_Projects\\Face_Rec_System\\opencvtube\\src\\faces.py')

while x:
    if keyboard.is_pressed('1'):
        os.system('faces.py')
        x = False
    if keyboard.is_pressed('2'):
        os.system('entrance.py')
        x = False