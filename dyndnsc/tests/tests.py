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
    #assert arg_hash in sample_data
    response.content_type = 'text/plain; charset=utf-8'
    return str("good %s" % arg_myip)


class DyndnsApp(Bottle):
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


class DetectorTests(unittest.TestCase):
    def test_detector_interfaces(self):
        for cls in dyndnsc.detector.IPDetector.__subclasses__():
            self.assertTrue(hasattr(cls, 'getName'))

    def test_dns(self):
        NAME = "dns"
        self.assertEqual(NAME, dyndnsc.detector.IPDetector_DNS.getName())
        detector = dyndnsc.detector.IPDetector_DNS("localhost")
        self.assertFalse(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1"))
        self.assertTrue(detector.getCurrentValue() in ("::1", "127.0.0.1"))
        detector.emit("test")

    def test_command(self):
        NAME = "command"
        cmd = "echo 127.0.0.1"
        self.assertEqual(NAME, dyndnsc.detector.IPDetector_Command.getName())
        detector = dyndnsc.detector.IPDetector_Command({"command": cmd})
        self.assertFalse(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        self.assertTrue(detector.detect() in ("::1", "127.0.0.1"))
        self.assertTrue(detector.getCurrentValue() in ("::1", "127.0.0.1"))
        detector.emit("test")

    def test_iface(self):
        NAME = "iface"
        self.assertEqual(NAME, dyndnsc.detector.IPDetector_Iface.getName())
        detector = dyndnsc.detector.IPDetector_Iface()
        self.assertTrue(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        #self.assertNotEqual(None, detector.getCurrentValue())
        detector.emit("test")

    def test_teredo(self):
        NAME = "teredo"
        self.assertEqual(NAME, dyndnsc.detector.IPDetector_Teredo.getName())
        detector = dyndnsc.detector.IPDetector_Teredo()
        self.assertTrue(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        #self.assertNotEqual(None, detector.getCurrentValue())
        detector.emit("test")

    def test_webcheck(self):
        NAME = "webcheck"
        self.assertEqual(NAME, dyndnsc.detector.IPDetector_WebCheck.getName())
        detector = dyndnsc.detector.IPDetector_WebCheck()
        self.assertFalse(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        #self.assertNotEqual(None, detector.getCurrentValue())
        detector.emit("test")


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


class NoipTest(BottleServerTest):

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


class DynDnscTestCases(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def test_commanddetector(self):
        det = dyndnsc.detector.IPDetector_Command(options={'command': 'echo "127.0.0.1"'})
        self.assertEqual("127.0.0.1", det.detect())
        det = dyndnsc.detector.IPDetector_Command(options={'command': 'echo "127.0.0.2"'})
        self.assertEqual("127.0.0.2", det.detect())

    def test_teredo(self):
        # constructor: test invalid options
        det = dyndnsc.detector.IPDetector_Teredo(options={'iface': 'tun0'})
        logging.info(det.detect())
        # self.assertEquals(type(d.detect()), type(''))

    def donttest_update_noip(self):
        logging.basicConfig()
        config = {}
        config['hostname'] = "dyndnsc.no-ip.biz"
        config['userid'] = "example"
        config['password'] = "foobar"
        config['protocol'] = "noip"
        config['method'] = "random"
        config['sleeptime'] = 60
        dyndnsclient = dyndnsc.getDynDnsClientForConfig(config)
        self.assertTrue(dyndnsclient.needsCheck())

    def test_update_dummy(self):
        config = {}
        config['hostname'] = "dyndnsc.no-ip.biz"
        config['userid'] = "example"
        config['password'] = "foobar"
        config['protocol'] = "dummy"
        config['method'] = "random"
        config['sleeptime'] = 60
        dyndnsclient = dyndnsc.getDynDnsClientForConfig(config)
        self.assertTrue(dyndnsclient.needsCheck())
        dyndnsclient.needsForcedCheck()
        dyndnsclient.check()
        dyndnsclient.sync()
        dyndnsclient.stateHasChanged()

if __name__ == '__main__':
    DyndnsApp('localhost', 8000).run()
