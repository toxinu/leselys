#!/usr/bin/env python
# coding: utf-8
import os

from leselys.logger import stream_logger
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI', 'localhost')

connection = MongoClient(MONGO_URI)
db = connection['leselys']

from leselys.reader import Reader
reader = Reader()
