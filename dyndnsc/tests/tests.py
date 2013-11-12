# -*- coding: utf-8 -*-

import unittest
import logging

import dyndnsc

logging.basicConfig(level=logging.DEBUG)


class DynDnscTestCases(unittest.TestCase):
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
        self.assertTrue(dyndnsclient.needsCheck())
        dyndnsclient.needsForcedCheck()
        dyndnsclient.check()
        dyndnsclient.sync()
        dyndnsclient.stateHasChanged()
