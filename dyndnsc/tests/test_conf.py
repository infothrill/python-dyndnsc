# -*- coding: utf-8 -*-

import unittest

from dyndnsc.conf import getConfiguration
from dyndnsc.resources import getFilename, PROFILES_INI


class TestConfig(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testgetConfiguration(self):
        parser = getConfiguration(getFilename(PROFILES_INI))
        self.assertFalse(parser.getboolean('dyndnsc', 'daemon'))
