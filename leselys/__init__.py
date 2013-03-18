# coding: utf-8

__title__ = 'leselys'
__version__ = '0.1.5'
__author__ = 'Geoffrey Lehée'
__license__ = ''
__copyright__ = 'Copyright 2013 Geoffrey Lehée'

from leselys.core import Core

defaults = {'host': '127.0.0.1',
            'port': 5000,
            'debug': False}

core = Core(**defaults)
