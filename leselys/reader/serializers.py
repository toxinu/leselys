# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import Feed


class FeedSerializer(serializers.ModelSerializer):
    folder = serializers.PrimaryKeyRelatedField(required=False)

    class Meta:
        model = Feed
        fields = (
            'title', 'custom_title', 'url', 'ordering',
            'website_url', 'favicon_url', 'folder')
        read_only_fields = ('updated', 'in_error', 'error')