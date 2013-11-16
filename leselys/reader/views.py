# -*- coding: utf-8 -*-
import json

from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Feed
from .models import Story
from .models import Folder
from .serializers import FeedSerializer
from .serializers import StoryListSerializer
from .serializers import StoryDetailSerializer


class CacheMixin(object):
    cache_timeout = None

    @method_decorator(cache_page(cache_timeout))
    def dispatch(self, *args, **kwargs):
        return super(CacheMixin, self).dispatch(*args, **kwargs)


class OrderingAPIView(View):
    def get(self, request, *args, **kwargs):
        response_json = []
        for ordering in Feed.ORDERING_CHOICES:
            response_json.append({'id': ordering[0], 'name': ordering[1]})
        return HttpResponse(json.dumps(response_json))


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
    serializer_class = StoryListSerializer
    cache_timeout = 60 * 60

    def get_queryset(self):
        qs = Story.objects.all().defer('description')

        feed = self.request.QUERY_PARAMS.get('feed')
        if feed:
            try:
                feed = int(feed)
                qs = qs.filter(feed=feed)
            except ValueError:
                pass

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

    def delete(self, request, *args, **kwargs):
        folder = self.get_object()
        if folder:
            if folder.feed_set.count() > 0:
                return HttpResponseBadRequest("Still feeds in this folder.")
            if Folder.objects.all().count() <= 1:
                return HttpResponseBadRequest("Can't remove last folder.")
        return super(FolderDetailAPIView, self).delete(request, *args, **kwargs)
