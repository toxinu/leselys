#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import unittest

from flask import request

from leselys import core
from leselys.backends.storage.tests import *


core.app.config['TESTING'] = True


class TestLeselysAPI(unittest.TestCase):

    def setUp(self):
        core.load_config('config.ini')
        core.load_storage()
        core.load_session()
        core.load_wsgi()

        self.r = core.app.test_client()

    def test_01_home(self):
        with self.r as c:
            rv = c.get('/?jsonsify=true')
            print(rv.status_code)
            print(rv.data)

if __name__ == "__main__":
    unittest.main()
