# -*- coding: utf-8 -*-

"""Tests for updaters."""

import unittest

try:
    from unittest import mock
except ImportError:
    import mock


class TestUpdaterCommon(unittest.TestCase):
    """Updater test cases."""

    def test_updater_builtin_plugins(self):
        """Run test."""
        import dyndnsc.updater.builtin
        self.assertTrue(len(dyndnsc.updater.builtin.PLUGINS) > 0)

    def test_updater_base_class(self):
        """Run test."""
        from dyndnsc.updater.base import UpdateProtocol
        cls = UpdateProtocol
        self.assertTrue(hasattr(cls, "configuration_key"))
        self.assertTrue(hasattr(cls, "init_argnames"))
        self.assertEqual(type(cls.init_argnames()), type([]))
        self.assertTrue(hasattr(cls, "register_arguments"))
        self.assertTrue(hasattr(cls, "help"))
        self.assertEqual(type(cls.help()), type(""))
        instance = cls()
        self.assertRaises(NotImplementedError, instance.update, "foo")

        # For the purpose of this test, we fake an implementation of
        # configuration_key:
        cls._configuration_key = "none"

        # ensure the argparser method 'add_argument' is called:
        argparser = mock.Mock()
        argparser.add_argument = mock.MagicMock(name="add_argument")
        self.assertFalse(argparser.add_argument.called)
        cls.register_arguments(argparser)
        self.assertTrue(argparser.add_argument.called)

    def test_updater_interfaces(self):
        """Run test."""
        from dyndnsc.updater.manager import updater_classes, get_updater_class
        for cls in updater_classes():
            self.assertTrue(hasattr(cls, "configuration_key"))
            self.assertEqual(cls, get_updater_class(cls.configuration_key))
            self.assertTrue(hasattr(cls, "update"))
            self.assertTrue(hasattr(cls, "register_arguments"))
            self.assertTrue(hasattr(cls, "help"))
            self.assertEqual(str, type(cls.configuration_key))
            self.assertTrue(str, type(cls.help()))
        self.assertTrue(len(updater_classes()) > 0)
        self.assertRaises(ValueError, get_updater_class, "nonexistent")
