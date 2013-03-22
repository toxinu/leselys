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

from leselys.helpers import login_required
from leselys.helpers import cached
from leselys.helpers import retrieve_feeds_from_opml
from leselys.helpers import export_to_opml

storage = leselys.core.storage
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


# Refresh a feed
@app.route('/api/refresh/<feed_id>')
@login_required
@cached(30)
def resfresh(feed_id):
    return jsonify(reader.refresh(feed_id))


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
                rsp.set_cookie('token', signer.sign(password_md5))
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


# [WIP]: Set settings
@app.route('/api/settings/<setting>/<value>')
@login_required
def change_settings(setting, value):
    pass
