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
    # server_metadata_url contains all relevant URLs including the access_token_url,
    # authorize_url, userinfo_endpoint, etc.
    # client_kwargs - Scope of information we are requesting from Google.
    oauth.init_app(app)
    oauth.register(
        name="google",
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )

    # Register Blueprint for Routes
    app.register_blueprint(auth_blueprint)

    # Setup Flask-Login
    login = LoginManager(app)

    @login.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app
