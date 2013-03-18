# coding: utf-8
import sys


def _load_storage(storage_name):
        storage = __import__("leselys.backends.storage._%s" % storage_name)
        storage = sys.modules["leselys.backends.storage._%s" % storage_name]
        if storage is None:
            raise Exception('Failed to load %s storage backend' % storage_name)
        return storage
