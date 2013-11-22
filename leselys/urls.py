# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('leselys.core.urls')),
    url(r'^', include('leselys.reader.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^uploads/(?P<path>.*)$',
         'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
