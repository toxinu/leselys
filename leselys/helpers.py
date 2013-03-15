# coding: utf-8
import sys
import datetime

from functools import wraps

import leselys

from flask import redirect
from flask import request
from flask import session
from flask import url_for

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
	if parsed_date[4] == "0":
		_min = "00"
	else:
		_min = parsed_date[4]
	return {'year': parsed_date[0],
			'month': parsed_date[1],
			'day': parsed_date[2],
			'hour': parsed_date[3],
			'min': parsed_date[4]}

# Decorator for webapp
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

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
