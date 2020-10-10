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

import logging

from turberfield.punchline.theme import Theme
from turberfield.punchline.widget import Widget


class January(Theme):

    @property
    def widgets(self):
        return Widget.register(
            Widget(self.parent_package, "css", "fonts", optional=False),
        )

    @property
    def definitions(self):
        return {
            "titles": "Tenderness, sans-serif",
            "blocks": "Tenderness, sans-serif",
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
