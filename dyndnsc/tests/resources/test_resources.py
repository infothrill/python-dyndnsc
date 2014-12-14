# -*- coding: utf-8 -*-

import unittest
import os

from dyndnsc.resources import getFilename, PROFILES_INI


class TestResources(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testGetFilename(self):
        self.assertTrue(os.path.isfile(getFilename(PROFILES_INI)))
