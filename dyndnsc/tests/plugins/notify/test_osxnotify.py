# -*- coding: utf-8 -*-

"""Tests for OS X notification."""

import unittest


class TestOSXNotify(unittest.TestCase):
    """Test cases for OS X notification."""

    def test_osxnotify(self):
        """Run tests."""
        try:
            from dyndnsc.plugins.notify import osxnotify
        except ImportError:
            pass
        else:
            plugin = osxnotify.OSXNotifyPlugin()
            plugin.initialize()
            plugin.after_remote_ip_update("127.0.0.1", status=0)
