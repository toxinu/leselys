# -*- coding: utf-8 -*-
import os
import sys
import ConfigParser

from leselys import core
from leselys.config import get_config
from leselys.backends import _load_backend

def app(config_path):
    config = ConfigParser.ConfigParser()

    if not os.path.exists(config_path):
        print('Error: "%s" file not exists.' % config_path)
        sys.exit(1)

    config.read(config_path)

    # Create backend
    backend_settings = {}
    for item in config.items('backend'):
        backend_settings[item[0]] = item[1]
    del backend_settings['type']

    # Flask webserver config
    if config.has_section('webserver') and config.get('webserver', 'host'):
        core.host = config.get('webserver', 'host')
    if config.has_section('webserver') and config.get('webserver', 'port'):
        core.port = config.get('webserver', 'port')
    if config.has_section('webserver') and config.get('webserver', 'debug'):
        if config.get('webserver', 'debug') in ['True', 'true']:
            core.debug = True
        else:
            core.debug = False

    backend_module = _load_backend(config.get('backend', 'type'))
    core.backend = backend_module
    core.backend_settings = backend_settings
    core.load_backend()
    core.load_wsgi()

    app = core.app
    return app
