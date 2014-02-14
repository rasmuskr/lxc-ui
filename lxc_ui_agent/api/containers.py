import json
import logging

import flask

import lxc_ui_agent.lxc.containers
import helpers


logger = logging.getLogger(__name__)
container_blueprint = flask.Blueprint(__name__, "containers")


@container_blueprint.route("/groups/", methods=["GET", ])
@helpers.secured_endpoint
def groups():
    if flask.request.method == "GET":
        data = {}
        groups = lxc_ui_agent.lxc.containers.list_groups()
        data["groups"] = groups
        return flask.jsonify(data)

    return flask.Response(status=400)


@container_blueprint.route("/groups/<group_name>/containers/", methods=["POST", "GET"])
@helpers.secured_endpoint
def containers_create(group_name):
    if flask.request.method == "GET":
        data = {}
        containers = lxc_ui_agent.lxc.containers.list_containers(group_name)
        data["containers"] = containers
        return flask.jsonify(data)

    elif flask.request.method == "POST":
        data = json.loads(flask.request.data)
        if type(data) is not dict:
            return flask.Response("root data not dict", status=400)

        if "container_name" not in data:
            return flask.Response("container_name missing", status=400)

        container_name = data["container_name"]

        status = lxc_ui_agent.lxc.containers.create_container(container_name, group_name)

        logger.debug("created container %s", status)

        if not status:
            return flask.Response("failed to create container", status=500)

        return flask.Response(status=201)

    return flask.Response(status=400)


@container_blueprint.route("/groups/<group_name>/containers/<container_name>/", methods=["DELETE", "GET", ])
@helpers.secured_endpoint
def container_info(group_name, container_name):
    if flask.request.method == "GET":
        data = {
            "container_name": container_name,
            "group_name": group_name,

        }
        return flask.jsonify(data)

    elif flask.request.method == "DELETE":

        status = lxc_ui_agent.lxc.containers.delete_container(container_name, group_name)

        if not status:
            return flask.Response("failed to create container", status=500)

        return flask.Response(status=200)

    return flask.Response(status=400)