from flask import Blueprint

auth_blueprint = Blueprint("main", __name__)


@auth_blueprint.route("/api/ping")
def ping():
    return {"message": "pong"}


@auth_blueprint.route("/login")
def login():
    pass


@auth_blueprint.route("/callback")
def oauth_callback():
    pass


@auth_blueprint.route("/logout")
def logout():
    pass
