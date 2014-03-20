import os


port_counter = 0


def get_next_port_number():
    global port_counter
    port_number = 5100 + port_counter
    port_counter += 1
    return port_number


def start_agent(port):
    path = os.path.abspath(os.path.dirname(__file__))
    lxc_ui_agent_binary = os.path.join(path, "..", "..", "..", "lxc_ui_agent", "lxc_ui_agent.py")
    options = "--mock_lxc_binaries --port %s" % (port, )


class AgentRunner(object):
    def __init__(self, port):
        pass

    def run(self):
        pass
    