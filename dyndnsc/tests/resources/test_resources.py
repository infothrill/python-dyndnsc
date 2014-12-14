# -*- coding: utf-8 -*-

import unittest
import os

from dyndnsc.resources import getFilename, getStream, getString, exists, PROFILES_INI


class TestResources(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_get_filename(self):
        self.assertTrue(os.path.isfile(getFilename(PROFILES_INI)))

    def test_exists(self):
        self.assertTrue(exists(PROFILES_INI))
        self.assertFalse(exists(getFilename(".fubar-non-existant")))

    def test_get_string(self):
        self.assertEqual(str, type(getString(PROFILES_INI)))

    def test_get_stream(self):
        self.assertTrue(hasattr(getStream(PROFILES_INI), 'close'))
