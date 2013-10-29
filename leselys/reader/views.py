# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .mixins import ListCreateAPIViewMixin

from .models import Story
from .models import Feed
from .models import Folder
from .serializers import FeedSerializer


class FeedListView(ListCreateAPIViewMixin, ListCreateAPIView):
    model = Feed
    serializer_class = FeedSerializer


class FeedDetailView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    model = Feed


class StoryListView(ListAPIView):
    model = Story


class StoryDetailView(RetrieveUpdateAPIView):
    model = Story


class FolderListView(ListCreateAPIViewMixin, ListCreateAPIView):
    model = Folder
    paginate_by = None


class FolderDetailView(RetrieveUpdateDestroyAPIView):
    model = Folder
