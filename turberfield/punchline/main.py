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
from collections import Counter
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
            output = args.output or path.joinpath("output")
            articles = [
                i._replace(path=output.resolve()) for i in Build.filter_pages(Build.find_articles(path, theme))
            ]
            logging.debug(theme.settings)

        tags = Counter([t for a in articles for t in a.tags])
        feeds = defaultdict(set)
        with theme as writer:
            for n, page in enumerate(writer.expand(articles, tags)):
                page.path.parent.mkdir(parents=True, exist_ok=True)
                page.path.write_text(page.html)
                for feed_name in page.feeds:
                    feeds[feed_name].add(page)
            logging.info("Rendered {0} pages.".format(n + 1))

            # Write feed output
            for feed_name, pages in feeds.items():
                settings = theme.get_feed_settings(feed_name)
                feed = writer.publish(pages, **settings)
                feed_path = output.joinpath(
                    settings.getpath("feed_url").relative_to(settings.getpath("feed_url").anchor)
                )
                feed_path.parent.mkdir(parents=True, exist_ok=True)
                feed_path.write_text(json.dumps(feed, indent=0))

            extras = list(writer.cover(pages, feeds, tags))
        logging.info("Wrote output to {0}".format(theme.root))

    return 0

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
