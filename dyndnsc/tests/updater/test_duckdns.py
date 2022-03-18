# -*- coding: utf-8 -*-

"""Tests for duckdns."""

import unittest

import responses


class TestDuckdns(unittest.TestCase):
    """Test cases for Duckdns."""

    def setUp(self):
        """Run setup."""
        from responses import matchers
        responses.add(
            responses.GET,
            "https://www.duckdns.org/update",
            match=[matchers.query_string_matcher("domains=duckdns&token=dummy&ip=127.0.0.1")],
            body="OK 127.0.0.1",
            status=200,
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
        responses.add(
            responses.GET,
            "https://www.duckdns.org/update",
            match=[matchers.query_string_matcher("domains=duckdns&token=dummy&ip=")],
            body="OK",
            status=200,
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """Teardown."""
        unittest.TestCase.tearDown(self)

    @responses.activate
    def test_duckdns(self):
        """Run tests for duckdns."""
        from dyndnsc.updater import duckdns
        NAME = "duckdns"
        self.assertEqual(
            NAME, duckdns.UpdateProtocolDuckdns.configuration_key)

        options = {
            "hostname": "duckdns.example.com",
            "token": "dummy",
            "url": "https://www.duckdns.org/update"
        }
        updater = duckdns.UpdateProtocolDuckdns(**options)
        # normal IP test:
        theip = "127.0.0.1"
        self.assertEqual(theip, updater.update(theip))

        # empty/no IP test:
        self.assertEqual(None, updater.update(None))
