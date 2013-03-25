#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from leselys import core


from flask import request

core.app.config['TESTING'] = True
core.load_config('config.ini')
core.load_storage()
core.load_session()
core.load_wsgi()

class TestLeselysAPI(unittest.TestCase):

    def setUp(self):
        self.r = core.app.test_client()

    def test_01_home(self):
        with self.r as c:
            rv = c.get('/?jsonsify=true')
            print(rv.status_code)
            print(rv.data)

if __name__ == "__main__":
    unittest.main()
