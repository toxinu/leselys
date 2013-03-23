# coding: utf-8
import leselys

from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import make_response
from flask import jsonify

from leselys.helpers import login_required
from leselys.themes import themes

storage = leselys.core.storage
app = leselys.core.app
reader = leselys.core.reader
signer = leselys.core.signer

# Each template context have the feeds list
# Context which return feeds list to every template


@app.context_processor
def get_feeds():
    return dict(feeds=reader.get_feeds())


@app.context_processor
def get_theme():
    _themes = dict((k.lower(), v) for k,v in themes.iteritems())
    theme = session.get('theme_name')
    if not theme:
        theme = storage.get_setting('theme_name')
        if not theme:
            theme = 'journal'
            storage.set_setting('theme_name', theme)
    return dict(current_theme_name=theme, current_theme_url=_themes[theme])

#######################################################################
# VIEWS
#######################################################################


@app.route('/')
@login_required
def home():
    home_template = render_template('home.html')
    if request.args.get('jsonify', 'false') == "true":
        return jsonify(success=True, content=home_template)
    return home_template


@app.route('/settings')
@login_required
def settings():
    settings_context = storage.get_settings()
    settings_template = render_template('settings.html', settings=settings_context, themes=themes)
    if request.args.get('jsonify', 'false') == "true":
        return jsonify(success=True, content=settings_template)
    return settings_template


@app.route('/login')
def login_view():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    if request.cookies.get('remember'):
        username = request.cookies.get('username')
        password_md5 = request.cookies.get('password')
        if username in storage.get_users():
            try:
                password_unsigned = signer.unsign(
                    password_md5, max_age=15 * 24 * 60 * 60)
            except:
                return render_template('login.html')
            if password_unsigned == storage.get_password(username):
                return redirect(url_for('home'))
    return render_template('login.html')
