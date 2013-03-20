# coding: utf-8
import leselys

from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import make_response

from leselys.helpers import login_required

storage = leselys.core.storage
app = leselys.core.app
reader = leselys.core.reader
signer = leselys.core.signer

# Each template context have the feeds list
# Context which return feeds list to every template


@app.context_processor
def get_feeds():
    return dict(feeds=reader.get_subscriptions())

#######################################################################
# VIEWS
#######################################################################


@app.route('/')
@login_required
def home():
    return render_template('home.html')


@app.route('/settings')
@login_required
def settings():
    _settings = storage.get_settings()
    return render_template('settings.html', settings=_settings)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember', False)

        if storage.is_valid_login(username, password):
            session['logged_in'] = True
            rsp = make_response(redirect(url_for('home')))
            if remember:
                session.permanent = True
                rsp.set_cookie('remember', True)
                rsp.set_cookie('username', username)
                rsp.set_cookie('token', signer.sign(password_md5))
            return rsp
        else:
            return render_template('login.html')
    else:
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


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    rsp = make_response(redirect(url_for('login')))
    rsp.set_cookie('username', None)
    rsp.set_cookie('token', None)
    rsp.set_cookie('remember', False)
    return rsp
