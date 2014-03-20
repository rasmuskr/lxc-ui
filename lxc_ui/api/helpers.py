import functools
import logging

import flask

import db.tokens


logger = logging.getLogger(__name__)

token_db = db.tokens.TokenDB()


def check_auth(token):
    flask.request.__dict__["extra_auth_data"] = None

    token_data = token_db.get_token_data(token)
    if token_data is None:
        return False

    flask.request.__dict__["extra_auth_data"] = token_data

    return True


def secured_endpoint(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        try:
            auth = flask.request.headers["Authorization"]
            # strip bearer
            token = auth[7:]
            if not token or not check_auth(token):
                logger.debug("failed auth '%s'", token)
                return flask.Response("Unauthorized", status=401)
        except Exception as e:
            return flask.Response("Unauthorized, failed to auth '%s'" % (e.message, ), status=401)

        # if we get here we are okay to run it... but we run it outside try except to get proper exception behaviour
        return f(*args, **kwargs)

    return decorated