from __future__ import absolute_import

import unittest

from ._storage import Storage


class StorageTestCase(unittest.TestCase):
    # Tests for leselys.backends._storage.Storage

    def test_api(self):
        # Basic API for any Storage backend.
        obj = Storage()
        obj.add_feed
        obj.add_story
        obj.all_stories
        obj.get_feed_by_id
        obj.get_feed_by_title
        obj.get_feed_count
        obj.get_feed_setting
        obj.get_feed_unread
        obj.get_feed_unread_count
        obj.get_feeds
        obj.get_password
        obj.get_setting
        obj.get_settings
        obj.get_stories
        obj.get_story_by_guid
        obj.get_story_by_id
        obj.get_story_by_title
        obj.is_valid_password
        obj.remove_feed
        obj.remove_story
        obj.set_feed_setting
        obj.set_password
        obj.set_setting
        obj.update_feed
        obj.update_password
        obj.update_story
