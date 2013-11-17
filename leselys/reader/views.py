# -*- coding: utf-8 -*-
import json

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import View

from .models import Folder
from .models import Subscription

from leselys.mixins import CacheMixin


class OrderingAPIView(View):
    def get(self, request, *args, **kwargs):
        response_json = []
        for ordering in Subscription.ORDERING_CHOICES:
            response_json.append({'id': ordering[0], 'name': ordering[1]})
        return HttpResponse(json.dumps(response_json))


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
            if folder.id == 1:
                return HttpResponseBadRequest("Can't remove default folder.")
            if folder.feed_set.count() > 0:
                return HttpResponseBadRequest("Still subscriptions in this folder.")
            if Folder.objects.all().count() <= 1:
                return HttpResponseBadRequest("Can't remove last folder.")
        return super(FolderDetailAPIView, self).delete(request, *args, **kwargs)
