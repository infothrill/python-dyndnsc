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
        config['hostname'] = "dyndnsc.no-ip.biz"
        config['userid'] = "example"
        config['password'] = "foobar"
        config['protocol'] = "dummy"
        config['method'] = "random"
        config['sleeptime'] = 60
        dyndnsclient = dyndnsc.getDynDnsClientForConfig(config)
        self.assertTrue(dyndnsclient.needs_check())
        dyndnsclient.needs_forced_check()
        dyndnsclient.check()
        dyndnsclient.sync()
        dyndnsclient.has_state_changed()
