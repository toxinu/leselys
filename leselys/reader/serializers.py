# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Feed
from .models import Story


class FeedSerializer(serializers.ModelSerializer):
    unread_counter = serializers.IntegerField(source='unread_counter', read_only=True)
    ordering_text = serializers.CharField(source='get_ordering_display', read_only=True)
    folder_text = serializers.CharField(source='folder.name', read_only=True)

    class Meta:
        model = Feed
        read_only_fields = ('updated', 'in_error', 'error')


class StoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'title', 'published', 'updated', 'readed', 'feed')


class StoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        read_only_fields = (
            'title', 'guid', 'description', 'published', 'updated', 'feed')
