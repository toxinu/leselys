# -*- coding: utf-8 -*-
from celery import task


@task
def retrieve_entries(subscription):
    from .models import Story

    stories = []
    for entry in subscription.feed.entry_set.all().order_by('published').only('id')[:10]:
        story = Story(entry_id=entry.id, subscription=subscription)
        stories.append(story)
    Story.objects.bulk_create(stories)
