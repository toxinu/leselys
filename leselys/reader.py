#!/usr/bin/env python
# coding: utf-8
import feedparser
import threading
import time

from leselys.core import db

if not db.settings.find_one().get('acceptable_elements', False):
	settings = db.settings.find_one()
	settings['acceptable_elements'] = ["object","embed","iframe"]
	db.settings.remove(settings['_id'])
	db.settings.save(settings)

acceptable_elements = db.settings.find_one().get('acceptable_elements', [])

for element in acceptable_elements:
	feedparser._HTMLSanitizer.acceptable_elements.add(element)

class Retriever(threading.Thread):
	def __init__(self, title, data=None):
		threading.Thread.__init__(self)
		self.title = title
		self.data = data

	def run(self):
		feed = db.subscriptions.find_one({'title': self.title})
		feed_id = feed['_id']

		if self.data is None:			
			url = feed['url']
			self.data = feedparser.parse(url)['entries']

		for entrie in self.data:
			title = entrie['title']
			link = entrie['link']
			try:
				description = entrie['content'][0]['value']
			except KeyError:
				description = entrie['summary']
			published = entrie['published']

			_id = db.entries.save({'title':title,'link':link,'description':description,'published':published,'feed_id':feed_id,'read':False})

class Reader(object):
	def __init__(self):
		pass

	def add(self, url):
		r = feedparser.parse(url)
		title = r['feed']['title']
		
		feed_id = db.subscriptions.find_one({'title':title})
		if not feed_id:
			if r.feed.update:
				feed_id = db.subscriptions.save({'url':url, 'title': title, 'last_update': r.feed.updated, 'read': False})
			else:
				feed_id = db.subscriptions.save({'url':url, 'title': title, 'last_update': None, 'read': False})
		else:
			return {'success':False}

		retriever = Retriever(title=title, data=r['entries'])
		retriever.start()

		return {'success':True,'title':title,'feed_id':feed_id}

	def delete(self, title):
		try:
			_id = db.subscriptions.find_one({'title':title})['_id']
			db.remove(_id)
		except:
			pass

	def get(self, feed_id):

		res = []
		for entrie in db.entries.find({'feed_id':feed_id}):
			res.append({"title":entrie['title'],"_id":entrie['_id'],"read":entrie['read']})

		return res

	def get_subscriptions(self):
		subscriptions = []
		for sub in db.subscriptions.find():
			subscriptions.append({'title':sub['title'],'id':sub['_id']})
		return subscriptions

	def refreshAll(self):
		for subscription in db.subscriptions.find():
			r = feedparser.parse(subscription['url'])

			print(subscription['last_update'])
			feed_update = subscription['last_update']
			if r.published_parsed > feed_update:
				print('NEW RSS')
			else:
				print('UP TO DATE')
			
			#self.get(subscription['title'])

	def read(self, entry_id):
		entry = db.entries.find_one({'_id': entry_id})
		db.entries.remove(entry_id)
		entry['read'] = True
		db.entries.save(entry)
		return entry
