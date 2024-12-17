from urllib.parse import urlencode

from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .models import User, db

HOMEPAGE = "http://localhost:5173"

auth_blueprint = Blueprint("main", __name__, url_prefix="/api")

oauth = OAuth()


@auth_blueprint.route("/ping")
def ping():
    """
    Test route.
    """
    return "pong"


@auth_blueprint.route("/login")
def login():
    """
    This route starts the OAuth login flow.
    """
    if not current_user.is_anonymous:
        return redirect(HOMEPAGE)

    # Generate the callback URL which Google calls after the client logs in.
    query_string = urlencode(
        {
            "client_id": "",
            "redirect_uri": "",
            "response_type": "code",
            "scope": "",
            "state": "",
        }
    )
    return redirect(f"?{query_string}")


@auth_blueprint.route("/authorize")
def authorize():
    """
    This route is called by the OAuth provider after the user consents.
    It will update the user in the database and log them in.
    """
    token = oauth.google.authorize_access_token()

    # Extract Relevant User Info
    user_info = token["userinfo"]
    email = user_info.get("email")
    name = user_info.get("name")

    # Find / Create User in DB
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, name=name)
        db.session.add(user)
        db.session.commit()

    # Log-In the User
    login_user(user)

    # Redirect to React frontend.
    return redirect(HOMEPAGE)


@auth_blueprint.route("/logout")
def logout():
    """
    Logs the user out.
    """
    logout_user()
    return redirect(HOMEPAGE)


@auth_blueprint.route("/user")
@login_required
def user():
    """
    Allows frontend to retrieve logged-in user information.
    """
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
