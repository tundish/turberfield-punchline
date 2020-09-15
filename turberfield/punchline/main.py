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

from turberfield.utils.misc import gather_installed
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
        cfg = Settings.config_parser()
        cfg.read(cfg_path)
        # logging.config.fileConfig(cfg, disable_existing_loggers=False)
        logging.info("Using config file at {0}".format(cfg_path))

        # Discover themes
        themes = dict(gather_installed("turberfield.interfaces.theme"))
        logging.info(themes)

        # Select theme
        theme_module = importlib.import_module("turberfield.punchline.themes.january")
        theme = theme_module.January(cfg)
        logging.info(theme.settings)

        for path in args.inputs:
            output = args.output or path.joinpath("output")
            pages = [i._replace(path=output.resolve()) for i in Build.filter_pages(Build.find_pages(path))]

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

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
