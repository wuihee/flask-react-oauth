from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, url_for

auth_blueprint = Blueprint("main", __name__)

oauth = OAuth()
oauth.register(
    name="google",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    client_kwargs={"scope": "openid profile"},
)


@auth_blueprint.route("/api/ping")
def ping():
    return {"message": "pong"}


@auth_blueprint.route("/login")
def login():
    redirect_uri = url_for("authorize", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@auth_blueprint.route("/authorize")
def authorize():
    token = oauth.google.authorize_access_token()
    response = oauth.google.get("account/verify_credentials.json")
    response.rase_for_status()
    profile = response.json()
    return redirect("/")


@auth_blueprint.route("/logout")
def logout():
    pass
