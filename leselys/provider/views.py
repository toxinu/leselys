# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed as FeedView

from ..core.models import Feed
from ..core.models import Entry


class FeedProviderView(FeedView):

    def get_object(self, request, feed_id):
        return get_object_or_404(Feed, pk=feed_id)

    def title(self, obj):
        return obj.title

    def link(self, obj):
        return obj.url

    def description(self, obj):
        return obj.title

    def items(self, obj):
        return Entry.objects.filter(feed=obj).order_by('-published')[:20]

    def item_link(self, item):
        return item.url
