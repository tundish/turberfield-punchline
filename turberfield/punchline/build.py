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
import importlib
import inspect
import itertools
import logging
import operator
import pathlib
import re
import uuid

from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.model import Model

import turberfield.punchline
from turberfield.punchline.site import Site
from turberfield.punchline.theme import Theme
from turberfield.punchline.types import Eponymous
from turberfield.utils.misc import gather_installed


class ModelAssignsStrings(Model):

    def visit_Setter(self, node):
        ref, attr = node["arguments"][0].split(".")
        entity = self.get_entity(ref)
        val = re.compile("\|(\w+)\|").sub(self.substitute_property, node["arguments"][1])
        self.shots[-1].items.append(Model.Property(self.speaker, entity.persona, attr, val))


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
    def build_model(text, theme, uid=None, path:pathlib.Path=None, model_type=ModelAssignsStrings):
        theme.settings.id = uid or theme.settings.id
        path = path or pathlib.Path(".")
        script = SceneScript(path, doc=SceneScript.read(text))
        ensemble = list(Eponymous.create(script)) + [theme.settings]
        script.cast(script.select(ensemble))
        model = model_type(script.fP, script.doc)
        script.doc.walkabout(model)
        return model

    @staticmethod
    def pages_from_model(model, name, path=None, now=None):
        now = now or datetime.datetime.now()
        lc = Build.lifecycle(dict(model.metadata))
        data = Site.multidict(model.metadata)
        for n, (scene, shots) in enumerate(itertools.groupby(model.shots, key=operator.attrgetter("scene"))):
            yield Site.Page(
                (lc.view_at or lc.made_at or now, name, n), None,
                Theme.slug(name), Theme.slug(scene), lc, scene, model,
                text=None, html=None, path=path,
                feeds=frozenset(Site.feeds_from_script(model) or ["all"]),
                tags=frozenset(v.lower() for k, v in model.metadata if k.lower() == "tag")
            )

    @staticmethod
    def build_pages(text, theme, uid=None, path:pathlib.Path=None, name="inline", now=None):
        path = path or pathlib.Path(".")
        model = Build.build_model(text, theme, uid, path)
        yield from Build.pages_from_model(model, name, path, now)

    @staticmethod
    def find_articles(root: pathlib.Path, theme: Theme):
        for parent in {i.parent for i in root.glob("**/*.rst")}:
            uid = Build.write_folder_id(parent)
            for path in parent.glob("*.rst"):
                yield from Build.build_pages(path.read_text(), theme, uid=uid, path=path, name=path.stem)

    @staticmethod
    def find_theme(cfg, output, default="january"):
        name = cfg[cfg.default_section].get("theme", default)
        try:
            theme_module = importlib.import_module(name)
            theme_class = next(
                i for i in vars(theme_module).values()
                if inspect.isclass(i) and issubclass(i, Theme)
                and inspect.getmodule(i) is theme_module
            )
            logging.info("Selected {0.__name__} theme from '{1}'".format(theme_class, name))
        except (ModuleNotFoundError, StopIteration):
            themes = dict(gather_installed("turberfield.interfaces.theme"))
            theme_class = themes.get(name) or themes.get(default)
            logging.info("Selected '{0.__name__}' theme from [ {1} ]".format(theme_class, ",".join(themes.keys())))
            theme_module = inspect.getmodule(theme_class)

        theme_package = ".".join(theme_module.__name__.split(".")[:-1])
        return theme_class and theme_class(cfg, output.resolve(), parent_package=theme_package)

    @staticmethod
    def filter_pages(pages, theme: Theme, now=None):
        now = now or datetime.datetime.now()
        handled = []
        for page in sorted(pages, key=operator.attrgetter("key")):
            if not page.lifecycle.view_at or page.lifecycle.view_at <= now:
                if not page.lifecycle.drop_at or page.lifecycle.drop_at > now:
                    if page.path.name in theme.handlers:
                        handled.append(page)
                    else:
                        yield page
        yield from handled
