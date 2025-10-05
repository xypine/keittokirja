import secrets
from flask import session, request

from lib.errors import CSRFError

CSRF_KEY = "csrf_token"


def implant_csrf_token():
    session[CSRF_KEY] = secrets.token_hex(16)


def check_csrf_token():
    if request.form["csrf_token"] != session["csrf_token"]:
        raise CSRFError()
