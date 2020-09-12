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
import itertools
import operator
import string

from turberfield.dialogue.model import Model


class Site:

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


    @staticmethod
    def multidict(items: list):
        return defaultdict(
            list, {
                k: [i[1] for i in g]
                for k, g in itertools.groupby(
                    items, key=operator.itemgetter(0)
                )
            }
        )

    @staticmethod
    def feeds_from_script(model, keys=("category", "feed")):
        return {v.lower() for k, v in model.metadata if k.lower() in keys}
