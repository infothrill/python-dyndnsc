# -*- coding: utf-8 -*-

"""Tests for plugin manager."""

import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from dyndnsc.plugins import manager


class Dummy(object):
    """Empty Dummy class used to test plugin system."""

    pass


class TestPluginProxy(unittest.TestCase):
    """Test cases for the PluginProxy."""

    def test_proxy_constructor(self):
        """Test the plugin proxy constructor."""
        self.assertRaises(TypeError, manager.PluginProxy)
        self.assertRaises(AttributeError, manager.PluginProxy, "_invalid_interface_method_", [])
        # now a valid method:
        self.assertEqual(type(manager.PluginProxy("options", [])), manager.PluginProxy)

    def test_proxy_mock_plugin(self):
        """Test the plugin proxy."""
        # mock a plugin and assert it will be called by the proxy:
        plugin1 = Dummy()
        plugin1.initialize = mock.MagicMock()
        proxy = manager.PluginProxy("initialize", [plugin1])
        proxy()
        plugin1.initialize.assert_called_once_with()


class TestNullPluginManager(unittest.TestCase):
    """Test cases for NullPluginManager."""

    def test_nullplugin_manager(self):
        """Run basic test for the NullPluginManager."""
        mgr = manager.NullPluginManager()
        mgr.initialize()


class TestPluginManager(unittest.TestCase):
    """Test cases for plugin managers."""

    def test_plugin_manager(self):
        """Test plugin manager."""
        plugin1 = Dummy()
        plugins = [plugin1]
        mgr = manager.PluginManager(plugins, manager.PluginProxy)
        self.assertTrue(hasattr(mgr, "load_plugins"))  # does nothing but must exist
        self.assertEqual(mgr.plugins, plugins)
        self.assertTrue(hasattr(mgr, "__iter__"))
        self.assertEqual([plugin for plugin in mgr], plugins)
        mgr.plugins = []
        self.assertEqual(mgr.plugins, [])
        mgr.plugins = plugins
        self.assertEqual(mgr.plugins, plugins)
        # configure plugins with no input:
        mgr.configure(None)
        self.assertEqual(mgr.plugins, [])  # no plugins remain
        # start over:
        mgr.plugins = plugins

        parser = mock.Mock()
        parser.DYNDNSC_WITH_DUMMY = 1
        mgr.configure(parser)
        self.assertEqual(mgr.plugins, plugins)  # plugin remains!

        mgr.initialize()

    def test_builtin_plugin_manager(self):
        """Run tests for BuiltinPluginManager."""
        mgr = manager.BuiltinPluginManager()
        self.assertEqual(mgr.plugins, [])
        mgr.load_plugins()
        # depending on test environment, some plugins might have been loaded:
        self.assertTrue(len(mgr.plugins) >= 0)

    def test_entrypoint_plugin_manager(self):
        """Run tests for EntryPointPluginManager."""
        mgr = manager.EntryPointPluginManager()
        self.assertEqual(mgr.plugins, [])
        mgr.load_plugins()
        self.assertEqual(mgr.plugins, [])
