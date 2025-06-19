import sqlite3

def init_db():
    conn = sqlite3.connect('../users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password BLOB,
            private_key BLOB
        )
    ''')
    conn.commit()
    conn.close()

def show_database():
    conn = sqlite3.connect('../users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print("Users:")
    for row in rows:
        print(row)
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    show_database()
