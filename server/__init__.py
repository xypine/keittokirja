from os import environ
from flask import Flask, flash, request, redirect, render_template, abort


from lib.db import close_db, get_db
from lib.errors import CSRFError, UserError
from server.auth import auth
from server.ingredients import ingredients
from server.recipes import recipes

# Flask boilerplate to get context & global data up and running

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = environ["SECRET_KEY"]


@app.errorhandler(UserError)
def handle_user_error(e):
    flash(str(e), "error")
    return redirect(request.referrer or "/")


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    abort(403)


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


app.teardown_appcontext(close_db)


# All normal routes
app.register_blueprint(auth)
app.register_blueprint(ingredients)
app.register_blueprint(recipes)


# Homepage
from lib.recipes import RecipeListing


@app.route("/")
def index():
    recipes = RecipeListing.get(get_db(), limit=6)
    return render_template("home.html", top_picks=recipes)
