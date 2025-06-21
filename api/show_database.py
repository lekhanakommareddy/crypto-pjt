import sqlite3
import os

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
        # Decode private key if it's bytes
        if isinstance(row[2], bytes):
            try:
                priv_key = row[2].decode('utf-8')
            except Exception:
                priv_key = str(row[2])
        else:
            priv_key = str(row[2])
        print(f"{row[0]} | {row[1]} | {priv_key[:40]}...")  # Only show first 40 chars for clarity
    cursor.close()
    conn.close()

if __name__ == "__main__":
    show_database()
