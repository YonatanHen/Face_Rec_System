import cv2
from tkinter import *
import keyboard
import os
import pygame
import sys
import datetime


#playing sound in background helping with accessability for visually impaired users
pygame.mixer.init()
pygame.mixer.music.load('background_audio.mp3')
pygame.mixer.music.play(999)
#set volume of background music
pygame.mixer.music.set_volume(0.4) 

if keyboard.is_pressed('s'):
    pygame.mixer.music.pause()
os.system('window.py')


print(datetime.datetime.now())
x = True

#Enter the system
print("Welcome,Please use the face-recognition system or enter password&username to log in")
print("Face recognition will open automatically\nEnter 'q' to exit")
print("If you want to enter with password&username enter 2,if you regret and want to enter with face recognition,enter 1.")
print("Stop music with 's' button")


#opening face recognition system when running
os.system('faces.py')

while x:
    if keyboard.is_pressed('1'):
        os.system('faces.py')
        x = False
    if keyboard.is_pressed('2'):
        os.system('entrance.py')
        x = False
    if keyboard.is_pressed('s'):
        pygame.mixer.music.pause()
    if keyboard.is_pressed('q'):
        cap.release()
        cv2.destroyAllWindows()
        x=False
