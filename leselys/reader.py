# coding: utf-8
import datetime
import feedparser
import threading
import leselys
import copy

from leselys.helpers import u
from leselys.helpers import get_datetime
from leselys.helpers import get_dicttime

backend = leselys.core.backend

#########################################################################
# Set defaults settings
#########################################################################
if not backend.get_setting('acceptable_elements'):
    backend.set_setting('acceptable_elements', ["object", "embed", "iframe"])

# Acceptable elements are special tag that you can disable in entries rendering
acceptable_elements = backend.get_setting('acceptable_elements')

for element in acceptable_elements:
    feedparser._HTMLSanitizer.acceptable_elements.add(element)

#########################################################################
# Retriever object
#########################################################################


class Retriever(threading.Thread):
    """The Retriever object has to retrieve all feeds asynchronously and
    return it to the Reader when a new subscription arrives
    """

    def __init__(self, feed):
        threading.Thread.__init__(self)
        # self.feed is raw parsed feed
        self.feed = feed
        self.title = feed.feed['title']
        self.data = feed['entries']

    def run(self):
        # This feed comes from database
        feed = backend.get_feed_by_title(self.title)

        for entry in self.data:
            title = entry['title']
            link = entry['link']
            try:
                description = entry['content'][0]['value']
            except KeyError:
                description = entry['summary']

            if entry.get('updated_parsed'):
                last_update = get_dicttime(entry.updated_parsed)
            else:
                last_update = get_dicttime(datetime.datetime.now().timetuple())

            if entry.get('published_parsed', False):
                published = get_dicttime(entry.published_parsed)
            else:
                published = get_dicttime(datetime.datetime.now().timetuple())

            backend.add_story({
                'title': title,
                'link': link,
                'description': description,
                'published': published,
                'last_update': last_update,
                'feed_id': feed['_id'],
                'read': False})


class Refresher(threading.Thread):
    """The Refresher object have to retrieve all new entries asynchronously
    """

    def __init__(self, feed):
        threading.Thread.__init__(self)
        self.feed = feed
        self.feed_id = u(feed['_id'])

    def run(self):
        self.data = feedparser.parse(self.feed['url'])

        local_update = get_datetime(self.feed['last_update'])
        if self.data.feed.get('updated_parsed'):
            remote_update = get_datetime(self.data.feed.updated_parsed)
            remote_update_raw = get_dicttime(self.data.feed.updated_parsed)
        elif self.data.get('updated_parsed'):
            remote_update = get_datetime(self.data.updated_parsed)
            remote_update_raw = get_dicttime(self.data.updated_parsed)
        elif self.data.feed.get('published_parsed'):
            remote_update = get_datetime(self.data.feed.published_parsed)
            remote_update_raw = get_dicttime(self.data.feed.published_parsed)
        elif self.data.get('published_parsed'):
            remote_update = get_datetime(self.data.published_parsed)
            remote_update_raw = get_dicttime(self.data.published_parsed)
        else:
            remote_update = datetime.datetime.now()
            remote_update_raw = get_dicttime(remote_update.timetuple())

        if remote_update > local_update:
            print(':: %s is outdated' % self.feed['title'])
            readed = []
            for entry in backend.get_stories(self.feed['_id']):
                if entry['read']:
                    readed.append(entry['title'])
                backend.remove_story(entry['_id'])

            retriever = Retriever(self.data)
            retriever.start()
            retriever.join()

            for entry in readed:
                if backend.get_story_by_title(entry):
                    entry = backend.get_story_by_title(entry)
                    entry['read'] = True
                    backend.update_story(entry['_id'], copy.copy(entry))

            self.feed['last_update'] = remote_update_raw
            backend.update_feed(self.feed_id, self.feed)

#########################################################################
# Reader object
#########################################################################


class Reader(object):
    """The Reader object is the subscriptions manager, it handles all
    new feed, read/unread state and refresh feeds
    """

    def add(self, url):
        url = url.strip()
        feed = feedparser.parse(url)

        # Bad feed
        if not feed.feed.get('title', False):
            return {'success': False, 'output': 'Bad feed'}

        title = feed.feed['title']

        feed_id = backend.get_feed_by_title(title)
        if not feed_id:
            if feed.feed.get('updated_parsed'):
                feed_update = get_dicttime(feed.feed.updated_parsed)
            elif feed.get('updated_parsed'):
                feed_update = get_dicttime(feed.updated_parsed)
            elif feed.feed.get('published_parsed'):
                feed_update = get_dicttime(feed.feed.published_parsed)
            elif feed.get('published_parsed'):
                feed_update = get_dicttime(feed.published_parsed)
            else:
                feed_update = get_dicttime(datetime.datetime.now().timetuple())

            feed_id = backend.add_feed({'url': url,
                                        'title': title,
                                        'last_update': feed_update})
        else:
            return {'success': False, 'output': 'Feed already exists'}

        retriever = Retriever(feed)
        retriever.start()

        return {
            'success': True,
            'title': title,
            'feed_id': feed_id,
            'output': 'Feed added',
            'counter': len(feed['entries'])}

    def delete(self, feed_id):
        if not backend.get_feed_by_id(feed_id):
            return {'success': False, "output": "Feed not found"}
        backend.remove_feed(feed_id)
        return {"success": True, "output": "Feed removed"}

    def get(self, feed_id, order_type='normal'):
        res = []
        for entry in backend.get_stories(feed_id):
            res.append({
                "title": entry['title'],
                "_id": entry['_id'],
                "read": entry['read'],
                'last_update': entry['last_update']})

        # Must implement different order_type

        # Readed
        readed = []
        for entry in res:
            if entry['read']:
                readed.append(entry)
        readed.sort(key=lambda r: get_datetime(r['last_update']), reverse=True)
        # Unread
        unreaded = []
        for entry in res:
            if not entry['read']:
                unreaded.append(entry)
        unreaded.sort(key=lambda r: get_datetime(r['last_update']),
                      reverse=True)
        return unreaded + readed

    def get_subscriptions(self):
        feeds = []
        for feed in backend.get_feeds():
            feeds.append({'title': feed['title'],
                          'id': feed['_id'],
                          'counter': self.get_unread(feed['_id'])
                          })
        return feeds

    def refresh_all(self):
        for subscription in backend.get_feeds():
            refresher = Refresher(subscription)
            refresher.start()
        return []

    def get_unread(self, feed_id):
        return len(backend.get_feed_unread(feed_id))

    def read(self, story_id):
        """
        Return story content, set it at readed state and give
        previous read state for counter
        """
        story = backend.get_story_by_id(story_id)
        if story['read']:
            return {'success': False,
                    'output': 'Story already readed',
                    'content': story}

        # Save read state before update it for javascript counter in UI
        story['read'] = True
        backend.update_story(story['_id'], copy.copy(story))
        return {'success': True, 'content': story}

    def unread(self, story_id):
        story = backend.get_story_by_id(story_id)
        if not story['read']:
            return {'success': False, 'output': 'Story already unreaded'}
        story['read'] = False
        backend.update_story(story['_id'], copy.copy(story))
        return {'success': True, 'content': story}
