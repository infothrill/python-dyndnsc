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

    def testPluginBase(self):
        plugin = base.Plugin()

        self.assertEquals(type(plugin.help()), str)
        plugin.configure(True)

        argparser = mock.Mock()
        argparser.add_argument = mock.MagicMock(name="add_argument")
        expected_args = ["--with-%s" % plugin.name]
        expected_kwargs = {
            'action': "store_true",
            'dest': plugin.enableOpt,
            'default': None,
            'help': "Enable plugin %s: %s [%s]" % ('Plugin', plugin.help(),
                                                   "DYNDNC_WITH_PLUGIN")
        }

        plugin.options(argparser, {})
        argparser.add_argument.assert_called_once_with(*expected_args,
                                                       **expected_kwargs)

    def testIPluginInterface(self):
        self.assertRaises(TypeError, base.IPluginInterface)
