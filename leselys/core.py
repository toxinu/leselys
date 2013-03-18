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
        self.backend = None
        self.backend_settings = None

    def load_backend(self):
        self.backend = self.backend.Backend(**self.backend_settings)

    def load_wsgi(self):
        from leselys.reader import Reader
        self.reader = Reader()

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.urandom(24)
        self.signer = TimestampSigner(self.app.config['SECRET_KEY'])
        self.cache = SimpleCache()

        from leselys import views
        from leselys import api


    def run(self):
        from leselys.reader import Reader
        self.reader = Reader()

        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = os.urandom(24)
        self.signer = TimestampSigner(self.app.config['SECRET_KEY'])
        self.cache = SimpleCache()

        from leselys import views
        from leselys import api
        self.app.run(host=self.host, port=int(self.port), debug=self.debug)
