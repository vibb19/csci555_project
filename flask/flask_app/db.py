import sqlite3

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
    
def create_db():
    conn = get_db_connection()
    with open('schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def insert_random_entries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Test1', 'Putting some random stuff in for now')
            )

    cursor.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Test2', 'Putting some more random stuff in for now')
            )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    insert_random_entries()