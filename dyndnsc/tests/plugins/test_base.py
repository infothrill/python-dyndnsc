# -*- coding: utf-8 -*-

"""Tests for base plugin stuff."""

import unittest

from dyndnsc.plugins import base


class TestPluginBase(unittest.TestCase):
    """Test cases for plugin base code."""

    def testIPluginInterface(self):
        """Run test."""
        self.assertRaises(TypeError, base.IPluginInterface)
