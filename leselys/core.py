# coding: utf-8
import os
import sys

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import leselys
import werkzeug
import flask
import celery
import requests

from itsdangerous import TimestampSigner
from flask import Flask
from werkzeug.contrib.cache import SimpleCache

from leselys.backends.storage import _load_storage
from leselys.backends.session import _load_session

# from http://flask.pocoo.org/snippets/35/
class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

class Core(object):
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5000
        self.debug = False
        self.storage = None
        self.storage_settings = {}
        self.session = None
        self.session_settings = {}

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.urandom(24)
        self.app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
        self.app.wsgi_app = ReverseProxied(self.app.wsgi_app)

        py_v = sys.version_info
        py_v = "%s.%s.%s" % (py_v[0], py_v[1], py_v[2])
        self.app.config.versions = {'python': py_v,
                                    'leselys': leselys.__version__,
                                    'flask': flask.__version__,
                                    'werkzeug': werkzeug.__version__,
                                    'celery': celery.__version__,
                                    'requests': requests.__version__}

        self.signer = TimestampSigner(self.app.config['SECRET_KEY'])
        self.cache = SimpleCache()

    def load_config(self, config_path, args={}):
        if not os.path.exists(config_path):
            print('Error: "%s" file not exists.' % config_path)
            sys.exit(1)
        self.args = args
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

        if self.config.has_section('webserver') and self.config.get('webserver', 'host'):
            self.host = self.config.get('webserver', 'host')
        if self.config.has_section('webserver') and self.config.get('webserver', 'port'):
            self.port = self.config.get('webserver', 'port')
        if self.config.has_section('webserver') and self.config.get('webserver', 'debug'):
            if self.config.get('webserver', 'debug') in ['True', 'true']:
                self.debug = True
            else:
                self.debug = False
        self.host = self.host or self.args.get('--host')
        self.port = self.port or self.args.get('--port')
        self.debug = self.debug or self.args.get('--debug')

        self.app.config['DEBUG'] = self.debug

        if not self.config.has_section('storage'):
            print('Missing storage section in configuration file')
            sys.exit(1)
        if not self.config.get('storage', 'type'):
            print('Missing type setting in storage section in configuration file')
            sys.exit(1)
        if not self.config.has_section('session'):
            self.config.add_section('session')
            self.config.set('session', 'type', 'memory')

        if not self.config.has_section('worker'):
            print('Missing worker section in configuration file')
            sys.exit(1)
        if not self.config.has_option('worker', 'interval'):
            self.config.set('worker', 'interval', '10')
        if not self.config.has_option('worker', 'retention'):
            self.config.set('worker', 'retention', '30')
        if not self.config.has_option('worker', 'story_before_retention'):
            self.config.set('worker', 'story_before_retention', '50')

    def load_storage(self):
        for item in self.config.items('storage'):
            self.storage_settings[item[0]] = item[1]
        del self.storage_settings['type']

        self.storage_module = _load_storage(self.config.get('storage', 'type'))
        self.storage = self.storage_module(**self.storage_settings)

    def load_session(self):
        if self.config.get('session', 'type') == "memory":
            return

        for item in self.config.items('session'):
            self.session_settings[item[0]] = item[1]
        del self.session_settings['type']

        self.session_module = _load_session(self.config.get('session', 'type'))
        self.session = self.session_module.Session(**self.session_settings)
        self.app.session_interface = self.session

    def load_wsgi(self):
        from leselys.reader import Reader
        self.reader = Reader()

        from leselys import views
        from leselys import api

    def run(self):
        from leselys.reader import Reader
        self.reader = Reader()

        from leselys import views
        from leselys import api
        self.app.run(host=self.host, port=int(self.port), use_reloader=self.debug)
