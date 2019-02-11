# -*- coding: utf-8 -*-

"""Tests for duckdns."""

import unittest
from time import sleep
from multiprocessing import Process
from random import randint

from bottle import Bottle, run, response, request


def nicupdate():
    """Return fake update response. Implemented as a bottle callback."""
    # print(dict(request.query))
    arg_hostname = request.query.domains
    arg_token = request.query.token
    arg_myip = request.query.ip
    assert len(arg_hostname) > 0  # noqa: @assert_used
    # duckdns doesn't want fqdns:
    assert "." not in arg_hostname, "hostname must not contain dots"  # noqa: @assert_used
    assert len(arg_token) > 0  # noqa: @assert_used
    # duckdns allows empty IP:
    assert len(arg_myip) >= 0  # noqa: @assert_used
    response.content_type = "text/plain; charset=utf-8"
    return str("OK %s" % arg_myip)


class DuckdnsApp(Bottle):
    """Minimal http server that resembles an actual duckdns service."""

    def __init__(self, host="localhost", port=8000):
        """Initialize."""
        super(DuckdnsApp, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.route(path="/update", callback=nicupdate)

    def _bottle_run(self):
        run(self, host=self.host, port=self.port, debug=False, quiet=True)

    def start(self):
        """Start the server subprocess."""
        self.process = Process(target=self._bottle_run)
        self.process.start()
        # even though I have a super fast quad core cpu, this is not working
        # consistently if we don't sleep here!
        sleep(3.5)

    def stop(self):
        """Stop the server subprocess."""
        self.process.terminate()
        self.process = None
        # sleep(1)


class TestDuckdnsBottleServer(unittest.TestCase):
    """Test cases for Duckdns."""

    def setUp(self):
        """Start local server."""
        portnumber = randint(8000, 8900)  # noqa: S311
        self.server = DuckdnsApp("127.0.0.1", portnumber)
        self.url = "http://127.0.0.1:%i/update" % portnumber
        self.server.start()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """Stop local server."""
        self.server.stop()
        self.server = None
        unittest.TestCase.tearDown(self)

    def test_duckdns(self):
        """Run tests for duckdns."""
        from dyndnsc.updater import duckdns
        NAME = "duckdns"
        self.assertEqual(
            NAME, duckdns.UpdateProtocolDuckdns.configuration_key)

        theip = "127.0.0.1"
        options = {
            "hostname": "duckdns.example.com",
            "token": "dummy",
            "url": self.url
        }
        updater = duckdns.UpdateProtocolDuckdns(**options)
        # normal IP test:
        self.assertEqual(theip, updater.update(theip))

        # empty/no IP test:
        self.assertEqual(None, updater.update(None))


if __name__ == "__main__":
    DuckdnsApp("localhost", 8000).run()
