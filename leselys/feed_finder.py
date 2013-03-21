from HTMLParser import HTMLParser

class FeedFinder(HTMLParser):
    """
    HTML parser which collects all rss/atom auto discovery links.
    """
    feed_content_types = ['application/rss+xml', 'application/atom+xml',
            'application/xml']

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
        """Find feed auto discovery links from html document.

        Returns list of tuples. Each tuple is form of (href, title). Title
        is empty string if not present.
        """
        parser = FeedFinder()
        parser.feed(html_document)
        parser.close()
        return parser.feeds
