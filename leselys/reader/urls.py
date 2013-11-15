# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.views.generic import TemplateView

from .views import FeedListAPIView
from .views import FeedDetailAPIView
from .views import StoryListAPIView
from .views import StoryDetailAPIView
from .views import FolderListAPIView
from .views import FolderDetailAPIView

urlpatterns = patterns(
    '',
    (r'^$', TemplateView.as_view(template_name="index.html")),
    (r'^api/feed/(?P<pk>\d+)', FeedDetailAPIView.as_view()),
    (r'^api/feed', FeedListAPIView.as_view()),
    (r'^api/story/(?P<pk>\d+)', StoryDetailAPIView.as_view()),
    (r'^api/story', StoryListAPIView.as_view()),
    (r'^api/folder/(?P<pk>\d+)', FolderDetailAPIView.as_view()),
    (r'^api/folder', FolderListAPIView.as_view())
)
