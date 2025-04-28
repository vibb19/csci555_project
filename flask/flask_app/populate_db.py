import sqlite3

DATABASE = 'mydatabase.db'

def populate_users():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
    # Create table if it doesn't exist
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            profilepic TEXT NOT NULL,
            image1 TEXT NOT NULL,
            image2 TEXT NOT NULL,
            image3 TEXT NOT NULL
        )
    ''')
    
    # Insert multiple users
    users = [(f'user_{i}',f'{i}.jpg', f'{i+1}.jpg', f'{i+2}.jpg', f'{i+3}.jpg') for i in range(100)]  # <- fix: wrap each name in a tuple

    cur.executemany('INSERT INTO users (name, profilepic, image1, image2, image3) VALUES (?, ?, ?, ?, ?)', users)
    
    conn.commit()
    conn.close()
    print("Inserted dummy users.")

if __name__ == '__main__':
    populate_users()
