# coding: utf-8
import leselys

from flask import jsonify
from flask import request
from flask import make_response
from flask import session
from flask import redirect
from flask import render_template
from flask import url_for

from threading import Thread

from leselys.themes import themes
from leselys.helpers import login_required
from leselys.helpers import cached
from leselys.helpers import retrieve_feeds_from_opml
from leselys.helpers import export_to_opml

storage = leselys.core.storage
reader = leselys.core.reader
app = leselys.core.app
signer = leselys.core.signer

#######################################################################
# API
#######################################################################

# Get unreaded counters
@app.route('/api/counters')
@login_required
@cached(10)
def get_counters():
    feeds = reader.get_feeds()
    res = []
    for feed in feeds:
        res.append((feed['id'], feed['counter']))
    return jsonify(success=True, content=res)

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


# Refresh a feed
@app.route('/api/refresh/<feed_id>')
@login_required
@cached(30)
def resfresh(feed_id):
    return jsonify(reader.refresh(feed_id))


# Mark all as read
@app.route('/api/all_read/<feed_id>')
@login_required
def all_read(feed_id):
    return jsonify(reader.mark_all_read(feed_id))


# Mark all as unread
@app.route('/api/all_unread/<feed_id>')
@login_required
def all_unread(feed_id):
    return jsonify(reader.mark_all_unread(feed_id))


# Import opml
@app.route('/api/import/opml', methods=['POST'])
@login_required
@cached(10)
def import_opml():
    opml_file = request.form['file']
    for feed in retrieve_feeds_from_opml(opml_file):
        t = Thread(target=reader.add, args=(feed['url'],))
        t.start()
    return jsonify(success=True, output='Imported file is processing...')


# Export opml
@app.route('/api/export/opml')
@login_required
@cached(10)
def export_opml():
    rsp = make_response(export_to_opml())
    rsp.headers['Content-Type'] = "application/atom+xml"
    return rsp


# Login
@app.route('/api/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    remember = request.form.get('remember', False)
    if storage.is_valid_login(username, password):
            session['logged_in'] = True
            if request.args.get('jsonify', "true") == "false":
                rsp = redirect(url_for('home'))
            else:
                rsp = make_response(jsonify(success=True, output="Successfully logged in."))
            if remember:
                session.permanent = True
                rsp.set_cookie('remember', True)
                rsp.set_cookie('username', username)
                rsp.set_cookie('token', signer.sign(password))
            return rsp
    else:
        if request.args.get('jsonify', "true") == "false":
            return redirect(url_for('login_view'))
        else:
            return jsonify(success=False, output="Bad credentials.", callback="/api/login")


# Logout
@app.route('/logout')
@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    if request.args.get('jsonify', "true") == "false" or request.path == "/logout":
        rsp = make_response(redirect(url_for('login_view')))
    else:
        rsp = make_response(jsonify(success=True, output="Successfully logged out."))
    rsp.set_cookie('username', None)
    rsp.set_cookie('token', None)
    rsp.set_cookie('remember', False)
    return rsp

# Set theme
@app.route('/api/settings/theme', methods=['POST'])
@login_required
def set_theme():
    theme_name = request.form['theme'].lower()
    _themes = dict((k.lower(), v) for k,v in themes.iteritems())
    if not theme_name in _themes.keys():
        return jsonify(success=False, output='Theme not exists')

    storage.set_setting('theme_name', theme_name)
    session['theme_name'] = theme_name
    return jsonify(success=True, output='Theme changed')

# Set settings
@app.route('/api/settings', methods=['POST'])
@login_required
def change_setting():
    key = request.form['key']
    value = request.form['value']
    storage.set_setting(setting, value)
    return jsonify(success=True, output="%s setting have been set at %s" % (setting, value))
