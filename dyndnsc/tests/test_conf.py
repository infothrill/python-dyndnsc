# -*- coding: utf-8 -*-

import unittest

from dyndnsc.conf import getConfiguration


class TestConfig(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testgetConfiguration(self):
        getConfiguration()
