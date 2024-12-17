import secrets
from urllib.parse import urlencode

import requests
from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .models import User, db

HOMEPAGE = "http://localhost:5173"
GOOGLE_AUTH_ENDPOINT = ""
GOOGLE_TOKEN_ENDPOINT = ""
GOOGLE_USERINFO_ENDPOINT = ""

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
    # Generate a random state to prevent CSRF attacks.
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state

    # Generate the callback URL which Google calls after the client logs in.
    params = urlencode(
        {
            "client_id": "",
            "redirect_uri": url_for("main.authorize", _external=True),
            "response_type": "code",
            "scope": "email profile",
            "state": state,
        }
    )
    auth_url = (
        requests.Request("GET", GOOGLE_AUTH_ENDPOINT, params=params).prepare().url
    )
    return redirect(auth_url)


@auth_blueprint.route("/authorize")
def authorize():
    """
    This route is called by the OAuth provider after the user consents.
    It will update the user in the database and log them in.
    """
    # Verify the state matches to prevent CSRF attack.
    state = request.args.get("state")
    if state != session.get("oauth_state"):
        return "Invalid state parameter.", 400

    code = request.args.get("code")
    if not code:
        return "Missing code parameter.", 400

    # Exchange authorization code for an access token.
    data = {
        "code": code,
        "client_id": "",
        "client_secret": "",
        "redirect_uri": "",
        "gran_type": "authorization_code",
    }
    token_response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data)
    if token_response.status_code != 200:
        return f"Failed to fetch token: {token_response.text}", 400

    token_data = token_response.json()
    access_token = token_data.get("access_token")
    if not access_token:
        return "No access token in response", 400

    # Use access token to get user info.
    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(GOOGLE_USERINFO_ENDPOINT, headers=headers)
    if userinfo_response.status_code != 200:
        return f"Failed to fetch user info {userinfo_response.text}"

    user_info = userinfo_response.json()
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
