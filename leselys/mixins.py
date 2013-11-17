# -*- coding: utf-8 -*-
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class CacheMixin(object):
    cache_timeout = None

    @method_decorator(cache_page(cache_timeout))
    def dispatch(self, *args, **kwargs):
        return super(CacheMixin, self).dispatch(*args, **kwargs)
