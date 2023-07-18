# we can make mysql database connection via terminal or mysql workbench 
# down here we look at how to connect to a database (mysql) using python code

import mysql.connector

# to connect to databas
dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'your username here',
    passwd = 'your password here'
)

# define a cursor object (or an object) to interact with the database
cursorObject = dataBase.cursor()

# create database
cursorObject.execute("CREATE DATABASE thorappan")

print("DONE!")
