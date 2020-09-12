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

from turberfield.dialogue.directives import Entity
from turberfield.dialogue.types import Persona
from turberfield.utils.misc import group_by_type


class Eponymous(Persona):

    @staticmethod
    def name_from_entity(entity):
        return entity["arguments"][0].replace("_", " ").title()

    @classmethod
    def create(cls, script):
        entities = group_by_type(script.doc)[Entity.Declaration]
        for entity in entities:
            yield cls(name=cls.name_from_entity(entity))

