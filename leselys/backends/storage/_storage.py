# -*- coding: utf-8 -*-
import bcrypt


class Storage(object):
    def _hash_string(self, string):
        string = string.encode('utf-8')
        return bcrypt.hashpw(string, bcrypt.gensalt()).encode('utf-8')

    def is_valid_password(self, password):
        """
        Check if password is valid.

        password : plaintext password
        """
        password = password.encode('utf-8')
        stored = self.get_password().encode('utf-8')
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
