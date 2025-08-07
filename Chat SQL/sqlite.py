import sqlite3

## Connect to SQLite database
connection = sqlite3.connect('student.db')

## Create a cursor object using the connection
cursor = connection.cursor()

## create a table
table_info = """
create table STUDENT (NAME VARCHAR(25), CLASS VARCHAR(25),
SECTION VARCHAR(25), MARKS INT)
"""
cursor.execute(table_info)

## Insert data into the table
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Alice', 'Data Science', 'A', 85)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Bob', 'Data Science', 'B', 90)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Charlie', 'Data Science', 'A', 78)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('David', 'DEVOPS', 'B', 88)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Eve', 'DEVOPS', 'A', 92)")

## Display the all the records in the table
print("All records in the STUDENT table:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

## Commit the changes
connection.commit()

## Close the connection
connection.close()