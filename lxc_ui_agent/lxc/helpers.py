import subprocess
import logging

logger = logging.getLogger(__name__)


def run(cmd, output=False):
    logger.debug("running command '%s'", cmd)
    if output:
        try:
            out = subprocess.check_output('{}'.format(cmd), shell=True)
        except subprocess.CalledProcessError as e:
            logger.error("Failed to call subprocess for command '%s' error '%s'", cmd, e.message)
            out = False
        return out

    return not subprocess.check_call('{}'.format(cmd), shell=True)

