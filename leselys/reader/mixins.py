# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response


class ListCreateAPIViewMixin(object):
    def pre_create(self, *args, **kwargs):
        pass

    def post_create(self, *args, **kwargs):
        pass

    def pre_validate(self, *args, **kwargs):
        pass

    def post_validate(self, *args, **kwargs):
        pass

    def save(self, *args, **kwargs):
        self.pre_save(self.serializer.object)
        self.object = self.serializer.save(force_insert=True)
        self.post_save(self.object, created=True)

    def create(self, request, *args, **kwargs):
        self.pre_create(*args, **kwargs)
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        self.pre_validate(*args, **kwargs)
        if serializer.is_valid():
            self.post_validate(*args, **kwargs)
            self.save(*args, **kwargs)
            headers = self.get_success_headers(serializer.data)

            self.post_create(*args, **kwargs)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        self.post_create(*args, **kwargs)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)