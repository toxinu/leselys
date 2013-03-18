# coding: utf-8
import leselys

from flask import jsonify
from flask import request
from flask import make_response

from threading import Thread

from leselys.helpers import login_required
from leselys.helpers import cached
from leselys.helpers import retrieve_feeds_from_opml
from leselys.helpers import export_to_opml


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


# Set story as readed
@app.route('/api/read/<story_id>')
@login_required
def read(story_id):
    return jsonify(reader.read(story_id))


# Set story as unreaded
@app.route('/api/unread/<story_id>')
@login_required
def unread(story_id):
    return jsonify(reader.unread(story_id))


# Refresh all feeds
@app.route('/api/refresh')
@login_required
@cached(30)
def refresh():
    return jsonify(success=True, content=reader.refresh_all())


# Import opml
@app.route('/api/import/opml', methods=['POST'])
@login_required
@cached(10)
def import_opml():
    file = request.form['file']
    for feed in retrieve_feeds_from_opml(file):
        t = Thread(target=reader.add, args=(feed['url'],))
        t.start()
    return jsonify(success=True, output='Imported file is processing...')


# Export opml
@app.route('/api/export/opml')
@login_required
@cached(10)
def export_opml():
    rsp = make_response(export_to_opml())
    rsp.headers['Content-Type'] = "application/xml"
    return rsp


# [WIP]: Set settings
@app.route('/api/settings/<setting>/<value>')
@login_required
def change_settings(setting, value):
    pass
