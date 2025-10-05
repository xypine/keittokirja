import os
import sqlite3
from flask import g

database_url = os.environ["DATABASE_URL"]


def connect():
    return sqlite3.connect(database_url)


def get_db():
    if "db" not in g:
        g.db = connect()

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
