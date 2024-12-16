from authlib.integrations.flask_client import OAuth
from flask import Blueprint, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .models import User, db

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
    # Generate the callback URL which Google calls after the client logs in.
    redirect_uri = url_for("main.authorize", _external=True)

    # Construct the URL to Google's login page including:
    #   - redirect_uri
    #   - client_id
    #   - Randomly generated state parameter for CSRF protection.
    return oauth.google.authorize_redirect(redirect_uri)


@auth_blueprint.route("/authorize")
def authorize():
    """
    This route is called by Google after the user consents.
    Google includes query parameters including a:
      - code: A temporary authorization token that Flask will exchange for
              an access token.
      - state: The state value our app generated to protect against CSRF.
    """
    token = oauth.google.authorize_access_token()

    print(token)

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
    return redirect("http://localhost:5173")


@auth_blueprint.route("/logout")
def logout():
    """
    Logs the user out.
    """
    logout_user()
    return redirect("http://localhost:5173")


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
