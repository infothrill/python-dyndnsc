# -*- coding: utf-8 -*-

import unittest
import logging
import dyndnsc


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

    def test_iface(self):
        NAME = "iface"
        self.assertEqual(NAME, dyndnsc.detector.IPDetector_Iface.getName())
        detector = dyndnsc.detector.IPDetector_Iface()
        self.assertTrue(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        #self.assertNotEqual(None, detector.getCurrentValue())

    def test_teredo(self):
        NAME = "teredo"
        self.assertEqual(NAME, dyndnsc.detector.IPDetector_Teredo.getName())
        detector = dyndnsc.detector.IPDetector_Teredo()
        self.assertTrue(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        #self.assertNotEqual(None, detector.getCurrentValue())

    def test_webcheck(self):
        NAME = "webcheck"
        self.assertEqual(NAME, dyndnsc.detector.IPDetector_WebCheck.getName())
        detector = dyndnsc.detector.IPDetector_WebCheck()
        self.assertFalse(detector.canDetectOffline())
        self.assertEqual(NAME, detector.getName())
        self.assertEqual(None, detector.getCurrentValue())
        self.assertTrue(type(detector.detect()) in (type(None), str))
        #self.assertNotEqual(None, detector.getCurrentValue())


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


