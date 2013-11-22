# -*- coding: utf-8 -*-
from django.conf.urls import patterns

from .views import EntryListAPIView
from .views import EntryDetailAPIView
from .views import FeedDetailAPIView
from .views import FeedListAPIView

urlpatterns = patterns(
    '',
    (r'^api/feed/(?P<pk>\d+)', FeedDetailAPIView.as_view()),
    (r'^api/feed', FeedListAPIView.as_view()),
    (r'^api/entry/(?P<pk>\d+)', EntryDetailAPIView.as_view()),
    (r'^api/entry', EntryListAPIView.as_view()),
)
