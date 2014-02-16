import functools
import logging

import flask


logger = logging.getLogger(__name__)


def check_auth(token):
    expected_token = flask.current_app.config.get("lxc_ui_agent_config", {}).get("expected_token", None)

    if expected_token is not None and token == expected_token:
        return True
    return False


def secured_endpoint(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth = flask.request.headers["Authorization"]
            token = auth[7:]
            if not token or not check_auth(token):
                logger.debug("failed auth '%s'", token)
                return flask.Response("Unauthorized", status=401)
        except Exception as e:
            return flask.Response("Unauthorized, failed to auth '%s'" % (e.message, ), status=401)

        # if we get here we are okay to run it... but we run it outside try except to get proper exception behaviour
        return f(*args, **kwargs)

    return decorated