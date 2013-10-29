# -*- coding: utf-8 -*-
from sofart import Database
from leselys.backends.storage._storage import Storage

import sys

print("Don't use sofart backend, totaly not usable.")
sys.exit(1)


class Sofart(Storage):
    def __init__(self, **kwargs):
        self.path = kwargs['path']
        self.mode = kwargs['mode']
        self.db = Database(self.path, self.mode)

    def get_password(self):
        password = self.get_setting('password')
        if password:
            return password
        return False

    def set_password(self, password):
        return self.set_setting('password', self._hash_string(password))

    def set_feed_setting(self, feed_id, setting_type, value):
        setting = self.db.feedsettings.find_one({'feed_id': feed_id, 'setting_type': setting_type})
        if setting:
            self.db.feedsettings.remove(setting['_id'])
        self.db.feedsettings.save({'feed_id': feed_id, 'setting_type': setting_type, 'value': value})

    def get_feed_setting(self, feed_id, setting_type):
        return self.db.feedsettings.find_one({'feed_id': feed_id, 'setting_type': setting_type})

    def set_setting(self, key, value):
        self.db.settings.save({key: value})

    def get_setting(self, key):
        setting = self.db.settings.find_one({key: {'$exists': True}})
        if setting:
            return setting[key]
        return False

    def get_settings(self):
        settings = {}
        for setting in self.db.settings.find():
            settings.update(setting)
        del settings['_id']
        return settings

    def add_feed(self, content):
        return self.db.feeds.save(content)

    def remove_feed(self, _id):
        self.db.feeds.remove(_id)
        for entry in self.db.stories.find({'feed_id': _id}):
            self.db.stories.remove(entry['_id'])
        for setting in self.db.feedsettings.find({'feed_id': _id}):
            self.db.feedsettings.remove(setting['_id'])

    def get_feed_by_id(self, _id):
        return self.db.feeds.find_one({'_id': _id})

    def get_feed_by_title(self, title):
        return self.db.feeds.find_one({'title': title})

    def update_feed(self, _id, content):
        self.db.feeds.remove(_id)
        return self.db.feeds.save(content)

    def get_feeds(self):
        res = []
        for feed in self.db.feeds.find():
            res.append(feed)
        return res

    def all_stories(self):
        res = []
        feeds = {}
        for feed in self.db.feeds.find():
            feeds[feed['_id']] = feed['title']

        for story in self.db.stories.find():
            story['_id'] = story['_id']
            story['feed_title'] = feeds[story['feed_id']]
            res.append(story)
        return res

    def add_story(self, content):
        return self.db.stories.save(content)

    def remove_story(self, _id):
        self.db.stories.remove(_id)

    def update_story(self, _id, content):
        self.db.stories.remove(_id)
        return self.db.stories.save(content)

    def get_story_by_id(self, _id):
        return self.db.stories.find_one({'_id': _id})

    def get_story_by_title(self, feed_id, title):
        return self.db.stories.find_one({'title': title, 'feed_id': feed_id})

    def get_feed_unread(self, feed_id):
        res = []
        for feed in self.db.stories.find({'feed_id': feed_id, 'read': False}):
            res.append(feed)
        return res

    def get_stories(self, feed_id):
        res = []
        for story in self.db.stories.find({'feed_id': feed_id}):
            res.append(story)
        return res
