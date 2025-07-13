import sqlite3

def init_db():
    conn = sqlite3.connect('file_mgmt.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        path TEXT NOT NULL UNIQUE,
        is_folder INTEGER NOT NULL,
        parent_id INTEGER,
        FOREIGN KEY(parent_id) REFERENCES files(id)
    )
    ''')
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")

