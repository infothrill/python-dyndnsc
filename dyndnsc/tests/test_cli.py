# -*- coding: utf-8 -*-

import unittest
import argparse
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from dyndnsc.common.six import StringIO
from dyndnsc import cli


class TestCli(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_create_argparser(self):
        parser, arg_defaults = cli.create_argparser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))
        self.assertTrue(isinstance(arg_defaults, dict))

    def test_list_presets(self):
        sample_config = """[preset:testpreset]
updater = fubarUpdater
updater-url = https://update.example.com/nic/update
updater-moreparam = some_stuff
detector = webcheck4
detector-family = INET
detector-url = http://ip.example.com/
detector-parser = plain"""
        p = configparser.ConfigParser()
        p.readfp(StringIO(sample_config))
        output = StringIO()
        cli.list_presets(p, out=output)
        buf = output.getvalue()

        self.assertEqual(len(sample_config.splitlines()), len(buf.splitlines()))
        self.assertTrue(buf.startswith("testpreset"))
        self.assertTrue("fubarUpdater" in buf)
        self.assertTrue(buf.endswith(os.linesep))
