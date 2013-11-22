# -*- coding: utf-8 -*-
import datetime
import feedparser

from datetime import timedelta

from celery import task
from celery.task.base import periodic_task
from celery.utils.log import get_task_logger

from django.conf import settings
from django.utils.timezone import utc

from .models import Feed
from .models import Entry
from .helpers import get_datetime

from leselys.reader.models import Story
from leselys.reader.models import Subscription

feedparser.USER_AGENT = settings.FEEDPARSER_USER_AGENT
logger = get_task_logger(__name__)

FEEDPARSER_BOZO_EXCEPTION = settings.FEEDPARSER_BOZO_EXCEPTION

try:
    FETCH_INTERVAL = settings.FETCH_INTERVAL
except AttributeError:
    FETCH_INTERVAL = timedelta(hours=1)

try:
    MAX_FEEDS_AGE = settings.MAX_FEEDS_AGE
except AttributeError:
    MAX_FEEDS_DAY_AGE = 30


if FETCH_INTERVAL:
    @periodic_task(run_every=FETCH_INTERVAL)
    @task
    def fetch_all():
        logger.info(':: Fetching all feeds')

        for feed in Feed.objects.all().values('id'):
            fetch_feed.apply_async((feed['id'],))


@task
def fetch_feed(feed_id=None, raw_data=None, feed=None):
    # Give just feed_id (when async task)
    # Or give raw_data + feed (when called from model)
    if not feed_id and not raw_data:
        return 'FAILURE'

    if not feed:
        feed = Feed.objects.get(id=feed_id)
        logger.info(':: Fetching feed (%s)' % feed.url)

    if not raw_data:
        feed_data = feedparser.parse(feed.url)
    else:
        feed_data = raw_data

    if feed_data.bozo and \
            (feed_data.bozo_exception.__class__ not in FEEDPARSER_BOZO_EXCEPTION.keys()):

        feed.in_error = True
        try:
            feed.error = feed_data.bozo_exception.getMessage()
        except:
            feed.error = feed_data.bozo_exception
        feed.save()
        return 'FAILURE'

    # Update title if it change
    if feed_data.feed.get('title') != feed.title:
        feed.title = feed_data.feed.get('title')
    # Add website url if not setted
    if feed_data.feed.get('link') != feed.website_url:
        feed.website_url = feed_data.feed.get('link', feed.website_url)

    # Update it
    if feed_data.feed.get('updated_parsed'):
        feed.updated = get_datetime(feed_data.feed.get('updated_parsed'))
    elif feed_data.get('updated_parsed'):
        feed.updated = get_datetime(feed_data.get('updated_parsed'))
    elif feed_data.feed.get('published_parsed'):
        feed.updated = get_datetime(feed_data.feed.get('published_parsed'))
    elif feed_data.get('published_parsed'):
        feed.updated = get_datetime(feed_data.get('published_parsed'))
    else:
        feed.updated = datetime.datetime.utcnow().replace(tzinfo=utc)

    feed.in_error = False
    feed.error = ""
    feed.save()

    entries = []
    for entry_data in feed_data.get('entries', []):
        title = entry_data.get('guid') or entry_data.get('title')
        entry = Entry(guid=title,
                      title=entry_data.get('title'),
                      feed=feed,
                      url=entry_data.get('link'))

        try:
            entry.description = entry_data['content'][0]['value']
        except KeyError:
            entry.description = entry_data['summary']

        if entry_data.get('updated_parsed'):
            entry.updated = get_datetime(entry_data.get('updated_parsed'))
        else:
            entry.updated = datetime.datetime.utcnow().replace(tzinfo=utc)

        if entry_data.get('published_parsed', False):
            entry.published = get_datetime(entry_data.get('published_parsed'))
        else:
            entry.published = datetime.datetime.utcnow().replace(tzinfo=utc)

        entries.append(entry)

    Entry.objects.bulk_create(entries)

    stories = []
    for subscription in Subscription.objects.filter(feed=feed):
        for entry in entries:
            story = Story(entry=entry, subscription=subscription)
            stories.append(story)

    Story.objects.bulk_create(stories)
