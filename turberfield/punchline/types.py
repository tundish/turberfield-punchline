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

