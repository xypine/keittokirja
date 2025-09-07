#!/usr/bin/env python3

import sqlite3
import hashlib
import os
from glob import glob

DATABASE_URL = os.environ["DATABASE_URL"]

# Connect to database
conn = sqlite3.connect(DATABASE_URL)
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS migration (
        filename TEXT PRIMARY KEY,
        sha_hash TEXT NOT NULL,
        applied_at DATETIME NOT NULL
    )
"""
)
conn.commit()

# Get all migration files sorted
migration_files = sorted(glob("./migrations/*.sql"))

for sql_file in migration_files:
    filename = os.path.basename(sql_file)

    # Read file and calculate SHA hash
    with open(sql_file, "rb") as f:
        content = f.read()
        sha_hash = hashlib.sha256(content).hexdigest()

    # Check if migration has been run
    cur.execute(
        "SELECT sha_hash, applied_at FROM migration WHERE filename = ?", (filename,)
    )
    result = cur.fetchone()

    if result:
        # Migration exists - verify hash
        if result[0] != sha_hash:
            conn.close()
            raise Exception(
                f"ERROR: Migration {filename} has been modified! "
                f"Expected hash: {result[0]}, Current hash: {sha_hash}"
            )
        print(f"Skipping {filename:<24} already applied at {result[1]}")
    else:
        # Run migration
        print(f"Running {filename}")
        cur.executescript(content.decode("utf-8"))

        # Record migration
        cur.execute(
            "INSERT INTO migration (filename, sha_hash, applied_at) VALUES (?, ?, CURRENT_TIMESTAMP)",
            (filename, sha_hash),
        )
        conn.commit()
        print(f"Applied {filename}")

conn.close()
