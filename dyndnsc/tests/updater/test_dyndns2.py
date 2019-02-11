# -*- coding: utf-8 -*-

"""Tests for dyndns2."""

import unittest
from time import sleep
from multiprocessing import Process
from random import randint

from bottle import Bottle, run, response, request


def nicupdate():
    """Return fake update response. Implemented as a bottle callback."""
    arg_hostname = request.query.hostname
    arg_myip = request.query.myip
    assert len(arg_hostname) > 0  # noqa: @assert_used
    assert len(arg_myip) > 0  # noqa: @assert_used
    response.content_type = "text/plain; charset=utf-8"
    return str("good %s" % arg_myip)


class Dyndns2App(Bottle):
    """A minimal http server that resembles an actual dyndns service."""

    def __init__(self, host="localhost", port=8000):
        """Initialize."""
        super(Dyndns2App, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.route(path="/nic/update", callback=nicupdate)

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


class TestDyndns2BottleServer(unittest.TestCase):
    """Test cases for Dyndns2."""

    def setUp(self):
        """Start local server."""
        portnumber = randint(8000, 8900)  # noqa: S311
        self.server = Dyndns2App("127.0.0.1", portnumber)
        self.url = "http://127.0.0.1:%i/nic/update" % portnumber
        self.server.start()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """Stop local server."""
        self.server.stop()
        self.server = None
        unittest.TestCase.tearDown(self)

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


if __name__ == "__main__":
    Dyndns2App("localhost", 8000).run()
