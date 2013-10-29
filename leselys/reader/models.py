# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from .helpers import get_feed_urls


class Folder(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Story(models.Model):
    guid = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    description = models.TextField()
    published = models.DateTimeField(default=datetime.now, auto_now_add=True)
    updated = models.DateTimeField(default=datetime.now, auto_now_add=True)
    readed = models.BooleanField(default=False)
    feed = models.ForeignKey('Feed')

    class Meta:
        verbose_name_plural = "stories"

    def __unicode__(self):
        return self.title


class Feed(models.Model):
    ORDERING_AUTO = 0
    ORDERING_NEWER = 1
    ORDERING_OLDER = 2
    DEFAULT_ORDERING = ORDERING_AUTO
    ORDERING_CHOICES = (
        (ORDERING_AUTO, 'Automatic'),
        (ORDERING_NEWER, 'Newer'),
        (ORDERING_OLDER, 'Older'))
    DEFAULT_ERROR_MSG = u'This feed has never been fetched'
    DEFAULT_FOLDER = 1

    title = models.CharField(max_length=300, blank=True)
    custom_title = models.CharField(max_length=300, blank=True)
    url = models.URLField(unique=True)
    updated = models.DateTimeField(default=datetime.now, auto_now_add=True)
    ordering = models.SmallIntegerField(
        choices=ORDERING_CHOICES, default=DEFAULT_ORDERING, blank=True)
    website_url = models.URLField(blank=True)
    favicon_url = models.URLField(blank=True)
    in_error = models.BooleanField(default=True)
    error = models.CharField(blank=True, max_length=1000, default=DEFAULT_ERROR_MSG)
    folder = models.ForeignKey('Folder', default=DEFAULT_FOLDER)

    def __unicode__(self):
        return self.title or self.url

    @property
    def initialized(self):
        return self.error != Feed.DEFAULT_ERROR_MSG

    @property
    def counter(self):
        return Story.objects.filter(feed=self.id, readed=False).count()

    def initialize(self):
        from leselys.reader.tasks import fetch_feed

        feed_guesser = get_feed_urls(self.url)
        if feed_guesser['success']:
            feed_data, self.url, self.favicon_url = feed_guesser['output']
            self.title = feed_data.feed.get('title', self.url)
            self.website_url = feed_data.feed.get('link', self.url)
            self.in_error = False
            self.error = ""
            self.save()
            fetch_feed(feed=self, raw_data=feed_data)
        else:
            self.in_error = True
            self.error = feed_guesser['output']

        return self.in_error

    def fetch(self):
        from leselys.reader.tasks import fetch_feed
        fetch_feed(feed=self)
        return self.in_error

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.url
        if not self.in_error:
            self.error = ""

        super(Feed, self).save(*args, **kwargs)

        if not self.initialized:
            self.initialize()

    def refresh(self):
        from leselys.reader.tasks import fetch_feed
        fetch_feed.apply_async((self.id,))
