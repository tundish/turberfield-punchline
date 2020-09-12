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

from collections import defaultdict
import datetime
import itertools
import logging
import operator
import pathlib
import uuid

from turberfield.dialogue.model import SceneScript

import turberfield.punchline
from turberfield.punchline.site import Site
from turberfield.punchline.theme import Theme
from turberfield.punchline.types import Eponymous


class Build:

    @staticmethod
    def lifecycle(data: dict, defaults: Site.Lifecycle=None):
        defaults = defaults._asdict() if defaults else {}
        formats = {10: "%Y-%m-%d", 16: "%Y-%m-%d %H:%M", 19: "%Y-%m-%d %H:%M:%S"}
        timestamps = [(k, data.get(k)) for k in Site.Lifecycle._fields if k.endswith("_at")]
        datetimes = [
            datetime.datetime.strptime(v, formats[len(v)])
            if v and len(v) in formats else defaults.get(k) for k, v in timestamps
        ]
        return Site.Lifecycle(*datetimes)

    @staticmethod
    def write_folder_id(path):
        uid_path = path.joinpath("uuid.hex")
        if uid_path.is_file():
            return uuid.UUID(hex=uid_path.read_text().strip())
        else:
            rv = uuid.uuid4()
            uid_path.write_text(rv.hex)
            return rv

    @staticmethod
    def build_pages(text, uid=None, path:pathlib.Path=None, name="inline", now=None):
        uid = uid or uuid.uuid4()
        path = path or pathlib.Path(".")
        now = now or datetime.datetime.now()
        script = SceneScript(path, doc=SceneScript.read(text, name=name))
        ensemble = list(Eponymous.create(script))
        script.cast(script.select(ensemble))
        model = script.run()
        lc = Build.lifecycle(dict(model.metadata))
        data = Site.multidict(model.metadata)
        for n, (scene, shots) in enumerate(itertools.groupby(model.shots, key=operator.attrgetter("scene"))):
            yield Site.Page(
                (lc.view_at or lc.made_at or now, name, n), None,
                Theme.slug(name), Theme.slug(scene), lc, scene, model,
                text=None, html=None, path=None,
                feeds=frozenset(Site.feeds_from_script(model) or ["all"]),
                tags=frozenset(v.lower() for k, v in model.metadata if k.lower() == "tag")
            )

    @staticmethod
    def find_pages(root: pathlib.Path):
        for parent in {i.parent for i in root.glob("**/*.rst")}:
            uid = Build.write_folder_id(parent)
            for path in parent.glob("*.rst"):
                yield from Build.build_pages(path.read_text(), uid=uid, path=path, name=path.stem)

    @staticmethod
    def filter_pages(pages, now=None):
        now = now or datetime.datetime.now()
        for page in sorted(pages, key=operator.attrgetter("key")):
            if not page.lifecycle.view_at or page.lifecycle.view_at <= now:
                if not page.lifecycle.drop_at or page.lifecycle.drop_at > now:
                    yield page


    @staticmethod
    def feeds_from_pages(pages, default=None, keys=("category", "feed")):
        rv = defaultdict(set)
        for page in pages:
            if default:
                rv[default].add(page)
            for k, v in page.model.metadata:
                if k.lower() in keys:
                    rv[v.lower()].add(page)
        return rv
