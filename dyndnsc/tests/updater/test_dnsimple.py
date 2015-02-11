# -*- coding: utf-8 -*-
"""
Tests for dnsimple updater. Since we rely on an external library implementing
the actual interfacing with the remote service, the tests in here merely check
the behavior of the Dyndnsc wrapper class.
"""

import unittest

try:
    import unittest.mock as mock
except ImportError:
    import mock

import sys

sys.modules['dnsimple_dyndns'] = mock.Mock()


class TestDnsimpleUpdater(unittest.TestCase):
    def test_mocked_dnsimple(self):
        from dyndnsc.updater.dnsimple import UpdateProtocolDnsimple
        theip = "127.0.0.1"
        self.assertEqual("dnsimple", UpdateProtocolDnsimple.configuration_key())
        upd = UpdateProtocolDnsimple(hostname="dnsimple_record.example.com", key="1234")
        upd.handler.update_record.return_value = theip
        self.assertEqual(theip, upd.update(theip))
        upd.handler.update_record.assert_called_once_with(name="dnsimple_record", address=theip)
