import flask

app = flask.Flask(__name__)


@app.route('/')
def root():
    """

    """

    data = {
        "test": "hest",
    }

    return flask.jsonify(data)


if __name__ == "__main__":
    app.run("0.0.0.0", 4800, debug=True)
