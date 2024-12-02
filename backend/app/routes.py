from flask import Blueprint

blueprint = Blueprint("main", __name__)


@blueprint.route("/api/ping")
def ping():
    return {"message": "pong"}
