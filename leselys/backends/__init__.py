import sys


def _load_backend(backend_name):
        backend = __import__("leselys.backends._%s" % backend_name)
        backend = sys.modules["leselys.backends._%s" % backend_name]
        if backend is None:
            raise Exception('Failed to load %s backend' % backend_name)
        return backend
