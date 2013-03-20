# -*- coding: utf-8 -*-
import hashlib

class Storage(object):
    def _hash_string(self, string):
            m = hashlib.md5()
            m.update(string)
            return m.hexdigest()

    def is_valid_login(self, username, password):
        """
        Check if username/password combinatin is valid login.

        username : plaintext username
        password : plaintext password
        """
        if username in self.get_users():
            hashed = self._hash_string(password)
            if hashed == self.get_password(username):
                return True
        else:
            return False

    def create_user(self, username, password):
        """
        Create new user to DB. Hashes password.

        username : plaintext username
        password : plaintext password
        """
        hashed = self._hash_string(password)
        return self.add_user(username, hashed)

    def update_password(self, username, new_password):
        """
        Update password for given username. Hashes password.

        username : plaintext username
        password : plaintext password
        """
        hashed = self._hash_string(password)
        return self.set_password(username, hashed)

