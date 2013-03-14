# coding: utf-8
import leselys

from flask import jsonify
from flask import request

reader = leselys.core.reader
app = leselys.core.app

#######################################################################
# API
#######################################################################
# Add feed
@app.route('/api/add', methods=['POST'])
def add():
	return jsonify(reader.add(request.form['url']))

# Remove feed
@app.route('/api/remove/<feed_id>', methods=['DELETE'])
def remove(feed_id):
	return jsonify(reader.delete(feed_id))

# Return list of entries for given feed_id
@app.route('/api/get/<feed_id>')
def get(feed_id):
	return jsonify(content=reader.get(feed_id))

# Set entry as readed
@app.route('/api/read/<entry_id>')
def read(entry_id):
	entry = reader.read(entry_id)
	return jsonify(success=True, content=entry)

# Return number of unreaded entries
@app.route('/api/unread/<feed_id>')
def count_unread(feed_id):
	return jsonify(count=reader.get_unread(feed_id))

# Refresh all feeds
@app.route('/api/refresh')
def refresh():
	result = reader.refresh_all()
	return jsonify(success=True, content=result)

# [WIP]: Set settings
@app.route('/api/settings/<setting>/<value>')
def change_settings(setting, value):
	pass