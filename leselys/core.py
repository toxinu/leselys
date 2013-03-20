# coding: utf-8
import os

from itsdangerous import TimestampSigner
from flask import Flask
from werkzeug.contrib.cache import SimpleCache


class Core(object):
    def __init__(self, host, port, debug):
        self.host = host
        self.port = int(port)
        self.debug = debug
        self.storage = None
        self.storage_settings = None
        self.session = None
        self.session_settings = None

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.urandom(24)
        self.signer = TimestampSigner(self.app.config['SECRET_KEY'])
        self.cache = SimpleCache()

    def load_storage(self, storage_klass, storage_settings):
        self.storage_settings = storage_settings
        self.storage = storage_klass(**self.storage_settings)

    def load_session(self):
        if self.session == "memory":
            return
        self.session = self.session.Session(**self.session_settings)
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
        self.app.run(host=self.host, port=int(self.port), debug=self.debug, use_reloader=self.debug)
