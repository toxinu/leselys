# -*- coding: utf-8 -*-
from django.conf.urls import patterns

from .views import StoryListAPIView
from .views import StoryDetailAPIView
from .views import FolderListAPIView
from .views import OrderingListAPIView
from .views import SubscriptionListAPIView

urlpatterns = patterns(
    '',
    (r'^api/ordering', OrderingListAPIView.as_view()),
    (r'^api/story/(?P<pk>\d+)', StoryDetailAPIView.as_view()),
    (r'^api/story', StoryListAPIView.as_view()),
    (r'^api/folder', FolderListAPIView.as_view()),
    (r'^api/subscription', SubscriptionListAPIView.as_view())
)
