#!/usr/bin/env python
# coding: utf-8
import os
import feedparser

from leselys.core import reader
from leselys.core import db
from leselys.web import app

from flask import render_template, jsonify, g, request

@app.context_processor
def get_subscriptions():
	return dict(subscriptions=reader.get_subscriptions())

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/add', methods=['POST'])
def add():
	return jsonify(reader.add(request.form['url']))
	if not r['success']:
		return jsonify(success=False)
	return jsonify(success=True, id=feed_id, title=title)

@app.route('/api/get/<feed_id>')
def get(feed_id):
	return jsonify(content=reader.get(feed_id))

@app.route('/api/read/<entry_id>')
def read(entry_id):
	entry = reader.read(entry_id)
	return jsonify(success=True, content=entry)

@app.route('/api/refresh')
def refresh():
	reader.refreshAll()
	return true

@app.route('/api/settings/<setting>/<value>')
def change_settings(setting, value):
	pass

@app.route('/settings')
def settings():
	_settings = db.settings.find_one()
	del _settings['_id']
	return render_template('settings.html', settings=_settings)
