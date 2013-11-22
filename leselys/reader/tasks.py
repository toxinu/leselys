# -*- coding: utf-8 -*-
from celery import task


@task
def create_stories(subscription, nb=10):
    from .models import Story

    stories = []
    for entry in subscription.feed.entry_set.all().order_by('published').only('id')[:nb]:
        story = Story(entry_id=entry.id, subscription=subscription)
        stories.append(story)
    Story.objects.bulk_create(stories)
