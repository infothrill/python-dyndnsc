# -*- coding: utf-8 -*-

import unittest
from time import sleep
from multiprocessing import Process

from bottle import Bottle, run, response, request


def nicupdate():
    arg_hostname = request.query.domains
    arg_token = request.query.token
    arg_myip = request.query.ip
    assert len(arg_hostname) > 0
    assert len(arg_token) > 0
    assert len(arg_myip) > 0
    response.content_type = 'text/plain; charset=utf-8'
    return str("good %s" % arg_myip)


class DuckdnsApp(Bottle):

    """
    A minimal http server that resembles an actual duckdns service
    """

    def __init__(self, host='localhost', port=8000):
        super(DuckdnsApp, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.route(path='/update', callback=nicupdate)

    def run(self):
        run(self, host=self.host, port=self.port, debug=False, quiet=True)

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        # even though I have a super fast quad core cpu, this is not working
        # consistently if we don't sleep here!
        sleep(3.5)

    def stop(self):
        self.process.terminate()
        self.process = None
        # sleep(1)

    @property
    def url(self):
        return 'http://%s:%s' % (self.host, str(self.port))


class TestDuckdns2BottleServer(unittest.TestCase):

    def setUp(self):
        """
        Start local server
        """
        import random
        portnumber = random.randint(8000, 8900)
        self.server = DuckdnsApp('127.0.0.1', portnumber)
        self.url = "http://127.0.0.1:%i/update" % portnumber
        self.server.start()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """
        Stop local server.
        """
        self.server.stop()
        self.server = None
        unittest.TestCase.tearDown(self)

    def test_dyndns2(self):
        import dyndnsc.updater.duckdns as duckdns
        NAME = "duckdns"
        theip = "127.0.0.1"
        options = {"hostname": "duckdns.example.com",
                   "token": "dummy",
                   "url": self.url
                   }
        self.assertEqual(
            NAME, duckdns.UpdateProtocolDuckdns.configuration_key())
        updater = duckdns.UpdateProtocolDuckdns(**options)
        self.assertEqual(str, type(updater.url()))
        self.assertEqual(self.url, updater.url())
        res = updater.update(theip)
        self.assertEqual(theip, res)


if __name__ == '__main__':
    DuckdnsApp('localhost', 8000).run()
