import flask


api_blueprint = flask.Blueprint(__name__, "api")


@api_blueprint.route("/groups/<group_name>/containers/", methods=['POST', 'GET'])
def containers_create(group_name):
    if flask.request.method == "POST":
        data = flask.request.json

        pass

    return "bla"


@api_blueprint.route("/groups/<group_name>/containers/<container_name>/", methods=['DELETE', 'GET'])
def container_info(group_name, container_name):
    return "bla"