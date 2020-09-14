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

import importlib
import importlib.resources
import logging
import pathlib
import shutil
import sys

from turberfield.dialogue.model import Model
from turberfield.punchline.presenter import Presenter
from turberfield.punchline.site import Site
from turberfield.punchline.theme import Theme
import turberfield.punchline.themes.january.render as render


class January(Theme):

    definitions = {
        #"washout": "hsl(50, 0%, 100%, 1.0)",
        #"shadows": "hsl(37, 93%, 12%, 0.7)",
        #"midtone": "hsl(86, 93%, 12%, 0.7)",
        #"hilight": "hsl(224, 70%, 16%, 0.7)",
        #"glamour": "hsl(76, 80%, 35%, 1.0)",
        #"gravity": "hsl(36, 20%, 18%, 1.0)",

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

    def __exit__(self, exc_type, exc_val, exc_tb):
        for d in ("css", "fonts"):
            with importlib.resources.path("turberfield.punchline.themes.january", d) as path:
                shutil.copytree(path, self.root.joinpath(d), dirs_exist_ok=True)

        return False

    def render_pages(self, pages, *args, **kwargs):
        for page in pages:
            presenter = Presenter(page.model)
            for n, frame in enumerate(presenter.frames):
                frame = presenter.animate(frame)
                next_frame = self.frame_path(page, n + 1).relative_to(page.path).as_posix()
                text = render.frame_to_text(frame)
                html = render.body_html(
                    next_=next_frame if n < len(presenter.frames) -1 else None,
                    refresh=Presenter.refresh_animations(frame) if presenter.pending else None,
                    title=page.title.capitalize(),
                ).format(
                    "",
                    render.dict_to_css(self.definitions),
                    render.frame_to_html(
                        frame, title=page.title.capitalize(), final=(n == len(presenter.frames) - 1)
                    )
                )
                path = self.frame_path(page, n)
                yield page._replace(ordinal=n, text=text, html=html, path=path)

    def render_with_feeds(self, pages, feeds: dict, *args, **kwargs):
        feed_links = "\n".join([
            '<link rel="alternate" type="application/json" title="{0[feed_title]}" href="{0[feed_url]}" />'.format(i)
            for i in feeds.values()
        ])
        for n, title in enumerate(("index",)):
            yield Site.Page(
                key=(n,), ordinal=0, script_slug=None, scene_slug=None, lifecycle=None,
                title=title.capitalize(),
                model=None,
                text="",
                html=render.body_html(title=title).format(
                    feed_links,
                    render.dict_to_css(self.definitions),
                    render.feed_to_html(pages, self.root, self.cfg),
                ),
                path=self.root.joinpath(title).with_suffix(".html"),
                feeds=tuple(), tags=tuple(),
            )

    def render(self, pages, *args, **kwargs):
        self.root = self.root or pathlib.Path(*min(i.path.parts for i in pages))
        pages = list(self.render_pages(pages, *args, **kwargs))
        feeds = {feed_name: self.get_feed_settings(feed_name) for page in pages for feed_name in page.feeds}
        yield from pages
        yield from self.render_with_feeds(pages, feeds, *args, **kwargs)
