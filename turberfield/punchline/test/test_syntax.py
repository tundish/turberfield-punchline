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

import textwrap
import unittest

from turberfield.punchline.build import Build
from turberfield.punchline.site import Site
from turberfield.punchline.theme import Theme
from turberfield.punchline.types import Settings


class SyntaxTests(unittest.TestCase):

    def setUp(self):
        cfg = Settings.config_parser()
        self.theme = Theme(cfg)

    def test_tags(self):
        text = textwrap.dedent("""
        :tag: one
        :tag: two

        Title
        =====
        Shot
        ----
        """)
        page = next(Build.build_pages(text, self.theme))
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
        page = next(Build.build_pages(text, self.theme))
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
        page = next(Build.build_pages(text, self.theme))
        self.assertEqual(1, len(page.model.shots))
        self.assertEqual(1, len(page.model.shots[0].items))
        self.assertNotIn("B", page.model.shots[0].items[0].text)
        self.assertNotIn("C", page.model.shots[0].items[0].text)
