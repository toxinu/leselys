#!/usr/bin/env python
# coding: utf-8

from leselys.core import reader
from leselys.web import app

from flask import jsonify

#######################################################################
# API
#######################################################################
# Add feed
@app.route('/api/add', methods=['POST'])
def add():
	return jsonify(reader.add(request.form['url']))

# Return list of entries for given feed_id
@app.route('/api/get/<feed_id>')
def get(feed_id):
	return jsonify(content=reader.get(feed_id))

# Set entry as readed
@app.route('/api/read/<entry_id>')
def read(entry_id):
	entry = reader.read(entry_id)
	return jsonify(success=True, content=entry)

# [WIP]: Refresh all feeds
@app.route('/api/refresh')
def refresh():
	reader.refreshAll()
	return true

# [WIP]: Set settings
@app.route('/api/settings/<setting>/<value>')
def change_settings(setting, value):
	pass

