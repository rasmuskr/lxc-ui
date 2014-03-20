import logging

logger = logging.getLogger(__name__)

import flask

app = flask.Flask(__name__)

import api.users

app.register_blueprint(api.users.users_blueprint)


@app.route("/")
def root():
    headers = {
        "Location": "/static/lxc-ui/index.html",
    }
    return flask.Response("Redirecting", status=302, headers=headers)


if __name__ == "__main__":
    logging.root.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)

    # load config
    app.config.from_pyfile('application.cfg', silent=True)
    app.run("0.0.0.0", 5000, debug=True)
