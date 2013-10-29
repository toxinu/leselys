# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.views.generic import TemplateView

from .views import FeedListView
from .views import FeedDetailView
from .views import StoryListView
from .views import StoryDetailView
from .views import FolderListView
from .views import FolderDetailView

urlpatterns = patterns(
    '',
    (r'^$', TemplateView.as_view(template_name="index.html")),
    (r'^api/feed/(?P<pk>\d+)', FeedDetailView.as_view()),
    (r'^api/feed', FeedListView.as_view()),
    (r'^api/story/(?P<pk>\d+)', StoryDetailView.as_view()),
    (r'^api/story', StoryListView.as_view()),
    (r'^api/folder/(?P<pk>\d+)', FolderDetailView.as_view()),
    (r'^api/folder', FolderListView.as_view())
)
