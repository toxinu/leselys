# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Story
from .models import Folder
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='get_title', read_only=True)
    unread_counter = serializers.IntegerField(source='unread_counter', read_only=True)
    ordering_text = serializers.CharField(source='get_ordering_display', read_only=True)
    folder_text = serializers.CharField(source='folder.name', read_only=True)

    class Meta:
        model = Subscription
        exclude = ('user', )


class StoryListSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='entry.title', read_only=True)
    url = serializers.CharField(source='entry.url', read_only=True)
    published = serializers.DateTimeField(source='entry.published', read_only=True)
    updated = serializers.DateTimeField(source='entry.updated', read_only=True)

    class Meta:
        model = Story
        read_only_fields = ('entry', 'subscription')


class StoryDetailSerializer(serializers.ModelSerializer):
    guid = serializers.CharField(source='entry.guid', read_only=True)
    title = serializers.CharField(source='entry.title', read_only=True)
    url = serializers.CharField(source='entry.url', read_only=True)
    published = serializers.DateTimeField(source='entry.published', read_only=True)
    updated = serializers.DateTimeField(source='entry.updated', read_only=True)
    description = serializers.CharField(source='entry.description', read_only=True)

    class Meta:
        model = Story
        read_only_fields = ('entry', 'subscription')


class FolderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        exclude = ('user', )
