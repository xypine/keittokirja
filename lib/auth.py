from werkzeug.security import generate_password_hash, check_password_hash
from sqlite3 import Connection
from flask import session
from os import environ

PRE_TRUSTED_USER = environ.get("TRUSTED_USER")


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


CREDENTIAL_CHECK_OK = 0
CREDENTIAL_CHECK_WRONG_DETAILS = 1
CREDENTIAL_CHECK_ERROR = 2
CREDENTIAL_CHECK_UNVERIFIED = 3


def check_credentials(db: Connection, username: str, password: str):
    try:
        [user_id, password_hash, verified] = db.execute(
            """
            SELECT id, password_hash, verified FROM user WHERE username = ?
            """,
            [username],
        ).fetchone()

        if check_password_hash(password_hash, password):
            if not verified and username != PRE_TRUSTED_USER:
                return CREDENTIAL_CHECK_UNVERIFIED

            session["user_id"] = user_id
            session["username"] = username
            return CREDENTIAL_CHECK_OK
    except Exception as e:
        print("Error logging in:", e)
        return CREDENTIAL_CHECK_ERROR

    return CREDENTIAL_CHECK_WRONG_DETAILS


def forget_session():
    del session["user_id"]
    del session["username"]
