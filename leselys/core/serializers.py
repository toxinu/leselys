# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Feed
from .models import Entry


class FeedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        read_only_fields = ('updated', 'in_error', 'error')


class EntryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        exclude = ('description', 'guid')
