import sqlite3

DATABASE = 'mydatabase.db'

def populate_users():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    # Create table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    
    # Insert multiple users
    users = [(f'user_{i}',) for i in range(100)]  # <- fix: wrap each name in a tuple

    cur.executemany('INSERT INTO users (name) VALUES (?)', users)
    
    conn.commit()
    conn.close()
    print("Inserted dummy users.")

if __name__ == '__main__':
    populate_users()
