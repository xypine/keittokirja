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

1. Build the docker image

```bash
docker build -t keittokirja .
```

2. Pick a secret key for session storage

```bash
# For example on linux
export SECRET_KEY="development-key"
```

3. Pick a location & name for the database

<sup>
See step 6 if you don't need a persistent database.
</sup>

```bash
# For example on linux
# The folder that will be mounted inside the container
export PERSIST_DIR="./persist"
# The name of the database file
export DATABASE_NAME="database.db"
```

4. Pick a username that will be able to register & log in without verification

```bash
# Normally a user can't log in after registering without manual verification of the user from the server admin
# TRUSTED_USER removes that restriction for a single user, in this case "matti_meikalainen"
export TRUSTED_USER="matti_meikalainen"
```

5. Run the application

```bash
# --rm removes the container after it stops
# -it enables interactive I/O, so ctrl+c works normally
# -p 8000:80 maps the port 80 inside the container to the port 8000 on your system
# -v is used to persist the database file in the current directory
# -e sets an environment variable
docker run \
    --rm \
    -it \
    -p 8000:80 \
    -v "./$PERSIST_DIR":"/persist" \
    -e SECRET_KEY="$SECRET_KEY" \
    -e DATABASE_URL="/persist/$DATABASE_NAME" \
    -e TRUSTED_USER="$TRUSTED_USER" \
    keittokirja

```

The server should start successfully, and be available on your browser in localhost:8000!

6. Running the application without a persistent database
   If you don't need a persistent database (quick testing, etc.) you can just remove some of the arguments:

```bash
docker run --rm -it -p 8000:80 -e SECRET_KEY="$SECRET_KEY" -e TRUSTED_USER="$TRUSTED_USER" keittokirja
```
