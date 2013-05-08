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
from datetime import datetime

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

# Set password
@app.route('/api/set_password', methods=['POST'])
def set_password():
    if storage.get_password():
        if not session.get('logged_in'):
            if request.args.get('jsonify', "true") == "false":
                return redirect(url_for('home'))
            else:
                return jsonify(success=False, content="Not allowed")

    password = request.form.get('password')
    storage.set_password(password)

    session['logged_in'] = True
    if request.args.get('jsonify', "true") == "false":
        rsp = redirect(url_for('home'))
    else:
        rsp = make_response(jsonify(success=True, output="Password setted."))
    return rsp


# Get unreaded counters
@app.route('/api/counters')
@login_required
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
# Or all if feed_id not specified
@app.route('/api/get', defaults={'feed_id': False})
@app.route('/api/get/<feed_id>')
@login_required
def get(feed_id):
    order_type = request.args.get('order_type', 'user')
    start = request.args.get('start', 0)
    end = request.args.get('end', 100)
    return jsonify(success=True, content=reader.get(feed_id, order_type, start, end))


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
    file_date = datetime.today().strftime("%m-%d-%Y")
    rsp.headers['Content-Disposition'] = "attachment; filename=\"%s_export.opml\"" % file_date
    return rsp


# Login
@app.route('/api/login', methods=['POST'])
def login():
    password = request.form['password']
    remember = request.form.get('remember', False)
    if storage.is_valid_password(password):
            session['logged_in'] = True
            if request.args.get('jsonify', "true") == "false":
                rsp = redirect(url_for('home'))
            else:
                rsp = make_response(jsonify(success=True, output="Successfully logged in."))
            if remember:
                session.permanent = True
                rsp.set_cookie('remember', True)
                rsp.set_cookie('token', signer.sign(password))
            return rsp
    else:
        if request.args.get('jsonify', "true") == "false":
            return redirect(url_for('login_view'))
        else:
            return jsonify(success=False, output="Bad password.", callback="/api/login")


# Logout
@app.route('/logout')
@app.route('/api/logout')
def logout():
    session.pop('logged_in', None)
    if request.args.get('jsonify', "true") == "false" or request.path == "/logout":
        rsp = make_response(redirect(url_for('login_view')))
    else:
        rsp = make_response(jsonify(success=True, output="Successfully logged out."))
    rsp.set_cookie('token', None)
    rsp.set_cookie('remember', False)
    return rsp


# Set theme
@app.route('/api/settings/theme', methods=['POST'])
@login_required
def set_theme():
    theme_name = request.form['theme'].lower()
    _themes = dict((k.lower(), v) for k, v in themes.iteritems())
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


# Set feedsettings
@app.route('/api/feedsettings', methods=['POST'])
@login_required
def change__feed_setting():
    feed_id = request.form['feed_id']
    key = request.form['key']
    value = request.form['value']
    storage.set_feed_setting(feed_id, key, value)
    return jsonify(success=True, output="%s setting have been set at %s" % (key, value))
