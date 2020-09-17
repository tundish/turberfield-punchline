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

from collections import Counter
import importlib
import importlib.resources
import logging
import pathlib
import shutil
import sys

from turberfield.dialogue.model import Model
from turberfield.punchline.site import Site
from turberfield.punchline.theme import Theme


class January(Theme):

    def __exit__(self, exc_type, exc_val, exc_tb):
        for d in ("css", "fonts"):
            with importlib.resources.path("turberfield.punchline.themes.january", d) as path:
                shutil.copytree(path, self.root.joinpath(d), dirs_exist_ok=True)

        return False

    @property
    def definitions(self):
        return {
            "titles": '"Bernier Shade", sans-serif',
            "blocks": '"Bernier Regular", sans-serif',
            "mono": ", ".join([
                "SFMono-Regular", "Menlo", "Monaco",
                "Consolas", '"Liberation Mono"',
                '"Courier New"', "monospace"
            ]),
            "detail": '"Palatino Linotype", "Book Antiqua", Palatino, serif',
            "system": ", ".join([
                "BlinkMacSystemFont", '"Segoe UI"', '"Helvetica Neue"',
                '"Apple Color Emoji"', '"Segoe UI Emoji"', '"Segoe UI Symbol"',
                "Arial", "sans-serif"
            ]),
        }

    def cover(self, pages, feeds: dict, tags: Counter, *args, **kwargs):
        self.root = self.root or pathlib.Path(*min(i.path.parts for i in articles))
        feed_settings = {i: self.get_feed_settings(i) for i in feeds}
        feed_links = "\n".join([
            '<link rel="alternate" type="application/json" title="{0[feed_title]}" href="{0[feed_url]}" />'.format(i)
            for i in feed_settings.values()
        ])
        for n, title in enumerate(("index",)):
            yield Site.Page(
                key=(n,), ordinal=0, script_slug=None, scene_slug=None, lifecycle=None,
                title=title.capitalize(),
                model=None,
                text="",
                html=self.render_body_html(title=title).format(
                    feed_links,
                    self.render_dict_to_css(vars(self.settings)),
                    self.render_feed_to_html(pages, self.root, self.cfg),
                ),
                path=self.root.joinpath(title).with_suffix(".html"),
                feeds=tuple(), tags=tuple(),
            )
