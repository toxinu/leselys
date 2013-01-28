# coding: utf-8
import os

from sofart import Database
from flask import Flask

from leselys.logger import stream_logger

class Core(object):
	def __init__(self, path, mode, host, port, debug):

		self.path = path
		self.mode = mode
		self.host = host
		self.port = int(port)
		self.debug = debug

	def run(self):
		self.db = Database(self.path, mode=self.mode)
		if not self.db.settings.find_one():
			self.db.settings.save({'acceptable_elements': []})

		from leselys.reader import Reader
		self.reader = Reader()

		SECRET_KEY = os.urandom(24)
		self.app = Flask(__name__)
		self.app.config.from_object(__name__)
		self.app.config.from_envvar('FLASKR_SETTINGS', silent=True)

		from leselys import views
		from leselys import api
		self.app.run(host=self.host, port=int(self.port), debug=self.debug)