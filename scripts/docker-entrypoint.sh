#!/usr/bin/env sh
set -e # exit on first error

SCRIPT_DIR="$(dirname "$0")"

echo "Running migrations..."
"$SCRIPT_DIR/migrate.py"

echo "Starting gunicorn..."
uv run gunicorn --bind 0.0.0.0:80 --workers 4 app:app
