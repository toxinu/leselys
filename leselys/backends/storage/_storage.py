# -*- coding: utf-8 -*-
import bcrypt


class Storage(object):
    def _hash_string(self, string):
        return bcrypt.hashpw(string, bcrypt.gensalt())

    def is_valid_login(self, username, password):
        """
        Check if username/password combination is valid login.

        username : plaintext username
        password : plaintext password
        """
        if username in self.get_users():
            stored = self.get_password(username)
            if bcrypt.hashpw(password, stored) == stored:
                return True
        else:
            return False

    def create_user(self, username, password):
        """
        Create new user to DB. Hashes password with bcrypt.

        username : plaintext username
        password : plaintext password
        """
        hashed = self._hash_string(password)
        return self.add_user(username, hashed)

    def update_password(self, username, password):
        """
        Update password for given username. Hashes password with bcrypt.

        username : plaintext username
        password : plaintext password
        """
        hashed = self._hash_string(password)
        return self.set_password(username, hashed)
