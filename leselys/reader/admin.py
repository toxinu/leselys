# -*- coding: utf-8 -*-
from django.contrib import admin

from leselys.reader.models import Folder
from leselys.reader.models import Feed
from leselys.reader.models import Story


admin.site.register(Folder)
admin.site.register(Feed)
admin.site.register(Story)

from djcelery.models import TaskState, WorkerState
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)
