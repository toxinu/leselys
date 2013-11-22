# -*- coding: utf-8 -*-
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Feed
from .tasks import fetch_feed
from .helpers import get_feed_urls


@receiver(post_save, sender=Feed)
def init_feed(sender, instance, created, **kwargs):
    if created:

        feed_guesser = get_feed_urls(instance.url)
        if feed_guesser['success']:
            feed_data, instance.url, instance.favicon_url = feed_guesser['output']
            instance.title = feed_data.feed.get('title', instance.url)
            instance.website_url = feed_data.feed.get('link', instance.url)
            instance.in_error = False
            instance.error = ""
            instance.full_clean()
            instance.save()
            fetch_feed.apply_async((instance.id, feed_data))
        else:
            instance.in_error = True
            instance.error = feed_guesser['output']
