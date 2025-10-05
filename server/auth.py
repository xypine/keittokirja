from os import environ
from flask import request, render_template, redirect, Blueprint

from lib.auth import (
    CREDENTIAL_CHECK_OK,
    CREDENTIAL_CHECK_UNVERIFIED,
    PRE_TRUSTED_USER,
    try_login,
    create_credentials,
    forget_session,
)
from server import get_db


VERIFY_CONTACT = environ.get("VERIFY_CONTACT") or "the administrator"
auth = Blueprint("auth", __name__)


@auth.route("/login")
def login_form():
    return render_template("auth/login.html")


@auth.route("/login", methods=["POST"])
def login():
    db = get_db()

    username = request.form["username"]
    password = request.form["password"]

    result = try_login(db, username, password)
    if result == CREDENTIAL_CHECK_OK:
        return redirect("/")
    elif result == CREDENTIAL_CHECK_UNVERIFIED:
        return f"Your user is still unverified, please contact {VERIFY_CONTACT} to get your account verified"

    return "Wrong username or password"


@auth.route("/logout")
def logout():
    forget_session()
    return redirect("/")


@auth.route("/register")
def register_form():
    return render_template("auth/register.html")


@auth.route("/register", methods=["POST"])
def register():
    db = get_db()

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        return "Passwords don't match."

    result = create_credentials(db, username, password1)
    if result:
        if username == PRE_TRUSTED_USER:
            return "User created, you can now log in!"
        return f"User created, you can log in after your account has been verified. Contact {VERIFY_CONTACT} to get your account verified."

    return "Error creating user, maybe the username is already taken?"
