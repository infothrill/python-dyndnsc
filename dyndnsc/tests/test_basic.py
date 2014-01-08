# -*- coding: utf-8 -*-

import unittest

import dyndnsc


class TestDynDnsc(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_dummy(self):
        config = {}
        config['detector'] = "random"
        from dyndnsc.updater.manager import get_updater_class
        upd = get_updater_class("dummy")(hostname="example.com")
        config['updaters'] = (upd,)
        dyndnsclient = dyndnsc.getDynDnsClientForConfig(config)
        self.assertTrue(dyndnsclient.needs_check())
        dyndnsclient.needs_forced_check()
        dyndnsclient.check()
        dyndnsclient.sync()
        dyndnsclient.has_state_changed()
