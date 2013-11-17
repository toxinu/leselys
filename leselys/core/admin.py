# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Feed
from .models import Entry


admin.site.register(Feed)
admin.site.register(Entry)

from djcelery.models import TaskState, WorkerState
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
