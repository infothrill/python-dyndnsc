# -*- coding: utf-8 -*-

import unittest
import logging
from time import sleep
from multiprocessing import Process

from bottle import Bottle, run, response, request

import dyndnsc

logging.basicConfig(level=logging.DEBUG)


def nicupdate():
    arg_hostname = request.query.hostname
    arg_myip = request.query.myip
    assert len(arg_hostname) > 0
    assert len(arg_myip) > 0
    response.content_type = 'text/plain; charset=utf-8'
    return str("good %s" % arg_myip)


class DyndnsApp(Bottle):
    '''
    A minimal http server that resembles an actual dyndns service
    '''
    def __init__(self, host='localhost', port=8000):
        super(DyndnsApp, self).__init__()
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
        #sleep(1)

    @property
    def url(self):
        return 'http://{}:{}'.format(self.host, self.port)


class AUpdaterTests(unittest.TestCase):

    def test_updater_interfaces(self):
        from dyndnsc.updater import updaterClasses
        for c, cls in enumerate(updaterClasses()):
            self.assertTrue(hasattr(cls, 'configuration_key'))
            self.assertTrue(hasattr(cls, 'updateUrl'))
        self.assertTrue(c > 0)

    def test_dummy(self):
        NAME = "dummy"
        theip = "127.0.0.1"
        self.assertEqual(NAME, dyndnsc.updater.UpdateProtocolDummy.configuration_key())
        updater = dyndnsc.updater.UpdateProtocolDummy()
        self.assertEqual(str, type(updater.updateUrl()))
        self.assertEqual(theip, updater.update(theip))


class BottleServerTest(unittest.TestCase):
    def setUp(self):
        """
        Start local server
        """
        import random
        portnumber = random.randint(8000, 8900)
        self.server = DyndnsApp('127.0.0.1', portnumber)
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


class UpdaterTests(BottleServerTest):

    def test_noip(self):
        NAME = "noip"
        theip = "127.0.0.1"
        options = {"hostname": "no-ip.example.com", "userid": "dummy", "password": "1234"}
        self.assertEqual(NAME, dyndnsc.updater.UpdateProtocolNoip.configuration_key())
        updater = dyndnsc.updater.UpdateProtocolNoip(options)
        updater.updateurl = self.url
        self.assertEqual(str, type(updater.updateUrl()))
        self.assertEqual(self.url, updater.updateUrl())
        res = updater.update(theip)
        self.assertEqual(theip, res)

    def test_dyndns(self):
        NAME = "dyndns"
        theip = "127.0.0.1"
        options = {"hostname": "dyndns.example.com", "userid": "dummy", "password": "1234"}
        self.assertEqual(NAME, dyndnsc.updater.UpdateProtocolDyndns.configuration_key())
        updater = dyndnsc.updater.UpdateProtocolDyndns(options)
        updater.updateurl = self.url
        self.assertEqual(str, type(updater.updateUrl()))
        self.assertEqual(self.url, updater.updateUrl())
        res = updater.update(theip)
        self.assertEqual(theip, res)

    def test_nsupdate_info(self):
        NAME = "nsupdate"
        theip = "127.0.0.1"
        options = {"hostname": "nsupdate_info.example.com", "userid": "dummy", "password": "1234"}
        self.assertEqual(NAME, dyndnsc.updater.UpdateProtocolNsUpdate.configuration_key())
        updater = dyndnsc.updater.UpdateProtocolNsUpdate(options)
        updater.updateurl = self.url
        self.assertEqual(str, type(updater.updateUrl()))
        self.assertEqual(self.url, updater.updateUrl())
        res = updater.update(theip)
        self.assertEqual(theip, res)


if __name__ == '__main__':
    DyndnsApp('localhost', 8000).run()
