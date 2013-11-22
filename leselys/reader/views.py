# -*- coding: utf-8 -*-
import json

from rest_framework.generics import ListAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View

from .models import Story
from .models import Folder
from .models import Subscription

from .serializers import FolderListSerializer
from .serializers import StoryListSerializer
from .serializers import StoryDetailSerializer
from .serializers import SubscriptionSerializer

from ..mixins import OnlyOwnedMixin


class OrderingListAPIView(View):
    def get(self, request, *args, **kwargs):
        response_json = []
        for ordering in Subscription.ORDERING_CHOICES:
            response_json.append({'id': ordering[0], 'name': ordering[1]})
        return HttpResponse(json.dumps(response_json))


class SubscriptionListAPIView(ListCreateAPIView, OnlyOwnedMixin):
    model = Subscription
    serializer_class = SubscriptionSerializer

    def pre_save(self, obj):
        obj.user = self.request.user


class StoryListAPIView(ListAPIView, OnlyOwnedMixin):
    model = Story
    serializer_class = StoryListSerializer


class StoryDetailAPIView(RetrieveUpdateAPIView, OnlyOwnedMixin):
    model = Story
    serializer_class = StoryDetailSerializer


class FolderListAPIView(ListCreateAPIView, OnlyOwnedMixin):
    model = Folder
    serializer_class = FolderListSerializer
    paginate_by = None


class FolderDetailAPIView(RetrieveUpdateDestroyAPIView, OnlyOwnedMixin):
    model = Folder

    def delete(self, request, *args, **kwargs):
        folder = self.get_object()
        if folder:
            if folder.id == 1:
                return HttpResponseBadRequest("Can't remove default folder.")
            if folder.feed_set.count() > 0:
                return HttpResponseBadRequest("Still subscriptions in this folder.")
            if Folder.objects.all().count() <= 1:
                return HttpResponseBadRequest("Can't remove last folder.")
        return super(FolderDetailAPIView, self).delete(request, *args, **kwargs)
