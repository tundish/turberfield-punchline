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

import itertools
import pathlib
import textwrap
import unittest

from turberfield.punchline.build import Build
from turberfield.punchline.site import Site
from turberfield.punchline.theme import Theme
from turberfield.punchline.types import Settings


class ThemeTests(unittest.TestCase):

    def test_slug(self):
        text = "ABab234$%^&*-_ "
        rv = Theme.slug(text)
        self.assertEqual("abab234-_-", rv)

    def test_settings(self):
        cfg = Settings.config_parser()
        theme = Theme(cfg)
        self.assertTrue(hasattr(theme, "settings"))
        self.assertIsInstance(theme.settings, Settings)
        self.assertTrue(hasattr(theme.settings, "id"))
 
    def test_expand_multipages(self):
        text = textwrap.dedent("""
        Page One
        ========

        Shot One
        --------

        The text.

        .. fx:: tor.static.img  street.jpg
           :offset: 0
           :duration: 0

        Page Two
        ========

        Shot Two
        --------

        More text.

        .. fx:: turberfield.punchline.media  audio/fly_away.mp3
           :offset: 0
           :duration: 8000
           :loop: 12

        """)
        cfg = Settings.config_parser()
        theme = Theme(cfg)
        pages = list(Build.build_pages(text, theme))
        self.assertEqual(2, len(pages), pages)
        self.assertIsInstance(pages[0], Site.Page)
        self.assertIsInstance(pages[1], Site.Page)

        theme = Theme()
        rv = list(itertools.chain.from_iterable(theme.expand(i) for i in pages))
        self.assertEqual(4, len(rv), rv)


class TestPublish(unittest.TestCase):

    def test_empty_feed(self):
        theme = Theme()
        settings = theme.get_feed_settings("")
        self.assertIn("feed_url", settings)
        self.assertIn("feed_title", settings)

        rv = theme.publish([], **settings)
        self.assertEqual("https://jsonfeed.org/version/1.1", rv.get("version"))

    def test_publish_multipages(self):
        text = textwrap.dedent("""
        Page One
        ========

        Shot One
        --------

        The text.

        .. fx:: tor.static.img  street.jpg
           :offset: 0
           :duration: 0

        Page Two
        ========

        Shot Two
        --------

        More text.

        .. fx:: turberfield.punchline.media  audio/fly_away.mp3
           :offset: 0
           :duration: 8000
           :loop: 12

        """)
        cfg = Settings.config_parser()
        theme = Theme(cfg)
        pages = list(Build.build_pages(text, theme))
        self.assertEqual(2, len(pages), pages)
        self.assertIsInstance(pages[0], Site.Page)
        self.assertIsInstance(pages[1], Site.Page)

        theme = Theme()
        pages = itertools.chain.from_iterable(theme.expand(i) for i in pages)
        settings = theme.get_feed_settings("all")
        feed = theme.publish(pages, **settings)
        self.assertEqual(2, len(feed["items"]))

    def test_publish_multishots(self):
        text = textwrap.dedent("""
        Page One
        ========

        Shot One
        --------

        The text.

        .. fx:: tor.static.img  street.jpg
           :offset: 0
           :duration: 0

        Shot Two
        --------

        More text.

        .. fx:: turberfield.punchline.media  audio/fly_away.mp3
           :offset: 0
           :duration: 8000
           :loop: 12

        """)
        cfg = Settings.config_parser()
        theme = Theme(cfg)
        pages = list(Build.build_pages(text, theme))
        self.assertEqual(1, len(pages), pages)
        self.assertIsInstance(pages[0], Site.Page)

        theme = Theme()
        pages = itertools.chain.from_iterable(theme.expand(i) for i in pages)
        settings = theme.get_feed_settings("all")
        feed = theme.publish(pages, **settings)
        self.assertEqual(1, len(feed["items"]))
