#This page open the possibilty to enter the system with password&userName
import sqlite3
import datetime

usersDB=sqlite3.connect('users.db')
cursor=usersDB.cursor() #cursor enable traversal over the records in database
while True:
    username=input("Enter user-name:")
    password=input("Enter password:")
    cursor=usersDB.cursor() #cursor enable traversal over the records in database
    cursor.execute("SELECT * FROM users WHERE username=? and password=?",[(username),(password)])
    results=cursor.fetchall()
    if results:
        for i in results:
            print("Welcome "+i[0]+" "+i[1])
            enter_time=datetime.datetime.now()
            print("Entrance time:{0}".format(enter_time))
            cursor.execute("UPDATE users SET entrance=? Where username=?",[(enter_time),(username)])
            usersDB.commit()
        break
    else:
        print("user-name and password not recognized,please enter again")


