#!/usr/bin/env bash

find ./migrations -name "*.sql" -type f | sort | while read -r sql_file; do
    echo "Running $sql_file"
    sqlite3 $DATABASE_URL < $sql_file
done
