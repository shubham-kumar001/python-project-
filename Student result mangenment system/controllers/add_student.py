import sqlite3
from database.database import connect_db
from utils.validation import validate_name

def add_student(name):
    try:
        validate_name(name)
    except ValueError as e:
        print(e)
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO students (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()
    print(f"Student {name} added successfully!")
