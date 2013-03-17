# coding: utf-8
import feedparser
import threading
import leselys
import copy

from leselys.helpers import u
from leselys.helpers import get_datetime
from leselys.helpers import get_dicttime

backend = leselys.core.backend

####################################################################################
# Set defaults settings
####################################################################################
if not backend.get_setting('acceptable_elements'):
    backend.set_setting('acceptable_elements', ["object", "embed", "iframe"])

# Acceptable elements are special tag that you can disable in entries rendering
acceptable_elements = backend.get_setting('acceptable_elements')

for element in acceptable_elements:
    feedparser._HTMLSanitizer.acceptable_elements.add(element)

####################################################################################
# Retriever object
####################################################################################
class Retriever(threading.Thread):
    """ The Retriever object have to retrieve all feeds asynchronously and return it to
    the Reader when a new subscription arrived """

    def __init__(self, title, data=None):
        threading.Thread.__init__(self)
        self.title = title
        self.data = data

    def run(self):
        feed = backend.get_feed_by_title(self.title)
        feed_id = u(feed['_id'])

        if self.data is None:
            url = feed['url']
            self.data = feedparser.parse(url)['entries']

        for entry in self.data:
            title = entry['title']
            link = entry['link']
            print('Add -> %s' % title)
            try:
                description = entry['content'][0]['value']
            except KeyError:
                description = entry['summary']

            last_update = get_dicttime(entry.updated_parsed)

            if entry.get('published_parsed', False):
                published = get_dicttime(entry.published_parsed)
            else:
                published = None

            _id = backend.add_story({
                    'title':title,
                    'link':link,
                    'description':description,
                    'published':published,
                    'last_update':last_update,
                    'feed_id':feed_id,
                    'read':False})

class Refresher(threading.Thread):
    """ The Refresher object have to retrieve all new entries asynchronously """

    def __init__(self, feed):
        threading.Thread.__init__(self)
        self.feed = feed
        self.feed_id = u(feed['_id'])

    def run(self):
        print('Checking %s feed' % self.feed['_id'])
        self.data = feedparser.parse(self.feed['url'])

        local_update = get_datetime(self.feed['last_update'])
        if self.data.feed.get('updated_parsed'):
            remote_update = get_datetime(self.data.feed.updated_parsed)
        elif self.data.get('updated_parsed'):
            remote_update = get_datetime(self.data.updated_parsed)
        elif self.data.feed.get('published_parsed'):
            remote_update = get_datetime(self.data.feed.published_parsed)
        elif self.data.get('published_parsed'):
            remote_update = get_datetime(self.data.published_parsed)
        else:
            return

        print(':: %s' % self.feed['title'])
        if remote_update > local_update:
            readed = []
            for entry in backend.get_stories(self.feed['_id']):
                print('!!! 1')
                if entry['read']:
                    print('!!! 2')
                    readed.append(entry['title'])
                backend.remove_story(entry['_id'])

            retriever = Retriever(title=self.feed['title'], data=self.data.entries)
            retriever.start()
            retriever.join()

            for entry in readed:
                print('!!! 3')
                if backend.get_story_by_title(entry):
                    print('!!! 4')
                    entry = backend.get_story_by_title(entry)
                    entry['read'] = True
                    backend.update_story(entry['_id'], copy.copy(entry))

####################################################################################
# Reader object
####################################################################################
class Reader(object):
    """ The Reader object is the subscriptions manager, it handle all new feed, read/unread
    state and refresh feeds"""

    def add(self, url):
        url = url.strip()
        r = feedparser.parse(url)

        # Bad feed
        if not r.feed.get('title', False):
            return {'success': False, 'output':'Bad feed'}

        title = r.feed['title']

        feed_id = backend.get_feed_by_title(title)
        if not feed_id:
            if r.feed.get('updated_parsed'):
                feed_update = get_dicttime(r.feed.updated_parsed)
            elif r.get('updated_parsed'):
                feed_update = get_dicttime(r.updated_parsed)
            elif r.feed.get('published_parsed'):
                feed_update = get_dicttime(r.feed.published_parsed)
            elif r.get('published_parsed'):
                feed_update = get_dicttime(r.published_parsed)
            else:
                return {'success':False, 'output':'Parsing error'}
            feed_id = backend.add_feed({'url':url, 'title': title, 'last_update': feed_update})
        else:
            return {'success':False, 'output':'Feed already exists'}

        retriever = Retriever(title=title, data=r['entries'])
        retriever.start()

        return {
            'success': True,
            'title': title,
            'feed_id': feed_id,
            'output': 'Feed added',
            'counter': len(r['entries'])}

    def delete(self, feed_id):
        if not backend.get_feed_by_id(feed_id):
            return {'success': False, "output": "Feed not found"}
        backend.remove_feed(feed_id)
        return {"success": True, "output": "Feed removed"}

    def get(self, feed_id):
        res = []
        for entry in backend.get_stories(feed_id):
            print('===')
            print(entry)
            print('===')
            res.append({"title":entry['title'],"_id":entry['_id'],"read":entry['read']})
        return res

    def get_subscriptions(self):
        feeds = []
        for feed in backend.get_feeds():
            feeds.append({'title':feed['title'],'id':feed['_id'], 'counter':self.get_unread(feed['_id'])})
        return feeds

    def refresh_all(self):
        feeds_id = []
        for subscription in backend.get_feeds():
            refresher = Refresher(subscription)
            refresher.start()    
        return []

    def get_unread(self, feed_id):
        return len(backend.get_feed_unread(feed_id))

    def read(self, entry_id):
        """
        Return entry content, set it at readed state and give
        previous read state for counter
        """
        entry = backend.get_story_by_id(entry_id)

        # Save read state before update it for javascript counter in UI
        entry['last_read_state'] = entry['read']
        entry['read'] = True
        backend.update_story(entry['_id'], copy.copy(entry))
        print('!!!!')
        print(entry)
        print('!!!!')
        return entry

    def unread(self, story_id):
        story = backend.get_story_by_id(story_id)
        story['read'] = False
        backend.update_story(story['_id'], copy.copy(story))
        return True
