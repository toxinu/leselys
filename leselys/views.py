# coding: utf-8
import leselys

from flask import render_template
from flask import jsonify
from flask import request

backend = leselys.core.backend
app = leselys.core.app
reader = leselys.core.reader

# Each template context have the subscriptions list
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
	_settings = backend.get_settings()
	return render_template('settings.html', settings=_settings)
