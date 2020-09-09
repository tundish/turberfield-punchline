import pathlib
import textwrap
import unittest

from uncarved.lockdown.build import build_pages
from uncarved.lockdown.site import Site
from uncarved.lockdown.theme import Theme


class ThemeTests(unittest.TestCase):

    def test_slug(self):
        text = "ABab234$%^&*-_ "
        rv = Theme.slug(text)
        self.assertEqual("abab234-_-", rv)

    def test_render_multipages(self):
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

        .. fx:: uncarved.lockdown.media  audio/fly_away.mp3
           :offset: 0
           :duration: 8000
           :loop: 12
        
        """)
        pages = list(build_pages(text))
        self.assertEqual(2, len(pages), pages)
        self.assertIsInstance(pages[0], Site.Page)
        self.assertIsInstance(pages[1], Site.Page)

        theme = Theme()
        pages = theme.render({})


class TestPublish(unittest.TestCase):

    def test_empty_feed(self):
        theme = Theme()
        settings = theme.get_feed_settings("")
        self.assertIn("feed_url", settings)
        self.assertIn("feed_title", settings)

        rv = theme.publish([], **settings)
        self.fail(rv)
