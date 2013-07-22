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

    def add_feed(self, content):
        raise NotImplementedError

    def add_story(self, content):
        raise NotImplementedError

    def all_stories(self, ordering, start, stop):
        raise NotImplementedError

    def get_feed_by_id(self, id):
        raise NotImplementedError

    def get_feed_by_title(self, title):
        raise NotImplementedError

    def get_feed_by_title(self, title):
        raise NotImplementedError

    def get_feed_count(self, feed_id=False):
        raise NotImplementedError

    def get_feed_setting(self, feed_id, setting_type):
        raise NotImplementedError

    def get_feed_unread(self, feed_id):
        raise NotImplementedError

    def get_feed_unread_count(self, feed_id=False):
        raise NotImplementedError

    def get_feeds(self):
        raise NotImplementedError

    def get_password(self):
        raise NotImplementedError

    def get_setting(self, key):
        raise NotImplementedError

    def get_settings(self):
        raise NotImplementedError

    def get_stories(self, feed_id, ordering, start, stop):
        raise NotImplementedError

    def get_story_by_guid(self, feed_id, guid):
        raise NotImplementedError

    def get_story_by_id(self, _id):
        raise NotImplementedError

    def get_story_by_title(self, feed_id, title):
        raise NotImplementedError

    def remove_feed(self, _id):
        raise NotImplementedError

    def remove_story(self, _id):
        raise NotImplementedError

    def set_feed_setting(self, feed_id, setting_type, value):
        raise NotImplementedError

    def set_password(self, password):
        raise NotImplementedError

    def set_setting(self, key, value):
        raise NotImplementedError

    def update_feed(self, _id, content):
        raise NotImplementedError

    def update_story(self, _id, content):
        raise NotImplementedError

