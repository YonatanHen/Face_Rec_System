import pickle
import camera
import datetime
import time
from gtts import gTTS
import os 
from playsound import playsound
import sqlite3
import pygame
from Functions import *
from tkinter import *
from adminMenu import AdminMenu

def showDetails(x,username):
    if (x):
        usersDB=sqlite3.connect('users.db')
        cursor=usersDB.cursor()
        result=cursor.execute("SELECT * FROM users WHERE username=?",[(username)])
        days=0
        for row in result:
            root=Tk()
            root.title("Show {} details".format(row[2]))
            label0=Label(root,text="total hours: {}".format(row[5])).grid(row=0)
            if(float(row[5])%24!=0):
                days+=1
            if (float(row[5])>=24):
                days=float(row[5])//24
            label1=Label(root,text="total days: {}".format(days)).grid(row=1)
            label2=Label(root,text="Enter your hourly wage: ").grid(row=2,column=0)
            salary=DoubleVar(root,0.0)
            entry1=Entry(root,textvariable=salary).grid(row=2,column=1)
            btn=Button(root,text="Submit",command=lambda:Label(root,text="Total gross profits are {0}".format(salary.get()*float(row[5]))).grid(row=3) if\
            salary.get()>=0 else
            messagebox.showerror("Error","Salary must be postivie number!")).grid(row=2,column=2)
        root.mainloop()
    else:
       print("OK! Have a nice Day!")

 
def faces():
    #playing sound in background helping with accessability for visually impaired users.
    pygame.mixer.init()
    pygame.mixer.music.load('background_audio.mp3')
    pygame.mixer.music.play(999)
    #set volume of background music
    pygame.mixer.music.set_volume(0.4)
    if os.path.isfile("match.mp3"):
        os.remove("match.mp3")
    face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt.xml')
    eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_smile.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("./recognizers/face-trainner.yml")
    labels = {"person_name": 1}
    with open("pickles/face-labels.pickle", 'rb') as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}
    cap = cv2.VideoCapture(0)
    #make 4k
    cap.set(3, 3840)
    cap.set(4, 2160)
    i=0
    isRecCounter = 0
    counter2 = 0
    lrcounter = 8
    name = "None"
    tempname = "None"
    color = (0,0,255)
    beepflag = 1
    tempmatch = "analyzing..."
    trysCounter=0
    #beepuls = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    stroke = 2 #font thickness
    playsound('Take_Down.mp3',False)
    while(True):
        '''
        if cv2.waitKey(20) & 0xFF == ord('v'):
            if beepflag == 0:
                beepflag = 1
            if beepflag == 1:
                beepflag = 0
        if beepflag == 1:
            beepuls += 1
            if beepuls % 25 == 0:
                playsound('beep.mp3',False)
                '''
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv2.flip(frame,1)
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=12, minNeighbors=5)
        for (x, y, w, h) in faces:
            #print(x,yq,w,h)
            roi_gray = gray[y:y+h, x:x+w] #(ycord_start, ycord_end)
            roi_color = frame[y:y+h, x:x+w]
            # recognize? deep learned model predict keras tensorflow pytorch scikit learn
            id_, conf = recognizer.predict(roi_gray)
            if conf>=54.5 and conf <= 60:
                #print(conf)
                #print(5:id_)
                #print(labels[id_], name, isRecCounter,counter2)
                if labels[id_] == name or name == "None":
                    isRecCounter=isRecCounter+1
                    counter2 = 0
                    if isRecCounter == 5:
                        tempname = name
                if tempname != name:
                    counter2 += 1
                #if counter2 % 8==0:
                #    isRecCounter = 0
                    
                name = labels[id_]
                #match sound
                if isRecCounter > 10:
                    match = "Match found: " + tempname
                    color = (0, 255, 0)
                    cv2.putText(frame, match, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                    tts = gTTS(text=match, lang = 'en')
                    tts.save("match.mp3")
                    if os.path.isfile("match.mp3"):
                        playsound("match.mp3",False)
                        cv2.imshow('frame',frame)
                        #delete camera window if match found.
                        cap.release()
                        cv2.destroyAllWindows()
                        sleep(2)
                        usersDB=sqlite3.connect('users.db')
                        cursor=usersDB.cursor() #cursor enable traversal over the records in database
                        results=face_recognize(tempname)
                        for i in results:
                            if(i[6] != "blind worker"):
                                #print("Time is:{0}".format(datetime.datetime.now()))
                                if(i[7] =='no'):
                                    welcome=Tk()
                                    welcome.title("Welcome "+i[0]+" "+i[1])
                                    time_label=Label(welcome,text="Date & Time:{0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                                    time_label.pack()
                                    playsound("welcome.mp3",False)
                                    watchDataVar=IntVar()
                                    watchDataVar.set(0)
                                    Checkbutton(welcome,text="Mark the box to watch your data", variable=watchDataVar).pack()
                                    Button(welcome,text="Submit",command=lambda:showDetails(watchDataVar.get(),str(i[2]))).pack()
                                    welcome.mainloop()
                                    #Admin's menu
                                    if(i[6]=='admin'):
                                        option=input("I see that you are an admin! Do you want to reach the menu? y/n:")
                                        if(option=='y' or option=='Y'):
                                            AdminMenu()
                                        elif(option=='n' or option=='N'):
                                            print("OK,Have a nice day!")
                                        else:
                                            print("I see that as 'no',Have a nice day!")
                                    enter_time=float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)
                                    cursor.execute("UPDATE users SET entrance=?,isInside='yes' WHERE username=?",[(enter_time),(tempname)])
                                    usersDB.commit()
                                elif(i[7]=='yes'):
                                    print("Goodbye "+i[0]+" "+i[1])
                                    total=str(float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)-(float(i[4])))
                                    total="%.2f" %(float(i[5])+float(total))
                                    total = Time_Fixer(total)
                                    cursor.execute("UPDATE users SET total=?,isInside='no',entrance=0 WHERE username=?",[(total),(tempname)])
                                    usersDB.commit()
                                    playsound("godbye.mp3",False)
                                break
                            else:
                                if(i[7] =='no'):
                                    print("Welcome "+i[0]+" "+i[1])
                                    playsound("welcome.mp3",False)
                                    enter_time=float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)
                                    cursor.execute("UPDATE users SET entrance=?,isInside='yes' WHERE username=?",[(enter_time),(tempname)])
                                    usersDB.commit()
                                else:
                                    print("Goodbye "+i[0]+" "+i[1])
                                    total=str(float(datetime.datetime.now().hour)+(datetime.datetime.now().minute*0.01)-(float(i[4])))
                                    total="%.2f" %(float(i[5])+float(total))
                                    total = Time_Fixer(total)
                                    cursor.execute("UPDATE users SET total=?,isInside='no',entrance=0 WHERE username=?",[(total),(tempname)])
                                    usersDB.commit()
                                    playsound("godbye.mp3",False) 
                        if os.path.isfile("match.mp3") :
                            os.remove("match.mp3")
                        tempmatch = match
                        pygame.mixer.music.pause()
                    os.system("entrance.py")
                elif isRecCounter > 5:
                    color = (0, 255, 0) #green
                    cv2.putText(frame, tempname, (x,y), font, 1, color, stroke, cv2.LINE_AA)
                    
                else:
                    color = (0, 0, 255) #red
                    cv2.putText(frame, "analyzing...", (x,y), font, 1, color, stroke, cv2.LINE_AA)
                                
            else:
                trysCounter+=1
                #counter2+=1
                if trysCounter==5:
                    cv2.putText(frame,"Failed attempt !", (x,y), font, 1, color, stroke, cv2.LINE_AA)
                    for _ in range(100):
                        cv2.imshow('frame',frame)
            stroke = 2
            end_cord_x = x + w
            end_cord_y = y + h
            cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
            # sound
            if x < 350:
                if lrcounter % 10 == 0:
                    playsound('moveright.mp3',False)
                lrcounter+=1
            
            elif x > 680:
                if lrcounter % 10 == 0:
                    playsound('moveleft.mp3',False)
                lrcounter+=1
            if cv2.waitKey(20) & 0xFF == ord('p'):
                i+=1
                if isRecCounter>10 and counter2 == 0:
                    img_item =  "images\\" + tempname + "\\" + tempname + str(i) +".png"
                else:
                    img_item =  "unknown\\unknown" + str(i) +".png" 
                cv2.imwrite(img_item, roi_color)
                now = (datetime.datetime.now()).strftime("%Y-%m-%d %H_%M_%S")
            subitems = smile_cascade.detectMultiScale(roi_gray)
            #for (ex,ey,ew,eh) in subitems:
            #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        # Display the resulting frame
        cv2.imshow('frame',frame)
        if trysCounter>100:
            color = (0, 0, 255)
            playsound("Five_failed_attempts.mp3")
            cv2.putText(frame, "Failed attempts !", (x,y), font, 1, color, stroke, cv2.LINE_AA)
            for _ in range(100):
                cv2.imshow('frame',frame)
                
            img_item =  "unknown\\unknown" + str(i) +".png"
            cv2.imwrite(img_item, roi_color)
            pygame.mixer.music.pause()
            cap.release()
            cv2.destroyAllWindows()
            time.sleep(1)
            os.system("main.py")
            break
        if cv2.waitKey(20) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break

