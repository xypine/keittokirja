from flask import Flask, render_template, request

app = Flask(__name__)


@app.context_processor
def inject_nav_items():
    current_endpoint = request.endpoint or "unknown"

    nav_items = [
        {
            "url": "/",
            "label": "Search",
            "endpoint": "index",
            "active": current_endpoint == "index",
        },
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


@app.route("/ingredients")
def ingredients():
    return render_template("ingredients.html")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html")


@app.route("/page")
def hello_world():
    return render_template("sample.html")
