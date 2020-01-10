import cv2
from tkinter import *
import keyboard
import os
import pygame
import sys
import datetime
import faces

#playing sound in background helping with accessability for visually impaired users.
pygame.mixer.init()
pygame.mixer.music.load('background_audio.mp3')
pygame.mixer.music.play(999)
#set volume of background music
pygame.mixer.music.set_volume(0.4)

if keyboard.is_pressed('s'):
    pygame.mixer.music.pause()

os.system('MainPageWindow.py')
print(datetime.datetime.now())
x = True

#opening face recognition system when running
pygame.mixer.music.pause()
faces.faces()

while x:
    if keyboard.is_pressed('1'):
        pygame.mixer.music.pause()
        faces.faces()
        x = False
    if keyboard.is_pressed('2'):
        pygame.mixer.music.pause()
        os.system('entrance.py')
        x = False
    if keyboard.is_pressed('s'):
        pygame.mixer.music.pause()
    if keyboard.is_pressed('q'):
        cap.release()
        cv2.destroyAllWindows()
        x=False
