#This page open the possibilty to enter the system with password&userName
import sqlite3

usersDB=sqlite3.connect('users.db')
cursor=usersDB.cursor() #cursor enable traversal over the records in database
while True:
    username=input("Enter user-name:")
    password=input("Enter password:")
    cursor=usersDB.cursor() #cursor enable traversal over the records in database
    find_user=("SELECT * FROM users WHERE username=? and password=?")
    cursor.execute(find_user,[(username),(password)])
    results=cursor.fetchall()
    if results:
        for i in results:
            print("Welcome "+i[0]+" "+i[1])
        break
    else:
        print("user-name and password not recognized,please enter again")


