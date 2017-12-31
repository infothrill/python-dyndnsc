# -*- coding: utf-8 -*-

"""Tests for base plugin stuff."""

import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from dyndnsc.plugins import base


class TestPluginBase(unittest.TestCase):
    """Test cases for plugin base code."""

    def test_plugin_argument_options(self):
        """Run test for argument options."""
        plugin = base.Plugin()

        self.assertEqual(type(plugin.help()), str)
        plugin.configure(True)

        argparser = mock.Mock()
        argparser.add_argument = mock.MagicMock(name="add_argument")
        expected_args = ["--with-%s" % plugin.name]
        expected_kwargs = {
            "action": "store_true",
            "dest": plugin.enableOpt,
            "default": None,
            "help": "Enable plugin %s: %s [%s]" % ("Plugin", plugin.help(),
                                                   "DYNDNSC_WITH_PLUGIN")
        }

        plugin.options(argparser, {})
        argparser.add_argument.assert_called_once_with(*expected_args,
                                                       **expected_kwargs)

    def test_plugin_argument_configure(self):
        """Run test for plugin arg configuration."""
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
        """Run test."""
        self.assertRaises(TypeError, base.IPluginInterface)
