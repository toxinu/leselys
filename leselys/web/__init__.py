#!/usr/bin/env python
# coding: utf-8
import os

from flask import Flask

SECRET_KEY = os.urandom(24)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

from leselys.web import views
from leselys.web import api
