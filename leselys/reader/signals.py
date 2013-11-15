# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from leselys.reader.models import Feed
#from leselys.reader.tasks import init_feed


# @receiver(post_save, sender=Feed)
# def init_feed_callback(sender, instance, created, **kwargs):
#     if created:
#         init_feed.apply_async((instance.id,))
