# -*- coding: utf-8 -*-

import unittest
import os

from dyndnsc.resources import getFilename, getStream, getString, exists, PRESETS_INI


class TestResources(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_get_filename(self):
        self.assertTrue(os.path.isfile(getFilename(PRESETS_INI)))

    def test_exists(self):
        self.assertTrue(exists(PRESETS_INI))
        self.assertFalse(exists(getFilename(".fubar-non-existent")))

    def test_get_string(self):
        self.assertTrue(type(getString(PRESETS_INI)) in (str, bytes))

    def test_get_stream(self):
        obj = getStream(PRESETS_INI)
        if hasattr(obj, 'close'):
            obj.close()
        else:
            self.fail("getStream() didn't return an object with a close() method")
