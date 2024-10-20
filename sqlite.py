import sqlite3

# connect to sqlite
connection = sqlite3.connect("student.db")

# create a cursor object to insert record,create table
cursor = connection.cursor()

#create the table
table_info="""
create table STUDENT(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25), MARKS INT)
"""

cursor.execute(table_info)

#insert some more records
cursor.execute("""Insert Into STUDENT values("alabama","AI Agent","A", 70)""")
cursor.execute("""Insert Into STUDENT values("anvesh","Data","c", 90)""")
cursor.execute("""Insert Into STUDENT values("zombi","Analytics","B", 70)""")
cursor.execute("""Insert Into STUDENT values("pochanki","AI","A", 70)""")
cursor.execute("""Insert Into STUDENT values("moneky","NLP","B", 70)""")

#Display all the records
print("The inserted records")
data = cursor.execute("""Select * from STUDENT""")
for row in data:
    print(row)

# commit your changes in database 
connection.commit()
connection.close()   