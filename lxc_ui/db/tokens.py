import time
import string
import random


class TokenDB(object):
    def __init__(self):
        self._token_db = {}
        self._token_size = 512
        self._token_ttl = 60 * 60 * 2

    def _generate_token(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(self._token_size))

    def add_token(self, username):
        now = time.time()
        token = self._generate_token()
        # make sure we do not overwrite a token already in there
        while token in self._token_db:
            token = self._generate_token()

        if token not in self._token_db:
            self._token_db[token] = list()
        self._token_db[token].append({
            "username": username,
            "entry_time": now,
        })

    def get_token_data(self, token):
        if token not in self._token_db:
            return None

        token_dict = self._token_db[token]
        now = time.time()
        if (now - token_dict["entry_time"]) > self._token_ttl:
            # token no longer valid
            del self._token_db[token]
            return None

        return token_dict
