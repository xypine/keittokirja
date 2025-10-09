import os
import sqlite3
from flask import g

database_url = os.environ["DATABASE_URL"]


def connect():
    conn = sqlite3.connect(database_url)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if "db" not in g:
        g.db = connect()

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
