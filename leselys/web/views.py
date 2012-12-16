#!/usr/bin/env python
# coding: utf-8
import os
import feedparser

from leselys.core import db
from leselys.core import reader
from leselys.web import app

from flask import render_template, jsonify, g, request

@app.context_processor
def get_subscriptions():
	return dict(subscriptions=reader.get_subscriptions())

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/add', methods=['POST'])
def add():
	title = reader.add(request.form['url'])
	return jsonify(success=True, name=title)

@app.route('/api/get/<name>')
def get(name):
	content = reader.get(name)
	print(content)
	return jsonify(content=reader.get(name))

@app.route('/dump')
def dump():
	for r in db.subscriptions.find():
		print(r)
	return 'dumped'