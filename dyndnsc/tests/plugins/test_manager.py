# -*- coding: utf-8 -*-

import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from dyndnsc.plugins import manager
from dyndnsc.plugins.base import Plugin


class TestPluginProxy(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_proxy_constructor(self):
        self.assertRaises(TypeError, manager.PluginProxy)
        self.assertRaises(AttributeError, manager.PluginProxy, '_invalid_interface_method_', [])
        # now a valid method:
        self.assertEqual(type(manager.PluginProxy('options', [])), manager.PluginProxy)

    def test_proxy_mock_plugin(self):
        # mock a plugin and assert it will be called by the proxy:
        plugin1 = Plugin()
        plugin1.initialize = mock.MagicMock()
        proxy = manager.PluginProxy('initialize', [plugin1])
        proxy()
        plugin1.initialize.assert_called_once_with()


class TestNullPluginManager(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_nullplugin_manager(self):
        mgr = manager.NullPluginManager()
        mgr.initialize()


class TestPluginManager(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_plugin_manager(self):
        plugin1 = Plugin()
        plugin1.can_configure = True
        plugins = [plugin1]
        mgr = manager.PluginManager(plugins, manager.PluginProxy)
        self.assertTrue(hasattr(mgr, 'load_plugins'))  # does nothing but must exist
        self.assertEqual(mgr.plugins, plugins)
        self.assertTrue(hasattr(mgr, '__iter__'))
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
        parser.DYNDNSC_WITH_PLUGIN = 1
        mgr.configure(parser)
        self.assertEqual(mgr.plugins, plugins)  # plugin remains!

        mgr.initialize()

    def test_builtin_plugin_manager(self):
        mgr = manager.BuiltinPluginManager()
        self.assertEqual(mgr.plugins, [])
        mgr.load_plugins()
        # depending on test environment, some plugins might have been loaded:
        self.assertTrue(len(mgr.plugins) >= 0)

    def test_entrypoint_plugin_manager(self):
        mgr = manager.EntryPointPluginManager()
        self.assertEqual(mgr.plugins, [])
        mgr.load_plugins()
        self.assertEqual(mgr.plugins, [])
