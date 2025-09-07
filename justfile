# https://just.systems

default:
    uv run flask run

edit:
    uv run nvim

db-migrate:
    ./scripts/migrate.py

db-wipe:
    rm -rf dev.db && just db-migrate
