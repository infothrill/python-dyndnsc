# -*- coding: utf-8 -*-

import unittest
from time import sleep
from multiprocessing import Process

from bottle import Bottle, run, response, request


def nicupdate():
    arg_hostname = request.query.hostname
    arg_myip = request.query.myip
    assert len(arg_hostname) > 0
    assert len(arg_myip) > 0
    response.content_type = 'text/plain; charset=utf-8'
    return str("good %s" % arg_myip)


class Dyndns2App(Bottle):

    """
    A minimal http server that resembles an actual dyndns service
    """

    def __init__(self, host='localhost', port=8000):
        super(Dyndns2App, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.route(path='/nic/update', callback=nicupdate)

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


class TestDyndns2BottleServer(unittest.TestCase):

    def setUp(self):
        """
        Start local server
        """
        import random
        portnumber = random.randint(8000, 8900)
        self.server = Dyndns2App('127.0.0.1', portnumber)
        self.url = "http://127.0.0.1:%i/nic/update" % portnumber
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
        import dyndnsc.updater.dyndns2 as dyndns2
        NAME = "dyndns2"
        theip = "127.0.0.1"
        options = {"hostname": "dyndns.example.com",
                   "userid": "dummy", "password": "1234",
                   "url": self.url
                   }
        self.assertEqual(
            NAME, dyndns2.UpdateProtocolDyndns2.configuration_key())
        updater = dyndns2.UpdateProtocolDyndns2(**options)
        self.assertEqual(str, type(updater.url()))
        self.assertEqual(self.url, updater.url())
        res = updater.update(theip)
        self.assertEqual(theip, res)


if __name__ == '__main__':
    Dyndns2App('localhost', 8000).run()
