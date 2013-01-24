#!/usr/bin/env python
# coding: utf-8
import feedparser
import threading

from leselys.core import db
from leselys.helpers import u
from leselys.helpers import get_datetime
from leselys.helpers import get_dicttime

####################################################################################
# Set defaults settings
####################################################################################
if not db.settings.find_one().get('acceptable_elements', False):
	settings = db.settings.find_one()
	settings['acceptable_elements'] = ["object","embed","iframe"]
	db.settings.remove(settings['_id'])
	db.settings.save(settings)

# Acceptable elements are special tag that you can disable in entries rendering
acceptable_elements = db.settings.find_one().get('acceptable_elements', [])

for element in acceptable_elements:
	feedparser._HTMLSanitizer.acceptable_elements.add(element)

####################################################################################
# Retriever object
####################################################################################
class Retriever(threading.Thread):
	""" The Retriever object have to retrieve all feeds asynchronously and return it to
	the Reader when a new subscription arrived """

	def __init__(self, title, data=None):
		threading.Thread.__init__(self)
		self.title = title
		self.data = data

	def run(self):
		feed = db.subscriptions.find_one({'title': self.title})
		feed_id = u(feed['_id'])

		if self.data is None:
			url = feed['url']
			self.data = feedparser.parse(url)['entries']

		for entry_id, entry in enumerate(self.data):
			title = entry['title']
			link = entry['link']
			try:
				description = entry['content'][0]['value']
			except KeyError:
				description = entry['summary']

			last_update = get_dicttime(entry.updated_parsed)

			if entry.get('published_parsed', False):
				published = get_dicttime(entry.published_parsed)
			else:
				published = None

			_id = db.entries.save({
					'entry_id': entry_id,
					'title':title,
					'link':link,
					'description':description,
					'published':published,
					'last_update':last_update,
					'feed_id':feed_id,
					'read':False})

class Refresher(threading.Thread):
	""" The Refresher object have to retrieve all new entries asynchronously """

	def __init__(self, feed_id, data=None):
		threading.Thread.__init__(self)
		self.feed_id = u(feed_id)
		self.data = data

	def run(self):
		if self.data is None:
			feed = db.subscriptions.find_one({'_id': self.feed_id})
			self.data = feedparser.parse(feed['url'])

		readed = []
		for entry in db.entries.find({'feed_id':self.feed_id}):
			if entry['read']:
				readed.append(entry['title'])
			db.entries.remove(entry['_id'])

		retriever = Retriever(title=self.data.feed['title'], data=self.data.entries)
		retriever.start()
		retriever.join()

		for entry in db.entries.find({'feed_id':self.feed_id}):
			if entry['title'] in readed:
				entry['read'] = True
				db.entries.remove(entry['_id'])
				db.entries.save(entry)
				readed.pop(entry['_id'])

####################################################################################
# Reader object
####################################################################################
class Reader(object):
	""" The Reader object is the subscriptions manager, it handle all new feed, read/unread
	state and refresh feeds"""

	def add(self, url):
		url = url.strip()
		r = feedparser.parse(url)

		# Bad feed
		if not r.feed.get('title', False):
			return {'success': False, 'output':'Bad feed'}

		title = r.feed['title']

		feed_id = db.subscriptions.find_one({'title':title})
		if not feed_id:
			feed_update = get_dicttime(r.feed.updated_parsed)
			feed_id = db.subscriptions.save({'url':url, 'title': title, 'last_update': feed_update, 'read': False})
		else:
			return {'success':False, 'output':'Feed already exists'}

		retriever = Retriever(title=title, data=r['entries'])
		retriever.start()

		return {'success':True,'title':title,'feed_id':feed_id,'output':'Feed added'}

	def delete(self, title):
		try:
			_id = db.subscriptions.find_one({'title':title})['_id']
			db.remove(_id)
		except:
			pass

	def get(self, feed_id):
		res = []
		for entry in db.entries.find({'feed_id':feed_id}):
			res.append({"title":entry['title'],"_id":entry['_id'],"read":entry['read']})
		return res

	def get_subscriptions(self):
		subscriptions = []
		for sub in db.subscriptions.find():
			subscriptions.append({'title':sub['title'],'id':sub['_id'], 'counter':self.get_unread(sub['_id'])})
		return subscriptions

	def refresh_all(self):
		for subscription in db.subscriptions.find():
			r = feedparser.parse(subscription['url'])

			local_update = get_datetime(subscription['last_update'])
			remote_update = get_datetime(r.feed.updated_parsed)

			if remote_update > local_update:
				print('Update feed: %s' % subscription['title'])
				refresher = Refresher(subscription['_id'], r)
				refresher.start()

	def get_entry(self, entry_id):
		entry = db.entries.find_one({'_id': entry_id})
		return entry['content']

	def get_unread(self, feed_id):
		res = 0
		for i in db.entries.find({'feed_id':feed_id, 'read':False}):
			res += 1
		return res

	def read(self, entry_id):
		state = False
		entry = db.entries.find_one({'_id': entry_id})
		db.entries.remove(entry['_id'])
		if entry['read']:
			state = False
		entry['read'] = True
		db.entries.save(entry)
		return entry

	def unread(self, entry_id):
		entry = db.entries.find_one({'_id': entry_id})
		db.entries.remove(entry_id)
		entry['read'] = False
		db.entries.save(entry)
		return True
