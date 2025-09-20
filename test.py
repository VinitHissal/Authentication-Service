import sqlite3

def vinitdatabase():
    conn = sqlite3.connect("testing.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employee (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()


def adduser(username, password):
    conn = sqlite3.connect("testing.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Employee (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()  


def authenticate(username, password):
    conn = sqlite3.connect("testing.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT password FROM Employee WHERE username = ?", (username,)
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return False  
    return row[0] == password 

def checkpw(password: str) -> bool:
    if password.isalnum():
        return False
    if password.islower():
        return False
    if password.isupper():
        return False
    if not (8 <= len(password) <= 16):
        return False
    if any(char.isspace() for char in password):
        return False
    if not any(char.isdigit() for char in password):
        return False
    return True
