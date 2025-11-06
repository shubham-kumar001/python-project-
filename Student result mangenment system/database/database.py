import connect_db
from config.config import DB_PATH

def connect_db():
    return sqlite3.connect(DB_PATH)

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Students table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                      )''')
    
    # Results table
    cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        subject TEXT,
                        mark INTEGER,
                        FOREIGN KEY(student_id) REFERENCES students(id)
                      )''')
    
    conn.commit()
    conn.close()

# Initialize DB tables
create_tables()
