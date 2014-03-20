import logging

logger = logging.getLogger(__name__)

import flask

app = flask.Flask(__name__)

# stuff global vars in here so we can mess with them for testing
import lxc.containers

app.config["singletons"] = {}
app.config["singletons"]["containers"] = lxc.containers.Containers()

import api.containers

app.register_blueprint(api.containers.container_blueprint)


@app.route('/')
def root():
    """
    """
    data = {
    }
    return flask.jsonify(data)


import argparse

parser = argparse.ArgumentParser(description='LXC UI Agent application.')
parser.add_argument('--port', type=int, default=4800, help='the port the agent should listen on')
parser.add_argument('--listen_address', default="0.0.0.0", help='the address the agent should listen on')
parser.add_argument('--mock_lxc_binaries', action='store_true', default=False,
                    help='if we should run against testing lxc_binaries')

if __name__ == "__main__":
    logging.root.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)

    args = parser.parse_args()

    if args.mock_lxc_binaries:
        import lxc.test.helpers

        app.config["singletons"]["containers"] = lxc.test.helpers.get_containers_with_mock_binaries()

        # make sure the directory is deleted after we exit
        def cleanup_on_exit():
            lxc.test.helpers.cleanup_containers_with_mock_binaries(app.config["singletons"]["containers"])
            pass

        import atexit

        atexit.register(cleanup_on_exit)


    # load config
    app.config.from_pyfile('application.cfg', silent=True)

    # if no token is set in config just make one up :)
    default_token = "secret-pre-shared-token"
    if "lxc_ui_agent_config" not in app.config:
        app.config["lxc_ui_agent_config"] = {}
    if "expected_token" not in app.config["lxc_ui_agent_config"]:
        app.config["lxc_ui_agent_config"]["expected_token"] = default_token

    logger.debug("starting server with token '%s'" % (app.config["lxc_ui_agent_config"]["expected_token"], ))
    app.run(args.listen_address, args.port, debug=True)
