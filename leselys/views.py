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
from flask import make_response

from leselys.helpers import login_required

backend = leselys.core.backend
app = leselys.core.app
reader = leselys.core.reader
signer = leselys.core.signer

# Each template context have the subscriptions list
# Context which return subscriptions list to every template
@app.context_processor
def get_subscriptions():
	return dict(subscriptions=reader.get_subscriptions())

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
	_settings = backend.get_settings()
	return render_template('settings.html', settings=_settings)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember', False)
        m = hashlib.md5()
        m.update(password)
        password_md5 = m.hexdigest()

        if username not in backend.get_users():
            return render_template('login.html')
        elif backend.get_password(username) != password_md5:
            return render_template('login.html')
        else:
            session['logged_in'] = True
            rsp = make_response(redirect(url_for('home')))
            if remember:
                session.permanent = True
                rsp.set_cookie('remember', True)
                rsp.set_cookie('username', username)
                rsp.set_cookie('token', signer.sign(password_md5))
            return rsp
            #return redirect(url_for('home'))
    else:
        if session.get('logged_in'):
            return redirect(url_for('home'))
        if request.cookies.get('remember'):
            username = request.cookies.get('username')
            password_md5 = request.cookies.get('password')
            if username in backend.get_users():
                try:
                    password_unsigned = signer.unsign(password_md5, max_age=15*24*60*60)
                except:
                    return redirect(url_for('login'))
                if password_unsigner == backend.get_password(username):
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
    #return redirect(url_for('login'))