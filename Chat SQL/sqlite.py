import sqlite3

## Connect to SQLite database
try:
    with sqlite3.connect('student.db') as connection:
        cursor = connection.cursor()

        ## Create a table if it doesn't exist
        table_info = """
        CREATE TABLE IF NOT EXISTS STUDENT (
            NAME VARCHAR(25),
            CLASS VARCHAR(25),
            SECTION VARCHAR(25),
            MARKS INT
        )
        """
        cursor.execute(table_info)

        ## Check if the table is empty before inserting data
        cursor.execute("SELECT COUNT(*) FROM STUDENT")
        if cursor.fetchone()[0] == 0:
            ## Insert data into the table
            cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Alice', 'Data Science', 'A', 85)")
            cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Bob', 'Data Science', 'B', 90)")
            cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Charlie', 'Data Science', 'A', 78)")
            cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('David', 'DEVOPS', 'B', 88)")
            cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Eve', 'DEVOPS', 'A', 92)")
            connection.commit()
            print("Initial data inserted into the STUDENT table.")
        else:
            print("STUDENT table already contains data. Skipping initial data insertion.")

        ## Display all records in the table
        print("\nAll records in the STUDENT table:")
        data = cursor.execute("SELECT * FROM STUDENT")
        for row in data:
            print(row)

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
