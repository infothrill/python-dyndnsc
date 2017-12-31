# -*- coding: utf-8 -*-

"""Tests for the conf module."""

import unittest
# py23
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from dyndnsc.common.six import PY3
from dyndnsc.common.six import StringIO

from dyndnsc.conf import get_configuration, collect_config
from dyndnsc.resources import get_filename, PRESETS_INI


class TestConfig(unittest.TestCase):
    """Test cases for config."""

    def test_get_configuration(self):
        """Run basic test for configuration parser."""
        parser = get_configuration(get_filename(PRESETS_INI))
        # TODO: this is not a good test. Improve!
        self.assertFalse(parser.has_section("dyndnsc"))

    def test_config_builtin_presets(self):
        """Run tests for builtin presets."""
        parser = get_configuration(get_filename(PRESETS_INI))
        # in the built-in presets.ini, we don't want anything but presets:
        self.assertTrue(len(parser.sections()) > 0)
        for section in parser.sections():
            self.assertTrue(
                section.startswith("preset:"), "section starts with preset:")

    def test_collect_configuration(self):
        """Test minimal example of a working config."""
        sample_config = """[dyndnsc]
configs = testconfig

[testconfig]
use_preset = testpreset
updater-userid = bob
updater-password = XYZ
# test overwriting a preset value:
detector-url = http://myip.example.com/

[preset:testpreset]
updater = fubarUpdater
updater-url = https://update.example.com/nic/update
updater-moreparam = some_stuff
detector = webcheck4
detector-family = INET
detector-url = http://ip.example.com/
detector-parser = plain
        """
        parser = configparser.ConfigParser()
        if PY3:
            parser.read_file(StringIO(sample_config))
        else:
            parser.readfp(StringIO(sample_config))  # pylint: disable=deprecated-method
        config = collect_config(parser)
        self.assertEqual(dict, type(config))
        self.assertTrue("testconfig" in config)
        self.assertTrue("detector" in config["testconfig"])
        self.assertTrue(isinstance(config["testconfig"]["detector"], list))
        self.assertEqual(1, len(config["testconfig"]["detector"]))
        detector, detector_opts = config["testconfig"]["detector"][-1]
        self.assertEqual(detector, "webcheck4")  # from the preset
        self.assertEqual(detector_opts["url"], "http://myip.example.com/")  # from the user conf
        self.assertTrue("updater" in config["testconfig"])
        self.assertTrue(isinstance(config["testconfig"]["updater"], list))
        self.assertEqual(1, len(config["testconfig"]["updater"]))
        updater = config["testconfig"]["updater"][0]
        self.assertEqual("fubarUpdater", updater[0])
        self.assertTrue("url" in updater[1])
        self.assertTrue("moreparam" in updater[1])
        self.assertEqual("some_stuff", updater[1]["moreparam"])
