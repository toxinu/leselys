from __future__ import absolute_import

import unittest

from ._storage import Storage


class StorageTestCase(unittest.TestCase):
    # Tests for leselys.backends._storage.Storage

    def test_api(self):
        # Basic API for any Storage backend.
        obj = Storage()
        obj.is_valid_password
        obj.update_password
