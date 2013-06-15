# -*- coding: utf-8 -*-
import bcrypt


class Storage(object):
    def _hash_string(self, string):
        return bcrypt.hashpw(string, bcrypt.gensalt())

    def is_valid_password(self, password):
        """
        Check if password is valid.

        password : plaintext password
        """
        password = password
        stored = self.get_password()
        if not stored:
            return False
        if bcrypt.hashpw(password, stored) == stored:
            return True
        return False

    def update_password(self, password):
        """
        Update password. Hashes password with bcrypt.

        password : plaintext password
        """
        hashed = self._hash_string(password)
        return self.set_password(hashed)
