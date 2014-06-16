# coding: utf-8
import datetime
import feedparser
import threading
import leselys
import copy
import requests

try:
    from urlparse import urlparse
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urlparse
    from urllib.parse import urljoin

from leselys.helpers import get_datetime
from leselys.helpers import get_dicttime
from leselys.feed_finder import FeedFinder

feedparser.USER_AGENT = "Leselys/%s +https://github.com/socketubs/leselys" % leselys.__version__
storage = leselys.core.storage
config = leselys.core.config

#########################################################################
# Set defaults settings
#########################################################################
if not storage.get_setting('acceptable_elements'):
    storage.set_setting('acceptable_elements', ["object", "embed", "iframe"])

# Acceptable elements are special tag that you can disable in entries rendering
acceptable_elements = storage.get_setting('acceptable_elements')

for element in acceptable_elements:
    feedparser._HTMLSanitizer.acceptable_elements.add(element)

#########################################################################
# Retriever object
#########################################################################


class Retriever(threading.Thread):
    """
    The Retriever object has to retrieve all feeds asynchronously and
    return it to the Reader when a new subscription arrives
    """

    def __init__(self, feed, feed_from_db=None, do_retention=True):
        threading.Thread.__init__(self)
        # self.feed is raw parsed feed
        self.data = feed['entries']
        self.do_retention = do_retention

        if feed_from_db:
            self.title = feed_from_db.get('title')
        else:
            self.title = feed['feed']['title']

    def run(self):
        # This feed comes from database
        feed = storage.get_feed_by_title(self.title)
        feed_id = feed.get('_id')

        for entry in self.data:
            title = entry.get('title')
            link = entry.get('link')
            guid = entry.get('guid') or entry.get('id') or title

            if storage.get_story_by_guid(feed_id, guid):
                storage.remove_story(storage.get_story_by_guid(feed_id, guid).get('_id'))

            try:
                description = entry['content'][0]['value']
            except KeyError:
                description = entry['summary']

            if entry.get('updated_parsed'):
                last_update = get_datetime(entry.updated_parsed)
            else:
                last_update = datetime.datetime.now()
            if entry.get('published_parsed', False):
                published = get_datetime(entry.published_parsed)
            else:
                published = datetime.datetime.now()

            if self.do_retention:
                delta = datetime.datetime.now() - published
                if delta.days > int(config.get('worker', 'retention')):
                    continue

            storage.add_story({
                'title': title,
                'guid': guid,
                'link': link,
                'description': description,
                'published': published,
                'last_update': last_update,
                'feed_id': feed_id,
                'read': False})


class Refresher(threading.Thread):
    """
    The Refresher object have to retrieve all new entries asynchronously
    """

    def __init__(self, feed):
        threading.Thread.__init__(self)
        self.feed = feed
        self.feed_id = feed.get('_id')
        self.feed_title = feed.get('title')

    def run(self):
        self.data = feedparser.parse(self.feed.get('url'))
        if self.data.get('bozo_exception', False):
            print("!! Can't retrieve %s feed (%s)" % (self.feed_title.encode('utf-8'), self.data['bozo_exception']))
            return

        need_update = False
        # Update title if it change
        if self.data.feed.get('title') != self.feed_title:
            self.feed['title'] = self.data.feed.get('title')
            self.feed_title = self.feed['title']
            need_update = True
        # Add website url if not setted
        if self.data.feed.get('link') != self.feed.get('link'):
            self.feed['link'] = self.data.feed.get('link')
            self.feed_link = self.feed['link']
            need_update = True

        if need_update:
            storage.update_feed(self.feed_id, copy.copy(self.feed))

        local_update = self.feed.get('last_update')
        remote_update = False
        if self.data.feed.get('updated_parsed'):
            remote_update = get_datetime(self.data.feed.updated_parsed)
        if self.data.get('updated_parsed'):
            if remote_update:
                if get_datetime(self.data.updated_parsed) > remote_update:
                    remote_update = get_datetime(self.data.updated_parsed)
            else:
                remote_update = get_datetime(self.data.updated_parsed)
        if self.data.feed.get('published_parsed'):
            if remote_update:
                if get_datetime(self.data.feed.published_parsed) > remote_update:
                    remote_update = get_datetime(self.data.feed.published_parsed)
            else:
                remote_update = get_datetime(self.data.feed.published_parsed)
        if self.data.get('published_parsed'):
            if remote_update:
                if get_datetime(self.data.published_parsed) > remote_update:
                    remote_update = get_datetime(self.data.published_parsed)
            else:
                remote_update = get_datetime(self.data.published_parsed)

        if not remote_update:
            remote_update = datetime.datetime.now()

        if remote_update > local_update:
            print('!! %s is outdated.' % self.feed_title.encode('utf-8'))
            readed = []
            for entry in storage.get_stories(self.feed_id, "published", 0, 0):
                if entry.get('read'):
                    readed.append(entry.get('guid'))

            if len(self.data.entries) <= int(config.get('worker', 'story_before_retention')):
                do_retention = False
            else:
                do_retention = True

            retriever = Retriever(self.data, self.feed, do_retention=do_retention)
            retriever.start()
            retriever.join()

            for entry_guid in readed:
                entry = storage.get_story_by_guid(self.feed_id, entry_guid)
                if entry:
                    # print(' _ update: %s' % entry['title'].encode('utf-8'))
                    entry['read'] = True
                    storage.update_story(entry['_id'], copy.copy(entry))

            self.feed['last_update'] = remote_update
            storage.update_feed(self.feed_id, self.feed)

        else:
            print('=> %s is up-to-date.' % self.feed_title.encode('utf-8'))

#########################################################################
# Reader object
#########################################################################


class Reader(object):
    """The Reader object is the feeds manager, it handles all
    new feed, read/unread state and refresh feeds
    """

    def get_feed(self, url):
        """Given url might be point to http document or to actual feed. In case
        of http document, we try to find first feed auto discovery url.
        """
        stripped = url.strip()

        try:
            resp = requests.get(stripped)
        except Exception as err:
            return {'success': False, 'output': str(err)}

        feed = feedparser.parse(resp.text)
        if feed.version != '':
            return {'success': True, 'output': (feed, stripped)}

        urls = FeedFinder.parse(resp.text)
        feed_url = ''
        if len(urls) > 0:
            # Each url is tuple where href is first element.
            # NOTE : Sites might have several feeds available and we are just
            # naively picking first one found.
            feed_url = urls[0][0]
            if urlparse(feed_url)[1] == '':
                # We have empty 'netloc', meaning we have relative url
                feed_url = urljoin(stripped, feed_url)
        return {'success': True, 'output': (feedparser.parse(feed_url), feed_url)}

    def add(self, url):
        feed_guesser = self.get_feed(url)
        if feed_guesser['success']:
            feed, url = feed_guesser['output']
        else:
            return feed_guesser

        # Bad feed
        if feed.version == '' or not feed.feed.get('title'):
            return {'success': False, 'output': 'Bad feed'}

        title = feed.feed['title']
        link = feed.feed['link']
        feed_id = storage.get_feed_by_title(title)
        if not feed_id:
            if feed.feed.get('updated_parsed'):
                feed_update = get_datetime(feed.feed.updated_parsed)
            elif feed.get('updated_parsed'):
                feed_update = get_datetime(feed.updated_parsed)
            elif feed.feed.get('published_parsed'):
                feed_update = get_datetime(feed.feed.published_parsed)
            elif feed.get('published_parsed'):
                feed_update = get_datetime(feed.published_parsed)
            else:
                feed_update = datetime.datetime.now()

            feed_id = storage.add_feed({'url': url,
                                        'title': title,
                                        'link': link,
                                        'last_update': feed_update})
        else:
            return {'success': False, 'output': 'Feed already exists'}

        retriever = Retriever(feed, do_retention=False)
        retriever.start()

        return {
            'success': True,
            'title': title,
            'url': url,
            'link': link,
            'feed_id': feed_id,
            'output': 'Feed added',
            'counter': len(feed['entries'])}

    def delete(self, feed_id):
        if not storage.get_feed_by_id(feed_id):
            return {'success': False, "output": "Feed not found"}
        storage.remove_feed(feed_id)
        return {"success": True, "output": "Feed removed"}

    def get(self, feed_id=False, feed_type="combined-feed", order_type="user", start=0, stop=50):
        # Special feeds
        if not feed_id:
            if feed_type == "combined-feed":
                if order_type == "user" or order_type not in ['unreaded', 'published']:
                    order_type = storage.get_feed_setting('combined-feed', 'ordering')
                    if not order_type:
                        storage.set_feed_setting('combined-feed', 'ordering', 'unreaded')
                        order_type = 'unreaded'
                    else:
                        order_type = order_type['value']
            elif feed_type == "stared-feed":
                if order_type == "user" or order_type not in ['unreaded', 'published']:
                    order_type = storage.get_feed_setting('stared-feed', 'ordering')
                    if not order_type:
                        storage.set_feed_setting('stared-feed', 'ordering', 'unreaded')
                        order_type = 'unreaded'
                    else:
                        order_type = order_type['value']
            else:
                raise Exception('Unknown feed type (%s)' % feed_type)
        # Normal feed
        else:
            if order_type == "user" or order_type not in ['unreaded', 'published']:
                order_type = storage.get_feed_setting(feed_id, 'ordering')
                if not order_type:
                    storage.set_feed_setting(feed_id, 'ordering', 'unreaded')
                    order_type = 'unreaded'
                else:
                    order_type = order_type['value']

        # Get stories
        if not feed_id:
            if feed_type == "combined-feed":
                stories = storage.all_stories(order_type, start, stop)
            elif feed_type == "stared-feed":
                stories = storage.all_stared(order_type, start, stop)
            else:
                raise Exception('Unknown feed type (%s)' % feed_type)
        else:
            stories = storage.get_stories(feed_id, order_type, start, stop)

        length = storage.get_feed_unread_count(feed_id)
        res = []
        for story in stories:
            story['last_update'] = get_dicttime(story['last_update'])
            story['published'] = get_dicttime(story['published'])
            res.append(story)

        return {'entries': res, 'ordering': order_type, 'detail': {'start': start, 'stop': stop, 'length': length}}

    def get_combined_feed(self):
        order_type = storage.get_feed_setting('combined-feed', 'ordering')
        if not order_type:
            storage.set_feed_setting('combined-feed', 'ordering', 'unreaded')
            order_type = storage.get_feed_setting('combined-feed', 'ordering')
        return {'title': 'All stories',
                'id': 'combined_feed',
                'counter': self.get_unread(),
                'ordering': order_type}

    def get_feeds(self):
        feeds = []
        for feed in storage.get_feeds():
            feed_id = feed.get('_id')
            ordering = storage.get_feed_setting(feed_id, 'ordering')
            if not ordering:
                storage.set_feed_setting(feed_id, 'ordering', 'unreaded')
                ordering = storage.get_feed_setting(feed_id, 'ordering')

            ordering = ordering['value']

            feeds.append({'title': feed.get('title'),
                          'id': feed_id,
                          'url': feed.get('url'),
                          'link': feed.get('link', feed.get('url')),
                          'counter': self.get_unread(feed['_id']),
                          'ordering': ordering
                          })
        return sorted(feeds, key=lambda k: k['title'].lower())
        #return feeds

    def refresh(self, feed_id):
        feed = storage.get_feed_by_id(feed_id)
        refresher = Refresher(feed)
        refresher.start()
        refresher.join()
        feed['counter'] = self.get_unread(feed_id)
        return {'success': True, 'content': feed}

    def get_unread(self, feed_id=False):
        if not feed_id:
            return storage.get_feed_unread_count()
        return storage.get_feed_unread_count(feed_id)

    def mark_all_read(self, feed_id):
        if feed_id == "combined-feed":
            stories = storage.all_stories('unreaded', 0, 0)
        else:
            stories = storage.get_stories(feed_id, 'unreaded', 0, 0)

        for story in stories:
            story['read'] = True
            storage.update_story(story['_id'], copy.copy(story))
        return {'success': True, "content": "All feed stories updated"}

    def mark_all_unread(self, feed_id):
        for story in storage.get_stories(feed_id, 'unreaded', 0, 0):
            story['read'] = False
            storage.update_story(story['_id'], copy.copy(story))
        return {'success': True, "content": "All feed stories updated"}

    def read(self, story_id):
        """
        Return story content, set it at readed state and give
        previous read state for counter
        """
        story = storage.get_story_by_id(story_id)
        if story['read']:
            story['published'] = get_dicttime(story['published'])
            story['last_update'] = get_dicttime(story['last_update'])
            return {'success': False,
                    'output': 'Story already readed',
                    'content': story}

        # Save read state before update it for javascript counter in UI
        story['read'] = True
        storage.update_story(story['_id'], copy.copy(story))

        story['published'] = get_dicttime(story['published'])
        story['last_update'] = get_dicttime(story['last_update'])

        return {'success': True, 'content': story}

    def unread(self, story_id):
        story = storage.get_story_by_id(story_id)
        if not story['read']:
            story['published'] = get_dicttime(story['published'])
            story['last_update'] = get_dicttime(story['last_update'])
            return {'success': False, 'output': 'Story already unreaded'}
        story['read'] = False
        storage.update_story(story['_id'], copy.copy(story))

        story['published'] = get_dicttime(story['published'])
        story['last_update'] = get_dicttime(story['last_update'])

        return {'success': True, 'content': story}
