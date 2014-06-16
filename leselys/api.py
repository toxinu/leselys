# coding: utf-8
import leselys

from flask import jsonify
from flask import request
from flask import make_response
from flask import session
from flask import redirect
from flask import url_for

from threading import Thread
from datetime import datetime

from leselys.themes import themes
from leselys.helpers import login_required
from leselys.helpers import cached
from leselys.helpers import uncached
from leselys.helpers import retrieve_feeds_from_opml
from leselys.helpers import export_to_opml

storage = leselys.core.storage
reader = leselys.core.reader
app = leselys.core.app
signer = leselys.core.signer

#######################################################################
# API
#######################################################################


# Get feeds info
@app.route('/api/get_feeds')
def get_feeds():
    return jsonify(success=True, content=reader.get_feeds())


# Set password
@app.route('/api/set_password', methods=['POST'])
def set_password():
    # For demo
    heroku_urls = [
        "http://leselys.herokuapp.com/api/set_password",
        "https://leselys.herokuapp.com/api/set_password",
        "http://leselys.herokuapp.com:80/api/set_password",
        "https://leselys.herokuapp.com:443/api/set_password"]
    if request.url in heroku_urls:
        return jsonify(success=False, content="Funny little boy. Ip stored.")

    if storage.get_password():
        if not session.get('logged_in'):
            if request.args.get('jsonify', "true") == "false":
                return redirect(url_for('home'))
            else:
                return jsonify(success=False, content="Not allowed")

    password = request.form.get('password')
    if not password:
        return jsonify(success=False, content="Can't be empty")

    storage.set_password(password)

    session['logged_in'] = True
    if request.args.get('jsonify', "true") == "false":
        rsp = redirect(url_for('home'))
    else:
        rsp = make_response(jsonify(success=True, content="Password setted."))
    return rsp


# Get unreaded counters
@app.route('/api/counters')
@login_required
def get_counters():
    feeds = reader.get_feeds()
    res = []
    for feed in feeds:
        res.append((feed['id'], feed['counter']))

    res.append(('combined-feed', reader.get_combined_feed().get('counter', 0)))
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
@app.route('/api/get/<feed_id>')
@login_required
@cached(30)
def get(feed_id):
    start = int(request.args.get('start', 0))
    stop = int(request.args.get('stop', 50))

    if feed_id in ['combined-feed', 'stared-feed']:
        feed_type = feed_id
        feed_id = False
    else:
        feed_type = None

    order_type = request.args.get('order_type', 'user')
    return jsonify(success=True, content=reader.get(feed_id, feed_type, order_type, start, stop))


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
    uncached('/api/get/%s' % feed_id)
    return jsonify(reader.mark_all_read(feed_id))


# Mark all as unread
@app.route('/api/all_unread/<feed_id>')
@login_required
def all_unread(feed_id):
    uncached('/api/get/%s' % feed_id)
    return jsonify(reader.mark_all_unread(feed_id))


# Import opml
@app.route('/api/import/opml', methods=['POST'])
@login_required
@cached(10)
def import_opml():
    opml_file = request.files['file']
    try:
        feeds = retrieve_feeds_from_opml(opml_file.read())
    except Exception as err:
        return jsonify(success=False, output="Bad OPML file (%s)" % err)
    for feed in feeds:
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
                rsp.set_cookie('remember', "true")
                rsp.set_cookie('token', ''.join(str(signer.sign(storage.get_password())).split('.')[1:]))
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
    rsp.set_cookie('token', "true")
    rsp.set_cookie('remember', "false")
    return rsp


# Set theme
@app.route('/api/settings/theme', methods=['POST'])
@login_required
def set_theme():
    theme_name = request.form['theme'].lower()
    _themes = dict((k.lower(), v) for k, v in themes.items())
    if not theme_name in _themes.keys():
        return jsonify(success=False, output='Theme not exists')

    storage.set_setting('theme_name', theme_name)
    session['theme_name'] = theme_name
    return jsonify(success=True, output='Theme changed')


# Set settings
@app.route('/api/settings', methods=['POST'])
@login_required
def change_setting():
    setting = request.form['key']
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
