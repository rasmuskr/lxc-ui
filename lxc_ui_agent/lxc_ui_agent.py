import logging

logger = logging.getLogger(__name__)

import flask

app = flask.Flask(__name__)

import api.containers
app.register_blueprint(api.containers.container_blueprint)


@app.route('/')
def root():
    """

    """

    data = {
        "test": "hest",
    }

    return flask.jsonify(data)


if __name__ == "__main__":

    logging.root.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)

    # load config
    app.config.from_pyfile('application.cfg', silent=True)

    # if no token is set in config just make one up :)
    default_token = "secret-pre-shared-token"
    if "lxc_ui_agent_config" not in app.config:
        app.config["lxc_ui_agent_config"] = {}
    if "expected_token" not in app.config["lxc_ui_agent_config"]:
        app.config["lxc_ui_agent_config"]["expected_token"] = default_token

    logger.debug("starting server with token '%s'" % (app.config["lxc_ui_agent_config"]["expected_token"], ))
    app.run("0.0.0.0", 4800, debug=True)
