# coding: utf-8
import sys


def _load_session(session_name):
    if session_name == "memory":
        return "memory"
    session = __import__("leselys.backends.session._%s" % session_name)
    session = sys.modules["leselys.backends.session._%s" % session_name]
    if session is None:
        raise Exception('Failed to load %s session backend' % session_name)
    return session
