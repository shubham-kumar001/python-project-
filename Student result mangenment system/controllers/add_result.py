from database.database import connect_db
from utils.validation import validate_mark

def add_result(student_id, subject, mark):
    try:
        validate_mark(mark)
    except ValueError as e:
        print(e)
        return
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO results (student_id, subject, mark) VALUES (?, ?, ?)",
                   (student_id, subject, mark))
    conn.commit()
    conn.close()
    print(f"Result for student ID {student_id} added successfully!")
