# coding: utf-8
import sys


def _load_storage(storage_name):
        module_name = "leselys.backends.storage._%s" % storage_name
        __import__(module_name)
        module = sys.modules[module_name]
        if module is None:
            raise Exception("Failed to import storage backend module %s" % module_name)

        klass = getattr(module, storage_name.capitalize())
        if klass is None:
            raise Exception("Failed to load storage backend %s" % storage_name)

        return klass
