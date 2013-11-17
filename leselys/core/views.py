# -*- coding: utf-8 -*-
from rest_framework.generics import CreateAPIView

from .models import Feed
from .serializers import FeedCreateSerializer


class FeedCreateAPIView(CreateAPIView):
    model = Feed
    serializer_class = FeedCreateSerializer
