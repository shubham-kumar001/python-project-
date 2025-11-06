from database.database import connect_db

def calculate_student_result(student_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT subject, mark FROM results WHERE student_id = ?", (student_id,))
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        print("No results found for this student.")
        return
    
    total = sum(mark for subject, mark in results)
    percentage = total / len(results)
    
    print(f"Student ID: {student_id}")
    print("Results:")
    for subject, mark in results:
        print(f"{subject}: {mark}")
    print(f"Total Marks: {total}")
    print(f"Percentage: {percentage:.2f}%")
