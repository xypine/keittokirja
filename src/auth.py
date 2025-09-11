from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import Connection
from flask import session


def create_credentials(db: Connection, username: str, password: str):
    password_hash = generate_password_hash(password)

    try:
        db.execute(
            """
            INSERT INTO user (username, password_hash) VALUES (?, ?)
            """,
            [username, password_hash],
        )
        db.commit()
        return True
    except Exception as e:
        print("Error creating user:", e)
        pass

    return False


def check_credentials(db: Connection, username: str, password: str):
    try:
        [user_id, password_hash] = db.execute(
            """
            SELECT id, password_hash FROM user WHERE username = ?
            """,
            [username],
        ).fetchone()

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return True
    except Exception as e:
        print("Error logging in:", e)
        pass

    return False


def forget_session():
    del session["user_id"]
    del session["username"]
