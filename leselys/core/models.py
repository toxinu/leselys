# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return "%s's profile" % self.user


class Feed(models.Model):
    DEFAULT_ERROR_MSG = u'This feed has never been fetched'

    title = models.CharField(max_length=300, blank=True)

    url = models.URLField(unique=True)
    website_url = models.URLField(blank=True)
    favicon_url = models.URLField(blank=True)

    added = models.DateTimeField(default=datetime.now, auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)

    in_error = models.BooleanField(default=True)
    error = models.TextField(blank=True, default=DEFAULT_ERROR_MSG)

    def __unicode__(self):
        return self.title or self.url

    def fetch(self):
        from .tasks import fetch_feed
        fetch_feed(feed=self)
        return self.in_error

    def clean(self):
        if not self.title:
            self.title = self.url
        if not self.in_error:
            self.error = ""

    def save(self, *args, **kwargs):
        super(Feed, self).save(*args, **kwargs)

    def refresh(self):
        from .tasks import fetch_feed
        fetch_feed.apply_async((self.id,))


class Entry(models.Model):
    guid = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    url = models.URLField(null=True, blank=True)
    description = models.TextField()

    published = models.DateTimeField(default=datetime.now, auto_now_add=True)
    updated = models.DateTimeField(default=datetime.now, auto_now_add=True)

    feed = models.ForeignKey(Feed)

    class Meta:
        verbose_name_plural = "entries"

    def __unicode__(self):
        return self.title
