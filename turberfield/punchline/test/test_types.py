import unittest


import textwrap
import uuid

from turberfield.dialogue.model import Model
from turberfield.dialogue.model import SceneScript
from turberfield.punchline.build import Build
from turberfield.punchline.build import ModelAssignsStrings
from turberfield.punchline.types import Settings


class SettingsTests(unittest.TestCase):

    def setUp(self):
        self.cfg = Settings.config_parser()
        
    def test_init_from_setter(self):
        text = textwrap.dedent("""
        .. entity:: THEME_SETTINGS

        Scene
        =====

        Shot
        ----

        .. property:: THEME_SETTINGS.midtone hsl(86, 93%, 12%, 0.7)
        """)
        uid = uuid.uuid4()
        theme = type("Fake", (), {})()
        theme.settings = Settings(id=uid)
        script = SceneScript("inline", doc=SceneScript.read(text))
        script.cast(script.select([theme.settings]))
        model = ModelAssignsStrings(script.fP, script.doc)
        script.doc.walkabout(model)
        self.assertEqual(1, len(model.shots))
        shot = model.shots[0]
        self.assertEqual(1, len(shot.items))
        setter = shot.items[0]
        self.assertIsInstance(setter, Model.Property)

    def test_init_from_config(self):
        self.cfg.read_string(
        """
        [theme]
        washout = hsl(50, 0%, 100%, 1.0)
        shadows = hsl(37, 93%, 12%, 0.7)
        midtone = hsl(86, 93%, 12%, 0.7)
        hilight = hsl(224, 70%, 16%, 0.7)
        glamour = hsl(76, 80%, 35%, 1.0)
        gravity = hsl(36, 20%, 18%, 1.0)
        """
        )
        settings = Settings(**self.cfg["theme"])
        self.assertEqual("hsl(37, 93%, 12%, 0.7)", settings.shadows)

