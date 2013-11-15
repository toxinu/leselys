# -*- coding: utf-8 -*-
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


class FeedListAPIView(ListCreateAPIView):
    model = Feed
    serializer_class = FeedSerializer


class FeedDetailAPIView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    model = Feed
    serializer_class = FeedSerializer


class StoryListAPIView(ListAPIView):
    model = Story
    serializer_class = StorySerializer

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


class StoryDetailAPIView(RetrieveUpdateAPIView):
    model = Story
    serializer_class = StoryDetailSerializer


class FolderListAPIView(ListCreateAPIView):
    model = Folder
    paginate_by = None


class FolderDetailAPIView(RetrieveUpdateDestroyAPIView):
    model = Folder
