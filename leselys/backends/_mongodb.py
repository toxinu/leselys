# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bson.objectid import ObjectId


class Backend(object):
    def __init__(self, **kwargs):
        self.database = kwargs.get('database') or 'leselys'

        if kwargs.get('database'):
            del kwargs['database']
        self.connection = MongoClient(**kwargs)

        self.db = self.connection[self.database]

    def get_users(self):
        res = []
        for user in self.db.users.find():
            res.append(user['username'])
        return res

    def add_user(self, username, password):
        return str(self.db.users.save({'username': username,
                                       'password': password}))

    def remove_user(self, username):
        user = self.db.users.find_one({'username': username})
        if user:
            self.db.users.remove(user['_id'])

    def get_password(self, username):
        user = self.db.users.find_one({'username': username})
        if user:
            return user['password']
        return None

    def set_password(self, username, password):
        self.remove_user(username)
        return str(self.db.users.save({'username': username,
                                       'password': password}))

    def set_setting(self, key, value):
        return str(self.db.settings.save({key: value}))

    def get_setting(self, key):
        if not self.db.settings.find_one():
            return False
        if not self.db.settings.find_one().get(key, False):
            return False
        else:
            setting = self.db.settings.find_one()[key]
            return setting

    def get_settings(self):
        settings = {}
        for setting in self.db.settings.find():
            settings.update(setting)
        if settings:
            del settings['_id']
        return settings

    def add_feed(self, content):
        return str(self.db.feeds.save(content))

    def remove_feed(self, _id):
        self.db.feeds.remove(ObjectId(_id))
        for entry in self.db.stories.find({'feed_id': _id}):
            self.db.stories.remove(entry['_id'])

    def get_feed_by_id(self, _id):
        feed = self.db.feeds.find_one(ObjectId(_id))
        if feed:
            feed['_id'] = str(feed['_id'])
        return feed

    def get_feed_by_title(self, title):
        feed = self.db.feeds.find_one({'title': title})
        if feed:
            feed['_id'] = str(feed['_id'])
        return feed

    def update_feed(self, _id, content):
        self.db.feeds.remove(ObjectId(_id))
        if content['_id']:
            if not isinstance(content['_id'], ObjectId):
                try:
                    content['_id'] = ObjectId(content['_id'])
                except:
                    raise Exception('Update feed failed, cant find _id')
        return str(self.db.feeds.save(content))

    def get_feeds(self):
        res = []
        for feed in self.db.feeds.find():
            feed['_id'] = str(feed['_id'])
            res.append(feed)
        return res

    def add_story(self, content):
        return str(self.db.stories.save(content))

    def remove_story(self, _id):
        self.db.stories.remove(ObjectId(_id))

    def update_story(self, _id, content):
        self.db.stories.remove(ObjectId(_id))
        if content['_id']:
            if not isinstance(content['_id'], ObjectId):
                try:
                    content['_id'] = ObjectId(content['_id'])
                except:
                    raise Exception('Update story failed, cant find _id')
        return str(self.db.stories.save(content))

    def get_story_by_id(self, _id):
        story = self.db.stories.find_one(ObjectId(_id))
        if story:
            story['_id'] = str(story['_id'])
        return story

    def get_story_by_title(self, title):
        story = self.db.stories.find_one({'title': title})
        if story:
            story['_id'] = str(story['_id'])
        return story

    def get_feed_unread(self, feed_id):
        res = []
        for feed in self.db.stories.find({'feed_id': feed_id, 'read': False}):
            feed['_id'] = str(feed['_id'])
            res.append(feed)
        return res

    def get_stories(self, feed_id):
        res = []
        for story in self.db.stories.find({'feed_id': feed_id}):
            story['_id'] = str(story['_id'])
            res.append(story)
        return res
