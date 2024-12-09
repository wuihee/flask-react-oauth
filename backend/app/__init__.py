from flask import Flask
from flask_login import LoginManager

from .config import Config
from .models import User, db
from .routes import auth_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(auth_blueprint)

    login = LoginManager(app)

    @login.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    return app
