from flask import Blueprint, render_template, request, redirect, session

from lib.csrf import check_csrf_token
from lib.ingredients import Ingredient, NewIngredient
from lib.utils import or_empty
from server import get_db

ingredients = Blueprint("ingredients", __name__)


@ingredients.route("/ingredients")
def ingredients_list():
    db = get_db()

    user_id = session.get("user_id")
    created_by = request.args.get("created_by")
    created_by_id = None
    if created_by == "me":
        created_by_id = user_id
    name_like = request.args.get("name_like")
    ingredients = Ingredient.get(db, created_by_id, name_like)
    return render_template(
        "ingredients.html",
        ingredients=ingredients,
        created_by=or_empty(created_by),
        name_like=or_empty(name_like),
    )


@ingredients.route("/ingredients/new")
def ingredients_new():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    return render_template("ingredients_new.html")


@ingredients.route("/ingredients/new", methods=["POST"])
def new_ingredient_handler():
    check_csrf_token()
    db = get_db()

    name = request.form["name"]
    user_id = session["user_id"]

    new = NewIngredient(name, user_id)
    new.insert(db)

    return redirect("/ingredients")


@ingredients.route("/ingredients/<ingredient_id>/delete", methods=["POST"])
def delete_recipe_ingredient_handler(ingredient_id: int):
    check_csrf_token()
    db = get_db()

    user_id = session["user_id"]

    Ingredient.delete(db, ingredient_id, user_id)

    return redirect(f"/ingredients")
