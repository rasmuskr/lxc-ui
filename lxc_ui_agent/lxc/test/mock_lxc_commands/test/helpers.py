import os
import sys
import subprocess

import logging

logger = logging.getLogger(__name__)


def lxc_ls(lxc_path):
    path = os.path.abspath(os.path.dirname(__file__))
    lxc_executable = os.path.join(path, "..", "lxc-ls.py")

    args = ""
    if lxc_path:
        args += "--lxcpath \"" + lxc_path + "\" "
    full_command = '"{python}" "{executable}" {args}'.format(python=sys.executable, executable=lxc_executable,
                                                             args=args)
    logger.debug("calling lxc-ls: %s", full_command)
    output = subprocess.check_output(full_command, shell=True)
    logger.debug("output from lxc-ls: %s", output)
    return output


def lxc_create(lxc_path, name, template="ubuntu"):
    path = os.path.abspath(os.path.dirname(__file__))
    lxc_executable = os.path.join(path, "..", "lxc-create.py")

    args = ""
    if lxc_path:
        args += "--lxcpath \"" + lxc_path + "\" "
    if name:
        args += "--name \"" + name + "\" "
    if template:
        args += "--template \"" + template + "\" "

    full_command = '"{python}" "{executable}" {args}'.format(python=sys.executable, executable=lxc_executable,
                                                             args=args)
    logger.debug("calling lxc-create: %s", full_command)
    output = subprocess.check_output(full_command, shell=True)
    logger.debug("output from lxc-create: %s", output)
    return output


def lxc_destroy(lxc_path, name):
    path = os.path.abspath(os.path.dirname(__file__))
    lxc_executable = os.path.join(path, "..", "lxc-destroy.py")

    args = ""
    if lxc_path:
        args += "--lxcpath \"" + lxc_path + "\" "
    if name:
        args += "--name \"" + name + "\" "

    full_command = '"{python}" "{executable}" {args}'.format(python=sys.executable, executable=lxc_executable,
                                                             args=args)
    logger.debug("calling lxc-destroy: %s", full_command)
    output = subprocess.check_output(full_command, shell=True)
    logger.debug("output from lxc-destroy: %s", output)
    return output


def lxc_info(lxc_path, name):
    path = os.path.abspath(os.path.dirname(__file__))
    lxc_executable = os.path.join(path, "..", "lxc-info.py")

    args = ""
    if lxc_path:
        args += "--lxcpath \"" + lxc_path + "\" "
    if name:
        args += "--name \"" + name + "\" "

    full_command = '"{python}" "{executable}" {args}'.format(python=sys.executable, executable=lxc_executable,
                                                             args=args)
    logger.debug("calling lxc-info: %s", full_command)
    output = subprocess.check_output(full_command, shell=True)
    logger.debug("output from lxc-info: %s", output)
    return output


def lxc_start(lxc_path, name):
    path = os.path.abspath(os.path.dirname(__file__))
    lxc_executable = os.path.join(path, "..", "lxc-start.py")

    args = ""
    if lxc_path:
        args += "--lxcpath \"" + lxc_path + "\" "
    if name:
        args += "--name \"" + name + "\" "

    args += "--daemon "

    full_command = '"{python}" "{executable}" {args}'.format(python=sys.executable, executable=lxc_executable,
                                                             args=args)
    logger.debug("calling lxc-start: %s", full_command)
    output = subprocess.check_output(full_command, shell=True)
    logger.debug("output from lxc-start: %s", output)
    return output


def lxc_stop(lxc_path, name):
    path = os.path.abspath(os.path.dirname(__file__))
    lxc_executable = os.path.join(path, "..", "lxc-stop.py")

    args = ""
    if lxc_path:
        args += "--lxcpath \"" + lxc_path + "\" "
    if name:
        args += "--name \"" + name + "\" "

    full_command = '"{python}" "{executable}" {args}'.format(python=sys.executable, executable=lxc_executable,
                                                             args=args)
    logger.debug("calling lxc-stop: %s", full_command)
    output = subprocess.check_output(full_command, shell=True)
    logger.debug("output from lxc-stop: %s", output)
    return output