# -*- coding: utf-8 -*-
from leselys import core


def app(config_path):
    core.load_config(config_path)
    core.load_storage()
    core.load_session()
    core.load_wsgi()
    app = core.app
    return app
