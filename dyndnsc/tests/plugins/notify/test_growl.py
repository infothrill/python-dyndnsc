# -*- coding: utf-8 -*-

"""Tests for Growl."""

import unittest


class TestGrowlPlugin(unittest.TestCase):
    """Test cases for Growl."""

    def test_growl(self):
        """Run tests."""
        try:
            from dyndnsc.plugins.notify import growl
        except ImportError:
            pass
        else:
            plugin = growl.GrowlPlugin()
            plugin.initialize()
            plugin.after_remote_ip_update("127.0.0.1", status=0)
