# -*- coding: utf-8 -*-
from django.conf.urls import patterns
from django.views.generic import TemplateView

from .views import FeedListCreateAPIView

urlpatterns = patterns(
    '',
    (r'^$', TemplateView.as_view(template_name="index.html")),
    (r'^api/feed', FeedListCreateAPIView.as_view())
)
