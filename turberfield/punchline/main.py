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

import argparse
from collections import defaultdict
import configparser
import datetime
import importlib
import importlib.resources
import json
import logging
import logging.config
import pathlib
import sys


from turberfield.dialogue.model import SceneScript
from turberfield.dialogue.types import Persona

from turberfield.punchline.build import Build
from turberfield.punchline.types import Settings

from turberfield.utils.misc import group_by_type


def parser():
    rv = argparse.ArgumentParser()
    with importlib.resources.path("turberfield.punchline", "default.cfg") as default_config_path:
        rv.add_argument(
            "--config", action="append", type=pathlib.Path,
            default=[default_config_path],
            help="Specify one or more site configurations."
        )
    rv.add_argument(
        "--theme", type=str, default="january",
        help="Specify a them to use by name or dotted path to class."
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
    logging.info("Running Punchline")
    for cfg_path in args.config:
        cfg = Settings.config_parser()
        cfg.read(cfg_path)
        # logging.config.fileConfig(cfg, disable_existing_loggers=False)
        logging.info("Using config file at {0}".format(cfg_path))

        theme = Build.find_theme(args.theme, cfg)
        if not theme:
            logging.critical("No theme found.")
            return 1

        for path in args.inputs:
            pages = list(Build.filter_pages(Build.find_articles(path, theme)))
            output = args.output or path.joinpath("output")
            cover_pages = {page for page in pages if page.path.name in theme.covers.values()}
            articles = [
                page._replace(path=output.resolve()) for page in pages if page not in cover_pages
            ]
            logging.debug(theme.settings)

        feeds = defaultdict(set)
        tags = defaultdict(set)
        with theme as writer:
            for article in articles:
                for page in writer.expand(article, tags):
                    page.path.parent.mkdir(parents=True, exist_ok=True)
                    page.path.write_text(page.html)
                    for feed_name in page.feeds:
                        feeds[feed_name].add(page)
                    for tag_name in page.tags:
                        tags[tag_name].add(page)

            logging.info("Processed {0} article{1}.".format(len(articles), "" if len(articles) == 1 else "s"))
            # Write feed output
            for feed_name, pages in feeds.items():
                settings = theme.get_feed_settings(feed_name)
                feed = writer.publish(pages, **settings)
                feed_path = output.joinpath(
                    settings.getpath("feed_url").relative_to(settings.getpath("feed_url").anchor)
                )
                feed_path.parent.mkdir(parents=True, exist_ok=True)
                feed_path.write_text(json.dumps(feed, indent=0))

            logging.info("Rendered {0} page{1}.".format(len(pages), "" if len(pages) == 1 else "s"))
            facades = {}
            for cover_page in cover_pages:
                for page in writer.cover(page, feeds, tags, facades):
                    page.path.parent.mkdir(parents=True, exist_ok=True)
                    page.path.write_text(page.html)
            logging.info("Created {0} cover page{1}.".format(
                len(cover_pages), "" if len(cover_pages) == 1 else "s")
            )

        logging.info("Wrote output to {0}".format(theme.root))

    return 0

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
