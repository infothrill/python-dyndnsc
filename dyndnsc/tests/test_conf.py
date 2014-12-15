# -*- coding: utf-8 -*-

import unittest

from dyndnsc.conf import getConfiguration, collect_config
from dyndnsc.resources import getFilename, PROFILES_INI


class TestConfig(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_getConfiguration(self):
        parser = getConfiguration(getFilename(PROFILES_INI))
        self.assertFalse(parser.getboolean('dyndnsc', 'daemon'))

    def test_collectConfiguration(self):
        """
        minimal example of a working config
        """
        sample_config = """[dyndnsc]
configs = testconfig
daemon = false

[testconfig]
use_profile = testprofile
updater-userid = bob
updater-password = XYZ

[profile:testprofile]
updater = dyndns2
updater-url = https://update.example.com/nic/update
detector = webcheck4
detector-family = INET
detector-url = http://ip.example.com/
detector-parser = plain
        """
        from ConfigParser import ConfigParser
        from StringIO import StringIO
        p = ConfigParser()
        p.readfp(StringIO(sample_config))
        config = collect_config(p)
        self.assertEqual(dict, type(config))
        self.assertTrue('detector' in config)
