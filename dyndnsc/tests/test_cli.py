# -*- coding: utf-8 -*-

import unittest
import argparse


from dyndnsc import cli


class TestCli(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_create_argparser(self):
        parser = cli.create_argparser()
        self.assertTrue(isinstance(parser, argparse.ArgumentParser))
