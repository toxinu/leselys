# -*- coding: utf-8 -*-

from pymongo import MongoClient
from bson.objectid import ObjectId
from leselys.backends.storage._storage import Storage


class Mongodb(Storage):
    def __init__(self, **kwargs):
        self.database = kwargs.get('database') or 'leselys'

        if kwargs.get('database'):
            del kwargs['database']
        self.connection = MongoClient(**kwargs)

        self.db = self.connection[self.database]

    def get_password(self):
        password = self.get_setting('password')
        if password:
            return password
        return False

    def set_password(self, password):
        return self.set_setting('password', self._hash_string(password))

    def set_feed_setting(self, feed_id, setting_type, value):
        setting = self.db.feedsettings.find_one({'feed_id': feed_id, 'setting_type': setting_type})
        if setting and setting.get('_id'):
            self.db.feedsettings.save({
                '_id': settings['_id'],
                'feed_id': feed_id,
                'setting_type': setting_type,
                'value': value
            })
        self.db.feedsettings.save({'feed_id': feed_id, 'setting_type': setting_type, 'value': value})


    def get_feed_setting(self, feed_id, setting_type):
        setting = self.db.feedsettings.find_one({'feed_id': feed_id, 'setting_type': setting_type})
        if setting:
            setting['_id'] = str(setting['_id'])
        return setting

    def set_setting(self, key, value):
        self.db.settings.remove({key: {'$exists': True}})
        return str(self.db.settings.save({key: value}))

    def get_setting(self, key):
        setting = self.db.settings.find_one({key: {'$exists': True}})
        if setting:
            return setting[key]
        return False

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
        for setting in self.db.feedsettings.find({'feed_id': _id}):
            self.db.feedsettings.remove(setting['_id'])

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

    def all_stories(self, ordering, start, stop):
        res = []
        feeds = {}
        for feed in self.db.feeds.find():
            feeds[str(feed['_id'])] = feed['title']

        if ordering == "unreaded":
            for story in self.db.stories.find({"read": False}).sort('last_update', -1).skip(start).limit(stop - start):
                story['_id'] = str(story['_id'])
                story['feed_title'] = feeds[story['feed_id']]
                res.append(story)
            nb_read = len(res)
            if (stop - start) - nb_read <= 0 and stop - start != 0:
                return res
            for story in self.db.stories.find({"read": True}).sort('last_update', -1).limit((stop - start) - nb_read):
                story['_id'] = str(story['_id'])
                story['feed_title'] = feeds[story['feed_id']]
                res.append(story)
        elif ordering == "published":
            for story in self.db.stories.find().sort('last_update', -1).skip(start).limit(stop - start):
                story['_id'] = str(story['_id'])
                story['feed_title'] = feeds[story['feed_id']]
                res.append(story)

        return res

    def add_story(self, content):
        return str(self.db.stories.save(content))

    def remove_story(self, _id):
        self.db.stories.remove(ObjectId(_id))

    def update_story(self, _id, content):
        if content['_id']:
            if not isinstance(content['_id'], ObjectId):
                try:
                    content['_id'] = ObjectId(content['_id'])
                except:
                    raise Exception('Update story failed, cant find _id')
        return str(self.db.stories.save(content))

    def get_story_by_guid(self, feed_id, guid):
        story = self.db.stories.find_one({'guid': guid, 'feed_id': feed_id})
        if story:
            story['_id'] = str(story['_id'])
        return story

    def get_story_by_id(self, _id):
        story = self.db.stories.find_one({'_id': ObjectId(_id)})
        if story:
            story['_id'] = str(story['_id'])
        return story

    def get_story_by_title(self, feed_id, title):
        story = self.db.stories.find_one({'title': title, 'feed_id': feed_id})
        if story:
            story['_id'] = str(story['_id'])
        return story

    def get_feed_unread(self, feed_id):
        res = []
        for feed in self.db.stories.find({'feed_id': feed_id, 'read': False}).sort('last_update', -1):
            feed['_id'] = str(feed['_id'])
            res.append(feed)
        return res

    def get_feed_unread_count(self, feed_id=False):
        if not feed_id:
            return self.db.stories.find({'read': False}).count()
        return self.db.stories.find({'feed_id': feed_id, 'read': False}).count()

    def get_stories(self, feed_id, ordering, start, stop):
        res = []
        if ordering == "unreaded":
            for story in self.db.stories.find({"feed_id": feed_id, "read": False}).sort('last_update', -1).skip(start).limit(stop - start):
                story['_id'] = str(story['_id'])
                res.append(story)
            nb_read = len(res)
            if (stop - start) - nb_read <= 0 and stop - start != 0:
                return res
            for story in self.db.stories.find({"feed_id": feed_id, "read": True}).sort('last_update', -1).limit((stop-start)-nb_read):
                story['_id'] = str(story['_id'])
                res.append(story)
        elif ordering == "published":
            for story in self.db.stories.find({"feed_id": feed_id}).sort('last_update', -1).skip(start).limit(stop - start):
                story['_id'] = str(story['_id'])
                res.append(story)

        return res
