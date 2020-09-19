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

import importlib
import logging
import shutil

from turberfield.punchline.theme import Theme


class January(Theme):

    def __exit__(self, exc_type, exc_val, exc_tb):
        for d in ("css", "fonts"):
            with importlib.resources.path("turberfield.punchline.themes.january", d) as path:
                shutil.copytree(path, self.root.joinpath(d), dirs_exist_ok=True)

        return False

    @property
    def definitions(self):
        return {
            "titles": '"Bernier Shade", sans-serif',
            "blocks": '"Bernier Regular", sans-serif',
            "mono": ", ".join([
                "SFMono-Regular", "Menlo", "Monaco",
                "Consolas", '"Liberation Mono"',
                '"Courier New"', "monospace"
            ]),
            "detail": '"Palatino Linotype", "Book Antiqua", Palatino, serif',
            "system": ", ".join([
                "BlinkMacSystemFont", '"Segoe UI"', '"Helvetica Neue"',
                '"Apple Color Emoji"', '"Segoe UI Emoji"', '"Segoe UI Symbol"',
                "Arial", "sans-serif"
            ]),
        }
