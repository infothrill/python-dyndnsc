# -*- coding: utf-8 -*-

import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock


class TestUpdaterCommon(unittest.TestCase):
    def test_updater_builtin_plugins(self):
        import dyndnsc.updater.builtin
        self.assertTrue(len(dyndnsc.updater.builtin.plugins) > 0)

    def test_updater_base_class(self):
        from dyndnsc.updater.base import UpdateProtocol
        cls = UpdateProtocol
        self.assertTrue(hasattr(cls, 'configuration_key'))
        self.assertTrue(hasattr(cls, 'init_argnames'))
        self.assertEqual(type(cls.init_argnames()), type([]))
        self.assertTrue(hasattr(cls, 'register_arguments'))
        self.assertTrue(hasattr(cls, 'service_url'))
        self.assertTrue(hasattr(cls, 'help'))
        self.assertEqual(type(cls.configuration_key()), type(""))
        self.assertEqual(type(cls.help()), type(""))

        # ensure the argparser method 'add_argument' is called:
        argparser = mock.Mock()
        argparser.add_argument = mock.MagicMock(name="add_argument")
        self.assertFalse(argparser.add_argument.called)
        cls.register_arguments(argparser)
        self.assertTrue(argparser.add_argument.called)

    def test_updater_interfaces(self):
        from dyndnsc.updater.manager import updater_classes, get_updater_class
        for cls in updater_classes():
            self.assertTrue(hasattr(cls, 'configuration_key'))
            self.assertEqual(cls, get_updater_class(cls.configuration_key()))
            self.assertTrue(hasattr(cls, 'update'))
            self.assertTrue(hasattr(cls, 'register_arguments'))
            self.assertTrue(hasattr(cls, 'help'))
            self.assertTrue(type(cls.configuration_key()) == type(""))
            self.assertTrue(type(cls.help()) == type(""))
        self.assertTrue(len(updater_classes()) > 0)
        self.assertRaises(KeyError, get_updater_class, 'nonexistant')
