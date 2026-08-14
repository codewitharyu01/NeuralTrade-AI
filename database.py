import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
def init_db():

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        fullname TEXT NOT NULL,

        email TEXT UNIQUE NOT NULL,

        password TEXT NOT NULL

    )

    """)

    conn.commit()
    conn.close()


def register_user(fullname,email,password):

    password = generate_password_hash(password)

    conn = sqlite3.connect("users.db")

    cursor = conn.cursor()

    try:

        cursor.execute(

            "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",

            (fullname,email,password)

        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()

def login_user(email, password):

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT fullname,email,password FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user[2], password):

        return {
            "fullname": user[0],
            "email": user[1]
        }

    return None