# Keittokirja

## Functionality

- Users can browse other users' recipes
- Users can search for recipes based on their names
- Users can search for recipes based on the required ingredients
- Users can view all recipes added by a specific user
- Users can register & login
- Users can add their own recipes
- Users can specify which ingredients a recipe requires
- Users can add ingredients into the system
- Users can add aliases for existing ingredients
- Users can specify which ingredients they have in stock
- Users can search for recipes they can make with their currently stocked ingredients

## Set-up

1. Pick a secret key for session storage, and a trusted (admin) username

```bash
# For example on linux
export SECRET_KEY="development-key"
# Normally a user can't log in after registering without manual verification of the user from the server admin
# TRUSTED_USER removes that restriction for a single user, in this case "matti_meikalainen"
export TRUSTED_USER="matti_meikalainen"
```

2. Pick a location & name for the database

```bash
# For example on linux, without docker
export DATABASE_URL="./database.db"


# For example WITH DOCKER
# The directory that will be mounted inside the container
export PERSIST_DIR="./persist"
# The name of the database file inside that directory
export DATABASE_NAME="database.db"

```

<sup>
See step 5 if you don't need to persist data (docker only)
</sup>

3. Install dependencies locally or build the docker image

```bash
# For example on linux, if you have uv installed (recommended)
uv sync # probably not even needed!

# For example on linux, if you don't have uv installed
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# For example with docker
docker build -t keittokirja .
```

4. Run the application

```bash
# For example on linux
# 1. Create and migrate database
./scripts/migrate.py
# 2. Run the server
# With UV
uv run flask run
# Without UV
flask run

# For example with docker
# --rm removes the container after it stops
# -it enables interactive I/O, so ctrl+c works normally
# -p 5000:80 maps the port 80 inside the container to the port 5000 on your system
# -v is used to persist the database file in the current directory
# -e sets an environment variable
docker run \
    --rm \
    -it \
    -p 5000:80 \
    -v "./$PERSIST_DIR":"/persist" \
    -e SECRET_KEY="$SECRET_KEY" \
    -e DATABASE_URL="/persist/$DATABASE_NAME" \
    -e TRUSTED_USER="$TRUSTED_USER" \
    keittokirja

```

The server should start successfully, and be available on your browser in localhost:5000!

5. Running the application without persistent data
   If you don't need to persist data (quick testing, etc.) you can just remove some of the arguments:

```bash
docker run --rm -it -p 8000:80 -e SECRET_KEY="$SECRET_KEY" -e TRUSTED_USER="$TRUSTED_USER" keittokirja
```
