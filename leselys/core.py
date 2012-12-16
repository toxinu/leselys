#!/usr/bin/env python
# coding: utf-8
from leselys.logger import stream_logger
from sofart import Database

db = Database('/tmp/lesesys.db')

from leselys.reader import Reader
reader = Reader()
