#!/usr/bin/env python
# coding: utf-8
import os

from leselys.logger import stream_logger
from sofart import Database

db = Database('/tmp/leselys.db', mode='single')

from leselys.reader import Reader
reader = Reader()
