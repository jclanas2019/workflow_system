import sqlite3

def setup_database():
    conn = sqlite3.connect('monitoring.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS monitoring (
        id INTEGER PRIMARY KEY,
        dag_id TEXT,
        task_name TEXT,
        task_type TEXT,
        start_time TEXT,
        end_time TEXT,
        duration REAL
    )
    ''')
    conn.commit()
    conn.close()

setup_database()
