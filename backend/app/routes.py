from flask import Blueprint

auth_blueprint = Blueprint("main", __name__)


@auth_blueprint.route("/api/ping")
def ping():
    return {"message": "pong"}
