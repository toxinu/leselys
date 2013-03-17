# coding: utf-8
import leselys

from flask import jsonify
from flask import request
from flask import flash

from threading import Thread

from leselys.helpers import login_required
from leselys.helpers import cached
from leselys.helpers import retrieve_feeds_from_opml


from flask import render_template

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
@app.route('/api/get/<feed_id>', defaults={'order_type': 'normal'})
@app.route('/api/get/<feed_id>/<order_type>')
@login_required
def get(feed_id, order_type):
	return jsonify(content=reader.get(feed_id, order_type))

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
@cached(1)
def refresh():
	result = reader.refresh_all()
	return jsonify(success=True, content=result)

# Upload opml
@app.route('/api/import/opml', methods=['POST'])
@login_required
@cached(10)
def import_opml():
	file = request.form['file']
	for feed in retrieve_feeds_from_opml(file):
		t = Thread(target=reader.add, args=(feed['url'],))
		t.start()
	return jsonify(success=True, output='Imported file is processing...')

# [WIP]: Set settings
@app.route('/api/settings/<setting>/<value>')
@login_required
def change_settings(setting, value):
	pass
