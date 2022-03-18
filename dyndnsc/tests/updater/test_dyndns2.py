# -*- coding: utf-8 -*-

"""Tests for dyndns2."""

import unittest

import responses


class TestDyndns2(unittest.TestCase):
    """Test cases for Dyndns2."""

    def setUp(self):
        """Run setup."""
        self.url = "https://dyndns.example.com/nic/update"
        from responses import matchers
        responses.add(
            responses.GET,
            self.url,
            match=[matchers.query_string_matcher("myip=127.0.0.1&hostname=dyndns.example.com")],
            body="good 127.0.0.1",
            status=200,
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """Teardown."""
        unittest.TestCase.tearDown(self)

    @responses.activate
    def test_dyndns2(self):
        """Run tests."""
        from dyndnsc.updater import dyndns2
        NAME = "dyndns2"
        theip = "127.0.0.1"
        options = {
            "hostname": "dyndns.example.com",
            "userid": "dummy", "password": "1234",
            "url": self.url
        }
        self.assertTrue(
            NAME == dyndns2.UpdateProtocolDyndns2.configuration_key)
        self.assertEqual(
            NAME, dyndns2.UpdateProtocolDyndns2.configuration_key)
        updater = dyndns2.UpdateProtocolDyndns2(**options)
        res = updater.update(theip)
        self.assertEqual(theip, res)
