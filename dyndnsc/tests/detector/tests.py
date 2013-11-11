# -*- coding: utf-8 -*-

import unittest
import logging

import dyndnsc

logging.basicConfig(level=logging.DEBUG)


class DetectorTests(unittest.TestCase):
    def test_detector_interfaces(self):
        for cls in dyndnsc.detector.IPDetector.__subclasses__():
            self.assertTrue(hasattr(cls, 'getName'))
        for cls in dyndnsc.detector.detectorClasses():
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
