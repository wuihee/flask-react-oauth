from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

from .config import Config
from .models import User, db
from .routes import auth_blueprint, oauth


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # In dev, allow CORS for all domains on all routes.
    CORS(app)

    # Initialize DB and create tables.
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Initialize OAuth
    oauth.init_app(app)
    oauth.register(
        name="google",
        access_token_url="https://oauth2.googleapis.com/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
        client_kwargs={"scope": "openid email profile"},
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
        redirect_uri="http://localhost:5000/api/authorize",
    )

    # Register Blueprint for Routes
    app.register_blueprint(auth_blueprint)

    # Setup Flask-Login
    login = LoginManager(app)

    @login.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app
