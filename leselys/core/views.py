# -*- coding: utf-8 -*-
from rest_framework.generics import ListCreateAPIView

from .models import Feed
from .serializers import FeedCreateSerializer


class FeedListCreateAPIView(ListCreateAPIView):
    model = Feed
    serializer_class = FeedCreateSerializer
