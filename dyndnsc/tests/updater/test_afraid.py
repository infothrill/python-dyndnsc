# -*- coding: utf-8 -*-

import unittest
from time import sleep
from multiprocessing import Process
# import logging

from bottle import Bottle, run, response, request

# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s  %(message)s')


class AfraidApp(Bottle):
    """
    A minimal http server that resembles an actual freedns.afraid.org service
    """
    def __init__(self, host='localhost', port=8000):
        super(AfraidApp, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.route(path='/api/', callback=self.api)
        self.route(path='/dynamic/update.php', callback=self.update)

    def api(self):
        arg_action = request.query.action
        arg_sha = request.query.sha
        assert arg_action == "getdyndns"
        assert len(arg_sha) > 0
        response.content_type = 'text/plain; charset=utf-8'
        return """dummyhostname.example.com|127.0.0.2|%s/dynamic/update.php?sdvnkdnvv\r\n""" % self.url

    def update(self):
        response.content_type = 'text/plain; charset=utf-8'
        # sample text as returned after a successful update:
        return """Updated 1 host(s) foo.example.com to 127.0.0.1 in 0.178 seconds"""

    def run(self, debug=False, quiet=True):
        run(self, host=self.host, port=self.port, debug=debug, quiet=quiet)

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        # even though I have a super fast quad core cpu, this is not working
        # consistently if we don't sleep here!
        sleep(4.5)

    def stop(self):
        self.process.terminate()
        self.process = None

    @property
    def url(self):
        return 'http://%s:%s' % (self.host, str(self.port))


class TestAfraidBottleServer(unittest.TestCase):
    def setUp(self):
        """
        Start local fake test server
        """
        import random
        portnumber = random.randint(8000, 8900)
        self.server = AfraidApp('127.0.0.1', portnumber)
        self.url = "http://127.0.0.1:%i/api/" % portnumber
        self.server.start()
        unittest.TestCase.setUp(self)

    def tearDown(self):
        """
        Stop local server.
        """
        self.server.stop()
        self.server = None
        unittest.TestCase.tearDown(self)

    def test_afraid(self):
        import dyndnsc.updater.afraid as afraid
        NAME = "afraid"
        options = {
            "hostname": "dummyhostname.example.com",
            "userid": "dummy",
            "password": "1234",
            "url": self.url
        }
        self.assertEqual(NAME, afraid.UpdateProtocolAfraid.configuration_key())
        updater = afraid.UpdateProtocolAfraid(**options)
        res = updater.update()
        self.assertEqual("127.0.0.1", res)

if __name__ == '__main__':
    AfraidApp('localhost', 8000).run(debug=True, quiet=False)
