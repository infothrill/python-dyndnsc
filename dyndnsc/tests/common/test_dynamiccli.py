# -*- coding: utf-8 -*-

import unittest

from dyndnsc.common.dynamiccli import parse_cmdline_args, DynamicCliMixin


class Dummy(DynamicCliMixin):
    def __init__(self, userid, password):
        pass

    @staticmethod
    def configuration_key():
        return "dummy"

    @staticmethod
    def configuration_key_prefix():
        return "foo"


class TestDynamicCli(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_cmdline_updater_args(self):
        self.assertRaises(TypeError, parse_cmdline_args, None)
        self.assertRaises(ValueError, parse_cmdline_args, None, None)
        self.assertRaises(NotImplementedError, parse_cmdline_args, object(), [DynamicCliMixin])
        self.assertEqual({}, parse_cmdline_args(object(), []))

        # test that a sample valid config parses:
        from argparse import Namespace
        args = Namespace()
        args.foo_dummy = True
        args.foo_dummy_userid = "bob"
        args.foo_dummy_password = "******"

        parsed = parse_cmdline_args(args, [Dummy])
        self.assertEqual(1, len(parsed))
        self.assertTrue(isinstance(parsed, dict))
        self.assertTrue('foo' in parsed)
        self.assertTrue(isinstance(parsed['foo'], list))
        self.assertEqual(1, len(parsed['foo']))
        self.assertTrue(isinstance(parsed['foo'][0], tuple))
        self.assertEqual(parsed['foo'][0][0], 'dummy')
        self.assertTrue(isinstance(parsed['foo'][0][1], dict))
        self.assertTrue("userid" in parsed['foo'][0][1].keys())
        self.assertTrue("password" in parsed['foo'][0][1].keys())
