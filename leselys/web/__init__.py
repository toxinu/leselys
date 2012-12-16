#!/usr/bin/env python
# coding: utf-8
import os

from flask import Flask
from flask.ext.pymongo import PyMongo

SECRET_KEY = os.urandom(24)
USERNAME = 'admin'
PASSWORD = 'admin'
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

app.config['MONGO_DBNAME'] = 'leselys'
app.config['MONGO_HOST'] = os.environ.get('MONGO_URI', 'localhost')
mongo = PyMongo(app, config_prefix='MONGO')

from leselys.web import views
