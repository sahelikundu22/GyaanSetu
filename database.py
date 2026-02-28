import sqlite3

DB_NAME = "gyaanset.db"

def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   points INTEGER DEFAULT 0)
                   """)
    
    connection.commit()
    connection.close()


def insert_user(name, email):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (name, email, points) VALUES (?, ?, ?)",
            (name, email, 0)
        )
        connection.commit()
        return True
    
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def get_user_by_email(email):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()

    connection.close()
    return user