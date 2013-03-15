# coding: utf-8
import hashlib
import leselys

from flask import render_template
from flask import jsonify
from flask import request
from flask import flash
from flask import session
from flask import redirect
from flask import url_for

from leselys.helpers import login_required

backend = leselys.core.backend
app = leselys.core.app
reader = leselys.core.reader

# Each template context have the subscriptions list
# Context which return subscriptions list to every template
@app.context_processor
def get_subscriptions():
	return dict(subscriptions=reader.get_subscriptions())

#######################################################################
# VIEWS
#######################################################################
# Home
@app.route('/')
@login_required
def home():
    return render_template('home.html')

# Settings
@app.route('/settings')
@login_required
def settings():
	_settings = backend.get_settings()
	return render_template('settings.html', settings=_settings)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        m = hashlib.md5()
        m.update(password)
        password_md5 = m.hexdigest()

        if username not in backend.get_users():
            flash('Invalid credentials 1', 'error')
        elif backend.get_password(username) != password_md5:
            flash('Invalid credentials 2', 'error')
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out', 'success')
    return redirect(url_for('login'))
