import textwrap
import unittest

from uncarved.lockdown.build import build_pages
from uncarved.lockdown.site import Site


class SyntaxTests(unittest.TestCase):

    def test_tags(self):
        text = textwrap.dedent("""
        :tag: one
        :tag: two

        Title
        =====
        Shot
        ----
        """)
        page = next(build_pages(text))
        rv = page.model.metadata
        self.assertEqual(2, len(rv))
        self.assertTrue(all(k == "tag" for k, v in rv))

    def test_multidict(self):
        text = textwrap.dedent("""
        :tag: one
        :tag: two

        Title
        =====
        Shot
        ----
        """)
        page = next(build_pages(text))
        rv = Site.multidict(page.model.metadata)
        self.assertEqual(1, len(rv))
        self.assertEqual(["one", "two"], rv["tag"])

    def test_scenescript_means_no_further_titling(self):
        text = textwrap.dedent("""
        :tag: one
        :tag: two

        Scene
        +++++

        Shot
        ====

        A

        Title
        -----

        B

        Subtitle
        ````````

        C
        """)
        page = next(build_pages(text))
        self.assertEqual(1, len(page.model.shots))
        self.assertEqual(1, len(page.model.shots[0].items))
        self.assertNotIn("B", page.model.shots[0].items[0].text)
        self.assertNotIn("C", page.model.shots[0].items[0].text)
