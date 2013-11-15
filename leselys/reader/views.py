# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Story
from .models import Feed
from .models import Folder
from .serializers import FeedSerializer
from .serializers import StorySerializer
from .serializers import StoryDetailSerializer


class CacheMixin(object):
    cache_timeout = None

    @method_decorator(cache_page(cache_timeout))
    def dispatch(self, *args, **kwargs):
        return super(CacheMixin, self).dispatch(*args, **kwargs)


class FeedListAPIView(ListCreateAPIView, CacheMixin):
    model = Feed
    serializer_class = FeedSerializer
    cache_timeout = 60 * 60


class FeedDetailAPIView(CreateAPIView, RetrieveUpdateDestroyAPIView, CacheMixin):
    model = Feed
    serializer_class = FeedSerializer
    cache_timeout = 60 * 60


class StoryListAPIView(ListAPIView, CacheMixin):
    model = Story
    serializer_class = StorySerializer
    cache_timeout = 60 * 60

    def get_queryset(self):
        qs = Story.objects.all().defer('description')

        feed = self.request.QUERY_PARAMS.get('feed')
        if feed:
            qs = qs.filter(feed=feed)

        readed = self.request.QUERY_PARAMS.get('readed')
        if readed in ['', 'true', 'True', '1', 'yes']:
            qs = qs.filter(readed=True)
        elif readed in ['false', '0', 'no']:
            qs = qs.filter(readed=False)

        return qs


class StoryDetailAPIView(RetrieveUpdateAPIView, CacheMixin):
    model = Story
    serializer_class = StoryDetailSerializer
    cache_timeout = 60 * 60


class FolderListAPIView(ListCreateAPIView, CacheMixin):
    model = Folder
    paginate_by = None
    cache_timeout = 60 * 60


class FolderDetailAPIView(RetrieveUpdateDestroyAPIView, CacheMixin):
    model = Folder
    cache_timeout = 60 * 60
