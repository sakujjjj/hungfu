import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="hungfu"
)

mycursor = mydb.cursor()
print(mycursor)
sql_code = "select name from member "
mycursor.execute(sql_code)
print(mycursor)
# print(mycursor.fetchall())
print(mycursor.fetchone())
# for x in mycursor:
#     print(x)
