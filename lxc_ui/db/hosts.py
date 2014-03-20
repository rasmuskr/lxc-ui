import json
import os.path


default_host_data = {
    "hosts": {
        "localhost": {
            "shared_secret": "secret-pre-shared-token",
            "address": "http://127.0.0.1:4900",
            "groups": [
                "default_group",
            ],
        },
    },
}


class HostsDB(object):
    def __init__(self, host_db_file="host_db.json"):
        self.host_db_file = host_db_file

    def _write_default_file(self):
        with open(self.host_db_file, 'w') as f:
            json.dump(default_host_data, f)

    def _read_file(self):
        if os.path.isfile(self.host_db_file):
            self._write_default_file()

        with open(self.host_db_file) as f:
            return json.load(f)

    def get_hosts(self):
        file_data = self._read_file()

        if "hosts" not in file_data:
            return {}

        return file_data["hosts"]