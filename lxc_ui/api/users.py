import logging
import json

import flask

import helpers
import db.users


logger = logging.getLogger(__name__)
users_blueprint = flask.Blueprint(__name__, "users")

user_db = db.users.UserDB()


@users_blueprint.route("/users/login/", methods=["POST", ])
def groups():
    if flask.request.method == "POST":

        data = json.loads(flask.request.data)
        if type(data) is not dict:
            return flask.Response("root data not dict", status=400)

        if "username" not in data or "password" not in data:
            return flask.Response("container_name missing", status=400)

        username = data["username"]
        password = data["password"]

        if user_db.check_user_password(username, password) is not True:
            return flask.Response("username or password wrong", status=401)

        token = helpers.token_db.add_token(username)

        return_data = {
            "token": token,
        }

        return flask.Response(return_data, status=201)

    return flask.Response(status=400)

