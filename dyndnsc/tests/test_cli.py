# -*- coding: utf-8 -*-

"""Tests for the cli."""

import unittest
import argparse
import os
# py23
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from dyndnsc.common.six import PY3
from dyndnsc.common.six import StringIO
from dyndnsc import cli


class TestCli(unittest.TestCase):
    """Test cases for Cli."""

    def test_create_argparser(self):
        """Run tests for create_argparser()."""
        parser, arg_defaults = cli.create_argparser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))
        self.assertTrue(isinstance(arg_defaults, dict))

    def test_list_presets(self):
        """Run tests for list_presets()."""
        sample_config = """[preset:testpreset]
updater = fubarUpdater
updater-url = https://update.example.com/nic/update
updater-moreparam = some_stuff
detector = webcheck4
detector-family = INET
detector-url = http://ip.example.com/
detector-parser = plain"""
        parser = configparser.ConfigParser()
        if PY3:
            parser.read_file(StringIO(sample_config))
        else:
            parser.readfp(StringIO(sample_config))  # pylint: disable=deprecated-method
        output = StringIO()
        cli.list_presets(parser, out=output)
        buf = output.getvalue()

        self.assertEqual(len(sample_config.splitlines()), len(buf.splitlines()))
        self.assertTrue(buf.startswith("testpreset"))
        self.assertTrue("fubarUpdater" in buf)
        self.assertTrue(buf.endswith(os.linesep))
