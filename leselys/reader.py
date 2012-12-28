#!/usr/bin/env python
# coding: utf-8
import feedparser
import threading
import time
import datetime

from leselys.core import db

# Set defaults settings
if not db.settings.find_one().get('acceptable_elements', False):
	settings = db.settings.find_one()
	settings['acceptable_elements'] = ["object","embed","iframe"]
	db.settings.remove(settings['_id'])
	db.settings.save(settings)

# Acceptable elements are special tag that you can disable in entrie rendering
acceptable_elements = db.settings.find_one().get('acceptable_elements', [])

for element in acceptable_elements:
	feedparser._HTMLSanitizer.acceptable_elements.add(element)

# Date helpers
def get_datetime(unparsed_date):
	if isinstance(unparsed_date, dict):
		return datetime.datetime(
						unparsed_date['year'],
						unparsed_date['month'],
						unparsed_date['day'],
						unparsed_date['hour'],
						unparsed_date['min']
					)
	else:
		return datetime.datetime(
						unparsed_date[0],
						unparsed_date[1],
						unparsed_date[2],
						unparsed_date[3],
						unparsed_date[4]
					)

def get_dicttime(parsed_date):
	return {'year': parsed_date[0],
			'month': parsed_date[1],
			'day': parsed_date[2],
			'hour': parsed_date[3],
			'min': parsed_date[4]}

class Retriever(threading.Thread):
	""" The Retriever object have to retrieve all feeds asynchronously and return it to
	the Reader when a new subscription arrived """

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
		threading.Thread.__init__(self, data=None)
		self.feed_id = feed_id
		self.data = data

	def run(self):
		feed = db.subscriptions.find_one({'_id': feed_id})
		if self.data is None:
			self.data = feedparser.parse(feed['url'])

		readed = []
		for entry in db.entries.find({'feed_id':self.feed_id}):
			if entry['read']:
				readed.apppend(entry['_id'])
				db.entries.remove(entry['_id'])

		retriever = Retriever(title=self.data['title'], data=self.data)
		retriever.start()
		retriever.join()

		for entry in db.entries.find({'feed_id':self.feed_id}):
			if entry['_id'] in readed:
				entry['read'] = True
				db.entries.remove(entry['_id'])
				db.entries.save(entry)
				readed.pop(entry['_id'])

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
			print(feed_update)

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
		for entrie in db.entries.find({'feed_id':feed_id}):
			res.append({"title":entrie['title'],"_id":entrie['_id'],"read":entrie['read']})

		return res

	def get_subscriptions(self):
		subscriptions = []
		for sub in db.subscriptions.find():
			subscriptions.append({'title':sub['title'],'id':sub['_id']})
		return subscriptions

	def refresh_all(self):
		for subscription in db.subscriptions.find():
			r = feedparser.parse(subscription['url'])

			local_update = get_datetime(subscription['last_update'])
			remote_update = get_datetime(r.updated_parsed)

			print('========')
			print(local_update)
			print(r.updated_parsed)
			print(r.updated)
			print(remote_update)
			print('========')
			if remote_update > local_update:
				refresher = Refresher(subscription['_id'], r)
				refresher.start()

	def get_entry(self, entry_id):
		entry = db.entries.find_one({'_id': entry_id})
		return entry['content']

	def read(self, entry_id):
		entry = db.entries.find_one({'_id': entry_id})
		db.entries.remove(entry_id)
		entry['read'] = True
		db.entries.save(entry)
		return entry

	def unread(self, entry_id):
		entry = db.entries.find_one({'_id': entry_id})
		db.entries.remove(entry_id)
		entry['read'] = False
		db.entries.save(entry)
		return True
