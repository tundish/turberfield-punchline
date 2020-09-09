#!/usr/bin/env python3
# encoding: utf-8

import argparse
from collections import defaultdict
from collections import namedtuple
import configparser
import datetime
import importlib
import importlib.resources
import itertools
import json
import logging
import logging.config
import operator
import pathlib
import string
import sys
import uuid


from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import Persona
from turberfield.utils.misc import group_by_type

import uncarved.lockdown
from uncarved.lockdown.site import Site
from uncarved.lockdown.theme import Theme
from uncarved.lockdown.types import Eponymous

def lifecycle(data: dict, defaults: Site.Lifecycle=None):
    defaults = defaults._asdict() if defaults else {}
    formats = {10: "%Y-%m-%d", 16: "%Y-%m-%d %H:%M", 19: "%Y-%m-%d %H:%M:%S"}
    timestamps = [(k, data.get(k)) for k in Site.Lifecycle._fields if k.endswith("_at")]
    datetimes = [
        datetime.datetime.strptime(v, formats[len(v)])
        if v and len(v) in formats else defaults.get(k) for k, v in timestamps
    ]
    return Site.Lifecycle(*datetimes)

def write_folder_id(path):
    uid_path = path.joinpath("uuid.hex")
    if uid_path.is_file():
        return uuid.UUID(hex=uid_path.read_text().strip())
    else:
        rv = uuid.uuid4()
        uid_path.write_text(rv.hex)
        return rv

def build_pages(text, uid=None, path:pathlib.Path=None, name="inline", now=None):
    uid = uid or uuid.uuid4()
    path = path or pathlib.Path(".")
    now = now or datetime.datetime.now()
    script = SceneScript(path, doc=SceneScript.read(text, name=name))
    ensemble = list(Eponymous.create(script))
    script.cast(script.select(ensemble))
    model = script.run()
    lc = lifecycle(dict(model.metadata))
    data = Site.multidict(model.metadata)
    for n, (scene, shots) in enumerate(itertools.groupby(model.shots, key=operator.attrgetter("scene"))):
        yield Site.Page(
            (lc.view_at or lc.made_at or now, name, n), None,
            Theme.slug(name), Theme.slug(scene), lc, scene, model,
            text=None, html=None, path=None,
            feeds=frozenset(Site.feeds_from_script(model) or ["all"]),
            tags=frozenset(v.lower() for k, v in model.metadata if k.lower() == "tag")
        )

def find_pages(root: pathlib.Path):
    for parent in {i.parent for i in root.glob("**/*.rst")}:
        uid = write_folder_id(parent)
        for path in parent.glob("*.rst"):
            yield from build_pages(path.read_text(), uid=uid, path=path, name=path.stem)

def filter_pages(pages, now=None):
    now = now or datetime.datetime.now()
    for page in sorted(pages, key=operator.attrgetter("key")):
        if not page.lifecycle.view_at or page.lifecycle.view_at <= now:
            if not page.lifecycle.drop_at or page.lifecycle.drop_at > now:
                yield page


def feeds_from_pages(pages, default=None, keys=("category", "feed")):
    rv = defaultdict(set)
    for page in pages:
        if default:
            rv[default].add(page)
        for k, v in page.model.metadata:
            if k.lower() in keys:
                rv[v.lower()].add(page)
    return rv


def config_parser():
    cfg = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        converters={"path": pathlib.Path},
    )
    cfg.optionxform = str
    return cfg


def parser():
    rv = argparse.ArgumentParser()
    with importlib.resources.path("uncarved.lockdown", "default.cfg") as default_config_path:
        rv.add_argument(
            "--config", action="append", type=pathlib.Path,
            default=[default_config_path],
            help="Specify one or more site configurations."
        )
    rv.add_argument(
        "inputs", nargs="+", type=pathlib.Path,
        help="Set one or more search paths."
    )
    rv.add_argument(
        "--output", required=False, default=None, type=pathlib.Path,
        help="Set directory for output."
    )
    return rv


def main(args):
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s|%(name)s|%(message)s",
        level=logging.INFO
    )
    for cfg_path in args.config:
        cfg = config_parser()
        cfg.read(cfg_path)
        # logging.config.fileConfig(cfg, disable_existing_loggers=False)

        logging.info("Using config file at {0}".format(cfg_path))
        for path in args.inputs:
            output = args.output or path.joinpath("output")
            pages = [i._replace(path=output.resolve()) for i in filter_pages(find_pages(path))]

        # Discover themes
        # Select theme
        theme_module = importlib.import_module("uncarved.lockdown.themes.carving.main")
        theme = theme_module.theme(cfg)

        feeds = defaultdict(set)
        with theme as writer:
            for page in writer.render(pages):
                page.path.parent.mkdir(parents=True, exist_ok=True)
                page.path.write_text(page.html)
                for feed_name in page.feeds:
                    feeds[feed_name].add(page)

            # Write feed output
            for feed_name, pages in feeds.items():
                settings = writer.get_feed_settings(feed_name)
                feed = writer.publish(pages, **settings)
                feed_path = output.joinpath(
                    settings.getpath("feed_url").relative_to(settings.getpath("feed_url").anchor)
                )
                feed_path.parent.mkdir(parents=True, exist_ok=True)
                feed_path.write_text(json.dumps(feed, indent=0))

        logging.info(theme.root)

    return 0

if __name__ == "__main__":
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)
