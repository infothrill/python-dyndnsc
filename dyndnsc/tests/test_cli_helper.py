# -*- coding: utf-8 -*-

import unittest
from dyndnsc.cli_helper import parse_cmdline_updater_args, parse_cmdline_detector_args


class Test_cli_helper(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_parse_cmdline_updater_args(self):
        self.assertRaises(ValueError, parse_cmdline_updater_args, None)
        self.assertEqual([], parse_cmdline_updater_args(object()))

        # test that a sample valid config parses:
        from argparse import Namespace
        args = Namespace()
        args.updater_dyndns2 = True
        args.updater_dyndns2_userid = "bob"
        args.updater_dyndns2_password = "******"
        args.updater_dyndns2_hostname = "ahost.example.com"
        args.updater_dyndns2_service_url = "http://service.example.com"

        updaters = parse_cmdline_updater_args(args)
        self.assertEqual(1, len(updaters))
        self.assertEqual(tuple, type(updaters[0]))
        self.assertEqual("dyndns2", updaters[0][0])
        self.assertEqual(dict, type(updaters[0][1]))
        self.assertTrue("userid" in updaters[0][1].keys())
        self.assertTrue("password" in updaters[0][1].keys())
        self.assertTrue("hostname" in updaters[0][1].keys())
        self.assertTrue("service_url" in updaters[0][1].keys())

    def test_parse_cmdline_detector_args(self):
        self.assertRaises(ValueError, parse_cmdline_detector_args, None)
        self.assertRaises(AttributeError, parse_cmdline_detector_args, object())
        self.assertRaises(ValueError, parse_cmdline_detector_args, "")
        self.assertEqual(('fancydetector', {}), parse_cmdline_detector_args("fancydetector"))
        self.assertEqual(('fancydetector', {"opt":"val"}), parse_cmdline_detector_args("fancydetector,opt:val"))
