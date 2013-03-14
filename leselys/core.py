# coding: utf-8
import os

from flask import Flask
from leselys.logger import stream_logger

class Core(object):
    def __init__(self, host, port, debug):
        self.host = host
        self.port = int(port)
        self.debug = debug
        self.backend = None
        self.backend_settings = None

    def run(self):
        self.backend = self.backend.Backend(**self.backend_settings)

        from leselys.reader import Reader
        self.reader = Reader()

        SECRET_KEY = os.urandom(24)
        self.app = Flask(__name__)
        self.app.config.from_object(__name__)
        self.app.config.from_envvar('FLASKR_SETTINGS', silent=True)

        from leselys import views
        from leselys import api
        self.app.run(host=self.host, port=int(self.port), debug=self.debug)
