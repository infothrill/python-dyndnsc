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
        self.assertFalse(exists(getFilename(".fubar-non-existent")))

    def test_get_string(self):
        self.assertTrue(type(getString(PROFILES_INI)) in (str, bytes))

    def test_get_stream(self):
        obj = getStream(PROFILES_INI)
        if hasattr(obj, 'close'):
            obj.close()
        else:
            self.fail("getStream() didn't return an object with a close() method")
