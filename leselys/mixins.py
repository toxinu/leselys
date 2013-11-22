# -*- coding: utf-8 -*-


class OnlyOwnedMixin(object):
    def get_queryset(self):
        qs = super(OnlyOwnedMixin, self).get_queryset()
        qs = qs.filter(user=self.request.user)

        return qs
