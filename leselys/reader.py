#!/usr/bin/env python
# coding: utf-8
import feedparser

from leselys.core import db

class Reader(object):
	def __init__(self):
		pass

	def add(self, url):
		title = feedparser.parse(url)['feed']['title']
		if not db.subscriptions.find_one({'title':title}):
			db.subscriptions.save({'url':url, 'title': title})
		return title

	def delete(self, title):
		try:
			_id = db.subscriptions.find_one({'title':title})['_id']
			db.remove(_id)
		except:
			pass

	def get(self, title):
		url = db.subscriptions.find_one({'title': title})['url']
		r = feedparser.parse(url)['entries']
		res = []
		for entrie in r:
			title = entrie['title']
			link = entrie['link']
			description = entrie['description']
			published = entrie['published']

			res.append({'title':title,'link':link,'description':description,'published':published})

		return res

	def get_subscriptions(self):
		subscriptions = []
		for sub in db.subscriptions.find():
			subscriptions.append(sub['title'])
		return subscriptions
