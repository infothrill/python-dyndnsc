# -*- coding: utf-8 -*-

import unittest
import logging
from time import sleep
from multiprocessing import Process

from bottle import Bottle, run, response, route, request

import dyndnsc


@route('/nic/update')
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
        run(self, host=self.host, port=self.port, debug=True, quiet=False)

    def start(self):
        self.process = Process(target=self.run)
        self.process.start()
        sleep(1)

    def stop(self):
        self.process.terminate()
        self.process = None

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


class UpdaterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Start local server
        """
        cls.server = DyndnsApp('localhost', 8000)
        cls.url = "http://localhost:8000/nic/update"
        cls.server.start()

    def test_updater_interfaces(self):
        for cls in dyndnsc.updater.UpdateProtocol.__subclasses__():
            self.assertTrue(hasattr(cls, 'configuration_key'))
            self.assertTrue(hasattr(cls, 'updateUrl'))

    def test_dummy(self):
        NAME = "dummy"
        theip = "127.0.0.1"
        self.assertEqual(NAME, dyndnsc.updater.UpdateProtocolDummy.configuration_key())
        self.assertEqual(str, type(dyndnsc.updater.UpdateProtocolDummy.updateUrl()))
        updater = dyndnsc.updater.UpdateProtocolDummy()
        self.assertEqual(theip, updater.update(theip))
        updater.emit("test")

    def test_noip(self):
        NAME = "noip"
        theip = "127.0.0.2"
        options = {"hostname": "example.com", "userid": "dummy", "password": "1234"}
        dyndnsc.updater.UpdateProtocolNoip.updateurl = self.url
        self.assertEqual(NAME, dyndnsc.updater.UpdateProtocolNoip.configuration_key())
        self.assertEqual(str, type(dyndnsc.updater.UpdateProtocolNoip.updateUrl()))
        updater = dyndnsc.updater.UpdateProtocolNoip(options)
        res = updater.update(theip)
        self.assertEqual(theip, res)
        updater.emit("test")

    @classmethod
    def tearDownClass(cls):
        """
        Stop local server.
        """
        cls.server.stop()


class DynDnscTestCases(unittest.TestCase):
    def setUp(self):
        logging.info("TestCases are being initialized")
        unittest.TestCase.setUp(self)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

#     def test_version(self):
#         import pkg_resources
#         print(pkg_resources.get_distribution("dyndnsc").version)  # pylint: disable=E1103

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
        logging.basicConfig()
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
