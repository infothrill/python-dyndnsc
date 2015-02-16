# -*- coding: utf-8 -*-

import unittest
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from dyndnsc.common.six import StringIO

from dyndnsc.conf import get_configuration, collect_config
from dyndnsc.resources import getFilename, PRESETS_INI


class TestConfig(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_get_configuration(self):
        parser = get_configuration(getFilename(PRESETS_INI))
        # TODO: this is not a good test. Improve!
        self.assertFalse(parser.has_section("dyndnsc"))

    def test_config_builtin_presets(self):
        parser = get_configuration(getFilename(PRESETS_INI))
        # in the built-in presets.ini, we don't want anything but presets:
        for section in parser.sections():
            self.assertTrue(
                section.startswith("preset:"), "section starts with preset:")

    def test_collect_configuration(self):
        """
        minimal example of a working config
        """
        sample_config = """[dyndnsc]
configs = testconfig

[testconfig]
use_preset = testpreset
updater-userid = bob
updater-password = XYZ

[preset:testpreset]
updater = fubarUpdater
updater-url = https://update.example.com/nic/update
updater-moreparam = some_stuff
detector = webcheck4
detector-family = INET
detector-url = http://ip.example.com/
detector-parser = plain
        """
        p = configparser.ConfigParser()
        p.readfp(StringIO(sample_config))  # XXX readfp() is deprecated since py 3.2
        config = collect_config(p)
        self.assertEqual(dict, type(config))
        self.assertTrue('testconfig' in config)
        self.assertTrue('detector' in config['testconfig'])
        self.assertTrue(isinstance(config['testconfig']['detector'], list))
        self.assertEqual(1, len(config['testconfig']['detector']))
        self.assertTrue('updater' in config['testconfig'])
        self.assertTrue(isinstance(config['testconfig']['updater'], list))
        self.assertEqual(1, len(config['testconfig']['updater']))
        updater = config['testconfig']['updater'][0]
        self.assertEqual("fubarUpdater", updater[0])
        self.assertTrue("url" in updater[1])
        self.assertTrue("moreparam" in updater[1])
        self.assertEqual("some_stuff", updater[1]["moreparam"])
