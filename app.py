from flask import Flask, render_template, request, redirect, session

from src.ingredients import Ingredient, NewIngredient
from src.db import connect
from src.auth import check_credentials, create_credentials, forget_session

app = Flask(__name__)
app.secret_key = "DEVDEVDEV"


@app.context_processor
def inject_nav_items():
    current_endpoint = request.endpoint or "unknown"

    nav_items = [
        {
            "url": "/ingredients",
            "label": "Ingredients",
            "endpoint": "ingredients",
            "active": current_endpoint.startswith("ingredients"),
        },
        {
            "url": "/recipes",
            "label": "Recipes",
            "endpoint": "recipes",
            "active": current_endpoint.startswith("recipes"),
        },
    ]

    return dict(nav_items=nav_items)


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/login")
def login_form():
    return render_template("auth/login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    result = check_credentials(connect(), username, password)
    if result:
        return redirect("/")
    return "Wrong username or password"


@app.route("/register")
def register_form():
    return render_template("auth/register.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "Passwords don't match."

    result = create_credentials(connect(), username, password1)
    if result:
        return "User created, you can now log in"

    return "Error creating user, maybe the username is already taken?"


@app.route("/logout")
def logout():
    forget_session()
    return redirect("/")


@app.route("/ingredients")
def ingredients():
    ingredients = Ingredient.get_all()
    return render_template("ingredients.html", ingredients=ingredients)


@app.route("/ingredients/new")
def new_ingredient():
    return render_template("ingredients_new.html")


@app.route("/ingredients/new", methods=["POST"])
def new_message():
    name = request.form["name"]
    user_id = session["user_id"]

    new = NewIngredient(name, user_id)
    new.insert(connect())

    return redirect("/ingredients")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/page")
def hello_world():
    return render_template("sample.html")
