#!/usr/bin/env python3
# encoding: UTF-8

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
from collections import defaultdict
from collections import namedtuple
import itertools
import logging
import operator
import pathlib
import string

from turberfield.dialogue.model import Model
from turberfield.punchline.presenter import Presenter
from turberfield.punchline.render import Renderer
from turberfield.punchline.site import Site
from turberfield.punchline.types import Settings


Lifecycle = namedtuple("Lifecycle", ["made_at", "view_at", "edit_at", "drop_at"])
Page = namedtuple(
    "Page", [
        "key", "ordinal", "script_slug", "scene_slug", "lifecycle",
        "title", "model",
        "text", "html",
        "path",
        "feeds", "tags",
    ]
)


class Theme(Renderer):

    @staticmethod
    def frame_path(page, ordinal):
        return page.path.joinpath(page.script_slug, page.scene_slug, f"{ordinal:03d}").with_suffix(".html")

    @staticmethod
    def slug(text, table="".maketrans({i: i for i in string.ascii_letters + string.digits + "_-"})):
        mapping = {ord(i): None for i in text}
        mapping.update(table)
        mapping[ord(" ")] = "-"
        return text.translate(mapping).lower()

    def __init__(self, cfg=None, root=None, **kwargs):
        self.cfg = cfg
        self.root = root
        theme_section = self.cfg["theme"] if self.cfg and "theme" in self.cfg else {}
        self.settings = Settings(**dict(self.definitions, **theme_section))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    def get_feed_settings(self, feed_name):
        try:
            section = self.cfg[feed_name]
        except KeyError:
            section = self.cfg[self.cfg.default_section]
        except TypeError:
            return {"site_url": "/", "feed_name": "all", "feed_url": "/feed.json", "feed_title": "JSON Feed"}

        return section

    @property
    def definitions(self):
        return dict()

    def expand(self, articles, *args, **kwargs):
        self.root = self.root or pathlib.Path(*min(i.path.parts for i in articles))
        for page in articles:
            presenter = Presenter(page.model)
            for n, frame in enumerate(presenter.frames):
                frame = presenter.animate(frame)
                next_frame = self.frame_path(page, n + 1).relative_to(page.path).as_posix()
                text = self.render_frame_to_text(frame)
                html = self.render_body_html(
                    next_= next_frame if n < len(presenter.frames) -1 else None,
                    refresh=Presenter.refresh_animations(frame) if presenter.pending else None,
                    title=page.title.capitalize(),
                ).format(
                    "",
                    self.render_dict_to_css(vars(self.settings)),
                    self.render_frame_to_html(
                        frame, title=page.title.capitalize(), final=(n == len(presenter.frames) - 1)
                    )
                )
                path = self.frame_path(page, n)
                yield page._replace(ordinal=n, text=text, html=html, path=path)

    def cover(self, pages, feeds: dict, tags: Counter, *args, **kwargs):
        """
        Nav: tag cloud and article list
        Article: Summary view of article

        """
        self.root = self.root or pathlib.Path(*min(i.path.parts for i in articles))
        feed_settings = {i: self.get_feed_settings(i) for i in feeds}
        feed_links = "\n".join([
            '<link rel="alternate" type="application/json" title="{0[feed_title]}" href="{0[feed_url]}" />'.format(i)
            for i in feed_settings.values()
        ])
        #TODO A deque for each zone on the cover page. They get passed to each Facade in turn
        # Facade decides; section aside main. Class is allocated by name.
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

    def publish(self, pages, *, site_url, feed_name, feed_url, feed_title, **kwargs):
        rv = {
            "version": "https://jsonfeed.org/version/1.1",
            "title": feed_title,
            "feed_url": feed_url,
            "authors": [],
            "hubs": [],
            "items": [],
        }

        items = {k: list(v) for k, v in itertools.groupby(
            sorted(pages, key=operator.attrgetter("key")), key=operator.attrgetter("key")
        )}
        for _, series in sorted(items.items()):
            page = series[0]
            metadata = Site.multidict(page.model.metadata)
            page_path = page.path.relative_to(self.root).as_posix() if self.root else page.path
            item = {
                "id": f"{site_url}{page_path}",
                "url": f"{site_url}{page_path}",
                "title": page.title.title(),
                "content_text": "\n".join([i.text or "" for i in series]),
                "content_html": page.html,
            }
            if page.lifecycle.view_at:
                item["date_published"] = page.lifecycle.view_at.date().isoformat()
            if page.lifecycle.edit_at:
                item["date_modified"] = page.lifecycle.edit_at.isoformat()
            if "summary" in metadata:
                item["summary"] = "\n".join(metadata["summary"])
            if "author" in metadata:
                item["authors"] = [{"name": i} for i in metadata["author"]]

            #attachments = [i for i in page.model.shots if isinstance(i, (Model.Audio, Model.Still))]
            rv["items"].append(item)
        return rv

