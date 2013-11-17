# -*- coding: utf-8 -*-
import requests
import datetime
import feedparser

from django.conf import settings
from django.utils.timezone import utc

try:
    from HTMLParser import HTMLParser
except ImportError:
    from html.parser import HTMLParser

try:
    from urlparse import urlparse
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urlparse
    from urllib.parse import urljoin

FEEDPARSER_BOZO_EXCEPTION = settings.FEEDPARSER_BOZO_EXCEPTION
BLANK_FAVICON = settings.STATIC_URL + "img/blank_icon.gif"


def get_datetime(unparsed_date):
    if isinstance(unparsed_date, dict):
        return datetime.datetime(
            unparsed_date['year'],
            unparsed_date['month'],
            unparsed_date['day'],
            unparsed_date['hour'],
            unparsed_date['min'],
            tzinfo=utc)
    else:
        return datetime.datetime(
            unparsed_date[0],
            unparsed_date[1],
            unparsed_date[2],
            unparsed_date[3],
            unparsed_date[4],
            tzinfo=utc)


class FaviconFinder(HTMLParser):
    favicon_content_type = ['image/x-icon']

    def __init__(self):
        HTMLParser.__init__(self)
        self.favicon_url = BLANK_FAVICON

    def handle_starttag(self, tag, attrs):
        if tag != 'link':
            return

        # Favicon
        is_favicon = False
        for attr in attrs:
            if attr[0] == 'type' and \
                    (attr[1] in FaviconFinder.favicon_content_type) or \
                    attr[1] == 'shortcut icon':
                is_favicon = True
                break
        if is_favicon:
            for attr in attrs:
                if attr[0] == 'href' and attr[1]:
                    self.favicon_url = attr[1]

    @staticmethod
    def parse(html_document):
        """
        Find feed auto discovery links from html document.

        Returns list of tuples. Each tuple is form of (href, title). Title
        is empty string if not present.
        """
        parser = FaviconFinder()
        parser.feed(html_document)
        parser.close()
        return parser.favicon_url


class FeedFinder(HTMLParser):
    """
    HTML parser which collects all rss/atom auto discovery links.
    """
    # These are used to determine if <link> is feed auto discovery link
    feed_content_types = ['application/rss+xml', 'application/atom+xml']

    def __init__(self):
        HTMLParser.__init__(self)
        self.feeds = []

    def handle_starttag(self, tag, attrs):
        if tag != 'link':
            return

        href = ''
        title = ''
        is_feed = False
        for attr in attrs:
            if attr[0] == 'type' and attr[1] in FeedFinder.feed_content_types:
                is_feed = True
            if attr[0] == 'href':
                href = attr[1]
            if attr[0] == 'title':
                title = attr[1]
        if is_feed:
            self.feeds.append((href, title))

    @staticmethod
    def parse(html_document):
        """
        Find feed auto discovery links from html document.

        Returns list of tuples. Each tuple is form of (href, title). Title
        is empty string if not present.
        """
        parser = FeedFinder()
        parser.feed(html_document)
        parser.close()
        return parser.feeds


def get_feed_urls(url):
        """
        Given url might be point to http document or to actual feed. In case
        of http document, we try to find first feed auto discovery url.
        """
        stripped = url.strip()

        try:
            resp = requests.get(stripped)
        except Exception as err:
            return {'success': False, 'output': str(err)}

        feed = feedparser.parse(resp.text)
        if not feed.bozo or (
                feed.bozo_exception.__class__ in FEEDPARSER_BOZO_EXCEPTION.keys()):

            # Remove it cause it's not serializable
            if feed.get('bozo_exception', False):
                del feed["bozo_exception"]

            favicon_url = BLANK_FAVICON
            if feed.feed.get('link', False):
                resp = requests.get(feed.feed.get('link'))
                favicon_url = FaviconFinder.parse(resp.text)
                if favicon_url:
                    if urlparse(favicon_url)[1] == '':
                        favicon_url = urljoin(stripped, favicon_url)

            return {'success': True, 'output': (feed, stripped, favicon_url)}

        urls = FeedFinder.parse(resp.text)
        feed_url = u''
        if len(urls) > 0:
            # Each url is tuple where href is first element.
            # NOTE : Sites might have several feeds available and we are just
            # naively picking first one found.
            feed_url = urls[0][0]
            if urlparse(feed_url)[1] == '':
                # We have empty 'netloc', meaning we have relative url
                feed_url = urljoin(stripped, feed_url)
        if not feed_url:
            return {'success': False, 'output': "Can't find any rss links."}

        favicon_url = FaviconFinder.parse(resp.text)
        if favicon_url:
            if favicon_url != BLANK_FAVICON:
                if urlparse(favicon_url)[1] == "":
                    favicon_url = urljoin(stripped, favicon_url)

        return {'success': True,
                'output': (feedparser.parse(feed_url), feed_url, favicon_url)}
