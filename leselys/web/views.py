#!/usr/bin/env python
# coding: utf-8

from leselys.core import reader
from leselys.core import db
from leselys.web import app

from flask import render_template

# Context which return subscriptions list to every template
@app.context_processor
def get_subscriptions():
	return dict(subscriptions=reader.get_subscriptions())

#######################################################################
# VIEWS
#######################################################################
# Home
@app.route('/')
def home():
    return render_template('home.html')

# Settings
@app.route('/settings')
def settings():
	_settings = db.settings.find_one()
	del _settings['_id']
	return render_template('settings.html', settings=_settings)

