# -*- coding: utf-8 -*-
from django.conf.urls import patterns

from .views import FeedListCreateAPIView

urlpatterns = patterns(
    '',
    (r'^api/feed', FeedListCreateAPIView.as_view())
)
