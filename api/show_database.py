import sqlite3
import os

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
    db_path = os.path.abspath('../users.db')
    print(f"Using database at: {db_path}\n")
    conn = sqlite3.connect('../users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, private_key FROM users")
    rows = cursor.fetchall()
    print("ID | Username | Private Key")
    print("-" * 60)
    for row in rows:
        # If private_key is stored as bytes, convert to string for display
        if isinstance(row[2], bytes):
            try:
                priv_key = row[2].decode('utf-8')
            except:
                priv_key = row[2]  # fallback, may display as bytes
        else:
            priv_key = row[2]
        print(f"{row[0]} | {row[1]} | {priv_key}")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    init_db()
    show_database()
