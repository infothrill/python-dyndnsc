# -*- coding: utf-8 -*-

import unittest

import dyndnsc


def get_valid_updater():
    from dyndnsc.updater.dummy import UpdateProtocolDummy
    return UpdateProtocolDummy(hostname="example.com")


def get_valid_detector():
    from dyndnsc.detector.null import IPDetector_Null
    return IPDetector_Null()


class TestDynDnsClient(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_dyndnsclient_init_args(self):
        # at least a valid updater must be provided:
        self.assertRaises(ValueError, dyndnsc.DynDnsClient)
        self.assertRaises(ValueError, dyndnsc.DynDnsClient, updater=1)
        self.assertTrue(isinstance(dyndnsc.DynDnsClient(updater=get_valid_updater()), dyndnsc.DynDnsClient))

        # a detector is optional but must be of correct type:
        self.assertRaises(ValueError, dyndnsc.DynDnsClient, updater=get_valid_updater(), detector=1)
        client = dyndnsc.DynDnsClient(updater=get_valid_updater(), detector=get_valid_detector())
        self.assertTrue(isinstance(client, dyndnsc.DynDnsClient))

    def test_dyndnsclient_factory(self):
        # the type of these exceptions is not formally required,
        # but we want to have some basic form of argument validity checking
        # Note: we prefer ValueError for semantically wrong options
        self.assertRaises(TypeError, dyndnsc.getDynDnsClientForConfig, None)
        self.assertRaises(ValueError, dyndnsc.getDynDnsClientForConfig, {})
        self.assertRaises(ValueError, dyndnsc.getDynDnsClientForConfig,
                          {'updater': ()})

        # create a dummy config:
        config = {}
        config['interval'] = 10
        config['detector'] = (("random", {}),)
        config['updater'] = (("dummy", {'hostname': "example.com"}),)
        dyndnsclient = dyndnsc.getDynDnsClientForConfig(config)
        self.assertEqual(dyndnsclient.detector.af(), dyndnsclient.dns.af())
        self.assertTrue(dyndnsclient.needs_check())
        dyndnsclient.needs_sync()
        dyndnsclient.check()
        dyndnsclient.sync()
        dyndnsclient.has_state_changed()
