import sqlite3

DATABASE = 'mydatabase.db'
IMAGE_COUNT = 100  # Total number of available images

def populate_users():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    
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
    
    # Generate 20,000 users with cyclic image assignments
    num_users = 20000
    users = [
        (
            f'user_{i}',
            f'{(i % IMAGE_COUNT)}.jpg',
            f'{(i + 1) % IMAGE_COUNT}.jpg',
            f'{(i + 2) % IMAGE_COUNT}.jpg',
            f'{(i + 3) % IMAGE_COUNT}.jpg'
        ) 
        for i in range(num_users)
    ]

    cur.executemany('''
        INSERT INTO users (name, profilepic, image1, image2, image3)
        VALUES (?, ?, ?, ?, ?)
    ''', users)
    
    conn.commit()
    conn.close()
    print(f"Inserted {num_users} users with cyclic image assignments.")

if __name__ == '__main__':
    populate_users() # avg entry is ~ 46 bytes
