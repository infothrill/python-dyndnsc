# -*- coding: utf-8 -*-

import unittest
from time import sleep
from multiprocessing import Process
#import logging

from bottle import Bottle, run, response, request

#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s  %(message)s')


class AfraidApp(Bottle):
    '''
    A minimal http server that resembles an actual freedns.afraid.org service
    '''
    def __init__(self, host='localhost', port=8000):
        super(AfraidApp, self).__init__()
        self.host = host
        self.port = port
        self.process = None
        self.route(path='/api/', callback=self.api)

    def api(self):
        arg_action = request.query.action
        arg_sha = request.query.sha
        assert arg_action == "getdyndns"
        assert len(arg_sha) > 0
        response.content_type = 'text/plain; charset=utf-8'
        return """dummyhostname.example.com|127.0.0.2|%s/dynamic/update.php?sdvnkdnvv\r\n""" % self.url

    def run(self, debug=False, quiet=True):
        run(self, host=self.host, port=self.port, debug=debug, quiet=quiet)

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        # even though I have a super fast quad core cpu, this is not working
        # consistently if we don't sleep here!
        sleep(3.5)

    def stop(self):
        self.process.terminate()
        self.process = None
        #sleep(1)

    @property
    def url(self):
        return 'http://%s:%s' % (self.host, str(self.port))


class TestAfraid2BottleServer(unittest.TestCase):
    def setUp(self):
        """
        Start local server
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
        import dyndnsc.updater.afraid
        NAME = "afraid"
        options = {
                   "hostname": "afraid.example.com",
                   "userid": "dummy",
                   "password": "1234",
                   "url": self.url
                   }
        self.assertEqual(NAME, dyndnsc.updater.afraid.UpdateProtocolAfraid.configuration_key())
        updater = dyndnsc.updater.afraid.UpdateProtocolAfraid(options)
        res = updater.update()
        #self.assertEqual(theip, res)

if __name__ == '__main__':
    AfraidApp('localhost', 8000).run(debug=True, quiet=False)
