# coding: utf-8
import leselys

from flask import jsonify
from flask import request

from leselys.helpers import login_required
from leselys.helpers import cached

reader = leselys.core.reader
app = leselys.core.app

#######################################################################
# API
#######################################################################
# Add feed
@app.route('/api/add', methods=['POST'])
@login_required
def add():
	return jsonify(reader.add(request.form['url']))

# Remove feed
@app.route('/api/remove/<feed_id>', methods=['DELETE'])
@login_required
def remove(feed_id):
	return jsonify(reader.delete(feed_id))

# Return list of entries for given feed_id
@app.route('/api/get/<feed_id>')
@login_required
@cached(2*60)
def get(feed_id):
	return jsonify(content=reader.get(feed_id))

# Set entry as readed
@app.route('/api/read/<entry_id>')
@login_required
def read(entry_id):
	entry = reader.read(entry_id)
	return jsonify(success=True, content=entry)

# Return number of unreaded entries
@app.route('/api/unread/<feed_id>')
@login_required
def count_unread(feed_id):
	return jsonify(count=reader.get_unread(feed_id))

# Refresh all feeds
@app.route('/api/refresh')
@login_required
@cached(1*60)
def refresh():
	result = reader.refresh_all()
	return jsonify(success=True, content=result)

# [WIP]: Set settings
@app.route('/api/settings/<setting>/<value>')
@login_required
def change_settings(setting, value):
	pass
