import cv2
from tkinter import *
import keyboard
import os
import pygame

#playing sound in background helping with accessability for visually impaired users
pygame.mixer.init()
pygame.mixer.music.load('background_audio.mp3')
pygame.mixer.music.play(999)

print("Welcome,Please use the face-recognition system or enter password&username to log in")
print("Enter 1 for face recognition or 2 to password&username:")
x = True

while x:
    if keyboard.is_pressed('1'):
        os.system('C:\\Users\\יונתן\\Documents\\Python_Projects\\Face_Rec_System\\opencvtube\\src\\faces.py')
        x = False
    if keyboard.is_pressed('2'):
        os.system('C:\\Users\\יונתן\\Documents\\Python_Projects\\Face_Rec_System\\entrance.py')
        x = False
