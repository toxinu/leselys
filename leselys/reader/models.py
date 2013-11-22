# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from leselys.core.models import Feed
from leselys.core.models import Entry

from .tasks import create_stories


class Folder(models.Model):
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.id == 1:
            raise Exception("Can't delete folder with id 1.")
        return super(Folder, self).delete(*args, **kwargs)


class Subscription(models.Model):
    DEFAULT_FOLDER = 1
    ORDERING_AUTO = 0
    ORDERING_NEWER = 1
    ORDERING_OLDER = 2
    DEFAULT_ORDERING = ORDERING_AUTO
    ORDERING_CHOICES = (
        (ORDERING_AUTO, 'Automatic'),
        (ORDERING_NEWER, 'Newer'),
        (ORDERING_OLDER, 'Older'))

    feed = models.ForeignKey(Feed)
    user = models.ForeignKey(User)
    ordering = models.SmallIntegerField(
        choices=ORDERING_CHOICES, default=DEFAULT_ORDERING, blank=True)
    folder = models.ForeignKey(Folder, default=DEFAULT_FOLDER)
    title = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        return u"%s's feed subscription for %s" % (self.feed, self.user)

    @property
    def unread_counter(self):
        return Story.objects.filter(subscription=self.id, readed=False).count()

    def get_title(self):
        if self.title:
            return self.title
        return self.feed.title

    def save(self, *args, **kwargs):
        super(Subscription, self).save(*args, **kwargs)
        create_stories(self)


class Story(models.Model):
    entry = models.ForeignKey(Entry)
    subscription = models.ForeignKey(Subscription)
    readed = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%s's story for subscription's %s" % (self.entry, self.subscription.id)

    class Meta:
        verbose_name_plural = "stories"
