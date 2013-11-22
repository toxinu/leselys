# -*- coding: utf-8 -*-
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListCreateAPIView

from .models import Feed
from .models import Entry
from .serializers import FeedListSerializer
from .serializers import EntryListSerializer


class FeedListAPIView(ListCreateAPIView):
    model = Feed
    serializer_class = FeedListSerializer


class FeedDetailAPIView(RetrieveAPIView):
    model = Feed


class EntryListAPIView(ListAPIView):
    model = Entry
    serializer_class = EntryListSerializer


class EntryDetailAPIView(RetrieveAPIView):
    model = Entry
