# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Story
from .models import Folder
from .models import Subscription


admin.site.register(Story)
admin.site.register(Folder)
admin.site.register(Subscription)
