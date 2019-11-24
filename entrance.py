#This page open the possibilty to enter the system with password&userName
import sqlite3

#print("connect")
db=sqlite3.connect('users.db')
cursor=db.cursor() #cursor enable traversal over the records in database
cursor.execute('select * from users')
for row in cursor:
    print(row)