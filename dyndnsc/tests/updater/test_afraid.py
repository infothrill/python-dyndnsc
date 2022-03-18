# -*- coding: utf-8 -*-

"""Tests for afraid."""

import unittest

import responses


class TestAfraid(unittest.TestCase):
    """Test cases for Afraid."""

    def setUp(self):
        """Run setup."""
        responses.add(
            responses.GET,
            "https://freedns.afraid.org/dynamic/update.php?sdvnkdnvv",
            body="Updated 1 host(s) foo.example.com to 127.0.0.1 in 0.178 seconds",
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
        from responses import matchers
        responses.add(
            responses.GET,
            "https://freedns.afraid.org/api/",
            match=[matchers.query_string_matcher("action=getdyndns&sha=8637d0e37ad5ec987709e5bd868131d6cf972f69")],
            body="dummyhostname.example.com|127.0.0.2|https://freedns.afraid.org/dynamic/update.php?sdvnkdnvv\r\n",
            headers={"Content-Type": "text/plain; charset=utf-8"}
        )
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """Teardown."""
        unittest.TestCase.tearDown(self)

    @responses.activate
    def test_afraid(self):
        """Run tests."""
        from dyndnsc.updater import afraid
        NAME = "afraid"
        options = {
            "hostname": "dummyhostname.example.com",
            "userid": "dummy",
            "password": "1234"
        }
        self.assertEqual(NAME, afraid.UpdateProtocolAfraid.configuration_key)
        updater = afraid.UpdateProtocolAfraid(**options)
        res = updater.update()
        self.assertEqual("127.0.0.1", res)
