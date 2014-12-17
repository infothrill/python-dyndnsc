# -*- coding: utf-8 -*-

import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

from dyndnsc.plugins import base


class TestPluginBase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_Plugin_argument_options(self):
        plugin = base.Plugin()

        self.assertEqual(type(plugin.help()), str)
        plugin.configure(True)

        argparser = mock.Mock()
        argparser.add_argument = mock.MagicMock(name="add_argument")
        expected_args = ["--with-%s" % plugin.name]
        expected_kwargs = {
            'action': "store_true",
            'dest': plugin.enableOpt,
            'default': None,
            'help': "Enable plugin %s: %s [%s]" % ('Plugin', plugin.help(),
                                                   "DYNDNSC_WITH_PLUGIN")
        }

        plugin.options(argparser, {})
        argparser.add_argument.assert_called_once_with(*expected_args,
                                                       **expected_kwargs)

    def test_Plugin_argument_configure(self):
        plugin = base.Plugin()
        # by default, plugins are disabled:
        self.assertEqual(False, plugin.enabled)

        # let's build some fake arguments to enable the plugin, which first
        # needs to be configurable:
        plugin.can_configure = True
        from argparse import Namespace
        args = Namespace()
        args.enable_plugin_plugin = True  # the base plugin is called "plugin"
        plugin.configure(args)
        self.assertEqual(True, plugin.enabled)

    def testIPluginInterface(self):
        self.assertRaises(TypeError, base.IPluginInterface)
