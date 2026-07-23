import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="waqas@050675",
    database="ai_support"
)

if connection.is_connected():
    print("Connected to MySQL successfully!")

connection.close()