# -*- coding: utf-8 -*-

"""Tests for resources."""

import unittest
import os

from dyndnsc.resources import get_filename, get_stream, get_string, exists, PRESETS_INI


class TestResources(unittest.TestCase):
    """Test cases for resources."""

    def setUp(self):
        """Run setup hooks."""
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """Run teardown hooks."""
        unittest.TestCase.tearDown(self)

    def test_get_filename(self):
        """Run test."""
        self.assertTrue(os.path.isfile(get_filename(PRESETS_INI)))

    def test_exists(self):
        """Run test."""
        self.assertTrue(exists(PRESETS_INI))
        self.assertFalse(exists(get_filename(".fubar-non-existent")))

    def test_get_string(self):
        """Run test."""
        self.assertTrue(type(get_string(PRESETS_INI)) in (str, bytes))

    def test_get_stream(self):
        """Run test."""
        obj = get_stream(PRESETS_INI)
        if hasattr(obj, "close"):
            obj.close()
        else:
            self.fail("get_stream() didn't return an object with a close() method")
