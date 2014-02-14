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
    token = "secret-pre-shared-token"
    app.config["lxc_ui_agent_config"] = {}
    app.config["lxc_ui_agent_config"]["expected_token"] = token
    app.run("0.0.0.0", 4800, debug=True)
