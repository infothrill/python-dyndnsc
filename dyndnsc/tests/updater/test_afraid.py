# -*- coding: utf-8 -*-

"""Tests for afraid."""

import unittest
from multiprocessing import Process
from random import randint
from time import sleep

from bottle import Bottle, run, response, request


class AfraidApp(Bottle):
    """A minimal http server that resembles an actual freedns.afraid.org service."""

    def __init__(self, host="localhost", port=8000):
        """Initiliaze."""
        super(AfraidApp, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.route(path="/api/", callback=self.api)
        self.route(path="/dynamic/update.php", callback=self.update)

    def api(self):
        """Return fake api response. Implemented as a bottle callback."""
        arg_action = request.query.action
        arg_sha = request.query.sha
        assert arg_action == "getdyndns"  # noqa: @assert_used
        assert len(arg_sha) > 0  # noqa: @assert_used
        response.content_type = "text/plain; charset=utf-8"
        return """dummyhostname.example.com|127.0.0.2|%s/dynamic/update.php?sdvnkdnvv\r\n""" % self.url

    def update(self):
        """Return fake update response. Implemented as a bottle callback."""
        response.content_type = "text/plain; charset=utf-8"
        # sample text as returned after a successful update:
        return """Updated 1 host(s) foo.example.com to 127.0.0.1 in 0.178 seconds"""

    def _bottle_run(self, debug=False, quiet=True):
        run(self, host=self.host, port=self.port, debug=debug, quiet=quiet)

    def start(self):
        """Start the server subprocess."""
        self.process = Process(target=self._bottle_run)
        self.process.start()
        # even though I have a super fast quad core cpu, this is not working
        # consistently if we don't sleep here!
        sleep(4.5)

    def stop(self):
        """Start the server subprocess."""
        self.process.terminate()
        self.process = None

    @property
    def url(self):
        """Return URL of this server."""
        return "http://%s:%s" % (self.host, str(self.port))


class TestAfraidBottleServer(unittest.TestCase):
    """Test cases for Afraid."""

    def setUp(self):
        """Start local test server."""
        portnumber = randint(8000, 8900)  # noqa: S311
        self.server = AfraidApp("127.0.0.1", portnumber)
        self.url = "http://127.0.0.1:%i/api/" % portnumber
        self.server.start()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """Stop local server."""
        self.server.stop()
        self.server = None
        unittest.TestCase.tearDown(self)

    def test_afraid(self):
        """Run tests."""
        from dyndnsc.updater import afraid
        NAME = "afraid"
        options = {
            "hostname": "dummyhostname.example.com",
            "userid": "dummy",
            "password": "1234",
            "url": self.url
        }
        self.assertEqual(NAME, afraid.UpdateProtocolAfraid.configuration_key)
        updater = afraid.UpdateProtocolAfraid(**options)
        res = updater.update()
        self.assertEqual("127.0.0.1", res)


if __name__ == "__main__":
    AfraidApp("localhost", 8000).run(debug=True, quiet=False)
