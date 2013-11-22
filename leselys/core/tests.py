# -*- coding: utf-8 -*-
from django.test import TestCase

from .models import Feed
from .models import Entry


class FeedTestCase(TestCase):
    def setUp(self):
        self.feed_url = "http://www.cnn.com/"

    def test_add_feed(self):
        feed = Feed(url=self.feed_url)
        feed.full_clean()
        feed.save()

    def test_auto_fetch_stories(self):
        feed = Feed(url=self.feed_url)
        feed.full_clean()
        feed.save()

        self.assertNotEqual(Entry.objects.filter(feed=feed.id).count(), 0)
