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
import textwrap


class Widget:

    Fragment = namedtuple("Fragment", ["metadata", "style", "body", "text"])

    catalogue = set()

    def __init__(self, package, *resources, config="theme", optional=False):
        self.package = package
        self.resources = resources
        self.config = config
        self.optional = optional

    def __call__(self, *args, **kwargs):
        return self.Fragment(None, "", "", "")

    @classmethod
    def register(cls, *args):
        for f in args:
            if isinstance(f, cls):
                cls.catalogue.add(f)
        return cls.catalogue.copy()


class WebBadge(Widget):

    def __call__(self, *args, **kwargs):
        text = kwargs.get("text", "")
        kwargs["text"] = "".join("<span>{0}</span> ".format(i) for i in text.split(" "))
        html = textwrap.dedent("""
        <section class="punchline-widget punchline-widget-{0}">
        <img src="{src}" alt="{alt}" width="{width}" height="{height}"/>
        <a href="{url}">{text}</a>
        </section>
        """).format(self.__class__.__name__.lower(), **kwargs)
        return self.Fragment(None, None, html, text)
