#!/usr/bin/env python
# coding: utf-8

from leselys.core import reader
from leselys.core import db
from leselys.web import app

from flask import render_template
from flask import jsonify
from flask import request

# Each template context have the subscriptions list
@app.context_processor
def get_subscriptions():
	return dict(subscriptions=reader.get_subscriptions())

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/add', methods=['POST'])
def add():
	return jsonify(reader.add(request.form['url']))

@app.route('/api/get/<feed_id>')
def get(feed_id):
	return jsonify(content=reader.get(feed_id))

@app.route('/api/read/<entry_id>')
def read(entry_id):
	entry = reader.read(entry_id)
	return jsonify(success=True, content=entry)

@app.route('/api/unread/<entry_id>')
def unread(entry_id):
	entry = reader.unread(entry_id)
	return jsonify(success=True)

@app.route('/api/refresh')
def refresh():
	reader.refresh_all()
	return jsonify(success=True)

@app.route('/api/settings/<setting>/<value>')
def change_settings(setting, value):
	pass

@app.route('/settings')
def settings():
	_settings = db.settings.find_one()
	del _settings['_id']
	return render_template('settings.html', settings=_settings)
