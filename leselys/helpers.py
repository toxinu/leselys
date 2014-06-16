# coding: utf-8
import sys
import datetime

from functools import wraps

import leselys

from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask import jsonify

from leselys.externals import opml
from xml.sax.saxutils import escape as escape_xml

# Unicode python 2-3
if sys.version < '3':
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x


# Date helpers
def get_datetime(unparsed_date):
    if isinstance(unparsed_date, dict):
        return datetime.datetime(
            unparsed_date['year'],
            unparsed_date['month'],
            unparsed_date['day'],
            unparsed_date['hour'],
            unparsed_date['min'],
            tzinfo=None)
    else:
        return datetime.datetime(
            unparsed_date[0],
            unparsed_date[1],
            unparsed_date[2],
            unparsed_date[3],
            unparsed_date[4],
            tzinfo=None)


def get_dicttime(parsed_date):
    return {'year': parsed_date.year,
            'month': parsed_date.month,
            'day': parsed_date.day,
            'hour': parsed_date.hour,
            'min': parsed_date.minute}


# Decorator for webapp
def login_required(f):
    storage = leselys.core.storage
    signer = leselys.core.signer

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # No password setted
        if not storage.get_password():
            if request.args.get('jsonify', "false") == "false":
                return redirect(url_for('welcome'))
            else:
                return jsonify(success=False, output="You need to set a password.")

        # Not in cache
        if not session.get('logged_in'):
            # No cookie
            if request.cookies.get('remember') == "false":
                if request.args.get('jsonify', "false") == "false":
                    return redirect(url_for('login_view'))
                else:
                    return jsonify(success=False, output="Failed to log in.")
            else:
                password_md5 = "%s.%s" % (storage.get_password(), request.cookies.get('token'))
                try:
                    password_unsigned = signer.unsign(
                        password_md5, max_age=15 * 24 * 60 * 60)
                except:
                    if request.args.get('jsonify', "false") == "false":
                        return redirect(url_for('login_view'))
                    else:
                        return jsonify(success=False, output="Failed to log in.")
                if password_unsigned == storage.get_password():
                    return f(*args, **kwargs)
                else:
                    if request.args.get('jsonify', "false") == "false":
                        return redirect(url_for('login_view'))
                    else:
                        return jsonify(success=False, output="Failed to log in.")
        return f(*args, **kwargs)
    return decorated_function


def uncached(view):
    cache = leselys.core.cache
    cache.set('view/%s' % view, None)


def cached(timeout=5 * 60, key='view/%s'):
    cache = leselys.core.cache

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator


def retrieve_feeds_from_opml(opml_raw):
    result = []
    feeds = opml.from_string(opml_raw)
    for outline in feeds:
        if len(outline) > 0:
            for feed in outline:
                if feed.type == 'rss':
                    result.append({'title': feed.text, 'url': feed.xmlUrl})
        else:
            if outline.type == 'rss':
                result.append({'title': outline.text, 'url': outline.xmlUrl})
    return result


def export_to_opml():
    storage = leselys.core.storage
    header = """<?xml version="1.0"?>
<opml version="1.0">
  <head>
    <title>Leselys feeds export</title>
  </head>
  <body>
"""
    body = ""
    footer = """\n</body>\n</opml>"""

    for feed in storage.get_feeds():
        body += """
    <outline text="%s"
        title="%s" type="rss"
        xmlUrl="%s" htmlUrl="%s"/>""" % (
            escape_xml(feed['title']),
            escape_xml(feed['title']),
            escape_xml(feed['url']),
            escape_xml(feed['url']))

    return header + body + footer


def refresh_all():
    from leselys.reader import Refresher
    print(' :: Run refresh task')
    feeds = leselys.core.storage.get_feeds()
    for feed in feeds:
        refresher = Refresher(feed)
        refresher.start()
        refresher.join()


def run_retention(delta_day, story_before_retention):
    storage = leselys.core.storage
    print(' :: Run retention task')
    for feed in storage.get_feeds():
        print("=> %s" % feed['title'].encode('utf-8'))

        stories = storage.get_stories(feed['_id'], 'unreaded', 0, 0)
        nb_stories = len(stories)
        for story in stories:
            if nb_stories <= story_before_retention:
                print('   | No many stories, so I keept it.')
                break
            delta = datetime.datetime.now() - story['last_update']
            print('  | %s (%s days)' % (story['_id'], delta.days))
            if delta.days > delta_day:
                print('    | deleted.')
                storage.remove_story(story['_id'])
                nb_stories -= 1
