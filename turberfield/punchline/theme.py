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


from collections import defaultdict
from collections import namedtuple
import importlib
import importlib.resources
import inspect
import itertools
import logging
import operator
import pathlib
import shutil
import string

from turberfield.dialogue.model import Model
from turberfield.punchline.presenter import Presenter
from turberfield.punchline.render import Renderer
from turberfield.punchline.site import Site
from turberfield.punchline.types import Settings
from turberfield.punchline.widget import Widget
from turberfield.punchline.widget import ListOfContents
from turberfield.punchline.widget import WebBadge


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
    def frame_path(location, frame, ordinal, fmt=None):
        if fmt:
            return location.joinpath(Theme.slug(frame["scene"]), fmt.format(ordinal)).with_suffix(".html")
        else:
            return location.joinpath(Theme.slug(frame["scene"]), Theme.slug(frame["name"])).with_suffix(".html")

    @staticmethod
    def slug(text, table="".maketrans({i: i for i in string.ascii_letters + string.digits + "_-"})):
        mapping = {ord(i): None for i in text}
        mapping.update(table)
        mapping[ord(" ")] = "-"
        return text.translate(mapping).lower()

    def __init__(self, cfg=None, output=None, parent_package=None, **kwargs):
        self.cfg = cfg
        self.output = output or pathlib.Path(".")
        self.parent_package = parent_package
        theme_section = (
            {k: v for k, v in self.cfg["theme"].items() if k not in self.cfg[self.cfg.default_section]}
            if self.cfg and "theme" in self.cfg else {}
        )
        self.settings = Settings(**dict(self.definitions, **theme_section))
        Widget.register(
            ListOfContents("turberfield.punchline", config="jsonfeed.org", optional=False, output=output)
        )
        Widget.register(
            WebBadge("turberfield.punchline", "assets", config="turberfield.punchline")
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for w in self.widgets:
            if w.config in self.cfg:
                for resource in w.resources:
                    with importlib.resources.path(w.package, resource) as path:
                        shutil.copytree(path, self.output.joinpath(resource), dirs_exist_ok=True)
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

    @property
    def widgets(self):
        return [i for i in Widget.catalogue if not (i.optional and i.config not in self.cfg)]

    @property
    def is_refresh_enabled(self):
        return getattr(self.settings, "punchline-states-refresh", "").lower() != "none"

    def expand(self, page, *args, fragments=[], **kwargs):
        presenter = Presenter(page.model)
        fragments = {key: filter(None, values) for key, *values in zip(Widget.Fragment._fields, *fragments)}

        metadata = Site.multidict(page.model.metadata)
        dwell = float(next(reversed(metadata["dwell"]), "0.3"))
        pause = float(next(reversed(metadata["pause"]), "1.0"))
        nodes = next(reversed(metadata["nodes"]), "")
        has_nav = not any(i for i in self.handlers if i.split(".")[0] == page.path.stem)
        for n, frame in enumerate(presenter.frames):
            frame = presenter.animate(frame, dwell, pause, react=True)
            text = "\n".join(itertools.chain((self.render_frame_to_text(frame), ), fragments["text"]))

            if self.is_refresh_enabled and n < len(presenter.frames) - 1:
                next_frame = self.frame_path(
                    self.output, presenter.frames[n + 1], n + 1, fmt=nodes
                ).relative_to(self.output).as_posix()
            else:
                next_frame = None

            body = "\n".join(itertools.chain(
                (self.render_frame_to_html(
                    frame, title=page.title.capitalize(), final=(next_frame is None and has_nav)
                ), ),
                fragments["body"])
            )

            html = self.render_body_html(
                next_= next_frame,
                refresh=Presenter.refresh_animations(frame) if presenter.pending else None,
                title=page.title.capitalize(),
            ).format(
                "\n".join(fragments["head"]),
                self.render_dict_to_css(vars(self.settings)),
                body
            )

            path = self.frame_path(self.output, frame, n, fmt=nodes)
            yield page._replace(ordinal=n, text=text, html=html, path=path)

    @property
    def handlers(self):
        return {
            "index.rst": self.cover,
            "about.rst": self.cover,
            "contact.rst": self.cover,
        }

    def cover(self, page, feeds: dict, tags: dict, *args, **kwargs):
        logging.info("Found handler for {0.path}".format(page))
        fragments = [Widget.Fragment(
            head="\n".join([
                '<link rel="alternate" type="application/json" title="{feed_title}" href="{feed_url}" />'.format(
                    **self.get_feed_settings(f)
                )
            for f in feeds]),
            style=None, body=None, text=None
        )]
        fragments += [
            w(page, feeds, tags, **dict(self.cfg[w.config].items()) if w.config in self.cfg else {})
            for w in self.widgets
        ]

        title = self.cfg[self.cfg.default_section]["site_title"]
        rv = list(self.expand(page._replace(title=title), fragments=fragments))
        rv.insert(0, rv[0]._replace(path=self.output.joinpath(page.path.stem).with_suffix(".html")))
        yield from rv

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
            sorted(pages, key=lambda x: x.key + (x.ordinal,)), key=operator.attrgetter("key")
        )}
        for _, series in sorted(items.items()):
            page = series[0]
            metadata = Site.multidict(page.model.metadata)
            page_path = page.path.relative_to(self.output).as_posix() if self.output else page.path
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
