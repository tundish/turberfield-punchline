#!/usr/bin/env python3
# encoding: utf-8

# This file is part of turberfield.
#
# Turberfield is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Turberfield is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with turberfield.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import textwrap
import unittest

from turberfield.punchline.build import Build
from turberfield.punchline.site import Site


FRAGMENT = """{
    "version": "https://jsonfeed.org/version/1.1",
    "title": "My Example Feed",
    "home_page_url": "https://example.org/",
    "feed_url": "https://example.org/feed.json",
    "description": "",
    "user_comment": "",
    "icon": "",
    "favicon": "",
    "authors": [
        {
            "name": "",
            "url": "",
            "avatar": "",
        }
    ],
    "language": "",
    "expired": "",
    "hubs": [
        {
            "type": "",
            "url": "",
        }
    ],
    "items": [
        {
            "id": "2",
            "content_text": "This is a second item.",
        },
        {
            "id": "1",
            "title": "",
            "summary": "",
            "image": "",
            "date_published": "",
            "date_modified": "",
            "content_html": "<p>Hello, world!</p>",
            "url": "https://example.org/initial-post",
            "authors": [
                {
                    "name": "",
                    "url": "",
                    "avatar": "",
                }
            ],
            "tags": [
                "",
            ],
            "attachments": [
                {
                    "url": "",
                    "mime_type": "",
                    "title": "",
                    "size_in_bytes": 0,
                    "duration_in_seconds": 3,
                },
            ],
        }
    ]
}"""

class TestBuild(unittest.TestCase):

    def test_lifecycle_parse_error(self):
        data = {"made_at": "202-07-26 18:00", "view_at": "2020-07-27", "edit_at": "2020-07-31T13:28:03"}
        with self.assertRaises(ValueError) as err:
            rv = Build.lifecycle(data)

        self.assertTrue("2020-07-31T13:28:03" in str(err.exception))

    def test_lifecycle_no_defaults(self):
        data = {"made_at": "2020-07-26 18:00", "view_at": "2020-07-27", "edit_at": "2020-07-31 13:28:03"}
        rv = Build.lifecycle(data)
        self.assertIsInstance(rv, Site.Lifecycle)
        self.assertIsInstance(rv.made_at, datetime.datetime)
        self.assertIsInstance(rv.view_at, datetime.datetime)
        self.assertIsInstance(rv.edit_at, datetime.datetime)
        self.assertIsNone(rv.drop_at)

    def test_lifecycle_with_defaults(self):
        defaults = Site.Lifecycle(None, None, None, datetime.datetime.now())
        data = {"made_at": "2020-07-26 18:00", "view_at": "2020-07-27", "edit_at": "2020-07-31 13:28:03"}
        rv = Build.lifecycle(data, defaults)
        self.assertIsInstance(rv, Site.Lifecycle)
        self.assertIsInstance(rv.made_at, datetime.datetime)
        self.assertIsInstance(rv.view_at, datetime.datetime)
        self.assertIsInstance(rv.edit_at, datetime.datetime)
        self.assertIsInstance(rv.drop_at, datetime.datetime)

