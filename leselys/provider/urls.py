# -*- coding: utf-8 -*-
from django.conf.urls import patterns

from .views import FeedProviderView

urlpatterns = patterns(
    '',
    (r'^api/rss/(?P<feed_id>\d+)$', FeedProviderView())
)
