import os
import logging

import helpers


logger = logging.getLogger(__name__)

lxc_base_dir = "/var/lib/lxc/"


def list_groups():
    group_list = []
    try:
        ls_dir = os.listdir(lxc_base_dir)
        for d in ls_dir:
            if os.path.isdir(lxc_base_dir + d):
                group_list.append(lxc_base_dir + d)
    except OSError as e:
        logger.error("Failed do list directory '%s', error '%s'", lxc_base_dir, e.message)

    return group_list


def list_containers(group_name):
    dir_name = lxc_base_dir + "" + group_name + "/"
    command = "lxc-ls "
    command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

    output = helpers.run(command, output=True)

    logger.debug("listing containers for group '%s', output from command '%s'", group_name, output)

    container_names = []
    for line in output.splitlines():
        container_names.append(line)

    logger.debug("listing containers for group '%s', containers '%s'", group_name, container_names)

    return container_names


def create_container(container_name, group_name, template_name="ubuntu"):
    if container_name in list_containers(group_name):
        return False

    dir_name = lxc_base_dir + "" + group_name + "/"

    command = "lxc-create "
    command += "--name {container_name} ".format(container_name=container_name)
    command += "--template {template_name} ".format(template_name=template_name)
    command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

    result = helpers.run(command)

    logger.debug("created container '%s' for group '%s', result from command '%s'", container_name, group_name, result)

    return result


def delete_container(container_name, group_name):
    if container_name not in list_containers(group_name):
        return False

    dir_name = lxc_base_dir + "" + group_name + "/"

    command = "lxc-destroy "
    command += "--name {container_name} ".format(container_name=container_name)
    command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

    result = helpers.run(command)

    logger.debug("deleting '%s' for group '%s', result from command '%s'", container_name, group_name, result)

    return result


def stop_container(container_name, group_name):
    if container_name not in list_containers(group_name):
        return False

    dir_name = lxc_base_dir + "" + group_name + "/"

    command = "lxc-stop "
    command += "--name {container_name} ".format(container_name=container_name)
    command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

    result = helpers.run(command)

    logger.debug("stopping '%s' for group '%s', result from command '%s'", container_name, group_name, result)

    return result


def start_container(container_name, group_name):
    if container_name not in list_containers(group_name):
        return False

    dir_name = lxc_base_dir + "" + group_name + "/"

    command = "lxc-start "
    command += "--name {container_name} ".format(container_name=container_name)
    command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

    result = helpers.run(command)

    logger.debug("starting '%s' for group '%s', result from command '%s'", container_name, group_name, result)

    return result