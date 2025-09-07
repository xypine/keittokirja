import sqlite3
import os

database_url = os.environ["DATABASE_URL"]


def connect():
    return sqlite3.connect(database_url)
