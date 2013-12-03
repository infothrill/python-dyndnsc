# -*- coding: utf-8 -*-

import unittest


class TestUpdaterCommon(unittest.TestCase):
    def test_updater_builtin_plugins(self):
        import dyndnsc.updater.builtin
        self.assertTrue(len(dyndnsc.updater.builtin.plugins) > 0)

    def test_updater_interfaces(self):
        from dyndnsc.updater.manager import updater_classes, get_updater_class
        for cls in updater_classes():
            self.assertTrue(hasattr(cls, 'configuration_key'))
            self.assertTrue(hasattr(cls, 'update'))
        self.assertTrue(len(updater_classes()) > 0)
        self.assertRaises(KeyError, get_updater_class, 'nonexistant')
