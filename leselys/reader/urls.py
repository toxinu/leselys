# -*- coding: utf-8 -*-
from django.conf.urls import patterns

from .views import SubscriptionAPIView
from .views import StoryAPIView

urlpatterns = patterns(
    '',
    (r'^api/subscription', SubscriptionAPIView.as_view()),
    (r'^api/story', StoryAPIView.as_view())
)
