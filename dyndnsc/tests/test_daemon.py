# -*- coding: utf-8 -*-

"""Tests for the daemon module."""

import unittest

from dyndnsc import daemon


class TestDaemon(unittest.TestCase):
    """Test cases for the daemon module."""

    def test_daemonize(self):
        """For now, test not so much."""
        self.assertTrue(len(dir(daemon)) > 0)
