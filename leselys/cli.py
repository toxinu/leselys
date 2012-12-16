#!/usr/bin/env python
# coding: utf-8

import sys

from leselys.core import stream_logger

class Cli(object):
	def __init__(self, *args, **kwargs):
		self.args = kwargs
		stream_logger.disabled = False

	def start(self):
		pass