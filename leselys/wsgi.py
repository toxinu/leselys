# -*- coding: utf-8 -*-
import os
import sys
import ConfigParser

from leselys import core
from leselys.backends.storage import _load_storage

def app(config_path):
    config = ConfigParser.ConfigParser()

    if not os.path.exists(config_path):
        print('Error: "%s" file not exists.' % config_path)
        sys.exit(1)

    config.read(config_path)

    # Create storage
    storage_settings = {}
    for item in config.items('storage'):
        storage_settings[item[0]] = item[1]
    del storage_settings['type']

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

    storage_module = _load_storage(config.get('storage', 'type'))
    core.storage = storage_module
    core.storage_settings = storage_settings
    core.load_storage()
    core.load_wsgi()

    app = core.app
    return app
