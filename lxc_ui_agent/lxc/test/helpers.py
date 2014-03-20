import tempfile
import shutil
import os
import sys
import logging

import lxc.containers


logger = logging.getLogger(__name__)


def get_containers_with_mock_binaries():
    temp_dir = tempfile.mkdtemp()
    logger.debug("created temp directory %s", temp_dir)

    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "mock_lxc_commands")
    lxc_commands = {
        "lxc-create": "\"" + sys.executable + "\" \"" + os.path.join(path, "lxc-create.py") + "\"",
        "lxc-destroy": "\"" + sys.executable + "\" \"" + os.path.join(path, "lxc-destroy.py") + "\"",
        "lxc-info": "\"" + sys.executable + "\" \"" + os.path.join(path, "lxc-info.py") + "\"",
        "lxc-ls": "\"" + sys.executable + "\" \"" + os.path.join(path, "lxc-ls.py") + "\"",
        "lxc-start": "\"" + sys.executable + "\" \"" + os.path.join(path, "lxc-start.py") + "\"",
        "lxc-stop": "\"" + sys.executable + "\" \"" + os.path.join(path, "lxc-stop.py") + "\"",
    }

    containers = lxc.containers.Containers()
    containers.lxc_base_dir = temp_dir
    containers.lxc_commands = lxc_commands

    return containers


def cleanup_containers_with_mock_binaries(containers):
    shutil.rmtree(containers.lxc_base_dir)
    logger.debug("removed temp directory %s", containers.lxc_base_dir)