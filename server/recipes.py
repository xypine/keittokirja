from flask import Blueprint, render_template, request, redirect, session

from lib.ingredients import Ingredient
from lib.utils import or_empty
from lib.recipes import Recipe, NewRecipe, RecipeListing
from lib.requirements import NewRequirement, Requirement
from lib.steps import NewStep, Step
from server import get_db

recipes = Blueprint("recipes", __name__)


@recipes.route("/recipes")
def recipes_list():
    db = get_db()

    user_id = session.get("user_id")
    created_by = request.args.get("created_by")
    created_by_id = None
    if created_by == "me":
        created_by_id = user_id
    name_like = request.args.get("name_like")
    recipes = RecipeListing.get(db, created_by_id, name_like)
    return render_template(
        "recipes.html",
        recipes=recipes,
        created_by=or_empty(created_by),
        name_like=or_empty(name_like),
        logged_in=bool(user_id),
    )


@recipes.route("/recipes/new")
def recipes_new():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    return render_template("recipes_new.html")


@recipes.route("/recipes/new", methods=["POST"])
def new_recipe_handler():
    db = get_db()

    name = request.form["name"]
    user_id = session["user_id"]

    new = NewRecipe(name, user_id)
    new.insert(db)

    return redirect(f"/recipes/{new.slug}/edit")


@recipes.route("/recipes/<slug>")
def recipe(slug: str):
    db = get_db()

    user_id = session.get("user_id")
    recipe = Recipe.get_by_slug(db, slug)
    return render_template(
        "recipe.html",
        recipe=recipe,
        own=(recipe.created_by == user_id),
        logged_in=bool(user_id),
    )


@recipes.route("/recipes/<slug>/edit")
def recipe_edit(slug: str):
    db = get_db()

    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    recipe = Recipe.get_by_slug(db, slug)
    recipes = RecipeListing.get(db)
    ingredients = Ingredient.get(db)
    return render_template(
        "recipe_edit.html", recipe=recipe, recipes=recipes, ingredients=ingredients
    )


@recipes.route("/recipes/<recipe_id>/ingredients", methods=["POST"])
def new_recipe_ingredient_handler(recipe_id: int):
    db = get_db()

    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]
    amount = request.form["amount"]
    extra_info = request.form["extra_info"]
    ingredient_id = request.form["ingredient_id"]
    ingredient_recipe_id = request.form["ingredient_recipe_id"]

    new = NewRequirement(
        user_id, recipe_id, amount, extra_info, ingredient_id, ingredient_recipe_id
    )
    new.insert(db)

    return redirect(f"/recipes/{recipe_slug}/edit")


@recipes.route(
    "/recipes/<recipe_id>/ingredients/<requirement_id>/delete", methods=["POST"]
)
def delete_recipe_ingredient_handler(recipe_id: int, requirement_id: int):
    db = get_db()

    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]

    Requirement.delete(db, requirement_id, recipe_id, user_id)

    return redirect(f"/recipes/{recipe_slug}/edit")


@recipes.route("/recipes/<recipe_id>/steps", methods=["POST"])
def new_recipe_step_handler(recipe_id: int):
    db = get_db()

    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]
    summary = request.form["summary"]
    details = request.form["details"]

    if len(summary) < 3:
        raise Exception("summary must be at least 3 characters long")

    new = NewStep(user_id, recipe_id, summary, details)
    new.insert(db)

    return redirect(f"/recipes/{recipe_slug}/edit")


@recipes.route("/recipes/<recipe_id>/steps/<step_id>/edit", methods=["POST"])
def edit_recipe_step_handler(recipe_id: int, step_id: int):
    db = get_db()

    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]
    summary = request.form["summary"]
    details = request.form["details"]

    if len(summary) < 3:
        raise Exception("summary must be at least 3 characters long")

    Step(step_id, recipe_id, summary, details).put(db, user_id)

    return redirect(f"/recipes/{recipe_slug}/edit")


@recipes.route("/recipes/<recipe_id>/steps/<step_id>/delete", methods=["POST"])
def delete_recipe_step_handler(recipe_id: int, step_id: int):
    db = get_db()

    user_id = session["user_id"]
    recipe_slug = request.form["recipe_slug"]

    Step.delete(db, step_id, recipe_id, user_id)

    return redirect(f"/recipes/{recipe_slug}/edit")
