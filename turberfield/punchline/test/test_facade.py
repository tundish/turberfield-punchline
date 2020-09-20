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


import unittest

from collections import defaultdict
from collections import namedtuple

from turberfield.punchline.facade import Facade


class FacadeTests(unittest.TestCase):

    def setUp(self):
        self.cfg = Settings.config_parser()
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
        facade = Facade()
        kwargs = self.cfg[facade.label] if facade.label in self.cfg else {}
        rv = facade(**kwargs)
        self.assertIsInstance(rv, Facade.Fragment)
