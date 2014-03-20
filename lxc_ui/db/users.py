import json
import os.path


default_user_data = {
    "users": {
        "admin": {
            "password_enc": "123456",
            "groups": [
                "default_group",
            ],
        },
    },
    "groups": {
        "default_group": {
            "description": "This is the default group.",
        }
    },
}


class UserDB(object):
    def __init__(self, user_db_file="user_db.json"):
        self.user_db_file = user_db_file

    def _write_default_file(self):
        with open(self.user_db_file, 'w') as f:
            json.dump(default_user_data, f)

    def _read_file(self):

        if os.path.isfile(self.user_db_file):
            self._write_default_file()

        with open(self.user_db_file) as f:
            return json.load(f)

    def check_user_password(self, username, password):
        file_data = self._read_file()
        if "users" not in file_data:
            return False
        if username not in file_data["users"]:
            return False
        if "password_enc" not in file_data["users"][username]:
            return False
        if file_data["users"][username]["password_enc"] == password:
            return True
        return False

    def get_user_groups(self, username):
        file_data = self._read_file()
        if "users" not in file_data:
            return []
        if username not in file_data["users"]:
            return []
        if "groups" not in file_data["users"][username]:
            return []

        return file_data["users"][username]["groups"]

    def get_group_data(self, group_name):
        file_data = self._read_file()
        if "groups" not in file_data:
            return {}
        if group_name not in file_data["groups"]:
            return {}

        return file_data["groups"][group_name]