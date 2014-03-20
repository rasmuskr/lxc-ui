import os
import logging

import helpers


logger = logging.getLogger(__name__)


class Containers(object):
    lxc_base_dir = "/var/lib/lxc/"

    lxc_commands = {
        "lxc-create": "/usr/bin/lxc-create",
        "lxc-destroy": "/usr/bin/lxc-destroy",
        "lxc-info": "/usr/bin/lxc-info",
        "lxc-ls": "/usr/bin/lxc-ls",
        "lxc-start": "/usr/bin/lxc-start",
        "lxc-stop": "/usr/bin/lxc-stop",
    }

    def list_groups(self):
        group_list = []
        try:
            ls_dir = os.listdir(self.lxc_base_dir)
            logger.debug("listing basedir, content was '%s'", ls_dir)
            for d in ls_dir:
                full_path = os.path.join(self.lxc_base_dir, d)
                if os.path.isdir(full_path):
                    group_list.append(d)
        except OSError as e:
            logger.error("Failed do list directory '%s', error '%s'", self.lxc_base_dir, e.message)

        return group_list


    def list_containers(self, group_name):
        dir_name = os.path.join(self.lxc_base_dir, group_name)
        command = self.lxc_commands["lxc-ls"] + " "
        command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

        output = helpers.run(command, output=True)

        logger.debug("listing containers for group '%s', output from command '%s'", group_name, output)

        container_names = []
        for line in output.splitlines():
            container_names.append(line)

        logger.debug("listing containers for group '%s', containers '%s'", group_name, container_names)

        return container_names


    def create_container(self, container_name, group_name, template_name="ubuntu"):
        if container_name in self.list_containers(group_name):
            return False

        dir_name = os.path.join(self.lxc_base_dir, group_name)

        command = self.lxc_commands["lxc-create"] + " "
        command += "--name {container_name} ".format(container_name=container_name)
        command += "--template {template_name} ".format(template_name=template_name)
        command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

        result = helpers.run(command)

        logger.debug("created container '%s' for group '%s', result from command '%s'", container_name, group_name,
                     result)

        return result


    def delete_container(self, container_name, group_name):
        if container_name not in self.list_containers(group_name):
            return False

        dir_name = os.path.join(self.lxc_base_dir, group_name)

        command = self.lxc_commands["lxc-destroy"] + " "
        command += "--name {container_name} ".format(container_name=container_name)
        command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

        result = helpers.run(command)

        logger.debug("deleting '%s' for group '%s', result from command '%s'", container_name, group_name, result)

        return result


    def container_status(self, container_name, group_name):
        if container_name not in self.list_containers(group_name):
            return {
                "status": "error",
            }

        dir_name = os.path.join(self.lxc_base_dir, group_name)

        command = self.lxc_commands["lxc-info"] + " "
        command += "--name {container_name} ".format(container_name=container_name)
        command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

        result = helpers.run(command, output=True)

        result_dict = {}
        for line in result.splitlines():
            split_list = line.split(":")
            if len(split_list) != 2:
                logger.debug("failed to split line '%s'", line)
                continue

            key, value = split_list
            key = key.strip()
            value = value.strip()

            if key == "state":
                result_dict["state"] = value

        return result_dict


    def stop_container(self, container_name, group_name):
        if container_name not in self.list_containers(group_name):
            return False

        dir_name = os.path.join(self.lxc_base_dir, group_name)

        command = self.lxc_commands["lxc-stop"] + " "
        command += "--name {container_name} ".format(container_name=container_name)
        command += "--lxcpath {dir_name} ".format(dir_name=dir_name)

        result = helpers.run(command)

        logger.debug("stopping '%s' for group '%s', result from command '%s'", container_name, group_name, result)

        return result


    def start_container(self, container_name, group_name):
        if container_name not in self.list_containers(group_name):
            return False

        dir_name = os.path.join(self.lxc_base_dir, group_name)

        command = self.lxc_commands["lxc-start"] + " "
        command += "--name {container_name} ".format(container_name=container_name)
        command += "--lxcpath {dir_name} ".format(dir_name=dir_name)
        command += "--daemon "

        result = helpers.run(command)

        logger.debug("starting '%s' for group '%s', result from command '%s'", container_name, group_name, result)

        return result


singleton = Containers()