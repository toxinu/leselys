#!/usr/bin/env python
# coding: utf-8
import sys
import datetime

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
	return {'year': parsed_date[0],
			'month': parsed_date[1],
			'day': parsed_date[2],
			'hour': parsed_date[3],
			'min': parsed_date[4]}