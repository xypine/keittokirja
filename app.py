from os import environ
from flask import Flask, render_template, request, redirect, session

from src.ingredients import Ingredient, NewIngredient
from src.recipes import Recipe, NewRecipe, RecipeListing
from src.db import connect
from src.auth import (
    CREDENTIAL_CHECK_OK,
    CREDENTIAL_CHECK_UNVERIFIED,
    PRE_TRUSTED_USER,
    check_credentials,
    create_credentials,
    forget_session,
)
from src.requirements import NewRequirement, Requirement
from src.steps import NewStep, Step
from src.utils import or_empty

app = Flask(__name__)
app.secret_key = environ["SECRET_KEY"]

VERIFY_CONTACT = environ.get("VERIFY_CONTACT") or "the administrator"


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
    recipes = RecipeListing.get(connect(), limit=6)
    return render_template("home.html", top_picks=recipes)


@app.route("/login")
def login_form():
    return render_template("auth/login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    result = check_credentials(connect(), username, password)
    if result == CREDENTIAL_CHECK_OK:
        return redirect("/")
    elif result == CREDENTIAL_CHECK_UNVERIFIED:
        return f"Your user is still unverified, please contact {VERIFY_CONTACT} to get your account verified"

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
        if username == PRE_TRUSTED_USER:
            return "User created, you can now log in!"
        return f"User created, you can log in after your account has been verified. Contact {VERIFY_CONTACT} to get your account verified."

    return "Error creating user, maybe the username is already taken?"


@app.route("/logout")
def logout():
    forget_session()
    return redirect("/")


@app.route("/ingredients")
def ingredients():
    user_id = session.get("user_id")
    created_by = request.args.get("created_by")
    created_by_id = None
    if created_by == "me":
        created_by_id = user_id
    name_like = request.args.get("name_like")
    ingredients = Ingredient.get(connect(), created_by_id, name_like)
    return render_template(
        "ingredients.html",
        ingredients=ingredients,
        created_by=or_empty(created_by),
        name_like=or_empty(name_like),
    )


@app.route("/ingredients/new")
def ingredients_new():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    return render_template("ingredients_new.html")


@app.route("/ingredients/new", methods=["POST"])
def new_ingredient_handler():
    name = request.form["name"]
    user_id = session["user_id"]

    new = NewIngredient(name, user_id)
    new.insert(connect())

    return redirect("/ingredients")


@app.route("/recipes")
def recipes():
    user_id = session.get("user_id")
    created_by = request.args.get("created_by")
    created_by_id = None
    if created_by == "me":
        created_by_id = user_id
    name_like = request.args.get("name_like")
    recipes = RecipeListing.get(connect(), created_by_id, name_like)
    return render_template(
        "recipes.html",
        recipes=recipes,
        created_by=or_empty(created_by),
        name_like=or_empty(name_like),
        logged_in=bool(user_id),
    )


@app.route("/recipes/new")
def recipes_new():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    return render_template("recipes_new.html")


@app.route("/recipes/new", methods=["POST"])
def new_recipe_handler():
    name = request.form["name"]
    user_id = session["user_id"]

    new = NewRecipe(name, user_id)
    new.insert(connect())

    return redirect(f"/recipes/{new.slug}/edit")


@app.route("/recipes/<slug>")
def recipe(slug: str):
    user_id = session.get("user_id")
    recipe = Recipe.get_by_slug(connect(), slug)
    return render_template(
        "recipe.html",
        recipe=recipe,
        own=(recipe.created_by == user_id),
        logged_in=bool(user_id),
    )


@app.route("/recipes/<slug>/edit")
def recipe_edit(slug: str):
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    recipe = Recipe.get_by_slug(connect(), slug)
    recipes = RecipeListing.get(connect())
    ingredients = Ingredient.get(connect())
    return render_template(
        "recipe_edit.html", recipe=recipe, recipes=recipes, ingredients=ingredients
    )


@app.route("/recipes/<recipe_id>/ingredients", methods=["POST"])
def new_recipe_ingredient_handler(recipe_id: int):
    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]
    amount = request.form["amount"]
    extra_info = request.form["extra_info"]
    ingredient_id = request.form["ingredient_id"]
    ingredient_recipe_id = request.form["ingredient_recipe_id"]

    new = NewRequirement(
        user_id, recipe_id, amount, extra_info, ingredient_id, ingredient_recipe_id
    )
    new.insert(connect())

    return redirect(f"/recipes/{recipe_slug}/edit")


@app.route("/recipes/<recipe_id>/ingredients/<requirement_id>/delete", methods=["POST"])
def delete_recipe_ingredient_handler(recipe_id: int, requirement_id: int):
    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]

    Requirement.delete(connect(), requirement_id, recipe_id, user_id)

    return redirect(f"/recipes/{recipe_slug}/edit")


@app.route("/recipes/<recipe_id>/steps", methods=["POST"])
def new_recipe_step_handler(recipe_id: int):
    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]
    summary = request.form["summary"]
    details = request.form["details"]

    if len(summary) < 3:
        raise Exception("summary must be at least 3 characters long")

    new = NewStep(user_id, recipe_id, summary, details)
    new.insert(connect())

    return redirect(f"/recipes/{recipe_slug}/edit")


@app.route("/recipes/<recipe_id>/steps/<step_id>/edit", methods=["POST"])
def edit_recipe_step_handler(recipe_id: int, step_id: int):
    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]
    summary = request.form["summary"]
    details = request.form["details"]

    if len(summary) < 3:
        raise Exception("summary must be at least 3 characters long")

    Step(step_id, recipe_id, summary, details).put(connect(), user_id)

    return redirect(f"/recipes/{recipe_slug}/edit")


@app.route("/recipes/<recipe_id>/steps/<step_id>/delete", methods=["POST"])
def delete_recipe_step_handler(recipe_id: int, step_id: int):
    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]

    Step.delete(connect(), step_id, recipe_id, user_id)

    return redirect(f"/recipes/{recipe_slug}/edit")
