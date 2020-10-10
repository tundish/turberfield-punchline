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
            "--config", type=pathlib.Path,
            default=default_config_path, help="Specify a site configuration file."
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
    cfg = Settings.config_parser()
    cfg.read(args.config)
    # logging.config.fileConfig(cfg, disable_existing_loggers=False)
    logging.info("Using config file at {0}".format(args.config))

    output = args.output or args.inputs[0].joinpath("output")
    sys.path.append(str(args.config.parent.resolve()))
    theme = Build.find_theme(cfg, output=output)
    if not theme:
        logging.critical("No theme found.")
        return 1

    for path in args.inputs:
        articles = list(Build.filter_pages(Build.find_articles(path, theme), theme))

    feeds = {f: set() for p in articles for f in p.feeds}
    tags = {t: set() for p in articles for t in p.tags}
    tally = Counter()
    with theme as writer:
        for article in articles:
            handler = writer.handlers.get(article.path.name, writer.expand)
            for page in handler(article, feeds, tags, output=output.resolve()):
                page.path.parent.mkdir(parents=True, exist_ok=True)
                page.path.write_text(page.html)
                for feed_name in page.feeds:
                    feeds[feed_name].add(page)
                for tag_name in page.tags:
                    tags[tag_name].add(page)
            tally[handler] += 1

        n_articles = tally[theme.expand]
        logging.info("Processed {0} article{1}.".format(n_articles, "" if n_articles == 1 else "s"))

        n_pages = len({page for pages in feeds.values() for page in pages})
        logging.info("Rendered {0} page{1}.".format(n_pages, "" if n_pages == 1 else "s"))

        n_covers = sum(tally.values()) - n_articles
        logging.info("Created {0} cover page{1}.".format(n_covers, "" if n_covers == 1 else "s"))

        # Write feed output
        for n, (feed_name, pages) in enumerate(feeds.items()):
            settings = theme.get_feed_settings(feed_name)
            feed = writer.publish(pages, **settings)
            feed_path = theme.output.joinpath(
                settings.getpath("feed_url").relative_to(settings.getpath("feed_url").anchor)
            )
            feed_path.parent.mkdir(parents=True, exist_ok=True)
            feed_path.write_text(json.dumps(feed, indent=0))

        logging.info("Compiled {0} feed{1}.".format(n + 1, "" if not n else "s"))

    logging.info("Wrote output to {0}".format(theme.output))

    return 0

def run():
    p = parser()
    args = p.parse_args()
    rv = main(args)
    sys.exit(rv)

if __name__ == "__main__":
    run()
